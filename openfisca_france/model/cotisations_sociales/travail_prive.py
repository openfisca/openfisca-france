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

import logging


from numpy import int16, minimum as min_, ones, round as round_
from openfisca_core.accessors import law
from openfisca_core.enumerations import Enum
from openfisca_core.columns import EnumCol, FloatCol
from openfisca_core.formulas import SimpleFormulaColumn


from ..base import *  # noqa
from . import apply_bareme_for_relevant_type_sal


log = logging.getLogger(__name__)
taux_versement_transport_by_localisation_entreprise = None


# TODO:
# contribution patronale de prévoyance complémentaire
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)


@reference_formula
class accident_du_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations patronales accident du travail et maladie professionelle"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        taux_accident_travail = simulation.calculate('taux_accident_travail', period)

        prive = (type_sal == CAT['prive_cadre']) + (type_sal == CAT['prive_non_cadre'])
        return period, - salbrut * taux_accident_travail * prive  # TODO: check public


@reference_formula
class agff_tranche_a_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage AGFF tranche A (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "agff",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class agff_tranche_a_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage AGFF tranche A (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation_non_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "agffnc",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )

        cotisation_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "agffc",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation_cadre + cotisation_non_cadre


@reference_formula
class agirc_tranche_b_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC tranche B (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "agirc",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class agirc_tranche_b_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC tranche B (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "agirc",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class apec_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations agence pour l'emploi des cadres (APEC, employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "apec",
            base = salbrut,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation  # TODO: check public notamment contractuel


@reference_formula
class ags(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution à l'association pour la gestion du régime de garantie des créances des salariés (AGS, employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "chomfg",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class apec_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations Agenece pour l'emploi des cadres (APEC, employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "apec",
            base = salbrut,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation  # TODO: check public notamment contractuel


@reference_formula
class arrco_tranche_a_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche A (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "arrco",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class arrco_tranche_a_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche A (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "arrco",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class assedic_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage tranche A (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "assedic",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class assedic_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage tranche A (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "assedic",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class conge_individuel_formation_cdd(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution au financement des congé individuel de formation (CIF) des salariées en CDD"

    # TODO: date de début

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        law = simulation.legislation_at(period.start).cotsoc.conge_individuel_formation

        cotisation = - law.cdd * (contrat_de_travail_duree == 1) * (
            salbrut +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
            )
        return period, cotisation


@reference_formula
class contribution_developpement_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution additionnelle au développement de l'apprentissage"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        # TODO: check entreprise redevable
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "apprentissage_add",
            base = redevable_taxe_apprentissage * (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class contribution_solidarite_autonomie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution solidarité autonomie (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "csa",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class cotisation_exceptionnelle_temporaire_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation_exceptionnelle_temporaire (employe)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "cet",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class cotisation_exceptionnelle_temporaire_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation exceptionnelle temporaire (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "cet",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class contribution_supplementaire_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution supplémentaire à l'apprentissage"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        ratio_alternants = simulation.calculate('ratio_alternants', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
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
            taux_contribution = (effectif_entreprise >= 250) * taux.plus_de_250
            # TODO: gestion de la place dans le XML pb avec l'arbe des paramètres / preprocessing
        return period, - taux_contribution * (
            salbrut +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
            )


@reference_formula
class famille(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation famille (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "famille",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class fnal_tranche_a(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation fonds national action logement (FNAL tout employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "fnal1",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation * (taille_entreprise <= 2)


@reference_formula
class fnal_tranche_a_plus_20(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Fonds national action logement (FNAL, employeur avec plus de 20 salariés)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "fnal2",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),  # plus de 20 salariés TODO: Be more explicit
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation * (taille_entreprise > 2)


@reference_formula
class forfait_social(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Forfait social"

    # TODO instaure le 1er janvier 20009
    def function(self, simulation, period):

        assiette = simulation.calculate('prevoyance_obligatoire_cadre', period)  # TODO: complete this
        return period, assiette * .08  # TODO valeur 2014 paramètres varient beaucoup entre 2009 et


@reference_formula
class formation_professionnelle(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Formation professionnelle"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation_0_9 = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "formprof_09",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ) * (taille_entreprise == 1),  # moins de 10 salariés TODO: Be more explicit
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        cotisation_10_19 = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "formprof_1019",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ) * (taille_entreprise == 2),  # moins de 20 salariés TODO: Be more explicit
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        cotisation_20 = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "formprof_20",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ) * (taille_entreprise > 2),  # plus de 20 salariés TODO: Be more explicit
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation_0_9 + cotisation_10_19 + cotisation_20


@reference_formula
class maladie_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "maladie",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class maladie_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "maladie",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class mhsup(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Heures supplémentaires comptées négativement"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        hsup = simulation.calculate('hsup', period)

        return period, -hsup


@reference_formula
class participation_effort_construction(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Participation à l'effort de construction"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "construction",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class plafond_securite_sociale(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Plafond de la securite sociale"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        nombre_jours_calendaires = simulation.calculate('nombre_jours_calendaires', period)
        _P = simulation.legislation_at(period.start)

        plafond_temps_plein = _P.cotsoc.gen.plafond_securite_sociale
        plafond_securite_sociale = min_(nombre_jours_calendaires, 30) / 30 * plafond_temps_plein
        return period, plafond_securite_sociale


@reference_formula
class prevoyance_obligatoire_cadre(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation de prévoyance pour les cadres et assimilés"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        salbrut = simulation.calculate('salbrut', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        prevoyance_obligatoire_cadre_taux = simulation.calculate('prevoyance_obligatoire_cadre_taux', period)

        cotisation = - (
            (type_sal == CAT['prive_cadre']) *
            min_(salbrut, plafond_securite_sociale) *
            prevoyance_obligatoire_cadre_taux
            )
        return period, cotisation


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

    def function(self, simulation, period):
        period = period
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)

        taille_entreprise = (
            (effectif_entreprise > 0).astype(int16) +
            (effectif_entreprise > 10).astype(int16) +
            (effectif_entreprise > 20).astype(int16) +
            (effectif_entreprise > 250).astype(int16)
            )
        return period, taille_entreprise


@reference_formula
class taxe_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "apprentissage",
            base = redevable_taxe_apprentissage * (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


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
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        _P = simulation.legislation_at(period.start)

        bareme = _P.cotsoc.taxes_sal.taux_maj
        bareme.multiply_thresholds(1 / 12, decimals = 2, inplace = True)
        base = salbrut - prevoyance_obligatoire_cadre

        return period, - (
            bareme.calc(
                base,
                round_base_decimals = 2) +
            round_(_P.cotsoc.taxes_sal.taux.metro * base, 2)
            ) * assujettie_taxe_salaires


@reference_formula
class taux_accident_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Approximation du taux accident à partir de l'exposition au risque donnée"
    start_date = date(2012, 1, 1)

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')  # TODO month ?
        exposition_accident = simulation.calculate('exposition_accident', period)
        accident = simulation.legislation_at(period.start).cotsoc.accident

        return period, (exposition_accident == 0) * accident.faible + (exposition_accident == 1) * accident.moyen \
            + (exposition_accident == 2) * accident.eleve + (exposition_accident == 3) * accident.treseleve


@reference_formula
class taux_versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u""

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        localisation_entreprise = simulation.calculate('localisation_entreprise', period)
        _P = simulation.legislation_at(period.start)

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

    #    global taux_versement_transport_by_localisation_entreprise
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
        return period, rate * ones(len(localisation_entreprise))


@reference_formula
class versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Versement transport"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        taux_versement_transport = simulation.calculate('taux_versement_transport', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        base = (
            salbrut +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
            )
        cotisation = - taux_versement_transport * base
        return period, cotisation


@reference_formula
class vieillesse_deplafonnee_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse déplafonnée (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "vieillessedeplaf",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class vieillesse_plafonnee_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse plafonnée (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "vieillesse",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class vieillesse_deplafonnee_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse déplafonnée"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "vieillessedeplaf",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class vieillesse_plafonnee_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse plafonnée (employeur)"


    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "vieillesseplaf",
            base = (
                salbrut +
                (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation
