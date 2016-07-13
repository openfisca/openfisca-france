# -*- coding: utf-8 -*-

from functools import partial
from numpy import (
    busday_count as original_busday_count, datetime64, maximum as max_, minimum as min_, timedelta64,
    )

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf

class indemnites_stage(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnités de stage"


class revenus_stage_formation_pro(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus de stage de formation professionnelle"


class bourse_recherche(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Bourse de recherche"




class sal_pen_exo_etr(Variable):
    cerfa_field = {
        QUIFOY['vous']: u"1AC",
        QUIFOY['conj']: u"1BC",
        QUIFOY['pac1']: u"1CC",
        QUIFOY['pac2']: u"1DC",
        }
    column = IntCol(val_type = "monetary")
    entity_class = Individus
    label = u"Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif"
    start_date = date(2013, 1, 1)




class frais_reels(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AK",
        QUIFOY['conj']: u"1BK",
        QUIFOY['pac1']: u"1CK",
        QUIFOY['pac2']: u"1DK",
        QUIFOY['pac3']: u"1EK",
        }
    column = IntCol(val_type = "monetary")
    entity_class = Individus
    label = u"Frais réels"

  # (f1ak, f1bk, f1ck, f1dk, f1ek)


class hsup(Variable):
    cerfa_field = {
        QUIFOY['vous']: u"1AU",
        QUIFOY['conj']: u"1BU",
        QUIFOY['pac1']: u"1CU",
        QUIFOY['pac2']: u"1DU",
        }
    column = IntCol(val_type = "monetary")
    entity_class = Individus
    label = u"Heures supplémentaires : revenus exonérés connus"
    start_date = date(2007, 1, 1)
    stop_date = date(2013, 12, 13)

  # (f1au, f1bu, f1cu, f1du)

class ppe_du_sa(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AV",
        QUIFOY['conj']: u"1BV",
        QUIFOY['pac1']: u"1CV",
        QUIFOY['pac2']: u"1DV",
        QUIFOY['pac3']: u"1QV",
        }
    column = IntCol
    entity_class = Individus
    label = u"Prime pour l'emploi des salariés: nombre d'heures payées dans l'année"

  # (f1av, f1bv, f1cv, f1dv, f1qv)

class ppe_tp_sa(Variable):
    cerfa_field = {
        QUIFOY['vous']: u"1AX",
        QUIFOY['conj']: u"1BX",
        QUIFOY['pac1']: u"1CX",
        QUIFOY['pac2']: u"1DX",
        QUIFOY['pac3']: u"1QX",
        }

    column = BoolCol
    entity_class = Individus
    label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière"

  # (f1ax, f1bx, f1cx, f1dx, f1qx)

class nbsala(Variable):
    column = EnumCol(
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
            ,
        )
    entity_class = Individus
    label = u"Nombre de salariés dans l'établissement de l'emploi actuel"



class tva_ent(Variable):
    column = BoolCol(default = True)
    entity_class = Individus
    label = u"L'entreprise employant le salarié paye de la TVA"



# build_column('code_risque', EnumCol(label = u"Code risque pour les accidents du travail"))
# TODO: Complete label, add enum and relevant default.

class exposition_accident(Variable):
    column = EnumCol(
        enum = Enum([
            u"Faible",
            u"Moyen",
            u"Élevé",
            u"Très élevé",
            ])
            ,
        )
    entity_class = Individus
    label = u"Exposition au risque pour les accidents du travail"




class allegement_fillon_mode_recouvrement(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"fin_d_annee",
                u"anticipe_regularisation_fin_de_periode",
                u"progressif",
                ],
            ),
        )
    entity_class = Individus
    label = u"Mode de recouvrement des allègements Fillon"


class allegement_cotisation_allocations_familiales_mode_recouvrement(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"fin_d_annee",
                u"anticipe_regularisation_fin_de_periode",
                u"progressif",
                ],
            ),
        )
    entity_class = Individus
    label = u"Mode de recouvrement de l'allègement de la cotisation d'allocations familiales"


