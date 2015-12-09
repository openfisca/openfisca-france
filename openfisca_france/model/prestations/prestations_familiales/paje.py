# -*- coding: utf-8 -*-

from __future__ import division

from numpy import (round, floor, maximum as max_, minimum as min_, logical_not as not_, datetime64)

from ...base import *  # noqa analysis:ignore
from .base_ressource import nb_enf, age_en_mois_benjamin


# Prestations familiales
build_column('inactif', BoolCol(entity = 'fam',
                    label = u"Parent inactif (PAJE-CLCA)"))

build_column('partiel1', BoolCol(entity = 'fam',
                     label = u"Parent actif à moins de 50% (PAJE-CLCA)"))

build_column('partiel2', BoolCol(entity = 'fam',
                     label = u"Parent actif entre 50% et 80% (PAJE-CLCA)"))

build_column('categ_inv', PeriodSizeIndependentIntCol(label = u"Catégorie de handicap (AEEH)"))

build_column('opt_colca', BoolCol(entity = 'fam',
                      label = u"Opte pour le COLCA"))

build_column('empl_dir', BoolCol(entity = 'fam',
                     label = u"Emploi direct (CLCMG)"))

build_column('ass_mat', BoolCol(entity = 'fam',
                    label = u"Assistante maternelle (CLCMG)"))

build_column('gar_dom', BoolCol(entity = 'fam',
                    label = u"Garde à domicile (CLCMG)"))


