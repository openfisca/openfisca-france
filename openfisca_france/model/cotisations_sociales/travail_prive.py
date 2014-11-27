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

from numpy import ones, zeros
from openfisca_core.accessors import law
from openfisca_core.enumerations import Enum
from openfisca_core.columns import EnumCol, FloatCol
from openfisca_core.formulas import SimpleFormulaColumn


from ..base import CAT, QUIFAM, QUIFOY, QUIMEN
from ..base import Individus, reference_formula


CHEF = QUIFAM['chef']
DEBUG_SAL_TYPE = 'public_titulaire_hospitaliere'
log = logging.getLogger(__name__)
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


taux_versement_transport_by_localisation_entreprise = None


def apply_bareme_for_relevant_type_sal(
        bareme_by_type_sal_name = None,
        bareme_name = None,
        type_sal = None,
        base = None,
        ):
    assert bareme_by_type_sal_name is not None
    assert bareme_name is not None
    assert base is not None
    assert type_sal is not None
    cotisation = zeros(len(base))
    for type_sal_enum in CAT:
        if type_sal_enum[0] not in bareme_by_type_sal_name:  # to deal with public_titulaire_militaire
            continue
        bareme = bareme_by_type_sal_name[type_sal_enum[0]].get(bareme_name)  # TODO; should have better warnings
        if bareme:
            cotisation += bareme.calc(base) * (type_sal == type_sal_enum[1])
    return - cotisation

# TODO:
# contribution patronale de prévoyance complémentaire
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)


