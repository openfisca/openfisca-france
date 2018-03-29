# -*- coding: utf-8 -*-

from __future__ import division

from numpy import floor

from openfisca_france.model.base import *  # noqa analysis:ignore


class unites_consommation(Variable):
    value_type = float
    entity = Menage
    label = u"Unités de consommation du ménage, selon l'échelle de l'INSEE"
    reference = u"https://insee.fr/fr/metadonnees/definition/c1802"
    definition_period = YEAR

    def formula(menage, period, parameters):
        age_individu = menage.members('age', period.first_month)
        uc_individu = 0.5 * (age_individu >= 14) + 0.3 * (age_individu < 14)
        return 0.5 + menage.sum(uc_individu)  # 1 uc pour la personne de référence


class type_menage(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Menage
    label = u"Type de ménage"
    definition_period = YEAR

    def formula(menage, period):
        '''
        Type de menage
        TODO: prendre les enfants du ménage et non ceux de la famille
        Attention : des erreurs peuvent subsister quand ménage et famille ne coincide pas (cas des ménages complexes)
        '''

        af_nbenf = menage.personne_de_reference.famille('af_nbenf', period.first_month)
        isole = not_(menage.personne_de_reference.famille('en_couple', period.first_month))

        return (
            0 * (isole * (af_nbenf == 0)) +  # Célibataire
            1 * (not_(isole) * (af_nbenf == 0)) +  # Couple sans enfants
            2 * (not_(isole) * (af_nbenf == 1)) +  # Couple un enfant
            3 * (not_(isole) * (af_nbenf == 2)) +  # Couple deux enfants
            4 * (not_(isole) * (af_nbenf == 3)) +  # Couple trois enfants et plus
            5 * (isole * (af_nbenf == 1)) +  # Famille monoparentale un enfant
            6 * (isole * (af_nbenf == 2)) +  # Famille monoparentale deux enfants
            7 * (isole * (af_nbenf == 3))
            )  # Famille monoparentale trois enfants et plus


class revenu_disponible(Variable):
    value_type = float
    entity = Menage
    label = u"Revenu disponible du ménage"
    reference = "http://fr.wikipedia.org/wiki/Revenu_disponible"
    definition_period = YEAR

    def formula(menage, period, parameters):
        pensions_i = menage.members('pensions', period)
        revenus_du_capital_i = menage.members('revenus_du_capital', period)
        revenus_du_travail_i = menage.members('revenus_du_travail', period)
        pensions = menage.sum(pensions_i)
        revenus_du_capital = menage.sum(revenus_du_capital_i)
        revenus_du_travail = menage.sum(revenus_du_travail_i)

        impots_directs = menage('impots_directs', period)

        # On prend en compte les PPE touchés par un foyer fiscal dont le déclarant principal est dans le ménage
        ppe_i = menage.members.foyer_fiscal('ppe', period)  # PPE du foyer fiscal auquel appartient chaque membre du ménage
        ppe = menage.sum(ppe_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)  # On somme seulement pour les déclarants principaux

        # On prend en compte les prestations sociales touchées par une famille dont le demandeur est dans le ménage
        prestations_sociales_i = menage.members.famille('prestations_sociales', period)  # PF de la famille auquel appartient chaque membre du ménage
        prestations_sociales = menage.sum(prestations_sociales_i, role = Famille.DEMANDEUR)  # On somme seulement pour les demandeurs

        return (
            revenus_du_travail
            + impots_directs
            + pensions
            + ppe
            + prestations_sociales
            + revenus_du_capital
            )


class niveau_de_vie(Variable):
    value_type = float
    entity = Menage
    label = u"Niveau de vie du ménage"
    definition_period = YEAR

    def formula(menage, period):
        revenu_disponible = menage('revenu_disponible', period)
        uc = menage('unites_consommation', period)
        return revenu_disponible / uc


class revenu_net_individu(Variable):
    value_type = float
    entity = Individu
    label = u"Revenu net de l'individu"
    definition_period = YEAR

    def formula(individu, period):
        pensions = individu('pensions', period)
        revenus_du_capital = individu('revenus_du_capital', period)
        revenus_du_travail = individu('revenus_du_travail', period)

        return pensions + revenus_du_capital + revenus_du_travail


class revenu_net(Variable):
    entity = Menage
    label = u"Revenu net du ménage"
    value_type = float
    reference = u"http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php",
    definition_period = YEAR

    def formula(menage, period):
        revenu_net_individus = menage.members('revenu_net_individu', period)
        return menage.sum(revenu_net_individus)


class niveau_de_vie_net(Variable):
    value_type = float
    entity = Menage
    label = u"Niveau de vie net du ménage"
    definition_period = YEAR

    def formula(menage, period):
        revenu_net = menage('revenu_net', period)
        uc = menage('unites_consommation', period)

        return revenu_net / uc


class revenu_initial_individu(Variable):
    value_type = float
    entity = Individu
    label = u"Revenu initial de l'individu"
    definition_period = YEAR

    def formula(individu, period):
        cotisations_employeur_contributives = individu('cotisations_employeur_contributives', period)
        cotisations_salariales_contributives = individu('cotisations_salariales_contributives', period)
        pensions = individu('pensions', period)
        revenus_du_capital = individu('revenus_du_capital', period)
        revenus_du_travail = individu('revenus_du_travail', period)

        return (
            revenus_du_travail
            + pensions
            + revenus_du_capital
            - cotisations_employeur_contributives
            - cotisations_salariales_contributives
            )


class revenu_initial(Variable):
    entity = Menage
    label = u"Revenu initial du ménage"
    value_type = float
    definition_period = YEAR

    def formula(menage, period):
        revenu_initial_individus = menage.members('revenu_initial_individu', period)
        return menage.sum(revenu_initial_individus)


class niveau_de_vie_initial(Variable):
    value_type = float
    entity = Menage
    label = u"Niveau de vie initial du ménage"
    definition_period = YEAR

    def formula(menage, period):
        revenu_initial = menage('revenu_initial', period)
        uc = menage('unites_consommation', period)

        return revenu_initial / uc


class revenu_primaire(Variable):
    value_type = float
    entity = Menage
    label = u"Revenu primaire du ménage (revenus superbruts avant tout prélèvement). Il est égal à la valeur ajoutée produite par les résidents."
    definition_period = YEAR

    def formula(individu, period):
        revenus_du_travail = individu('revenus_du_travail', period)
        revenus_du_capital = individu('revenus_du_capital', period)
        cotisations_employeur = individu('cotisations_employeur', period)
        cotisations_salariales = individu('cotisations_salariales', period)

        return revenus_du_travail + revenus_du_capital - cotisations_employeur - cotisations_salariales - chomage_imposable


class revenus_du_travail(Variable):
    value_type = float
    entity = Individu
    label = u"Revenus du travail (salariés et non salariés)"
    reference = "http://fr.wikipedia.org/wiki/Revenu_du_travail"
    definition_period = YEAR

    def formula(individu, period):
        salaire_net = individu('salaire_net', period, options = [ADD])
        revenus_non_salaries = individu('rpns', period, options = [ADD])  # TODO ou rpns_individu

        return salaire_net + revenus_non_salaries


class pensions(Variable):
    value_type = float
    entity = Individu
    label = u"Pensions et revenus de remplacement"
    reference = "http://fr.wikipedia.org/wiki/Rente"
    definition_period = YEAR

    def formula(individu, period):
        chomage_net = individu('chomage_net', period, options = [ADD])
        retraite_nette = individu('retraite_nette', period, options = [ADD])
        pensions_alimentaires_percues = individu('pensions_alimentaires_percues', period, options = [ADD])
        pensions_invalidite = individu('pensions_invalidite', period, options = [ADD])

        # Revenus du foyer fiscal, que l'on projette uniquement sur le 1er déclarant
        foyer_fiscal = individu.foyer_fiscal
        pensions_alimentaires_versees = foyer_fiscal('pensions_alimentaires_versees', period)
        retraite_titre_onereux = foyer_fiscal('retraite_titre_onereux', period, options = [ADD])
        pen_foyer_fiscal = pensions_alimentaires_versees + retraite_titre_onereux
        pen_foyer_fiscal_projetees = pen_foyer_fiscal * (individu.has_role(foyer_fiscal.DECLARANT_PRINCIPAL))

        return (
            chomage_net
            + retraite_nette
            + pensions_alimentaires_percues
            + pensions_invalidite
            + pen_foyer_fiscal_projetees
            )


class cotsoc_bar(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Cotisations sociales sur les revenus du capital imposés au barème"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        csg_cap_bar = foyer_fiscal('csg_cap_bar', period)
        prelsoc_cap_bar = foyer_fiscal('prelsoc_cap_bar', period)
        crds_cap_bar = foyer_fiscal('crds_cap_bar', period)

        return csg_cap_bar + prelsoc_cap_bar + crds_cap_bar


class cotsoc_lib(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        csg_cap_lib = foyer_fiscal('csg_cap_lib', period)
        prelsoc_cap_lib = foyer_fiscal('prelsoc_cap_lib', period)
        crds_cap_lib = foyer_fiscal('crds_cap_lib', period)

        return csg_cap_lib + prelsoc_cap_lib + crds_cap_lib


class revenus_du_capital(Variable):
    value_type = float
    entity = Individu
    label = u"Revenus du patrimoine"
    reference = "http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"
    definition_period = YEAR

    def formula(individu, period):

        # Revenus du foyer fiscal, que l'on projette uniquement sur le 1er déclarant
        foyer_fiscal = individu.foyer_fiscal
        fon = foyer_fiscal('fon', period)
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options = [ADD])
        cotsoc_lib = foyer_fiscal('cotsoc_lib', period)
        rev_cap_lib = foyer_fiscal('rev_cap_lib', period, options = [ADD])
        imp_lib = foyer_fiscal('imp_lib', period)
        cotsoc_bar = foyer_fiscal('cotsoc_bar', period)

        revenus_foyer_fiscal = fon + rev_cap_bar + cotsoc_lib + rev_cap_lib + imp_lib + cotsoc_bar
        revenus_foyer_fiscal_projetes = revenus_foyer_fiscal * individu.has_role(foyer_fiscal.DECLARANT_PRINCIPAL)

        rac = individu('rac', period)

        return revenus_foyer_fiscal_projetes + rac


class prestations_sociales(Variable):
    value_type = float
    entity = Famille
    label = u"Prestations sociales"
    reference = "http://fr.wikipedia.org/wiki/Prestation_sociale"
    definition_period = YEAR

    def formula(famille, period):
        '''
        Prestations sociales
        '''
        prestations_familiales = famille('prestations_familiales', period)
        minima_sociaux = famille('minima_sociaux', period)
        aides_logement = famille('aides_logement', period)

        return prestations_familiales + minima_sociaux + aides_logement


class prestations_familiales(Variable):
    value_type = float
    entity = Famille
    label = u"Prestations familiales"
    reference = "http://www.social-sante.gouv.fr/informations-pratiques,89/fiches-pratiques,91/prestations-familiales,1885/les-prestations-familiales,12626.html"
    definition_period = YEAR

    def formula(famille, period):
        af = famille('af', period, options = [ADD])
        cf = famille('cf', period, options = [ADD])
        ars = famille('ars', period)
        aeeh = famille('aeeh', period, options = [ADD])
        paje = famille('paje', period, options = [ADD])
        asf = famille('asf', period, options = [ADD])
        crds_pfam = famille('crds_pfam', period)

        return af + cf + ars + aeeh + paje + asf + crds_pfam


class minimum_vieillesse(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Minimum vieillesse (ASI + ASPA)"
    definition_period = YEAR

    def formula(famille, period):
        return famille('asi', period, options = [ADD]) + famille('aspa', period, options = [ADD])


class minima_sociaux(Variable):
    value_type = float
    entity = Famille
    label = u"Minima sociaux"
    reference = "http://fr.wikipedia.org/wiki/Minima_sociaux"
    definition_period = YEAR

    def formula(famille, period, parameters):
        aah_i = famille.members('aah', period, options = [ADD])
        caah_i = famille.members('caah', period, options = [ADD])
        aah = famille.sum(aah_i)
        caah = famille.sum(caah_i)
        aefa = famille('aefa', period)
        api = famille('api', period, options = [ADD])
        ass = famille('ass', period, options = [ADD])
        minimum_vieillesse = famille('minimum_vieillesse', period, options = [ADD])
        # Certaines réformes ayant des effets de bords nécessitent que le rsa soit calculé avant la ppa
        rsa = famille('rsa', period, options = [ADD])
        ppa = famille('ppa', period, options = [ADD])
        psa = famille('psa', period, options = [ADD])

        return aah + caah + minimum_vieillesse + rsa + aefa + api + ass + psa + ppa


class aides_logement(Variable):
    value_type = float
    entity = Famille
    label = u"Aides logement nets"
    reference = "http://vosdroits.service-public.fr/particuliers/N20360.xhtml"
    definition_period = YEAR

    def formula(famille, period):
        apl = famille('apl', period, options = [ADD])
        als = famille('als', period, options = [ADD])
        alf = famille('alf', period, options = [ADD])
        crds_logement = famille('crds_logement', period, options = [ADD])

        return apl + als + alf + crds_logement


class impots_directs(Variable):
    value_type = float
    entity = Menage
    label = u"Impôts directs"
    reference = "http://fr.wikipedia.org/wiki/Imp%C3%B4t_direct"
    definition_period = YEAR

    def formula(menage, period, parameters):
        taxe_habitation = menage('taxe_habitation', period)

        # On projette comme pour PPE dans revenu_disponible
        irpp_i = menage.members.foyer_fiscal('irpp', period)
        irpp = menage.sum(irpp_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)

        return irpp + taxe_habitation


class crds(Variable):
    value_type = float
    entity = Individu
    label = u"Contributions au remboursement de la dette sociale"
    definition_period = YEAR

    def formula(individu, period):
        # CRDS sur revenus individuels
        crds_salaire = individu('crds_salaire', period, options = [ADD])
        crds_retraite = individu('crds_retraite', period, options = [ADD])
        crds_chomage = individu('crds_chomage', period, options = [ADD])
        crds_individu = crds_salaire + crds_retraite + crds_chomage
        # CRDS sur revenus de la famille, projetés seulement sur la première personne
        crds_pfam = individu.famille('crds_pfam', period)
        crds_logement = individu.famille('crds_logement', period, options = [ADD])
        crds_mini = individu.famille('crds_mini', period, options = [ADD])
        crds_famille = crds_pfam + crds_logement + crds_mini
        crds_famille_projetes = crds_famille * individu.has_role(Famille.DEMANDEUR)
        # CRDS sur revenus du foyer fiscal, projetés seulement sur la première personne
        crds_fon = individu.foyer_fiscal('crds_fon', period)
        crds_pv_mo = individu.foyer_fiscal('crds_pv_mo', period)
        crds_pv_immo = individu.foyer_fiscal('crds_pv_immo', period)
        crds_cap_bar = individu.foyer_fiscal('crds_cap_bar', period)
        crds_cap_lib = individu.foyer_fiscal('crds_cap_lib', period)
        crds_foyer_fiscal = crds_fon + crds_pv_mo + crds_pv_immo + crds_cap_bar + crds_cap_lib
        crds_foyer_fiscal_projetee = crds_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        return crds_individu + crds_famille_projetes + crds_foyer_fiscal_projetee


class csg(Variable):
    value_type = float
    entity = Individu
    label = u"Contribution sociale généralisée"
    definition_period = YEAR

    def formula(individu, period):
        csg_imposable_salaire = individu('csg_imposable_salaire', period, options = [ADD])
        csg_deductible_salaire = individu('csg_deductible_salaire', period, options = [ADD])
        csg_imposable_chomage = individu('csg_imposable_chomage', period, options = [ADD])
        csg_deductible_chomage = individu('csg_deductible_chomage', period, options = [ADD])
        csg_imposable_retraite = individu('csg_imposable_retraite', period, options = [ADD])
        csg_deductible_retraite = individu('csg_deductible_retraite', period, options = [ADD])
        # CSG prélevée sur les revenus du foyer fiscal, projetés seulement sur la première personne
        csg_fon = individu.foyer_fiscal('csg_fon', period)
        csg_cap_lib = individu.foyer_fiscal('csg_cap_lib', period)
        csg_cap_bar = individu.foyer_fiscal('csg_cap_bar', period)
        csg_pv_mo = individu.foyer_fiscal('csg_pv_mo', period)
        csg_pv_immo = individu.foyer_fiscal('csg_pv_immo', period)
        csg_foyer_fiscal = csg_fon + csg_cap_lib + csg_cap_bar + csg_pv_mo + csg_pv_immo
        csg_foyer_fiscal_projetee = csg_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return (
            csg_imposable_salaire
            + csg_deductible_salaire
            + csg_imposable_chomage
            + csg_deductible_chomage
            + csg_imposable_retraite
            + csg_deductible_retraite
            + csg_foyer_fiscal_projetee
            )


class cotisations_non_contributives(Variable):
    value_type = float
    entity = Individu
    label = u"Cotisations sociales non contributives"
    definition_period = YEAR

    def formula(individu, period):
        cotisations_employeur_non_contributives = individu('cotisations_employeur_non_contributives',
            period, options = [ADD])
        cotisations_salariales_non_contributives = individu('cotisations_salariales_non_contributives',
            period, options = [ADD])

        return cotisations_employeur_non_contributives + cotisations_salariales_non_contributives


class prelsoc_cap(Variable):
    value_type = float
    entity = Individu
    label = u"Prélèvements sociaux sur les revenus du capital"
    reference = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"
    definition_period = YEAR

    def formula(individu, period):
        # Prélevements effectués sur les revenus du foyer fiscal
        prelsoc_fon = individu.foyer_fiscal('prelsoc_fon', period)
        prelsoc_cap_lib = individu.foyer_fiscal('prelsoc_cap_lib', period)
        prelsoc_cap_bar = individu.foyer_fiscal('prelsoc_cap_bar', period)
        prelsoc_pv_mo = individu.foyer_fiscal('prelsoc_pv_mo', period)
        prelsoc_pv_immo = individu.foyer_fiscal('prelsoc_pv_immo', period)
        prel_foyer_fiscal = prelsoc_fon + prelsoc_cap_lib + prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_pv_immo

        return prel_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)


class check_csk(Variable):
    value_type = float
    entity = Menage
    label = u"check_csk"
    definition_period = YEAR

    def formula(menage, period):

        # Prélevements effectués sur les revenus des foyers fiscaux, projetés sur les déclarants principaux
        prelsoc_cap_bar = menage.members.foyer_fiscal('prelsoc_cap_bar', period)
        prelsoc_pv_mo = menage.members.foyer_fiscal('prelsoc_pv_mo', period)
        prelsoc_fon = menage.members.foyer_fiscal('prelsoc_fon', period)

        prel_foyer_fiscal_i = (prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_fon) * menage.members.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return menage.sum(prel_foyer_fiscal_i)


class check_csg(Variable):
    value_type = float
    entity = Menage
    label = u"check_csg"
    definition_period = YEAR

    def formula(menage, period):

        # CSG prélevée sur les revenus des foyers fiscaux, projetée sur les déclarants principaux
        csg_cap_bar = menage.members.foyer_fiscal('csg_cap_bar', periop)
        csg_pv_mo = menage.members.foyer_fiscal('csg_pv_mo', periop)
        csg_fon = menage.members.foyer_fiscal('csg_fon', periop)

        csg_foyer_fiscal_i = (csg_cap_bar + csg_pv_mo + csg_fon) * menage.members.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return menage.sum(csg_foyer_fiscal_i)


class check_crds(Variable):
    value_type = float
    entity = Menage
    label = u"check_crds"
    definition_period = YEAR

    def formula(menage, period):
        # CRDS prélevée sur les revenus des foyers fiscaux, projetée sur les déclarants principaux
        crds_pv_mo = menage.members.foyer_fiscal('crds_pv_mo', period)
        crds_fon = menage.members.foyer_fiscal('crds_fon', period)
        crds_cap_bar = menage.members.foyer_fiscal('crds_cap_bar', period)

        crds_foyer_fiscal_i = (crds_pv_mo + crds_fon + crds_cap_bar) * menage.members.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return menage.sum(crds_foyer_fiscal_i)
