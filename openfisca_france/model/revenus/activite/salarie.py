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


from functools import partial
from numpy import (
    busday_count as original_busday_count, datetime64, maximum as max_, minimum as min_, timedelta64, zeros,
    )


from ...base import *  # noqa analysis:ignore
from ...prestations.prestations_familiales.base_ressource import nb_enf

build_column('indemnites_stage', FloatCol(entity = 'ind', label = u"Indemnités de stage"))
build_column('revenus_stage_formation_pro', FloatCol(entity = 'ind', label = u"Revenus de stage de formation professionnelle"))
build_column('bourse_recherche', FloatCol(entity = 'ind', label = u"Bourse de recherche"))


build_column('sal_pen_exo_etr', IntCol(
    entity = 'ind',
    label = u"Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif",
    val_type = "monetary",
    cerfa_field = {
        QUIFOY['vous']: u"1AC",
        QUIFOY['conj']: u"1BC",
        QUIFOY['pac1']: u"1CC",
        QUIFOY['pac2']: u"1DC",
        },
    start = date(2013, 1, 1),
    ))


build_column('frais_reels', IntCol(label = u"Frais réels",
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
    column = DateCol(),
    entity_class = Individus,
    label = u"Date de début du contrat d'apprentissage",
    name = 'apprentissage_contrat_debut',
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
    name = 'avantage_en_nature_valeur_reelle',
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
    name = 'contrat_de_travail_debut',  # debut
    )
reference_input_variable(
    column = DateCol(default = date(2099, 12, 31)),
    entity_class = Individus,
    label = u"Date de départ de l'entreprise",
    name = 'contrat_de_travail_fin',   # fin
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
    column = FixedStrCol(max_length = 5),
    entity_class = Individus,
    label = u"Localisation entreprise (depcom)",
    name = 'depcom_entreprise',
    )
reference_input_variable(
    column = FixedStrCol(max_length = 5),
    entity_class = Individus,
    label = u"Localisation entreprise (Code postal)",
    name = 'code_postal_entreprise',
    )
reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    base_function = requested_period_last_value,
    label = u"Effectif de l'entreprise",
    name = 'effectif_entreprise',
    set_input = set_input_dispatch_by_period,
    )
reference_input_variable(
    column = BoolCol(),
    entity_class = Individus,
    label = u"Entreprise assujettie à la contribution économique territoriale",
    name = 'entreprise_assujettie_cet',
    )
reference_input_variable(
    column = BoolCol(),
    entity_class = Individus,
    label = u"Entreprise assujettie à l'impôt sur les sociétés (IS)",
    name = 'entreprise_assujettie_is',
    )
reference_input_variable(
    column = BoolCol(),
    entity_class = Individus,
    label = u"Entreprise assujettie à la TVA",
    name = 'entreprise_assujettie_tva',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Bénéfice de l'entreprise",
    name = 'entreprise_benefice',
    set_input = set_input_divide_by_period,
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Bilan de l'entreprise",
    name = 'entreprise_bilan',
    )
reference_input_variable(
    column = FloatCol(),
    entity_class = Individus,
    label = u"Chiffre d'affaire de l'entreprise",
    name = 'entreprise_chiffre_affaire',
    )
reference_input_variable(
    column = DateCol(),
    entity_class = Individus,
    label = u"Date de création de l'entreprise",
    name = 'entreprise_creation',
    )
reference_input_variable(
    base_function = requested_period_last_value,
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
    base_function = requested_period_last_value,
    column = FloatCol(default = 0.015),  # 1.5% est le minimum en 2014
    entity_class = Individus,
    label = u"Taux de cotisation employeur pour la prévoyance obligatoire des cadres",
    name = 'prevoyance_obligatoire_cadre_taux_employe',
    )
reference_input_variable(
    base_function = requested_period_last_value,
    column = FloatCol(default = 0.015),  # 1.5% est le minimum en 2014
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
    label = u"Salaire de base, en général appelé salaire brut, la 1ère ligne sur la fiche de paie",
    name = 'salaire_de_base',
    set_input = set_input_divide_by_period,
    url = u'http://www.insee.fr/fr/methodes/default.asp?page=definitions/salaire-mensuel-base-smb.htm',
    )
