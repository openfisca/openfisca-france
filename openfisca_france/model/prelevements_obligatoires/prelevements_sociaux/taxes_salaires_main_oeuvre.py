# -*- coding: utf-8 -*-

from __future__ import division

import logging

import numpy as np

from openfisca_france.model.base import *

# TODO:
# check hsup everywhere !

# Helpers

from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme

log = logging.getLogger(__name__)

taux_aot_by_depcom = None
taux_smt_by_depcom = None


# Cotisations proprement dites


class conge_individuel_formation_cdd(Variable):
    value_type = float
    entity = Individu
    label = u"Contribution au financement des congé individuel de formation (CIF) des salariées en CDD"
    definition_period = MONTH

    # TODO: date de début
    def formula(individu, period, parameters):
        contrat_de_travail_duree = individu('contrat_de_travail_duree', period)
        TypesContratDeTravailDuree = contrat_de_travail_duree.possible_values
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)

        law = parameters(period).cotsoc.conge_individuel_formation
        cotisation = - law.cdd * (contrat_de_travail_duree == TypesContratDeTravailDuree.cdd) * assiette_cotisations_sociales
        return cotisation


class redevable_taxe_apprentissage(Variable):
    value_type = bool
    entity = Individu
    label = u"Entreprise redevable de la taxe d'apprentissage"
    definition_period = MONTH

    def formula(individu, period, parameters):
        # L'association a but non lucratif ne paie pas d'IS de droit commun article 206 du Code général des impôts
        # -> pas de taxe d'apprentissage
        association = individu('entreprise_est_association_non_lucrative', period)

        return not_(association)


class contribution_developpement_apprentissage(Variable):
    value_type = float
    entity = Individu
    label = u"Contribution additionnelle au développement de l'apprentissage"
    definition_period = MONTH

    def formula(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = "employeur",
            bareme_name = "apprentissage_add",
            variable_name = "contribution_developpement_apprentissage",
            )
        return cotisation * redevable_taxe_apprentissage


