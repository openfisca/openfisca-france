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
        name = "ingenieur_etude5_2014_07",
        period = "2014-07",   #
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 1,  # "anticipe_regularisation_fin_de_periode"
            assujettie_taxe_salaires = False,
            avantages_en_nature_valeur_reelle = 0,
            contrat_de_travail = 0,  # temps plein
            contrat_de_travail_arrivee = "2014-01-01",
            contrat_de_travail_depart = "2014-12-31",
            contrat_de_travail_duree = 0,  # CDI
            effectif_entreprise = 3000,
            heures_non_remunerees_volume = 0,
            heures_remunerees_volume = 0,
            # exposition_accident = 3,
            indemnites_forfaitaires = 160 + 40.95,  # indemnités transports et repas
            indemnites_journalieres_maladie = 0,
            code_postal_entreprise = "75014",
            prevoyance_obligatoire_cadre_taux_employeur = 0.0074,  # 1.5% est le minimum
            primes_salaires = 0,
            prise_en_charge_employeur_retraite_complementaire = 0,
            prise_en_charge_employeur_prevoyance_complementaire = 30.82,
            prise_en_charge_employeur_retraite_supplementaire = 0,
            ratio_alternants = 0,
            redevable_taxe_apprentissage = 1,
            remboursement_transport_base = 0,  # Le double d'indmnités de transport indiqué sur la fiche de paie
            salaire_de_base = 3000,
            taux_accident_travail = 0.011,
            taux_versement_transport = 0,
            titre_restaurant_valeur_unitaire = 0,
            titre_restaurant_volume = 0,
            type_sal = 1,  # non cadre
            volume_jours_ijss = 0,
            ),
        output_variables = dict(
            # TODO à inclure dans la décomposition et à finir de coder forfait_social = -3.8, # 47.49 de base
            # TODO à coder taxe_handicapes = 18.40

            # salsuperbrut = 0,
            # cotisations_patronales = 0,
            remboursement_transport = 0,
            ircantec_employeur = 0,
            pension_civile_employeur = 0,
            rafp_employeur = 0,

            # cotisations_patronales_non_contributives = 0,
            allocations_temporaires_invalidite = 0,
            accident_du_travail = -33,
            famille = -157.5,
            maladie_employeur = -3000 * .128,  # est aggrégé avec vieillesse
            taxe_salaires = 0,

            # cotisations_patronales_main_d_oeuvre = 0,
            conge_individuel_formation_cdd = 0,
            contribution_developpement_apprentissage = -3000 * 0.0018,  # aggrégé avec taxe apprentissage
            contribution_solidarite_autonomie = 0,
            contribution_supplementaire_apprentissage = 0,
            fnal = -15,

            # cotisations_patronales_contributives = 0,
            ags = -9,
            agff_tranche_a_employeur = -36.00,
            agirc_gmp_employeur = -41.17,
            agirc_tranche_b_employeur = -41.17,
            apec_employeur = -1.08,
            arrco_tranche_a_employeur = -137.4,
            assedic_employeur = -120,
            cotisation_exceptionnelle_temporaire_employeur = -6.60,
            vieillesse_deplafonnee_employeur = -3000 * 0.0175,  # est aggrégé avec maladie
            vieillesse_plafonnee_employeur = -253.5,
            fonds_emploi_hospitalier = 0,
            formation_professionnelle = -48,
            participation_effort_construction = -13.5,
            prevoyance_obligatoire_cadre = -22.2,
            taxe_apprentissage = -3000 * 0.005,  # aggrégé avec contribution supplémentaire apprentissage
            versement_transport = 0,

            allegement_fillon = 0,
            credit_impot_competitivite_emploi = 120,
            forfait_social = -4.72,
            tehr = {'2014': 0},
            salaire_de_base = 3000,

            # cotisations_salariales = 0,

            # cotisations_salariales_contributives = 0,
            agff_tranche_a_employe = -24,
            agirc_gmp_employe = -25,
            agirc_tranche_b_employe = -25.00,  # agirc_gmp_employe,
            apec_employe = -0.72,
            arrco_tranche_a_employe = -91.5,
            assedic_employe = -72,
            cotisation_exceptionnelle_temporaire_employe = -3.9,
            vieillesse_deplafonnee_employe = -3000 * .0025,  # est agrégée avec maladie sur la fiche de paie
            vieillesse_plafonnee_employe = -204,
            ircantec_employe = 0,
            pension_civile_employe = 0,
            rafp_employe = 0,

            # cotisations_salariales_non_contributives = 0,
            maladie_employe = -3000 * .0075,  # est agrégée avec vieillesse déplaf. sur la fiche de paie
            contribution_exceptionnelle_solidarite_employe = 0,
            csgsald = -150.32,
            mhsup = 0,
            salnet = 2395.55,

            # salaire imposable
            csgsali = -70.74,
            crdssal = -14.74,  # 0.5*2947.50 (attention dans fiche, taux csg/crds aggrégé)
            hsup = 0,
            # sal = 2395.55,  # salaire imposable
            depense_cantine_titre_restaurant_employe = 0,

            #salaire_net_a_payer = 2478.49,

            ),
        ),
    ]