@reference_formula
class mhsup(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Heures supplémentaires comptées négativement"

    def function(self, hsup):
        return -hsup

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


############################################################################
# # Salaires
############################################################################

@reference_formula
class accident_du_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations patronales accident du travail et maladie professionelle"

    def function(self, salbrut, type_sal, taux_accident_travail):
        prive = (type_sal == CAT['prive_cadre']) + (type_sal == CAT['prive_non_cadre'])
        return - salbrut * taux_accident_travail * prive  # TODO: check public

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class apec_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations agence pour l'emploi des cadres (APEC, employé)"

    def function(self, salbrut, type_sal, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "apec",
            base = salbrut,
            type_sal = type_sal,
            )
        return cotisation  # TODO: check public notamment contractuel

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class apec_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations Agenece pour l'emploi des cadres (APEC, employeur)"

    def function(self, salbrut, type_sal, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "apec",
            base = salbrut,
            type_sal = type_sal,
            )
        return cotisation  # TODO: check public notamment contractuel

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class agff_tranche_a_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage AGFF tranche A (employé)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation= apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "agff",
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
class agff_tranche_a_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage AGFF tranche A (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation_non_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "agffnc",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            type_sal = type_sal,
            )

        cotisation_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "agffc",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            type_sal = type_sal,
            )
        return cotisation_cadre + cotisation_non_cadre

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class agirc_tranche_b_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC tranche B (employé)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "agirc",
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
class agirc_tranche_b_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC tranche B (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "agirc",
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
class ags(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution à l'association pour la gestion du régime de garantie des créances des salariés (AGS, employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "chomfg",
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
class arrco_tranche_a_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche A (employé)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "arrco",
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
class arrco_tranche_a_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche A (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "arrco",
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
class assedic_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage tranche A (employé)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "assedic",
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
class assedic_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage tranche A (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "assedic",
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
class contribution_developpement_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution additionnelle au développement de l'apprentissage"

    def function(self, redevable_taxe_apprentissage, salbrut, hsup, type_sal, primes_fonction_publique,
                 indemnite_residence, _P):
        # TODO: check entreprise redevable
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "apprentissage_add",
            base = redevable_taxe_apprentissage * (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            type_sal = type_sal,
            )
        return cotisation

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class contribution_supplementaire_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution supplémentaire à l'apprentissage"

    def function(self, redevable_taxe_apprentissage, salbrut, hsup, type_sal, primes_fonction_publique,
                 indemnite_residence, part_d_alternants, effectifs_entreprise, period,
                 taux = law.cotsoc.contribution_supplementaire_apprentissage):

        if period.start.year > 2012:
            taux_contribution = redevable_taxe_apprentissage * (
                (effectifs_entreprise < 2000) * (part_d_alternants < .01) * taux.moins_2000_moins_1pc_alternants +
                (effectifs_entreprise >= 2000) * (part_d_alternants < .01) * taux.plus_2000_moins_1pc_alternants +
                (.01 <= part_d_alternants < .02) * taux.entre_1_2_pc_alternants +
                (.02 <= part_d_alternants < .03) * taux.entre_2_3_pc_alternants +
                (.03 <= part_d_alternants < .04) * taux.entre_3_4_pc_alternants +
                (.04 <= part_d_alternants < .05) * taux.entre_4_5_pc_alternants
                )
        else:
            taux_contribution = (effectifs_entreprise >= 250) * taux.plus_de_250
            # TODO: gestion de la place dans le XML pb avec l'arbe des paramètres / preprocessing
        return - taux_contribution * (
            salbrut +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
            )

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class contribution_solidarite_autonomie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution solidarité autonomie (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "csa",
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
class cotisation_exceptionnelle_temporaire_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation_exceptionnelle_temporaire (employe)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "cet",
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
class cotisation_exceptionnelle_temporaire_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation exceptionnelle temporaire (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "cet",
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
class cotisation_exceptionelle_temporaire_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation_exceptionelle_temporaire (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "cet",
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
class famille(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation famille (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "famille",
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
class fnal_tranche_a(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation fonds national action logement (FNAL tout employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "fnal1",
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
class fnal_tranche_a_plus_20(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Fonds national action logement (FNAL, employeur avec plus de 20 salariés)"

    def function(self, salbrut, hsup, taille_entreprise, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "fnal2",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ) * (taille_entreprise > 2),  # plus de 20 salariés TODO: Be more explicit
            type_sal = type_sal,
            )
        return cotisation

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class formation_professionnelle(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Formation professionnelle"

    def function(self, salbrut, hsup, taille_entreprise, type_sal, indemnite_residence, primes_fonction_publique, _P):

        cotisation_0_9 = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "formprof_09",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ) * (taille_entreprise == 1),  # moins de 10 salariés TODO: Be more explicit
            type_sal = type_sal,
            )
        cotisation_10_19 = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "formprof_1019",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ) * (taille_entreprise == 2),  # moins de 20 salariés TODO: Be more explicit
            type_sal = type_sal,
            )
        cotisation_20 = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "formprof_20",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ) * (taille_entreprise > 2),  # plus de 20 salariés TODO: Be more explicit
            type_sal = type_sal,
            )
        return cotisation_0_9 + cotisation_10_19 + cotisation_20

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class maladie_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (employé)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "maladie",
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
class maladie_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "maladie",
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
class participation_effort_construction(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Participation à l'effort de construction"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique,
                 indemnite_residence, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "construction",
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
class taxe_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"

    def function(self, redevable_taxe_apprentissage, salbrut, hsup, type_sal, primes_fonction_publique,
                 indemnite_residence, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "apprentissage",
            base = redevable_taxe_apprentissage * (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            type_sal = type_sal,
            )
        return cotisation

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class taux_versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u""

    def function(self, localisation_entreprise, _P):
    #    import csv
    #    import json
    #    import openfisca_france
    #    import pkg_resources
        aot_salarie = 0 # Autorité organisatrice des transports du salarié (nul si absent)
        smt_salarie = 0 # Syndicat mixte des transports du salarié (nul si absent)

        entreprise_seuil_employe_aot = 0 # "L'entreprise emploie-t-elle 9 salariés ou plus dans le périmètre
                                   # de l'Autorité organisatrice de transport (AOT) suivante :"
    #  Taux du versement de transport dans l'AOT du salari<E9> -> *SALARIE.TX_VT (Valeur par d<E9>faut: '0.00000')
    #
    #% Cas ou le salari<E9> travaille dans une commune avec AOT
    #
    #        2.6.2 [Versement de transport additionnel]
    #
    #              # Question : "L'entreprise emploie-t-elle 9 salari<E9>s ou plus dans le p<E9>rim<E8>tre du Syndicat mixte de tranports (SMT) suivant ?"
    #
    #              # Affichage : Afficher le nom du SMT (SALARIE.NOM_SMT) ainsi que toutes les communes couvertes par le SMT (SALARIE.SMT.LISTE_COMMUNES)
    #
    #              # Mode de saisie : <E0> cocher au choix : "oui" / "non" (case coch<E9>e par d<E9>faut : "oui")
    #
    #              # Enregistrements:
    #                R<E9>ponse -> *SALARIE.IS_SMT_9P (bool : '1' si "oui" / '0' si "non")
    #                Taux du versement de transport additionel dans le SMT du salari<E9> -> *SALARIE.TX_VTA (Valeur par d<E9>faut: '0.0000')
    #
    #        }

        global taux_versement_transport_by_localisation_entreprise
    #    if taux_versement_transport_by_localisation_entreprise is None:
    #        with pkg_resources.resource_stream(
    #            openfisca_france.__name__,
    #            'assets/versement_transport/versement_transport.csv',
    #            ) as csv_file:
    #            csv_reader = csv.DictReader(csv_file)
    #            taux_versement_transport_by_localisation_entreprise = {
    #                # Keep only first char of Zonage column because of 1bis value considered equivalent to 1.
    #                row['CODGEO']: int(row['Taux'][0])
    #                for row in csv_reader
    #                }
    #        # Add subcommunes (arrondissements and communes associées), use the same value as their parent commune.
    #        with pkg_resources.resource_stream(
    #            openfisca_france.__name__,
    #            'assets/versement_transport/versement_transport_by_subcommune_depcom.json',
    #            ) as json_file:
    #            commune_depcom_by_subcommune_depcom = json.load(json_file)
    #            for subcommune_depcom, commune_depcom in commune_depcom_by_subcommune_depcom.iteritems():
    #                taux_versement_transport_by_localisation_entreprise[subcommune_depcom] = taux_versement_transport_by_localisation_entreprise[commune_depcom]
    #
    #    default_value = _P.cotsoc.cotisations_employeur.__dict__['prive_non_cadre']["transport"].rates[0]
    #    return fromiter(
    #        (
    #            taux_versement_transport_by_localisation_entreprise.get(localisation_entreprise_cell, default_value)
    #            for localisation_entreprise_cell in localisation_entreprise
    #            ),
    #        dtype = float,
    #        )
        rate = _P.cotsoc.cotisations_employeur.__dict__['prive_non_cadre']["transport"].rates[0]
        return rate * ones(len(localisation_entreprise))

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Versement transport"

    def function(self, salbrut, hsup, indemnite_residence, primes_fonction_publique, taux_versement_transport,
                 type_sal, _P):
        base = (
            salbrut +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
            )
        cotisation = - taux_versement_transport * base
        return cotisation

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class vieillesse_deplafonnee_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse déplafonnée (employé)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "vieillessedeplaf",
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
class vieillesse_plafonnee_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse plafonnée (employé)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "vieillesse",
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
class vieillesse_deplafonnee_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse déplafonnée"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "vieillessedeplaf",
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
class vieillesse_plafonnee_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse plafonnée (employeur)"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "vieillesseplaf",
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
class taux_accident_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Approximation du taux accident à partir de l'exposition au risque donnée"

    def function(self, exposition_accident, period, accident = law.cotsoc.accident):
        if period.start.year >= 2012:
            return (exposition_accident == 0) * accident.faible + (exposition_accident == 1) * accident.moyen \
                + (exposition_accident == 2) * accident.eleve + (exposition_accident == 3) * accident.treseleve

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')  # TODO month ?


@reference_formula
class taille_entreprise(SimpleFormulaColumn):
    column = EnumCol(
        enum = Enum(
            [
                u"Non pertinent",
                u"Moins de 10 salariés",
                u"De 10 à 19 salariés",
                u"De 20 à 249 salariés",
                u"Plus de 250 salariés",
                ],
            ),
        default = 0,
        )
    entity_class = Individus
    label = u"Catégode taille d'entreprise (pour calcul des cotisations sociales)"
    url = u"http://www.insee.fr/fr/themes/document.asp?ref_id=ip1321"

    def function(self, effectifs_entreprise):
        taille_entreprise = (
            effectifs_entreprise > 0 +
            effectifs_entreprise > 10 +
            effectifs_entreprise > 20 +
            effectifs_entreprise > 250
            )
        return taille_entreprise

    def get_output_period(self, period):
        return period
