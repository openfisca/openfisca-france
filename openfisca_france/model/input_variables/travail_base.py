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


import datetime


from ..base import *  # noqa analysis:ignore


# Socio-economic data
# Données d'entrée de la simulation à fournir à partir d'une enquête ou générées par le générateur de cas type

reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"fin_d_annee",
                u"anticipe_regularisation_fin_de_periode",
                u"progressif",
                ],
            ),
        ),
    entity_class = Individus,
    label = u"Mode de recouvrement des allègements Fillon",
    name = 'allegement_fillon_mode_recouvrement',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Taux ARRCO tranche A employeur) propre à l'entreprise",
    name = 'arrco_tranche_a_taux_employeur',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Taux ARRCO tranche A salarié) propre à l'entreprise",
    name = 'arrco_tranche_a_taux_salarie',
    )
reference_input_variable(
    column = BoolCol(),
    entity_class = Individus,
    label = u"Entreprise assujettie à la taxe sur les salaires",
    name = 'assujettie_taxe_salaires',
    )
reference_input_variable(
    column = BoolCol(),
    entity_class = Individus,
    label = u"Avantages en nature (Valeur réelle)",
    name = 'avantages_en_nature_valeur_reelle',
    )
reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"temps_plein",
                u"temps_partiel",
                u"forfait_heures_semaines",
                u"forfait_heures_mois",
                u"forfait_heures_annee",
                u"forfait_jours_annee",
                ],
            ),
        ),
    entity_class = Individus,
    label = u"Type contrat de travail",
    name = 'contrat_de_travail',
    )
reference_input_variable(
    column = DateCol(default = datetime.date(1870, 1, 1)),
    entity_class = Individus,
    label = u"Date d'arrivée dans l'entreprise",
    name = 'contrat_de_travail_arrivee',  # debut
    )
reference_input_variable(
    column = DateCol(default = datetime.date(2099, 12, 31)),
    entity_class = Individus,
    label = u"Date de départ de l'entreprise",
    name = 'contrat_de_travail_depart',   # fin
    )
reference_input_variable(
    column = EnumCol(
        enum = Enum([
            u"cdi",
            u"cdd",
            ]),
        ),
    entity_class = Individus,
    label = u"Type (durée determinée ou indéterminée) du contrat de travail",
    name = 'contrat_de_travail_duree',
    )
reference_input_variable(
    column = EnumCol(
        enum = Enum([
            u"Mensuel avec régularisation en fin d'année",
            u"Annuel",
            ]),
        ),
    entity_class = Individus,
    label = u"Mode de recouvrement des cotisations sociales",
    name = 'cotisation_sociale_mode_recouvrement',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Effectif de l'entreprise",
    name = 'effectif_entreprise',
    )
reference_input_variable(
    column = FixedStrCol(max_length = 5),
    entity_class = Individus,
    label = u"Localisation entreprise",
    name = 'localisation_entreprise',  # TODO; à adpater sur le format depcom ?
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Nombre de tickets restaurant",
    name = 'nombre_tickets_restaurant',
    )
reference_input_variable(
    column = FloatCol(default = .015),  # 1.5% est le minimum en 2014
    entity_class = Individus,
    label = u"Taux de cotisation employeur pour la prévoyance obligatoire des cadres",
    name = 'prevoyance_obligatoire_cadre_taux_employe',
    )
reference_input_variable(
    column = FloatCol(default = .015),  # 1.5% est le minimum en 2014
    entity_class = Individus,
    label = u"Taux de cotisation employeur pour la prévoyance obligatoire des cadres",
    name = 'prevoyance_obligatoire_cadre_taux_employeur',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Indemnités, primes et avantages en argent",
    name = 'primes_salaires',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Part salariale des cotisations de prévoyance complémentaire prise en charge par l'employeur",
    name = 'prise_en_charge_employeur_prevoyance_complementaire',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Part salariale des cotisations de retraite complémentaire prise en charge par l'employeur",
    name = 'prise_en_charge_employeur_retraite_complementaire',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Part salariale des cotisations de retraite supplémentaire prise en charge par l'employeur",
    name = 'prise_en_charge_employeur_retraite_supplementaire',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Ratio d'alternants dans l'effectif moyen",
    name = 'ratio_alternants',
    )
reference_input_variable(
    column = BoolCol(default = True),
    entity_class = Individus,
    label = u"Entreprise redevable de la taxe d'apprentissage",
    name = 'redevable_taxe_apprentissage',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Base pour le calcul du remboursement des frais de transport",
    name = 'remboursement_transport_base',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Salaire de base",
    name = 'salaire_de_base',
    )
reference_input_variable(
    column = FloatCol(default = .5),
    entity_class = Individus,
    label = u"Taux de participation de l'employeur au titre restaurant",
    name = 'titre_restaurant_taux_employeur',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Valeur faciale unitaire du titre restaurant",
    name = 'titre_restaurant_valeur_unitaire',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Volume des titres restaurant",
    name = 'titre_restaurant_volume',
    )
reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"prive_non_cadre",
                u"prive_cadre",
                u"public_titulaire_etat",
                u"public_titulaire_militaire",
                u"public_titulaire_territoriale",
                u"public_titulaire_hospitaliere",
                u"public_non_titulaire",
                ],
            ),
        ),
    entity_class = Individus,
    label = u"Catégorie de salarié",
    name = 'type_sal',
    )
reference_input_variable(
    column = IntCol(),  # TODO default la valeur de la durée légale ?
    entity_class = Individus,
    label = u"Durée mensuelle collective dans l'entreprise (heures, temps plein)",
    name = 'heures_duree_collective_entreprise',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)",
    name = 'heures_non_remunerees_volume',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Volume des heures rémunérées contractuellement (heures/mois, temps partiel)",
    name = 'heures_remunerees_volume',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Volume des heures rémunérées à un forfait heures",
    name = 'forfait_heures_remunerees_volume',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Volume des heures rémunérées à forfait jours",
    name = 'forfait_jours_remuneres_volume',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Volume des jours pour lesquels sont versés une idemnité journalière par la sécurité sociale",
    name = 'volume_jours_ijss',
    )
