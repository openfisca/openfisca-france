from openfisca_france.model.base import *


class professionnalisation(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est en contrat de professionnalisation"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000031088014/2016-01-01/"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        age = individu('age', period)
        ass = individu('ass', period)
        rsa = individu.famille('rsa', period)
        aah = individu('aah', period)

        age_condition = (16 <= age) * (age < 25)
        dummy_ass = ass > 0
        dummy_rmi = rsa > 0
        dummy_aah = aah > 0

        return (age_condition + dummy_ass + dummy_aah + dummy_rmi) > 0


class qualifie(Variable):
    value_type = bool
    entity = Individu
    label = "Etat du niveau de formation ou de qualification avant le contrat de professionnalisation"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://travail-emploi.gouv.fr/formation-professionnelle/formation-en-alternance-10751/contrat-de-professionnalisation"


class remuneration_professionnalisation(Variable):
    value_type = float
    entity = Individu
    label = "Rémunération de l'apprenti sous contrat de professionalisation"
    reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    #  La rémunération minimale varie en fonction de l'âge et du niveau de qualification des bénéficiaires des contrats
    #  de professionnalisation :
    #
    #  Pour les personnes de moins de 21 ans :
    #  au minimum 55 % du Smic,
    #  au minimum 65 % du Smic si le jeune est titulaire d'une qualification au moins égale au baccalauréat
    #  professionnel ou d'un titre ou d'un diplôme à finalité professionnelle de même niveau.
    #
    #  Pour les personnes ayant entre 21 et 25 ans :
    #  au minimum 70 % du Smic,
    #  au minimum 80 % du Smic si le bénéficiaire est titulaire d'une qualification au moins égale à celle d'un
    #  baccalauréat professionnel ou d'un titre/diplôme à finalité professionnelle de même niveau.
    #
    #  Pour les personnes âgées de plus de 26 ans :
    #  au minimum le Smic,
    #  au minimum 85 % du salaire minimum prévu par la convention ou l'accord de branche auquel est soumise
    #  l'entreprise.

    def formula(individu, period, parameters):
        age = individu('age', period)
        smic = parameters(period).marche_travail.salaire_minimum.smic.smic_b_horaire * 52 * 35 / 12
        professionnalisation = individu('professionnalisation', period)
        qualifie = individu('qualifie', period)
        salaire_en_smic = [
            dict(
                part_de_smic_by_qualification = {
                    'non_qualifie': .55,
                    'qualifie': .65
                    },
                age_min = 16,
                age_max = 21,
                ),
            dict(
                part_de_smic_by_qualification = {
                    1: .70,
                    },
                age_min = 21,
                age_max = 25,
                ),
            dict(
                part_de_smic_by_qualification = {
                    1: 1.0,
                    },
                age_min = 26,
                age_max = 99
                )
            ]

        taux_smic = age * 0.0
        for age_interval in salaire_en_smic:
            age_condition = (age_interval['age_min'] <= age) * (age <= age_interval['age_max'])
            taux_smic[age_condition] = sum([
                (qualifie[age_condition] == qualification) * part_de_smic
                for qualification, part_de_smic in age_interval['part_de_smic_by_qualification'].items()
                ])
        return taux_smic * smic * professionnalisation


class exoneration_cotisations_employeur_professionnalisation(Variable):
    value_type = float
    entity = Individu
    label = "Exonération de cotisations patronales pour l'emploi d'un apprenti"
    reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    #  Exonération de cotisations sociales patronales d'assurance maladie-maternité, de vieillesse de base,
    #  d'invalidité-décès et d'allocations familiales au titre des rémunérations versées aux demandeurs d'emploi de
    #  plus de 45 ans
    #
    #  Les salariés en contrat de professionnalisation ne sont pas comptabilisés dans l'effectif de l'entreprise pendant
    #  la durée du contrat s'il est à durée déterminée ou pendant l'action de professionnalisation si le contrat est à
    #  durée indéterminée.
    #  Remboursement de certaines dépenses par les organismes collecteurs paritaires agréés (OPCA)
    #  Aide forfaitaire versée par Pôle emploi pour l'embauche d'un demandeur d'emploi de 26 ans et plus
    #  En cas d'embauche d'un demandeur d'emploi de 26 ans et plus, l'employeur peut bénéficier d'une aide forfaitaire
    #  (AFE) d'un montant maximum de 2 000 euros par bénéficiaire. Pour les salariés à temps partiel, le montant de
    #  l'aide est proratisé en fonction du temps de travail effectif.
    #  Aide spécifique de 686 euros par accompagnement et pour une année pleine est attribuée sous certaines conditions
    #  aux groupements d'employeurs qui organisent dans le cadre des contrats de professionnalisation

    def formula(individu, period, parameters):
        age = individu('age', period)
        mmid_employeur = individu('mmid_employeur', period)
        famille = individu('famille', period)
        vieillesse_plafonnee_employeur = individu('vieillesse_plafonnee_employeur', period)
        # FIXME: correspond bien à vieillesse de base ?
        cotisations_exonerees = mmid_employeur + famille + vieillesse_plafonnee_employeur

        return cotisations_exonerees * (age > 45)
        # FIXME: On est bien d'accord qu'il y a les exos uniquement pour les
        # plus de 45 ans?

# TODO: vérifier aucun avantage pour l'employé ??