class contribution_supplementaire_apprentissage(Variable):
    value_type = float
    entity = Individu
    label = u"Contribution supplémentaire à l'apprentissage"
    reference = u"https://www.service-public.fr/professionnels-entreprises/vosdroits/F22574"
    definition_period = MONTH

    def formula_2010_01_01(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        ratio_alternants = individu('ratio_alternants', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)

        cotsoc_params = parameters(period).cotsoc
        csa_params = cotsoc_params.contribution_supplementaire_apprentissage

        if period.start.year > 2012:
            # Exception Alsace-Moselle : CGI Article 1609 quinvicies IV
            # https://www.legifrance.gouv.fr/affichCode.do;jsessionid=36F88516571C1CA136D91A7A84A2D65B.tpdila09v_1?idSectionTA=LEGISCTA000029038088&cidTexte=LEGITEXT000006069577&dateTexte=20161219
            multiplier = (salarie_regime_alsace_moselle * csa_params.multiplicateur_alsace_moselle) + (1 - salarie_regime_alsace_moselle)

            taxe_due = (effectif_entreprise >= 250) * (ratio_alternants < .05)
            taux_conditionnel = (
                (effectif_entreprise < 2000) * (ratio_alternants < .01) * csa_params.moins_2000_moins_1pc_alternants
                + (effectif_entreprise >= 2000) * (ratio_alternants < .01) * csa_params.plus_2000_moins_1pc_alternants
                + (.01 <= ratio_alternants) * (ratio_alternants < .02) * csa_params.entre_1_2_pc_alternants
                + (.02 <= ratio_alternants) * (ratio_alternants < .03) * csa_params.entre_2_3_pc_alternants
                + (.03 <= ratio_alternants) * (ratio_alternants < .04) * csa_params.entre_3_4_pc_alternants
                + (.04 <= ratio_alternants) * (ratio_alternants < .05) * csa_params.entre_4_5_pc_alternants
                )
            taux_contribution = taxe_due * taux_conditionnel * multiplier
        else:
            taux_contribution = (effectif_entreprise >= 250) * cotsoc_params.contribution_supplementaire_apprentissage.plus_de_250
            # TODO: gestion de la place dans le XML pb avec l'arbre des paramètres / preprocessing
        return - taux_contribution * assiette_cotisations_sociales * redevable_taxe_apprentissage


class cotisations_employeur_main_d_oeuvre(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisation sociales employeur main d'oeuvre"
    definition_period = MONTH

    def formula(individu, period, parameters):
        conge_individuel_formation_cdd = individu('conge_individuel_formation_cdd', period)
        contribution_developpement_apprentissage = individu(
            'contribution_developpement_apprentissage', period)
        contribution_supplementaire_apprentissage = individu(
            'contribution_supplementaire_apprentissage', period)
        financement_organisations_syndicales = individu('financement_organisations_syndicales', period)
        fnal = individu('fnal', period)
        formation_professionnelle = individu('formation_professionnelle', period)
        participation_effort_construction = individu('participation_effort_construction', period, options = [ADD])
        prevoyance_obligatoire_cadre = individu('prevoyance_obligatoire_cadre', period, options = [ADD])
        complementaire_sante_employeur = individu('complementaire_sante_employeur', period, options = [ADD])

        taxe_apprentissage = individu('taxe_apprentissage', period, options = [ADD])
        versement_transport = individu('versement_transport', period, options = [ADD])

        cotisations_employeur_main_d_oeuvre = (
            conge_individuel_formation_cdd
            + contribution_developpement_apprentissage
            + contribution_supplementaire_apprentissage
            + financement_organisations_syndicales
            + fnal
            + formation_professionnelle
            + participation_effort_construction
            + prevoyance_obligatoire_cadre
            + complementaire_sante_employeur
            + taxe_apprentissage
            + versement_transport
            )

        return cotisations_employeur_main_d_oeuvre


class fnal(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisation fonds national action logement (FNAL)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        fnal_tranche_a = individu('fnal_tranche_a', period)
        fnal_tranche_a_plus_20 = individu('fnal_tranche_a_plus_20', period)
        return fnal_tranche_a + fnal_tranche_a_plus_20


class fnal_tranche_a(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisation fonds national action logement (FNAL tout employeur)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        taille_entreprise = individu('taille_entreprise', period)
        TypesTailleEntreprise = taille_entreprise.possible_values

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal1',
            variable_name = "fnal_tranche_a",
            )
        entreprise_eligible = (
            (taille_entreprise == TypesTailleEntreprise.non_pertinent)
            + (taille_entreprise == TypesTailleEntreprise.moins_de_10)
            + (taille_entreprise == TypesTailleEntreprise.de_10_a_19)
            )
        return cotisation * entreprise_eligible


class fnal_tranche_a_plus_20(Variable):
    value_type = float
    entity = Individu
    label = u"Fonds national action logement (FNAL, employeur avec plus de 20 salariés)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        taille_entreprise = individu('taille_entreprise', period)
        TypesTailleEntreprise = taille_entreprise.possible_values

        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'fnal2',
            variable_name = 'fnal_tranche_a_plus_20',
            )
        entreprise_eligible = (
            (taille_entreprise == TypesTailleEntreprise.de_20_a_249)
            + (taille_entreprise == TypesTailleEntreprise.plus_de_250)
            )
        return cotisation * entreprise_eligible


class financement_organisations_syndicales(Variable):
    value_type = float
    entity = Individu
    label = u"Contribution patronale au financement des organisations syndicales"
    definition_period = MONTH

    def formula_2015_01_01(individu, period, parameters):
        categorie_salarie = individu('categorie_salarie', period)
        cotisation = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'financement_organisations_syndicales',
            variable_name = 'financement_organisations_syndicales',
            )
        contrat_de_droit_prive = (
            + (categorie_salarie == TypesCategorieSalarie.prive_non_cadre)
            + (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            )

        return cotisation * contrat_de_droit_prive


class formation_professionnelle(Variable):
    value_type = float
    entity = Individu
    label = u"Formation professionnelle"
    reference = u"https://www.service-public.fr/professionnels-entreprises/vosdroits/F22570"
    definition_period = MONTH

    def formula(individu, period, parameters):
        taille_entreprise = individu('taille_entreprise', period)
        TypesTailleEntreprise = taille_entreprise.possible_values

        cotisation_0_9 = (taille_entreprise == TypesTailleEntreprise.moins_de_10) * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_09',
            variable_name = 'formation_professionnelle',
            )

        cotisation_10_19 = (taille_entreprise == TypesTailleEntreprise.de_10_a_19) * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_1019',
            variable_name = 'formation_professionnelle',
            )

        entreprise_eligible = (
            (taille_entreprise == TypesTailleEntreprise.de_20_a_249)
            + (taille_entreprise == TypesTailleEntreprise.plus_de_250)
            )
        cotisation_20 = entreprise_eligible * apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_20',
            variable_name = 'formation_professionnelle',
            )
        return cotisation_0_9 + cotisation_10_19 + cotisation_20


