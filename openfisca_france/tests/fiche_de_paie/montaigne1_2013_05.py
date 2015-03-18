# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 14:55:12 2015

@author: m.monnet
"""

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
        name = "Mme Lucile",
        period = "2014-01",   #
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 1,  # "anticipe_regularisation_fin_de_periode"
            assujettie_taxe_salaires = True,
            avantages_en_nature_valeur_reelle = 0,
            code_postal_entreprise = "75014",
            contrat_de_travail = 0,  # temps plein
            contrat_de_travail_arrivee = "2014-01-01",
            contrat_de_travail_depart = "2014-12-31",
            contrat_de_travail_duree = 0,  # CDI
            effectif_entreprise = 500,
            heures_non_remunerees_volume = 0,
            heures_remunerees_volume = 0,
            # exposition_accident = 3,
            indemnites_forfaitaires = 0,
            indemnites_journalieres_maladie = 0,
            nombre_tickets_restaurant = 0,
            # prevoyance_obligatoire_cadre_taux_employeur = .0,  # 1.5% est le minimum
            prevoyance_obligatoire_cadre = -105.83,
            primes_salaires = 0,
            prise_en_charge_employeur_retraite_complementaire = 156.36,  # "article 83 totalité" dans fiche
            prise_en_charge_employeur_prevoyance_complementaire = 0,
            prise_en_charge_employeur_retraite_supplementaire = 0,
            ratio_alternants = 0,
            redevable_taxe_apprentissage = 0,
            remboursement_transport_base = 67.10,
            salaire_de_base = 3420,
            taux_accident_travail = 0,
            taux_versement_transport = 0.027,
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
            remboursement_transport = 33.55,

            # cotisations_patronales_contributives = 0,
            ags = -11.95,
            agff_tranche_a_employeur = -37.55,
            agirc_gmp_employeur = 0,
            agirc_tranche_b_employeur = -108.26,
            apec_employeur = -0.31,
            arrco_tranche_a_employeur = -143.31,
            assedic_employeur = -(125.16 + 34.15),
            cotisation_exceptionnelle_temporaire_employeur = 0,
            vieillesse_deplafonnee_employeur = -69.70,
            vieillesse_plafonnee_employeur = -264.40,
            fonds_emploi_hospitalier = 0,
            ircantec_employeur = 0,
            pension_civile_employeur = 0,
            rafp_employeur = 0,

            # cotisations_patronales_non_contributives = 0,
            allocations_temporaires_invalidite = 0,
            accident_du_travail = -59.74,
            famille = -209.10,
            maladie_employeur = -509.80,
            taxe_salaires = 504.24,

            # cotisations_patronales_main_d_oeuvre = 0,
            conge_individuel_formation_cdd = 0,
            contribution_developpement_apprentissage = 0,
            contribution_solidarite_autonomie = -11.95,
            contribution_supplementaire_apprentissage = 0,
            fnal_tranche_a = -3.13,
            fnal_tranche_a_plus_20 = 0,
            formation_professionnelle = -21.91,
            participation_effort_construction = 0,
            prevoyance_obligatoire_cadre = -105.83,
            taxe_apprentissage = 0,
            versement_transport = -26.88,

            allegement_fillon = 0,
            credit_impot_competitivite_emploi = 0,
            forfait_social = -(19.71 + 31.27),
            tehr = {'2014': 0},
            # assiette_cotisations_sociales = 0,

            # cotisations_salariales = 0,

            # cotisations_salariales_contributives = 0,
            agff_tranche_a_employe = -25.03,
            agirc_gmp_employe = 0,
            agirc_tranche_b_employe = -66.17,
            apec_employe = -0.20,
            arrco_tranche_a_employe = -95.43,
            assedic_employe = -(20.49 + 75.10),
            cotisation_exceptionnelle_temporaire_employe = 0,
            vieillesse_deplafonnee_employe = -9.96,
            vieillesse_plafonnee_employe = -212.77,
            ircantec_employe = 0,
            pension_civile_employe = 0,
            rafp_employe = 0,

            # cotisations_salariales_non_contributives = 0,
            maladie_employe = -29.87,
            contribution_exceptionnelle_solidarite_employe = 0,
            csgsald = -220.17,
            mhsup = -26,
            salnet = 3048.55,

            # salaire imposable
            csgsali = -103.61,
            crdssal = -21.59,
            hsup = 17,
            sal = 3354.54,  # salaire imposable
            depense_cantine_titre_restaurant_employe = 0,

            salaire_net_a_payer = 3048.55,

            ),
        ),
    ]
