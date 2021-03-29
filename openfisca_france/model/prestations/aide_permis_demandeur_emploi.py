from openfisca_france.model.base import Variable, Individu, TypesActivite, MONTH


class aide_permis_demandeur_emploi_eligibilite_financiere(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité financière à l'aide à l’obtention du permis de conduire automobile pour les demandeurs d’emploi"
    reference = [
        "Délibération n°2011/13 du 11 avril 2011",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n201113-du-11-avril.html?type=dossiers/2011/bope-n2011-36-du-18-avril-2011"
        ]
    definition_period = MONTH

    def formula(individu, period, parameters):
        sans_rsa = individu.famille('rsa', period) <= 0
        sans_aah = individu('aah', period) <= 0

        allocation_journaliere_minimum = parameters(period).allocation_retour_emploi.montant_minimum
        plafond_chomage = allocation_journaliere_minimum * 31
        chomage_minimum = individu('chomage_brut', period) <= plafond_chomage

        return sans_rsa * sans_aah * chomage_minimum


class aide_permis_demandeur_emploi_eligibilite_individu(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité individuelle à l'aide à l’obtention du permis de conduire automobile pour les demandeurs d’emploi"
    reference = [
        "Délibération n°2011/13 du 11 avril 2011",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n201113-du-11-avril.html?type=dossiers/2011/bope-n2011-36-du-18-avril-2011"
        ]
    definition_period = MONTH

    def formula(individu, period):
        return individu('activite', period) == TypesActivite.chomeur


class aide_permis_demandeur_emploi(Variable):
    value_type = float
    entity = Individu
    label = "Aide à l’obtention du permis de conduire automobile pour les demandeurs d’emploi"
    reference = [
        "Délibération n°2011/13 du 11 avril 2011",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n201113-du-11-avril.html?type=dossiers/2011/bope-n2011-36-du-18-avril-2011",
        "Instruction PE n°2011-205 du 9 décembre 2011",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-pe-n2011-205-du-9-de.html?type=dossiers/2011/bope-n2011-112-du-9-decembre-201",
        ]
    definition_period = MONTH

    def formula(individu, period, parameters):
        eligibilite_financiere = individu('aide_permis_demandeur_emploi_eligibilite_financiere', period)
        eligibilite_individu = individu('aide_permis_demandeur_emploi_eligibilite_individu', period)

        montant = parameters(period).prestations.transport.aide_permis_demandeur_emploi.montant
        return montant * eligibilite_financiere * eligibilite_individu