class participation_effort_construction(Variable):
    value_type = float
    entity = Individu
    label = u"Participation à l'effort de construction"
    definition_period = MONTH

    def formula(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)

        bareme = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'construction',
            variable_name = 'participation_effort_construction',
            )

        seuil = parameters(period).cotsoc.pat.commun.construction_node.seuil
        cotisation = bareme * (effectif_entreprise >= seuil)

        return cotisation


class taxe_apprentissage(Variable):
    value_type = float
    entity = Individu
    label = u"Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"
    reference = u"https://www.service-public.fr/professionnels-entreprises/vosdroits/F22574"
    definition_period = MONTH

    def formula(individu, period, parameters):
        redevable_taxe_apprentissage = individu('redevable_taxe_apprentissage', period)
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)

        cotisation_regime_alsace_moselle = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage_alsace_moselle',
            variable_name = 'taxe_apprentissage',
            )

        cotisation_regime_general = apply_bareme(
            individu,
            period,
            parameters,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage',
            variable_name = 'taxe_apprentissage',
            )

        cotisation = np.where(
            salarie_regime_alsace_moselle,
            cotisation_regime_alsace_moselle,
            cotisation_regime_general,
            )

        return cotisation * redevable_taxe_apprentissage


class taxe_salaires(Variable):
    value_type = float
    entity = Individu
    label = u"Taxe sur les salaires"
    definition_period = MONTH
# Voir
# http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8920/fichedescriptiveformulaire_8920.pdf

    def formula(individu, period, parameters):
        assujettie_taxe_salaires = individu('assujettie_taxe_salaires', period)
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        prevoyance_obligatoire_cadre = individu('prevoyance_obligatoire_cadre', period)
        complementaire_sante_employeur = individu('complementaire_sante_employeur', period)
        prise_en_charge_employeur_prevoyance_complementaire = individu(
            'prise_en_charge_employeur_prevoyance_complementaire', period, options = [ADD])

        entreprise_est_association_non_lucrative = individu('entreprise_est_association_non_lucrative', period)
        effectif_entreprise = individu('effectif_entreprise', period)

        # impots.gouv.fr
        # La taxe est due notamment par les : [...] organismes sans but lucratif
        assujettissement = assujettie_taxe_salaires + entreprise_est_association_non_lucrative

        parametres = parameters(period).cotsoc.taxes_sal
        bareme = parametres.taux_maj
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
                )
            + round_(parametres.taux.metro * base, 2)
            )

        # Une franchise et une décôte s'appliquent à cette taxe
        # Etant donné que nous n'avons pas la distribution de salaires de l'entreprise,
        # elles sont estimées en prenant l'effectif de l'entreprise et
        # considérant que l'unique salarié de la individu est la moyenne.
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
                True: individu.filled_array(0),
                False: estimation_abattue / effectif_entreprise / 12
                })

        return - cotisation * assujettissement
