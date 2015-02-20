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


tests = [
    dict(
        name = "ingenieur_ssii1_2013_08",
        period = "2013-08",   #
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 0,  # "anticipe_regularisation_fin_de_periode"
            arrco_tranche_a_taux_employeur = .04539,
            arrco_tranche_a_taux_salarie = .03024,
            assujettie_taxe_salaires = False,
            avantages_en_nature_valeur_reelle = 0,
            contrat_de_travail = 0,  # temps plein
            contrat_de_travail_arrivee = "2013-01-01",
            contrat_de_travail_depart = "2013-12-31",
            contrat_de_travail_duree = 0,  # CDI
            effectif_entreprise = 5000,
            heures_non_remunerees_volume = 21.0,
            # exposition_accident = 3,
            localisation_entreprise = "77023",
            nombre_tickets_restaurant = 0,
            prevoyance_obligatoire_cadre_taux_employeur = .015,  # 1.5% est le minimum
            primes_salaires = 24.88,
            prise_en_charge_employeur_retraite_complementaire = 0,
            prise_en_charge_employeur_prevoyance_complementaire = 0,
            prise_en_charge_employeur_retraite_supplementaire = 0,
            ratio_alternants = 0,
            redevable_taxe_apprentissage = 1,
            remboursement_transport_base = 0,
            salaire_de_base = 2887.79 - 399.79,
            taux_accident_travail = 0.011,
            taux_versement_transport = 0.015,
            titre_restaurant_valeur_unitaire = 0,
            titre_restaurant_volume = 0,
            type_sal = {"2013-08": 1},  # cadre
            volume_jours_ijss = 0,
            ),
        output_variables = dict(
            # TODO à inclure dans la décomposition et à finir de coder forfait_social = -3.8, # 47.49 de base
            # TODO à coder taxe_handicapes = 18.40

            # salsuperbrut = 0,
            # cotisations_patronales = 0,

            # cotisations_patronales_contributives = 0,
            ags = -7.54,
            agff_tranche_a_employeur = -30.15,
            apec_employeur = -0.9,
            arrco_tranche_a_employeur = -114.06,
            agirc_tranche_b_employeur = -41.13,
            assedic_employeur = -100.52,
            cotisation_exceptionnelle_temporaire_employeur = -5.53,
            vieillesse_deplafonnee_employeur = -40.21,
            vieillesse_plafonnee_employeur = -211.08,
            fonds_emploi_hospitalier = 0,
            ircantec_employeur = 0,
            pension_civile_employeur = 0,
            rafp_employeur = 0,

            # cotisations_patronales_non_contributives = 0,
            allocations_temporaires_invalidite = 0,
            accident_du_travail = -27.64,
            famille = -135.70,
            maladie_employeur = -321.65,
            taxe_salaires = 0,

            # cotisations_patronales_main_d_oeuvre = 0,
            conge_individuel_formation_cdd = 0,
            contribution_developpement_apprentissage = -4.52,
            contribution_solidarite_autonomie = -7.54,
            # contribution_supplementaire_apprentissage = 0,
            fnal_tranche_a = 0,
            fnal_tranche_a_plus_20 = -12.56,
            formation_professionnelle = -40.21,
            participation_effort_construction = -11.31,
            # prevoyance_obligatoire_cadre = -192.43, # cette valeur est la part salarié TODO devrait être 37.69
            taxe_apprentissage = -12.56,
            versement_transport = -37.69,

            allegement_fillon = 0,
            credit_impot_competitivite_emploi = 2512.88 * 0.04,  # pas indiqué dans la fiche
            tehr = {'2013': 0},
            salbrut = 2512.88,
            assiette_cotisations_sociales = 2512.88,

            # cotisations_salariales = 0,

            # cotisations_salariales_contributives = 0,
            agff_tranche_a_employe = -20.10,
            agirc_tranche_b_employe = -25.13,
            apec_employe = -0.6,
            arrco_tranche_a_employe = -75.99,
            assedic_employe = -60.31,
            cotisation_exceptionnelle_temporaire_employe = -3.27,
            vieillesse_deplafonnee_employe = -2.51,
            vieillesse_plafonnee_employe = -169.62,
            ircantec_employe = 0,
            pension_civile_employe = 0,
            rafp_employe = 0,

            # cotisations_salariales_non_contributives = 0,
            maladie_employe = -18.85,
            contribution_exceptionnelle_solidarite_employe = 0,
            # csgsald = -127.45,
            mhsup = 0,
            # salnet = 1969.3,

            # salaire imposable
            # csgsali = -59.98,
            # crdssal = -12.5,
            hsup = 0,
            # sal = 1955.78,

            depense_cantine_titre_restaurant_employe = 0,

            # salaire_net_a_payer = 1969.3,

            ),
        ),
    ]
