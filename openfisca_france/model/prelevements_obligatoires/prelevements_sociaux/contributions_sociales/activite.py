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

from numpy import zeros

from ....base import *  # noqa analysis:ignore
from .base import montant_csg_crds


log = logging.getLogger(__name__)


# TODO: prise_en_charge_employeur_retraite_supplementaire à la CSG/CRDS et au forfait social
# T0D0 : gérer assiette csg


@reference_formula
class csgsald(SimpleFormulaColumn):
    column = FloatCol
    label = u"CSG déductible sur les salaires"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        # indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        # TODO: mettre à part ?
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        hsup = simulation.calculate('hsup', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)

        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_avec_abattement = (
                remuneration_principale + salaire_de_base + primes_fonction_publique + indemnite_residence +
                supp_familial_traitement - hsup
                ),
            base_sans_abattement = - prevoyance_obligatoire_cadre, # TODO + indemnites_journalieres_maladie,
            law_node = law.csg.activite.deductible,
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
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        # indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        # TODO: mettre ailleurs
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)

        hsup = simulation.calculate('hsup', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            law_node = law.csg.activite.imposable,
            base_avec_abattement = (
                salaire_de_base + remuneration_principale +
                primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup
                ),
            base_sans_abattement = - prevoyance_obligatoire_cadre, # TODO: mettre ailleurs + indemnites_journalieres_maladie,
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
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        # indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        # TODO: mettre ailleurs
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        hsup = simulation.calculate('hsup', period)

        remuneration_principale = simulation.calculate('remuneration_principale', period)

        law = simulation.legislation_at(period.start)

        montant_crds = montant_csg_crds(
            law_node = law.crds.activite,
            base_avec_abattement = (
                salaire_de_base + remuneration_principale +
                primes_fonction_publique + indemnite_residence + supp_familial_traitement - hsup
                ),
            base_sans_abattement = - prevoyance_obligatoire_cadre,
            #  + indemnites_journalieres_maladie, TODO: mettre ailleurs
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
        salaire_de_base = simulation.calculate_add('salaire_de_base', period)
        primes_fonction_publique = simulation.calculate_add('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate_add('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate_add('supp_familial_traitement', period)
        csgsald = simulation.calculate_add('csgsald', period)
        cotisations_salariales = simulation.calculate('cotisations_salariales', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)
        hsup = simulation.calculate('hsup', period)
        # Quand sal est calculé sur une année glissante, rev_microsocial_declarant1 est calculé sur l'année légale
        # correspondante. Quand sal est calculé sur un mois, rev_microsocial_declarant1 est calculé par division du
        # montant pour l'année légale.
        rev_microsocial_declarant1 = simulation.calculate_add_divide('rev_microsocial_declarant1',
            period.offset('first-of'))

        return period, (
            salaire_de_base + remuneration_principale +
            primes_fonction_publique + indemnite_residence + supp_familial_traitement + csgsald +
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

        salaire_de_base = simulation.get_array('salaire_de_base', period)
        if salaire_de_base is None:
            return period, zeros(self.holder.entity.count)

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
    url = u"http://vosdroits.service-public.fr/professionnels-entreprises/F32096.xhtml"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        salaire_de_base = simulation.calculate_add('salaire_de_base', period)  # TODO: check base
        law = simulation.legislation_at(period.start)

        bar = law.cotsoc.tehr
        return period, -bar.calc(salaire_de_base)


@reference_formula
class salsuperbrut(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires superbruts/coût du travail"

    def function(self, simulation, period):
        period = period
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        primes_fonction_publique = simulation.calculate_add('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate_add('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate_add('supp_familial_traitement', period)
        cotisations_patronales = simulation.calculate('cotisations_patronales', period)
        depense_cantine_titre_restaurant_employeur = simulation.calculate(
            'depense_cantine_titre_restaurant_employeur', period)
        allegement_fillon = simulation.calculate_add('allegement_fillon', period)
        credit_impot_competitivite_emploi = simulation.calculate_add('credit_impot_competitivite_emploi', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            'reintegration_titre_restaurant_employeur', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)

        taxe_salaires = simulation.calculate('taxe_salaires', period)
        tehr = simulation.calculate_divide('tehr', period)

        salsuperbrut = (
            salaire_de_base + depense_cantine_titre_restaurant_employeur - reintegration_titre_restaurant_employeur +
            remuneration_principale +
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
