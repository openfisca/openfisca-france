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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import logging

from numpy import maximum as max_, minimum as min_

from ..base import (
    CAT, FloatCol, Individus, QUIFAM, QUIFOY, QUIMEN, reference_formula, SimpleFormulaColumn, TAUX_DE_PRIME,
    )

CHEF = QUIFAM['chef']
log = logging.getLogger(__name__)
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


from .travail import apply_bareme_for_relevant_type_sal


@reference_formula
class allocations_temporaires_invalidite(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations temporaires d'invalidité (ATI, fonction publique et collectivités locales)"
    # patronale, non-contributive

    def function(self, salbrut, type_sal, primes_fonction_publique, supp_familial_traitement, indemnite_residence, _P):

        eligibles = (
            (type_sal == CAT['public_titulaire_etat']) +
            (type_sal == CAT['public_titulaire_hospitaliere']) +
            (type_sal == CAT['public_non_titulaire'])
            ) > 0  # TODO check
        base = salbrut + (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
        base = eligibles * base
        cotisation_etat = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "ati",
            base = salbrut,
            type_sal = type_sal,
            )
        cotisation_collectivites_locales = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "atiacl",
            base = salbrut,
            type_sal = type_sal,
            )
        return cotisation_etat + cotisation_collectivites_locales

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class cotisation_exceptionnelle_solidarite_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation exceptionnelle de solidarité (employe)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "excep_solidarite",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            type_sal = type_sal,
            )
        return cotisation

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class pension_civile_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pension civile employé"
    url = u"http://www.ac-besancon.fr/spip.php?article2662",

    def function(self, salbrut, type_sal, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        terr_or_hosp = (
            type_sal == CAT['public_titulaire_territoriale']) | (type_sal == CAT['public_titulaire_hospitaliere'])
        pension_civile_employe = (
            (type_sal == CAT['public_titulaire_etat']) * sal['public_titulaire_etat']['pension'].calc(salbrut)
            + terr_or_hosp * sal['public_titulaire_territoriale']['cnracl1'].calc(salbrut)
            )
        return -pension_civile_employe

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class pension_civile_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation patronale pension civile"
    url = u"http://www.ac-besancon.fr/spip.php?article2662"

    def function(self, salbrut, type_sal, _P):
        # Note : salbrut est égal au traitement indiciaire brut
        pat = _P.cotsoc.cotisations_employeur.__dict__
        terr_or_hosp = (
            (type_sal == CAT['public_titulaire_territoriale']) |
            (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        cot_pat_pension_civile = (
            (type_sal == CAT['public_titulaire_etat']) * pat['public_titulaire_etat']['pension'].calc(salbrut)
            + terr_or_hosp * pat['public_titulaire_territoriale']['cnracl'].calc(salbrut)
            )
        return -cot_pat_pension_civile

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class rafp_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part salariale de la retraite additionelle de la fonction publique"
#    Part salariale de la retraite additionelle de la fonction publique
#    TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
#    Note: sal_brut est le traitement indiciaire brut pour les fonctionnaires

    def function(self, salbrut, type_sal, primes_fonction_publique, supp_familial_traitement, indemnite_residence, _P):
        eligibles = ((type_sal == CAT['public_titulaire_etat'])
                     + (type_sal == CAT['public_titulaire_territoriale'])
                     + (type_sal == CAT['public_titulaire_hospitaliere']))
        tib = salbrut * eligibles

        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * tib)
        # Même régime pour etat et colloc
        rafp_employe = eligibles * _P.cotsoc.cotisations_salarie.public_titulaire_etat['rafp'].calc(assiette)
        return -rafp_employe

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')



@reference_formula
class rafp_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part patronale de la retraite additionelle de la fonction publique"

    # TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
    # Note: salbrut est le traitement indiciaire brut pour les fonctionnaires
    def function(self, salbrut, type_sal, primes_fonction_publique, supp_familial_traitement, indemnite_residence, _P):
        eligibles = ((type_sal == CAT['public_titulaire_etat'])
                     + (type_sal == CAT['public_titulaire_territoriale'])
                     + (type_sal == CAT['public_titulaire_hospitaliere']))
        tib = salbrut * eligibles
        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * tib)
        bareme_rafp = _P.cotsoc.cotisations_employeur.public_titulaire_etat['rafp']
        rafp_employeur = eligibles * bareme_rafp.calc(assiette)
        return - rafp_employeur

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class primes_fonction_publique(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul des primes pour les fonctionnaries"
#   Note: sal_brut est égal au traitement indiciaire brut

    def function(self, type_sal, salbrut):
        public = (
            (type_sal == CAT['public_titulaire_etat'])
            + (type_sal == CAT['public_titulaire_territoriale'])
            + (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        tib = salbrut * public
        return TAUX_DE_PRIME * tib

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


def _traitement_brut_mensuel(indice_maj, _P):
        Indice_majore_100_annuel = _P.fonc.IM_100
        traitement_brut = Indice_majore_100_annuel * indice_maj / 100 / 12
        return traitement_brut


@reference_formula
class gipa(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de garantie individuelle du pouvoir d'achat"

    def function(self, type_sal, _P):
        # http://www.emploi-collectivites.fr/salaire-fonction-publique#calcul-indice-salarial
        pass

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class indemnite_residence(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de résidence des fonctionnaires"

    def function(self, salbrut, type_sal, zone_apl_individu, _P):
        zone_apl = zone_apl_individu
        P = _P.fonc.indem_resid
        min_zone_1, min_zone_2, min_zone_3 = P.min * P.taux.zone1, P.min * P.taux.zone2, P.min * P.taux.zone3
        taux = P.taux.zone1 * (zone_apl == 1) + P.taux.zone2 * (zone_apl == 2) + P.taux.zone3 * (zone_apl == 3)
        plancher = min_zone_1 * (zone_apl == 1) + min_zone_2 * (zone_apl == 2) + min_zone_3 * (zone_apl == 3)
        return max_(plancher, taux * salbrut) * (type_sal >= 2)

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class indice_majore(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indice majoré"

    def function(self, type_sal, salbrut, _P):
        traitement_annuel_brut = _P.fonc.IM_100
        return (salbrut * 100 * 12/ traitement_annuel_brut) * (type_sal >= 2)

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class supp_familial_traitement(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Supplément familial de traitement"
    # Attention : par hypothèse ne peut êre attribué qu'à la tête du ménage
    # TODO: gérer le cas encore problématique du conjoint fonctionnaire

    def function(self, type_sal, salbrut, af_nbenf_holder, _P):
        # TODO: un seul sft par couple où est présent un fonctionnaire
        fonc_nbenf = self.cast_from_entity_to_role(af_nbenf_holder, role = CHEF)
        P = _P.fonc.supp_fam
        part_fixe_1 = P.fixe.enf1
        part_fixe_2 = P.fixe.enf2
        part_fixe_supp = P.fixe.enfsupp
        part_fixe = (
            part_fixe_1 * (fonc_nbenf == 1) + part_fixe_2 * (fonc_nbenf == 2)
            + part_fixe_supp * max_(0, fonc_nbenf - 2)
            )
        # pct_variable_1 = 0
        pct_variable_2 = P.prop.enf2
        pct_variable_3 = P.prop.enf3
        pct_variable_supp = P.prop.enfsupp
        pct_variable = (
            pct_variable_2 * (fonc_nbenf == 2) + (pct_variable_3) * (fonc_nbenf == 3)
            + pct_variable_supp * max_(0, fonc_nbenf - 3))

        indice_maj_min = P.IM_min
        indice_maj_max = P.IM_max

        traitement_brut_mensuel_min = _traitement_brut_mensuel(indice_maj_min, _P)
        plancher_mensuel_1 = part_fixe
        plancher_mensuel_2 = part_fixe + traitement_brut_mensuel_min * pct_variable_2
        plancher_mensuel_3 = part_fixe + traitement_brut_mensuel_min * pct_variable_3
        plancher_mensuel_supp = traitement_brut_mensuel_min * pct_variable_supp

        plancher = (plancher_mensuel_1 * (fonc_nbenf == 1) +
                    plancher_mensuel_2 * (fonc_nbenf == 2) +
                    plancher_mensuel_3 * (fonc_nbenf >= 3) +
                    plancher_mensuel_supp * max_(0, fonc_nbenf - 3))

        traitement_brut_mensuel_max = _traitement_brut_mensuel(indice_maj_max, _P)
        plafond_mensuel_1 = part_fixe
        plafond_mensuel_2 = part_fixe + traitement_brut_mensuel_max * pct_variable_2
        plafond_mensuel_3 = part_fixe + traitement_brut_mensuel_max * pct_variable_3
        plafond_mensuel_supp = traitement_brut_mensuel_max * pct_variable_supp

        plafond = (plafond_mensuel_1 * (fonc_nbenf == 1) + plafond_mensuel_2 * (fonc_nbenf == 2) +
                   plafond_mensuel_3 * (fonc_nbenf == 3) +
                   plafond_mensuel_supp * max_(0, fonc_nbenf - 3))

        sft = min_(max_(part_fixe + pct_variable * salbrut, plancher), plafond) * (type_sal >= 2)
        # Nota Bene:
        # type_sal is an EnumCol which enum is:
        # CAT = Enum(['prive_non_cadre',
        #             'prive_cadre',
        #             'public_titulaire_etat',
        #             'public_titulaire_militaire',
        #             'public_titulaire_territoriale',
        #             'public_titulaire_hospitaliere',
        #             'public_non_titulaire'])
        return sft

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')