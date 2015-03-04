# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import (round, floor, zeros, maximum as max_, minimum as min_, logical_not as not_, logical_and as and_, logical_or as or_)

from ..base import *  # noqa
from ..pfam import nb_enf, age_en_mois_benjamin


@reference_formula
class paje(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"PAJE - Ensemble des prestations"
    start_date = date(2004, 1, 1)
    url = "http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/la-prestation-d-accueil-du-jeune-enfant-paje-0"

    def function(self, simulation, period):
        '''
        Prestation d'accueil du jeune enfant
        '''
        period = period.start.offset('first-of', 'month').period('year')
        paje_base = simulation.calculate('paje_base', period)
        paje_nais = simulation.calculate('paje_nais', period)
        paje_clca = simulation.calculate('paje_clca', period)
        paje_clmg = simulation.calculate('paje_clmg', period)
        paje_colca = simulation.calculate('paje_colca', period)

        return period, paje_base + paje_nais + paje_clca + paje_clmg + paje_colca


@reference_formula
class paje_base_temp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de base de la PAJE sans tenir compte d'éventuels cumuls"
    start_date = date(2004, 1, 1)

    def function(self, simulation, period):
        '''
        Prestation d'accueil du jeune enfant - allocation de base
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_holder = simulation.compute('age', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        br_pf = simulation.calculate('br_pf', period)
        isol = simulation.calculate('isol', period)
        biact = simulation.calculate('biact', period)
        smic55_holder = simulation.compute('smic55', period, accept_other_period = True)
        P = simulation.legislation_at(period.start).fam

        # TODO cumul des paje si et seulement si naissance multiples

        # TODO : théorie, il faut comparer les revenus de l'année n-2 à la bmaf de
        # l'année n-2 pour déterminer l'éligibilité avec le cf_seuil. Il faudrait
        # pouvoir déflater les revenus de l'année courante pour en tenir compte.
        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        bmaf = P.af.bmaf
        bmaf2 = P.af.bmaf_n_2

        base = round(P.paje.base.taux * bmaf, 2)
        base2 = round(P.paje.base.taux * bmaf2, 2)

        # L'allocation de base est versée jusqu'au dernier jour du mois civil précédant
        # celui au cours duquel l'enfant atteint l'âge de 3 ans.

        nbenf = nb_enf(age, smic55, 0, P.paje.base.age - 1)

        plaf_tx = (nbenf > 0) + P.paje.base.plaf_tx1 * min_(af_nbenf, 2) + P.paje.base.plaf_tx2 * max_(af_nbenf - 2, 0)
        majo = isol | biact
        plaf = P.paje.base.plaf * plaf_tx + (plaf_tx > 0) * P.paje.base.plaf_maj * majo
        plaf2 = plaf + 12 * base2  # TODO vérifier l'aspect différentielle de la PAJE et le plaf2 de la paje

        paje_base = (nbenf > 0) * ((br_pf < plaf) * base +
                               (br_pf >= plaf) * max_(plaf2 - br_pf, 0) / 12)
        # non cumulabe avec la CF, voir Paje_CumulCf
        return period, 12 * paje_base  # annualisé


@reference_formula
class paje_nais(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de naissance de la PAJE"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2550.xhtml"

    def function(self, simulation, period):
        '''
        Prestation d'accueil du jeune enfant - Allocation de naissance
        '''
        period = period.start.offset('first-of', 'month').period('year')
        agem_holder = simulation.compute('agem', period)
        age_holder = simulation.compute('age', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        br_pf = simulation.calculate('br_pf', period)
        isol = simulation.calculate('isol', period)
        biact = simulation.calculate('biact', period)
        P = simulation.legislation_at(period.start).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        agem = self.split_by_roles(agem_holder, roles = ENFS)

        bmaf = P.af.bmaf
        nais_prime = round(100 * P.paje.nais.prime_tx * bmaf) / 100
        # Versée au 7e mois de grossesse dans l'année
        # donc les enfants concernés sont les enfants qui ont -2 mois
        nbnais = 0
        for age_m in agem.itervalues():
            # nbnais += (age_m == -2) cas mensuel
            nbnais += (age_m >= -2) * (age_m < 10)

        nbaf = 0  # Et on compte le nombre d'enfants AF présents  pour le seul mois de la prime
        for age_m in agem.itervalues():
            nbaf += (age_m >= 10)

        nbenf = nbaf + nbnais  # On ajoute l'enfant à  naître;

        paje_plaf = P.paje.base.plaf

        plaf_tx = (nbenf > 0) + P.paje.base.plaf_tx1 * min_(af_nbenf, 2) + P.paje.base.plaf_tx2 * max_(af_nbenf - 2, 0)
        majo = isol | biact
        plaf = P.paje.base.plaf * plaf_tx + (plaf_tx > 0) * P.paje.base.plaf_maj * majo
        elig = (br_pf <= plaf) * (nbnais != 0)
        nais_brut = nais_prime * elig * (nbnais)
        return period, nais_brut


@reference_formula
class paje_clca(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"PAJE - Complément de libre choix d'activité"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F313.xhtml"

    def function(self, simulation, period):
        """
        Prestation d'accueil du jeune enfant - Complément de libre choix d'activité
        'fam'

        Parameters:
        -----------

        age :  âge en mois
        af_nbenf : nombre d'enfants aus sens des allocations familiales
        paje_base : allocation de base de la PAJE
        inactif : indicatrice d'inactivité
        partiel1 : Salarié: Temps de travail ne dépassant pas 50 % de la durée du travail fixée dans l'entreprise pour les salariés
                   VRP ou non salarié travaillant à temps partiel: Temps de travail ne dépassant pas 76 heures par mois
                      et un revenu professionnel mensuel inférieur ou égal à (smic_8.27*169*85 %)
        partiel2 :  Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
                    VRP ou non salarié travaillant à temps partiel: Temps de travail compris entre 77 et 122 heures par mois et un revenu professionnel mensuel ne dépassant pas
                                                                    (smic_8.27*169*136 %)

        http://www.caf.fr/wps/portal/particuliers/catalogue/metropole/paje
        """
        period = period.start.offset('first-of', 'month').period('year')
        agem_holder = simulation.compute('agem', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        paje_base = simulation.calculate('paje_base', period)
        inactif = simulation.calculate('inactif', period)
        partiel1 = simulation.calculate('partiel1', period)
        partiel2 = simulation.calculate('partiel2', period)
        P = simulation.legislation_at(period.start).fam

        agem = self.split_by_roles(agem_holder, roles = ENFS)

        paje = paje_base >= 0
        # durée de versement :
        # Pour un seul enfant à charge, le CLCA est versé pendant une période de 6 mois (P.paje.clca.duree1)
        # à partir de la naissance ou de la cessation des IJ maternité et paternité.
        # A partir du 2ème enfant, il est versé jusqu’au mois précédant le 3ème anniversaire
        # de l’enfant.

        # Calcul de l'année et mois de naisage_in_months( du cadet
        # TODO: ajuster en fonction de la cessation des IJ etc
        age_m_benjamin = age_en_mois_benjamin(agem)
        condition1 = (af_nbenf == 1) * (age_m_benjamin >= 0) * (age_m_benjamin < P.paje.clca.duree1)
        age_benjamin = floor(age_m_benjamin / 12)
        condition2 = (age_benjamin <= (P.paje.base.age - 1))
        condition = (af_nbenf >= 2) * condition2 + condition1
        paje_clca = (condition * P.af.bmaf) * (
                    (not_(paje)) * (inactif * P.paje.clca.sansab_tx_inactif +
                                partiel1 * P.paje.clca.sansab_tx_partiel1 +
                                partiel2 * P.paje.clca.sansab_tx_partiel2) +
                    (paje) * (inactif * P.paje.clca.avecab_tx_inactif +
                                partiel1 * P.paje.clca.avecab_tx_partiel1 +
                                partiel2 * P.paje.clca.avecab_tx_partiel2))
        return period, 12 * paje_clca  # annualisé


@reference_formula
class paje_clca_taux_plein(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice Clca taux plein"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F313.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        paje_clca = simulation.calculate('paje_clca', period)
        inactif = simulation.calculate('inactif', period)

        return period, (paje_clca > 0) * inactif


@reference_formula
class paje_clca_taux_partiel(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice Clca taux partiel"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F313.xhtml"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        paje_clca = simulation.calculate('paje_clca', period)
        partiel1 = simulation.calculate('partiel1', period)

        return period, (paje_clca > 0) * partiel1


    # TODO gérer les cumuls avec autres revenus et colca voir site caf


@reference_formula
class paje_clmg(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"PAJE - Complément de libre choix du mode de garde"
    start_date = date(2004, 1, 1)
    url = "http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/le-complement-de-libre-choix-du-mode-de-garde"

    def function(self, simulation, period):
        '''
        Prestation d accueil du jeune enfant - Complément de libre choix du mode de garde

        Les conditions

        Vous devez :

            avoir un enfant de moins de 6 ans né, adopté ou recueilli en vue d'adoption à partir du 1er janvier 2004
            employer une assistante maternelle agréée ou une garde à domicile.
            avoir une activité professionnelle minimale
                si vous êtes salarié cette activité doit vous procurer un revenu minimum de :
                    si vous vivez seul : une fois la BMAF
                    si vous vivez en couple  soit 2 fois la BMAF
                si vous êtes non salarié, vous devez être à jour de vos cotisations sociales d'assurance vieillesse

        Vous n'avez pas besoin de justifier d'une activité min_ si vous êtes :

            bénéficiaire de l'allocation aux adultes handicapés (Aah)
            au chômage et bénéficiaire de l'allocation d'insertion ou de l'allocation de solidarité spécifique
            bénéficiaire du Revenu de solidarité active (Rsa), sous certaines conditions de ressources étudiées par votre Caf, et inscrit dans une démarche d'insertion
            étudiant (si vous vivez en couple, vous devez être tous les deux étudiants).

        Autres conditions à remplir : Assistante maternelle agréée     Garde à domicile
        Son salaire brut ne doit pas dépasser par jour de garde et par enfant 5 fois le montant du Smic horaire brut, soit au max 45,00 €.
        Vous ne devez pas bénéficier de l'exonération des cotisations sociales dues pour la personne employée.
        '''
        period = period.start.offset('first-of', 'month').period('year')
        aah_holder = simulation.compute('aah', period)
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period, accept_other_period = True)
        etu_holder = simulation.compute('etu', period)
        sal_holder = simulation.compute('sal', period)
        hsup_holder = simulation.compute('hsup', period)
        concub = simulation.calculate('concub', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        br_pf = simulation.calculate('br_pf', period)
        empl_dir = simulation.calculate('empl_dir', period)
        ass_mat = simulation.calculate('ass_mat', period)
        gar_dom = simulation.calculate('gar_dom', period)
        paje_clca_taux_partiel = simulation.calculate('paje_clca_taux_partiel', period)
        paje_clca_taux_plein = simulation.calculate('paje_clca_taux_plein', period)
        P = simulation.legislation_at(period.start).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        hsup = self.split_by_roles(hsup_holder, roles = [CHEF, PART])
        sal = self.split_by_roles(sal_holder, roles = [CHEF, PART])
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        aah = self.sum_by_entity(aah_holder)

        # condition de revenu minimal

        cond_age_enf = (nb_enf(age, smic55, P.paje.clmg.age1, P.paje.clmg.age2 - 1) > 0)
        cond_sal = (sal[CHEF] + sal[PART] + hsup[CHEF] + hsup[PART] > 12 * P.af.bmaf_n_2 * (1 + concub))
    # TODO:    cond_rpns    =
        cond_act = cond_sal  # | cond_rpns

        cond_nonact = (aah > 0) | (etu[CHEF] & etu[PART])  # | (ass>0)
    #  TODO: RSA insertion, alloc insertion, ass
        elig = cond_age_enf & (cond_act | cond_nonact)
        nbenf = af_nbenf
        seuil1 = P.paje.clmg.seuil11 * (nbenf == 1) + P.paje.clmg.seuil12 * (nbenf >= 2) + max_(nbenf - 2, 0) * P.paje.clmg.seuil1sup
        seuil2 = P.paje.clmg.seuil21 * (nbenf == 1) + P.paje.clmg.seuil22 * (nbenf >= 2) + max_(nbenf - 2, 0) * P.paje.clmg.seuil2sup

    #        Si vous bénéficiez du Clca taux partiel (= vous travaillez entre 50 et 80% de la durée du travail fixée dans l'entreprise),
    #        vous cumulez intégralement le Clca et le Cmg.
    #        Si vous bénéficiez du Clca taux partiel (= vous travaillez à 50% ou moins de la durée
    #        du travail fixée dans l'entreprise), le montant des plafonds Cmg est divisé par 2.
        seuil1 = seuil1 * (1 - .5 * paje_clca_taux_partiel)
        seuil2 = seuil2 * (1 - .5 * paje_clca_taux_partiel)

        clmg = P.af.bmaf * ((nb_enf(age, smic55, 0, P.paje.clmg.age1 - 1) > 0) +
                               0.5 * (nb_enf(age, smic55, P.paje.clmg.age1, P.paje.clmg.age2 - 1) > 0)
                               ) * (
            empl_dir * (
                (br_pf < seuil1) * P.paje.clmg.empl_dir1 +
                ((br_pf >= seuil1) & (br_pf < seuil2)) * P.paje.clmg.empl_dir2 +
                (br_pf >= seuil2) * P.paje.clmg.empl_dir3) +
            ass_mat * (
                (br_pf < seuil1) * P.paje.clmg.ass_mat1 +
                ((br_pf >= seuil1) & (br_pf < seuil2)) * P.paje.clmg.ass_mat2 +
                (br_pf >= seuil2) * P.paje.clmg.ass_mat3) +
            gar_dom * (
                (br_pf < seuil1) * P.paje.clmg.domi1 +
                ((br_pf >= seuil1) & (br_pf < seuil2)) * P.paje.clmg.domi2 +
                (br_pf >= seuil2) * P.paje.clmg.domi3))
        # TODO: connecter avec le crédit d'impôt
        # Si vous bénéficiez du Clca taux plein (= vous ne travaillez plus ou interrompez votre activité professionnelle),
        # vous ne pouvez pas bénéficier du Cmg.
        paje_clmg = elig * not_(paje_clca_taux_plein) * clmg
        # TODO vérfiez les règles de cumul
        return period, 12 * paje_clmg  # annualisé


@reference_formula
class paje_colca(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"PAJE - Complément optionnel de libre choix d'activité"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F15110.xhtml"

    def function(self, simulation, period):
        '''
        Prestation d'accueil du jeune enfant - Complément optionnel de libre choix du mode de garde
        '''
        period = period.start.offset('first-of', 'month').period('year')
        af_nbenf = simulation.calculate('af_nbenf', period)
        agem_holder = simulation.compute('agem', period)
        opt_colca = simulation.calculate('opt_colca', period)
        paje_base = simulation.calculate('paje_base', period)
        P = simulation.legislation_at(period.start).fam

        agem = self.split_by_roles(agem_holder, roles = ENFS)

        age_m_benjamin = age_en_mois_benjamin(agem)
        condition = (age_m_benjamin < 12 * P.paje.colca.age) * (age_m_benjamin >= 0)
        nbenf = af_nbenf
        paje = (paje_base > 0)
        paje_colca = opt_colca * condition * (nbenf >= 3) * P.af.bmaf * (
            (paje) * P.paje.colca.avecab + not_(paje) * P.paje.colca.sansab)
        return period, 12 * paje_colca  # annualisé


    # TODO: cumul avec clca self.colca_tot_m


@reference_formula
class paje_base(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de base de la PAJE"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2552.xhtml"

    def function(self, simulation, period):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        period = period.start.offset('first-of', 'month').period('year')
        paje_base_temp = simulation.calculate('paje_base_temp', period)
        cf_temp = simulation.calculate('cf_temp', period)

        # On regarde ce qui est le plus intéressant pour la famille, chaque mois
        paje_base = (paje_base_temp >= cf_temp) * paje_base_temp
        return period, round(paje_base, 2)


def _afeama(self, age_holder, smic55_holder, ape, af_nbenf, br_pf, P = law.fam):
    '''
    Aide à la famille pour l'emploi d'une assistante maternelle agréée
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    # TODO http://web.archive.org/web/20080205163300/http://www.caf.fr/wps/portal/particuliers/catalogue/metropole/afeama
    # Les seuils sont de 80 et 110 % de l'ARS
    # Vérifier que c'est la même chose pour le clmg

    elig = not_(ape)  # assistante maternelle agréee
    # Vous devez:
    #    faire garder votre enfant de moins de 6 ans par une assistante maternelle agréée dont vous êtes l'employeur
    #    déclarer son embauche à l'Urssaf
    #    lui verser un salaire ne dépassant pas par jour de garde et par enfant 5 fois le montant horaire du Smic, soit au max_ 42,20 €
    #
    # Si vous cessez de travailler et bénéficiez de l'allocation parentale d'éducation, vous ne recevrez plus l'Afeama.
    # Vos enfants doivent être nés avant le 1er janvier 2004.

    # TODO calcul des cotisations urssaf
    #
    nbenf_afeama = nb_enf(age, smic55, P.af.age1, P.afeama.age - 1)
    nbenf = elig * af_nbenf * (nbenf_afeama > 0)

    nb_par_ars = (nbenf == 1 + max_(nbenf - 1, 0) * (1 + P.ars.plaf_enf_supp))
    seuil1 = (P.afeama.mult_seuil1 * P.ars.plaf) * nb_par_ars
    seuil2 = (P.afeama.mult_seuil2 * P.ars.plaf) * nb_par_ars

    afeama = nbenf_afeama * P.af.bmaf * (
            (br_pf < seuil1) * P.afeama.taux_mini +
            ((br_pf >= seuil1) & (br_pf < seuil2)) * P.afeama.taux_median +
            (br_pf >= seuil2) * P.afeama.taux_maxi)
    return 12 * afeama  # annualisé

    # L'AFEAMA comporte 2 volets complémentaires: l'AFEAMA proprement dit qui consiste à prendre en charge les cotisations sociales sur les salaires, d'une part,
    # et une allocation complémentaire versée aux parents, la majoration AFEAMA, d'autre part.
    # Le système de majoration AFEAMA a été modifié au 1er janvier 2001 :
    # Jusqu'en décembre 2000, son montant ne dépendait que de l'âge de l'enfant.
    # Depuis janvier 2001, il dépend également de la catégorie de revenus des parents employeurs (fonction de leur base ressources et du nombre d'enfants qu'ils ont à charge).
    # Parallélement, son plafonnement a été ramené de 100 % à 85 % du salaire net versé à l'assistante maternelle (sauf si ces 85 % sont inférieurs au montant de la majoration la moins élevée, compte tenu de l'âge de l'enfant).
    # La catégorie de revenus des parents employeurs est déterminée par la CAF en fonction de la base ressources du ménage.
    # Le tableau suivant récapitule les montants pris en compte depuis le 1er juillet 2007 pour la détermination du montant maximal de la majoration AFEAMA selon les catégories de revenus :
    # Base ressources du ménage
    #                 1 enfant                      2 enfants             par enfant suppémentaire
    # revenus    inférieurs à 17 593 €             inférieurs à 21 653 €          4060 €
    #            inférieurs à 24 190 €             inférieurs à 29 773 €          5583 €
    #            supérieurs à 24 190 €             supérieurs à 29 773 €          5583 €
    # Montant base ressources 2006, au 1er juillet 2007


def _aged(self, age_holder, smic55_holder, br_pf, ape_taux_partiel, dep_trim, P = law.fam):
    '''
    Allocation garde d'enfant à domicile

    les deux conjoints actif et revenu min requis, jusqu'aux 6 ans de l'enfant né avant le 01/01/2004, emploi d'une garde A DOMICILE
    cette allocation consiste en une prise en charge partielle des charges sociales inhérentes à l'emploi d'une personne à domicile.
    Si vous avez au moins un enfant  de moins de 3 ans gardé au domicile, 2 cas :
    Revenus 2005 > 37 241  € : la CAF prend en charge 50% des charges sociales (plafonné à 1 106 € par trimestre),
    Revenus 2005 < 37 341  € : la CAF prend en charge 75% des charges sociales (plafonné à 1 659 € par trimestre).
    Si vous avez un enfant de plus de 3 ans gardé au domicile (1 seul cas, sans condition de ressources) :
    la CAF prend en charge 50% des charges sociales (plafonné à 553 € par trimestre)
    '''
    # TODO: trimestrialiser
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    nbenf = nb_enf(age, smic55, 0, P.aged.age1 - 1)
    nbenf2 = nb_enf(age, smic55, 0, P.aged.age2 - 1)
    elig1 = (nbenf > 0)
    elig2 = not_(elig1) * (nbenf2 > 0) * ape_taux_partiel
    depenses = 4 * dep_trim  # gérer les dépenses trimestrielles
    aged3 = elig1 * (max_(P.aged.remb_plaf1 - P.aged.remb_taux1 * depenses, 0) * (br_pf > P.aged.revenus_plaf)
       + (br_pf <= P.aged.revenus_plaf) * max_(P.aged.remb_taux2 * depenses - P.aged.remb_plaf1, 0))
    aged6 = elig2 * max_(P.aged.remb_taux2 * depenses - P.aged.remb_plaf2, 0)
    return 12 * (aged3 + aged6)  # annualisé


@reference_formula
class ape_temp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation parentale d'éducation"
    stop_date = date(2004, 1, 1)
    url = "http://fr.wikipedia.org/wiki/Allocation_parentale_d'%C3%A9ducation_en_France"

    def function(self, simulation, period):
        '''
        Allocation parentale d'éducation
        'fam'

        L’allocation parentale d’éducation s’adresse aux parents qui souhaitent arrêter ou
        réduire leur activité pour s’occuper de leurs jeunes enfants, à condition que ceux-ci
        soient nés avant le 01/01/2004. En effet, pour les enfants nés depuis cette date,
        dans le cadre de la Prestation d’Accueil du Jeune Enfant, les parents peuvent bénéficier
        du « complément de libre choix d’activité. »

        Les personnes en couple peuvent toutes deux bénéficier de l’APE à taux plein, mais pas en même temps. En revanche,
        elles peuvent cumuler deux taux partiels, à condition que leur total ne dépasse pas le montant du taux plein.

        TODO: cumul,  adoption, triplés,
        Cumul d'allocations : Cette allocation n'est pas cumulable pour un même ménage avec
        - une autre APE (sauf à taux partiel),
        - ou l'allocation pour jeune enfant (APJE) versée à partir de la naissance,
        - ou le complément familial,
        - ou l'allocation d’adulte handicapé (AAH).
        Enfin, il est à noter que cette allocation n’est pas cumulable avec :
        - une pension d’invalidité ou une retraite ;
        - des indemnités journalières de maladie, de maternité ou d’accident du travail ;
        - des allocations chômage. Il est tout de même possible de demander aux ASSEDIC la suspension de ces dernières pour
          percevoir l’APE.

        L'allocation parentale d'éducation n'est pas soumise à condition de ressources, sauf l’APE à taux partiel pour les
        professions non salariées.
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', accept_other_period = True)
        inactif = simulation.calculate('inactif', period)
        partiel1 = simulation.calculate('partiel1', period)
        partiel2 = simulation.calculate('partiel2', period)
        P = simulation.legislation_at(period.start).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        elig = (nb_enf(age, smic55, 0, P.ape.age - 1) >= 1) & (nb_enf(age, smic55, 0, P.af.age2) >= 2)
        # Inactif
        # Temps partiel 1
        # Salarié:
        # Temps de travail ne dépassant pas 50 % de la durée du travail fixée dans l'entreprise
        # VRP ou non salarié travaillant à temps partiel:
        # Temps de travail ne dépassant pas 76 heures par mois et un revenu professionnel mensuel inférieur ou égal à (smic_8.27*169*85 %)
        # partiel1 = zeros((12,self.taille))

        # Temps partiel 2
        # Salarié:
        # Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
        # Temps de travail compris entre 77 et 122 heures par mois et un revenu professionnel mensuel ne dépassant pas
        #  (smic_8.27*169*136 %)
        ape = elig * (inactif * P.ape.tx_inactif + partiel1 * P.ape.tx_50 + partiel2 * P.ape.tx_80)
        # Cummul APE APJE CF
        return period, 12 * ape  # annualisé


@reference_formula
class apje_temp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation pour le jeune enfant"
    stop_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2552.xhtml"

    def function(self, simulation, period):
        '''
        Allocation pour jeune enfant
        '''
        period = period.start.offset('first-of', 'month').period('year')
        br_pf = simulation.calculate('br_pf', period)
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', accept_other_period = True)
        isol = simulation.calculate('isol', period)
        biact = simulation.calculate('biact', period)
        P = simulation.legislation_at(period.start).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        # TODO: APJE courte voir doc ERF 2006
        nbenf = nb_enf(age, smic55, 0, P.apje.age - 1)
        bmaf = P.af.bmaf
        bmaf_n_2 = P.af.bmaf_n_2
        base = round(P.apje.taux * bmaf, 2)
        base2 = round(P.apje.taux * bmaf_n_2, 2)

        plaf_tx = (nbenf > 0) + P.apje.plaf_tx1 * min_(nbenf, 2) + P.apje.plaf_tx2 * max_(nbenf - 2, 0)
        majo = isol | biact
        plaf = P.apje.plaf * plaf_tx + P.apje.plaf_maj * majo
        plaf2 = plaf + 12 * base2

        apje = (nbenf >= 1) * ((br_pf <= plaf) * base
                                + (br_pf > plaf) * max_(plaf2 - br_pf, 0) / 12.0)

        # Pour bénéficier de cette allocation, il faut que tous les enfants du foyer soient nés, adoptés, ou recueillis en vue d’une adoption avant le 1er janvier 2004, et qu’au moins l’un d’entre eux ait moins de 3 ans.
        # Cette allocation est verséE du 5ème mois de grossesse jusqu’au mois précédant le 3ème anniversaire de l’enfant.

        # Non cumul APE APJE CF
        #  - L’allocation parentale d’éducation (APE), sauf pour les femmes enceintes.
        #    L’APJE est alors versée du 5ème mois de grossesse jusqu’à la naissance de l’enfant.
        #  - Le CF
        return period, 12 * apje  # annualisé


@reference_formula
class ape(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation parentale d'éducation"
    stop_date = date(2004, 1, 1)
    url = "http://fr.wikipedia.org/wiki/Allocation_parentale_d'%C3%A9ducation_en_France"

    def function(self, simulation, period):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        period = period.start.offset('first-of', 'month').period('year')
        apje_temp = simulation.calculate('apje_temp', period)
        ape_temp = simulation.calculate('ape_temp', period)
        cf_temp = simulation.calculate('cf_temp', period)

        ape = (apje_temp < ape_temp) * (cf_temp < ape_temp) * ape_temp
        return period, round(ape, 2)


@reference_formula
class apje(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation pour le jeune enfant"
    stop_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2552.xhtml"

    def function(self, simulation, period):
        '''
        L'APJE n'est pas cumulable avec le complément familial et l'APE
        '''
        period = period.start.offset('first-of', 'month').period('year')
        apje_temp = simulation.calculate('apje_temp', period)
        ape_temp = simulation.calculate('ape_temp', period)
        cf_temp = simulation.calculate('cf_temp', period)

        apje = (cf_temp < apje_temp) * (ape_temp < apje_temp) * apje_temp
        return period, round(apje, 2)
