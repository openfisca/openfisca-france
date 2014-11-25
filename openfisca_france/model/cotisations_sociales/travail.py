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

import datetime
import logging

from numpy import logical_not as not_, logical_or as or_, ones, maximum as max_, minimum as min_, zeros
from openfisca_core.accessors import law

from openfisca_core.columns import FloatCol
from openfisca_core.formulas import EntityToPersonColumn, SimpleFormulaColumn

from openfisca_core.taxscales import TaxScalesTree, scale_tax_scales

from ..base import CAT, QUIFAM, QUIFOY, QUIMEN, TAUX_DE_PRIME
from ..base import FoyersFiscaux, Individus, reference_formula


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
#        print type_sal_enum[0]
#        print bareme
        if bareme:
#            if type_sal_enum[0] == "public_titulaire_territoriale" and bareme_name == "ati":
#                print type_sal_enum[0]
#                print type_sal_enum[1]
#                print bareme
#                print base
#                print bareme.calc(base) * (type_sal == type_sal_enum[1])
            cotisation += bareme.calc(base) * (type_sal == type_sal_enum[1])
    return - cotisation

# TODO:
# toutes les taxes d'apprentissages (noms et barèmes à vérifier)
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
        cotisation = apply_bareme_for_relevant_type_sal(
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
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "agffnc",
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
    label = u"Cotisation_exceptionnelle_temporaire (employeur)"

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
class cotisations_patronales_contributives(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales contributives"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, rafp_employeur,
                 pension_civile_employeur, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotisations_patronales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    if category[0] in [
                        "prive_cadre",
                        "prive_non_cadre",
                        "public_non_titulaire",
                        "public_titulaire_hospitaliere",
                        ]: #  TODO: move up
                        is_contrib = (bar.option == "contrib") & (bar.name not in ['cnracl', 'rafp', 'pension'])
                        temp = -(
                            iscat * bar.calc(
                                salbrut + (category[0] == 'public_non_titulaire') * (
                                    indemnite_residence + primes_fonction_publique
                                    )
                                )
                            ) * is_contrib
                        cotisations_patronales += temp

        cotisations_patronales += rafp_employeur + pension_civile_employeur
        return cotisations_patronales

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')



@reference_formula
class cotisations_patronales_main_d_oeuvre(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales main d'oeuvre"

    # TODO: A discriminer selon la taille de l'entreprise
    # Il s'agit de prélèvements sur les salaires que la CN ne classe pas dans les cotisations sociales
    #  En particulier, la CN classe:
    #     - D291: taxe sur les salaire, versement transport, FNAL, CSA, taxe d'apprentissage, formation continue
    #     - D993: participation à l'effort de construction

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cotisations_patronales_transport, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotisations_patronales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_mo = (bar.option == "main-d-oeuvre")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                                 indemnite_residence + primes_fonction_publique
                                 ))
                             * is_mo)
                    cotisations_patronales += temp
        return cotisations_patronales + cotisations_patronales_transport

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')

@reference_formula
class cotisations_patronales_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales: versement transport"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        transport = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index of the category
            if category[0] in pat.keys():  # category[0] is the name of the category
                if 'transport' in pat[category[0]]:
                    bar = pat[category[0]]['transport']
                    temp = -bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                        indemnite_residence + primes_fonction_publique)) * iscat  # check
                    transport += temp
        return transport

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
class cotisations_patronales_accident(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations patronales accident du travail et maladie professionelle"

    def function(self, salbrut, taux_accident_travail, type_sal):
        prive = (type_sal == CAT['prive_cadre']) + (type_sal == CAT['prive_non_cadre'])
        return -salbrut * taux_accident_travail * prive  # TODO: check public

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')  # TODO month ?


@reference_formula
class cotisations_patronales_noncontrib(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales non contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cotisations_patronales_accident, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotisations_patronales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_noncontrib = (bar.option == "noncontrib")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                                 indemnite_residence + primes_fonction_publique))
                             * is_noncontrib)
                    cotisations_patronales += temp
        return cotisations_patronales + cotisations_patronales_accident

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')



