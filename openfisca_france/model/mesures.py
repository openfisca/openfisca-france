# -*- coding: utf-8 -*-

from __future__ import division

from numpy import floor, logical_not as not_

from openfisca_france.model.base import *  # noqa analysis:ignore


class uc(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"Unités de consommation"

    def function(self, simulation, period):
        '''
        Calcule le nombre d'unités de consommation du ménage avec l'échelle de l'insee
        'men'
        '''
        period = period.this_year
        age_en_mois_holder = simulation.compute('age_en_mois', period)

        age_en_mois = self.split_by_roles(age_en_mois_holder)

        uc_adt = 0.5
        uc_enf = 0.3
        uc = 0.5
        for agm in age_en_mois.itervalues():
            age = floor(agm / 12)
            adt = (15 <= age) & (age <= 150)
            enf = (0 <= age) & (age <= 14)
            uc += adt * uc_adt + enf * uc_enf
        return period, uc


class typ_men(Variable):
    column = PeriodSizeIndependentIntCol(default = 0)
    entity = Menage
    label = u"Type de ménage"

    def function(self, simulation, period):
        '''
        type de menage
        'men'
        TODO: prendre les enfants du ménage et non ceux de la famille
        '''
        period = period.this_year
        en_couple_holder = simulation.compute('en_couple', period)
        af_nbenf_holder = simulation.compute('af_nbenf', period)

        af_nbenf = self.cast_from_entity_to_role(af_nbenf_holder, role = CHEF)
        af_nbenf = self.sum_by_entity(af_nbenf)
        isole = not_(self.cast_from_entity_to_role(en_couple_holder, role = CHEF))
        isole = self.sum_by_entity(isole)

        _0_kid = af_nbenf == 0
        _1_kid = af_nbenf == 1
        _2_kid = af_nbenf == 2
        _3_kid = af_nbenf >= 3

        return period, (0 * (isole & _0_kid) +  # Célibataire
                1 * (not_(isole) & _0_kid) +  # Couple sans enfants
                2 * (not_(isole) & _1_kid) +  # Couple un enfant
                3 * (not_(isole) & _2_kid) +  # Couple deux enfants
                4 * (not_(isole) & _3_kid) +  # Couple trois enfants et plus
                5 * (isole & _1_kid) +  # Famille monoparentale un enfant
                6 * (isole & _2_kid) +  # Famille monoparentale deux enfants
                7 * (isole & _3_kid))  # Famille monoparentale trois enfants et plus


class revdisp(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"Revenu disponible du ménage"
    url = "http://fr.wikipedia.org/wiki/Revenu_disponible"

    def function(self, simulation, period):
        '''
        Revenu disponible - ménage
        'men'
        '''
        period = period.start.period('year').offset('first-of')
        rev_trav_holder = simulation.compute('rev_trav', period)
        pen_holder = simulation.compute('pen', period)
        rev_cap_holder = simulation.compute('rev_cap', period)
        psoc_holder = simulation.compute('psoc', period)
        ppe_holder = simulation.compute('ppe', period)
        impo = simulation.calculate('impo', period)

        pen = self.sum_by_entity(pen_holder)
        ppe = self.cast_from_entity_to_role(ppe_holder, role = VOUS)
        ppe = self.sum_by_entity(ppe)
        psoc = self.cast_from_entity_to_role(psoc_holder, role = CHEF)
        psoc = self.sum_by_entity(psoc)
        rev_cap = self.sum_by_entity(rev_cap_holder)
        rev_trav = self.sum_by_entity(rev_trav_holder)

        return period, rev_trav + pen + rev_cap + psoc + ppe + impo


class nivvie(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"Niveau de vie du ménage"

    def function(self, simulation, period):
        '''
        Niveau de vie du ménage
        'men'
        '''
        period = period.this_year
        revdisp = simulation.calculate('revdisp', period)
        uc = simulation.calculate('uc', period)

        return period, revdisp / uc


class revenu_net_individu(Variable):
    column = FloatCol
    entity = Individu
    label = u"Revenu net de l'individu"

    def function(self, simulation, period):
        period = period.this_year
        pen = simulation.calculate('pen', period)
        rev_cap = simulation.calculate('rev_cap', period)
        rev_trav = simulation.calculate('rev_trav', period)

        return period, pen + rev_cap + rev_trav


class revnet(Variable):
    entity = Menage
    label = u"Revenu net du ménage"
    column = FloatCol
    url = u"http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php",

    def function(menage, period):
        revenu_net_individus = menage.members('revenu_net_individu', period)
        return period, menage.sum(revenu_net_individus)


class nivvie_net(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"Niveau de vie net du ménage"

    def function(self, simulation, period):
        '''
        Niveau de vie net du ménage
        'men'
        '''
        period = period.this_year
        revnet = simulation.calculate('revnet', period)
        uc = simulation.calculate('uc', period)

        return period, revnet / uc


class revenu_initial_individu(Variable):
    column = FloatCol
    entity = Individu
    label = u"Revenu initial de l'individu"

    def function(self, simulation, period):
        period = period.this_year
        cotisations_employeur_contributives = simulation.calculate('cotisations_employeur_contributives', period)
        cotisations_salariales_contributives = simulation.calculate('cotisations_salariales_contributives', period)
        pen = simulation.calculate('pen', period)
        rev_cap = simulation.calculate('rev_cap', period)
        rev_trav = simulation.calculate('rev_trav', period)

        return period, (rev_trav + pen + rev_cap - cotisations_employeur_contributives -
            cotisations_salariales_contributives)


class revini(Variable):
    entity = Menage
    label = u"Revenu initial du ménage"
    column = FloatCol

    def function(menage, period):
        revenu_initial_individus = menage.members('revenu_initial_individu', period)
        return period, simulation.menage.sum(revenu_initial_individus)


class nivvie_ini(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"Niveau de vie initial du ménage"

    def function(self, simulation, period):
        '''
        Niveau de vie initial du ménage
        'men'
        '''
        period = period.this_year
        revini = simulation.calculate('revini', period)
        uc = simulation.calculate('uc', period)

        return period, revini / uc


def _revprim(rev_trav, chomage_imposable, rev_cap, cotisations_employeur, cotisations_salariales):
    '''
    Revenu primaire du ménage
    Ensemble des revenus d'activités superbruts avant tout prélèvement
    Il est égale à la valeur ajoutée produite par les résidents
    'men'
    '''
    return rev_trav + rev_cap - cotisations_employeur - cotisations_salariales - chomage_imposable


class rev_trav(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Revenus du travail (salariés et non salariés)"
    url = "http://fr.wikipedia.org/wiki/Revenu_du_travail"

    def function(self, simulation, period):
        '''
        Revenu du travail
        '''
        period = period.this_year
        revenu_assimile_salaire = simulation.calculate('revenu_assimile_salaire', period)
        rag = simulation.calculate('rag', period)
        ric = simulation.calculate('ric', period)
        rnc = simulation.calculate('rnc', period)

        return period, revenu_assimile_salaire + rag + ric + rnc


class pen(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Pensions et revenus de remplacement"
    url = "http://fr.wikipedia.org/wiki/Rente"

    def function(individu, period):
        '''
        Pensions
        '''
        period = period.start.period('year').offset('first-of')
        chomage_net = individu('chomage_net', period)
        retraite_nette = individu('retraite_nette', period)
        pensions_alimentaires_percues = individu('pensions_alimentaires_percues', period)

        # Revenus du foyer fiscal, que l'on projette uniquement sur le 1er déclarant
        foyer_fiscal = individu.foyer_fiscal
        pensions_alimentaires_versees = foyer_fiscal('pensions_alimentaires_versees', period)
        retraite_titre_onereux = foyer_fiscal('retraite_titre_onereux', period, options = [ADD])
        pen_foyer_fiscal = pensions_alimentaires_versees + retraite_titre_onereux
        pen_foyer_fiscal_projetees = pen_foyer_fiscal * (individu.has_role(foyer_fiscal.DECLARANT_PRINCIPAL))

        return period, (chomage_net + retraite_nette + pensions_alimentaires_percues + pen_foyer_fiscal_projetees)


class cotsoc_bar(Variable):
    column = FloatCol(default = 0)
    entity = FoyerFiscal
    label = u"Cotisations sociales sur les revenus du capital imposés au barème"

    def function(self, simulation, period):
        '''
        Cotisations sociales sur les revenus du capital imposés au barème
        '''
        period = period.start.period('year').offset('first-of')
        csg_cap_bar = simulation.calculate('csg_cap_bar', period)
        prelsoc_cap_bar = simulation.calculate('prelsoc_cap_bar', period)
        crds_cap_bar = simulation.calculate('crds_cap_bar', period)

        return period, csg_cap_bar + prelsoc_cap_bar + crds_cap_bar


class cotsoc_lib(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire"

    def function(self, simulation, period):
        '''
        Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire
        '''
        period = period.this_year
        csg_cap_lib = simulation.calculate('csg_cap_lib', period)
        prelsoc_cap_lib = simulation.calculate('prelsoc_cap_lib', period)
        crds_cap_lib = simulation.calculate('crds_cap_lib', period)

        return period, csg_cap_lib + prelsoc_cap_lib + crds_cap_lib


class rev_cap(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Revenus du patrimoine"
    url = "http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"

    def function(individu, period):
        '''
        Revenus du patrimoine
        '''
        period = period.this_year

        # Revenus du foyer fiscal, que l'on projette uniquement sur le 1er déclarant
        foyer_fiscal = individu.foyer_fiscal
        fon = foyer_fiscal('fon', period)
        rev_cap_bar = foyer_fiscal('rev_cap_bar', period, options= [ADD])
        cotsoc_lib = foyer_fiscal('cotsoc_lib', period)
        rev_cap_lib = foyer_fiscal('rev_cap_lib', period, options= [ADD])
        imp_lib = foyer_fiscal('imp_lib', period)
        cotsoc_bar = foyer_fiscal('cotsoc_bar', period)

        revenus_foyer_fiscal = fon + rev_cap_bar + cotsoc_lib + rev_cap_lib + imp_lib + cotsoc_bar
        revenus_foyer_fiscal_projetes = revenus_foyer_fiscal * individu.has_role(foyer_fiscal.DECLARANT_PRINCIPAL)

        rac = individu('rac', period)

        return period, revenus_foyer_fiscal_projetes + rac


class psoc(Variable):
    column = FloatCol(default = 0)
    entity = Famille
    label = u"Prestations sociales"
    url = "http://fr.wikipedia.org/wiki/Prestation_sociale"

    def function(self, simulation, period):
        '''
        Prestations sociales
        '''
        period = period.this_year
        pfam = simulation.calculate('pfam', period)
        mini = simulation.calculate('mini', period)
        aides_logement = simulation.calculate('aides_logement', period)

        return period, pfam + mini + aides_logement


class pfam(Variable):
    column = FloatCol(default = 0)
    entity = Famille
    label = u"Prestations familiales"
    url = "http://www.social-sante.gouv.fr/informations-pratiques,89/fiches-pratiques,91/prestations-familiales,1885/les-prestations-familiales,12626.html"

    def function(self, simulation, period):
        '''
        Prestations familiales
        '''
        period = period.this_year
        af = simulation.calculate_add('af', period)
        cf = simulation.calculate_add('cf', period)
        ars = simulation.calculate('ars', period)
        aeeh = simulation.calculate('aeeh', period)
        paje = simulation.calculate_add('paje', period)
        asf = simulation.calculate_add('asf', period)
        crds_pfam = simulation.calculate('crds_pfam', period)

        return period, af + cf + ars + aeeh + paje + asf + crds_pfam


class mini(Variable):
    column = FloatCol(default = 0)
    entity = Famille
    label = u"Minima sociaux"
    url = "http://fr.wikipedia.org/wiki/Minima_sociaux"

    def function(self, simulation, period):
        '''
        Minima sociaux
        '''
        period = period.this_year
        aspa = simulation.calculate_add('aspa', period)
        aah_holder = simulation.compute_add('aah', period)
        caah_holder = simulation.compute_add('caah', period)
        asi = simulation.calculate_add('asi', period)
        rsa = simulation.calculate_add('rsa', period)
        aefa = simulation.calculate('aefa', period)
        api = simulation.calculate('api', period)
        ass = simulation.calculate_add('ass', period)
        ppa = simulation.calculate_add('ppa', period)
        psa = simulation.calculate_add('psa', period)

        aah = self.sum_by_entity(aah_holder)
        caah = self.sum_by_entity(caah_holder)

        return period, aspa + aah + caah + asi + rsa + aefa + api + ass + psa + ppa


class aides_logement(Variable):
    column = FloatCol(default = 0)
    entity = Famille
    label = u"Allocations logements"
    url = "http://vosdroits.service-public.fr/particuliers/N20360.xhtml"

    def function(self, simulation, period):
        '''
        Prestations logement
        '''
        period = period.this_year
        apl = simulation.calculate_add('apl', period)
        als = simulation.calculate_add('als', period)
        alf = simulation.calculate_add('alf', period)
        crds_logement = simulation.calculate_add('crds_logement', period)

        return period, apl + als + alf + crds_logement


class impo(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"Impôts directs"
    url = "http://fr.wikipedia.org/wiki/Imp%C3%B4t_direct"

    def function(self, simulation, period):
        '''
        Impôts directs
        '''
        period = period.this_year
        irpp_holder = simulation.compute('irpp', period)
        taxe_habitation = simulation.calculate('taxe_habitation', period)

        irpp = self.cast_from_entity_to_role(irpp_holder, role = VOUS)
        irpp = self.sum_by_entity(irpp)

        return period, irpp + taxe_habitation


class crds(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Contributions au remboursement de la dette sociale"

    def function(individu, period):
        """Contribution au remboursement de la dette sociale"""
        period = period.this_year

        # CRDS sur revenus individuels
        crds_salaire = individu('crds_salaire', period, options = [ADD])
        crds_retraite = individu('crds_retraite', period, options = [ADD])
        crds_chomage = individu('crds_chomage', period, options = [ADD])
        crds_individu = crds_salaire + crds_retraite + crds_chomage


        # CRDS sur revenus de la famille, projetés seulement sur la première personne
        crds_pfam = individu.famille('crds_pfam', period)
        crds_logement = individu.famille('crds_logement', period, options = [ADD])
        crds_mini = individu.famille('crds_mini', period, options = [ADD])
        crds_famille =  crds_pfam + crds_logement + crds_mini
        crds_famille_projetes = crds_famille * individu.has_role(Famille.DEMANDEUR)

        # CRDS sur revenus du foyer fiscal, projetés seulement sur la première personne
        crds_fon = individu.foyer_fiscal('crds_fon', period)
        crds_pv_mo = individu.foyer_fiscal('crds_pv_mo', period)
        crds_pv_immo = individu.foyer_fiscal('crds_pv_immo', period)
        crds_cap_bar = individu.foyer_fiscal('crds_cap_bar', period)
        crds_cap_lib = individu.foyer_fiscal('crds_cap_lib', period)
        crds_foyer_fiscal = crds_fon + crds_pv_mo + crds_pv_immo + crds_cap_bar + crds_cap_lib
        crds_foyer_fiscal_projetee = crds_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return period, crds_individu + crds_famille_projetes + crds_foyer_fiscal_projetee


class csg(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Contributions sociales généralisées"

    def function(individu, period):
        """Contribution sociale généralisée"""
        period = period.this_year
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

        return period, (csg_imposable_salaire + csg_deductible_salaire + csg_imposable_chomage +
                csg_deductible_chomage + csg_imposable_retraite + csg_deductible_retraite + csg_foyer_fiscal_projetee)


class cotsoc_noncontrib(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Cotisations sociales non contributives"

    def function(self, simulation, period):
        '''
        Cotisations sociales non contributives (hors prelsoc_cap_lib, prelsoc_cap_bar)
        '''
        period = period.this_year
        cotisations_employeur_non_contributives = simulation.calculate('cotisations_employeur_non_contributives',
            period)
        cotisations_salariales_non_contributives = simulation.calculate('cotisations_salariales_non_contributives',
            period)

        return period, cotisations_employeur_non_contributives + cotisations_salariales_non_contributives


class prelsoc_cap(Variable):
    column = FloatCol(default = 0)
    entity = Individu
    label = u"Prélèvements sociaux sur les revenus du capital"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"

    def function(individu, period):
        """
        Prélèvements sociaux sur les revenus du capital
        """
        period = period.this_year

        # Prélevements effectués sur les revenus du foyer fiscal
        prelsoc_fon = individu.foyer_fiscal('prelsoc_fon', period)
        prelsoc_cap_lib = individu.foyer_fiscal('prelsoc_cap_lib', period)
        prelsoc_cap_bar = individu.foyer_fiscal('prelsoc_cap_bar', period)
        prelsoc_pv_mo = individu.foyer_fiscal('prelsoc_pv_mo', period)
        prelsoc_pv_immo = individu.foyer_fiscal('prelsoc_pv_immo', period)
        prel_foyer_fiscal = prelsoc_fon + prelsoc_cap_lib + prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_pv_immo

        return period, prel_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)


class check_csk(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"check_csk"

    def function(menage, period):
        period = period.this_year

        foyer_fiscal = menage.personne_de_reference.foyer_fiscal

        # Prélevements effectués sur les revenus du foyer fiscal
        prelsoc_cap_bar = foyer_fiscal('prelsoc_cap_bar', period)
        prelsoc_pv_mo = foyer_fiscal('prelsoc_pv_mo', period)
        prelsoc_fon = foyer_fiscal('prelsoc_fon', period)

        return period, prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_fon


class check_csg(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"check_csg"

    def function(menage, period):
        period = period.this_year

        foyer_fiscal = menage.personne_de_reference.foyer_fiscal

        # CSG prélevée sur les revenus du foyer fiscal
        csg_cap_bar = foyer_fiscal('csg_cap_bar', periop)
        csg_pv_mo = foyer_fiscal('csg_pv_mo', periop)
        csg_fon = foyer_fiscal('csg_fon', periop)

        return period, csg_cap_bar + csg_pv_mo + csg_fon


class check_crds(Variable):
    column = FloatCol(default = 0)
    entity = Menage
    label = u"check_crds"

    def function(menage, period):
        period = period.this_year

        foyer_fiscal = menage.personne_de_reference.foyer_fiscal

        # CRDS prélevée sur les revenus du foyer fiscal
        crds_pv_mo = foyer_fiscal('crds_pv_mo', period)
        crds_fon = foyer_fiscal('crds_fon', period)
        crds_cap_bar = foyer_fiscal('crds_cap_bar', period)

        return period, crds_pv_mo + crds_fon + crds_cap_bar
