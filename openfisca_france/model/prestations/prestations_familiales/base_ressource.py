# -*- coding: utf-8 -*-

from __future__ import division

from numpy import int32, logical_not as not_, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore

class autonomie_financiere(Variable):
    column = BoolCol
    entity = Individus
    label = u"Indicatrice d'autonomie financière vis-à-vis des prestations familiales"

    def function(self, simulation, period):
        period = period.this_month
        salaire_net = simulation.calculate_add('salaire_net', period.start.period('month', 6).offset(-6))
        _P = simulation.legislation_at(period.start)

        nbh_travaillees = 169
        smic_mensuel_brut = _P.cotsoc.gen.smic_h_b * nbh_travaillees

        # Oui on compare du salaire net avec un bout du SMIC brut ...
        return period, salaire_net / 6 >= (_P.fam.af.seuil_rev_taux * smic_mensuel_brut)


class prestations_familiales_enfant_a_charge(Variable):
    column = BoolCol
    entity = Individus
    label = u"Enfant considéré à charge au sens des prestations familiales"

    def function(self, simulation, period):
        period = period.this_month

        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        autonomie_financiere = simulation.calculate('autonomie_financiere', period)
        age = simulation.calculate('age', period)
        rempli_obligation_scolaire = simulation.calculate('rempli_obligation_scolaire', period)

        pfam = simulation.legislation_at(period.start).fam

        condition_enfant = ((age >= pfam.enfants.age_minimal) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.enfants.age_limite) * not_(autonomie_financiere)

        return period, or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


class prestations_familiales_base_ressources_individu(Variable):
    column = FloatCol(default = 0)
    entity = Individus
    label = u"Base ressource individuelle des prestations familiales"

    def function(self, simulation, period):
        period = period.this_month
        annee_fiscale_n_2 = period.n_2

        traitements_salaires_pensions_rentes = simulation.calculate('traitements_salaires_pensions_rentes', annee_fiscale_n_2)
        hsup = simulation.calculate('hsup', annee_fiscale_n_2)
        rpns = simulation.calculate('rpns', annee_fiscale_n_2)
        glo = simulation.calculate('glo', annee_fiscale_n_2)
        div = simulation.calculate('div', annee_fiscale_n_2)

        return period, traitements_salaires_pensions_rentes + hsup + rpns + glo + div


class biactivite(Variable):
    column = BoolCol(default = False)
    entity = Familles
    label = u"Indicatrice de biactivité"

    def function(self, simulation, period):
        period = period.this_month
        annee_fiscale_n_2 = period.n_2

        pfam = simulation.legislation_at(annee_fiscale_n_2.start).fam
        seuil_rev = 12 * pfam.af.bmaf

        base_ressources_i = simulation.calculate('prestations_familiales_base_ressources_individu', period)

        return period, simulation.famille.all(base_ressources_i >= seuil_rev, role = PARENT)


class div(Variable):
    column = FloatCol(default = 0)
    entity = Individus
    label = u"Dividendes imposés"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        rpns_pvce = simulation.calculate('rpns_pvce', period)
        rpns_pvct = simulation.calculate('rpns_pvct', period)
        rpns_mvct = simulation.calculate('rpns_mvct', period)
        rpns_mvlt = simulation.calculate('rpns_mvlt', period)
        f3vc_holder = simulation.compute('f3vc', period)
        f3ve_holder = simulation.compute('f3ve', period)
        f3vg_holder = simulation.compute('f3vg', period)
        f3vh_holder = simulation.compute('f3vh', period)
        f3vl_holder = simulation.compute('f3vl', period)
        f3vm_holder = simulation.compute('f3vm', period)
        f3vt_holder = simulation.compute('f3vt', period)

        f3vc = self.cast_from_entity_to_role(f3vc_holder, role = VOUS)
        f3ve = self.cast_from_entity_to_role(f3ve_holder, role = VOUS)
        f3vg = self.cast_from_entity_to_role(f3vg_holder, role = VOUS)
        f3vh = self.cast_from_entity_to_role(f3vh_holder, role = VOUS)
        f3vl = self.cast_from_entity_to_role(f3vl_holder, role = VOUS)
        f3vm = self.cast_from_entity_to_role(f3vm_holder, role = VOUS)
        f3vt = self.cast_from_entity_to_role(f3vt_holder, role = VOUS)

        return period, f3vc + f3ve + f3vg - f3vh + f3vl + f3vm + f3vt + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt


