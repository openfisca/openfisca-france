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
        name = "Salarié IPP",
        period = "2014-11",
        input_variables = dict(
            assujettie_taxe_salaires = True,
            contrat_de_travail_duree = 1,  # CDD
            contrat_de_travail_arrivee = "2014-11-02",
            effectif_entreprise = 3000,
            # exposition_accident = 3,
            code_postal_entreprise = "75014",
            prevoyance_obligatoire_cadre_taux_employeur = .0157,
            ratio_alternants = 0,
            redevable_taxe_apprentissage = 0,
            salaire_de_base = 4600,
            taux_accident_travail = .015,
            taux_versement_transport = .027,
            titre_restaurant_valeur_unitaire = 9,
            titre_restaurant_volume = 19,
            type_sal = 1,
            ),
        output_variables = dict(
            conge_individuel_formation_cdd = -46,
            contribution_solidarite_autonomie = -13.8,
            participation_effort_construction = -20.70,
            fnal = -23,
            formation_professionnelle = -73.6,
            versement_transport = -124.20,
            # cotisations_patronales_main_d_oeuvre = ,
            agff_tranche_a_employe = -24.20 - 14.18,
            agff_tranche_a_employeur = - 36.30 - 20.48,
            ags = -13.80,
            apec_employeur = - 1.09 - .57,
            cotisation_exceptionnelle_temporaire_employeur = -10.12,
            arrco_tranche_a_employeur = -138.53 - 199.75,
            # agirc_tranche_b_employeur = -199.75,  # Inclus dans arcco
            assedic_employeur = - 120.99 - 63.01,
            # assedic_tranche_a_employeur = -120.99  # Inclus dans assedic
            # assedic_tranche_b_employeur = -63.01  # Inclus dans assedic
            vieillesse_deplafonnee_employeur = -80.5,
            vieillesse_plafonnee_employeur = -255.59,

            # cotisations_patronales_contributives = ,

            accident_du_travail = -69,
            famille = -241.5,
            maladie_employeur = - 588.80,
            # cotisations_patronales = - 2836.38 + 19 * 4.5,  # montant juste TODO: A compléter avec presta manquantes
            taxe_salaires = - 197.52 - 27.07 - 315.27,
            prevoyance_obligatoire_cadre = -47.49,

            forfait_social = -3.8, # 47.49 de base
            cotisation_exceptionnelle_temporaire_employe = -5.98,
            maladie_employe = - 34.5,
            # cotisations_salariales_non_contributives = ,

            apec_employe = -.73 - .38,
            arrco_tranche_a_employe = -92.25,
            agirc_tranche_b_employe = - 122.09,
            # assedic_tranche_a_employe = -72.59  # Inclus dans assedic
            # assedic_tranche_b_employe = 37.81,  # Inclus dans assedic
            assedic_employe = -72.59 - 37.81,

            vieillesse_deplafonnee_employe = -11.5,
            vieillesse_plafonnee_employe = -205.68,
            # cotisations_salariales_contributives = ,

            # cotisations_salariales = ,
            csgsald = -232.92,
            csgsali = -109.61,
            crdssal = -22.83,
            reintegration_titre_restaurant_employeur = 0,
            depense_cantine_titre_restaurant_employeur = 19 * 4.5,

            sal = 3745.19,  # salaire imposable
            depense_cantine_titre_restaurant_employe = -19 * 4.5,

            salaire_net_a_payer = 3527.25,


            # TODO taxe_handicapes = 18.40
            ),
        ),
    ]
