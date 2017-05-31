# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import logical_or as or_, logical_and as and_

import numpy as np

import openfisca_france
from openfisca_france.model.base import *  # noqa analysis:ignore

log = logging.getLogger(__name__)

taux_aot_by_depcom = None
taux_smt_by_depcom = None


# TODO:
# check hsup everywhere !

# Helpers

from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme

# Cotisations proprement dites


class conge_individuel_formation_cdd(Variable):
    column = FloatCol
    entity = Individu
    label = u"Contribution au financement des congé individuel de formation (CIF) des salariées en CDD"
    definition_period = MONTH

    # TODO: date de début
    def formula(self, simulation, period):
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        law = simulation.legislation_at(period.start).cotsoc.conge_individuel_formation

        cotisation = - law.cdd * (contrat_de_travail_duree == 1) * assiette_cotisations_sociales
        return cotisation


class redevable_taxe_apprentissage(Variable):
    column = BoolCol
    entity = Individu
    label = u"Entreprise redevable de la taxe d'apprentissage"
    definition_period = MONTH

    def formula(self, simulation, period):
        # L'association a but non lucratif ne paie pas d'IS de droit commun article 206 du Code général des impôts
        # -> pas de taxe d'apprentissage
        association = simulation.calculate('entreprise_est_association_non_lucrative', period)

        return not_(association)


class contribution_developpement_apprentissage(Variable):
    column = FloatCol
    entity = Individu
    label = u"Contribution additionnelle au développement de l'apprentissage"
    definition_period = MONTH

    def formula(self, simulation, period):
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)

        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "apprentissage_add",
            variable_name = self.__class__.__name__,
            )
        return cotisation * redevable_taxe_apprentissage