class rev_coll(Variable):
    column = FloatCol(default = 0)
    entity = FoyersFiscaux
    label = u"Revenus perçus par le foyer fiscal à prendre en compte dans la base ressource des prestations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')

        # Quand rev_coll est calculé sur une année glissante, retraite_titre_onereux_net et pensions_alimentaires_versees sont calculés sur l'année légale correspondante.
        retraite_titre_onereux_net = simulation.calculate('retraite_titre_onereux_net', period.offset('first-of'))
        pensions_alimentaires_versees = simulation.calculate('pensions_alimentaires_versees', period.offset('first-of'))
        rev_cap_lib = simulation.calculate_add('rev_cap_lib', period)
        rev_cat_rvcm = simulation.calculate('rev_cat_rvcm', period)
        abat_spe = simulation.calculate('abat_spe', period)
        fon = simulation.calculate('fon', period)
        f7ga = simulation.calculate('f7ga', period)
        f7gb = simulation.calculate('f7gb', period)
        f7gc = simulation.calculate('f7gc', period)
        rev_cat_pv = simulation.calculate('rev_cat_pv', period)

        # TODO: ajouter les revenus de l'étranger etr*0.9
        # pensions_alimentaires_versees is negative since it is paid by the declaree
        return period, (retraite_titre_onereux_net + rev_cap_lib + rev_cat_rvcm + fon + pensions_alimentaires_versees - f7ga - f7gb - f7gc - abat_spe + rev_cat_pv)


class prestations_familiales_base_ressources(Variable):
    column = FloatCol(default = 0)
    entity = Familles
    label = u"Base ressource des prestations familiales"

    def function(self, simulation, period):
        '''
        Base ressource des prestations familiales de la famille
        'fam'
        '''
        period = period.this_month
        # period_legacy = period.start.offset('first-of', 'month').period('year')
        annee_fiscale_n_2 = period.n_2

        base_ressources_i = simulation.calculate('prestations_familiales_base_ressources_individu', period)
        enfant_i = simulation.calculate('est_enfant_dans_famille', period)
        enfant_a_charge_i = simulation.calculate('prestations_familiales_enfant_a_charge', period)
        ressources_i = (not_(enfant_i) + enfant_a_charge_i) * base_ressources_i
        base_ressources_i_total = self.sum_by_entity(ressources_i)

        # Revenus du foyer fiscal
        rev_coll = simulation.calculate('rev_coll', annee_fiscale_n_2)
        rev_coll_famille = simulation.famille.transpose(rev_coll, origin_entity = FoyersFiscaux)

        base_ressources = base_ressources_i_total + rev_coll_famille
        return period, base_ressources


############################################################################
# Helper functions
############################################################################


def nb_enf(simulation, period, age_min, age_max):
    """
    Renvoie le nombre d'enfant au sens des allocations familiales dont l'âge est compris entre ag1 et ag2
    """
    period = period.this_month
    age = simulation.calculate('age', period)
    autonomie_financiere = simulation.calculate('autonomie_financiere', period)

#        Les allocations sont dues à compter du mois civil qui suit la naissance
#        ag1==0 ou suivant les anniversaires ag1>0.
#        Un enfant est reconnu à charge pour le versement des prestations
#        jusqu'au mois précédant son age limite supérieur (ag2 + 1) mais
#        le versement à lieu en début de mois suivant
    condition = (age >= age_min) * (age <= age_max) * not_(autonomie_financiere)

    return simulation.famille.sum(condition, role = ENFANT)



def age_en_mois_benjamin(ages_en_mois):
    '''
    Renvoie un vecteur (une entree pour chaque famille) avec l'age du benjamin.  # TODO check age_en_mois > 0
    '''
    age_en_mois_benjamin = 12 * 9999
    for age_en_mois in ages_en_mois.itervalues():
        isbenjamin = (age_en_mois < age_en_mois_benjamin) & (age_en_mois != -9999)
        age_en_mois_benjamin = isbenjamin * age_en_mois + not_(isbenjamin) * age_en_mois_benjamin
    return age_en_mois_benjamin
