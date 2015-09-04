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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division


from numpy import datetime64, timedelta64


from ....base import *  # noqa analysis:ignore


@reference_formula
class professionnalisation(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"L'individu est en contrat de professionnalisation"
    url = "http://www.apce.com/pid879/contrat-de-professionnalisation.html?espace=1&tp=1"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age = simulation.calculate('age', period)
        ass = simulation.calculate_add('ass', period)
        rsa = simulation.calculate('rsa', period)
        aah = simulation.calculate('aah', period)

        age_condition = (16 <= age) * (age < 25)
        dummy_ass = ass > 0
        dummy_rmi = rsa > 0
        dummy_aah = aah > 0

        return period, (age_condition + dummy_ass + dummy_aah + dummy_rmi) > 0


@reference_formula
class remuneration_professionnalisation(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
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
        period = period.start.offset('first-of', 'month').period('month')
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


@reference_formula
class exoneration_cotisations_employeur_apprenti(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
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
        period = period.start.offset('first-of', 'month').period('month')
        age = simulation.calculate('age', period)
        mmid_employeur = simulation.calculate('mmid_employeur', period)
        famille = simulation.calculate('famille', period)
        vieillesse_plafonnee_employeur = simulation.calculate('vieillesse_plafonnee_employeur', period)  # correspond à
        # vieillesse de base?
        cotisations_exonerees = mmid_employeur + famille + vieillesse_plafonnee_employeur

        return period, cotisations_exonerees * (age > 45)  # On est bien d'accord qu'il y a les exos uniquement pour les
        # plus de 45 ans?

# O est d'accord aucun avantage pour l'employé ??
#  @reference_formula
#  class exoneration_cotisations_salariales_apprenti(SimpleFormulaColumn):
#    column = FloatCol
#    entity_class = Individus
#    label = u"Exonération de cotisations salariales pour l'emploi d'un apprenti"
#    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
#
#    def function(self, simulation, period):
#        cotisations_salariales = simulation.calculate('cotisations_salariales', period)
#        return period, - cotisations_salariales