class contribution_supplementaire_apprentissage(Variable):
    column = FloatCol
    entity = Individu
    label = u"Contribution supplémentaire à l'apprentissage"
    url = u"https://www.service-public.fr/professionnels-entreprises/vosdroits/F22574"
    definition_period = MONTH

    def formula_2010_01_01(self, simulation, period):
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        ratio_alternants = simulation.calculate('ratio_alternants', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        salarie_regime_alsace_moselle = simulation.calculate('salarie_regime_alsace_moselle', period)

        cotsoc_params = simulation.legislation_at(period.start).cotsoc
        csa_params = cotsoc_params.contribution_supplementaire_apprentissage

        if period.start.year > 2012:
            # Exception Alsace-Moselle : CGI Article 1609 quinvicies IV
            # https://www.legifrance.gouv.fr/affichCode.do;jsessionid=36F88516571C1CA136D91A7A84A2D65B.tpdila09v_1?idSectionTA=LEGISCTA000029038088&cidTexte=LEGITEXT000006069577&dateTexte=20161219
            multiplier = (salarie_regime_alsace_moselle * csa_params.multiplicateur_alsace_moselle) + (1 - salarie_regime_alsace_moselle)

            taxe_due = (effectif_entreprise >= 250) * (ratio_alternants < .05)
            taux_conditionnel = (
                (effectif_entreprise < 2000) * (ratio_alternants < .01) * csa_params.moins_2000_moins_1pc_alternants +
                (effectif_entreprise >= 2000) * (ratio_alternants < .01) * csa_params.plus_2000_moins_1pc_alternants +
                (.01 <= ratio_alternants) * (ratio_alternants < .02) * csa_params.entre_1_2_pc_alternants +
                (.02 <= ratio_alternants) * (ratio_alternants < .03) * csa_params.entre_2_3_pc_alternants +
                (.03 <= ratio_alternants) * (ratio_alternants < .04) * csa_params.entre_3_4_pc_alternants +
                (.04 <= ratio_alternants) * (ratio_alternants < .05) * csa_params.entre_4_5_pc_alternants
                )
            taux_contribution = taxe_due * taux_conditionnel * multiplier
        else:
            taux_contribution = (effectif_entreprise >= 250) * cotsoc_params.contribution_supplementaire_apprentissage.plus_de_250
            # TODO: gestion de la place dans le XML pb avec l'arbre des paramètres / preprocessing
        return - taux_contribution * assiette_cotisations_sociales * redevable_taxe_apprentissage


class cotisations_employeur_main_d_oeuvre(Variable):
    base_function = requested_period_added_value
    column = FloatCol
    entity = Individu
    label = u"Cotisation sociales employeur main d'oeuvre"
    definition_period = MONTH

    def formula(self, simulation, period):
        conge_individuel_formation_cdd = simulation.calculate('conge_individuel_formation_cdd', period)
        contribution_developpement_apprentissage = simulation.calculate(
            'contribution_developpement_apprentissage', period)
        contribution_supplementaire_apprentissage = simulation.calculate(
            'contribution_supplementaire_apprentissage', period)
        financement_organisations_syndicales = simulation.calculate('financement_organisations_syndicales', period)
        fnal = simulation.calculate('fnal', period)
        formation_professionnelle = simulation.calculate('formation_professionnelle', period)
        participation_effort_construction = simulation.calculate_add('participation_effort_construction', period)
        prevoyance_obligatoire_cadre = simulation.calculate_add('prevoyance_obligatoire_cadre', period)
        complementaire_sante_employeur = simulation.calculate_add('complementaire_sante_employeur', period)

        taxe_apprentissage = simulation.calculate_add('taxe_apprentissage', period)
        versement_transport = simulation.calculate_add('versement_transport', period)

        cotisations_employeur_main_d_oeuvre = (
            conge_individuel_formation_cdd +
            contribution_developpement_apprentissage +
            contribution_supplementaire_apprentissage +
            financement_organisations_syndicales +
            fnal +
            formation_professionnelle +
            participation_effort_construction +
            prevoyance_obligatoire_cadre +
            complementaire_sante_employeur +
            taxe_apprentissage +
            versement_transport
            )
        return cotisations_employeur_main_d_oeuvre


class fnal(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation fonds national action logement (FNAL)"
    definition_period = MONTH

    def formula(self, simulation, period):
        fnal_tranche_a = simulation.calculate('fnal_tranche_a', period)
        fnal_tranche_a_plus_20 = simulation.calculate('fnal_tranche_a_plus_20', period)
        return fnal_tranche_a + fnal_tranche_a_plus_20


class fnal_tranche_a(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation fonds national action logement (FNAL tout employeur)"
    definition_period = MONTH

    def formula(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'fnal1',
            variable_name = self.__class__.__name__,
            )
        return cotisation * (taille_entreprise <= 2)


class fnal_tranche_a_plus_20(Variable):
    column = FloatCol
    entity = Individu
    label = u"Fonds national action logement (FNAL, employeur avec plus de 20 salariés)"
    definition_period = MONTH

    def formula(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'fnal2',
            variable_name = self.__class__.__name__,
            )
        return cotisation * (taille_entreprise > 2)


class financement_organisations_syndicales(Variable):
    column = FloatCol
    entity = Individu
    label = u"Contribution patronale au financement des organisations syndicales"
    definition_period = MONTH

    def formula_2015_01_01(self, simulation, period):
        categorie_salarie = simulation.calculate('categorie_salarie', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'financement_organisations_syndicales',
            variable_name = self.__class__.__name__,
            )
        return cotisation * or_(categorie_salarie <= 1, categorie_salarie == 6)


class formation_professionnelle(Variable):
    column = FloatCol
    entity = Individu
    label = u"Formation professionnelle"
    url = u"https://www.service-public.fr/professionnels-entreprises/vosdroits/F22570"
    definition_period = MONTH

    def formula(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation_0_9 = (taille_entreprise == 1) * apply_bareme(
            simulation,
            period, cotisation_type = 'employeur',
            bareme_name = 'formprof_09',
            variable_name = self.__class__.__name__,
            )
        cotisation_10_19 = (taille_entreprise == 2) * apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_1019',
            variable_name = self.__class__.__name__,
            )
        cotisation_20 = (taille_entreprise > 2) * apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_20',
            variable_name = self.__class__.__name__,
            )
        return cotisation_0_9 + cotisation_10_19 + cotisation_20


class participation_effort_construction(Variable):
    column = FloatCol
    entity = Individu
    label = u"Participation à l'effort de construction"
    definition_period = MONTH

    def formula(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)

        bareme = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'construction',
            variable_name = self.__class__.__name__,
            )

        # TODO : seuil passé de 10 à 20 avec l'Ordonnance n° 2005-895 du 2 août 2005

        cotisation = (
            bareme * (effectif_entreprise >= 20) +
            self.zeros() * (effectif_entreprise < 20)
            )

        return cotisation


class taxe_apprentissage(Variable):
    column = FloatCol
    entity = Individu
    label = u"Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"
    url = u"https://www.service-public.fr/professionnels-entreprises/vosdroits/F22574"
    definition_period = MONTH

    def formula(self, simulation, period):
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        salarie_regime_alsace_moselle = simulation.calculate('salarie_regime_alsace_moselle', period)

        cotisation_regime_alsace_moselle = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage_alsace_moselle',
            variable_name = self.__class__.__name__,
            )

        cotisation_regime_general = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage',
            variable_name = self.__class__.__name__,
            )

        cotisation = np.where(
            salarie_regime_alsace_moselle,
            cotisation_regime_alsace_moselle,
            cotisation_regime_general,
        )

        # cotisation = salarie_regime_alsace_moselle * cotisation_regime_alsace_moselle + (1 - salarie_regime_alsace_moselle) * cotisation_regime_general

        return cotisation * redevable_taxe_apprentissage