class paje(Variable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"PAJE - Ensemble des prestations"
    start_date = date(2004, 1, 1)
    url = "http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/la-prestation-d-accueil-du-jeune-enfant-paje-0"  # noqa

    def function(self, simulation, period):
        '''
        Prestation d'accueil du jeune enfant
        '''
        period = period.this_month

        paje_base = simulation.calculate('paje_base', period)
        paje_naissance = simulation.calculate('paje_naissance', period)
        paje_clca = simulation.calculate('paje_clca', period)
        paje_clmg = simulation.calculate('paje_clmg', period)
        paje_colca = simulation.calculate('paje_colca', period)

        return period, paje_base + (paje_naissance + paje_clca + paje_clmg + paje_colca) / 12


class paje_base_montant(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant de la PAJE"
    start_date = date(2004, 1, 1)

    def function(self, simulation, period):
        period = period.this_month
        couple_biactif = simulation.calculate('biact', period)
        parent_isole = simulation.calculate('isol', period)
        nombre_enfants = simulation.calculate('af_nbenf', period)
        pfam = simulation.legislation_at(period.start).fam
        montant_taux_plein = pfam.af.bmaf * pfam.paje.base.taux

        def plafond_avant_avril_2014():
            plafond_de_base = pfam.paje.base.avant_2014.plaf
            maj_plafond_2_premiers_enfants = pfam.paje.base.avant_2014.plaf_tx1 * plafond_de_base
            maj_plafond_par_enfant_sup = pfam.paje.base.avant_2014.plaf_tx2 * plafond_de_base
            maj_plafond_seul_biactif = pfam.paje.base.avant_2014.plaf_maj

            plafond = (
                plafond_de_base +
                min_(nombre_enfants, 2) * maj_plafond_2_premiers_enfants +
                max_(nombre_enfants - 2, 0) * maj_plafond_par_enfant_sup +
                (couple_biactif + parent_isole) * maj_plafond_seul_biactif
            )
            return plafond

        def plafond_taux_plein():
            plafond_de_base = pfam.paje.base.apres_2014.taux_plein.plaf
            maj_plafond_seul_biactif = pfam.paje.base.apres_2014.taux_plein.plaf_maj
            maj_plafond_par_enfant = pfam.paje.base.apres_2014.plaf_tx_par_enf * plafond_de_base

            plafond = (
                plafond_de_base +
                nombre_enfants * maj_plafond_par_enfant +
                (couple_biactif + parent_isole) * maj_plafond_seul_biactif
            )
            return plafond

        def plafond_taux_partiel():
            plafond_de_base = pfam.paje.base.apres_2014.taux_partiel.plaf
            maj_plafond_seul_biactif = pfam.paje.base.apres_2014.taux_partiel.plaf_maj
            maj_plafond_par_enfant = pfam.paje.base.apres_2014.plaf_tx_par_enf * plafond_de_base

            plafond = (
                plafond_de_base +
                nombre_enfants * maj_plafond_par_enfant +
                (couple_biactif + parent_isole) * maj_plafond_seul_biactif
            )
            return plafond

        def enfant_eligible_ne_avant_avril_2014():
            paje_base_enfant_eligible_avant_reforme_2014 = simulation.compute('paje_base_enfant_eligible_avant_reforme_2014', period)
            return self.any_by_roles(paje_base_enfant_eligible_avant_reforme_2014)

        def enfant_eligible_ne_apres_avril_2014():
            paje_base_enfant_eligible_apres_reforme_2014 = simulation.compute('paje_base_enfant_eligible_apres_reforme_2014', period)
            return self.any_by_roles(paje_base_enfant_eligible_apres_reforme_2014)

        def montant_enfant_ne_avant_avril_2014():
            ressources = simulation.calculate('br_pf', period)
            return (ressources <= plafond_avant_avril_2014()) * montant_taux_plein

        def montant_enfant_ne_apres_avril_2014():
            ressources = simulation.calculate('br_pf', period)
            montant_taux_partiel = montant_taux_plein / 2

            montant = (
                (ressources <= plafond_taux_plein()) * montant_taux_plein +
                (ressources <= plafond_taux_partiel()) * (ressources > plafond_taux_plein()) * montant_taux_partiel
            )
            return montant

        montant = (
            enfant_eligible_ne_avant_avril_2014() * montant_enfant_ne_avant_avril_2014() +
            not_(enfant_eligible_ne_avant_avril_2014()) * enfant_eligible_ne_apres_avril_2014() * montant_enfant_ne_apres_avril_2014()
        )

        return period, montant


class paje_base_enfant_eligible_avant_reforme_2014(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant ouvrant droit à la PAJE de base né avant le 1er avril 2014"

    def function(self, simulation, period):
        period = period.this_month
        age = simulation.calculate('age', period)
        smic55 = simulation.calculate('smic55', period)
        birth = simulation.calculate('birth', period)
        ne_avant_2014 =  (datetime64('2014-04-01') - birth) > 0
        age_limite = simulation.legislation_at(period.start).fam.paje.base.age

        # L'allocation de base est versée jusqu'au dernier jour du mois civil précédant
        # celui au cours duquel l'enfant atteint l'âge de 3 ans.
        return period, (age < age_limite) * not_(smic55) * ne_avant_2014


class paje_base_enfant_eligible_apres_reforme_2014(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant ouvrant droit à la PAJE de base né après le 1er avril 2014"

    def function(self, simulation, period):
        period = period.this_month
        age = simulation.calculate('age', period)
        smic55 = simulation.calculate('smic55', period)
        birth = simulation.calculate('birth', period)
        ne_avant_2014 =  (datetime64('2014-04-01') - birth) > 0
        age_limite = simulation.legislation_at(period.start).fam.paje.base.age

        # L'allocation de base est versée jusqu'au dernier jour du mois civil précédant
        # celui au cours duquel l'enfant atteint l'âge de 3 ans.
        return period, (age < age_limite) * not_(smic55) * not_(ne_avant_2014)


class paje_naissance(Variable):
    calculate_output = calculate_output_add
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de naissance de la PAJE"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2550.xhtml"

    def function(self, simulation, period):
        '''
        Prestation d'accueil du jeune enfant - Allocation de naissance
        '''
        period = period.this_month
        age_en_mois_holder = simulation.compute('age_en_mois', period)
        # age_holder = simulation.compute('age', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        br_pf = simulation.calculate('br_pf', period)
        isol = simulation.calculate('isol', period)
        biact = simulation.calculate('biact', period)
        P = simulation.legislation_at(period.start).fam

        # age = self.split_by_roles(age_holder, roles = ENFS)
        age_en_mois = self.split_by_roles(age_en_mois_holder, roles = ENFS)

        bmaf = P.af.bmaf
        nais_prime = round(100 * P.paje.nais.prime_tx * bmaf) / 100
        # Versée au 7e mois de grossesse dans l'année
        # donc les enfants concernés sont les enfants qui ont -2 mois
        nbnais = 0
        for age_m in age_en_mois.itervalues():
            nbnais += (age_m == -2)  # cas mensuel
            # nbnais += (age_m >= -2) * (age_m < 10) # cas annuel

        nbenf = af_nbenf + nbnais  # On ajoute l'enfant à  naître;

        # Est-ce que ces taux n'ont pas été mis à jour en avril 2014 ?
        plaf_tx = (nbenf > 0) + P.paje.base.avant_2014.plaf_tx1 * min_(nbenf, 2) + P.paje.base.avant_2014.plaf_tx2 * max_(nbenf - 2, 0)
        majo = isol | biact
        plaf = P.paje.base.avant_2014.plaf * plaf_tx + (plaf_tx > 0) * P.paje.base.avant_2014.plaf_maj * majo
        elig = (br_pf <= plaf) * (nbnais != 0)
        nais_brut = nais_prime * elig * (nbnais)
        return period, nais_brut


class paje_clca(Variable):
    calculate_output = calculate_output_add
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
        partiel1 : Salarié: Temps de travail ne dépassant pas 50 % de la durée du travail fixée dans l'entreprise pour
                   les salariés VRP ou non salarié travaillant à temps partiel: Temps de travail ne dépassant pas 76
                   heures par mois et un revenu professionnel mensuel inférieur ou égal à (smic_8.27*169*85 %)
        partiel2 :  Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
                    VRP ou non salarié travaillant à temps partiel: Temps de travail compris entre 77 et 122 heures
                    par mois et un revenu professionnel mensuel ne dépassant pas (smic_8.27*169*136 %)

        http://www.caf.fr/wps/portal/particuliers/catalogue/metropole/paje
        """
        period = period.this_month

        age_en_mois_holder = simulation.compute('age_en_mois', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        paje_base = simulation.calculate('paje_base', period)
        inactif = simulation.calculate('inactif', period)
        partiel1 = simulation.calculate('partiel1', period)
        partiel2 = simulation.calculate('partiel2', period)

        P = simulation.legislation_at(period.start).fam

        age_en_mois = self.split_by_roles(age_en_mois_holder, roles = ENFS)

        paje = paje_base >= 0
        # durée de versement :
        # Pour un seul enfant à charge, le CLCA est versé pendant une période de 6 mois (P.paje.clca.duree1)
        # à partir de la naissance ou de la cessation des IJ maternité et paternité.
        # A partir du 2ème enfant, il est versé jusqu’au mois précédant le 3ème anniversaire
        # de l’enfant.

        # Calcul de l'année et mois de naisage_in_months( du cadet
        # TODO: ajuster en fonction de la cessation des IJ etc
        age_m_benjamin = age_en_mois_benjamin(age_en_mois)
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
        return period, paje_clca

class paje_prepare(Variable):
    column = FloatCol
    entity_class = Familles
    set_input = set_input_divide_by_period
    label = u"Prestation Partagée d’éducation de l’Enfant (PreParE)"


class paje_clca_taux_plein(Variable):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice Clca taux plein"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F313.xhtml"

    def function(self, simulation, period):
        period = period.this_month
        paje_clca = simulation.calculate('paje_clca', period)
        inactif = simulation.calculate('inactif', period)

        return period, (paje_clca > 0) * inactif


class paje_clca_taux_partiel(Variable):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Indicatrice Clca taux partiel"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F313.xhtml"

    def function(self, simulation, period):
        period = period.this_month
        paje_clca = simulation.calculate('paje_clca', period)
        partiel1 = simulation.calculate('partiel1', period)

        return period, (paje_clca > 0) * partiel1

    # TODO gérer les cumuls avec autres revenus et colca voir site caf


class paje_clmg(Variable):
    calculate_output = calculate_output_add
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"PAJE - Complément de libre choix du mode de garde"
    start_date = date(2004, 1, 1)
    url = "http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/le-complement-de-libre-choix-du-mode-de-garde"  # noqa

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
            bénéficiaire du Revenu de solidarité active (Rsa), sous certaines conditions de ressources étudiées par
            votre Caf, et inscrit dans une démarche d'insertionétudiant (si vous vivez en couple,
            vous devez être tous les deux étudiants).

        Autres conditions à remplir : Assistante maternelle agréée     Garde à domicile
        Son salaire brut ne doit pas dépasser par jour de garde et par enfant 5 fois le montant du Smic horaire brut,
        soit au max 45,00 €.
        Vous ne devez pas bénéficier de l'exonération des cotisations sociales dues pour la personne employée.
        '''
        period = period.this_month
        aah_holder = simulation.compute('aah', period)
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period, accept_other_period = True)
        etu_holder = simulation.compute('etu', period)
        salaire_imposable_holder = simulation.compute('salaire_imposable', period)
        hsup_holder = simulation.compute('hsup', period)
        concub = simulation.calculate('concub', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        br_pf = simulation.calculate('br_pf', period.this_month)
        empl_dir = simulation.calculate('empl_dir', period)
        ass_mat = simulation.calculate('ass_mat', period)
        gar_dom = simulation.calculate('gar_dom', period)
        paje_clca_taux_partiel = simulation.calculate('paje_clca_taux_partiel', period)
        paje_clca_taux_plein = simulation.calculate('paje_clca_taux_plein', period)
        P = simulation.legislation_at(period.start).fam
        P_n_2 = simulation.legislation_at(period.start.offset(-2, 'year')).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        hsup = self.split_by_roles(hsup_holder, roles = [CHEF, PART])
        salaire_imposable = self.split_by_roles(salaire_imposable_holder, roles = [CHEF, PART])
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        aah = self.sum_by_entity(aah_holder)

        # condition de revenu minimal

        bmaf_n_2 = P_n_2.af.bmaf
        cond_age_enf = (nb_enf(age, smic55, P.paje.clmg.age1, P.paje.clmg.age2 - 1) > 0)
        cond_sal = (
            salaire_imposable[CHEF] + salaire_imposable[PART] + hsup[CHEF] + hsup[PART] >
            12 * bmaf_n_2 * (1 + concub)
            )
    # TODO:    cond_rpns    =
        cond_act = cond_sal  # | cond_rpns

        cond_nonact = (aah > 0) | (etu[CHEF] & etu[PART])  # | (ass>0)
    #  TODO: RSA insertion, alloc insertion, ass
        elig = cond_age_enf & (cond_act | cond_nonact)
        nbenf = af_nbenf
        seuil1 = (P.paje.clmg.seuil11 * (nbenf == 1) + P.paje.clmg.seuil12 * (nbenf >= 2) +
                 max_(nbenf - 2, 0) * P.paje.clmg.seuil1sup)
        seuil2 = (P.paje.clmg.seuil21 * (nbenf == 1) + P.paje.clmg.seuil22 * (nbenf >= 2) +
                 max_(nbenf - 2, 0) * P.paje.clmg.seuil2sup)

    #        Si vous bénéficiez du Clca taux partiel (= vous travaillez entre 50 et 80% de la durée du travail fixée
    #        dans l'entreprise), vous cumulez intégralement le Clca et le Cmg.
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
        # Si vous bénéficiez du Clca taux plein
        # (= vous ne travaillez plus ou interrompez votre activité professionnelle),
        # vous ne pouvez pas bénéficier du Cmg.
        paje_clmg = elig * not_(paje_clca_taux_plein) * clmg
        # TODO vérfiez les règles de cumul
        return period, paje_clmg


class paje_colca(Variable):
    calculate_output = calculate_output_add
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"PAJE - Complément optionnel de libre choix d'activité"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F15110.xhtml"

    def function(self, simulation, period):
        '''
        Prestation d'accueil du jeune enfant - Complément optionnel de libre choix du mode de garde
        '''
        period = period.this_month

        af_nbenf = simulation.calculate('af_nbenf', period)
        age_en_mois_holder = simulation.compute('age_en_mois', period)
        opt_colca = simulation.calculate('opt_colca', period)
        paje_base = simulation.calculate('paje_base', period)

        P = simulation.legislation_at(period.start).fam

        age_en_mois = self.split_by_roles(age_en_mois_holder, roles = ENFS)
        age_m_benjamin = age_en_mois_benjamin(age_en_mois)
        condition = (age_m_benjamin < 12 * P.paje.colca.age) * (age_m_benjamin >= 0)
        nbenf = af_nbenf
        paje = (paje_base > 0)
        paje_colca = opt_colca * condition * (nbenf >= 3) * P.af.bmaf * (
            (paje) * P.paje.colca.avecab + not_(paje) * P.paje.colca.sansab)
        return period, paje_colca


# TODO: cumul avec clca self.colca_tot_m

class paje_base(Variable):
    calculate_output = calculate_output_add
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de base de la PAJE"
    start_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2552.xhtml"

    def function(self, simulation, period):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        period = period.this_month

        paje_base_montant = simulation.calculate('paje_base_montant', period)
        cf_montant = simulation.calculate('cf_montant', period)

        # On regarde ce qui est le plus intéressant pour la famille, chaque mois
        paje_base = (paje_base_montant >= cf_montant) * paje_base_montant
        return period, paje_base


# def _afeama(self, age_holder, smic55_holder, ape, af_nbenf, br_pf, P = law.fam):
#     '''
#     Aide à la famille pour l'emploi d'une assistante maternelle agréée
#     '''
#     age = self.split_by_roles(age_holder, roles = ENFS)
#     smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
#
#     # TODO http://web.archive.org/web/20080205163300/http://www.caf.fr/wps/portal/particuliers/catalogue/metropole/afeama
#     # Les seuils sont de 80 et 110 % de l'ARS
#     # Vérifier que c'est la même chose pour le clmg
#
#     elig = not_(ape)  # assistante maternelle agréee
#     # Vous devez:
#     #    faire garder votre enfant de moins de 6 ans par une assistante maternelle agréée dont vous êtes l'employeur
#     #    déclarer son embauche à l'Urssaf
#     #    lui verser un salaire ne dépassant pas par jour de garde et par enfant 5 fois le montant horaire du Smic,
#     #    soit au max_ 42,20 €
#     #
#     # Si vous cessez de travailler et bénéficiez de l'allocation parentale d'éducation, vous ne recevrez plus l'Afeama.
#     # Vos enfants doivent être nés avant le 1er janvier 2004.
#
#     # TODO calcul des cotisations urssaf
#     #
#     nbenf_afeama = nb_enf(age, smic55, P.af.age1, P.afeama.age - 1)
#     nbenf = elig * af_nbenf * (nbenf_afeama > 0)
#
#     nb_par_ars = (nbenf == 1 + max_(nbenf - 1, 0) * (1 + P.ars.plaf_enf_supp))
#     seuil1 = (P.afeama.mult_seuil1 * P.ars.plaf) * nb_par_ars
#     seuil2 = (P.afeama.mult_seuil2 * P.ars.plaf) * nb_par_ars
#
#     afeama = nbenf_afeama * P.af.bmaf * (
#             (br_pf < seuil1) * P.afeama.taux_mini +
#             ((br_pf >= seuil1) & (br_pf < seuil2)) * P.afeama.taux_median +
#             (br_pf >= seuil2) * P.afeama.taux_maxi)
#     return 12 * afeama  # annualisé
#
#     # L'AFEAMA comporte 2 volets complémentaires: l'AFEAMA proprement dit qui consiste à prendre en charge les
#     # cotisations sociales sur les salaires, d'une part, et une allocation complémentaire versée aux parents,
#     # la majoration AFEAMA, d'autre part.
#     # Le système de majoration AFEAMA a été modifié au 1er janvier 2001 :
#     # Jusqu'en décembre 2000, son montant ne dépendait que de l'âge de l'enfant.
#     # Depuis janvier 2001, il dépend également de la catégorie de revenus des parents employeurs (fonction de leur base
#     # ressources et du nombre d'enfants qu'ils ont à charge).
#     # Parallélement, son plafonnement a été ramené de 100 % à 85 % du salaire net versé à l'assistante maternelle
#     # (sauf si ces 85 % sont inférieurs au montant de la majoration la moins élevée, compte tenu de l'âge de l'enfant).
#     # La catégorie de revenus des parents employeurs est déterminée par la CAF en fonction de la base ressources
#     # du ménage.
#     # Le tableau suivant récapitule les montants pris en compte depuis le 1er juillet 2007 pour la détermination du
#     # montant maximal de la majoration AFEAMA selon les catégories de revenus :
#     # Base ressources du ménage
#     #                 1 enfant                      2 enfants             par enfant suppémentaire
#     # revenus    inférieurs à 17 593 €             inférieurs à 21 653 €          4060 €
#     #            inférieurs à 24 190 €             inférieurs à 29 773 €          5583 €
#     #            supérieurs à 24 190 €             supérieurs à 29 773 €          5583 €
#     # Montant base ressources 2006, au 1er juillet 2007
#
#
# def _aged(self, age_holder, smic55_holder, br_pf, ape_taux_partiel, dep_trim, P = law.fam):
#     '''
#     Allocation garde d'enfant à domicile
#
#     les deux conjoints actif et revenu min requis, jusqu'aux 6 ans de l'enfant né avant le 01/01/2004, emploi d'une
#     garde A DOMICILE
#     cette allocation consiste en une prise en charge partielle des charges sociales inhérentes à l'emploi d'une personne
#     à domicile.
#     Si vous avez au moins un enfant  de moins de 3 ans gardé au domicile, 2 cas :
#     Revenus 2005 > 37 241  € : la CAF prend en charge 50% des charges sociales (plafonné à 1 106 € par trimestre),
#     Revenus 2005 < 37 341  € : la CAF prend en charge 75% des charges sociales (plafonné à 1 659 € par trimestre).
#     Si vous avez un enfant de plus de 3 ans gardé au domicile (1 seul cas, sans condition de ressources) :
#     la CAF prend en charge 50% des charges sociales (plafonné à 553 € par trimestre)
#     '''
#     # TODO: trimestrialiser
#     age = self.split_by_roles(age_holder, roles = ENFS)
#     smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
#
#     nbenf = nb_enf(age, smic55, 0, P.aged.age1 - 1)
#     nbenf2 = nb_enf(age, smic55, 0, P.aged.age2 - 1)
#     elig1 = (nbenf > 0)
#     elig2 = not_(elig1) * (nbenf2 > 0) * ape_taux_partiel
#     depenses = 4 * dep_trim  # gérer les dépenses trimestrielles
#     aged3 = elig1 * (max_(P.aged.remb_plaf1 - P.aged.remb_taux1 * depenses, 0) * (br_pf > P.aged.revenus_plaf) +
#        (br_pf <= P.aged.revenus_plaf) * max_(P.aged.remb_taux2 * depenses - P.aged.remb_plaf1, 0))
#     aged6 = elig2 * max_(P.aged.remb_taux2 * depenses - P.aged.remb_plaf2, 0)
#     return 12 * (aged3 + aged6)  # annualisé


class ape_temp(Variable):
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

        Les personnes en couple peuvent toutes deux bénéficier de l’APE à taux plein, mais pas en même temps.
        En revanche, elles peuvent cumuler deux taux partiels, à condition que leur total ne dépasse pas le montant
        du taux plein.

        TODO: cumul,  adoption, triplés,
        Cumul d'allocations : Cette allocation n'est pas cumulable pour un même ménage avec
        - une autre APE (sauf à taux partiel),
        - ou l'allocation pour jeune enfant (APJE) versée à partir de la naissance,
        - ou le complément familial,
        - ou l'allocation d’adulte handicapé (AAH).
        Enfin, il est à noter que cette allocation n’est pas cumulable avec :
        - une pension d’invalidité ou une retraite ;
        - des indemnités journalières de maladie, de maternité ou d’accident du travail ;
        - des allocations chômage. Il est tout de même possible de demander aux ASSEDIC la suspension de ces dernières
          pour percevoir l’APE.

        L'allocation parentale d'éducation n'est pas soumise à condition de ressources, sauf l’APE à taux partiel pour
        les professions non salariées.
        '''
        period = period.this_month
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
        # Temps de travail ne dépassant pas 76 heures par mois et un revenu professionnel mensuel inférieur ou égal à
        # (smic_8.27*169*85 %)
        # partiel1 = zeros((12,self.taille))

        # Temps partiel 2
        # Salarié:
        # Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
        # Temps de travail compris entre 77 et 122 heures par mois et un revenu professionnel mensuel ne dépassant pas
        #  (smic_8.27*169*136 %)
        ape = elig * (inactif * P.ape.tx_inactif + partiel1 * P.ape.tx_50 + partiel2 * P.ape.tx_80)
        # Cummul APE APJE CF
        return period, ape  # annualisé


class apje_temp(Variable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation pour le jeune enfant"
    stop_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2552.xhtml"

    def function(self, simulation, period):
        '''
        Allocation pour jeune enfant
        '''
        period = period.this_month
        br_pf = simulation.calculate('br_pf', period.this_month)
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period.this_month)
        biact = simulation.calculate_add('biact', period)
        isol = simulation.calculate('isol', period)
        P = simulation.legislation_at(period.start).fam
        P_n_2 = simulation.legislation_at(period.start.offset(-2, 'year')).fam

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        # TODO: APJE courte voir doc ERF 2006
        nbenf = nb_enf(age, smic55, 0, P.apje.age - 1)
        bmaf = P.af.bmaf
        bmaf_n_2 = P_n_2.af.bmaf
        base = round(P.apje.taux * bmaf, 2)
        base2 = round(P.apje.taux * bmaf_n_2, 2)

        plaf_tx = (nbenf > 0) + P.apje.plaf_tx1 * min_(nbenf, 2) + P.apje.plaf_tx2 * max_(nbenf - 2, 0)
        majo = isol | biact
        plaf = P.apje.plaf * plaf_tx + P.apje.plaf_maj * majo
        plaf2 = plaf + 12 * base2

        apje = (nbenf >= 1) * ((br_pf <= plaf) * base + (br_pf > plaf) * max_(plaf2 - br_pf, 0) / 12.0)

        # Pour bénéficier de cette allocation, il faut que tous les enfants du foyer soient nés, adoptés, ou recueillis
        # en vue d’une adoption avant le 1er janvier 2004, et qu’au moins l’un d’entre eux ait moins de 3 ans.
        # Cette allocation est verséE du 5��me mois de grossesse jusqu���au mois précédant le 3ème anniversaire de
        # l’enfant.

        # Non cumul APE APJE CF
        #  - L’allocation parentale d’éducation (APE), sauf pour les femmes enceintes.
        #    L’APJE est alors versée du 5ème mois de grossesse jusqu’à la naissance de l’enfant.
        #  - Le CF
        return period, apje


class ape(Variable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation parentale d'éducation"
    stop_date = date(2004, 1, 1)
    url = "http://fr.wikipedia.org/wiki/Allocation_parentale_d'%C3%A9ducation_en_France"

    def function(self, simulation, period):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        period = period.this_month
        apje_temp = simulation.calculate('apje_temp', period)
        ape_temp = simulation.calculate('ape_temp', period)
        cf_montant = simulation.calculate('cf_montant', period)

        ape = (apje_temp < ape_temp) * (cf_montant < ape_temp) * ape_temp
        return period, round(ape, 2)


class apje(Variable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation pour le jeune enfant"
    stop_date = date(2004, 1, 1)
    url = "http://vosdroits.service-public.fr/particuliers/F2552.xhtml"

    def function(self, simulation, period):
        # L'APJE n'est pas cumulable avec le complément familial et l'APE
        period = period.this_month
        apje_temp = simulation.calculate('apje_temp', period)
        ape_temp = simulation.calculate('ape_temp', period)
        cf_montant = simulation.calculate('cf_montant', period)

        apje = (cf_montant < apje_temp) * (ape_temp < apje_temp) * apje_temp
        return period, round(apje, 2)
