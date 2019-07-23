# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class rente_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel de la rente d’accident du travail"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006743072&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(individu, period):
        previous_year = period.start.period('year').offset(-1)
        non_salarie_agricole = individu('tns_benefice_exploitant_agricole', previous_year, options=[ADD]) != 0
        rente_accident_travail_salarie = individu('rente_accident_travail_salarie', period)
        rente_accident_travail_exploitant_agricole = individu('rente_accident_travail_exploitant_agricole', period)

        return where(non_salarie_agricole, rente_accident_travail_exploitant_agricole, rente_accident_travail_salarie)


class rente_accident_travail_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Montant de la rente d’accident du travail pour les victimes salariées"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006743072&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(individu, period):
        previous_year = period.start.period('year').offset(-1)
        salarie = individu('salaire_net', previous_year, options=[ADD]) != 0
        rente_accident_travail_rachat = individu('rente_accident_travail_rachat', period)
        taux_incapacite = individu('taux_accident_travail', period)
        rente_accident_travail_base = individu('rente_accident_travail_base', period) * salarie
        rente_accident_travail_apres_rachat = individu('rente_accident_travail_apres_rachat', period)

        montant_rente_accident_travail = where(rente_accident_travail_rachat != 0, rente_accident_travail_apres_rachat,
                                               rente_accident_travail_base)

        return select(
            [taux_incapacite < 0.1, taux_incapacite >= 0.1],
            [0, montant_rente_accident_travail / 12]
            )


class rente_accident_travail_exploitant_agricole(Variable):
    value_type = float
    entity = Individu
    label = "Montant de la rente d’accident du travail pour les chefs d'exploitation ou d'entreprise agricole"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006071367&idArticle=LEGIARTI000006598097&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(individu, period):
        previous_year = period.start.period('year').offset(-1)
        non_salarie_agricole = individu('tns_benefice_exploitant_agricole', previous_year, options=[ADD]) != 0
        rente_accident_travail_rachat = individu('rente_accident_travail_rachat', period)
        taux_incapacite = individu('taux_accident_travail', period)
        rente_accident_travail_base = individu('rente_accident_travail_base', period) * non_salarie_agricole
        rente_accident_travail_apres_rachat = individu('rente_accident_travail_apres_rachat', period)

        montant_rente_accident_travail = where(rente_accident_travail_rachat != 0, rente_accident_travail_apres_rachat,
                                               rente_accident_travail_base)
        return select(
            [taux_incapacite < 0.3, taux_incapacite >= 0.3],
            [0, montant_rente_accident_travail / 12]
            )


class indemnite_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = "Indemnité selon le taux d'incapacité"
    reference = "https://www.legifrance.gouv.fr/affichCode.do?idSectionTA=LEGISCTA000006172216&cidTexte=LEGITEXT000006073189"
    definition_period = MONTH

    def formula(individu, period, parameters):
        indem_at = parameters(period).accident_travail.rente.taux
        taux_incapacite = individu('taux_accident_travail', period)

        return indem_at.indemnite_accident_travail.baremes.calc(taux_incapacite * 100)


class rente_accident_travail_base(Variable):
    value_type = float
    entity = Individu
    label = "Montant de base de la rente d’accident du travail"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006743072&dateTexte=&categorieLien=cid"
    definition_period = MONTH

    def formula(individu, period, parameters):
        param_rente_at = parameters(period).accident_travail.rente.taux
        taux_incapacite = individu('taux_accident_travail', period)
        taux = param_rente_at.bareme.calc(taux_incapacite)
        taux_rente_accident_travail = select([taux_incapacite < param_rente_at.taux_minimum], [0], default=taux)
        rente_accident_travail_base = individu('rente_accident_travail_salaire_utile', period) * taux_rente_accident_travail

        return rente_accident_travail_base


class demande_rachat(Variable):
    value_type = bool
    entity = Individu
    label = "La victime a demandé le rachat partiel de la rente"
    definition_period = MONTH


class rente_accident_travail_apres_rachat(Variable):
    value_type = float
    entity = Individu
    label = "Rente d’accident du travail, reliquat suite à conversion en capital"
    definition_period = MONTH

    def formula(individu, period, parameters):
        rente_at = parameters(period).accident_travail.rente.taux
        age = min_(max_(individu('age', period), 16), 100)
        rente_accident_travail_rachat = individu('rente_accident_travail_rachat', period)
        conversion_rente_capital = rente_at.capital_representatif[age]
        rente_accident_travail_base = individu('rente_accident_travail_base', period)
        rente_apres_rachat = rente_accident_travail_base - (rente_accident_travail_rachat / conversion_rente_capital)

        return rente_apres_rachat


class rente_accident_travail_rachat(Variable):
    value_type = float
    entity = Individu
    label = "Rachat de la rente d’accident du travail"
    reference = "https://www.legifrance.gouv.fr/eli/arrete/2016/12/19/AFSS1637858A/jo/texte"
    definition_period = MONTH

    def formula(individu, period, parameters):
        rente_at = parameters(period).accident_travail.rente.taux
        demande_rachat = individu('demande_rachat', period)
        age = min_(max_(individu('age', period), 16), 100)
        conversion_rente_capital = rente_at.capital_representatif[age]
        rente_accident_travail_base = individu('rente_accident_travail_base', period)
        rachat = (rente_accident_travail_base * conversion_rente_capital) / 4

        return rachat * demande_rachat


class pcrtp_nombre_actes_assistance(Variable):
    value_type = int
    entity = Individu
    label = "Nombre d'actes nécessitant l'assistance d'une tierce personne"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=6D8F7F6917ADFBDEAFE1D8A432F39229.tplgfr23s_2?idArticle=LEGIARTI000027267037&cidTexte=LEGITEXT000006073189&dateTexte=20181218"
    definition_period = MONTH


class pcrtp(Variable):
    value_type = float
    entity = Individu
    label = "Prestation complémentaire pour recours à tierce personne (PCRTP)"
    reference = "https://www.legifrance.gouv.fr/affichCode.do?idSectionTA=LEGISCTA000006172216&cidTexte=LEGITEXT000006073189"
    definition_period = MONTH

    def formula(individu, period, parameters):
        rente_at = parameters(period).accident_travail.rente.taux
        taux_incapacite = individu('taux_accident_travail', period)
        pcrtp_nombre_actes_assistance = individu('pcrtp_nombre_actes_assistance', period)
        montant_pcrtp = rente_at.pcrtp[pcrtp_nombre_actes_assistance]

        return montant_pcrtp * (taux_incapacite >= 0.8)


class rente_accident_travail_salaire_utile(Variable):
    value_type = float
    entity = Individu
    label = "Salaire utile pour calculer la rente d’accident du travail"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=7392B9902E4B974EAE8783FAF2D69849.tplgfr30s_1?idArticle=LEGIARTI000006750376&cidTexte=LEGITEXT000006073189&dateTexte=20180823"
    definition_period = MONTH

    def formula(individu, period, parameters):
        previous_year = period.start.period('year').offset(-1)
        rente_at = parameters(period).accident_travail.rente

        salaire_net = individu('salaire_net', previous_year, options=[ADD])
        tns_benefice_exploitant_agricole = individu('tns_benefice_exploitant_agricole', previous_year, options=[ADD])
        salaire = max_(salaire_net, tns_benefice_exploitant_agricole)
        salaire_net_base = max_(rente_at.salaire_net.salaire_minimum, salaire)
        coef = salaire_net_base / rente_at.salaire_net.salaire_minimum
        bareme = rente_at.salaire_net.bareme.calc(coef)
        return rente_at.salaire_net.salaire_minimum * bareme
