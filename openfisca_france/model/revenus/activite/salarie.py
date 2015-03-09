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


from ...base import *  # noqa analysis:ignore


build_column('indemnites_stage', FloatCol(entity = 'ind', label = u"Indemnités de stage"))
build_column('revenus_stage_formation_pro', FloatCol(entity = 'ind', label = u"Revenus de stage de formation professionnelle"))
build_column('bourse_recherche', FloatCol(entity = 'ind', label = u"Bourse de recherche"))



build_column('sali', IntCol(label = u"Revenus d'activité imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AJ",
                               QUIFOY['conj']: u"1BJ",
                               QUIFOY['pac1']: u"1CJ",
                               QUIFOY['pac2']: u"1DJ",
                               QUIFOY['pac3']: u"1EJ",
                               }))  # (f1aj, f1bj, f1cj, f1dj, f1ej)


build_column('sal_pen_exo_etr', IntCol(entity = 'ind',
                     label = u"Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"1AC",
                                    QUIFOY['conj']: u"1BC",
                                    QUIFOY['pac1']: u"1CC",
                                    QUIFOY['pac2']: u"1DC", },
                     start = date(2013, 1, 1),))


build_column('fra', IntCol(label = u"Frais réels",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AK",
                              QUIFOY['conj']: u"1BK",
                              QUIFOY['pac1']: u"1CK",
                              QUIFOY['pac2']: u"1DK",
                              QUIFOY['pac3']: u"1EK",
                              }))  # (f1ak, f1bk, f1ck, f1dk, f1ek)


build_column('hsup', IntCol(label = u"Heures supplémentaires : revenus exonérés connus",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = {QUIFOY['vous']: u"1AU",
                               QUIFOY['conj']: u"1BU",
                               QUIFOY['pac1']: u"1CU",
                               QUIFOY['pac2']: u"1DU",
                               }))  # (f1au, f1bu, f1cu, f1du, f1eu)

build_column('ppe_du_sa', IntCol(label = u"Prime pour l'emploi des salariés: nombre d'heures payées dans l'année",
                     cerfa_field = {QUIFOY['vous']: u"1AV",
                                    QUIFOY['conj']: u"1BV",
                                    QUIFOY['pac1']: u"1CV",
                                    QUIFOY['pac2']: u"1DV",
                                    QUIFOY['pac3']: u"1QV",
                                    }))  # (f1av, f1bv, f1cv, f1dv, f1qv)

build_column(
    'ppe_tp_sa',
    BoolCol(
        label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière",
        cerfa_field = {
            QUIFOY['vous']: u"1AX",
            QUIFOY['conj']: u"1BX",
            QUIFOY['pac1']: u"1CX",
            QUIFOY['pac2']: u"1DX",
            QUIFOY['pac3']: u"1QX",
            }
        )
    )  # (f1ax, f1bx, f1cx, f1dx, f1qx)

build_column(
    'nbsala',
    EnumCol(
        label = u"Nombre de salariés dans l'établissement de l'emploi actuel",
        enum = Enum([
            u"Sans objet",
            u"Aucun salarié",
            u"1 à 4 salariés",
            u"5 à 9 salariés",
            u"10 à 19 salariés",
            u"20 à 49 salariés",
            u"50 à 199 salariés",
            u"200 à 499 salariés",
            u"500 à 999 salariés",
            u"1000 salariés ou plus",
            u"Ne sait pas",
            ])
        )
    )

build_column('tva_ent', BoolCol(label = u"L'entreprise employant le salarié paye de la TVA",
                    default = True))

#    build_column('code_risque', EnumCol(label = u"Code risque pour les accidents du travail"))  # TODO: Complete label, add enum and relevant default.

build_column(
    'exposition_accident',
    EnumCol(
        label = u"Exposition au risque pour les accidents du travail",
        enum = Enum([
            u"Faible",
            u"Moyen",
            u"Élevé",
            u"Très élevé",
            ])
        )
    )

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
    column = FloatCol(),
    entity_class = Individus,
    label = u"Avantages en nature (Valeur réelle)",
    name = 'avantages_en_nature_valeur_reelle',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"indemnites_compensatrices_conges_payes",
    name = 'indemnites_compensatrices_conges_payes',
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
    column = DateCol(default = date(1870, 1, 1)),
    entity_class = Individus,
    label = u"Date d'arrivée dans l'entreprise",
    name = 'contrat_de_travail_arrivee',  # debut
    )
reference_input_variable(
    column = DateCol(default = date(2099, 12, 31)),
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
    is_permanent = True,
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
    column = FloatCol(),
    entity_class = Individus,
    label = u"Nouvelle bonification indicaire",
    name = 'nouvelle_bonification_indiciaire',
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
    column = FloatCol(),
    entity_class = Individus,
    label = u"Base pour le calcul du remboursement des frais de transport",
    name = 'remboursement_transport_base',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Indemnités forfaitaires (transport, nourriture)",
    name = 'indemnites_forfaitaires',
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
    column = FloatCol(),
    entity_class = Individus,
    label = u"Traitement indiciaire brut (TIB)",
    name = 'traitement_indiciaire_brut',
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
    column = FloatCol(),
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
