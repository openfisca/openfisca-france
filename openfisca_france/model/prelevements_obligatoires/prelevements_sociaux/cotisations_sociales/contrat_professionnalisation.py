# -*- coding: utf-8 -*-

from __future__ import division


from numpy import datetime64, timedelta64


from openfisca_france.model.base import *  # noqa analysis:ignore


class professionnalisation(Variable):
    column = BoolCol
    entity = Individu
    label = u"L'individu est en contrat de professionnalisation"
    url = "http://www.apce.com/pid879/contrat-de-professionnalisation.html?espace=1&tp=1"

    def function(self, simulation, period):
        period = period.this_month
        age = simulation.calculate('age', period)
        ass = simulation.calculate_add('ass', period)
        rsa = simulation.calculate('rsa', period)
        aah = simulation.calculate('aah', period)

        age_condition = (16 <= age) * (age < 25)
        dummy_ass = ass > 0
        dummy_rmi = rsa > 0
        dummy_aah = aah > 0

        return period, (age_condition + dummy_ass + dummy_aah + dummy_rmi) > 0


class remuneration_professionnalisation(Variable):
    column = FloatCol
    entity = Individu
    label = u"Rémunération de l'apprenti"
    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"

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

    def function(self, simulation, period):
        period = period.this_month
        age = simulation.calculate('age', period)
        smic = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b * 52 * 35 / 12
        professionnalisation = simulation.calculate('professionnalisation', period)
        qualifie = simulation.calculate('qualifie')
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
                for qualification, part_de_smic in age_interval['part_de_smic_by_qualification'].iteritems()
                ])
        return period, taux_smic * smic * professionnalisation


class exoneration_cotisations_employeur_professionnalisation(Variable):
    column = FloatCol
    entity = Individu
    label = u"Exonération de cotisations patronales pour l'emploi d'un apprenti"
    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"

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

    def function(self, simulation, period):
        period = period.this_month
        age = simulation.calculate('age', period)
        mmid_employeur = simulation.calculate('mmid_employeur', period)
        famille = simulation.calculate('famille', period)
        vieillesse_plafonnee_employeur = simulation.calculate('vieillesse_plafonnee_employeur', period)
        # FIXME: correspond bien à vieillesse de base ?
        cotisations_exonerees = mmid_employeur + famille + vieillesse_plafonnee_employeur

        return period, cotisations_exonerees * (age > 45)
        # FIXME: On est bien d'accord qu'il y a les exos uniquement pour les
        # plus de 45 ans?

# TODO: vérifier aucun avantage pour l'employé ??
