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
import math

from numpy import logical_not as not_, logical_or as or_, maximum as max_, minimum as min_


from openfisca_core.accessors import law
from openfisca_core.columns import FloatCol
from openfisca_core.formulas import EntityToPersonColumn, SimpleFormulaColumn
from openfisca_core.taxscales import scale_tax_scales


from ..base import CAT, QUIFAM, QUIFOY, QUIMEN
from ..base import FoyersFiscaux, Individus, reference_formula


CHEF = QUIFAM['chef']
DEBUG_SAL_TYPE = 'public_titulaire_hospitaliere'
log = logging.getLogger(__name__)
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


# TODO: intégrer prise_en_charge_employeur_prevoyance_complementaire
#       et prise_en_charge_employeur_retraite_supplementaire à la CSG/CRDS et au forfait social


@reference_formula
class cotisations_patronales(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"

    def function(self, cotisations_patronales_contributives, cotisations_patronales_non_contributives,
                 cotisations_patronales_main_d_oeuvre):
        return (
            cotisations_patronales_contributives +
            cotisations_patronales_non_contributives +
            cotisations_patronales_main_d_oeuvre
            )

    def get_output_period(self, period):
        return period


@reference_formula
class cotisations_patronales_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales patronales contributives"
    entity_class = Individus

    def function(self, ags, agff_tranche_a_employeur, apec_employeur, arrco_tranche_a_employeur, assedic_employeur,
                 cotisation_exceptionnelle_temporaire_employeur, fonds_emploi_hospitalier, ircantec_employeur,
                 pension_civile_employeur, rafp_employeur, vieillesse_deplafonnee_employeur,
                 vieillesse_plafonnee_employeur):

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
        return cotisations_patronales_contributives

    def get_output_period(self, period):
        return period


@reference_formula
class cotisations_patronales_main_d_oeuvre(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisation sociales patronales main d'oeuvre"
    entity_class = Individus

    def function(self, contribution_developpement_apprentissage,
                 contribution_solidarite_autonomie, contribution_supplementaire_apprentissage,
                 fnal_tranche_a, fnal_tranche_a_plus_20, formation_professionnelle,
                 participation_effort_construction,
                 taxe_apprentissage, versement_transport):

        cotisations_patronales_main_d_oeuvre = (
            contribution_developpement_apprentissage +
            contribution_solidarite_autonomie +
            contribution_supplementaire_apprentissage +
            formation_professionnelle +
            fnal_tranche_a +
            fnal_tranche_a_plus_20 +
            participation_effort_construction +
            taxe_apprentissage +
            versement_transport
            )
        return cotisations_patronales_main_d_oeuvre

    def get_output_period(self, period):
        return period


@reference_formula
class cotisations_patronales_non_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales patronales non-contributives"
    entity_class = Individus

    def function(self, accident_du_travail, allocations_temporaires_invalidite,
                 famille, maladie_employeur):

        cotisations_patronales_non_contributives = (
            allocations_temporaires_invalidite +
            accident_du_travail +
            famille +
            maladie_employeur
            )
        return cotisations_patronales_non_contributives

    def get_output_period(self, period):
        return period


@reference_formula
class cotisations_salariales_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales contributives"
    entity_class = Individus

    def function(self, agff_tranche_a_employe, agirc_tranche_b_employe, apec_employe, arrco_tranche_a_employe,
                 assedic_employe, cotisation_exceptionnelle_temporaire_employe, ircantec_employe,
                 pension_civile_employe, rafp_employe, vieillesse_deplafonnee_employe, vieillesse_plafonnee_employe):

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

        return cotisations_salariales_contributives

    def get_output_period(self, period):
        return period


@reference_formula
class cotisations_salariales_non_contributives(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales non-contributives"
    entity_class = Individus

    def function(self, contribution_exceptionnelle_solidarite_employe, maladie_employe):

        cotisations_salariales_non_contributives = (
            # prive
            maladie_employe +
            # public
            contribution_exceptionnelle_solidarite_employe
            )

        return cotisations_salariales_non_contributives

    def get_output_period(self, period):
        return period


@reference_formula
class cotisations_salariales(SimpleFormulaColumn):
    column = FloatCol
    label = u"Cotisations sociales salariales"
    entity_class = Individus

    def function(self, cotisations_salariales_contributives, cotisations_salariales_non_contributives):
        return cotisations_salariales_contributives + cotisations_salariales_non_contributives

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
            salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement + csgsald +
            cotisations_salariales - hsup + rev_microsocial_declarant1
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

        # mensuel classique : nbhr = nombre d'heures rémunérées sur un mois
        nbhr = 151.67

        # forfait jour nbjf = nombre de jours au forfait jour
        # nbhr = 151.67 * (nbjf / 218) * (52 / 12)

        # forfait heures nbhf = nombre d'heures au forfait heures
        # nbhr = 151.67 * (nbhf / 45.7) * (52 / 12)

        return salbrut / nbhr

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
        return period.start.period(u'year').offset('first-of')  # TODO: period


@reference_formula
class salsuperbrut(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires superbruts"

    def function(self, salbrut, primes_fonction_publique, indemnite_residence, supp_familial_traitement,
            cotisations_patronales, allegement_fillon, alleg_cice, taxes_sal, tehr):
        salsuperbrut = (
            salbrut + primes_fonction_publique + indemnite_residence + supp_familial_traitement
            - cotisations_patronales - allegement_fillon - alleg_cice - taxes_sal - tehr
            )
        return salsuperbrut

    def get_output_period(self, period):
        return period


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


