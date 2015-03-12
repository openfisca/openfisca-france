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
        name = "non_cadre",  # Tiré du calculateur IPP
        period = "2012-01",
        input_variables = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            depcom_entreprise = "69381",
            ratio_alternants = .025,
            salaire_de_base = 3000,
            taille_entreprise = 3,
            type_sal = 0,
            ),
        output_variables = dict(
            # patronales main d'oeuvre
            contribution_developpement_apprentissage = -5.4,
            contribution_supplementaire_apprentissage = -3,
            taxe_apprentissage = -15,
            contribution_solidarite_autonomie = -9,
            participation_effort_construction = -13.5,
            fnal_tranche_a_plus_20 = -15,
            formation_professionnelle = -48,
            versement_transport = -52.5,
            cotisations_patronales_main_d_oeuvre = -158.4 - 3,
            # -(206.4 -48) formation professionnelle conmptée deux fois
            # - 3 contribution_supplementaire_apprentissage
            # patronales non contributives
            accident_du_travail = -300,
            famille = -162,
            maladie_employeur = -384,
            cotisations_patronales_non_contributives = -846,

            # patronales contributives
            agff_tranche_a_employeur = -36,
            ags = -9,
            arrco_tranche_a_employeur = -135,
            assedic_employeur = -120,
            vieillesse_deplafonnee_employeur = -48,
            vieillesse_plafonnee_employeur = -249,
            cotisations_patronales_contributives = -597,
            cotisations_patronales = - 158.4 - 3 - 597 - 846,

            agff_tranche_a_employe = -24,
            arrco_tranche_a_employe = -90,
            assedic_employe = -72,
            maladie_employe = -22.5,
            vieillesse_deplafonnee_employe = -3,
            vieillesse_plafonnee_employe = -199.5,
            cotisations_salariales_contributives = -388.5,
            cotisations_salariales_non_contributives = -22.5,
            cotisations_salariales = -388.5 - 22.5,
            csgsald = -150.32,
            csgsali = -70.74,
            crdssal = -14.74,
            ),
        ),
    dict(
        name = "cadre",  # Tiré du calculateur IPP
        period = "2012-01",
        input_variables = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            depcom_entreprise = "69381",
            prevoyance_obligatoire_cadre_taux_employeur = 0,
            ratio_alternants = .025,
            salaire_de_base = 6000,
            taille_entreprise = 3,
            type_sal = 1,
            ),
        output_variables = dict(
            contribution_developpement_apprentissage = -10.80,
            taxe_apprentissage = -30,
            contribution_solidarite_autonomie = -18,
            contribution_supplementaire_apprentissage = -6,
            participation_effort_construction = -27,
            fnal_tranche_a_plus_20 = -30,
            # fnal_tranche_b_plus_20 = -14.85, # Inclus dans fnal_tranche_a_plus_20
            formation_professionnelle = -96,
            versement_transport = -105,
            cotisations_patronales_main_d_oeuvre = - (412.8 - 96) - 6,
            # -(421.8 - 96) formation professionnelle conmptée deux fois
            # - 6 contribution_supplementaire_apprentissage

            # agff_tranche_a_employe = -24.25,   # TODO: pas de tranche B dans le simulateur IPP
            agff_tranche_a_employeur = -74.97,
            ags = -18,
            apec_employeur = - 2.16,
            cotisation_exceptionnelle_temporaire_employeur = -13.20,
            arrco_tranche_a_employeur = -136.39 - 374.09,
            # agirc_tranche_b_employeur = -374.09,  # Inclus dans arcco
            assedic_employeur = - 121.24 - 118.76,
            # assedic_tranche_a_employeur = -11.24  # Inclus dans assedic
            # assedic_tranche_b_employeur = -118,76  # Inclus dans assedic
            vieillesse_deplafonnee_employeur = -96,
            vieillesse_plafonnee_employeur = -251.57,

            cotisations_patronales_contributives = -1206.38,

            accident_du_travail = -600,
            famille = -324,
            maladie_employeur = -768,
            cotisations_patronales_non_contributives = - 1692,
            cotisations_patronales = - 1692 - 1206.38 - (412.8 - 96) - 6,
            maladie_employe = - 45,
            cotisations_salariales_non_contributives = -45,

            apec_employe = -1.44,
            arrco_tranche_a_employe = -90.93,
            agirc_tranche_b_employe = -228.61,
            # assedic_tranche_a_employe = -72.74  # Inclus dans assedic
            # assedic_tranche_b_employe = -71,26,  # Inclus dans assedic
            assedic_employe = -72.74 - 71.26,
            vieillesse_deplafonnee_employe = -6,
            vieillesse_plafonnee_employe = -201.56,
            cotisations_salariales_contributives = -731.31,

            cotisations_salariales = -731.31 - 45,
            csgsald = -300.65,
            csgsali = -141.48,
            crdssal = -29.48,
            ),
        ),
    dict(
        name = "smicard_deloitte",  # http://www.challenges.fr/emploi/20140213.CHA0474/les-tresors-de-la-fiche-de-paie-d-un-smicard.html
        period = "2014-01",
        input_variables = dict(
            effectif_entreprise = 3000,
            depcom_entreprise = "69381",
            prevoyance_obligatoire_cadre_taux_employeur = 0,
            ratio_alternants = .025,
            salaire_de_base = 1445.42,
            taux_versement_transport = .026,
            type_sal = 0,
            allegement_fillon_mode_recouvrement = 1,
            ),
        output_variables = dict(
            contribution_developpement_apprentissage = -2.6,
            taxe_apprentissage = - (9.83 - 2.6),
            contribution_solidarite_autonomie = -4.34,
            # contribution_supplementaire_apprentissage = 0, # Manque chez Deloiite
            participation_effort_construction = -6.5,
            fnal_tranche_a_plus_20 = -1.45 - 5.78,
            # fnal_tranche_b_plus_20 = -14.85, # Inclus dans fnal_tranche_a_plus_20
            formation_professionnelle = -23.13,
            versement_transport = -37.58,
            # cotisations_patronales_main_d_oeuvre = - (412.8 - 96) - 6,
            # -(421.8 - 96) formation professionnelle conmptée deux fois
            # - 6 contribution_supplementaire_apprentissage

            # agff_tranche_a_employe = -24.25,   # TODO: pas de tranche B dans le simulateur IPP
            agff_tranche_a_employeur = -17.35,
            ags = - 4.34,
            apec_employeur = 0,
            cotisation_exceptionnelle_temporaire_employeur = 0,
            arrco_tranche_a_employeur = -66.2,
            # agirc_tranche_b_employeur = -374.09,  # Inclus dans arcco
            assedic_employeur = - 57.82,
            # assedic_tranche_a_employeur = -11.24  # Inclus dans assedic
            # assedic_tranche_b_employeur = -118,76  # Inclus dans assedic
            vieillesse_deplafonnee_employeur = -25.29,
            vieillesse_plafonnee_employeur = -122.14,

#            cotisations_patronales_contributives = -1206.38,

            accident_du_travail = -15.9,
            famille = -75.88,
            maladie_employeur = -185.01,
            # cotisations_patronales_non_contributives = - 1692,
            # cotisations_patronales = - 1692 - 1206.38 - (412.8 - 96) - 6,
            maladie_employe = - 10.84,
#            cotisations_salariales_non_contributives = -45,

            agff_tranche_a_employe = -11.56,
            apec_employe = 0,
            arrco_tranche_a_employe = -44.09,
            agirc_tranche_b_employe = 0,
            # assedic_tranche_a_employe = -72.74  # Inclus dans assedic
            # assedic_tranche_b_employe = -71,26,  # Inclus dans assedic
            assedic_employe = -34.69,
            vieillesse_deplafonnee_employe = -3.61,
            vieillesse_plafonnee_employe = -98.29,
#            cotisations_salariales_contributives = -731.31,

#            cotisations_salariales = -731.31 - 45,
            csgsald = -72.43,
            csgsali = -34.08,
            crdssal = -7.1,
            allegement_fillon = 375.81
            ),
        )
    ]