class apprentissage_contrat_debut(Variable):
    column = DateCol()
    entity_class = Individus
    label = u"Date de début du contrat d'apprentissage"


class arrco_tranche_a_taux_employeur(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Taux ARRCO tranche A employeur) propre à l'entreprise"


class arrco_tranche_a_taux_salarie(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Taux ARRCO tranche A salarié) propre à l'entreprise"


class assujettie_taxe_salaires(Variable):
    column = BoolCol()
    entity_class = Individus
    label = u"Entreprise assujettie à la taxe sur les salaires"


class avantage_en_nature_valeur_reelle(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Avantages en nature (Valeur réelle)"


class indemnites_compensatrices_conges_payes(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"indemnites_compensatrices_conges_payes"


class indemnite_fin_contrat_due(Variable):
    column = BoolCol()
    entity_class = Individus
    label = u"indemnite_fin_contrat_due"


class contrat_de_travail(Variable):
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
        )
    entity_class = Individus
    label = u"Type contrat de travail"


class contrat_de_travail_debut(Variable):
    column = DateCol(default = date(1870, 1, 1))
    entity_class = Individus
    label = u"Date d'arrivée dans l'entreprise"


class contrat_de_travail_fin(Variable):
    column = DateCol(default = date(2099, 12, 31))
    entity_class = Individus
    label = u"Date de départ de l'entreprise"


class contrat_de_travail_duree(Variable):
    column = EnumCol(
        enum = Enum([
            u"cdi",
            u"cdd",
            ]),
        )
    entity_class = Individus
    label = u"Type (durée determinée ou indéterminée) du contrat de travail"


class cotisation_sociale_mode_recouvrement(Variable):
    column = EnumCol(
        enum = Enum([
            u"Mensuel avec régularisation en fin d'année",
            u"Annuel",
            ]),
        )
    entity_class = Individus
    label = u"Mode de recouvrement des cotisations sociales"

class entreprise_est_association_non_lucrative(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est une association à but non lucratif, par exemple loi de 1901"


class depcom_entreprise(Variable):
    column = FixedStrCol(max_length = 5)
    entity_class = Individus
    label = u"Localisation entreprise (depcom)"


class code_postal_entreprise(Variable):
    column = FixedStrCol(max_length = 5)
    entity_class = Individus
    label = u"Localisation entreprise (Code postal)"


class effectif_entreprise(Variable):
    entity_class = Individus
    column = IntCol()
    base_function = requested_period_last_value
    label = u"Effectif de l'entreprise"
    set_input = set_input_dispatch_by_period


class entreprise_assujettie_cet(Variable):
    column = BoolCol()
    entity_class = Individus
    label = u"Entreprise assujettie à la contribution économique territoriale"


class entreprise_assujettie_is(Variable):
    column = BoolCol()
    entity_class = Individus
    label = u"Entreprise assujettie à l'impôt sur les sociétés (IS)"


class entreprise_assujettie_tva(Variable):
    column = BoolCol()
    entity_class = Individus
    label = u"Entreprise assujettie à la TVA"


class entreprise_benefice(Variable):
    column = FloatCol()
    entity_class = Individus
    set_input = set_input_divide_by_period
    label = u"Bénéfice de l'entreprise"


class entreprise_bilan(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Bilan de l'entreprise"


class entreprise_chiffre_affaire(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Chiffre d'affaire de l'entreprise"


class entreprise_creation(Variable):
    column = DateCol()
    entity_class = Individus
    label = u"Date de création de l'entreprise"


class nombre_tickets_restaurant(Variable):
    column = IntCol()
    entity_class = Individus
    base_function = requested_period_last_value
    label = u"Nombre de tickets restaurant"


class nouvelle_bonification_indiciaire(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Nouvelle bonification indicaire"


class prevoyance_obligatoire_cadre_taux_employe(Variable):
    column = FloatCol(default = 0.015)  # 1.5% est le minimum en 2014
    entity_class = Individus
    base_function = requested_period_last_value
    label = u"Taux de cotisation employeur pour la prévoyance obligatoire des cadres"


class prevoyance_obligatoire_cadre_taux_employeur(Variable):
    column = FloatCol(default = 0.015)  # 1.5% est le minimum en 2014
    entity_class = Individus
    base_function = requested_period_last_value
    label = u"Taux de cotisation employeur pour la prévoyance obligatoire des cadres"


class primes_salaires(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Indemnités, primes et avantages en argent"


class complementaire_sante_montant(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Montant de la complémentaire santé obligatoire retenue par l'employeur"


class complementaire_sante_taux_employeur(Variable):
    column = FloatCol(default = 0.5)
    # La part minimum légale est de 50 %
    entity_class = Individus
    label = u"Part de la complémentaire santé obligatoire payée par l'employeur"


class prise_en_charge_employeur_prevoyance_complementaire(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Part salariale des cotisations de prévoyance complémentaire prise en charge par l'employeur"


class prise_en_charge_employeur_retraite_complementaire(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Part salariale des cotisations de retraite complémentaire prise en charge par l'employeur"


class prise_en_charge_employeur_retraite_supplementaire(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Part salariale des cotisations de retraite supplémentaire prise en charge par l'employeur"


class ratio_alternants(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Ratio d'alternants dans l'effectif moyen"


class remboursement_transport_base(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Base pour le calcul du remboursement des frais de transport"


class indemnites_forfaitaires(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Indemnités forfaitaires (transport, nourriture)"


class salaire_de_base(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Salaire de base, en général appelé salaire brut, la 1ère ligne sur la fiche de paie"
    set_input = set_input_divide_by_period
    url = u'http://www.insee.fr/fr/methodes/default.asp?page=definitions/salaire-mensuel-base-smb.htm'


class titre_restaurant_taux_employeur(Variable):
    column = FloatCol(default = 0.5)
    entity_class = Individus
    label = u"Taux de participation de l'employeur au titre restaurant"


class titre_restaurant_valeur_unitaire(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Valeur faciale unitaire du titre restaurant"


class titre_restaurant_volume(Variable):
    column = IntCol()
    entity_class = Individus
    label = u"Volume des titres restaurant"


class traitement_indiciaire_brut(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Traitement indiciaire brut (TIB)"


class categorie_salarie(Variable):
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
        )
    entity_class = Individus
    label = u"Catégorie de salarié"


class heures_duree_collective_entreprise(Variable):
    column = IntCol()  # TODO default la valeur de la durée légale ?
    entity_class = Individus
    label = u"Durée mensuelle collective dans l'entreprise (heures, temps plein)"


class heures_non_remunerees_volume(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)"


class heures_remunerees_volume(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Volume des heures rémunérées contractuellement (heures/mois, temps partiel)"


class forfait_heures_remunerees_volume(Variable):
    column = IntCol()
    entity_class = Individus
    label = u"Volume des heures rémunérées à un forfait heures"


class forfait_jours_remuneres_volume(Variable):
    column = IntCol()
    entity_class = Individus
    label = u"Volume des heures rémunérées à forfait jours"


class volume_jours_ijss(Variable):
    column = IntCol()
    entity_class = Individus
    label = u"Volume des jours pour lesquels sont versés une idemnité journalière par la sécurité sociale"


class avantage_en_nature(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Avantages en nature"

    def function(self, simulation, period):
        period = period
        avantage_en_nature_valeur_reelle = simulation.calculate('avantage_en_nature_valeur_reelle', period)
        avantage_en_nature_valeur_forfaitaire = simulation.calculate('avantage_en_nature_valeur_forfaitaire', period)

        return period, avantage_en_nature_valeur_reelle + avantage_en_nature_valeur_forfaitaire


class avantage_en_nature_valeur_forfaitaire(Variable):
    # base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Evaluation fofaitaire des avantages en nature "

    # TODO: coplete this function
    def function(self, simulation, period):
        period = period
        avantage_en_nature_valeur_reelle = simulation.calculate('avantage_en_nature_valeur_reelle', period)

        return period, avantage_en_nature_valeur_reelle * 0


class depense_cantine_titre_restaurant_employe(Variable):
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


class depense_cantine_titre_restaurant_employeur(Variable):
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


class nombre_jours_calendaires(Variable):
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


class remboursement_transport(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Remboursement partiel des frais de transport par l'employeur"

    def function(self, simulation, period):

        remboursement_transport_base = simulation.calculate('remboursement_transport_base', period)
        # TODO: paramètres en dur dans le code
        return period, - .5 * remboursement_transport_base


# Fonction publique

class gipa(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de garantie individuelle du pouvoir d'achat"
    # TODO: à coder

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        return period, self.zeros()


class indemnite_residence(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de résidence des fonctionnaires"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)
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
            ) * (categorie_salarie >= 2)


class indice_majore(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Indice majoré"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        _P = simulation.legislation_at(period.start)

        traitement_annuel_brut = _P.fonc.IM_100
        return period, (traitement_indiciaire_brut * 100 * 12 / traitement_annuel_brut) * (categorie_salarie >= 2)


class primes_fonction_publique(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul des primes pour les fonctionnaries"
    url = u"http://vosdroits.service-public.fr/particuliers/F465.xhtml"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        public = (
            (categorie_salarie == CAT['public_titulaire_etat']) +
            (categorie_salarie == CAT['public_titulaire_territoriale']) +
            (categorie_salarie == CAT['public_titulaire_hospitaliere'])
            )
        return period, TAUX_DE_PRIME * traitement_indiciaire_brut * public


class af_nbenf_fonc(Variable):
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
        autonomie_financiere_holder = (salaire_de_base / 6) >= (law.fam.af.seuil_rev_taux * smic_mensuel_brut)
        age = self.split_by_roles(age_holder, roles = ENFS)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)
        af_nbenf = nb_enf(age, autonomie_financiere, law.fam.af.age1, law.fam.af.age2)

        return period, af_nbenf


class supp_familial_traitement(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Supplément familial de traitement"
    # Attention : par hypothèse ne peut êre attribué qu'à la tête du ménage
    # TODO: gérer le cas encore problématique du conjoint fonctionnaire

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        af_nbenf_fonc_holder = simulation.compute('af_nbenf_fonc', period)
        _P = simulation.legislation_at(period.start)

        fonc_nbenf = self.cast_from_entity_to_role(af_nbenf_fonc_holder, role = CHEF)
        P = _P.fonc.supp_fam
        part_fixe_1 = P.fixe.enf1
        part_fixe_2 = P.fixe.enf2
        part_fixe_supp = P.fixe.enfsupp
        part_fixe = (
            part_fixe_1 * (fonc_nbenf == 1) + part_fixe_2 * (fonc_nbenf == 2) +
            part_fixe_supp * max_(0, fonc_nbenf - 2)
            )
        # pct_variable_1 = 0
        pct_variable_2 = P.prop.enf2
        pct_variable_3 = P.prop.enf3
        pct_variable_supp = P.prop.enfsupp
        pct_variable = (
            pct_variable_2 * (fonc_nbenf == 2) + (pct_variable_3) * (fonc_nbenf == 3) +
            pct_variable_supp * max_(0, fonc_nbenf - 3))

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

        sft = (categorie_salarie >= 2) * min_(
            max_(part_fixe + pct_variable * traitement_indiciaire_brut, plancher),
            plafond
            )
        # Nota Bene:
        # categorie_salarie is an EnumCol which enum is:
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


class remuneration_principale(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Rémunération principale des agents titulaires de la fonction publique"

    def function(self, simulation, period):
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        nouvelle_bonification_indiciaire = simulation.calculate('nouvelle_bonification_indiciaire', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        return period, (
            (categorie_salarie >= 2) * (categorie_salarie <= 5) * (
                traitement_indiciaire_brut + nouvelle_bonification_indiciaire
                )
            )


class salaire_net_a_payer(Variable):
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


class salaire_super_brut_hors_allegements(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Salaire super-brut (fiche de paie): rémunération + cotisations sociales employeur"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        remuneration_principale = simulation.calculate('remuneration_principale', period)
        remuneration_apprenti = simulation.calculate_add('remuneration_apprenti', period)

        primes_fonction_publique = simulation.calculate_add('primes_fonction_publique', period)
        indemnite_residence = simulation.calculate_add('indemnite_residence', period)
        supp_familial_traitement = simulation.calculate_add('supp_familial_traitement', period)
        cotisations_employeur = simulation.calculate('cotisations_employeur', period)
        depense_cantine_titre_restaurant_employeur = simulation.calculate(
            'depense_cantine_titre_restaurant_employeur', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            'reintegration_titre_restaurant_employeur', period)
        indemnite_fin_contrat = simulation.calculate('indemnite_fin_contrat', period)
        salaire_super_brut_hors_allegements = (
            salaire_de_base + remuneration_principale + remuneration_apprenti +
            primes_fonction_publique + indemnite_residence + supp_familial_traitement + indemnite_fin_contrat +
            depense_cantine_titre_restaurant_employeur - reintegration_titre_restaurant_employeur
            - cotisations_employeur
            )

        return period, salaire_super_brut_hors_allegements


class salaire_super_brut(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Coût du travail à court terme. Inclut les exonérations et allègements de charges"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        salaire_super_brut_hors_allegements = simulation.calculate('salaire_super_brut_hors_allegements', period)
        exonerations_et_allegements = simulation.calculate('exonerations_et_allegements', period)

        return period, salaire_super_brut_hors_allegements - exonerations_et_allegements


class exonerations_et_allegements(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Charges, aides et crédits différées ou particulières"

    def function(self, simulation, period):
        exoneration_cotisations_employeur_apprenti = simulation.calculate_add(
            'exoneration_cotisations_employeur_apprenti', period)
        exoneration_cotisations_employeur_geographiques = simulation.calculate(
            'exoneration_cotisations_employeur_geographiques', period)
        exoneration_cotisations_employeur_jei = simulation.calculate_add(
            'exoneration_cotisations_employeur_jei', period)
        exoneration_cotisations_employeur_stagiaire = simulation.calculate_add(
            'exoneration_cotisations_employeur_stagiaire', period)

        allegement_fillon = simulation.calculate_add('allegement_fillon', period)
        allegement_cot_alloc_fam = simulation.calculate_add('allegement_cotisation_allocations_familiales', period)

        return period, (
            allegement_fillon +
            allegement_cot_alloc_fam +
            exoneration_cotisations_employeur_geographiques +
            exoneration_cotisations_employeur_jei +
            exoneration_cotisations_employeur_apprenti +
            exoneration_cotisations_employeur_stagiaire
            )


class cout_du_travail(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Coût du travail à long terme. Inclut les charges, aides et crédits différés"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        salaire_super_brut = simulation.calculate('salaire_super_brut', period)
        cout_differe = simulation.calculate('cout_differe', period)

        return period, salaire_super_brut - cout_differe


class cout_differe(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Charges, aides et crédits différées ou particulières"

    def function(self, simulation, period):
        credit_impot_competitivite_emploi = simulation.calculate_add('credit_impot_competitivite_emploi', period)
        aide_premier_salarie = simulation.calculate_add('aide_premier_salarie', period)
        aide_embauche_pme = simulation.calculate_add('aide_embauche_pme', period)
        tehr = simulation.calculate_divide('tehr', period)

        return period, credit_impot_competitivite_emploi + aide_premier_salarie + aide_embauche_pme + tehr