class taxe_salaires(Variable):
    column = FloatCol
    entity = Individu
    label = u"Taxe sur les salaires"
    definition_period = MONTH
# Voir
# http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8920/fichedescriptiveformulaire_8920.pdf

    def formula(self, simulation, period):
        assujettie_taxe_salaires = simulation.calculate('assujettie_taxe_salaires', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        complementaire_sante_employeur = simulation.calculate('complementaire_sante_employeur', period)
        prise_en_charge_employeur_prevoyance_complementaire = simulation.calculate_add(
            'prise_en_charge_employeur_prevoyance_complementaire', period)

        law = simulation.legislation_at(period.start)
        entreprise_est_association_non_lucrative = \
            simulation.calculate('entreprise_est_association_non_lucrative', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)

        # impots.gouv.fr
        # La taxe est due notamment par les : [...] organismes sans but lucratif
        assujettissement = assujettie_taxe_salaires + entreprise_est_association_non_lucrative

        parametres = law.cotsoc.taxes_sal
        bareme = parametres.taux_maj
        base = assiette_cotisations_sociales - prevoyance_obligatoire_cadre
        base = assiette_cotisations_sociales + (
                - prevoyance_obligatoire_cadre + prise_en_charge_employeur_prevoyance_complementaire
                - complementaire_sante_employeur
                )

        # TODO: exonérations apprentis
        # TODO: modify if DOM

        cotisation_individuelle = (
            bareme.calc(
                base,
                factor = 1 / 12,
                round_base_decimals = 2
                ) +
            round_(parametres.taux.metro * base, 2)
            )

        # Une franchise et une décôte s'appliquent à cette taxe
        # Etant donné que nous n'avons pas la distribution de salaires de l'entreprise,
        # elles sont estimées en prenant l'effectif de l'entreprise et
        # considérant que l'unique salarié de la simulation est la moyenne.
        # http://www.impots.gouv.fr/portal/dgi/public/popup?typePage=cpr02&espId=2&docOid=documentstandard_1845
        estimation = cotisation_individuelle * effectif_entreprise * 12
        conditions = [estimation < parametres.franchise, estimation <= parametres.decote_montant, estimation > parametres.decote_montant]
        results = [0, estimation - (parametres.decote_montant - estimation) * parametres.decote_taux, estimation]

        estimation_reduite = np.select(conditions, results)

        # Abattement spécial de taxe sur les salaires
        # Les associations à but non lucratif bénéficient d'un abattement important
        estimation_abattue_negative = estimation_reduite - parametres.abattement_special
        estimation_abattue = switch(
            entreprise_est_association_non_lucrative,
            {
                0: estimation_reduite,
                1: (estimation_abattue_negative >= 0) * estimation_abattue_negative,
                }
            )

        with np.errstate(invalid='ignore'):
            cotisation = switch(effectif_entreprise == 0, {
                True: self.zeros(),
                False: estimation_abattue / effectif_entreprise / 12
                })

        return - cotisation * assujettissement
