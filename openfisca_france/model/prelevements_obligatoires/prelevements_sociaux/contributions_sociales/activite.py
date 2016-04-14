# -*- coding: utf-8 -*-

from __future__ import division


import logging

from ....base import *  # noqa analysis:ignore
from .base import montant_csg_crds


log = logging.getLogger(__name__)


# TODO: prise_en_charge_employeur_retraite_supplementaire à la CSG/CRDS et au forfait social


class assiette_csg_abattue(Variable):
    column = FloatCol
    label = u"Assiette CSG - CRDS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        primes_salaires = simulation.calculate('primes_salaires', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        # indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        # TODO: mettre à part ?
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        hsup = simulation.calculate('hsup', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)
        stage_gratification_reintegration = simulation.calculate('stage_gratification_reintegration', period)
        indemnite_fin_contrat = simulation.calculate('indemnite_fin_contrat', period)

        return period, (
            remuneration_principale + salaire_de_base + primes_salaires + primes_fonction_publique +
            indemnite_residence + stage_gratification_reintegration + supp_familial_traitement - hsup +
            indemnite_fin_contrat
            )


class assiette_csg_non_abattue(Variable):
    column = FloatCol
    label = u"Assiette CSG - CRDS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        # TODO + indemnites_journalieres_maladie,
        return period, - prevoyance_obligatoire_cadre


