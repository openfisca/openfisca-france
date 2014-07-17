# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

from numpy import (floor, maximum as max_, logical_not as not_, logical_and as and_, logical_or as or_)
from openfisca_core.accessors import law

from ..input_variables.base import QUIFAM, QUIFOY
from ..pfam import nb_enf

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


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


def _ape(self, age_holder, smic55_holder, inactif, partiel1, partiel2, P = law.fam):
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
    return 12 * ape  # annualisé


def _apje(self, br_pf, age_holder, smic55_holder, isol, biact, P = law.fam):
    '''
    Allocation pour jeune enfant
    '''
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
    return 12 * apje  # annualisé


def _ape_cumul(apje_temp, ape_temp, cf_temp):
    '''
    L'allocation de base de la paje n'est pas cumulable avec le complément familial
    '''
    ape = (apje_temp < ape_temp) * (cf_temp < ape_temp) * ape_temp
    return round(ape, 2)


def _apje_cumul(apje_temp, ape_temp, cf_temp):
    '''
    L'APJE n'est pas cumulable avec le complément familial et l'APE
    '''
    apje = (cf_temp < apje_temp) * (ape_temp < apje_temp) * apje_temp
    return round(apje, 2)
