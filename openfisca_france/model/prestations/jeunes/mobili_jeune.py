from openfisca_france.model.base import (
    Variable, Individu, MONTH,
    TypesCategorieSalarie, TypesSecteurActivite, TypesStatutOccupationLogement,
    min_, where, set_input_dispatch_by_period, set_input_divide_by_period
    )


class mobili_jeune(Variable):
    value_type = float
    label = "Montant de l'aide au logement mobili-jeune"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.actionlogement.fr/l-aide-mobili-jeune"

    def formula_2012_07(individu, period, parameters):
        loyer = individu.menage('loyer', period)
        charges_locatives = individu.menage('charges_locatives', period)
        aide_logement = individu.famille('aide_logement', period)

        reste_a_charge = loyer + charges_locatives - aide_logement

        eligibilite = individu('mobili_jeune_eligibilite', period)

        return where(
            reste_a_charge >= parameters(period).prestations.mobili_jeune.montant.minimum,
            eligibilite * min_(reste_a_charge, parameters(period).prestations.mobili_jeune.montant.maximum),
            0,
            )


class mobili_jeune_eligibilite_employeur(Variable):
    value_type = bool
    label = "Conditions à remplir par l'employeur d'un demandeur d'aide au logement mobili-jeune"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.actionlogement.fr/l-aide-mobili-jeune"

    def formula_2012_07(individu, period):
        secteur_prive_non_agricole = (
            individu("categorie_salarie", period) == TypesCategorieSalarie.prive_non_cadre
            ) * (
                individu("secteur_activite_employeur", period) == TypesSecteurActivite.non_agricole
            )
        contributeur_peec = individu("peec_employeur", period)

        return secteur_prive_non_agricole * contributeur_peec


class mobili_jeune_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité à l'aide au logement mobili-jeune"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.actionlogement.fr/l-aide-mobili-jeune"
    documentation = '''
    Conditions non modélisées :
    Etre locataire d'un logement en proximité géographique avec le lieu de la formation ou de l'entreprise.
    Avoir déposé la demande 3 mois avant la date de démarrage du cycle de formation ou jusqu’à 6 mois après cette date.
    Avoir un reste à charge de loyer après déduction d'APL/ALS supérieur ou égal à 10€.
    '''

    def formula_2012_07(individu, period, parameters):
        condition_age = individu("age", period) < parameters(period).prestations.mobili_jeune.age_maximum

        alternant = individu("alternant", period)  # sous contrat d'apprentissage ou de professionnalisation
        mobili_jeune_eligibilite_employeur = individu("mobili_jeune_eligibilite_employeur", period)

        smic_mensuel_brut = individu("smic_proratise", period)
        condition_remuneration = individu("salaire_de_base", period) <= smic_mensuel_brut

        statut_occupation_logement = individu.menage("statut_occupation_logement", period)
        locataire = (
            (statut_occupation_logement == TypesStatutOccupationLogement.locataire_hlm)
            + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_vide)
            + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_meuble)
            + (statut_occupation_logement == TypesStatutOccupationLogement.locataire_foyer)
            )

        return condition_age * alternant * mobili_jeune_eligibilite_employeur * condition_remuneration * locataire
