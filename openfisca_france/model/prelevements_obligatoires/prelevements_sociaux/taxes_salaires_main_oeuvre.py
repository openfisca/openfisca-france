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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import csv
import logging
import pkg_resources

from numpy import fromiter, logical_or as or_, round as round_


import openfisca_france
from ...base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)

taux_aot_by_depcom = None
taux_smt_by_depcom = None


# TODO:
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)

# Helpers

from .cotisations_sociales.base import apply_bareme

# Cotisations proprement dites


@reference_formula
class conge_individuel_formation_cdd(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution au financement des congé individuel de formation (CIF) des salariées en CDD"

    # TODO: date de début
    def function(self, simulation, period):
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        law = simulation.legislation_at(period.start).cotsoc.conge_individuel_formation

        cotisation = - law.cdd * (contrat_de_travail_duree == 1) * assiette_cotisations_sociales
        return period, cotisation


@reference_formula
class contribution_developpement_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution additionnelle au développement de l'apprentissage"

    def function(self, simulation, period):
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "apprentissage_add",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * redevable_taxe_apprentissage


@reference_formula
class contribution_supplementaire_apprentissage(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution supplémentaire à l'apprentissage"

    @dated_function(date(2010, 1, 1))
    def function(self, simulation, period):
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        ratio_alternants = simulation.calculate('ratio_alternants', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        taux = simulation.legislation_at(period.start).cotsoc.contribution_supplementaire_apprentissage

        if period.start.year > 2012:
            taux_contribution = redevable_taxe_apprentissage * (
                (effectif_entreprise < 2000) * (ratio_alternants < .01) * taux.moins_2000_moins_1pc_alternants +
                (effectif_entreprise >= 2000) * (ratio_alternants < .01) * taux.plus_2000_moins_1pc_alternants +
                (.01 <= ratio_alternants) * (ratio_alternants < .02) * taux.entre_1_2_pc_alternants +
                (.02 <= ratio_alternants) * (ratio_alternants < .03) * taux.entre_2_3_pc_alternants +
                (.03 <= ratio_alternants) * (ratio_alternants < .04) * taux.entre_3_4_pc_alternants +
                (.04 <= ratio_alternants) * (ratio_alternants < .05) * taux.entre_4_5_pc_alternants
                )
        else:
            taux_contribution = (effectif_entreprise >= 250) * taux.plus_de_250 * redevable_taxe_apprentissage
            # TODO: gestion de la place dans le XML pb avec l'arbre des paramètres / preprocessing
        return period, - taux_contribution * assiette_cotisations_sociales


@reference_formula
class cotisations_employeur_main_d_oeuvre(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales employeur main d'oeuvre"

    def function(self, simulation, period):
        period = period
        conge_individuel_formation_cdd = simulation.calculate('conge_individuel_formation_cdd', period)
        contribution_developpement_apprentissage = simulation.calculate(
            'contribution_developpement_apprentissage', period)
        contribution_supplementaire_apprentissage = simulation.calculate(
            'contribution_supplementaire_apprentissage', period)
        financement_organisations_syndicales = simulation.calculate('financement_organisations_syndicales', period)
        fnal = simulation.calculate('fnal', period)
        formation_professionnelle = simulation.calculate('formation_professionnelle', period)
        participation_effort_construction = simulation.calculate_add('participation_effort_construction', period)
        prevoyance_obligatoire_cadre = simulation.calculate_add('prevoyance_obligatoire_cadre', period)
        taxe_apprentissage = simulation.calculate_add('taxe_apprentissage', period)
        versement_transport = simulation.calculate_add('versement_transport', period)

        cotisations_employeur_main_d_oeuvre = (
            conge_individuel_formation_cdd +
            contribution_developpement_apprentissage +
            contribution_supplementaire_apprentissage +
            financement_organisations_syndicales +
            fnal +
            formation_professionnelle +
            participation_effort_construction +
            prevoyance_obligatoire_cadre +
            taxe_apprentissage +
            versement_transport
            )
        return period, cotisations_employeur_main_d_oeuvre


@reference_formula
class fnal(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation fonds national action logement (FNAL)"

    def function(self, simulation, period):
        fnal_tranche_a = simulation.calculate('fnal_tranche_a', period)
        fnal_tranche_a_plus_20 = simulation.calculate('fnal_tranche_a_plus_20', period)
        return period, fnal_tranche_a + fnal_tranche_a_plus_20


@reference_formula
class fnal_tranche_a(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation fonds national action logement (FNAL tout employeur)"

    def function(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'fnal1',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * (taille_entreprise <= 2)


@reference_formula
class fnal_tranche_a_plus_20(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Fonds national action logement (FNAL, employeur avec plus de 20 salariés)"

    def function(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'fnal2',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * (taille_entreprise > 2)


@reference_formula
class financement_organisations_syndicales(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution patronale au financement des organisations syndicales"

    @dated_function(date(2015, 1, 1))
    def function(self, simulation, period):
        type_sal = simulation.calculate('type_sal', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'financement_organisations_syndicales',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * or_(type_sal <= 1, type_sal == 6)


@reference_formula
class formation_professionnelle(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Formation professionnelle"

    def function(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation_0_9 = (taille_entreprise == 1) * apply_bareme(
            simulation,
            period, cotisation_type = 'employeur',
            bareme_name = 'formprof_09',
            variable_name = self.__class__.__name__,
            )
        cotisation_10_19 = (taille_entreprise == 2) * apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_1019',
            variable_name = self.__class__.__name__,
            )
        cotisation_20 = (taille_entreprise > 2) * apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_20',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation_0_9 + cotisation_10_19 + cotisation_20


@reference_formula
class participation_effort_construction(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Participation à l'effort de construction"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'construction',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class taxe_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage',
            variable_name = self.__class__.__name__,
            )
        return period, redevable_taxe_apprentissage * cotisation


@reference_formula
class taxe_salaires(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe sur les salaires"
# Voir
# http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8920/fichedescriptiveformulaire_8920.pdf

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assujettie_taxe_salaires = simulation.calculate('assujettie_taxe_salaires', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        law = simulation.legislation_at(period.start)

        bareme = law.cotsoc.taxes_sal.taux_maj
        base = assiette_cotisations_sociales - prevoyance_obligatoire_cadre
        # TODO: exonérations apprentis
        # TODO: modify if DOM

        return period, - (
            bareme.calc(
                base,
                factor = 1 / 12,
                round_base_decimals = 2
                ) +
            round_(law.cotsoc.taxes_sal.taux.metro * base, 2)
            ) * assujettie_taxe_salaires


@reference_formula
class taux_versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u""

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        depcom_entreprise = simulation.calculate('depcom_entreprise', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        type_sal = simulation.calculate('type_sal', period)

        preload_taux_versement_transport()
        public = (type_sal >= 2)
        default_value = 0.0
        taux_aot = fromiter(
            (
                taux_aot_by_depcom.get(depcom_cell, default_value)
                for depcom_cell in depcom_entreprise
                ),
            dtype = 'float',
            )
        taux_smt = fromiter(
            (
                taux_smt_by_depcom.get(depcom_cell, default_value)
                for depcom_cell in depcom_entreprise
                ),
            dtype = 'float',
            )
        # "L'entreprise emploie-t-elle plus de 9 salariés  dans le périmètre de l'Autorité organisatrice de transport
        # (AOT) suivante ou syndicat mixte de transport (SMT)"
        return period, (taux_aot + taux_smt) * or_(effectif_entreprise > 9, public) / 100


@reference_formula
class versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Versement transport"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        taux_versement_transport = simulation.calculate('taux_versement_transport', period)
        cotisation = - taux_versement_transport * assiette_cotisations_sociales
        return period, cotisation


def preload_taux_versement_transport():
    global taux_aot_by_depcom
    global taux_smt_by_depcom
    if taux_aot_by_depcom is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/versement_transport/taux.csv',
                ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            taux_aot_by_depcom = {
                row['code INSEE']: float(row['taux'] or 0)  # autorité organisatrice des transports
                for row in csv_reader
                }
    if taux_smt_by_depcom is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/versement_transport/taux.csv',
                ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            taux_smt_by_depcom = {
                row['code INSEE']: float(row['taux additionnel'] or 0)  # syndicat mixte de transport
                for row in csv_reader
                }