reference_input_variable(
    column = FloatCol(default = 0.5),
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


@reference_formula
class avantage_en_nature(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Avantages en nature"

    def function(self, simulation, period):
        period = period
        avantage_en_nature_valeur_reelle = simulation.calculate('avantage_en_nature_valeur_reelle', period)
        avantage_en_nature_valeur_forfaitaire = simulation.calculate('avantage_en_nature_valeur_forfaitaire', period)

        return period, avantage_en_nature_valeur_reelle + avantage_en_nature_valeur_forfaitaire


@reference_formula
class avantage_en_nature_valeur_forfaitaire(SimpleFormulaColumn):
    # base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Evaluation fofaitaire des avantages en nature "

    # TODO: coplete this function
    def function(self, simulation, period):
        period = period
        avantage_en_nature_valeur_reelle = simulation.calculate('avantage_en_nature_valeur_reelle', period)

        return period, avantage_en_nature_valeur_reelle * 0


@reference_formula
class depense_cantine_titre_restaurant_employe(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Dépense de cantine et de titre restaurant à charge de l'employe"

    def function(self, simulation, period):
        period = period

        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)

        return period, - valeur_unitaire * volume * (1 - taux_employeur)


@reference_formula
class depense_cantine_titre_restaurant_employeur(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Dépense de cantine et de titre restaurant à charge de l'employeur"

    def function(self, simulation, period):
        period = period
        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)  # Compute with jours ouvrables ?
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)

        return period, valeur_unitaire * volume * taux_employeur


@reference_formula
class nombre_jours_calendaires(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Nombre de jours calendaires travaillés"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)

        busday_count = partial(original_busday_count, weekmask = "1" * 7)
        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month'))
        jours_travailles = max_(
            busday_count(
                max_(contrat_de_travail_debut, debut_mois),
                min_(contrat_de_travail_fin, fin_mois) + timedelta64(1, 'D')
                ),
            0,
            )

        return period, jours_travailles


@reference_formula
class remboursement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Remboursement partiel des frais de transport par l'employeur"

    def function(self, simulation, period):

        remboursement_transport_base = simulation.calculate('remboursement_transport_base', period)
        # TODO: paramètres en dur dans le code
        return period, - .5 * remboursement_transport_base


# Fonction publique

@reference_formula
class gipa(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de garantie individuelle du pouvoir d'achat"
    # TODO: à coder

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)

        return period, zeros(len(type_sal))


@reference_formula
class indemnite_residence(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de résidence des fonctionnaires"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        type_sal = simulation.calculate('type_sal', period)
        zone_apl_individu = simulation.calculate('zone_apl_individu', period)
        _P = simulation.legislation_at(period.start)

        zone_apl = zone_apl_individu  # TODO: ces zones ne correpondent pas aux zones APL
        P = _P.fonc.indem_resid
        min_zone_1, min_zone_2, min_zone_3 = P.min * P.taux.zone1, P.min * P.taux.zone2, P.min * P.taux.zone3
        taux = P.taux.zone1 * (zone_apl == 1) + P.taux.zone2 * (zone_apl == 2) + P.taux.zone3 * (zone_apl == 3)
        plancher = min_zone_1 * (zone_apl == 1) + min_zone_2 * (zone_apl == 2) + min_zone_3 * (zone_apl == 3)

        return period, max_(
            plancher,
            taux * (traitement_indiciaire_brut + salaire_de_base)
            ) * (type_sal >= 2)


@reference_formula
class indice_majore(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indice majoré"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        _P = simulation.legislation_at(period.start)

        traitement_annuel_brut = _P.fonc.IM_100
        return period, (traitement_indiciaire_brut * 100 * 12 / traitement_annuel_brut) * (type_sal >= 2)


@reference_formula
class primes_fonction_publique(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul des primes pour les fonctionnaries"
    url = u"http://vosdroits.service-public.fr/particuliers/F465.xhtml"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)

        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        public = (
            (type_sal == CAT['public_titulaire_etat'])
            + (type_sal == CAT['public_titulaire_territoriale'])
            + (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        return period, TAUX_DE_PRIME * traitement_indiciaire_brut * public


@reference_formula
class af_nbenf_fonc(SimpleFormulaColumn):
    column = IntCol
    entity_class = Familles
    label = u"Nombre d'enfants dans la famille au sens des allocations familiales pour le fonctionnaires"
    # Hack pour éviter une boucle infinie

    def function(self, simulation, period):
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        age_holder = simulation.compute('age', period)
        salaire_de_base = simulation.calculate_add('salaire_de_base', period.start.period('month', 6).offset(-6))
        law = simulation.legislation_at(period.start)
        nbh_travaillees = 169
        smic_mensuel_brut = law.cotsoc.gen.smic_h_b * nbh_travaillees
        smic55_holder = (salaire_de_base / 6) >= (law.fam.af.seuil_rev_taux * smic_mensuel_brut)
        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        af_nbenf = nb_enf(age, smic55, law.fam.af.age1, law.fam.af.age2)

        return period, af_nbenf


@reference_formula
class supp_familial_traitement(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Supplément familial de traitement"
    # Attention : par hypothèse ne peut êre attribué qu'à la tête du ménage
    # TODO: gérer le cas encore problématique du conjoint fonctionnaire

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        af_nbenf_fonc_holder = simulation.compute('af_nbenf_fonc', period)
        _P = simulation.legislation_at(period.start)

        fonc_nbenf = self.cast_from_entity_to_role(af_nbenf_fonc_holder, role = CHEF)
        P = _P.fonc.supp_fam
        part_fixe_1 = P.fixe.enf1
        part_fixe_2 = P.fixe.enf2
        part_fixe_supp = P.fixe.enfsupp
        part_fixe = (
            part_fixe_1 * (fonc_nbenf == 1) + part_fixe_2 * (fonc_nbenf == 2)
            + part_fixe_supp * max_(0, fonc_nbenf - 2)
            )
        # pct_variable_1 = 0
        pct_variable_2 = P.prop.enf2
        pct_variable_3 = P.prop.enf3
        pct_variable_supp = P.prop.enfsupp
        pct_variable = (
            pct_variable_2 * (fonc_nbenf == 2) + (pct_variable_3) * (fonc_nbenf == 3)
            + pct_variable_supp * max_(0, fonc_nbenf - 3))

        indice_maj_min = P.IM_min
        indice_maj_max = P.IM_max

        traitement_brut_mensuel_min = _traitement_brut_mensuel(indice_maj_min, _P)
        plancher_mensuel_1 = part_fixe
        plancher_mensuel_2 = part_fixe + traitement_brut_mensuel_min * pct_variable_2
        plancher_mensuel_3 = part_fixe + traitement_brut_mensuel_min * pct_variable_3
        plancher_mensuel_supp = traitement_brut_mensuel_min * pct_variable_supp

        plancher = (plancher_mensuel_1 * (fonc_nbenf == 1) +
                    plancher_mensuel_2 * (fonc_nbenf == 2) +
                    plancher_mensuel_3 * (fonc_nbenf >= 3) +
                    plancher_mensuel_supp * max_(0, fonc_nbenf - 3))

        traitement_brut_mensuel_max = _traitement_brut_mensuel(indice_maj_max, _P)
        plafond_mensuel_1 = part_fixe
        plafond_mensuel_2 = part_fixe + traitement_brut_mensuel_max * pct_variable_2
        plafond_mensuel_3 = part_fixe + traitement_brut_mensuel_max * pct_variable_3
        plafond_mensuel_supp = traitement_brut_mensuel_max * pct_variable_supp

        plafond = (plafond_mensuel_1 * (fonc_nbenf == 1) + plafond_mensuel_2 * (fonc_nbenf == 2) +
                   plafond_mensuel_3 * (fonc_nbenf == 3) +
                   plafond_mensuel_supp * max_(0, fonc_nbenf - 3))

        sft = min_(max_(part_fixe + pct_variable * traitement_indiciaire_brut, plancher), plafond) * (type_sal >= 2)
        # Nota Bene:
        # type_sal is an EnumCol which enum is:
        # CAT = Enum(['prive_non_cadre',
        #             'prive_cadre',
        #             'public_titulaire_etat',
        #             'public_titulaire_militaire',
        #             'public_titulaire_territoriale',
        #             'public_titulaire_hospitaliere',
        #             'public_non_titulaire'])
        return period, sft


def _traitement_brut_mensuel(indice_maj, law):
    Indice_majore_100_annuel = law.fonc.IM_100
    traitement_brut = Indice_majore_100_annuel * indice_maj / 100 / 12
    return traitement_brut


@reference_formula
class remuneration_principale(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Rémunération principale des agents titulaires de la fonction publique"

    def function(self, simulation, period):
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        nouvelle_bonification_indiciaire = simulation.calculate('nouvelle_bonification_indiciaire', period)
        type_sal = simulation.calculate('type_sal', period)
        return period, (
            (type_sal >= 2) * (type_sal <= 5) * (
                traitement_indiciaire_brut + nouvelle_bonification_indiciaire
                )
            )


@reference_formula
class salaire_net_a_payer(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Salaire net à payer (fiche de paie)"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        '''
        Calcul du salaire net à payer après déduction des sommes
        dues par les salarié avancées par l'employeur
        '''
        period = period
        salaire_net = simulation.calculate_add('salaire_net', period)
        depense_cantine_titre_restaurant_employe = simulation.calculate(
            'depense_cantine_titre_restaurant_employe')
        indemnites_forfaitaires = simulation.calculate('indemnites_forfaitaires', period)
        remuneration_apprenti = simulation.calculate('remuneration_apprenti', period)
        stage_gratification = simulation.calculate('stage_gratification', period)
        salaire_net_a_payer = (
            salaire_net +
            remuneration_apprenti +
            stage_gratification +
            depense_cantine_titre_restaurant_employe +
            indemnites_forfaitaires
            )
        return period, salaire_net_a_payer


@reference_formula
class salsuperbrut(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Salaires superbruts/coût du travail"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        remuneration_apprenti = simulation.calculate_add('remuneration_apprenti', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        primes_fonction_publique = simulation.calculate_add('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate_add('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate_add('supp_familial_traitement', period)
        cotisations_employeur = simulation.calculate('cotisations_employeur', period)
        depense_cantine_titre_restaurant_employeur = simulation.calculate(
            'depense_cantine_titre_restaurant_employeur', period)
        exoneration_cotisations_employeur_apprenti = simulation.calculate_add(
            'exoneration_cotisations_employeur_apprenti', period)
        exoneration_cotisations_employeur_geographiques = simulation.calculate(
            'exoneration_cotisations_employeur_geographiques', period)
        exoneration_cotisations_employeur_jei = simulation.calculate_add(
            'exoneration_cotisations_employeur_jei', period)
        exoneration_cotisations_employeur_stagiaire = simulation.calculate_add(
            'exoneration_cotisations_employeur_stagiaire', period)

        allegement_fillon = simulation.calculate_add('allegement_fillon', period)
        credit_impot_competitivite_emploi = simulation.calculate_add('credit_impot_competitivite_emploi', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            'reintegration_titre_restaurant_employeur', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)

        tehr = simulation.calculate_divide('tehr', period)
        salsuperbrut = (
            remuneration_apprenti +
            salaire_de_base + depense_cantine_titre_restaurant_employeur - reintegration_titre_restaurant_employeur +
            remuneration_principale +
            primes_fonction_publique + indemnite_residence + supp_familial_traitement
            - cotisations_employeur
            - allegement_fillon
            - exoneration_cotisations_employeur_geographiques
            - exoneration_cotisations_employeur_jei
            - exoneration_cotisations_employeur_apprenti
            - exoneration_cotisations_employeur_stagiaire
            - credit_impot_competitivite_emploi
            - tehr
            )

        return period, salsuperbrut
