# -*- coding: utf-8 -*-

from __future__ import division

import logging

from numpy import (datetime64, logical_and as and_, logical_not as not_, logical_or as or_, logical_xor as xor_,
    maximum as max_, minimum as min_, round)

from openfisca_france.model.base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


# TODO: 8ti et 8tk (cerfa 2047)
# TODO: CSG, CRDS et prélèvements sociaux sur revenu du patrimione, d'activité et de remplacement
# TODO: finir RPNS (prise en compte des plafonds / cases non codées : codées pour certaines années mais pas pour
# d'autres - car des cases sont réutilisées pour des variables différentes suivant les années)

# zetrf = zeros(taille)
# jeune_veuf = zeros(taille, dtype = bool)
# Reprise du crédit d'impôt en faveur des jeunes, des accomptes et des versements mensues de prime pour l'emploi
# reprise = zeros(taille) # TODO : reprise=J80
# Pcredit = P.credits_impots
# if hasattr(P.reductions_impots,'saldom'): Pcredit.saldom = P.reductions_impots.saldom
# credits_impot = Credits(Pcredit, table)
# Réduction d'impôt
# reductions = Reductions(IPnet, P.reductions_impots)

# def mcirra():
#    # impôt sur le revenu
#    mcirra = -((IMP<=-8)*IMP)
#    mciria = max_(0,(IMP>=0)*IMP)
# #        mciria = max_(0,(IMP>=0)*IMP - credimp_etranger - cont_rev_loc - ( f8to + f8tb + f8tc ))
#
#    # Dans l'ERFS, les prelevement libératoire sur les montants non déclarés
#    # sont intégrés. Pas possible de le recalculer.
#
#    # impot sur le revenu du foyer (hors prélèvement libératoire, revenus au quotient)
#    irpp   = -(mciria + ppetot - mcirra )


class jour_xyz(Variable):
    column = IntCol(default = 360)
    entity_class = FoyersFiscaux
    label = u"Jours décomptés au titre de cette déclaration"

class nbptr_n_2(Variable):
    column = PeriodSizeIndependentIntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Nombre de parts année n - 2"




###############################################################################
# # Initialisation de quelques variables utiles pour la suite
###############################################################################


class age(Variable):
    base_function = missing_value
    column = AgeCol(val_type = "age")
    entity_class = Individus
    label = u"Âge (en années)"

    def function(self, simulation, period):
        has_birth = simulation.get_or_new_holder('date_naissance')._array is not None
        if not has_birth:
            has_age_en_mois = bool(simulation.get_or_new_holder('age_en_mois')._array_by_period)
            if has_age_en_mois:
                return period, simulation.calculate('age_en_mois', period) // 12

            # If age is known at the same day of another year, compute the new age from it.
            holder = self.holder
            start = period.start
            if holder._array_by_period is not None:
                for last_period, last_array in sorted(holder._array_by_period.iteritems(), reverse = True):
                    last_start = last_period.start
                    if last_start.day == start.day:
                        return period, last_array + int((start.year - last_start.year) +
                            (start.month - last_start.month) / 12)

        date_naissance = simulation.calculate('date_naissance', period)
        return period, (datetime64(period.start) - date_naissance).astype('timedelta64[Y]')


class age_en_mois(Variable):
    base_function = missing_value
    column = AgeCol(val_type = "months")
    entity_class = Individus
    label = u"Âge (en mois)"

    def function(self, simulation, period):
        # If age_en_mois is known at the same day of another month, compute the new age_en_mois from it.
        holder = self.holder
        start = period.start
        if holder._array_by_period is not None:
            for last_period, last_array in sorted(holder._array_by_period.iteritems(), reverse = True):
                last_start = last_period.start
                if last_start.day == start.day:
                    return period, last_array + ((start.year - last_start.year) * 12 + (start.month - last_start.month))

        has_birth = simulation.get_or_new_holder('date_naissance')._array is not None
        if not has_birth:
            has_age = bool(simulation.get_or_new_holder('age')._array_by_period)
            if has_age:
                return period, simulation.calculate('age', period) * 12
        date_naissance = simulation.calculate('date_naissance', period)
        return period, (datetime64(period.start) - date_naissance).astype('timedelta64[M]')


