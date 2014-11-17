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

from numpy import fromiter, logical_not as not_, logical_or as or_, ones, maximum as max_, minimum as min_, zeros
from openfisca_core import periods
from openfisca_core.accessors import law
from openfisca_core.columns import FloatCol
from openfisca_core.formulas import SimpleFormulaColumn
from openfisca_core.enumerations import Enum
from openfisca_core.taxscales import TaxScalesTree, scale_tax_scales

from ..input_variables.base import QUIFAM, QUIFOY, QUIMEN
from ..base import Individus, reference_formula

TAUX_DE_PRIME = 1 / 4  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute

CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])
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
        bareme = bareme_by_type_sal_name[type_sal_enum[0]].get(bareme_name)
        if bareme:
            cotisation += bareme.calc(base) * (type_sal == type_sal_enum[1])
            if bareme.name == "arcco":
                print type_sal
                print base
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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


@reference_formula
class ags(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution à l'association pour la gestion du régime de Garantie des créances des Salariés (AGS)"

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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


@reference_formula
class taxe_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"

    def function(self, redevable_taxe_apprentissage, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, _P):
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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat_contrib(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales contributives"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, rafp_employeur,
                 pension_civile_employeur, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotpat = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    if category[0] in ["prive_cadre", "prive_non_cadre", "public_non_titulaire", "public_titulaire_hospitaliere"]:  # TODO: move up
                        is_contrib = (bar.option == "contrib") & (bar.name not in ['cnracl', 'rafp', 'pension'])
                        temp = -(iscat
                                 * bar.calc(salbrut + (category[0] == 'public_non_titulaire')
                                 * (indemnite_residence + primes_fonction_publique))
                                 ) * is_contrib
                        cotpat += temp
    #                    if is_contrib == 1:
    #                        if category[0] == DEBUG_SAL_TYPE:
    #                            if (temp != 0).all():
    #                                log.info(bar)
    #                                log.info(temp / 12)

    #        if category[0] == DEBUG_SAL_TYPE:
    #            log.info("rafp pat: %s" % str(rafp_employeur / 12))
    #            log.info("pension civile pat: %s" % str(pension_civile_employeur / 12))

        cotpat += rafp_employeur + pension_civile_employeur
        return cotpat

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat_main_d_oeuvre(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales main d'oeuvre"

    # TODO: A discriminer selon la taille de l'entreprise
    # Il s'agit de prélèvements sur les salaires que la CN ne classe pas dans les cotisations sociales
    #  En particulier, la CN classe:
    #     - D291: taxe sur les salaire, versement transport, FNAL, CSA, taxe d'apprentissage, formation continue
    #     - D993: participation à l'effort de construction

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cotpat_transport, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotpat = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_mo = (bar.option == "main-d-oeuvre")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes_fonction_publique))
                             * is_mo)
                    cotpat += temp
    #                if is_mo == 1:
    #                    if  category[0] == DEBUG_SAL_TYPE:
    #                        log.info(category[0])
    #                        log.info(bar.name)
    #                        log.info(temp / 12)
        return cotpat + cotpat_transport

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Versement transport"

    def function(self, salbrut, hsup, type_sal, indemnite_residence, primes_fonction_publique, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        transport = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index of the category
            if category[0] in pat.keys():  # category[0] is the name of the category
                if 'transport' in pat[category[0]]:
                    bar = pat[category[0]]['transport']
                    temp = -bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes_fonction_publique)) * iscat  # check
                    transport += temp
    #                if  category[0] == DEBUG_SAL_TYPE:
    #                    log.info(category[0])
    #                    log.info(bar.name)
    #                    log.info(temp / 12)
        return transport

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class taux_accident_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Approximation du taux accident à partir de l'exposition au risque donnée"

    def function(self, exposition_accident, period, accident = law.cotsoc.accident):
        if periods.date(period).year >= 2012:
            return (exposition_accident == 0) * accident.faible + (exposition_accident == 1) * accident.moyen \
                + (exposition_accident == 2) * accident.eleve + (exposition_accident == 3) * accident.treseleve
        else:
            return 0 * exposition_accident

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat_accident(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations patronales accident du travail et maladie professionelle"

    def function(self, salbrut, type_sal, taux_accident_travail):
        prive = (type_sal == CAT['prive_cadre']) + (type_sal == CAT['prive_non_cadre'])
        return -salbrut * taux_accident_travail * prive  # TODO: check public

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat_noncontrib(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales non contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cotpat_accident, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotpat = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_noncontrib = (bar.option == "noncontrib")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes_fonction_publique))
                             * is_noncontrib)
    #                log.info(temp)
    #                log.info("\n \n")
                    cotpat += temp
    #                if is_noncontrib == 1:
    #                    if  category[0] == DEBUG_SAL_TYPE:
    #                        log.info(category[0])
    #                        log.info(bar)
    #                        log.info(temp / 12)
    #                        log.info("\n \n")

    #    log.info("accident : %s" % cotpat_accident)
        return cotpat + cotpat_accident

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"

    def function(self, cotpat_contrib, cotpat_noncontrib, cotpat_main_d_oeuvre):
        return cotpat_contrib + cotpat_noncontrib + cotpat_main_d_oeuvre

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class seuil_fds(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul du seuil mensuel d'assujetissement à la contribution au fond de solidarité"

    def function(self, _P):
        from math import floor
        ind_maj_ref = _P.cotsoc.sal.fonc.commun.ind_maj_ref
        pt_ind = _P.cotsoc.sal.fonc.commun.pt_ind
        seuil_mensuel = floor((pt_ind * ind_maj_ref) / 12)
        return seuil_mensuel

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotsal_contrib(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cot_sal_rafp, pension_civile_employe, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        cotsal = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_contrib = (bar.option == "contrib") & (bar.name not in ["rafp", "pension", "cnracl1", "cnracl2"])  # dealed by pension civile and rafp
                    temp = -(iscat
                             * bar.calc(salbrut - hsup
                                        + (category[0] == 'public_non_titulaire') * (indemnite_residence + primes_fonction_publique))
                            ) * is_contrib
                    cotsal += temp
    #                log.info(bar)
    #                log.info(temp)
    #                if  category[0] == DEBUG_SAL_TYPE:
    #                    if (temp != 0).all():
    #                        log.info(category[0])
    #                        log.info(bar.name)
    #                        log.info(temp / 12)

    #        if category[0] == DEBUG_SAL_TYPE:
    #            log.info("pension_civile_employe %s" % str(pension_civile_employe / 12))
    #            log.info("rafp sal %s" % str(cot_sal_rafp / 12))

        public_titulaire = (
            (type_sal == CAT['public_titulaire_etat'])
            + (type_sal == CAT['public_titulaire_territoriale'])
            + (type_sal == CAT['public_titulaire_hospitaliere']))

        return cotsal + (pension_civile_employe + cot_sal_rafp) * public_titulaire

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class pension_civile_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pension civile employé"

    def function(self, salbrut, type_sal, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        terr_or_hosp = (
            type_sal == CAT['public_titulaire_territoriale']) | (type_sal == CAT['public_titulaire_hospitaliere'])
        pension_civile_employe = (
            (type_sal == CAT['public_titulaire_etat']) * sal['public_titulaire_etat']['pension'].calc(salbrut)
            + terr_or_hosp * sal['public_titulaire_territoriale']['cnracl1'].calc(salbrut)
            )
    #    if array(type_sal == DEBUG_SAL_TYPE).all():
    #        log.info('pension_civile_employe %s', pension_civile_employe / 12)

        return -pension_civile_employe

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cot_sal_rafp(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part salariale de la retraite additionelle de la fonction publique"

    def function(self, salbrut, type_sal, primes_fonction_publique, supp_familial_traitement, indemnite_residence, _P):
        eligibles = ((type_sal == CAT['public_titulaire_etat'])
                     + (type_sal == CAT['public_titulaire_territoriale'])
                     + (type_sal == CAT['public_titulaire_hospitaliere']))
        tib = salbrut * eligibles / 12

        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        plaf_ss = _P.cotsoc.gen.plaf_ss
        sal = scale_tax_scales(TaxScalesTree('sal', _P.cotsoc.sal), plaf_ss)
        assiette = min_(base_imposable / 12, plaf_ass * tib)
        # Même régime pour etat et colloc
        cot_sal_rafp = eligibles * sal['fonc']['etat']['rafp'].calc(assiette)
        return -12 * cot_sal_rafp

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotsal_noncontrib(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales non-contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cot_sal_rafp,
                 pension_civile_employe, cotsal_contrib, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        cotsal = zeros(len(salbrut))
        seuil_assuj_fds = seuil_fds(_P)
    #    log.info("seuil assujetissement FDS %i", seuil_assuj_fds)
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_exempt_fds = (category[0] in ['public_titulaire_etat', 'public_titulaire_territoriale', 'public_titulaire_hospitaliere']) * (bar.name == 'solidarite') * ((salbrut - hsup) / 12 <= seuil_assuj_fds)  # TODO: check assiette voir IPP
                    is_noncontrib = (bar.option == "noncontrib")  # and (bar.name in ["famille", "maladie"])
                    temp = -(iscat
                             * bar.calc(salbrut + primes_fonction_publique + indemnite_residence
                                        - hsup + cot_sal_rafp + pension_civile_employe
                                        + cotsal_contrib * (category[0] == 'public_non_titulaire') * (bar.name == "excep_solidarite"))  # * (category[0] == 'public_non_titulaire')
                             * is_noncontrib * not_(is_exempt_fds)
                             )
                    cotsal += temp
    #                if  category[0] == DEBUG_SAL_TYPE:
    #                    if (temp != 0).all():
    #                        log.info(category[0])
    #                        log.info(bar)
    #                        log.info(temp / 12)

        return cotsal

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotsal(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales"

    def function(self, cotsal_contrib, cotsal_noncontrib):
        return cotsal_contrib + cotsal_noncontrib

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class csgsald(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG deductible sur les salaires"

    def function(self, salbrut, primes_fonction_publique, indemnite_residence, supp_familial_traitement, hsup, _P):
        plaf_ss = _P.cotsoc.gen.plaf_ss
        csg = scale_tax_scales(_P.csg.act.deduc, plaf_ss)
        return -12 * csg.calc(
            (salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup) / 12
            )

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class csgsali(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CSG imposable sur les salaires"

    def function(self, salbrut, hsup, primes_fonction_publique, indemnite_residence, supp_familial_traitement, _P):
        plaf_ss = _P.cotsoc.gen.plaf_ss
        csg = scale_tax_scales(_P.csg.act.impos, plaf_ss)
        return -12 * csg.calc(
            (
                salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup
                ) / 12
            )

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class crdssal(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"CRDS sur les salaires"

    def function(self, salbrut, hsup, primes_fonction_publique, indemnite_residence, supp_familial_traitement, _P):
        plaf_ss = _P.cotsoc.gen.plaf_ss
        crds = scale_tax_scales(_P.crds.act, plaf_ss)
        return -12 * crds.calc(
            (
                salbrut - hsup + primes_fonction_publique + indemnite_residence + supp_familial_traitement
                ) / 12
            )

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


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
        if periods.date(period).year >= 2007:
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
        return period.start.period(u'year').offset('first-of')


@reference_formula
class alleg_cice(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Crédit d'imôt pour la compétitivité et l'emploi"

    def function(self, period, salbrut, sal_h_b, type_sal, taille_entreprise, cotsoc = law.cotsoc):
        if periods.date(period).year >= 2013:
            taux_cice = taux_exo_cice(sal_h_b, cotsoc)
            alleg_cice = (
                taux_cice
                * salbrut
                * or_((type_sal == CAT['prive_non_cadre']), (type_sal == CAT['prive_cadre']))
                )
            return alleg_cice

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


@reference_formula
class sal(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul du salaire imposable"

    def function(self, salbrut, primes_fonction_publique, indemnite_residence, supp_familial_traitement,
                 csgsald, cotsal, hsup, rev_microsocial):
        return (salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement
                + csgsald + cotsal - hsup)

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class salnet(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul du salaire net d'après définition INSEE"

    def function(self, sal, crdssal, csgsali):
        return sal + crdssal + csgsali

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class salsuperbrut(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires superbruts"

    def function(self, salbrut, primes_fonction_publique, indemnite_residence, supp_familial_traitement, cotpat,
                 alleg_fillon, alleg_cice, taxes_sal, tehr):
        salsuperbrut = (
            salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement
            - cotpat - alleg_fillon - alleg_cice - taxes_sal - tehr
            )
    #    expression = ("   salbrut             %s \n"
    #                  " + cotpat              %s \n"
    #                  " + primes_fonction_publique              %s \n"
    #                  " + indemnite_residence %s \n"
    #                  " - alleg_fillon        %s \n"
    #                  " - alleg_cice          %s \n"
    #                  " + taxes_sal           %s \n"
    #                  " + tehr                %s \n"
    #                  " = salsuperbut         %s") % (salbrut / 12, cotpat / 12, primes_fonction_publique / 12, indemnite_residence / 12,
    #                                                  - alleg_fillon / 12, -alleg_cice / 12, taxes_sal / 12, tehr / 12,
    #                                                  salsuperbrut / 12)
    #    log.info(expression)
        return salsuperbrut

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class pension_civile_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pension civile part patronale"

    def function(self, salbrut, type_sal, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        terr_or_hosp = (
            type_sal == CAT['public_titulaire_territoriale']
            ) | (
            type_sal == CAT['public_titulaire_hospitaliere']
            )
        pension_civile_employeur = (
            (type_sal == CAT['public_titulaire_etat']) * pat['public_titulaire_etat']['pension'].calc(salbrut)
            + terr_or_hosp * pat['public_titulaire_territoriale']['cnracl'].calc(salbrut)
            )
        return -pension_civile_employeur

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


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
        tib = salbrut * eligibles / 12
        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        plaf_ss = _P.cotsoc.gen.plaf_ss  # TODO: build somewhere else
        pat = scale_tax_scales(TaxScalesTree('pat', _P.cotsoc.pat), plaf_ss)
        assiette = min_(base_imposable / 12, plaf_ass * tib)

        bareme_rafp = _P.cotsoc.cotisations_employeur.public_titulaire_etat['rafp']
        rafp_employeur = eligibles * bareme_rafp.calc(assiette)
        return -12 * rafp_employeur

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


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
        return period.start.period(u'year').offset('first-of')


def _traitement_brut_mensuel( indice_maj, _P):
        Indice_majore_100 = _P.fonc.IM_100
        traitement_brut = Indice_majore_100 * indice_maj / 1200
        return traitement_brut


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

        plancher_mensuel_1 = part_fixe
        plancher_mensuel_2 = part_fixe + _traitement_brut_mensuel(indice_maj_min, _P) * pct_variable_2
        plancher_mensuel_3 = part_fixe + _traitement_brut_mensuel(indice_maj_min, _P) * pct_variable_3
        plancher_mensuel_supp = _traitement_brut_mensuel(indice_maj_min, _P) * pct_variable_supp

        plancher = (plancher_mensuel_1 * (fonc_nbenf == 1) +
                    plancher_mensuel_2 * (fonc_nbenf == 2) +
                    plancher_mensuel_3 * (fonc_nbenf >= 3) +
                    plancher_mensuel_supp * max_(0, fonc_nbenf - 3))

        plafond_mensuel_1 = part_fixe
        plafond_mensuel_2 = part_fixe + _traitement_brut_mensuel(indice_maj_max, _P) * pct_variable_2
        plafond_mensuel_3 = part_fixe + _traitement_brut_mensuel(indice_maj_max, _P) * pct_variable_3
        plafond_mensuel_supp = _traitement_brut_mensuel(indice_maj_max, _P) * pct_variable_supp

        plafond = (plafond_mensuel_1 * (fonc_nbenf == 1) + plafond_mensuel_2 * (fonc_nbenf == 2) +
                   plafond_mensuel_3 * (fonc_nbenf == 3) +
                   plafond_mensuel_supp * max_(0, fonc_nbenf - 3))

        sft = min_(max_(part_fixe + pct_variable * salbrut / 12, plancher), plafond) * (type_sal >= 2)
        # Nota Bene:
        # type_sal is an EnumCol which enum is:
        # CAT = Enum(['prive_non_cadre',
        #             'prive_cadre',
        #             'public_titulaire_etat',
        #             'public_titulaire_militaire',
        #             'public_titulaire_territoriale',
        #             'public_titulaire_hospitaliere',
        #             'public_non_titulaire'])
        return 12 * sft

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
        return 12 * max_(plancher, taux * salbrut / 12) * (type_sal >= 2)

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class indice_majore(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indice majoré"

    def function(self, type_sal, salbrut, _P):
        traitement_annuel_brut = _P.fonc.IM_100
        return (salbrut * 1200 / traitement_annuel_brut) * (type_sal >= 2)

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


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

############################################################################
# # Non salariés
############################################################################


@reference_formula
class rev_microsocial(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu net des cotisations sociales sous régime microsocial (auto-entrepreneur)"

    def function(self, assiette_service, assiette_vente, assiette_proflib, _P):
        P = _P.cotsoc.sal.microsocial
        total = assiette_service + assiette_vente + assiette_proflib
        prelsoc_ms = assiette_service * P.servi + assiette_vente * P.vente + assiette_proflib * P.rsi
        return self.cast_from_entity_to_role(total - prelsoc_ms,
                                             entity = 'foyer_fiscal', role = VOUS)

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')

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
