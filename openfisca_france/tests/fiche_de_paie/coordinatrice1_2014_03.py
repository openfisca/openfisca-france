# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:46:55 2015

@author: l.romanello
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
        name = "Madame Martin",
        period = "2014-03",   #
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 1,  # "anticipe_regularisation_fin_de_periode"
            assujettie_taxe_salaires = True,
            avantages_en_nature_valeur_reelle = 0,
            base_remboursement_transport = 0,
            contrat_de_travail = 1,  # temps plein
            contrat_de_travail_arrivee = "2013-07-02",
            contrat_de_travail_depart = "2014-12-31",
            contrat_de_travail_duree = 0,  # CDI
            effectif_entreprise = 3000,  
            heures_non_remunerees_volume = 0,
            # heures_remunerees_volume = 0, 
            # exposition_accident = 3,
            localisation_entreprise = "13299",
            nombre_tickets_restaurant = 0,
            prevoyance_obligatoire_cadre_taux_employeur = .015,  # 1.5% est le minimum
            prise_en_charge_employeur_retraite_complementaire = 82.44,
            prise_en_charge_employeur_prevoyance_complementaire = 0,
            prise_en_charge_employeur_retraite_supplementaire = 0,
            # ratio_alternants = 0, pas l'info
            redevable_taxe_apprentissage = 1,
            salaire_de_base = 1800,
            taux_accident_travail = 0.015,
            taux_versement_transport = 0,
            titre_restaurant_valeur_unitaire = 0,
            titre_restaurant_volume = 0,
            type_sal = 0,  # non cadre
            volume_jours_ijss = 0,
            ),
        output_variables = dict(
            # TODO à inclure dans la décomposition et à finir de coder forfait_social = -3.8, # 47.49 de base
            # TODO à coder taxe_handicapes = 18.40

            # salsuperbrut = 0,
            # cotisations_patronales = 0,

            # cotisations_patronales_contributives = 0,
            ags = -5.4,
            agff_tranche_a_employeur = -21.60,
            apec_employeur = 0,
            arrco_tranche_a_employeur = -82.44,
            assedic_employeur = -72,
            cotisation_exceptionnelle_temporaire_employeur = 0,
            vieillesse_deplafonnee_employeur = -31.5,
            vieillesse_plafonnee_employeur = -152.1,
            fonds_emploi_hospitalier = 0,
            ircantec_employeur = 0,
            pension_civile_employeur = 0,
            rafp_employeur = 0,

            # cotisations_patronales_non_contributives = 0,
            allocations_temporaires_invalidite = 0,
            accident_du_travail = -27,
            famille = -94.5,
            maladie_employeur = -230.4,
            taxe_salaires = -76.5 - 27.07 - 49.02,

            # cotisations_patronales_main_d_oeuvre = 0,
            conge_individuel_formation_cdd = 0,
            contribution_developpement_apprentissage = -3.24, #avec la taxe d'apprentissage 
            contribution_solidarite_autonomie = -5.4,
            # contribution_supplementaire_apprentissage = 0, pas dans la fiche
            fnal_tranche_a = 0,
            # fnal_tranche_a_plus_20 = 0, pas dans la fiche de paie
            formation_professionnelle = -28.8, 
            participation_effort_construction = -8.1,
            prevoyance_obligatoire_cadre = 0,
            taxe_apprentissage = -9,
            versement_transport = 0,

            # allegement_fillon = 222.12, PROBLEME (devrait être 0)
            alleg_cice = 0,
            tehr = 0,
            salbrut = 1800,

            # cotisations_salariales = 0,

            # cotisations_salariales_contributives = 0,
            agff_tranche_a_employe = -14.4,
            agirc_tranche_b_employe = 0,
            apec_employe = 0,
            arrco_tranche_a_employe = -54.9,
            assedic_employe = -43.2,
            cotisation_exceptionnelle_temporaire_employe = 0,
            vieillesse_deplafonnee_employe = -4.5,
            vieillesse_plafonnee_employe = -122.4,
            ircantec_employe = 0,
            pension_civile_employe = 0,
            rafp_employe = 0,

            # cotisations_salariales_non_contributives = 0,
            maladie_employe = -13.5, # regroupée avec vieillesse dans la fiche de paie
            contribution_exceptionnelle_solidarite_employe = 0,
            csgsald = -90.19,
            mhsup = 0,
            salnet = 1405.62,

            # salaire imposable
            csgsali = -42.44,
            crdssal = -8.84, # Avec la CSG dans la fiche de paie
            hsup = 0,
            # sal = 0, pas l'information

            depense_cantine_titre_restaurant_employe = 0,

            salaire_net_a_payer = 1405.62,

            ),
        ),
    ]