@reference_formula
class cotisations_patronales(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"

    def function(self, cotisations_patronales_contributives, cotisations_patronales_noncontrib, cotisations_patronales_main_d_oeuvre):
        return cotisations_patronales_contributives + cotisations_patronales_noncontrib + cotisations_patronales_main_d_oeuvre

    def get_output_period(self, period):
        return period


def seuil_fds(_P):
    '''
    Calcul du seuil mensuel d'assujetissement à la contribution au fond de solidarité
    '''
    from math import floor
    ind_maj_ref = _P.cotsoc.sal.fonc.commun.ind_maj_ref
    pt_ind = _P.cotsoc.sal.fonc.commun.pt_ind
    seuil_mensuel = floor((pt_ind * ind_maj_ref))
    return seuil_mensuel


@reference_formula
class cotisations_salariales_contrib(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, rafp_employe,
                 pension_civile_employe, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        cotisations_salariales = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_contrib = (bar.option == "contrib") & (
                        bar.name not in ["rafp", "pension", "cnracl1", "cnracl2"])  # dealed by pension civile and rafp
                    temp = -(iscat * bar.calc(
                        salbrut - hsup + (category[0] == 'public_non_titulaire') * (
                            indemnite_residence + primes_fonction_publique
                            )
                        )
                    ) * is_contrib
                    cotisations_salariales += temp
        public_titulaire = (
            (type_sal == CAT['public_titulaire_etat'])
            + (type_sal == CAT['public_titulaire_territoriale'])
            + (type_sal == CAT['public_titulaire_hospitaliere']))

        return cotisations_salariales + (pension_civile_employe + rafp_employe) * public_titulaire

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class cotisations_salariales_noncontrib(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales non-contributives"
    entity_class = Individus

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, rafp_employe,
                 pension_civile_employe, cotisations_salariales_contrib, P = law):
        sal = P.cotsoc.cotisations_salarie.__dict__
        cotisations_salariales = zeros(len(salbrut))
        seuil_assuj_fds = seuil_fds(P)
    #    log.info("seuil assujetissement FDS %i", seuil_assuj_fds)
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_exempt_fds = (category[0] in ['public_titulaire_etat', 'public_titulaire_territoriale', 'public_titulaire_hospitaliere']) * (bar.name == 'solidarite') * ((salbrut - hsup) <= seuil_assuj_fds)  # TODO: check assiette voir IPP
                    is_noncontrib = (bar.option == "noncontrib")  # and (bar.name in ["famille", "maladie"])
                    temp = -(
                        iscat * bar.calc(
                            salbrut + primes_fonction_publique + indemnite_residence - hsup + rafp_employe +
                            pension_civile_employe + cotisations_salariales_contrib * (
                                category[0] == 'public_non_titulaire'
                                )
                            * (
                                bar.name == "excep_solidarite"
                                )
                            ) * is_noncontrib * not_(is_exempt_fds)
                        )
                    cotisations_salariales += temp
        return cotisations_salariales

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class cotisations_salariales(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales"
    entity_class = Individus

    def function(self, cotisations_salariales_contrib, cotisations_salariales_noncontrib):
        return cotisations_salariales_contrib + cotisations_salariales_noncontrib

    def get_output_period(self, period):
        return period


@reference_formula
class csgsald(SimpleFormulaColumn):
    column = FloatCol
    label = u"CSG déductible sur les salaires"
    entity_class = Individus

    def function(self, salbrut, primes_fonction_publique, indemnite_residence, supp_familial_traitement, hsup, P = law):
        csg = scale_tax_scales(P.csg.act.deduc, P.cotsoc.gen.plaf_ss)
        return - csg.calc(salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class csgsali(SimpleFormulaColumn):
    column = FloatCol
    label = u"CSG imposables sur les salaires"
    entity_class = Individus

    def function(self, salbrut, hsup, primes_fonction_publique, indemnite_residence, supp_familial_traitement, P = law):
        csg = scale_tax_scales(P.csg.act.impos, P.cotsoc.gen.plaf_ss)
        return - csg.calc(
            salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup
            )

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class crdssal(SimpleFormulaColumn):
    column = FloatCol
    label = u"CRDS sur les salaires"
    entity_class = Individus

    def function(self, salbrut, hsup, primes_fonction_publique, indemnite_residence, supp_familial_traitement, P = law):
        crds = scale_tax_scales(P.crds.act, P.cotsoc.gen.plaf_ss)
        return - crds.calc(salbrut - hsup + primes_fonction_publique + indemnite_residence + supp_familial_traitement)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class sal(SimpleFormulaColumn):
    column = FloatCol
    label = u"Salaires imposables"
    entity_class = Individus

    def function(self, salbrut, primes_fonction_publique, indemnite_residence, supp_familial_traitement, csgsald,
                 cotisations_salariales, hsup, rev_microsocial_declarant1):
        return (
            salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement + csgsald + cotisations_salariales
            - hsup + rev_microsocial_declarant1
            )

    def get_output_period(self, period):
        return period


@reference_formula
class salnet(SimpleFormulaColumn):
    column = FloatCol
    label = u"Salaires nets d'après définition INSEE"
    entity_class = Individus

    def function(self, sal, crdssal, csgsali):
        '''
        Calcul du salaire net d'après définition INSEE
        net = net de csg et crds
        '''
        return sal + crdssal + csgsali

    def get_output_period(self, period):
        return period


@reference_formula
class sal_h_b(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire horaire brut"

    def function(self, salbrut):
        nbh_travaillees = 151.67 * 12
        return salbrut / nbh_travaillees

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class alleg_fillon(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement de charges patronales sur les bas et moyens salaires"

    def function(self, period, salbrut, sal_h_b, type_sal, taille_entreprise, cotsoc = law.cotsoc):
        if period.start.year >= 2007:
            # TODO: deal with taux between 2005 and 2007
            taux_fillon = taux_exo_fillon(sal_h_b, taille_entreprise, cotsoc)
            alleg_fillon = (
                taux_fillon
                * salbrut
                * ((type_sal == CAT['prive_non_cadre'])
                    | (type_sal == CAT['prive_cadre']))
                )
            return alleg_fillon
        else:
            return 0 * salbrut

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class alleg_cice(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Crédit d'imôt pour la compétitivité et l'emploi"

    def function(self, period, salbrut, sal_h_b, type_sal, taille_entreprise, cotsoc = law.cotsoc):
        if period.start.year >= 2013:
            taux_cice = taux_exo_cice(sal_h_b, cotsoc)
            alleg_cice = (
                taux_cice
                * salbrut
                * or_((type_sal == CAT['prive_non_cadre']), (type_sal == CAT['prive_cadre']))
                )
            return alleg_cice

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class taxes_sal(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxes sur les salaires"

    def function(self, salbrut, tva_ent, _P):
        P = _P.cotsoc.taxes_sal
        maj = P.taux_maj  # TODO: exonérations apprentis
        taxes_sal = maj.calc(salbrut) + P.taux.metro * salbrut  # TODO: modify if DOM
        return -taxes_sal * not_(tva_ent)

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


@reference_formula
class tehr(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe exceptionnelle de solidarité sur les très hautes rémunérations"

    def function(self, salbrut, _P):
        # TODO: a affiner avec condition de plafond
        #       sur le chiffre d'affaire des entreprises
        bar = _P.cotsoc.tehr
        return -bar.calc(salbrut)

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')  # TODO period


@reference_formula
class salsuperbrut(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires superbruts"

    def function(self, salbrut, primes_fonction_publique, indemnite_residence, supp_familial_traitement, cotisations_patronales,
                 alleg_fillon, alleg_cice, taxes_sal, tehr):
        salsuperbrut = (
            salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement
            - cotisations_patronales - alleg_fillon - alleg_cice - taxes_sal - tehr
            )
#        expression = ("   salbrut             %s \n"
#                      " + cotisations_patronales              %s \n"
#                      " + primes_fonction_publique              %s \n"
#                      " + indemnite_residence %s \n"
#                      " - alleg_fillon        %s \n"
#                      " - alleg_cice          %s \n"
#                      " + taxes_sal           %s \n"
#                      " + tehr                %s \n"
#                      " = salsuperbut         %s") % (salbrut, cotisations_patronales, primes_fonction_publique,
#                                                        indemnite_residence,
#                                                      - alleg_fillon, -alleg_cice, taxes_sal, tehr,
#                                                      salsuperbrut)
#        print expression
        return salsuperbrut

    def get_output_period(self, period):
        return period.start.period(u'month').offset('first-of')


############################################################################
# # Non salariés
############################################################################


@reference_formula
class rev_microsocial(SimpleFormulaColumn):
    """Revenu net des cotisations sociales sous régime microsocial (auto-entrepreneur)"""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu net des cotisations sociales pour le régime microsocial"
    start_date = datetime.date(2009, 1, 1)
    url = u"http://www.apce.com/pid6137/regime-micro-social.html"

    def function(self, assiette_service, assiette_vente, assiette_proflib, _P):
        P = _P.cotsoc.sal.microsocial
        total = assiette_service + assiette_vente + assiette_proflib
        prelsoc_ms = assiette_service * P.servi + assiette_vente * P.vente + assiette_proflib * P.rsi
        return total - prelsoc_ms

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class rev_microsocial_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Revenu net des cotisations sociales sous régime microsocial (auto-entrepreneur) (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = rev_microsocial


############################################################################
# # Helper functions
############################################################################


def taux_exo_fillon(sal_h_b, taille_entreprise, P):
    '''
    Exonération Fillon
    http://www.securite-sociale.fr/comprendre/dossiers/exocotisations/exoenvigueur/fillon.htm
    '''
    # La divison par zéro engendre un warning
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.

    smic_h_b = P.gen.smic_h_b
    Pf = P.exo_bas_sal.fillon
    seuil = Pf.seuil
    tx_max = (
        Pf.tx_max * (taille_entreprise > 2)
        + Pf.tx_max2 * (taille_entreprise <= 2)
        )
    if seuil <= 1:
        return 0
    return (tx_max * min_(1, max_(seuil * smic_h_b / (sal_h_b + 1e-10) - 1, 0)
                          / (seuil - 1)))


def taux_exo_cice(sal_h_b, P):
    smic_h_b = P.gen.smic_h_b
    Pc = P.exo_bas_sal.cice
    plafond = Pc.max * smic_h_b
    taux_cice = (sal_h_b <= plafond) * Pc.taux
    return taux_cice