class nb_adult(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'adulte(s) déclarants dans le foyer fiscal"

    def function(self, simulation, period):
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        celibataire_ou_divorce = simulation.calculate('celibataire_ou_divorce', period)
        veuf = simulation.calculate('veuf', period)

        return period, 2 * maries_ou_pacses + 1 * (celibataire_ou_divorce | veuf)


class nb_pac(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Nombre de personnes à charge dans le foyer fiscal"

    def function(self, simulation, period):
        period = period.this_year
        nbF = simulation.calculate('nbF', period)
        nbJ = simulation.calculate('nbJ', period)
        nbR = simulation.calculate('nbR', period)

        return period, nbF + nbJ + nbR


class enfant_a_charge(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant à charge non marié, de moins de 18 ans au 1er janvier de l'année de perception des" \
        u" revenus, ou né durant la même année, ou handicapés quel que soit son âge"

    def function(self, simulation, period):
        age = simulation.calculate('age', period)
        handicap = simulation.calculate('handicap', period)
        quifoy = simulation.calculate('quifoy', period)

        return period, (quifoy >= 2) * ((age < 18) + handicap)


class nbF(Variable):
    cerfa_field = u'F'
    entity_class = FoyersFiscaux
    column = FloatCol
    label = u"Nombre d'enfants à charge non mariés, qui ne sont pas en résidence alternée, de moins de 18 ans au 1er janvier de l'année de perception des" \
        u" revenus, ou nés durant la même année ou handicapés quel que soit leur âge"

    def function(self, simulation, period):
        period = period.this_year
        enfant_a_charge = simulation.compute('enfant_a_charge', period)
        garde_alternee = simulation.compute('garde_alternee', period)
        return period, self.sum_by_entity(enfant_a_charge.array * not_(garde_alternee.array))


class nbG(Variable):
    cerfa_field = u'G'
    entity_class = FoyersFiscaux
    column = FloatCol
    label = u"Nombre d'enfants qui ne sont pas en résidence alternée à charge titulaires de la carte d'invalidité."

    def function(self, simulation, period):
        period = period.this_year
        enfant_a_charge = simulation.compute('enfant_a_charge', period)
        garde_alternee = simulation.compute('garde_alternee', period)
        invalidite = simulation.compute('invalidite', period)
        return period, self.sum_by_entity(enfant_a_charge.array * not_(garde_alternee.array) * invalidite.array)


class nbH(Variable):
    cerfa_field = u'H'
    entity_class = FoyersFiscaux
    column = FloatCol
    label = u"Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de" \
        u" l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge"

    def function(self, simulation, period):
        period = period.this_year
        enfant_a_charge = simulation.compute('enfant_a_charge', period)
        garde_alternee = simulation.compute('garde_alternee', period)
        return period, self.sum_by_entity(enfant_a_charge.array * garde_alternee.array)


class nbI(Variable):
    cerfa_field = u'I'
    entity_class = FoyersFiscaux
    column = FloatCol
    label = u"Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité"

    def function(self, simulation, period):
        period = period.this_year
        enfant_a_charge = simulation.compute('enfant_a_charge', period)
        garde_alternee = simulation.compute('garde_alternee', period)
        invalidite = simulation.compute('invalidite', period)
        return period, self.sum_by_entity(enfant_a_charge.array * garde_alternee.array * invalidite.array)


class enfant_majeur_celibataire_sans_enfant(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant majeur célibataire sans enfant"

    def function(self, simulation, period):
        period = period.this_year
        age = simulation.calculate('age', period)
        handicap = simulation.calculate('handicap', period)
        quifoy = simulation.calculate('quifoy', period)

        return period, (quifoy >= 2) * (age >= 18) * not_(handicap)


class nbJ(PersonToEntityColumn):
    cerfa_field = u'J'
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants majeurs célibataires sans enfant"
    operation = 'add'
    variable = enfant_majeur_celibataire_sans_enfant


class nombre_enfants_majeurs_celibataires_sans_enfant(PersonToEntityColumn):
    entity_class = Menages
    label = u"Nombre d'enfants majeurs célibataires sans enfant"
    operation = 'add'
    variable = enfant_majeur_celibataire_sans_enfant


class maries_ou_pacses(Variable):
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Déclarants mariés ou pacsés"

    def function(self, simulation, period):
        period = period.this_year
        statut_marital_holder = simulation.compute('statut_marital', period)

        statut_marital = self.filter_role(statut_marital_holder, role = VOUS)

        return period, (statut_marital == 1) | (statut_marital == 5)


class celibataire_ou_divorce(Variable):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"Déclarant célibataire ou divorcé"

    def function(self, simulation, period):
        period = period.this_year
        statut_marital_holder = simulation.compute('statut_marital', period)

        statut_marital = self.filter_role(statut_marital_holder, role = VOUS)

        return period, (statut_marital == 2) | (statut_marital == 3)


class veuf(Variable):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"Déclarant veuf"

    def function(self, simulation, period):
        period = period.this_year
        statut_marital_holder = simulation.compute('statut_marital', period)

        statut_marital = self.filter_role(statut_marital_holder, role = VOUS)

        return period, statut_marital == 4


class jeune_veuf(Variable):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"Déclarant jeune veuf"

    def function(self, simulation, period):
        period = period.this_year
        statut_marital_holder = simulation.compute('statut_marital', period)

        statut_marital = self.filter_role(statut_marital_holder, role = VOUS)

        return period, statut_marital == 6


###############################################################################
# # Revenus catégoriels
###############################################################################


class revenu_assimile_salaire(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu imposé comme des salaires (salaires, mais aussi 3vj, 3vk)"

    def function(self, simulation, period):
        period = period.this_year
        salaire_imposable =  simulation.calculate_add('salaire_imposable', period)
        chomage_imposable = simulation.calculate_add('chomage_imposable', period)

        return period, salaire_imposable + chomage_imposable


class revenu_assimile_salaire_apres_abattements(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Salaires et chômage imposables après abattements"

    def function(self, simulation, period):
        period = period.this_year
        revenu_assimile_salaire = simulation.calculate('revenu_assimile_salaire', period)
        chomeur_longue_duree = simulation.calculate('chomeur_longue_duree', period)
        frais_reels = simulation.calculate('frais_reels', period)
        abatpro = simulation.legislation_at(period.start).ir.tspr.abatpro

        abattement_minimum = abatpro.min * not_(chomeur_longue_duree) + abatpro.min2 * chomeur_longue_duree
        abatfor = round(min_(max_(abatpro.taux * revenu_assimile_salaire, abattement_minimum), abatpro.max))
        return period, (
            (frais_reels > abatfor) * (revenu_assimile_salaire - frais_reels) + (frais_reels <= abatfor) * max_(0, revenu_assimile_salaire - abatfor)
            )


class revenu_activite_salariee(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu d'activité salariée"

    def function(self, simulation, period):
        period = period.this_year
        salaire_imposable =  simulation.calculate_add('salaire_imposable', period)

        return period, salaire_imposable


class revenu_activite_non_salariee(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu d'activité non salariée"

    def function(self, simulation, period):
        period = period.this_year
        rpns_i = simulation.calculate('rpns_individu', period)

        return period, rpns_i # TODO: vérifier cette définition


class revenu_activite(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus d'activités"

    def function(self, simulation, period):
        ''' Revenus d'activités '''
        period = period.this_year
        revenu_activite_non_salariee = simulation.calculate('revenu_activite_non_salariee', period)
        revenu_activite_salariee = simulation.calculate('revenu_activite_salariee', period)

        return period, revenu_activite_non_salariee + revenu_activite_salariee


class revenu_assimile_pension(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu imposé comme des pensions (retraites, pensions alimentaires, etc.)"

    def function(self, simulation, period):
        period = period.this_year
        pensions_alimentaires_percues = simulation.calculate_add('pensions_alimentaires_percues', period)
        pensions_alimentaires_percues_decl = simulation.calculate_add('pensions_alimentaires_percues_decl', period)
        retraite_imposable = simulation.calculate_add('retraite_imposable', period)

        return period, pensions_alimentaires_percues * pensions_alimentaires_percues_decl + retraite_imposable


class revenu_assimile_pension_apres_abattements(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Pensions après abattements"

    def function(self, simulation, period):
        period = period.this_year
        revenu_assimile_pension = simulation.calculate('revenu_assimile_pension', period)
        abatpen = simulation.legislation_at(period.start).ir.tspr.abatpen

        #    TODO: problème car les pensions sont majorées au niveau du foyer
    #    d11 = ( AS + BS + CS + DS + ES +
    #            AO + BO + CO + DO + EO )
    #    penv2 = (d11-f11> abatpen.max)*(penv + (d11-f11-abatpen.max)) + (d11-f11<= abatpen.max)*penv
    #    Plus d'abatement de 20% en 2006
        return period, max_(0, revenu_assimile_pension - round(max_(abatpen.taux * revenu_assimile_pension , abatpen.min)))


#    return max_(0, revenu_assimile_pension - min_(round(max_(abatpen.taux*revenu_assimile_pension , abatpen.min)), abatpen.max))  le max se met au niveau du foyer

class indu_plaf_abat_pen(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Plafonnement de l'abattement de 10% sur les pensions du foyer"

    def function(self, simulation, period):
        period = period.this_year
        rev_pen_holder = simulation.compute('revenu_assimile_pension', period)
        pen_net_holder = simulation.compute('revenu_assimile_pension_apres_abattements', period)
        abatpen = simulation.legislation_at(period.start).ir.tspr.abatpen

        revenu_assimile_pension_apres_abattements = self.sum_by_entity(pen_net_holder)
        revenu_assimile_pension = self.sum_by_entity(rev_pen_holder)

        abat = revenu_assimile_pension - revenu_assimile_pension_apres_abattements
        return period, abat - min_(abat, abatpen.max)


class abattement_salaires_pensions(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Abattement de 20% sur les salaires et pensions, en vigueur jusqu'à 2006"
    stop_date = date(2005, 12, 31)

    def function(self, simulation, period):
        period = period.this_year
        revenu_assimile_salaire_apres_abattements = simulation.calculate('revenu_assimile_salaire_apres_abattements', period)
        revenu_assimile_pension_apres_abattements = simulation.calculate('revenu_assimile_pension_apres_abattements', period)
        abatsalpen = simulation.legislation_at(period.start).ir.tspr.abatsalpen

        return period, min_(abatsalpen.taux * max_(revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements, 0), abatsalpen.max)


class retraite_titre_onereux(Variable):
    """Rentes viagères à titre onéreux (avant abattements)

    Annuel pour les impôts mais mensuel pour la base ressource des minimas sociaux donc mensuel.
    """
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Rentes viagères (rentes à titre onéreux)"
    set_input = set_input_divide_by_period
    url = u"http://fr.wikipedia.org/wiki/Rente_viagère"

    def function(self, simulation, period):
        year = period.start.period(u'year').offset('first-of')
        period = period.this_month
        f1aw = simulation.calculate('f1aw', year)
        f1bw = simulation.calculate('f1bw', year)
        f1cw = simulation.calculate('f1cw', year)
        f1dw = simulation.calculate('f1dw', year)

        return period, (f1aw + f1bw + f1cw + f1dw) / 12


class retraite_titre_onereux_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Rentes viagères (rentes à titre onéreux) (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = retraite_titre_onereux


class retraite_titre_onereux_net(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Rentes viagères après abattements"
    url = u"http://www.lafinancepourtous.fr/Vie-professionnelle-et-retraite/Retraite/Epargne-retraite/La-rente-viagere/La-fiscalite-de-la-rente-viagere"  # noqa

    def function(self, simulation, period):
        period = period.this_year
        f1aw = simulation.calculate('f1aw', period)
        f1bw = simulation.calculate('f1bw', period)
        f1cw = simulation.calculate('f1cw', period)
        f1dw = simulation.calculate('f1dw', period)
        abatviag = simulation.legislation_at(period.start).ir.tspr.abatviag

        return period, round(abatviag.taux1 * f1aw + abatviag.taux2 * f1bw + abatviag.taux3 * f1cw + abatviag.taux4 * f1dw)


class retraite_titre_onereux_net_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Rentes viagères après abattements (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = retraite_titre_onereux_net


class traitements_salaires_pensions_rentes(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Traitements salaires pensions et rentes individuelles"

    def function(self, simulation, period):
        period = period.this_year

        revenu_assimile_salaire_apres_abattements = simulation.calculate('revenu_assimile_salaire_apres_abattements', period)
        revenu_assimile_pension_apres_abattements = simulation.calculate('revenu_assimile_pension_apres_abattements', period)
        abattement_salaires_pensions = simulation.calculate('abattement_salaires_pensions', period)

        # Quand tspr est calculé sur une année glissante, retraite_titre_onereux_net_declarant1 est calculé sur l'année légale
        # correspondante.
        retraite_titre_onereux_net_declarant1 = simulation.calculate('retraite_titre_onereux_net_declarant1', period.offset('first-of'))

        return period, revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements - abattement_salaires_pensions + retraite_titre_onereux_net_declarant1


class rev_cat_pv(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Plus-values"
    start_date = date(2013, 1, 1)
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, simulation, period):
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        f3vh = simulation.calculate('f3vh', period)

        return period, f3vg - f3vh


class rev_cat_tspr(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Traitements, salaires, pensions et rentes"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, simulation, period):
        period = period.this_year
        tspr_holder = simulation.compute('traitements_salaires_pensions_rentes', period)
        indu_plaf_abat_pen = simulation.calculate('indu_plaf_abat_pen', period)

        traitements_salaires_pensions_rentes = self.sum_by_entity(tspr_holder)

        return period, traitements_salaires_pensions_rentes + indu_plaf_abat_pen


class deficit_rcm(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Deficit capitaux mobiliers"
    start_date = date(2009, 1, 1)
    url = "http://www.lefigaro.fr/impots/2008/04/25/05003-20080425ARTFIG00254-les-subtilites-des-revenus-de-capitaux-mobiliers-.php"

    def function(self, simulation, period):
        period = period.this_year
        f2aa = simulation.calculate('f2aa', period)
        f2al = simulation.calculate('f2al', period)
        f2am = simulation.calculate('f2am', period)
        f2an = simulation.calculate('f2an', period)
        f2aq = simulation.calculate('f2aq', period)
        f2ar = simulation.calculate('f2ar', period)
        _P = simulation.legislation_at(period.start)

        return period, f2aa + f2al + f2am + f2an + f2aq + f2ar


class rev_cat_rvcm(DatedVariable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Capitaux"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    @dated_function(start = date(2002, 1, 1), stop = date(2004, 12, 31))
    def function_20020101_20041231(self, simulation, period):
        """
        Revenus des valeurs et capitaux mobiliers
        """
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        deficit_rcm = simulation.calculate('deficit_rcm', period)
        f2ch = simulation.calculate('f2ch', period)
        f2dc = simulation.calculate('f2dc', period)
        f2ts = simulation.calculate('f2ts', period)
        f2ca = simulation.calculate('f2ca', period)
        f2fu = simulation.calculate('f2fu', period)
        f2go = simulation.calculate('f2go', period)
        f2gr = simulation.calculate('f2gr', period)
        f2tr = simulation.calculate('f2tr', period)
        _P = simulation.legislation_at(period.start)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl
        rvcm = simulation.legislation_at(period.start).ir.rvcm

        f2dc_bis = f2dc
        f2tr_bis = f2tr
        # # Calcul du revenu catégoriel
        # 1.2 Revenus des valeurs et capitaux mobiliers
        b12 = min_(f2ch, rvcm.abat_assvie * (1 + maries_ou_pacses))
        TOT1 = f2ch - b12  # c12
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie négative (à déduire des autres revenus nets de frais d'abattements
        g12a = -min_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.abatmob_taux)

        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + maries_ou_pacses)
        TOT2 = max_(0, rev - h12)
        # i121= -min_(0,rev - h12)

        # Part des frais s'imputant sur les revenus déclarés ligne TS
        F2 = f2ca - F1
        TOT3 = (f2ts - F2) + f2go * rvcm.majGO + f2tr_bis - g12a

        DEF = deficit_rcm
        return period, max_(TOT1 + TOT2 + TOT3 - DEF, 0)

    @dated_function(start = date(2005, 1, 1), stop = date(2012, 12, 31))
    def function_20050101_20121231(self, simulation, period):
        """
        Revenus des valeurs et capitaux mobiliers
        """
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        deficit_rcm = simulation.calculate('deficit_rcm', period)
        f2ch = simulation.calculate('f2ch', period)
        f2dc = simulation.calculate('f2dc', period)
        f2ts = simulation.calculate('f2ts', period)
        f2ca = simulation.calculate('f2ca', period)
        f2fu = simulation.calculate('f2fu', period)
        f2go = simulation.calculate('f2go', period)
        f2gr = simulation.calculate('f2gr', period)
        f2tr = simulation.calculate('f2tr', period)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl
        rvcm = simulation.legislation_at(period.start).ir.rvcm

        # Add f2da to f2dc and f2ee to f2tr when no PFL
        f2dc_bis = f2dc
        f2tr_bis = f2tr
        # # Calcul du revenu catégoriel
        # 1.2 Revenus des valeurs et capitaux mobiliers
        b12 = min_(f2ch, rvcm.abat_assvie * (1 + maries_ou_pacses))
        TOT1 = f2ch - b12  # c12
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie négative (à déduire des autres revenus nets de frais d'abattements
        g12a = -min_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.abatmob_taux)

        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + maries_ou_pacses)
        TOT2 = max_(0, rev - h12)
        # i121= -min_(0,rev - h12)

        # Part des frais s'imputant sur les revenus déclarés ligne TS
        F2 = f2ca - F1
        TOT3 = (f2ts - F2) + f2go * rvcm.majGO + f2tr_bis - g12a

        DEF = deficit_rcm
        return period, max_(TOT1 + TOT2 + TOT3 - DEF, 0)

    @dated_function(start = date(2013, 1, 1))
    def function_20130101_20151231(self, simulation, period):
        """
        Revenus des valeurs et capitaux mobiliers
        """
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        deficit_rcm = simulation.calculate('deficit_rcm', period)
        f2ch = simulation.calculate('f2ch', period)
        f2dc = simulation.calculate('f2dc', period)
        f2ts = simulation.calculate('f2ts', period)
        f2ca = simulation.calculate('f2ca', period)
        f2fu = simulation.calculate('f2fu', period)
        f2go = simulation.calculate('f2go', period)
        f2tr = simulation.calculate('f2tr', period)
        f2da = simulation.calculate('f2da', period)
        f2ee = simulation.calculate('f2ee', period)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl
        rvcm = simulation.legislation_at(period.start).ir.rvcm

        # Add f2da to f2dc and f2ee to f2tr when no PFL
        f2dc_bis = f2dc + f2da  # TODO: l'abattement de 40% est déduit uniquement en l'absence de revenus déclarés case 2DA
        f2tr_bis = f2tr + f2ee

        # # Calcul du revenu catégoriel
        # 1.2 Revenus des valeurs et capitaux mobiliers
        b12 = min_(f2ch, rvcm.abat_assvie * (1 + maries_ou_pacses))
        TOT1 = f2ch - b12  # c12
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie négative (à déduire des autres revenus nets de frais d'abattements
        g12a = -min_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2fu * (1 - rvcm.abatmob_taux)

        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + maries_ou_pacses)
        TOT2 = max_(0, rev - h12)
        # i121= -min_(0,rev - h12)

        # Part des frais s'imputant sur les revenus déclarés ligne TS
        F2 = f2ca - F1
        TOT3 = (f2ts - F2) + f2go * rvcm.majGO + f2tr_bis - g12a

        DEF = deficit_rcm
        return period, max_(TOT1 + TOT2 + TOT3 - DEF, 0)


class rfr_rvcm(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"rfr_rvcm"

    def function(self, simulation, period):
        '''
        Abattements sur rvcm à réintégrer dans le revenu fiscal de référence
        '''
        period = period.this_year
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        f2dc = simulation.calculate('f2dc', period)
        f2ts = simulation.calculate('f2ts', period)
        f2ca = simulation.calculate('f2ca', period)
        f2gr = simulation.calculate('f2gr', period)
        f2fu = simulation.calculate('f2fu', period)
        f2da = simulation.calculate('f2da', period)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl
        rvcm = simulation.legislation_at(period.start).ir.rvcm

        if finpfl:
            f2dc_bis = f2dc + f2da
        else:
            f2dc_bis = f2dc

        # Calcul de i121
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.abatmob_taux)

        # Abattements, limité au revenu
        h12 = rvcm.abatmob * (1 + maries_ou_pacses)
        i121 = - min_(0, rev - h12)
        return period, max_((rvcm.abatmob_taux) * (f2dc_bis + f2fu) - i121, 0)


class rev_cat_rfon(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Foncier"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, simulation, period):
        """
        Revenus fonciers
        TODO: add assert in validator
        """
        period = period.this_year
        f4ba = simulation.calculate('f4ba', period)
        f4bb = simulation.calculate('f4bb', period)
        f4bc = simulation.calculate('f4bc', period)
        f4bd = simulation.calculate('f4bd', period)
        f4be = simulation.calculate('f4be', period)
        microfoncier = simulation.legislation_at(period.start).ir.microfoncier

        # # Calcul du revenu catégoriel
        if ((f4be != 0) & ((f4ba != 0) | (f4bb != 0) | (f4bc != 0))).any():
            log.error(("Problème de déclarations des revenus : incompatibilité de la déclaration des revenus fonciers (f4ba, f4bb, f4bc) et microfonciers (f4be)"))

        a13 = f4ba + f4be - microfoncier.taux * f4be * (f4be <= microfoncier.max)
        b13 = f4bb
        c13 = a13 - b13
        d13 = f4bc
        e13 = c13 - d13 * (c13 >= 0)
        f13 = f4bd * (e13 >= 0)
        g13 = max_(0, e13 - f13)
        rev_cat_rfon = (c13 >= 0) * (g13 + e13 * (e13 < 0)) - (c13 < 0) * d13
        return period, rev_cat_rfon


class rev_cat_rpns(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu catégoriel - Revenus personnels non salariés"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, simulation, period):
        '''
        Revenus personnels non salariés
        'foy'
        '''
        period = period.this_year
        nbnc_pvce_holder = simulation.compute('nbnc_pvce', period)
        mbic_mvct = simulation.calculate('mbic_mvct', period)
        rpns_i_holder = simulation.compute('rpns_individu', period)
        defrag = simulation.calculate('defrag', period)
        defacc = simulation.calculate('defacc', period)
        defncn = simulation.calculate('defncn', period)
        defmeu = simulation.calculate('defmeu', period)

        return period, (
            self.sum_by_entity(rpns_i_holder) -
            self.sum_by_entity(nbnc_pvce_holder) - defrag - defncn - defacc - defmeu - mbic_mvct
            )


class rev_cat(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenus catégoriels"
    url = "http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"

    def function(self, simulation, period):
        '''
        Revenus Categoriels
        '''
        period = period.this_year
        rev_cat_tspr = simulation.calculate('rev_cat_tspr', period)
        rev_cat_rvcm = simulation.calculate('rev_cat_rvcm', period)
        rev_cat_rfon = simulation.calculate('rev_cat_rfon', period)
        rev_cat_rpns = simulation.calculate('rev_cat_rpns', period)
        rev_cat_pv = simulation.calculate('rev_cat_pv', period)

        return period, rev_cat_tspr + rev_cat_rvcm + rev_cat_rfon + rev_cat_rpns + rev_cat_pv


###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


class deficit_ante(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Déficit global antérieur"
    url = "http://impotsurlerevenu.org/declaration-de-revenus-fonciers-2044/796-deficits-anterieurs-restant-a-imputer-cadre-450.php"

    def function(self, simulation, period):
        '''
        Déficits antérieurs
        '''
        period = period.this_year
        f6fa = simulation.calculate('f6fa', period)
        f6fb = simulation.calculate('f6fb', period)
        f6fc = simulation.calculate('f6fc', period)
        f6fd = simulation.calculate('f6fd', period)
        f6fe = simulation.calculate('f6fe', period)
        f6fl = simulation.calculate('f6fl', period)

        return period, f6fa + f6fb + f6fc + f6fd + f6fe + f6fl


class rbg(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu brut global"
    url = "http://www.documentissime.fr/dossiers-droit-pratique/dossier-19-l-impot-sur-le-revenu-les-modalites-generales-d-imposition/la-determination-du-revenu-imposable/le-revenu-brut-global.html"

    def function(self, simulation, period):
        '''Revenu brut global
        '''
        period = period.this_year
        rev_cat = simulation.calculate('rev_cat', period)
        deficit_ante = simulation.calculate('deficit_ante', period)
        f6gh = simulation.calculate('f6gh', period)
        nbic_impm_holder = simulation.compute('nbic_impm', period)
        nacc_pvce_holder = simulation.compute('nacc_pvce', period)
        cga = simulation.legislation_at(period.start).ir.rpns.cga_taux2

        # (Total 17)
        # sans les revenus au quotient
        nacc_pvce = self.sum_by_entity(nacc_pvce_holder)
        return period, max_(0,
                    rev_cat + f6gh + (self.sum_by_entity(nbic_impm_holder) + nacc_pvce) * (1 + cga) - deficit_ante)


class csg_deduc_patrimoine(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Csg déductible sur le patrimoine"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS"

    def function(self, simulation, period):
        '''
        CSG déductible sur les revenus du patrimoine
        http://bofip.impots.gouv.fr/bofip/887-PGP
        '''
        period = period.this_year
        f6de = simulation.calculate('f6de', period)

        return period, max_(f6de, 0)


class csg_deduc_patrimoine_simulated(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Csg déductible sur le patrimoine simulée"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS"

    def function(self, simulation, period):
        '''
        Cette fonction simule le montant mentionné dans la case f6de de la déclaration 2042
        http://bofip.impots.gouv.fr/bofip/887-PGP
        '''
        period = period.this_year
        rev_cat_rfon = simulation.calculate('rev_cat_rfon', period)
        rev_cap_bar = simulation.calculate('rev_cap_bar', period)
        retraite_titre_onereux = simulation.calculate('retraite_titre_onereux', period)
        taux = simulation.legislation_at(period.start).csg.capital.deduc

        patrimoine_deduc = rev_cat_rfon + rev_cap_bar + retraite_titre_onereux
        return period, taux * patrimoine_deduc


class csg_deduc(Variable):  # f6de
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Csg déductible sur le patrimoine"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS"

    def function(self, simulation, period):
        ''' CSG déductible '''
        period = period.this_year
        rbg = simulation.calculate('rbg', period)
        csg_deduc_patrimoine = simulation.calculate('csg_deduc_patrimoine', period)

        # min_(f6de, max_(rbg, 0))
        return period, min_(csg_deduc_patrimoine, max_(rbg, 0))


class rng(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu net global"
    url = "http://impotsurlerevenu.org/definitions/114-revenu-net-global.php"

    def function(self, simulation, period):
        ''' Revenu net global (total 20) '''
        period = period.this_year
        rbg = simulation.calculate('rbg', period)
        csg_deduc = simulation.calculate('csg_deduc', period)
        charges_deduc = simulation.calculate('charges_deduc', period)

        return period, max_(0, rbg - csg_deduc - charges_deduc)


class rni(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu net imposable"
    url = "http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php"

    def function(self, simulation, period):
        ''' Revenu net imposable ou déficit à reporter'''
        period = period.this_year
        rng = simulation.calculate('rng', period)
        abat_spe = simulation.calculate('abat_spe', period)

        return period, rng - abat_spe


class ir_brut(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt sur le revenu brut avant non imposabilité et plafonnement du quotient"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        nbptr = simulation.calculate('nbptr', period)
        taux_effectif = simulation.calculate('taux_effectif', period)
        rni = simulation.calculate('rni', period)
        bareme = simulation.legislation_at(period.start).ir.bareme

        return period, (taux_effectif == 0) * nbptr * bareme.calc(rni / nbptr) + taux_effectif * rni


class ir_ss_qf(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt sans quotient familial"

    def function(self, simulation, period):
        '''
        Impôt sans quotient familial
        '''
        period = period.this_year
        rni = simulation.calculate('rni', period)
        nb_adult = simulation.calculate('nb_adult', period)
        bareme = simulation.legislation_at(period.start).ir.bareme

        A = bareme.calc(rni / nb_adult)
        return period, nb_adult * A


class ir_plaf_qf(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt après plafonnement du quotient familial et réduction complémentaire"

    def function(self, simulation, period):
        '''
        Impôt après plafonnement du quotient familial et réduction complémentaire
        '''
        period = period.this_year
        ir_brut = simulation.calculate('ir_brut', period)
        ir_ss_qf = simulation.calculate('ir_ss_qf', period)
        nb_adult = simulation.calculate('nb_adult', period)
        nb_pac = simulation.calculate('nb_pac', period)
        nbptr = simulation.calculate('nbptr', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        veuf = simulation.calculate('veuf', period)
        jeune_veuf = simulation.calculate('jeune_veuf', period)
        celibataire_ou_divorce = simulation.calculate('celibataire_ou_divorce', period)
        caseE = simulation.calculate('caseE', period)
        caseF = simulation.calculate('caseF', period)
        caseG = simulation.calculate('caseG', period)
        caseH = simulation.calculate('caseH', period)
        caseK = simulation.calculate('caseK', period)
        caseN = simulation.calculate('caseN', period)
        caseP = simulation.calculate('caseP', period)
        caseS = simulation.calculate('caseS', period)
        caseT = simulation.calculate('caseT', period)
        caseW = simulation.calculate('caseW', period)
        nbF = simulation.calculate('nbF', period)
        nbG = simulation.calculate('nbG', period)
        nbH = simulation.calculate('nbH', period)
        nbI = simulation.calculate('nbI', period)
        nbR = simulation.calculate('nbR', period)
        plafond_qf = simulation.legislation_at(period.start).ir.plafond_qf

        A = ir_ss_qf
        I = ir_brut

        aa0 = (nbptr - nb_adult) * 2  # nombre de demi part excédant nbadult
        # on dirait que les impôts font une erreur sur aa1 (je suis obligé de
        # diviser par 2)
        aa1 = min_((nbptr - 1) * 2, 2) / 2  # deux première demi part excédants une part
        aa2 = max_((nbptr - 2) * 2, 0)  # nombre de demi part restantes
        # celibataire_ou_divorce parents isolés
        condition61 = celibataire_ou_divorce & caseT
        B1 = plafond_qf.celib_enf * aa1 + plafond_qf.maries_ou_pacses * aa2
        # tous les autres
        B2 = plafond_qf.maries_ou_pacses * aa0  # si autre
        # celibataire_ou_divorce, veufs (non jeune_veuf) vivants seuls et autres conditions

        # TODO: année en dur... pour caseH
        condition63 = (celibataire_ou_divorce | (veuf & not_(jeune_veuf))) & not_(caseN) & (nb_pac == 0) & (caseK | caseE) & (caseH < 1981)
        B3 = plafond_qf.celib

        B = B1 * condition61 + \
            B2 * (not_(condition61 | condition63)) + \
            B3 * (condition63 & not_(condition61))
        C = max_(0, A - B)
        # Impôt après plafonnement
        IP0 = max_(I, C)

        # 6.2 réduction d'impôt pratiquée sur l'impot après plafonnement et le cas particulier des DOM
        # pas de réduction complémentaire
        condition62a = (I >= C)
        # réduction complémentaire
        condition62b = (I < C)
        # celibataire_ou_divorce veuf
        condition62caa0 = (celibataire_ou_divorce | (veuf & not_(jeune_veuf)))
        condition62caa1 = (nb_pac == 0) & (caseP | caseG | caseF | caseW)
        condition62caa2 = caseP & ((nbF - nbG > 0) | (nbH - nbI > 0))
        condition62caa3 = not_(caseN) & (caseE | caseK) & (caseH >= 1981)
        condition62caa = condition62caa0 & (condition62caa1 | condition62caa2 | condition62caa3)
        # marié pacs
        condition62cab = (maries_ou_pacses | jeune_veuf) & caseS & not_(caseP | caseF)

        condition62ca = (condition62caa | condition62cab)

        # plus de 590 euros si on a des plus de
        condition62cb = ((nbG + nbR + nbI) > 0) | caseP | caseF
        D = plafond_qf.reduc_postplafond * (condition62ca + ~condition62ca * condition62cb * (
            1 * caseP + 1 * caseF + nbG + nbR + nbI / 2))

        E = max_(0, A - I - B)
        Fo = D * (D <= E) + E * (E < D)
        IP1 = IP0 - Fo

        # TODO: 6.3 Cas particulier: Contribuables domiciliés dans les DOM.
        # conditionGuadMarReu =
        # conditionGuyane=
        # conitionDOM = conditionGuadMarReu | conditionGuyane
        # postplafGuadMarReu = 5100
        # postplafGuyane = 6700
        # IP2 = IP1 - conditionGuadMarReu*min( postplafGuadMarReu,.3*IP1)  - conditionGuyane*min(postplafGuyane,.4*IP1)

        # Récapitulatif

        return period, condition62a * IP0 + condition62b * IP1  # IP2 si DOM


class avantage_qf(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Avantage quotient familial"

    def function(self, simulation, period):
        period = period.this_year
        ir_ss_qf = simulation.calculate('ir_ss_qf', period)
        ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)

        return period, ir_ss_qf - ir_plaf_qf


class decote(DatedVariable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"décote"

    @dated_function(start = date(2015, 1, 1))
    def function_2015(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
        nb_adult = simulation.calculate('nb_adult', period)
        decote_seuil_celib = simulation.legislation_at(period.start).ir.decote.seuil_celib
        decote_seuil_couple = simulation.legislation_at(period.start).ir.decote.seuil_couple
        decote_celib = (ir_plaf_qf < 4 / 3 * decote_seuil_celib) * (decote_seuil_celib - 3 / 4 * ir_plaf_qf)
        decote_couple = (ir_plaf_qf < 4 / 3 * decote_seuil_couple) * (decote_seuil_couple - 3 / 4 * ir_plaf_qf)

        return period, (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        period = period.this_year
        ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
        nb_adult = simulation.calculate('nb_adult', period)
        decote_seuil_celib = simulation.legislation_at(period.start).ir.decote.seuil_celib
        decote_seuil_couple = simulation.legislation_at(period.start).ir.decote.seuil_couple
        decote_celib = (ir_plaf_qf < decote_seuil_celib) * (decote_seuil_celib - ir_plaf_qf)
        decote_couple = (ir_plaf_qf < decote_seuil_couple) * (decote_seuil_couple - ir_plaf_qf)

        return period, (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    @dated_function(start = date(2001, 1, 1), stop = date(2013, 12, 31))
    def function_2001_2013(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
        decote = simulation.legislation_at(period.start).ir.decote

        return period, (ir_plaf_qf < decote.seuil) * (decote.seuil - ir_plaf_qf) * 0.5


class decote_gain_fiscal(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Gain fiscal de la décote/Décote au sens Dgfip tel que sur la feuille d'impôt"
    start_date = date(1982, 1, 1)

    def function(self, simulation, period):
        '''
        Renvoie le gain fiscal du à la décote
        '''
        period = period.this_year
        decote = simulation.calculate('decote', period)
        ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)

        return period, min_(decote, ir_plaf_qf)


class nat_imp(Variable):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"nat_imp"

    def function(self, simulation, period):
        '''
        Renvoie True si le foyer est imposable, False sinon
        '''
        period = period.this_year
        iai = simulation.calculate('iai', period)
        credits_impot = simulation.calculate('credits_impot', period)
        cehr = simulation.calculate('cehr', period)

        # def _nat_imp(rni, nbptr, non_imposable = law.ir.non_imposable):
        # seuil = non_imposable.seuil + (nbptr - 1)*non_imposable.supp
        return period, (iai - credits_impot + cehr) > 0


class ip_net(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt sur le revenu après décote"

    def function(self, simulation, period):
        '''
        irpp après décote
        '''
        period = period.this_year
        ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
        cncn_info_holder = simulation.compute('cncn_info', period)
        decote = simulation.calculate('decote', period)
        taux = simulation.legislation_at(period.start).ir.rpns.taux16

        return period, max_(0, ir_plaf_qf + self.sum_by_entity(cncn_info_holder) * taux - decote)


class iaidrdi(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt après imputation des réductions d'impôt"

    def function(self, simulation, period):
        '''
        Impôt après imputation des réductions d'impôt
        '''
        period = period.this_year
        ip_net = simulation.calculate('ip_net', period)
        reductions = simulation.calculate('reductions', period)

        return period, ip_net - reductions


class cont_rev_loc(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Contribution sur les revenus locatifs"
    start_date = date(2001, 1, 1)

    def function(self, simulation, period):
        '''
        Contribution sur les revenus locatifs
        '''
        period = period.this_year
        f4bl = simulation.calculate('f4bl', period)
        crl = simulation.legislation_at(period.start).ir.crl

        return period, round(crl.taux * (f4bl >= crl.seuil) * f4bl)


class teicaa(Variable):  # f5rm
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance"

    def function(self, simulation, period):
        """
        Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance
        """
        period = period.this_year
        f5qm_holder = simulation.compute('f5qm', period)
        bareme = simulation.legislation_at(period.start).ir.teicaa

        f5qm = self.filter_role(f5qm_holder, role = VOUS)
        f5rm = self.filter_role(f5qm_holder, role = CONJ)

        return period, bareme.calc(f5qm) + bareme.calc(f5rm)


class assiette_vente(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Assiette régime microsociale pour les ventes"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        '''
        Assiette régime microsociale pour les ventes
        '''
        period = period.this_year
        ebic_impv_holder = simulation.compute('ebic_impv', period)

        return period, self.sum_by_entity(ebic_impv_holder)


class assiette_service(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Assiette régime microsociale pour les prestations et services"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        '''
        Assiette régime microsociale pour les prestations et services
        '''
        period = period.this_year
        ebic_imps_holder = simulation.compute('ebic_imps', period)

        return period, self.sum_by_entity(ebic_imps_holder)

    # P = _P.ir.rpns.microentreprise
    # assert (ebic_imps <= P.servi.max)


class assiette_proflib(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Assiette régime microsociale pour les professions libérales"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        '''
        Assiette régime microsociale pour les professions libérales
        '''
        period = period.this_year
        ebnc_impo_holder = simulation.compute('ebnc_impo', period)
        P = simulation.legislation_at(period.start).ir.rpns.microentreprise

        # TODO: distinction RSI/CIPAV (pour les cotisations sociales)
        # http://vosdroits.service-public.fr/professionnels-entreprises/F23267.xhtml
        return period, self.sum_by_entity(ebnc_impo_holder)

    # assert (ebnc_impo <= P.specialbnc.max)


class microsocial(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Assiette régime microsociale totale"
    start_date = date(2009, 1, 1)
    url = "http://fr.wikipedia.org/wiki/R%C3%A9gime_micro-social"

    def function(self, simulation, period):
        period = period.this_year
        assiette_service = simulation.calculate('assiette_service', period)
        assiette_vente = simulation.calculate('assiette_vente', period)
        assiette_proflib = simulation.calculate('assiette_proflib', period)
        microsocial = simulation.legislation_at(period.start).ir.rpns.microsocial

        return period, (
            assiette_service * microsocial.servi +
            assiette_vente * microsocial.vente + assiette_proflib * microsocial.bnc
            )


class microentreprise(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"microentreprise"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        period = period.this_year
        ebnc_impo_holder = simulation.compute('ebnc_impo', period)
        ebic_imps_holder = simulation.compute('ebic_imps', period)
        ebic_impv_holder = simulation.compute('ebic_impv', period)
        me = simulation.legislation_at(period.start).ir.rpns.microentreprise

        ebnc_impo = self.sum_by_entity(ebnc_impo_holder)
        ebic_imps = self.sum_by_entity(ebic_imps_holder)
        ebic_impv = self.sum_by_entity(ebic_impv_holder)
        return period, (
            ebnc_impo * (1 - me.specialbnc.taux) + ebic_imps * (1 - me.servi.taux) + ebic_impv * (1 - me.vente.taux)
            )


class plus_values(DatedVariable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Taxation des plus_values"

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_20070101_20071231(self, simulation, period):  # f3sd is in f3vd holder
        """
        Taxation des plus values
        TODO: 2013 f3Vg au barème / tout refaire
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        f3vh = simulation.calculate('f3vh', period)
        f3vl = simulation.calculate('f3vl', period)
        f3vm = simulation.calculate('f3vm', period)
        f3vi_holder = simulation.compute('f3vi', period)
        f3vf_holder = simulation.compute('f3vf', period)
        f3vd_holder = simulation.compute('f3vd', period)
        rpns_pvce_holder = simulation.compute('rpns_pvce', period)
        _P = simulation.legislation_at(period.start)
        plus_values = simulation.legislation_at(period.start).ir.plus_values

        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        #  TODO: remove this todo use sum for all fields after checking
            # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)

        return period, round(out)

    @dated_function(start = date(2008, 1, 1), stop = date(2011, 12, 31))
    def function_20080101_20111231(self, simulation, period):  # f3sd is in f3vd holder
        """
        Taxation des plus value
        TODO:  2013 f3Vg au barème / tout refaire
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        f3vh = simulation.calculate('f3vh', period)
        f3vl = simulation.calculate('f3vl', period)
        f3vm = simulation.calculate('f3vm', period)
        f3vi_holder = simulation.compute('f3vi', period)
        f3vf_holder = simulation.compute('f3vf', period)
        f3vd_holder = simulation.compute('f3vd', period)
        rpns_pvce_holder = simulation.compute('rpns_pvce', period)
        plus_values = simulation.legislation_at(period.start).ir.plus_values

        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        #  TODO: remove this todo use sum for all fields after checking
            # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)
            # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += plus_values.taux1 * f3vd

        return period, round(out)

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_20120101_20121231(self, simulation, period):  # f3sd is in f3vd holder
        """
        Taxation des plus value
        TODO: 2013 f3Vg au barème / tout refaire
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        f3vh = simulation.calculate('f3vh', period)
        f3vl = simulation.calculate('f3vl', period)
        f3vt = simulation.calculate('f3vt', period)
        f3vm = simulation.calculate('f3vm', period)
        f3vi_holder = simulation.compute('f3vi', period)
        f3vf_holder = simulation.compute('f3vf', period)
        f3vd_holder = simulation.compute('f3vd', period)
        rpns_pvce_holder = simulation.compute('rpns_pvce', period)
        plus_values = simulation.legislation_at(period.start).ir.plus_values

        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        # TODO: remove this todo use sum for all fields after checking
        # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.pea2 * f3vt +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)
        # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += plus_values.taux1 * f3vd
    #        out = plus_values.taux2 * f3vd + plus_values.taux3 * f3vi + plus_values.taux4 * f3vf + plus_values.taux1 *max_(
    #            0, f3vg - f3vh)
        out = (plus_values.taux2 * (f3vd + f3sd) + plus_values.taux3 * (f3vi + f3si) +
            plus_values.taux4 * (f3vf + f3sf) + plus_values.taux1 * max_(0, f3vg - f3vh) + plus_values.pvce * rpns_pvce)
                # TODO: chek this rpns missing ?
        return period, round(out)

    @dated_function(start = date(2013, 1, 1))
    def function_20130101_20151231(self, simulation, period):  # f3sd is in f3vd holder
        """
        Taxation des plus value
        TODO: 2013 f3Vg au barème / tout refaire
        """
        period = period.this_year
        f3vg = simulation.calculate('f3vg', period)
        f3vh = simulation.calculate('f3vh', period)
        f3vl = simulation.calculate('f3vl', period)
        f3vm = simulation.calculate('f3vm', period)
        f3vt = simulation.calculate('f3vt', period)
        f3vi_holder = simulation.compute('f3vi', period)
        f3vf_holder = simulation.compute('f3vf', period)
        f3vd_holder = simulation.compute('f3vd', period)
        f3sa = simulation.calculate('f3sa', period)
        rpns_pvce_holder = simulation.compute('rpns_pvce', period)
        _P = simulation.legislation_at(period.start)
        plus_values = simulation.legislation_at(period.start).ir.plus_values

        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        f3vd = self.filter_role(f3vd_holder, role = VOUS)
        f3sd = self.filter_role(f3vd_holder, role = CONJ)
        f3vi = self.filter_role(f3vi_holder, role = VOUS)
        f3si = self.filter_role(f3vi_holder, role = CONJ)
        f3vf = self.filter_role(f3vf_holder, role = VOUS)
        f3sf = self.filter_role(f3vf_holder, role = CONJ)
        #  TODO: remove this todo use sum for all fields after checking
        # revenus taxés à un taux proportionnel
        rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
        out = (plus_values.pvce * rpns_pvce +
               plus_values.taux1 * max_(0, f3vg - f3vh) +
               plus_values.caprisque * f3vl +
               plus_values.pea * f3vm +
               plus_values.pea2 * f3vt +
               plus_values.taux3 * f3vi +
               plus_values.taux4 * f3vf)

        # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += plus_values.taux1 * f3vd
        #  out = plus_values.taux2 * f3vd + plus_values.taux3 * f3vi + plus_values.taux4 * f3vf + plus_values.taux1 * max_(
        #          0, f3vg - f3vh)
        out = (plus_values.taux2 * (f3vd + f3sd) + plus_values.taux3 * (f3vi + f3si) +
            plus_values.taux4 * (f3vf + f3sf) + plus_values.taux1 * max_(0, - f3vh) + plus_values.pvce * (rpns_pvce + f3sa))
        # TODO: chek this 3VG
        return period, round(out)


class iai(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt avant imputations de l'impôt sur le revenu"
    url = "http://forum-juridique.net-iris.fr/finances-fiscalite-assurance/43963-declaration-impots.html"

    def function(self, simulation, period):
        '''
        impôt avant imputation de l'irpp
        '''
        period = period.this_year
        iaidrdi = simulation.calculate('iaidrdi', period)
        plus_values = simulation.calculate('plus_values', period)
        cont_rev_loc = simulation.calculate('cont_rev_loc', period)
        teicaa = simulation.calculate('teicaa', period)

        return period, iaidrdi + plus_values + cont_rev_loc + teicaa


class cehr(DatedVariable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Contribution exceptionnelle sur les hauts revenus"
    url = "http://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006069577&idSectionTA=LEGISCTA000025049019"

    @dated_function(start = date(2011, 1, 1))
    def function(self, simulation, period):
        '''
        Contribution exceptionnelle sur les hauts revenus
        'foy'
        '''
        period = period.this_year
        rfr = simulation.calculate('rfr', period)
        nb_adult = simulation.calculate('nb_adult', period)
        bareme = simulation.legislation_at(period.start).ir.cehr

        return period, bareme.calc(rfr / nb_adult) * nb_adult
        # TODO: Gérer le II.-1 du lissage interannuel ? (problème de non recours)


class irpp(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Impôt sur le revenu des personnes physiques"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_impot_revenu&espId=1&impot=IR&sfid=50"

    def function(self, simulation, period):
        '''
        Montant après seuil de recouvrement (hors ppe)
        '''
        period = period.this_year
        iai = simulation.calculate('iai', period)
        credits_impot = simulation.calculate('credits_impot', period)
        cehr = simulation.calculate('cehr', period)
        P = simulation.legislation_at(period.start).ir.recouvrement

        pre_result = iai - credits_impot + cehr
        return period, (
            (iai > P.seuil) * (
                (pre_result < P.min) * (pre_result > 0) * iai * 0 +
                ((pre_result <= 0) + (pre_result >= P.min)) * (- pre_result)
                ) +
            (iai <= P.seuil) * (
                (pre_result < 0) * (-pre_result) + (pre_result >= 0) * 0 * iai)
            )


class foyer_impose(Variable):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"Le foyer fiscal est imposé"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        irpp = simulation.calculate('irpp', period)
        return period, (irpp < 0)

###############################################################################
# # Autres totaux utiles pour la suite
###############################################################################


class pensions_alimentaires_versees(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Pensions alimentaires versées"
    url = u"http://vosdroits.service-public.fr/particuliers/F2.xhtml"

    def function(self, simulation, period):
        period = period.this_year
        f6gi = simulation.calculate('f6gi', period)
        f6gj = simulation.calculate('f6gj', period)
        f6el = simulation.calculate('f6el', period)
        f6em = simulation.calculate('f6em', period)
        f6gp = simulation.calculate('f6gp', period)
        f6gu = simulation.calculate('f6gu', period)

        return period, -(f6gi + f6gj + f6el + f6em + f6gp + f6gu)


class pensions_alimentaires_versees_declarant1(EntityToPersonColumn):
    entity_class = Individus
    label = u"Pensions alimentaires versées (pour le premier déclarant du foyer fiscal)"
    role = VOUS
    variable = pensions_alimentaires_versees


class rfr(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu fiscal de référence"

    def function(self, simulation, period):
        '''
        Revenu fiscal de référence
        f3vg -> rev_cat_pv -> ... -> rni
        '''
        period = period.this_year
        rni = simulation.calculate('rni', period)
        f3va_holder = simulation.compute('f3va', period)
        f3vi_holder = simulation.compute('f3vi', period)
        rfr_cd = simulation.calculate('rfr_cd', period)
        rfr_rvcm = simulation.calculate('rfr_rvcm', period)
        rpns_exon_holder = simulation.compute('rpns_exon', period)
        rpns_pvce_holder = simulation.compute('rpns_pvce', period)
        rev_cap_lib = simulation.calculate_add('rev_cap_lib', period)
        f3vz = simulation.calculate('f3vz', period)
        microentreprise = simulation.calculate('microentreprise', period)

        f3va = self.sum_by_entity(f3va_holder)
        f3vi = self.sum_by_entity(f3vi_holder)
        rpns_exon = self.sum_by_entity(rpns_exon_holder)
        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
        return period, (max_(0, rni) + rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va +
                f3vz + microentreprise)


class glo(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Gain de levée d'options"
    url = "http://www.officeo.fr/imposition-au-bareme-progressif-de-l-impot-sur-le-revenu-des-gains-de-levee-d-options-sur-actions-et-attributions-d-actions-gratuites"

    def function(self, simulation, period):
        '''
        Gains de levée d'option
        '''
        period = period.this_year
        f1tv = simulation.calculate('f1tv', period)
        f1tw = simulation.calculate('f1tw', period)
        f1tx = simulation.calculate('f1tx', period)
        f3vf = simulation.calculate('f3vf', period)
        f3vi = simulation.calculate('f3vi', period)
        f3vj = simulation.calculate('f3vj', period)

        return period, f1tv + f1tw + f1tx + f3vf + f3vi + f3vj


class rev_cap_bar(Variable):
    """Revenus du capital imposés au barème

    Annuel pour les impôts mais mensuel pour la base ressource des minimas sociaux donc mensuel.
    """
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenus du capital imposés au barème"
    set_input = set_input_divide_by_period
    url = "http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"

    def function(self, simulation, period):
        period = period.this_month
        year = period.this_year
        f2dc = simulation.calculate('f2dc', year)
        f2gr = simulation.calculate('f2gr', year)
        f2ch = simulation.calculate('f2ch', year)
        f2ts = simulation.calculate('f2ts', year)
        f2go = simulation.calculate('f2go', year)
        f2tr = simulation.calculate('f2tr', year)
        f2fu = simulation.calculate('f2fu', year)
        avf = simulation.calculate('avf', year)
        f2da = simulation.calculate('f2da', year)
        f2ee = simulation.calculate('f2ee', year)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl  # TODO remove ad check case
        majGO = simulation.legislation_at(period.start).ir.rvcm.majGO

        # year = period.start.year
        # if year <= 2011:
        #     return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf
        # elif year > 2011:
        #     return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf + (f2da + f2ee)
        return period, (f2dc + f2gr + f2ch + f2ts + f2go * majGO + f2tr + f2fu - avf + (f2da + f2ee) * finpfl) / 12


    # We add f2da an f2ee to allow for comparaison between years


class rev_cap_lib(DatedVariable):
    '''Revenu du capital imposé au prélèvement libératoire

    Annuel pour les impôts mais mensuel pour la base ressource des minimas sociaux donc mensuel.
    '''
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenu du capital imposé au prélèvement libératoire"
    set_input = set_input_divide_by_period
    url = "http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"

    @dated_function(start = date(2002, 1, 1), stop = date(2007, 12, 31))
    def function_20020101_20071231(self, simulation, period):
        period = period.this_month
        year = period.this_year
        f2dh = simulation.calculate('f2dh', year)
        f2ee = simulation.calculate('f2ee', year)
        _P = simulation.legislation_at(period.start)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl

        out = f2dh + f2ee
        return period, out * not_(finpfl) / 12

    @dated_function(start = date(2008, 1, 1))
    def function_20080101_20151231(self, simulation, period):
        period = period.this_month
        year = period.this_year
        f2da = simulation.calculate('f2da', year)
        f2dh = simulation.calculate('f2dh', year)
        f2ee = simulation.calculate('f2ee', year)
        _P = simulation.legislation_at(period.start)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl

        out = f2da + f2dh + f2ee
        return period, out * not_(finpfl) / 12


class avf(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Avoir fiscal et crédits d'impôt"

    def function(self, simulation, period):
        '''
        Avoir fiscal et crédits d'impôt (zavff)
        '''
        period = period.this_year
        f2ab = simulation.calculate('f2ab', period)

        return period, f2ab


class imp_lib(DatedVariable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Prelèvement libératoire sur les revenus du capital"
    url = "http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"

    @dated_function(start = date(2002, 1, 1), stop = date(2007, 12, 31))
    def function_20020101_20071231(self, simulation, period):
        '''
        Prelèvement libératoire sur les revenus du capital
        '''
        period = period.this_year
        f2dh = simulation.calculate('f2dh', period)
        f2ee = simulation.calculate('f2ee', period)
        _P = simulation.legislation_at(period.start)
        prelevement_liberatoire = simulation.legislation_at(period.start).ir.rvcm.prelevement_liberatoire

        out = -(prelevement_liberatoire.assvie * f2dh + prelevement_liberatoire.autre * f2ee)
        return period, out

    @dated_function(start = date(2008, 1, 1), stop = date(2012, 12, 31))
    def function_20080101_20121231(self, simulation, period):
        '''
        Prelèvement libératoire sur les revenus du capital
        '''
        period = period.this_year
        f2da = simulation.calculate('f2da', period)
        f2dh = simulation.calculate('f2dh', period)
        f2ee = simulation.calculate('f2ee', period)
        _P = simulation.legislation_at(period.start)
        finpfl = simulation.legislation_at(period.start).ir.autre.finpfl
        prelevement_liberatoire = simulation.legislation_at(period.start).ir.rvcm.prelevement_liberatoire

        out = -(prelevement_liberatoire.action * f2da + prelevement_liberatoire.autre * f2ee) * not_(finpfl) \
            - prelevement_liberatoire.assvie * f2dh
        return period, out


class fon(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Revenus fonciers"
    url = "http://impotsurlerevenu.org/definitions/220-revenu-foncier.php"

    def function(self, simulation, period):
        '''
        Revenus fonciers
        '''
        period = period.this_year
        f4ba = simulation.calculate('f4ba', period)
        f4bb = simulation.calculate('f4bb', period)
        f4bc = simulation.calculate('f4bc', period)
        f4bd = simulation.calculate('f4bd', period)
        f4be = simulation.calculate('f4be', period)
        microfoncier = simulation.legislation_at(period.start).ir.microfoncier

        return period, f4ba - f4bb - f4bc + round(f4be * (1 - microfoncier.taux))


class rpns_pvce(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Plus values de cession - Revenu des professions non salariées"

    def function(self, simulation, period):
        '''
        Plus values de cession
        'ind'
        frag_pvce (f5hx, f5ix, f5jx)
        arag_pvce (f5he, f5ie, f5je)
        mbic_pvce (f5kq, f5lq, f5mq)
        abic_pvce (f5ke, f5le, f5me)
        macc_pvce (f5nq, f5oq, f5pq)
        aacc_pvce (f5ne, f5oe, f5pe)
        mncn_pvce (f5kv, f5lv, f5mv)
        cncn_pvce (f5so, f5nt, f5ot)
        mbnc_pvce (f5hr, f5ir, f5jr)
        abnc_pvce (f5qd, f5rd, f5sd)
        '''
        period = period.this_year
        frag_pvce = simulation.calculate('frag_pvce', period)
        arag_pvce = simulation.calculate('arag_pvce', period)
        mbic_pvce = simulation.calculate('mbic_pvce', period)
        abic_pvce = simulation.calculate('abic_pvce', period)
        macc_pvce = simulation.calculate('macc_pvce', period)
        aacc_pvce = simulation.calculate('aacc_pvce', period)
        mbnc_pvce = simulation.calculate('mbnc_pvce', period)
        abnc_pvce = simulation.calculate('abnc_pvce', period)
        mncn_pvce = simulation.calculate('mncn_pvce', period)
        cncn_pvce = simulation.calculate('cncn_pvce', period)

        return period, (frag_pvce + arag_pvce + mbic_pvce + abic_pvce + macc_pvce + aacc_pvce + mbnc_pvce +
                abnc_pvce + mncn_pvce + cncn_pvce)


class rpns_exon(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Plus values de cession exonérées -Revenu des professions non salariées"

    def function(self, simulation, period):
        '''
        Plus values de cession
        'ind'
        frag_exon (f5hn, f5in, f5jn)
        arag_exon (f5hb, f5ib, f5jb)
        nrag_exon (f5hh, f5ih, f5jh)
        mbic_exon (f5kn, f5ln, f5mn)
        abic_exon (f5kb, f5lb, f5mb)
        nbic_exon (f5kh, f5lh, f5mh)
        macc_exon (f5nn, f5on, f5pn)
        aacc_exon (f5nb, f5ob, f5pb)
        nacc_exon (f5nh, f5oh, f5ph)
        mbnc_exon (f5hp, f5ip, f5jp)
        abnc_exon (f5qb, f5rb, f5sb)
        nbnc_exon (f5qh, f5rh, f5sh)
        nbnc_pvce (f5qj, f5rj, f5sj)
        '''
        period = period.this_year
        frag_exon = simulation.calculate('frag_exon', period)
        arag_exon = simulation.calculate('arag_exon', period)
        nrag_exon = simulation.calculate('nrag_exon', period)
        mbic_exon = simulation.calculate('mbic_exon', period)
        abic_exon = simulation.calculate('abic_exon', period)
        nbnc_proc = simulation.calculate('nbnc_proc', period)
        nbic_exon = simulation.calculate('nbic_exon', period)
        macc_exon = simulation.calculate('macc_exon', period)
        aacc_exon = simulation.calculate('aacc_exon', period)
        nacc_exon = simulation.calculate('nacc_exon', period)
        mbnc_exon = simulation.calculate('mbnc_exon', period)
        abnc_proc = simulation.calculate('abnc_proc', period)
        nrag_pvce = simulation.calculate('nrag_pvce', period)
        abnc_exon = simulation.calculate('abnc_exon', period)
        nbnc_exon = simulation.calculate('nbnc_exon', period)
        mncn_exon = simulation.calculate('mncn_exon', period)
        cncn_exon = simulation.calculate('cncn_exon', period)
        cncn_jcre = simulation.calculate('cncn_jcre', period)
        cncn_info = simulation.calculate('cncn_info', period)
        nbic_pvce = simulation.calculate('nbic_pvce', period)
        cga = simulation.legislation_at(period.start).ir.rpns.cga_taux2

        return period, (frag_exon + arag_exon + nrag_exon + mbic_exon + abic_exon + nbnc_proc * (1 + cga) +
                nbic_exon + macc_exon + aacc_exon + nacc_exon + mbnc_exon + abnc_proc +
                abnc_exon + nbnc_exon + mncn_exon + cncn_exon + cncn_jcre + cncn_info + nbic_pvce + nrag_pvce)


class defrag(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Déficit agricole des années antérieures"

    def function(self, simulation, period):
        period = period.this_year
        f5qf = simulation.calculate('f5qf', period)
        f5qg = simulation.calculate('f5qg', period)
        f5qn = simulation.calculate('f5qn', period)
        f5qo = simulation.calculate('f5qo', period)
        f5qp = simulation.calculate('f5qp', period)
        f5qq = simulation.calculate('f5qq', period)
        frag_impo_holder = simulation.compute('frag_impo', period)
        nrag_impg_holder = simulation.compute('nrag_impg', period)
        frag_fore_holder = simulation.compute('frag_fore', period)
        frag_pvct_holder = simulation.compute('frag_pvct', period)
        arag_impg_holder = simulation.compute('arag_impg', period)
        cga = simulation.legislation_at(period.start).ir.rpns.cga_taux2

        frag_fore = self.sum_by_entity(frag_fore_holder)
        frag_impo = self.sum_by_entity(frag_impo_holder)
        arag_impg = self.sum_by_entity(arag_impg_holder)
        nrag_impg = self.sum_by_entity(nrag_impg_holder)
        frag_pvct = self.sum_by_entity(frag_pvct_holder)
        return period, min_(f5qf + f5qg + f5qn + f5qo + f5qp + f5qq, (1 + cga) * (frag_impo + nrag_impg + frag_pvct)
                    + arag_impg + frag_fore)


class defacc(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Déficit industriels et commerciaux non professionnels des années antérieures"

    def function(self, simulation, period):
        period = period.this_year
        f5rn = simulation.calculate('f5rn', period)
        f5ro = simulation.calculate('f5ro', period)
        f5rp = simulation.calculate('f5rp', period)
        f5rq = simulation.calculate('f5rq', period)
        f5rr = simulation.calculate('f5rr', period)
        f5rw = simulation.calculate('f5rw', period)
        macc_impv_holder = simulation.compute('macc_impv', period)
        macc_imps_holder = simulation.compute('macc_imps', period)
        nacc_impn_holder = simulation.compute('nacc_impn', period)
        macc_pvct_holder = simulation.compute('macc_pvct', period)
        aacc_impn_holder = simulation.compute('aacc_impn', period)
        cga = simulation.legislation_at(period.start).ir.rpns.cga_taux2
        microentreprise = simulation.legislation_at(period.start).ir.rpns.microentreprise

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.max, rev), P.min)))

        nacc_impn = self.sum_by_entity(nacc_impn_holder)
        macc_pvct = self.sum_by_entity(macc_pvct_holder)
        macc_impv = self.sum_by_entity(macc_impv_holder)
        macc_imps = self.sum_by_entity(macc_imps_holder)
        aacc_impn = self.sum_by_entity(aacc_impn_holder)
        macc_timp = abat_rpns(macc_impv, microentreprise.vente) + abat_rpns(macc_imps, microentreprise.servi)
        return period, (
            min_(f5rn + f5ro + f5rp + f5rq + f5rr + f5rw, aacc_impn + macc_pvct + macc_timp + (1 + cga) * nacc_impn)
            )


class defncn(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Déficit non commerciaux non professionnels des années antérieures"

    def function(self, simulation, period):
        period = period.this_year
        f5ht = simulation.calculate('f5ht', period)
        f5it = simulation.calculate('f5it', period)
        f5jt = simulation.calculate('f5jt', period)
        f5kt = simulation.calculate('f5kt', period)
        f5lt = simulation.calculate('f5lt', period)
        f5mt = simulation.calculate('f5mt', period)
        mncn_impo_holder = simulation.compute('mncn_impo', period)
        mncn_pvct_holder = simulation.compute('mncn_pvct', period)
        cncn_aimp_holder = simulation.compute('cncn_aimp', period)
        cncn_bene_holder = simulation.compute('cncn_bene', period)
        cga = simulation.legislation_at(period.start).ir.rpns.cga_taux2
        spbnc = simulation.legislation_at(period.start).ir.rpns.microentreprise.specialbnc

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.max, rev), P.min)))
        cncn_bene = self.sum_by_entity(cncn_bene_holder)
        mncn_impo = self.sum_by_entity(mncn_impo_holder)
        mncn_pvct = self.sum_by_entity(mncn_pvct_holder)
        cncn_aimp = self.sum_by_entity(cncn_aimp_holder)
        return period, min_(f5ht + f5it + f5jt + f5kt + f5lt + f5mt, abat_rpns(mncn_impo, spbnc) +
                    mncn_pvct + cncn_aimp + (1 + cga) * cncn_bene)


class defmeu(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Déficit des locations meublées non professionnelles des années antérieures"

    def function(self, simulation, period):
        period = period.this_year
        f5ga = simulation.calculate('f5ga', period)
        f5gb = simulation.calculate('f5gb', period)
        f5gc = simulation.calculate('f5gc', period)
        f5gd = simulation.calculate('f5gd', period)
        f5ge = simulation.calculate('f5ge', period)
        f5gf = simulation.calculate('f5gf', period)
        f5gg = simulation.calculate('f5gg', period)
        f5gh = simulation.calculate('f5gh', period)
        f5gi = simulation.calculate('f5gi', period)
        f5gj = simulation.calculate('f5gj', period)
        alnp_imps_holder = simulation.compute('alnp_imps', period)
        nacc_defs_holder = simulation.compute('nacc_defs', period)

        nacc_defs = self.sum_by_entity(nacc_defs_holder)
        alnp_imps = self.sum_by_entity(alnp_imps_holder)
        return period, min_(f5ga + f5gb + f5gc + f5gd + f5ge + f5gf + f5gg + f5gh + f5gi + f5gj, alnp_imps + nacc_defs)


class rag(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus agricoles"
    url = "http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&impot=BA&pageId=prof_ba&sfid=50"

    def function(self, simulation, period):
        '''
        Revenus agricoles
        'ind'
        frag_exon (f5hn, f5in, f5jn)
        frag_impo (f5ho, f5io, f5jo)
        arag_exon (f5hb, f5ib, f5jb)
        arag_impg (f5hc, f5ic, f5jc)
        arag_defi (f5hf, f5if, f5jf)
        nrag_exon (f5hh, f5ih, f5jh)
        nrag_impg (f5hi, f5ii, f5ji)
        nrag_defi (f5hl, f5il, f5jl)
        nrag_ajag (f5hm, f5im, f5jm)
        '''
        period = period.this_year
        frag_exon = simulation.calculate('frag_exon', period)
        frag_impo = simulation.calculate('frag_impo', period)
        arag_exon = simulation.calculate('arag_exon', period)
        arag_impg = simulation.calculate('arag_impg', period)
        arag_defi = simulation.calculate('arag_defi', period)
        nrag_exon = simulation.calculate('nrag_exon', period)
        nrag_impg = simulation.calculate('nrag_impg', period)
        nrag_defi = simulation.calculate('nrag_defi', period)
        nrag_ajag = simulation.calculate('nrag_ajag', period)

        return period, (frag_exon + frag_impo +
                arag_exon + arag_impg - arag_defi +
                nrag_exon + nrag_impg - nrag_defi +
                nrag_ajag)


class ric(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Bénéfices industriels et commerciaux"
    url = "http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?pageId=prof_bic&espId=2&impot=BIC&sfid=50"

    def function(self, simulation, period):
        '''
        Bénéfices industriels et commerciaux
        'ind'
        mbic_exon (f5kn, f5ln, f5mn)
        abic_exon (f5kb, f5lb, f5mb)
        nbic_exon (f5kh, f5lh, f5mh)
        mbic_impv (f5ko, f5lo, f5mo)
        mbic_imps (f5kp, f5lp, f5mp)
        abic_impn (f5kc, f5lc, f5mc)
        abic_imps (f5kd, f5ld, f5md)
        nbic_impn (f5ki, f5li, f5mi)
        nbic_imps (f5kj, f5lj, f5mj)
        abic_defn (f5kf, f5lf, f5mf)
        abic_defs (f5kg, f5lg, f5mg)
        nbic_defn (f5kl, f5ll, f5ml)
        nbic_defs (f5km, f5lm, f5mm)
        nbic_apch (f5ks, f5ls, f5ms)
        '''
        period = period.this_year
        mbic_exon = simulation.calculate('mbic_exon', period)
        mbic_impv = simulation.calculate('mbic_impv', period)
        mbic_imps = simulation.calculate('mbic_imps', period)
        abic_exon = simulation.calculate('abic_exon', period)
        nbic_exon = simulation.calculate('nbic_exon', period)
        abic_impn = simulation.calculate('abic_impn', period)
        nbic_impn = simulation.calculate('nbic_impn', period)
        abic_imps = simulation.calculate('abic_imps', period)
        nbic_imps = simulation.calculate('nbic_imps', period)
        abic_defn = simulation.calculate('abic_defn', period)
        nbic_defn = simulation.calculate('nbic_defn', period)
        abic_defs = simulation.calculate('abic_defs', period)
        nbic_defs = simulation.calculate('nbic_defs', period)
        nbic_apch = simulation.calculate('nbic_apch', period)
        microentreprise = simulation.legislation_at(period.start).ir.rpns.microentreprise

        zbic = (mbic_exon + mbic_impv + mbic_imps
                + abic_exon + nbic_exon
                + abic_impn + nbic_impn
                + abic_imps + nbic_imps
                - abic_defn - nbic_defn
                - abic_defs - nbic_defs
                + nbic_apch)

        cond = (mbic_impv > 0) & (mbic_imps == 0)
        taux = microentreprise.vente.taux * cond + microentreprise.servi.taux * not_(cond)

        cbic = min_(
            mbic_impv + mbic_imps + mbic_exon,
            max_(
                microentreprise.vente.min,
                round(
                    mbic_impv * microentreprise.vente.taux + mbic_imps * microentreprise.servi.taux + mbic_exon * taux
                    )
                )
            )
        return period, zbic - cbic


class rac(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus accessoires individuels"
    url = "http://vosdroits.service-public.fr/particuliers/F1225.xhtml"

    def function(self, simulation, period):
        '''
        Revenus accessoires individuels
        'ind'
        macc_exon (f5nn, f5on, f5pn)
        aacc_exon (f5nb, f5ob, f5pb)
        nacc_exon (f5nh, f5oh, f5ph)
        macc_impv (f5no, f5oo, f5po)
        macc_imps (f5np, f5op, f5pp)
        aacc_impn (f5nc, f5oc, f5pc)
        aacc_imps (f5nd, f5od, f5pd)
        aacc_defn (f5nf, f5of, f5pf)
        aacc_defs (f5ng, f5og, f5pg)
        nacc_impn (f5ni, f5oi, f5pi)
        nacc_defn (f5nl, f5ol, f5pl)
        nacc_defs (f5nm, f5om, f5pm)
        mncn_impo (f5ku, f5lu, f5mu)
        cncn_bene (f5sn, f5ns, f5os)
        cncn_defi (f5sp, f5nu, f5ou, f5sr)
        f5sv????
        '''
        period = period.this_year
        macc_exon = simulation.calculate('macc_exon', period)
        macc_impv = simulation.calculate('macc_impv', period)
        macc_imps = simulation.calculate('macc_imps', period)
        aacc_exon = simulation.calculate('aacc_exon', period)
        aacc_impn = simulation.calculate('aacc_impn', period)
        aacc_imps = simulation.calculate('aacc_imps', period)
        aacc_defn = simulation.calculate('aacc_defn', period)
        aacc_defs = simulation.calculate('aacc_defs', period)
        nacc_exon = simulation.calculate('nacc_exon', period)
        nacc_impn = simulation.calculate('nacc_impn', period)
        nacc_defn = simulation.calculate('nacc_defn', period)
        nacc_defs = simulation.calculate('nacc_defs', period)
        mncn_impo = simulation.calculate('mncn_impo', period)
        cncn_bene = simulation.calculate('cncn_bene', period)
        cncn_defi = simulation.calculate('cncn_defi', period)
        microentreprise = simulation.legislation_at(period.start).ir.rpns.microentreprise

        zacc = (macc_exon + macc_impv + macc_imps
                + aacc_exon + aacc_impn + aacc_imps - aacc_defn - aacc_defs
                + nacc_exon + nacc_impn - nacc_defn - nacc_defs
                + mncn_impo + cncn_bene - cncn_defi)
    #TODO: aacc_imps aacc_defs
        cond = (macc_impv > 0) & (macc_imps == 0)
        taux = microentreprise.vente.taux * cond + microentreprise.servi.taux * not_(cond)

        cacc = min_(macc_impv + macc_imps + macc_exon + mncn_impo, max_(microentreprise.vente.min, round(
            macc_impv * microentreprise.vente.taux
            + macc_imps * microentreprise.servi.taux + macc_exon * taux
            + mncn_impo * microentreprise.specialbnc.taux)))

        return period, zacc - cacc


class rnc(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus non commerciaux individuels"
    url = "http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&pageId=prof_bnc&impot=BNC&sfid=50"

    def function(self, simulation, period):
        '''
        Revenus non commerciaux individuels
        'ind'
        mbnc_exon (f5hp, f5ip, f5jp)
        abnc_exon (f5qb, f5rb, f5sb)
        nbnc_exon (f5qh, f5rh, f5sh)
        mbnc_impo (f5hq, f5iq, f5jq)
        abnc_impo (f5qc, f5rc, f5sc)
        abnc_defi (f5qe, f5re, f5se)
        nbnc_impo (f5qi, f5ri, f5si)
        nbnc_defi (f5qk, f5rk, f5sk)
        f5ql, f5qm????
        '''
        period = period.this_year
        mbnc_exon = simulation.calculate('mbnc_exon', period)
        mbnc_impo = simulation.calculate('mbnc_impo', period)
        abnc_exon = simulation.calculate('abnc_exon', period)
        nbnc_exon = simulation.calculate('nbnc_exon', period)
        abnc_impo = simulation.calculate('abnc_impo', period)
        nbnc_impo = simulation.calculate('nbnc_impo', period)
        abnc_defi = simulation.calculate('abnc_defi', period)
        nbnc_defi = simulation.calculate('nbnc_defi', period)
        specialbnc = simulation.legislation_at(period.start).ir.rpns.microentreprise.specialbnc

        zbnc = (mbnc_exon + mbnc_impo
                + abnc_exon + nbnc_exon
                + abnc_impo + nbnc_impo
                - abnc_defi - nbnc_defi)

        cbnc = min_(mbnc_exon + mbnc_impo, max_(specialbnc.min, round((mbnc_exon + mbnc_impo) * specialbnc.taux)))

        return period, zbnc - cbnc


class rpns(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus individuels des professions non salariées"

    def function(self, simulation, period):
        period = period.this_year
        rag = simulation.calculate('rag', period)
        ric = simulation.calculate('ric', period)
        rac = simulation.calculate('rac', period)
        rnc = simulation.calculate('rnc', period)

        return period, rag + ric + rac + rnc


class rpns_pvct(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Plus values de court terme -Revenu des professions non salariées"

    def function(self, simulation, period):
        '''
        Plus values de court terme
        'ind'
        frag_pvct (f5hw, f5iw, f5jw)
        mbic_pvct (f5kx, f5lx, f5mx)
        macc_pvct (f5nx, f5ox, f5px)
        mbnc_pvct (f5hv, f5iv, f5jv)
        mncn_pvct (f5ky, f5ly, f5my)
        '''
        period = period.this_year
        frag_pvct = simulation.calculate('frag_pvct', period)
        mbic_pvct = simulation.calculate('mbic_pvct', period)
        macc_pvct = simulation.calculate('macc_pvct', period)
        mbnc_pvct = simulation.calculate('mbnc_pvct', period)
        mncn_pvct = simulation.calculate('mncn_pvct', period)

        return period, frag_pvct + macc_pvct + mbic_pvct + mbnc_pvct + mncn_pvct


class rpns_mvct(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Moins values de court terme - Revenu des professions non salariées"

    def function(self, simulation, period):
        """Moins values de court terme

        'ind'
        macc_mvct (f5iu)
        mncn_mvct (f5ju)
        mbnc_mvct (f5kz)
        """
        period = period.this_year
        macc_mvct_holder = simulation.compute('macc_mvct', period)
        mbnc_mvct = simulation.calculate('mbnc_mvct', period)
        mncn_mvct_holder = simulation.compute('mncn_mvct', period)

        macc_mvct = self.cast_from_entity_to_role(macc_mvct_holder, role = VOUS)
        mncn_mvct = self.cast_from_entity_to_role(mncn_mvct_holder, role = VOUS)
        return period, mbnc_mvct + macc_mvct  # mncn_mvct ?


class rpns_mvlt(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Moins values de long terme - Revenu des professions non salariées"

    def function(self, simulation, period):
        '''
        Moins values de long terme
        'ind'
        mbic_mvlt (f5kr, f5lr, f5mr)
        macc_mvlt (f5nr, f5or, f5pr)
        mncn_mvlt (f5kw, f5lw, f5mw)
        mbnc_mvlt (f5hs, f5is, f5js)
        '''
        period = period.this_year
        mbic_mvlt = simulation.calculate('mbic_mvlt', period)
        macc_mvlt = simulation.calculate('macc_mvlt', period)
        mbnc_mvlt = simulation.calculate('mbnc_mvlt', period)
        mncn_mvlt = simulation.calculate('mncn_mvlt', period)

        return period, mbic_mvlt + macc_mvlt + mbnc_mvlt + mncn_mvlt


class rpns_individu(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenus des professions non salariées individuels"

    def function(self, simulation, period):
        '''
        Revenus des professions non salariées individuels
        '''
        period = period.this_year
        frag_impo = simulation.calculate('frag_impo', period)
        arag_impg = simulation.calculate('arag_impg', period)
        nrag_impg = simulation.calculate('nrag_impg', period)
        arag_defi = simulation.calculate('arag_defi', period)
        nrag_defi = simulation.calculate('nrag_defi', period)
        mbic_impv = simulation.calculate('mbic_impv', period)
        mbic_imps = simulation.calculate('mbic_imps', period)
        abic_impn = simulation.calculate('abic_impn', period)
        abic_imps = simulation.calculate('abic_imps', period)
        abic_defn = simulation.calculate('abic_defn', period)
        abic_defs = simulation.calculate('abic_defs', period)
        nbic_impn = simulation.calculate('nbic_impn', period)
        nbic_imps = simulation.calculate('nbic_imps', period)
        nbic_defn = simulation.calculate('nbic_defn', period)
        nbic_defs = simulation.calculate('nbic_defs', period)
        macc_impv = simulation.calculate('macc_impv', period)
        macc_imps = simulation.calculate('macc_imps', period)
        nbic_mvct = simulation.calculate('nbic_mvct', period)
        aacc_impn = simulation.calculate('aacc_impn', period)
        aacc_defn = simulation.calculate('aacc_defn', period)
        aacc_gits = simulation.calculate('aacc_gits', period)
        nacc_impn = simulation.calculate('nacc_impn', period)
        nacc_defn = simulation.calculate('nacc_defn', period)
        nacc_defs = simulation.calculate('nacc_defs', period)
        aacc_imps = simulation.calculate('aacc_imps', period)
        mbnc_impo = simulation.calculate('mbnc_impo', period)
        nacc_meup = simulation.calculate('nacc_meup', period)
        abic_impm = simulation.calculate('abic_impm', period)
        abic_defm = simulation.calculate('abic_defm', period)
        abnc_impo = simulation.calculate('abnc_impo', period)
        abnc_defi = simulation.calculate('abnc_defi', period)
        nbic_impm = simulation.calculate('nbic_impm', period)
        alnp_imps = simulation.calculate('alnp_imps', period)
        nbnc_impo = simulation.calculate('nbnc_impo', period)
        nbnc_defi = simulation.calculate('nbnc_defi', period)
        alnp_defs = simulation.calculate('alnp_defs', period)
        cbnc_assc = simulation.calculate('cbnc_assc', period)
        mncn_impo = simulation.calculate('mncn_impo', period)
        cncn_bene = simulation.calculate('cncn_bene', period)
        cncn_defi = simulation.calculate('cncn_defi', period)
        abnc_proc = simulation.calculate('abnc_proc', period)
        rpns_pvct = simulation.calculate('rpns_pvct', period)
        rpns_mvct = simulation.calculate('rpns_mvct', period)
        nbnc_proc = simulation.calculate('nbnc_proc', period)
        frag_fore = simulation.calculate('frag_fore', period)
        f5sq = simulation.calculate('f5sq', period)
        mncn_exon = simulation.calculate('mncn_exon', period)
        cncn_exon = simulation.calculate('cncn_exon', period)
        cncn_aimp = simulation.calculate('cncn_aimp', period)
        cncn_adef = simulation.calculate('cncn_adef', period)
        cncn_info = simulation.calculate('cncn_info', period)
        cncn_jcre = simulation.calculate('cncn_jcre', period)
        revimpres = simulation.calculate('revimpres', period)
        pveximpres = simulation.calculate('pveximpres', period)
        pvtaimpres = simulation.calculate('pvtaimpres', period)
        cga_taux2 = simulation.legislation_at(period.start).ir.rpns.cga_taux2
        microentreprise = simulation.legislation_at(period.start).ir.rpns.microentreprise

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.max, rev), P.min)))

        # Jeunes agriculteurs montant de l'abattement de 50% ou 100%
        # nrag_ajag = f5hm + f5im + f5jm

    #    # déficits agricole des années antérieurs (imputables uniquement
    #    # sur des revenus agricoles)
    #    rag_timp = frag_impo + frag_pvct + arag_impg + nrag_impg
    #    cond = (AUTRE <= microentreprise.def_agri_seuil)
    #    def_agri = cond*(arag_defi + nrag_defi) + not_(cond)*min_(rag_timp, arag_defi + nrag_defi)
    #    # TODO : check 2006 cf art 156 du CGI pour 2006
    #    def_agri_ant    = min_(max_(0,rag_timp - def_agri), f5sq)

        def_agri = f5sq + arag_defi + nrag_defi

        # # B revenus industriels et commerciaux professionnels
        # regime micro entreprise
        mbic_timp = abat_rpns(mbic_impv, microentreprise.vente) + abat_rpns(mbic_imps, microentreprise.servi)

        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        abic_timp = abic_impn + abic_imps - (abic_defn + abic_defs)

        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)

        # Abatemment artisant pécheur
        # nbic_apch = f5ks + f5ls + f5ms # TODO : à intégrer qqpart

        # # C revenus industriels et commerciaux non professionnels
        # (revenus accesoires du foyers en nomenclature INSEE)

        # regime micro entreprise
        macc_timp = abat_rpns(macc_impv, microentreprise.vente) + abat_rpns(macc_imps, microentreprise.servi)
        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        aacc_timp = (max_(0, (aacc_impn + (aacc_gits > 0) * max_(microentreprise.servi.min, aacc_gits *
            (1 - microentreprise.vente.taux)) + (aacc_imps > 0) * max_(microentreprise.servi.min, aacc_imps *
            (1 - microentreprise.servi.taux)) + (nacc_meup > 0) * max_(microentreprise.servi.min, nacc_meup *
            (1 - microentreprise.vente.taux)) + nacc_defs - aacc_defn)))
        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nacc_timp = max_(0, nacc_impn - nacc_defn)

        # # E revenus non commerciaux non professionnels
        # regime déclaratif special ou micro-bnc
        mncn_timp = abat_rpns(mncn_impo, microentreprise.specialbnc)

        # régime de la déclaration controlée
        # total 11
        cncn_timp = max_(0, cncn_bene - cncn_defi)
        # Abatement jeunes créateurs

        # # D revenus non commerciaux professionnels
        # regime déclaratif special ou micro-bnc
        mbnc_timp = abat_rpns(mbnc_impo, microentreprise.specialbnc)

        # regime de la déclaration contrôlée bénéficiant de l'abattement association agréée
        abnc_timp = abnc_impo - abnc_defi

        # regime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
        nbnc_timp = nbnc_impo - nbnc_defi

        # # Totaux
        atimp = arag_impg + abic_timp + aacc_timp + abnc_timp
        ntimp = nrag_impg + nbic_timp + nacc_timp + nbnc_timp + cncn_timp

        majo_cga = max_(0, cga_taux2 * (ntimp + frag_impo))  # Pour ne pas avoir à majorer les déficits
        # total 6
        rev_NS = frag_impo + frag_fore + atimp + ntimp + majo_cga - def_agri

        # revenu net après abatement
        # total 7
        rev_NS_mi = mbic_timp + max_(0, macc_timp) + mbnc_timp + mncn_timp
        exon = max_(0, macc_timp + nacc_timp - rpns_mvct) - macc_timp - nacc_timp  # ajout artificiel
        RPNS = (rev_NS + rev_NS_mi + rpns_pvct + exon + abic_impm - abic_defm + alnp_imps + cncn_aimp - nbic_mvct)
        return period, RPNS


class abat_spe(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Abattements spéciaux"
    url = "http://bofip.impots.gouv.fr/bofip/2036-PGP"

    def function(self, simulation, period):
        """
        Abattements spéciaux

        - pour personnes âges ou invalides : âgé(e) de plus de 65 ans
          ou invalide (titulaire d’une pension d’invalidité militaire ou d’accident
          du travail d’au moins 40 % ou titulaire de la carte d’invalidité),
          abattement de 2 172 € si rng du foyer fiscal inférieur à 13 370 €
                        1 086 € si rng  compris entre 13 370 € et 21 570 €.
          Abattement doublé si conjoint remplit également ces conditions
          d’âge ou d’invalidité.
        - pour enfants à charge ayant fondé un foyer distinct : Si  rattachement
          enfants mariés ou pacsés ou enfants  célibataires, veufs, divorcés, séparés, chargés de famille,
          abattement 5 495 € par personne ainsi rattachée.
          Si l’enfant de la personne rattachée est réputé à charge de
          l’un et l’autre de ses parents (garde alternée), cet abattement est divisé
          par deux soit 2 748€. Exemple : 10 990 € pour un jeune ménage et 8 243 €
          pour un célibataire avec un jeune enfant en résidence alternée.
        """
        period = period.this_year
        age_holder = simulation.compute('age', period)
        caseP = simulation.calculate('caseP', period)
        caseF = simulation.calculate('caseF', period)
        rng = simulation.calculate('rng', period)
        nbN = simulation.calculate('nbN', period)
        abattements_speciaux = simulation.legislation_at(period.start).ir.abattements_speciaux

        age = self.split_by_roles(age_holder, roles = [VOUS, CONJ])

        ageV, ageC = age[VOUS], age[CONJ]
        invV, invC = caseP, caseF
        nb_elig_as = (1 * (((ageV >= 65) | invV) & (ageV > 0)) +
                      1 * (((ageC >= 65) | invC) & (ageC > 0))
                      )
        as_inv = (nb_elig_as * abattements_speciaux.inv_montant * ((rng <= abattements_speciaux.inv_max1)
                  + ((rng > abattements_speciaux.inv_max1) & (rng <= abattements_speciaux.inv_max2)) * 0.5))

        as_enf = nbN * abattements_speciaux.enf_montant

        return period, min_(rng, as_inv + as_enf)


class taux_effectif(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"taux_effectif"
    start_date = date(2009, 1, 1)

    def function(self, simulation, period):
        period = period.this_year
        rni = simulation.calculate('rni', period)
        nbptr = simulation.calculate('nbptr', period)
        microentreprise = simulation.calculate('microentreprise', period)
        abnc_proc_holder = simulation.compute('abnc_proc', period)
        nbnc_proc_holder = simulation.compute('nbnc_proc', period)
        bareme = simulation.legislation_at(period.start).ir.bareme
        cga = simulation.legislation_at(period.start).ir.rpns.cga_taux2

        abnc_proc = self.sum_by_entity(abnc_proc_holder)
        nbnc_proc = self.sum_by_entity(nbnc_proc_holder)
        base_fictive = rni + microentreprise + abnc_proc + nbnc_proc * (1 + cga)
        trigger = (microentreprise != 0) | (abnc_proc != 0) | (nbnc_proc != 0)
        return period, trigger * nbptr * bareme.calc(base_fictive / nbptr) / max_(1, base_fictive)


class taux_moyen_imposition(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Taux moyen d'imposition"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        rni = simulation.calculate('rni', period)
        irpp = simulation.calculate('irpp', period)
        return period, (
            (- irpp) / (rni + (rni == 0))
            ) * (rni > 0)


###############################################################################
# # Calcul du nombre de parts
###############################################################################


class nbptr(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Nombre de parts"
    url = "http://vosdroits.service-public.fr/particuliers/F2705.xhtml"

    def function(self, simulation, period):
        '''
        Nombre de parts du foyer
        'foy'
        note 1 enfants et résidence alternée (formulaire 2041 GV page 10)

        quotient_familial.conj : nb part associées au conjoint d'un couple marié ou pacsé
        quotient_familial.enf1 : nb part 2 premiers enfants
        quotient_familial.enf2 : nb part enfants de rang 3 ou plus
        quotient_familial.inv1 : nb part supp enfants invalides (I, G)
        quotient_familial.inv2 : nb part supp adultes invalides (R)
        quotient_familial.not31 : nb part supp note 3 : cases W ou G pour veuf, celib ou div
        quotient_familial.not32 : nb part supp note 3 : personne seule ayant élevé des enfants
        quotient_familial.not41 : nb part supp adultes invalides (vous et/ou conjoint) note 4
        quotient_familial.not42 : nb part supp adultes anciens combattants (vous et/ou conjoint) note 4
        quotient_familial.not6 : nb part supp note 6
        quotient_familial.isol : demi-part parent isolé (T)
        quotient_familial.edcd : enfant issu du mariage avec conjoint décédé;
        '''
        period = period.this_year
        nb_pac = simulation.calculate('nb_pac', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        celibataire_ou_divorce = simulation.calculate('celibataire_ou_divorce', period)
        veuf = simulation.calculate('veuf', period)
        jeune_veuf = simulation.calculate('jeune_veuf', period)
        nbF = simulation.calculate('nbF', period)
        nbG = simulation.calculate('nbG', period)
        nbH = simulation.calculate('nbH', period)
        nbI = simulation.calculate('nbI', period)
        nbR = simulation.calculate('nbR', period)
        nbJ = simulation.calculate('nbJ', period)
        caseP = simulation.calculate('caseP', period)
        caseW = simulation.calculate('caseW', period)
        caseG = simulation.calculate('caseG', period)
        caseE = simulation.calculate('caseE', period)
        caseK = simulation.calculate('caseK', period)
        caseN = simulation.calculate('caseN', period)
        caseF = simulation.calculate('caseF', period)
        caseS = simulation.calculate('caseS', period)
        caseL = simulation.calculate('caseL', period)
        caseT = simulation.calculate('caseT', period)
        quotient_familial = simulation.legislation_at(period.start).ir.quotient_familial

        no_pac = nb_pac == 0  # Aucune personne à charge en garde exclusive
        has_pac = not_(no_pac)
        no_alt = nbH == 0  # Aucun enfant à charge en garde alternée
        has_alt = not_(no_alt)

        # # nombre de parts liées aux enfants à charge
        # que des enfants en résidence alternée
        enf1 = (no_pac & has_alt) * (quotient_familial.enf1 * min_(nbH, 2) * 0.5
                                     + quotient_familial.enf2 * max_(nbH - 2, 0) * 0.5)
        # pas que des enfants en résidence alternée
        enf2 = (has_pac & has_alt) * ((nb_pac == 1) * (quotient_familial.enf1 * min_(nbH, 1) * 0.5
            + quotient_familial.enf2 * max_(nbH - 1, 0) * 0.5) + (nb_pac > 1) * (quotient_familial.enf2 * nbH * 0.5))
        # pas d'enfant en résidence alternée
        enf3 = quotient_familial.enf1 * min_(nb_pac, 2) + quotient_familial.enf2 * max_((nb_pac - 2), 0)

        enf = enf1 + enf2 + enf3
        # # note 2 : nombre de parts liées aux invalides (enfant + adulte)
        n2 = quotient_familial.inv1 * (nbG + nbI / 2) + quotient_familial.inv2 * nbR

        # # note 3 : Pas de personne à charge
        # - invalide

        n31a = quotient_familial.not31a * (no_pac & no_alt & caseP)
        # - ancien combatant
        n31b = quotient_familial.not31b * (no_pac & no_alt & (caseW | caseG))
        n31 = max_(n31a, n31b)
        # - personne seule ayant élevé des enfants
        n32 = quotient_familial.not32 * (no_pac & no_alt & ((caseE | caseK) & not_(caseN)))
        n3 = max_(n31, n32)
        # # note 4 Invalidité de la personne ou du conjoint pour les mariés ou
        # # jeunes veuf(ve)s
        n4 = max_(quotient_familial.not41 * (1 * caseP + 1 * caseF), quotient_familial.not42 * (caseW | caseS))

        # # note 5
        #  - enfant du conjoint décédé
        n51 = quotient_familial.cdcd * (caseL & ((nbF + nbJ) > 0))
        #  - enfant autre et parent isolé
        n52 = quotient_familial.isol * caseT * (((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2))) + 1 * has_pac)
        n5 = max_(n51, n52)

        # # note 6 invalide avec personne à charge
        n6 = quotient_familial.not6 * (caseP & (has_pac | has_alt))

        # # note 7 Parent isolé
        n7 = quotient_familial.isol * caseT * ((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2)) + 1 * has_pac)

        # # Régime des mariés ou pacsés
        m = 1 + quotient_familial.conj + enf + n2 + n4

        # # veufs  hors jeune_veuf
        v = 1 + enf + n2 + n3 + n5 + n6

        # # celib div
        c = 1 + enf + n2 + n3 + n6 + n7

        return period, (maries_ou_pacses | jeune_veuf) * m + (veuf & not_(jeune_veuf)) * v + celibataire_ou_divorce * c


###############################################################################
# # Calcul de la prime pour l'emploi
###############################################################################


class ppe_coef(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Coefficient - Prime pour l'emploi"

    def function(self, simulation, period):
        '''
        PPE: coefficient de conversion en cas de changement en cours d'année
        '''
        period = period.this_year
        jour_xyz = simulation.calculate('jour_xyz', period)

        nb_jour = (jour_xyz == 0) + jour_xyz
        return period, 360 / nb_jour


class ppe_elig(Variable):
    column = BoolCol(default = False)
    entity_class = FoyersFiscaux
    label = u"ppe_elig"

    def function(self, simulation, period):
        '''
        PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence
        'foy'
        CF ligne 1: http://bofip.impots.gouv.fr/bofip/3913-PGP.html
        '''
        period = period.this_year
        rfr = simulation.calculate('rfr', period)
        ppe_coef = simulation.calculate('ppe_coef', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        veuf = simulation.calculate('veuf', period)
        celibataire_ou_divorce = simulation.calculate('celibataire_ou_divorce', period)
        nbptr = simulation.calculate('nbptr', period)
        ppe = simulation.legislation_at(period.start).ir.credits_impot.ppe

        seuil = (veuf | celibataire_ou_divorce) * (ppe.eligi1 + 2 * max_(nbptr - 1, 0) * ppe.eligi3) \
                + maries_ou_pacses * (ppe.eligi2 + 2 * max_(nbptr - 2, 0) * ppe.eligi3)
        return period, (rfr * ppe_coef) <= seuil


class ppe_rev(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"ppe_rev"

    def function(self, simulation, period):
        '''
        base ressource de la ppe
        'ind'
        '''
        period = period.this_year
        salaire_imposable =  simulation.calculate_add('salaire_imposable', period)
        hsup = simulation.calculate('hsup', period)
        rpns = simulation.calculate('rpns', period)
        ppe = simulation.legislation_at(period.start).ir.credits_impot.ppe

        # Revenu d'activité salarié
        rev_sa = salaire_imposable + hsup  # TODO: + TV + TW + TX + AQ + LZ + VJ
        # Revenu d'activité non salarié
        rev_ns = min_(0, rpns) / ppe.abatns + max_(0, rpns) * ppe.abatns
            #TODO: très bizarre la partie min(0,rpns) - après vérification c'est dans la loi
        return period, rev_sa + rev_ns


class ppe_coef_tp(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"ppe_coef_tp"

    def function(self, simulation, period):
        '''
        PPE: coefficient de conversion temps partiel
        'ind'
        '''
        period = period.this_year
        ppe_du_sa = simulation.calculate('ppe_du_sa', period)
        ppe_du_ns = simulation.calculate('ppe_du_ns', period)
        ppe_tp_sa = simulation.calculate('ppe_tp_sa', period)
        ppe_tp_ns = simulation.calculate('ppe_tp_ns', period)
        ppe = simulation.legislation_at(period.start).ir.credits_impot.ppe

        frac_sa = ppe_du_sa / ppe.TP_nbh
        frac_ns = ppe_du_ns / ppe.TP_nbj
        tp = ppe_tp_sa | ppe_tp_ns | (frac_sa + frac_ns >= 1)
        return period, tp + not_(tp) * (frac_sa + frac_ns)


class ppe_base(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"ppe_base"

    def function(self, simulation, period):
        period = period.this_year
        ppe_rev = simulation.calculate('ppe_rev', period)
        ppe_coef_tp = simulation.calculate('ppe_coef_tp', period)
        ppe_coef_holder = simulation.compute('ppe_coef', period)

        ppe_coef = self.cast_from_entity_to_roles(ppe_coef_holder)

        return period, ppe_rev / (ppe_coef_tp + (ppe_coef_tp == 0)) * ppe_coef


class ppe_elig_individu(Variable):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"ppe_elig_i"

    def function(self, simulation, period):
        '''
        Eligibilité individuelle à la ppe
        Attention : condition de plafonnement introduite dans ppe brute
        'ind'
        '''
        period = period.this_year
        ppe_rev = simulation.calculate('ppe_rev', period)
        ppe_coef_tp = simulation.calculate('ppe_coef_tp', period)
        ppe = simulation.legislation_at(period.start).ir.credits_impot.ppe

        return period, (ppe_rev >= ppe.seuil1) & (ppe_coef_tp != 0)


class ppe_brute(Variable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Prime pour l'emploi brute"

    def function(self, simulation, period):
        '''
        Prime pour l'emploi (avant éventuel dispositif de cumul avec le RSA)
        'foy'
        Cf. http://travail-emploi.gouv.fr/informations-pratiques,89/fiches-pratiques,91/remuneration,113/la-prime-pour-l-emploi-ppe,1034.html
        '''
        period = period.this_year
        ppe_elig = simulation.calculate('ppe_elig', period)
        ppe_elig_i_holder = simulation.compute('ppe_elig_individu', period)
        ppe_rev_holder = simulation.compute('ppe_rev', period)
        ppe_base_holder = simulation.compute('ppe_base', period)
        ppe_coef = simulation.calculate('ppe_coef', period)
        ppe_coef_tp_holder = simulation.compute('ppe_coef_tp', period)
        nb_pac = simulation.calculate('nb_pac', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        celibataire_ou_divorce = simulation.calculate('celibataire_ou_divorce', period)
        veuf = simulation.calculate('veuf', period)
        caseT = simulation.calculate('caseT', period)
        caseL = simulation.calculate('caseL', period)
        nbH = simulation.calculate('nbH', period)
        ppe = simulation.legislation_at(period.start).ir.credits_impot.ppe

        ppe_base = self.split_by_roles(ppe_base_holder)
        ppe_coef_tp = self.split_by_roles(ppe_coef_tp_holder)
        ppe_elig_i = self.split_by_roles(ppe_elig_i_holder)
        ppe_rev = self.split_by_roles(ppe_rev_holder)

        eliv, elic, eli1, eli2, eli3 = ppe_elig_i[VOUS], ppe_elig_i[CONJ], ppe_elig_i[PAC1], \
            ppe_elig_i[PAC2], ppe_elig_i[PAC3]
        basevi, baseci = ppe_rev[VOUS], ppe_rev[CONJ]
        basev, basec, base1, base2, base3 = ppe_base[VOUS], ppe_base[CONJ], ppe_base[PAC1], ppe_base[PAC2], ppe_base[PAC1]
        coef_tpv, coef_tpc, coef_tp1, coef_tp2, coef_tp3 = ppe_coef_tp[VOUS], ppe_coef_tp[CONJ], \
            ppe_coef_tp[PAC1], ppe_coef_tp[PAC2], ppe_coef_tp[PAC1]

        nb_pac_ppe = max_(0, nb_pac - eli1 - eli2 - eli3)

        ligne2 = maries_ou_pacses & xor_(basevi >= ppe.seuil1, baseci >= ppe.seuil1)
        ligne3 = (celibataire_ou_divorce | veuf) & caseT & not_(veuf & caseT & caseL)
        ligne1 = not_(ligne2) & not_(ligne3)

        base_monact = ligne2 * (eliv * basev + elic * basec)
        base_monacti = ligne2 * (eliv * basevi + elic * baseci)

        def ppe_bar1(base):
    #        cond1 = ligne1 | ligne3
    #        cond2 = ligne2
    #        return 1 / ppe_coef * ((cond1 & (base <= ppe.seuil2)) * (base) * ppe.taux1 +
    #                           (cond1 & (base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base) * ppe.taux2 +
    #                           (cond2 & (base <= ppe.seuil2)) * (base * ppe.taux1) +
    #                           (cond2 & (base > ppe.seuil2) & (base <= ppe.seuil3)) * ((ppe.seuil3 - base) * ppe.taux2) +
    #                           (cond2 & (base > ppe.seuil4) & (base <= ppe.seuil5)) * (ppe.seuil5 - base) * ppe.taux3)
            return (1 / ppe_coef) * (
                ((base <= ppe.seuil2)) * (base) * ppe.taux1
                + ((base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base) * ppe.taux2
                + ligne2 * ((base > ppe.seuil4) & (base <= ppe.seuil5)) * (ppe.seuil5 - base) * ppe.taux3)

        def ppe_bar2(base):
            return (1 / ppe_coef) * (
                (base <= ppe.seuil2) * (base) * ppe.taux1
                + ((base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base1) * ppe.taux2)

        # calcul des primes individuelles.

        ppev = eliv * ppe_bar1(basev)
        ppec = elic * ppe_bar1(basec)
        ppe1 = eli1 * ppe_bar2(base1)
        ppe2 = eli2 * ppe_bar2(base2)
        ppe3 = eli3 * ppe_bar2(base3)

        # Primes de monoactivité
        ppe_monact_vous = (eliv & ligne2 & (basevi >= ppe.seuil1) & (basev <= ppe.seuil4)) * ppe.monact
        ppe_monact_conj = (elic & ligne2 & (baseci >= ppe.seuil1) & (basec <= ppe.seuil4)) * ppe.monact

        # Primes pour enfants à charge
        maj_pac = ppe_elig * (eliv | elic) * (
            (ligne1 & maries_ou_pacses & ((ppev + ppec) != 0) & (min_(basev, basec) <= ppe.seuil3)) * ppe.pac
            * (nb_pac_ppe + nbH * 0.5)
            + (ligne1 & (celibataire_ou_divorce | veuf) & eliv & (basev <= ppe.seuil3)) * ppe.pac * (nb_pac_ppe + nbH * 0.5)
            + (ligne2 & (base_monacti >= ppe.seuil1) & (base_monact <= ppe.seuil3)) * ppe.pac * (nb_pac_ppe + nbH * 0.5)
            + (ligne2 & (base_monact > ppe.seuil3) & (base_monact <= ppe.seuil5)) * ppe.pac
            * ((nb_pac_ppe != 0) + 0.5 * ((nb_pac_ppe == 0) & (nbH != 0)))
            + (ligne3 & (basevi >= ppe.seuil1) & (basev <= ppe.seuil3)) * (
                (min_(nb_pac_ppe, 1) * 2 * ppe.pac + max_(nb_pac_ppe - 1, 0) * ppe.pac)
                + (nb_pac_ppe == 0) * (min_(nbH, 2) * ppe.pac + max_(nbH - 2, 0) * ppe.pac * 0.5))
            + (ligne3 & (basev > ppe.seuil3) & (basev <= ppe.seuil5)) * ppe.pac
            * ((nb_pac_ppe != 0) * 2 + ((nb_pac_ppe == 0) & (nbH != 0))))

        def coef(coef_tp):
            return (coef_tp <= 0.5) * coef_tp * 1.45 + (coef_tp > 0.5) * (0.55 * coef_tp + 0.45)

        ppe_vous = ppe_elig * (ppev * coef(coef_tpv) + ppe_monact_vous)
        ppe_conj = ppe_elig * (ppec * coef(coef_tpc) + ppe_monact_conj)
        ppe_pac1 = ppe_elig * (ppe1 * coef(coef_tp1))
        ppe_pac2 = ppe_elig * (ppe2 * coef(coef_tp2))
        ppe_pac3 = ppe_elig * (ppe3 * coef(coef_tp3))

        ppe_tot = ppe_vous + ppe_conj + ppe_pac1 + ppe_pac2 + ppe_pac3 + maj_pac

        ppe_tot = (ppe_tot != 0) * max_(ppe.versmin, ppe_tot)

        return period, ppe_tot


class ppe(DatedVariable):
    column = FloatCol
    entity_class = FoyersFiscaux
    label = u"Prime pour l'emploi"
    url = "http://vosdroits.service-public.fr/particuliers/F2882.xhtml"

    @dated_function(stop = date(2015, 12, 31))
    def function(self, simulation, period):
        """
        PPE effectivement versée
        'foy'
        """
        period = period.this_year
        ppe_brute = simulation.calculate('ppe_brute', period)
        rsa_act_i_holder = simulation.compute('rsa_activite_individu', period)

        # TODO: les foyers qui paient l'ISF n'ont pas le droit à la PPE
        rsa_act_i = self.split_by_roles(rsa_act_i_holder, roles = [VOUS, CONJ])

        #   On retranche le RSA activité de la PPE
        #   Dans les agrégats officiels de la DGFP, c'est la PPE brute qu'il faut comparer
        ppe = max_(ppe_brute - rsa_act_i[VOUS] - rsa_act_i[CONJ], 0)
        return period, ppe
