from openfisca_france.model.base import *


class cheque_energie_unites_consommation(Variable):
    entity = Menage
    value_type = float
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=1EA40CA7787AF90A95D1E1B3155D9028.tplgfr29s_1?idArticle=LEGIARTI000032497834&cidTexte=LEGITEXT000023983208&dateTexte=20160511"
    label = "Unités de consommation du ménage pour le calcul du chèque Énergie"
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
        uc = parameters(period).cheque_energie.unites_consommation
        nb_personnes = menage.nb_persons()
        gardes_alternees = menage.sum(menage.members('garde_alternee', period.first_month))

        nb_personnes_ajuste = nb_personnes - 0.5 * gardes_alternees
        return (
            uc.premiere_personne
            + uc.deuxieme_personne * (nb_personnes_ajuste > 1) * (min_(nb_personnes_ajuste, 2) - 1)
            + uc.autres_personnes * (nb_personnes_ajuste > 2) * (nb_personnes_ajuste - 2)
            )


class cheque_energie_eligibilite_logement(Variable):
    entity = Menage
    value_type = bool
    reference = [
        "Article L124-1 du Code de l'énergie",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=5AB50D02153C9CB753729850314A2E17.tplgfr29s_1?idArticle=LEGIARTI000031057544&cidTexte=LEGITEXT000023983208&dateTexte=20180314",
        "Article LO6314-3 du Code général des collectivités territoriales",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=6A3717E70623B148432581CC8F585C5F.tplgfr31s_1?idArticle=LEGIARTI000006394061&cidTexte=LEGITEXT000006070633&dateTexte=20180316",
        ]
    label = "Éligibilité du logement occupé au chèque énergie"
    definition_period = YEAR
    set_input = set_input_dispatch_by_period

    def formula_2017(menage, period, parameters):
        statut_occupation_logement = menage('statut_occupation_logement', period.first_month)
        residence_saint_martin = menage('residence_saint_martin', period.first_month)

        return (
            not_(residence_saint_martin) * (
                + (statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant)
                + (statut_occupation_logement == TypesStatutOccupationLogement.proprietaire)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_vide)
                + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble)
                )
            )


class cheque_energie_montant(Variable):
    entity = Menage
    value_type = float
    reference = [
        "https://www.legifrance.gouv.fr/eli/decret/2016/5/6/DEVR1604032D/jo/article_1",
        "https://www.legifrance.gouv.fr/eli/arrete/2018/12/26/TRER1832961A/jo/texte",
        ]
    label = "Montant du chèque énergie"
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
        baremes = parameters(period).cheque_energie.baremes

        uc_menage = menage('cheque_energie_unites_consommation', period)
        rfr = menage.sum(menage.members.foyer_fiscal('rfr', period.n_2), role = FoyerFiscal.DECLARANT_PRINCIPAL)

        ressources_par_uc = rfr / uc_menage

        return (
            (uc_menage <= 1) * baremes.une_uc.calc(ressources_par_uc)
            + ((uc_menage > 1) * (uc_menage < 2)) * baremes.une_uc_a_deux_uc.calc(ressources_par_uc)
            + (uc_menage >= 2) * baremes.plus_de_deux_ucs.calc(ressources_par_uc)
            )


class cheque_energie(Variable):
    entity = Menage
    value_type = float
    reference = "https://chequeenergie.gouv.fr"
    label = "Montant auquel le ménage peut prétendre au titre du chèque energie"
    definition_period = YEAR
    set_input = set_input_divide_by_period

    def formula_2017(menage, period):
        eligible = menage('cheque_energie_eligibilite_logement', period)
        declarant = menage.sum(menage.members('age', period.first_month) * 0 + 1, role = FoyerFiscal.DECLARANT) > 0  # une colocation de personnes à la charge de leurs parents n'est pas éligible aux chèques énergie, par exemple
        montant = menage('cheque_energie_montant', period.this_year)
        return declarant * eligible * montant


class aide_exceptionnelle_cheque_energie(Variable):
    entity = Menage
    value_type = float
    label = "Aide exceptionnelle de 100 euros pour les personnes bénéficiaires du chèque énergie"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = "2021-12-31"

    def formula_2021_12_01(menage, period, parameters):
        cheque_energie = menage('cheque_energie', period.this_year)
        montant_aide = parameters(period).cheque_energie.aide_exceptionnelle

        return montant_aide * (cheque_energie > 0)