class csg_deductible_salaire(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    label = u"CSG déductible sur les salaires"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        assiette_csg_abattue = simulation.calculate('assiette_csg_abattue', period)
        assiette_csg_non_abattue = simulation.calculate('assiette_csg_non_abattue', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)

        law = simulation.legislation_at(period.start)
        montant_csg = montant_csg_crds(
            base_avec_abattement = assiette_csg_abattue,
            base_sans_abattement = assiette_csg_non_abattue,
            law_node = law.csg.activite.deductible,
            plafond_securite_sociale = plafond_securite_sociale,
            )
        return period, montant_csg


class csg_imposable_salaire(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    label = u"CSG imposables sur les salaires"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        assiette_csg_abattue = simulation.calculate('assiette_csg_abattue', period)
        assiette_csg_non_abattue = simulation.calculate('assiette_csg_non_abattue', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        law = simulation.legislation_at(period.start)

        montant_csg = montant_csg_crds(
            base_avec_abattement = assiette_csg_abattue,
            base_sans_abattement = assiette_csg_non_abattue,
            law_node = law.csg.activite.imposable,
            plafond_securite_sociale = plafond_securite_sociale,
            )

        return period, montant_csg


class crds_salaire(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    label = u"CRDS sur les salaires"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        assiette_csg_abattue = simulation.calculate('assiette_csg_abattue', period)
        assiette_csg_non_abattue = simulation.calculate('assiette_csg_non_abattue', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)

        law = simulation.legislation_at(period.start)

        montant_crds = montant_csg_crds(
            law_node = law.crds.activite,
            base_avec_abattement = assiette_csg_abattue,
            base_sans_abattement = assiette_csg_non_abattue,
            plafond_securite_sociale = plafond_securite_sociale,
            )

        return period, montant_crds


class forfait_social(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Forfait social"
    start_date = date(2009, 1, 1)

    # les contributions destinées au financement des prestations de prévoyance complémentaire versées
    # au bénéfice de leurs salariés, anciens salariés et de leurs ayants droit (entreprises à partir de 10 salariés),
    # la réserve spéciale de participation dans les sociétés coopératives ouvrières de production (Scop).

    def function(self, simulation, period):
        prevoyance_obligatoire_cadre = simulation.calculate_add('prevoyance_obligatoire_cadre', period)
        prise_en_charge_employeur_prevoyance_complementaire = simulation.calculate_add(
            'prise_en_charge_employeur_prevoyance_complementaire', period)
        prise_en_charge_employeur_retraite_complementaire = simulation.calculate_add(
            'prise_en_charge_employeur_retraite_complementaire', period)

        taux_plein = simulation.legislation_at(period.start).forfait_social.taux_plein
        taux_reduit = simulation.legislation_at(period.start).forfait_social.taux_reduit

        # TODO: complete this
        assiette_taux_plein = prise_en_charge_employeur_retraite_complementaire  # TODO: compléter l'assiette
        assiette_taux_reduit = - prevoyance_obligatoire_cadre + prise_en_charge_employeur_prevoyance_complementaire
        return period, - (
            assiette_taux_plein * taux_plein + assiette_taux_reduit * taux_reduit
            )


class salaire_imposable(Variable):
    base_function = requested_period_added_value
    column = FloatCol(
        cerfa_field = {
            QUIFOY['vous']: u"1AJ",
            QUIFOY['conj']: u"1BJ",
            QUIFOY['pac1']: u"1CJ",
            QUIFOY['pac2']: u"1DJ",
            QUIFOY['pac3']: u"1EJ",
            },  # (f1aj, f1bj, f1cj, f1dj, f1ej)
        val_type = "monetary",
        )
    entity_class = Individus
    label = u"Salaires imposables"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        primes_salaires = simulation.calculate('primes_salaires', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        csg_deductible_salaire = simulation.calculate('csg_deductible_salaire', period)
        cotisations_salariales = simulation.calculate('cotisations_salariales', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)
        hsup = simulation.calculate('hsup', period)
        rev_microsocial_declarant1 = simulation.calculate_divide('rev_microsocial_declarant1', period)
        indemnite_fin_contrat = simulation.calculate('indemnite_fin_contrat', period)

        return period, (
            salaire_de_base + primes_salaires + remuneration_principale +
            primes_fonction_publique + indemnite_residence + supp_familial_traitement + csg_deductible_salaire +
            cotisations_salariales - hsup + rev_microsocial_declarant1 + indemnite_fin_contrat
            )


class salaire_net(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Salaires nets d'après définition INSEE"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        '''
        Calcul du salaire net d'après définition INSEE
        net = net de csg et crds
        '''
        period = period.start.period(u'month').offset('first-of')

        # salaire_de_base = simulation.get_array('salaire_de_base', period)
        # if salaire_de_base is None:
        #     return period, self.zeros()
        salaire_imposable = simulation.calculate('salaire_imposable', period)
        crds_salaire = simulation.calculate('crds_salaire', period)
        csg_imposable_salaire = simulation.calculate('csg_imposable_salaire', period)

        return period, salaire_imposable + crds_salaire + csg_imposable_salaire


class tehr(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe exceptionnelle de solidarité sur les très hautes rémunérations"
    url = u"http://vosdroits.service-public.fr/professionnels-entreprises/F32096.xhtml"
    calculate_output = calculate_output_divide

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        salaire_de_base = simulation.calculate_add('salaire_de_base', period)  # TODO: check base
        law = simulation.legislation_at(period.start)

        bar = law.cotsoc.tehr
        return period, -bar.calc(salaire_de_base)


############################################################################
# # Non salariés
############################################################################


class rev_microsocial(Variable):
    """Revenu net des cotisations sociales sous régime microsocial (auto-entrepreneur)"""
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu net des cotisations sociales pour le régime microsocial"
    start_date = date(2009, 1, 1)
    url = u"http://www.apce.com/pid6137/regime-micro-social.html"

    def function(self, simulation, period):
        period = period.this_year
        assiette_service = simulation.calculate('assiette_service', period)
        assiette_vente = simulation.calculate('assiette_vente', period)
        assiette_proflib = simulation.calculate('assiette_proflib', period)
        _P = simulation.legislation_at(period.start)

        P = _P.cotsoc.sal.microsocial
        total = assiette_service + assiette_vente + assiette_proflib
        prelsoc_ms = assiette_service * P.servi + assiette_vente * P.vente + assiette_proflib * P.rsi
        return period, total - prelsoc_ms


class rev_microsocial_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Revenu net des cotisations sociales sous régime microsocial (auto-entrepreneur) (pour le premier déclarant du foyer fiscal)"  # noqa
    role = VOUS
    variable = rev_microsocial
