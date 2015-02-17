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

from ..base import *  # noqa
from .base import montant_csg_crds


log = logging.getLogger(__name__)


# TODO: prise_en_charge_employeur_retraite_supplementaire à la CSG/CRDS et au forfait social
# T0D0 : gérer assiette csg


@reference_formula
class cotisations_patronales(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"

    def function(self, simulation, period):
        period = period
        cotisations_patronales_contributives = simulation.calculate('cotisations_patronales_contributives', period)
        cotisations_patronales_non_contributives = simulation.calculate(
            'cotisations_patronales_non_contributives', period)
        cotisations_patronales_main_d_oeuvre = simulation.calculate('cotisations_patronales_main_d_oeuvre', period)

        return period, (
            cotisations_patronales_contributives +
            cotisations_patronales_non_contributives +
            cotisations_patronales_main_d_oeuvre
            )


@reference_formula
class cotisations_patronales_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales patronales contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        ags = simulation.calculate('ags', period)
        agff_tranche_a_employeur = simulation.calculate('agff_tranche_a_employeur', period)
        apec_employeur = simulation.calculate('apec_employeur', period)
        arrco_tranche_a_employeur = simulation.calculate('arrco_tranche_a_employeur', period)
        assedic_employeur = simulation.calculate('assedic_employeur', period)
        cotisation_exceptionnelle_temporaire_employeur = simulation.calculate(
            'cotisation_exceptionnelle_temporaire_employeur', period)
        fonds_emploi_hospitalier = simulation.calculate('fonds_emploi_hospitalier', period)
        ircantec_employeur = simulation.calculate('ircantec_employeur', period)
        pension_civile_employeur = simulation.calculate('pension_civile_employeur', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        rafp_employeur = simulation.calculate('rafp_employeur', period)
        vieillesse_deplafonnee_employeur = simulation.calculate('vieillesse_deplafonnee_employeur', period)
        vieillesse_plafonnee_employeur = simulation.calculate('vieillesse_plafonnee_employeur', period)

        cotisations_patronales_contributives = (
            # prive
            ags +
            agff_tranche_a_employeur +
            apec_employeur +
            arrco_tranche_a_employeur +
            assedic_employeur +
            cotisation_exceptionnelle_temporaire_employeur +
            vieillesse_deplafonnee_employeur +
            vieillesse_plafonnee_employeur +
            # public
            fonds_emploi_hospitalier +
            ircantec_employeur +
            pension_civile_employeur +
            rafp_employeur
            )
        return period, cotisations_patronales_contributives


@reference_formula
class cotisations_patronales_main_d_oeuvre(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisation sociales patronales main d'oeuvre"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        conge_individuel_formation_cdd = simulation.calculate('conge_individuel_formation_cdd', period)
        contribution_developpement_apprentissage = simulation.calculate(
            'contribution_developpement_apprentissage', period)
        contribution_solidarite_autonomie = simulation.calculate('contribution_solidarite_autonomie', period)
        contribution_supplementaire_apprentissage = simulation.calculate(
            'contribution_supplementaire_apprentissage', period)
        fnal_tranche_a = simulation.calculate('fnal_tranche_a', period)
        fnal_tranche_a_plus_20 = simulation.calculate('fnal_tranche_a_plus_20', period)
        formation_professionnelle = simulation.calculate('formation_professionnelle', period)
        participation_effort_construction = simulation.calculate('participation_effort_construction', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre')
        taxe_apprentissage = simulation.calculate('taxe_apprentissage', period)
        versement_transport = simulation.calculate('versement_transport', period)

        cotisations_patronales_main_d_oeuvre = (
            conge_individuel_formation_cdd +
            contribution_developpement_apprentissage +
            contribution_solidarite_autonomie +
            contribution_supplementaire_apprentissage +
            formation_professionnelle +
            fnal_tranche_a +
            fnal_tranche_a_plus_20 +
            participation_effort_construction +
            prevoyance_obligatoire_cadre +
            taxe_apprentissage +
            versement_transport
            )
        return period, cotisations_patronales_main_d_oeuvre


@reference_formula
class cotisations_patronales_non_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales patronales non-contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        accident_du_travail = simulation.calculate('accident_du_travail', period)
        allocations_temporaires_invalidite = simulation.calculate('allocations_temporaires_invalidite', period)
        famille = simulation.calculate('famille', period)
        maladie_employeur = simulation.calculate('maladie_employeur', period)
        taxe_salaires = simulation.calculate('taxe_salaires', period)

        cotisations_patronales_non_contributives = (
            allocations_temporaires_invalidite +
            accident_du_travail +
            famille +
            maladie_employeur +
            taxe_salaires
            )
        return period, cotisations_patronales_non_contributives


@reference_formula
class cotisations_salariales_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        agff_tranche_a_employe = simulation.calculate_add('agff_tranche_a_employe', period)
        agirc_tranche_b_employe = simulation.calculate_add('agirc_tranche_b_employe', period)
        apec_employe = simulation.calculate_add('apec_employe', period)
        arrco_tranche_a_employe = simulation.calculate_add('arrco_tranche_a_employe', period)
        assedic_employe = simulation.calculate_add('assedic_employe', period)
        cotisation_exceptionnelle_temporaire_employe = simulation.calculate_add(
            'cotisation_exceptionnelle_temporaire_employe', period)
        ircantec_employe = simulation.calculate_add('ircantec_employe', period)
        pension_civile_employe = simulation.calculate_add('pension_civile_employe', period)
        rafp_employe = simulation.calculate_add('rafp_employe', period)
        vieillesse_deplafonnee_employe = simulation.calculate_add('vieillesse_deplafonnee_employe', period)
        vieillesse_plafonnee_employe = simulation.calculate_add('vieillesse_plafonnee_employe', period)

        cotisations_salariales_contributives = (
            # prive
            agff_tranche_a_employe +
            agirc_tranche_b_employe +
            apec_employe +
            arrco_tranche_a_employe +
            assedic_employe +
            cotisation_exceptionnelle_temporaire_employe +
            vieillesse_deplafonnee_employe +
            vieillesse_plafonnee_employe +
            # public
            ircantec_employe +
            pension_civile_employe +
            rafp_employe
            )

        return period, cotisations_salariales_contributives


@reference_formula
class cotisations_salariales_non_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales non-contributives"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        contribution_exceptionnelle_solidarite_employe = simulation.calculate_add(
            'contribution_exceptionnelle_solidarite_employe', period)
        maladie_employe = simulation.calculate_add('maladie_employe', period)

        cotisations_salariales_non_contributives = (
            # prive
            maladie_employe +
            # public
            contribution_exceptionnelle_solidarite_employe
            )

        return period, cotisations_salariales_non_contributives


@reference_formula
class cotisations_salariales(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        cotisations_salariales_contributives = simulation.calculate('cotisations_salariales_contributives', period)
        cotisations_salariales_non_contributives = simulation.calculate(
            'cotisations_salariales_non_contributives', period)

        return period, cotisations_salariales_contributives + cotisations_salariales_non_contributives


@reference_formula
class csgsald(SimpleFormulaColumn):
    column = FloatCol
    label = u"CSG déductible sur les salaires"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        hsup = simulation.calculate('hsup', period)
        law = simulation.legislation_at(period.start)
        montant_csg = montant_csg_crds(
            law_node = law.csg.activite.deductible,
            base_avec_abattement = (
                salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup
                ),
            base_sans_abattement = - prevoyance_obligatoire_cadre + indemnites_journalieres_maladie,
            plafond_securite_sociale = plafond_securite_sociale,
            )
        return period, montant_csg


@reference_formula
class csgsali(SimpleFormulaColumn):
    column = FloatCol
    label = u"CSG imposables sur les salaires"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        hsup = simulation.calculate('hsup', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            law_node = law.csg.activite.imposable,
            base_avec_abattement = (
                salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup
                ),
            base_sans_abattement = - prevoyance_obligatoire_cadre + indemnites_journalieres_maladie,
            plafond_securite_sociale = plafond_securite_sociale,
            )

        return period, montant_csg


@reference_formula
class crdssal(SimpleFormulaColumn):
    column = FloatCol
    label = u"CRDS sur les salaires"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        hsup = simulation.calculate('hsup', period)
        law = simulation.legislation_at(period.start)

        montant_crds = montant_csg_crds(
            law_node = law.crds.activite,
            base_avec_abattement = (
                salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup
                ),
            base_sans_abattement = - prevoyance_obligatoire_cadre + indemnites_journalieres_maladie,
            plafond_securite_sociale = plafond_securite_sociale,
            )

        return period, montant_crds


@reference_formula
class sal(SimpleFormulaColumn):
    column = FloatCol
    label = u"Salaires imposables"
    entity_class = Individus

    def function(self, simulation, period):
        period = period
        salbrut = simulation.calculate_add('salbrut', period)
        primes_fonction_publique = simulation.calculate_add('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate_add('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate_add('supp_familial_traitement', period)
        csgsald = simulation.calculate_add('csgsald', period)
        cotisations_salariales = simulation.calculate('cotisations_salariales', period)
        hsup = simulation.calculate('hsup', period)
        # Quand sal est calculé sur une année glissante, rev_microsocial_declarant1 est calculé sur l'année légale
        # correspondante. Quand sal est calculé sur un mois, rev_microsocial_declarant1 est calculé par division du
        # montant pour l'année légale.
        rev_microsocial_declarant1 = simulation.calculate_add_divide('rev_microsocial_declarant1',
            period.offset('first-of'))

        return period, (
            salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement + csgsald +
            cotisations_salariales - hsup + rev_microsocial_declarant1
            )


@reference_formula
class salnet(SimpleFormulaColumn):
    column = FloatCol
    label = u"Salaires nets d'après définition INSEE"
    entity_class = Individus

    def function(self, simulation, period):
        '''
        Calcul du salaire net d'après définition INSEE
        net = net de csg et crds
        '''
        period = period
        sal = simulation.calculate('sal', period)
        crdssal = simulation.calculate_add('crdssal', period)
        csgsali = simulation.calculate_add('csgsali', period)

        return period, sal + crdssal + csgsali


@reference_formula
class salaire_net_a_payer(SimpleFormulaColumn):
    column = FloatCol
    label = u"Salaires nets d'après définition INSEE"
    entity_class = Individus

    def function(self, simulation, period):
        '''
        Calcul du salaire net à payer après déduction des sommes
        dues par les salarié avancées par l'employeur
        '''
        period = period
        salnet = simulation.calculate('salnet', period)
        depense_cantine_titre_restaurant_employe = simulation.calculate(
            'depense_cantine_titre_restaurant_employe')
        indemnites_forfaitaires = simulation.calculate('indemnites_forfaitaires', period)    
        salaire_net_a_payer = (
            salnet +
            depense_cantine_titre_restaurant_employe +
            indemnites_forfaitaires
            )
        return period, salaire_net_a_payer


@reference_formula
class tehr(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe exceptionnelle de solidarité sur les très hautes rémunérations"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')  # TODO: period
        salbrut = simulation.calculate('salbrut', period)
        law = simulation.legislation_at(period.start)

        bar = law.cotsoc.tehr
        return period, -bar.calc(salbrut)


@reference_formula
class salsuperbrut(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires superbruts/coût du travail"

    def function(self, simulation, period):
        period = period
        salbrut = simulation.calculate('salbrut', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        cotisations_patronales = simulation.calculate('cotisations_patronales', period)
        depense_cantine_titre_restaurant_employeur = simulation.calculate(
            'depense_cantine_titre_restaurant_employeur', period)
        allegement_fillon = simulation.calculate('allegement_fillon', period)
        credit_impot_competitivite_emploi = simulation.calculate('credit_impot_competitivite_emploi', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            'reintegration_titre_restaurant_employeur', period)
        taxe_salaires = simulation.calculate('taxe_salaires', period)
        tehr = simulation.calculate('tehr', period)

        salsuperbrut = (
            salbrut + depense_cantine_titre_restaurant_employeur - reintegration_titre_restaurant_employeur +
            primes_fonction_publique + indemnite_residence + supp_familial_traitement +
            - cotisations_patronales
            - allegement_fillon - credit_impot_competitivite_emploi - taxe_salaires - tehr
            )

        return period, salsuperbrut


############################################################################
# # Non salariés
############################################################################


@reference_formula
class rev_microsocial(SimpleFormulaColumn):
    """Revenu net des cotisations sociales sous régime microsocial (auto-entrepreneur)"""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu net des cotisations sociales pour le régime microsocial"
    start_date = date(2009, 1, 1)
    url = u"http://www.apce.com/pid6137/regime-micro-social.html"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        assiette_service = simulation.calculate('assiette_service', period)
        assiette_vente = simulation.calculate('assiette_vente', period)
        assiette_proflib = simulation.calculate('assiette_proflib', period)
        _P = simulation.legislation_at(period.start)

        P = _P.cotsoc.sal.microsocial
        total = assiette_service + assiette_vente + assiette_proflib
        prelsoc_ms = assiette_service * P.servi + assiette_vente * P.vente + assiette_proflib * P.rsi
        return period, total - prelsoc_ms


@reference_formula
class rev_microsocial_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Revenu net des cotisations sociales sous régime microsocial (auto-entrepreneur) (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = rev_microsocial
