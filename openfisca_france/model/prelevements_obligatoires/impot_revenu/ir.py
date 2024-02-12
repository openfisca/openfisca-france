import logging

from numpy import datetime64, timedelta64, logical_xor as xor_, round as round_, around

from numpy.core.defchararray import startswith

from openfisca_core.model_api import *
from openfisca_france.model.base import *


log = logging.getLogger(__name__)


# TODO: 8ti et 8tk (cerfa 2047)

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
#    impot_revenu_restant_a_payer   = -(mciria + ppetot - mcirra )


class jour_xyz(Variable):
    value_type = int
    default_value = 360
    entity = FoyerFiscal
    label = 'Jours décomptés au titre de cette déclaration'
    definition_period = YEAR


###############################################################################
# # Initialisation de quelques variables utiles pour la suite
###############################################################################


class age(Variable):
    unit = 'years'
    value_type = int
    default_value = AGE_INT_MINIMUM
    entity = Individu
    label = 'Âge (en années) au premier jour du mois'
    definition_period = MONTH
    is_period_size_independent = True
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        has_birth = individu.get_holder('date_naissance').get_known_periods()
        if not has_birth:
            has_age_en_mois = bool(individu.get_holder('age_en_mois').get_known_periods())
            if has_age_en_mois:
                return individu('age_en_mois', period) // 12

            # If age is known at the same day of another year, compute the new age from it.
            holder = individu.get_holder('age')
            start = period.start
            known_periods = holder.get_known_periods()
            if known_periods:
                for last_period in sorted(known_periods, reverse = True):
                    last_start = last_period.start
                    if last_start.day == start.day:
                        last_array = holder.get_array(last_period)
                        return (
                            last_array
                            + int(
                                start.year
                                - last_start.year
                                + (start.month - last_start.month) / 12
                                )
                            )

        date_naissance = individu('date_naissance', period)
        epsilon = timedelta64(1)
        return (datetime64(period.start) - date_naissance + epsilon).astype('timedelta64[Y]')


class age_en_mois(Variable):
    value_type = int
    default_value = AGE_INT_MINIMUM
    unit = 'months'
    entity = Individu
    label = 'Âge (en mois)'
    is_period_size_independent = True
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        # If age_en_mois is known at the same day of another month, compute the new age_en_mois from it.
        holder = individu.get_holder('age_en_mois')
        start = period.start
        known_periods = holder.get_known_periods()

        for last_period in sorted(known_periods, reverse = True):
            last_start = last_period.start
            if last_start.day == start.day:
                last_array = holder.get_array(last_period)
                return last_array + ((start.year - last_start.year) * 12 + (start.month - last_start.month))

        has_birth = individu.get_holder('date_naissance').get_known_periods()
        if not has_birth:
            has_age = bool(individu.get_holder('age').get_known_periods())
            if has_age:
                return individu('age', period) * 12
        date_naissance = individu('date_naissance', period)
        epsilon = timedelta64(1)
        return (datetime64(period.start) - date_naissance + epsilon).astype('timedelta64[M]')


class depcom_foyer(Variable):
    value_type = str
    max_length = 5
    entity = FoyerFiscal
    default_value = '00000'
    label = 'Code AFT du lieu de domicile fiscal'
    definition_period = YEAR
    set_input = set_input_dispatch_by_period
    # Cette variable est similaire à la variable "depcom" qui est le lieu de domicile du ménage tandis que "depcom_foyer" est le lieu de résidence fiscale du foyer fiscal.


class residence_fiscale_guadeloupe(Variable):
    value_type = bool
    entity = FoyerFiscal
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        depcom_foyer = foyer_fiscal('depcom_foyer', period)
        return startswith(depcom_foyer, b'971')


class residence_fiscale_martinique(Variable):
    value_type = bool
    entity = FoyerFiscal
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        depcom_foyer = foyer_fiscal('depcom_foyer', period)
        return startswith(depcom_foyer, b'972')


class residence_fiscale_guyane(Variable):
    value_type = bool
    entity = FoyerFiscal
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        depcom_foyer = foyer_fiscal('depcom_foyer', period)
        return startswith(depcom_foyer, b'973')


class residence_fiscale_reunion(Variable):
    value_type = bool
    entity = FoyerFiscal
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        depcom_foyer = foyer_fiscal('depcom_foyer', period)
        return startswith(depcom_foyer, b'974')


class residence_fiscale_mayotte(Variable):
    value_type = bool
    entity = FoyerFiscal
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        depcom_foyer = foyer_fiscal('depcom_foyer', period)
        return startswith(depcom_foyer, b'976')


class nb_adult(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Nombre d'adulte(s) déclarants dans le foyer fiscal"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        veuf = foyer_fiscal('veuf', period)

        return 2 * maries_ou_pacses + 1 * (celibataire_ou_divorce | veuf)


class nb_pac(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Nombre de personnes à charge dans le foyer fiscal'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        nbF = foyer_fiscal('nbF', period)
        nbJ = foyer_fiscal('nbJ', period)
        nbR = foyer_fiscal('nbR', period)

        return nbF + nbJ + nbR


class enfant_a_charge(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant à charge non marié, de moins de 18 ans non émancipé au 1er janvier de l'année de perception des revenus, ou né durant la même année, ou handicapé quel que soit son âge"
    definition_period = YEAR

    def formula(individu, period):
        janvier = period.first_month
        decembre = janvier.offset(11, 'month')

        majeur = individu('majeur', janvier)
        handicap = individu('handicap', decembre)
        is_pac = individu.has_role(FoyerFiscal.PERSONNE_A_CHARGE)

        return is_pac * (not_(majeur) + handicap)


class nbF(Variable):
    cerfa_field = 'F'
    entity = FoyerFiscal
    value_type = float
    label = "Nombre d'enfants à charge non mariés, qui ne sont pas en résidence alternée, de moins de 18 ans au 1er janvier de l'année de perception des"\
        ' revenus, ou nés durant la même année ou handicapés quel que soit leur âge'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        janvier = period.first_month

        enfant_a_charge = foyer_fiscal.members('enfant_a_charge', period)
        garde_alternee = foyer_fiscal.members('garde_alternee', janvier)
        return foyer_fiscal.sum(enfant_a_charge * not_(garde_alternee))


class nbG(Variable):
    cerfa_field = 'G'
    entity = FoyerFiscal
    value_type = float
    label = "Nombre d'enfants qui ne sont pas en résidence alternée à charge titulaires de la carte d'invalidité."
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        janvier = period.first_month

        enfant_a_charge = foyer_fiscal.members('enfant_a_charge', period)
        garde_alternee = foyer_fiscal.members('garde_alternee', janvier)
        invalidite = foyer_fiscal.members('invalidite', janvier)
        return foyer_fiscal.sum(enfant_a_charge * not_(garde_alternee) * invalidite)


class nbH(Variable):
    cerfa_field = 'H'
    entity = FoyerFiscal
    value_type = float
    label = "Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        janvier = period.first_month

        enfant_a_charge = foyer_fiscal.members('enfant_a_charge', period)
        garde_alternee = foyer_fiscal.members('garde_alternee', janvier)
        return foyer_fiscal.sum(enfant_a_charge * garde_alternee)


class nbI(Variable):
    cerfa_field = 'I'
    entity = FoyerFiscal
    value_type = float
    label = "Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        janvier = period.first_month

        enfant_a_charge = foyer_fiscal.members('enfant_a_charge', period)
        garde_alternee = foyer_fiscal.members('garde_alternee', janvier)
        invalidite = foyer_fiscal.members('invalidite', janvier)
        return foyer_fiscal.sum(enfant_a_charge * garde_alternee * invalidite)


class enfant_majeur_celibataire_sans_enfant(Variable):
    value_type = bool
    entity = Individu
    label = 'Enfant majeur célibataire sans enfant'
    definition_period = YEAR

    def formula(individu, period):
        janvier = period.first_month

        age = individu('age', janvier)
        handicap = individu('handicap', janvier)
        is_pac = individu.has_role(FoyerFiscal.PERSONNE_A_CHARGE)

        return is_pac * (age >= 18) * not_(handicap)


class nbJ(Variable):
    cerfa_field = 'J'
    entity = FoyerFiscal
    label = "Nombre d'enfants majeurs célibataires sans enfant"
    value_type = int
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        enfant_majeur_celibataire_sans_enfant = foyer_fiscal.members('enfant_majeur_celibataire_sans_enfant', period)
        return foyer_fiscal.sum(enfant_majeur_celibataire_sans_enfant)


class nombre_enfants_majeurs_celibataires_sans_enfant(Variable):
    entity = Menage
    label = "Nombre d'enfants majeurs célibataires sans enfant"
    value_type = int
    definition_period = YEAR

    def formula(menage, period):
        enfant_majeur_celibataire_sans_enfant = menage.members('enfant_majeur_celibataire_sans_enfant', period)
        return menage.sum(enfant_majeur_celibataire_sans_enfant)


class maries_ou_pacses(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Déclarants mariés ou pacsés'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        statut_marital = foyer_fiscal.declarant_principal('statut_marital', period.first_month)
        marie_ou_pacse = (statut_marital == TypesStatutMarital.marie) | (statut_marital == TypesStatutMarital.pacse)

        return marie_ou_pacse


class celibataire_ou_divorce(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Déclarant célibataire ou divorcé'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        statut_marital = foyer_fiscal.declarant_principal('statut_marital', period.first_month)
        celibataire_ou_divorce = (statut_marital == TypesStatutMarital.celibataire) | (
            statut_marital == TypesStatutMarital.divorce
            )

        return celibataire_ou_divorce


class veuf(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Déclarant veuf'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        statut_marital = foyer_fiscal.declarant_principal('statut_marital', period.first_month)
        veuf = (statut_marital == TypesStatutMarital.veuf)

        return veuf


class jeune_veuf(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Déclarant jeune veuf'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        statut_marital = foyer_fiscal.declarant_principal('statut_marital', period.first_month)
        jeune_veuf = (statut_marital == TypesStatutMarital.jeune_veuf)

        return jeune_veuf


###############################################################################
# # Revenus catégoriels
###############################################################################


class revenu_assimile_salaire(Variable):
    value_type = float
    entity = Individu
    label = 'Revenu imposé comme des salaires (salaires, mais aussi 3vj, 3vk)'
    definition_period = YEAR

    def formula(individu, period, parameters):
        salaire_imposable = individu('salaire_imposable', period, options = [ADD])
        chomage_imposable = individu('chomage_imposable', period, options = [ADD])
        f1tt = individu('f1tt', period)
        f3vj = individu('f3vj', period)
        salaires_imposable_particulier_employeur = individu('salaires_imposable_particulier_employeur', period)
        revenus_imposables_associes_gerants = individu('revenus_imposables_associes_gerants', period)
        droits_auteurs_imposables = individu('droits_auteurs_imposables', period)
        salaire_imposable_agents_assurance = individu('salaire_imposable_agents_assurance', period)

        return (
            salaire_imposable
            + chomage_imposable
            + f1tt
            + f3vj
            + salaires_imposable_particulier_employeur
            + revenus_imposables_associes_gerants
            + droits_auteurs_imposables
            + salaire_imposable_agents_assurance
            )


class revenu_assimile_salaire_apres_abattements(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires et chômage imposables après abattements'
    definition_period = YEAR

    def formula(individu, period, parameters):
        revenu_assimile_salaire = individu('revenu_assimile_salaire', period)
        chomeur_longue_duree = individu('chomeur_longue_duree', period)
        frais_reels = individu('frais_reels', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.deductions

        abattement_minimum = where(chomeur_longue_duree, P.abatpro.min2, P.abatpro.min)
        abatfor = round_(min_(max_(P.taux_salaires_pensions * revenu_assimile_salaire, abattement_minimum), P.abatpro.max))
        return (
            (frais_reels > abatfor)
            * (revenu_assimile_salaire - frais_reels)
            + (frais_reels <= abatfor)
            * max_(0, revenu_assimile_salaire - abatfor)
            )

    def formula_2018_01_01(individu, period, parameters):
        revenu_assimile_salaire = individu('revenu_assimile_salaire', period)
        frais_reels = individu('frais_reels', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.deductions

        abatfor = round_(min_(max_(P.taux_salaires_pensions * revenu_assimile_salaire, P.abatpro.min), P.abatpro.max))
        return (
            (frais_reels > abatfor)
            * (revenu_assimile_salaire - frais_reels)
            + (frais_reels <= abatfor)
            * max_(0, revenu_assimile_salaire - abatfor)
            )


class revenu_assimile_pension(Variable):
    value_type = float
    entity = Individu
    label = 'Revenu imposé comme des pensions (retraites, pensions alimentaires, etc.)'
    definition_period = YEAR

    def formula(individu, period):
        pensions_alimentaires_percues = individu('pensions_alimentaires_percues', period, options = [ADD])
        pensions_alimentaires_percues_decl = individu('pensions_alimentaires_percues_decl', period, options = [ADD])
        retraite_imposable = individu('retraite_imposable', period, options = [ADD])
        pension_invalidite = individu('pensions_invalidite', period, options = [ADD])

        return pensions_alimentaires_percues * pensions_alimentaires_percues_decl + retraite_imposable + pension_invalidite


class revenu_assimile_pension_apres_abattements(Variable):
    value_type = float
    entity = Individu
    label = 'Pensions après abattements'
    definition_period = YEAR

    def formula(individu, period, parameters):
        revenu_assimile_pension = individu('revenu_assimile_pension', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.deductions

        #    TODO: problème car les pensions sont majorées au niveau du foyer
    #    d11 = ( AS + BS + CS + DS + ES +
    #            AO + BO + CO + DO + EO )
    #    penv2 = (d11-f11> abatpen.max)*(penv + (d11-f11-abatpen.max)) + (d11-f11<= abatpen.max)*penv
    #    Plus d'abatement de 20% en 2006
        return max_(0, revenu_assimile_pension - round_(max_(P.taux_salaires_pensions * revenu_assimile_pension, P.abatpen.min)))


#    return max_(0, revenu_assimile_pension - min_(round_(max_(P.taux_salaires_pensions*revenu_assimile_pension , P.abatpen.min)), P.abatpen.max))  le max se met au niveau du foyer

class indu_plaf_abat_pen(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Plafonnement de l'abattement de 10% sur les pensions du foyer"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rev_pen_i = foyer_fiscal.members('revenu_assimile_pension', period)
        pen_net_i = foyer_fiscal.members('revenu_assimile_pension_apres_abattements', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.deductions

        revenu_assimile_pension_apres_abattements = foyer_fiscal.sum(pen_net_i)
        revenu_assimile_pension = foyer_fiscal.sum(rev_pen_i)

        abat = revenu_assimile_pension - revenu_assimile_pension_apres_abattements
        return abat - min_(abat, P.abatpen.max)


class abattement_salaires_pensions(Variable):
    value_type = float
    entity = Individu
    label = "Abattement de 20% sur les salaires et pensions, en vigueur jusqu'à 2006"
    end = '2005-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        revenu_assimile_salaire_apres_abattements = individu('revenu_assimile_salaire_apres_abattements', period)
        revenu_assimile_pension_apres_abattements = individu('revenu_assimile_pension_apres_abattements', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.deductions

        return min_(P.abat_supp.taux * max_(revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements, 0), P.abat_supp.max)


class rente_viagere_titre_onereux(Variable):
    '''Rentes viagères à titre onéreux (avant abattements)

    Annuel pour les impôts mais mensuel pour la base ressource des minimas sociaux donc mensuel.
    '''
    calculate_output = calculate_output_add
    value_type = float
    entity = FoyerFiscal
    label = 'Rentes viagères (rentes à titre onéreux)'
    set_input = set_input_divide_by_period
    reference = 'http://fr.wikipedia.org/wiki/Rente_viagère'
    definition_period = MONTH

    def formula(foyer_fiscal, period, parameters):
        year = period.this_year
        f1aw = foyer_fiscal('f1aw', year)
        f1bw = foyer_fiscal('f1bw', year)
        f1cw = foyer_fiscal('f1cw', year)
        f1dw = foyer_fiscal('f1dw', year)

        return (f1aw + f1bw + f1cw + f1dw) / 12


class rente_viagere_titre_onereux_net(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Rentes viagères après abattements'
    reference = 'http://www.lafinancepourtous.fr/Vie-professionnelle-et-retraite/Retraite/Epargne-retraite/La-rente-viagere/La-fiscalite-de-la-rente-viagere'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Selon la législation, le taux d'abattement appliqué dépend de l'âge du bénéficiaire lors du premier versement
        de la rente. Il y a quatre taux possibles. On suppoose que la case 1aw bénéficie du taux associé à l'âge le
        moins élevé, et ainsi de suite jusqu'à la case 1dw qui bénéficie du taux associé à l'âge le plus élevé.
        '''
        f1aw = foyer_fiscal('f1aw', period)
        f1bw = foyer_fiscal('f1bw', period)
        f1cw = foyer_fiscal('f1cw', period)
        f1dw = foyer_fiscal('f1dw', period)
        abatviag = parameters(period).impot_revenu.calcul_revenus_imposables.deductions.abatviag

        return round_(
            + abatviag.taux1 * f1aw
            + abatviag.taux2 * f1bw
            + abatviag.taux3 * f1cw
            + abatviag.taux4 * f1dw
            )


class traitements_salaires_pensions_rentes(Variable):
    value_type = float
    entity = Individu
    label = 'Traitements salaires pensions et rentes individuelles'
    definition_period = YEAR

    def formula(individu, period):
        revenu_assimile_salaire_apres_abattements = individu('revenu_assimile_salaire_apres_abattements', period)
        revenu_assimile_pension_apres_abattements = individu('revenu_assimile_pension_apres_abattements', period)
        abattement_salaires_pensions = individu('abattement_salaires_pensions', period)

        # Quand deductions est calculé sur une année glissante, rente_viagere_titre_onereux_net est calculé sur l'année légale
        # correspondante.
        rente_viagere_titre_onereux_net = individu.foyer_fiscal('rente_viagere_titre_onereux_net', period.offset('first-of'))
        rente_viagere_titre_onereux_net_declarant1 = rente_viagere_titre_onereux_net * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return (
            + revenu_assimile_salaire_apres_abattements
            + revenu_assimile_pension_apres_abattements
            + rente_viagere_titre_onereux_net_declarant1
            - abattement_salaires_pensions
            )


class revenu_categoriel_plus_values(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu catégoriel - Plus-values (plus-values imposées au barème, les autres entrent dans la variable plus_values_prelevement_forfaitaire_unique_ir si elles sont éligibles au pfu et dans taxation_plus_values_hors_bareme sinon)'
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        f3sb = foyer_fiscal('f3sb', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3vl = foyer_fiscal('f3vl', period)
        f3wb = foyer_fiscal('f3wb', period)

        return f3sb + f3vg + f3vl + f3wb

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        f3sb = foyer_fiscal('f3sb', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3wb = foyer_fiscal('f3wb', period)

        return f3sb + f3vg + f3wb

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        f3sb = foyer_fiscal('f3sb', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3wb = foyer_fiscal('f3wb', period)
        f3ua = foyer_fiscal('f3ua', period)  # Cette case existant avant, mais ses montants étaient inclus dans 3vg.

        return f3sb + f3vg + f3wb + f3ua

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        imposition_au_bareme = foyer_fiscal('f2op', period)
        f3sb = foyer_fiscal('f3sb', period)
        f3wb = foyer_fiscal('f3wb', period)
        f3vg = foyer_fiscal('f3vg', period)  # Brut d'abattement à partir de 2018
        f3sg = foyer_fiscal('f3sg', period)  # Abattement pour durée de détention de droit commun
        f3ua = foyer_fiscal('f3ua', period)  # Brut d'abattement à partir de 2018
        f3sl = foyer_fiscal('f3sl', period)  # Abattement pour durée de détention renforcé
        f3va = foyer_fiscal('f3va', period)  # Abattement fixe
        f3tj = foyer_fiscal('f3tj', period)

        pre_result = where(imposition_au_bareme, f3sb + max_(0, f3ua - f3sl - f3va) + max_(0, f3vg - f3sg) + f3tj, 0)

        return f3wb + pre_result

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        imposition_au_bareme = foyer_fiscal('f2op', period)
        f3sb = foyer_fiscal('f3sb', period)
        f3wb = foyer_fiscal('f3wb', period)
        f3vg = foyer_fiscal('f3vg', period)  # Brut d'abattement à partir de 2018
        f3sg = foyer_fiscal('f3sg', period)  # Abattement pour durée de détention de droit commun
        f3ua = foyer_fiscal('f3ua', period)  # Brut d'abattement à partir de 2018
        f3sl = foyer_fiscal('f3sl', period)  # Abattement pour durée de détention renforcé
        f3va = foyer_fiscal('f3va', period)  # Abattement fixe
        f3tj = foyer_fiscal('f3tj', period)
        f3tk = foyer_fiscal('f3tk', period)
        f3vt = foyer_fiscal('f3vt', period)

        pre_result = where(imposition_au_bareme, f3sb + max_(0, f3ua - f3sl - f3va) + max_(0, f3vg - f3sg) + max_(0, f3tj - f3tk) + f3vt, 0)

        return f3wb + pre_result


class revenu_categoriel_deductions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu catégoriel - Traitements, salaires, pensions et rentes'
    reference = 'http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        deductions_i = foyer_fiscal.members('traitements_salaires_pensions_rentes', period)
        indu_plaf_abat_pen = foyer_fiscal('indu_plaf_abat_pen', period)

        traitements_salaires_pensions_rentes = foyer_fiscal.sum(deductions_i)

        return traitements_salaires_pensions_rentes + indu_plaf_abat_pen


class deficit_rcm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Deficit capitaux mobiliers'
    reference = 'http://www.lefigaro.fr/impots/2008/04/25/05003-20080425ARTFIG00254-les-subtilites-des-revenus-de-capitaux-mobiliers-.php'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        f2aa = foyer_fiscal('f2aa', period)
        f2al = foyer_fiscal('f2al', period)
        f2am = foyer_fiscal('f2am', period)
        f2an = foyer_fiscal('f2an', period)
        f2aq = foyer_fiscal('f2aq', period)
        f2ar = foyer_fiscal('f2ar', period)

        return f2aa + f2al + f2am + f2an + f2aq + f2ar


class revenu_categoriel_capital(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu catégoriel - Capitaux'
    reference = 'http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2ca = foyer_fiscal('f2ca', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2gr = foyer_fiscal('f2gr', period)
        f2tr = foyer_fiscal('f2tr', period)
        rvcm = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        f2dc_bis = f2dc
        f2tr_bis = f2tr
        # # Calcul du revenu catégoriel
        # 1.2 Revenus des valeurs et capitaux mobiliers
        b12 = min_(f2ch, rvcm.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses))
        TOT1 = f2ch - b12  # c12
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
        F1 = f2ca / den * f2dc_bis  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie négative (à déduire des autres revenus nets de frais d'abattements
        g12a = -min_(f2dc_bis * (1 - rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement) - F1, 0)
        # partie positive
        g12b = max_(f2dc_bis * (1 - rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement)

        # Abattements, limité au revenu
        h12 = rvcm.revenus_capitaux_mobiliers_dividendes.abattement_forfaitaire * (1 + maries_ou_pacses)
        TOT2 = max_(0, rev - h12)
        # i121= -min_(0,rev - h12)

        # Part des frais s'imputant sur les revenus déclarés ligne TS
        F2 = f2ca - F1
        TOT3 = (f2ts - F2) + f2go * rvcm.majoration_revenus_reputes_distribues + f2tr_bis - g12a

        DEF = deficit_rcm
        return max_(TOT1 + TOT2 + TOT3 - DEF, 0)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2da = foyer_fiscal('f2da', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2ca = foyer_fiscal('f2ca', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2gr = foyer_fiscal('f2gr', period)
        f2tr = foyer_fiscal('f2tr', period)
        parameter_rvcm = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        part_frais_imputes_sur_f2dc = f2ca / max_(1, f2dc + f2ts) * f2dc
        part_frais_restant_a_imputer = -min_(f2dc * (1 - parameter_rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement * (f2da == 0)) - part_frais_imputes_sur_f2dc, 0)

        dividendes_apres_abattements = max_(f2dc * (1 - parameter_rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement * (f2da == 0)) - part_frais_imputes_sur_f2dc, 0)
        revenus_assurance_vie_apres_abattements = f2ch - min_(f2ch, parameter_rvcm.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses))
        rvcm_apres_abattements_proportionnels = (
            revenus_assurance_vie_apres_abattements
            + dividendes_apres_abattements
            + f2gr
            + f2fu * (1 - parameter_rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement * (f2da == 0))
            )
        rvcm_apres_abattements_proportionnels_et_fixes = max_(0, rvcm_apres_abattements_proportionnels - parameter_rvcm.revenus_capitaux_mobiliers_dividendes.abattement_forfaitaire * (1 + maries_ou_pacses))
        autres_rvcm_sans_abattements = (
            f2ts - (f2ca - part_frais_imputes_sur_f2dc)
            + f2go * parameter_rvcm.majoration_revenus_reputes_distribues
            + f2tr - part_frais_restant_a_imputer
            )

        return max_(rvcm_apres_abattements_proportionnels_et_fixes + autres_rvcm_sans_abattements - deficit_rcm, 0)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        f2ca = foyer_fiscal('f2ca', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2tr = foyer_fiscal('f2tr', period)
        f2ts = foyer_fiscal('f2ts', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        # Revenus après abatemment
        abattement_dividende = (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement
        abattement_assurance_vie = P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses)
        rvcm_apres_abattement = (
            f2fu + f2dc - abattement_dividende
            + f2ch - min_(f2ch, abattement_assurance_vie)
            + f2ts + f2tr + f2go * P.majoration_revenus_reputes_distribues
            )

        return max_(0, rvcm_apres_abattement - f2ca - deficit_rcm)

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        f2ca = foyer_fiscal('f2ca', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2tr = foyer_fiscal('f2tr', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2tt_2016 = foyer_fiscal('f2tt_2016', period)
        f2tu_2016 = foyer_fiscal('f2tu_2016', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        # Revenus après abatemment
        abattement_dividende = (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement
        abattement_assurance_vie = P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses)
        rvcm_apres_abattement = (
            f2fu + f2dc - abattement_dividende
            + f2ch - min_(f2ch, abattement_assurance_vie)
            + f2ts + f2tr + max_(0, f2tt_2016 - f2tu_2016) + f2go * P.majoration_revenus_reputes_distribues
            )

        return max_(0, rvcm_apres_abattement - f2ca - deficit_rcm)

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers
        Seule différence avec la formule précédente :
            On enlève la case 2TU. En 2016, 2TT contient les intérêts avant pertes
            et 2TU les pertes déductibles des intérêts inscrits en 2TT (si le montant en 2TU est > à celui en 2TT,
            la perte excédentaire est reportable sur les cinq années suivantes). En 2017, 2TT contient les intérêts
            après déduction des pertes. 2TU, et aussi 2TV, contiennent des pertes excéndentaires à reporter.
            Sources :
              - Brochure pratique de l'IR 2018 sur revenus 2017 : https://www.impots.gouv.fr/portail/www2/fichiers/documentation/brochure/ir_2018/files/assets/common/downloads/Brochure%20IR%202018.pdf
              - Brochure pratique de l'IR 2017 sur revenus 2016 : https://www.impots.gouv.fr/portail/www2/fichiers/documentation/brochure/ir_2017/files/assets/common/downloads/publication.pdf
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        f2ca = foyer_fiscal('f2ca', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2tr = foyer_fiscal('f2tr', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2tt = foyer_fiscal('f2tt', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        # Revenus après abatemment
        abattement_dividende = (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement
        abattement_assurance_vie = P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses)
        rvcm_apres_abattement = (
            f2fu + f2dc - abattement_dividende
            + f2ch - min_(f2ch, abattement_assurance_vie)
            + f2ts + f2tr + f2tt + f2go * P.majoration_revenus_reputes_distribues
            )

        return max_(0, rvcm_apres_abattement - f2ca - deficit_rcm)

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers

        NB : La mise en place du PFU supprime la taxation au barème de la plupart des revenus des valeurs et capitaux mobiliers.
        Ces revenus sortent donc de la variable `revenu_categoriel_capital` et entrent dans la variable `revenus_capitaux_prelevement_forfaitaire_unique_ir`.
        En revanche, si la case 2op est cochée, les revenus des valeurs et capitaux mobiliers sont taxés au barème et non au pfu.
        Dans ce cas, ils ne sortent pas de la variable `revenu_categoriel_capital`.
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm
        imposition_au_bareme = foyer_fiscal('f2op', period)

        # Revenus à prendre en compte dans les deux cas: pfu ou imposition au barème
        f2ch = foyer_fiscal('f2ch', period)
        f2yy = foyer_fiscal('f2yy', period)

        # Revenus à prendre en compte dans un seul cas: imposition au barème
        f2ca = foyer_fiscal('f2ca', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2tr = foyer_fiscal('f2tr', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2tt = foyer_fiscal('f2tt', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)
        f2zz = foyer_fiscal('f2zz', period)

        # Revenus après abatemment
        abattement_dividende = (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement
        abattement_assurance_vie = P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses)
        abattement_residuel = max_(abattement_assurance_vie - f2ch, 0)
        abattement_residuel2 = max_(abattement_residuel - f2vv, 0)
        pre_result = where(imposition_au_bareme, f2zz + max_(f2vv - abattement_residuel, 0) + max_(f2ww - abattement_residuel2, 0) + f2fu + f2dc - abattement_dividende
            + f2ts + f2tr + f2tt + f2go * P.majoration_revenus_reputes_distribues, 0)
        rvcm_apres_abattement = (
            f2yy
            + f2ch - min_(f2ch, abattement_assurance_vie)
            + pre_result
            )
        f2ca = where(imposition_au_bareme, f2ca, 0)

        return max_(0, rvcm_apres_abattement - f2ca - deficit_rcm)

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers

        Seule différence avec la formule précédente :
            On ajoute la case 2TQ qui représente des revenus qui étaient comptés dans 2TR jusqu'en 2018.
            Source : Brochure pratique revenus 2019 page 123 et 340: https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2020/accueil.htm
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm
        imposition_au_bareme = foyer_fiscal('f2op', period)

        # Revenus à prendre en compte dans les deux cas: pfu ou imposition au barème
        f2ch = foyer_fiscal('f2ch', period)
        f2yy = foyer_fiscal('f2yy', period)

        # Revenus à prendre en compte dans un seul cas: imposition au barème
        f2ca = foyer_fiscal('f2ca', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2tr = foyer_fiscal('f2tr', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2tt = foyer_fiscal('f2tt', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)
        f2zz = foyer_fiscal('f2zz', period)
        f2tq = foyer_fiscal('f2tq', period)

        # Revenus après abatemment
        abattement_dividende = (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement
        abattement_assurance_vie = P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses)
        abattement_residuel = max_(abattement_assurance_vie - f2ch, 0)
        abattement_residuel2 = max_(abattement_residuel - f2vv, 0)
        pre_result = where(imposition_au_bareme, f2zz + max_(f2vv - abattement_residuel, 0) + max_(f2ww - abattement_residuel2, 0) + f2fu + f2dc - abattement_dividende
            + f2ts + f2tr + f2tt + f2go * P.majoration_revenus_reputes_distribues + f2tq, 0)
        rvcm_apres_abattement = (
            f2yy
            + f2ch - min_(f2ch, abattement_assurance_vie)
            + pre_result
            )
        f2ca = where(imposition_au_bareme, f2ca, 0)

        return max_(0, rvcm_apres_abattement - f2ca - deficit_rcm)

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Revenus des valeurs et capitaux mobiliers

        Seule différence avec la formule précédente :
            On ajoute la case 2TZ qui représente des revenus qui étaient comptés dans 1AI jusqu'en 2018 et n'étaient pas éligibles au pfu.
            Source : Brochure pratique revenus 2020 page 119, 132 et 364: https://www.impots.gouv.fr/www2/fichiers/documentation/brochure/ir_2021/accueil.htm
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        deficit_rcm = foyer_fiscal('deficit_rcm', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm
        imposition_au_bareme = foyer_fiscal('f2op', period)

        # Revenus à prendre en compte dans les deux cas: pfu ou imposition au barème
        f2ch = foyer_fiscal('f2ch', period)
        f2yy = foyer_fiscal('f2yy', period)

        # Revenus à prendre en compte dans un seul cas: imposition au barème
        f2ca = foyer_fiscal('f2ca', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2go = foyer_fiscal('f2go', period)
        f2tr = foyer_fiscal('f2tr', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2tt = foyer_fiscal('f2tt', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)
        f2zz = foyer_fiscal('f2zz', period)
        f2tq = foyer_fiscal('f2tq', period)
        f2tz = foyer_fiscal('f2tz', period)

        # Revenus après abatemment
        abattement_dividende = (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement
        abattement_assurance_vie = P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses)
        abattement_residuel = max_(abattement_assurance_vie - f2ch, 0)
        abattement_residuel2 = max_(abattement_residuel - f2vv, 0)
        pre_result = where(imposition_au_bareme, f2zz + max_(f2vv - abattement_residuel, 0) + max_(f2ww - abattement_residuel2, 0) + f2fu + f2dc - abattement_dividende
            + f2ts + f2tr + f2tt + f2go * P.majoration_revenus_reputes_distribues + f2tq + f2tz, 0)
        rvcm_apres_abattement = (
            f2yy
            + f2ch - min_(f2ch, abattement_assurance_vie)
            + pre_result
            )
        f2ca = where(imposition_au_bareme, f2ca, 0)

        return max_(0, rvcm_apres_abattement - f2ca - deficit_rcm)


class rfr_rvcm_abattements_a_reintegrer(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Abattement sur revenus des valeurs et capitaux mobiliers à réintégrer dans le calcul du revenu fiscal de référence'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2ts = foyer_fiscal('f2ts', period)
        f2ca = foyer_fiscal('f2ca', period)
        f2gr = foyer_fiscal('f2gr', period)
        f2fu = foyer_fiscal('f2fu', period)
        f2da = foyer_fiscal('f2da', period)  # noqa F841
        rvcm = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        # Calcul de i121
        # Part des frais s'imputant sur les revenus déclarés case DC
        den = ((f2dc + f2ts) != 0) * (f2dc + f2ts) + ((f2dc + f2ts) == 0)
        F1 = f2ca / den * f2dc  # f12
        # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
        # partie positive
        g12b = max_(f2dc * (1 - rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement * (f2da == 0)) - F1, 0)
        rev = g12b + f2gr + f2fu * (1 - rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement * (f2da == 0))

        # Abattements, limité au revenu
        h12 = rvcm.revenus_capitaux_mobiliers_dividendes.abattement_forfaitaire * (1 + maries_ou_pacses)
        i121 = - min_(0, rev - h12)
        return max_((rvcm.revenus_capitaux_mobiliers_dividendes.taux_abattement) * (f2dc + f2fu) * (f2da == 0) - i121, 0)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        abattement_dividende = (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement

        return abattement_dividende

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        2 remarques :
            - À partir de 2018, les revenus de l'assurance-vie sont taxés au PFU et entrent dans le calcul du RFR via `revenus_capitaux_prelevement_forfaitaire_unique_ir`.
              Cette variable est brute d'abattement. Or, l'abattement sur les assurance-vie se déduit bien du RFR (contrairement à celui sur les dividendes). On le rajoute donc ici en négatif dans le cas où le foyer choisit le pfu.
              Si le foyer a choisi l'imposition au barème pour les revenus éligibles au pfu, les revenus de l'assurance-vie entrent dans le calcul du RFR via `revenus_categoriel` net d'abattement.
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        imposition_au_bareme = foyer_fiscal('f2op', period)
        f2ch = foyer_fiscal('f2ch', period)
        f2dh = foyer_fiscal('f2dh', period)
        f2vv = foyer_fiscal('f2vv', period)
        f2ww = foyer_fiscal('f2ww', period)
        f2dc = foyer_fiscal('f2dc', period)
        f2fu = foyer_fiscal('f2fu', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        abattement_assurance_vie = where(imposition_au_bareme, 0,
            (f2ch < P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses)) * max_(0, min_(f2vv + f2ww, P.produits_assurances_vies_assimiles.abattement * (1 + maries_ou_pacses) - f2ch - f2dh))
            )
        abattement_dividende = where(imposition_au_bareme, (f2fu + f2dc) * P.revenus_capitaux_mobiliers_dividendes.taux_abattement, 0)

        return - abattement_assurance_vie + abattement_dividende


class revenu_categoriel_foncier(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu catégoriel - Foncier'
    reference = 'http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Revenus fonciers
        '''
        f4ba = foyer_fiscal('f4ba', period)
        f4bb = foyer_fiscal('f4bb', period)
        f4bc = foyer_fiscal('f4bc', period)
        f4bd = foyer_fiscal('f4bd', period)
        f4be = foyer_fiscal('f4be', period)
        microfoncier = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro.microfoncier

        # Messages d'erreurs
        if ((f4ba != 0) & ((f4bb != 0) | (f4bc != 0))).any():
            log.error(('Problème de déclarations des revenus : incompatibilité de la déclaration des revenus fonciers (f4ba) et de déficits (f4bb, f4bc)'))
        if ((f4be != 0) & ((f4ba != 0) | (f4bb != 0) | (f4bc != 0))).any():
            log.error(('Problème de déclarations des revenus : incompatibilité de la déclaration des revenus fonciers (f4ba, f4bb, f4bc) et microfonciers (f4be)'))
        if (f4be > microfoncier.plafond_recettes).any():
            log.error(('Problème de déclarations des revenus : les revenus microfonciers (f4be) dépassent le maximum légal'))

        micro = min_(f4be, microfoncier.plafond_recettes) * (1 - microfoncier.taux)

        # Conditions
        deficit = (f4bc > 0) | (f4bb > 0)
        micro = f4be > 0

        # Calculs
        si_deficit = -f4bc
        si_micro = min_(f4be, microfoncier.plafond_recettes) * (1 - microfoncier.taux)
        sinon = max_(0, f4ba - f4bd)

        return select([deficit, micro],
                      [si_deficit, si_micro], sinon)


class revenu_categoriel_non_salarial(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu catégoriel - Revenus personnels non salariés'
    reference = 'http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        nbnc_pvce_i = foyer_fiscal.members('nbnc_pvce', period)
        rpns_i = foyer_fiscal.members('rpns_imposables', period)
        nbnc_pvce = foyer_fiscal.sum(nbnc_pvce_i)
        rpns = foyer_fiscal.sum(rpns_i)
        defrag = foyer_fiscal('defrag', period)
        defacc = foyer_fiscal('defacc', period)
        defncn = foyer_fiscal('defncn', period)
        defmeu = foyer_fiscal('defmeu', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2

        return (
            rpns
            - (1 + cga) * nbnc_pvce
            - defrag
            - defncn
            - defacc
            - defmeu
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        rpns_i = foyer_fiscal.members('rpns_imposables', period)
        rpns = foyer_fiscal.sum(rpns_i)
        defrag = foyer_fiscal('defrag', period)
        defacc = foyer_fiscal('defacc', period)
        defncn = foyer_fiscal('defncn', period)
        defmeu = foyer_fiscal('defmeu', period)

        return (
            rpns
            - defrag
            - defncn
            - defacc
            - defmeu
            )


class revenu_categoriel(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus catégoriels'
    reference = 'http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Revenus Categoriels
        '''
        rev_cat_deductions = foyer_fiscal('revenu_categoriel_deductions', period)
        rev_cat_rvcm = foyer_fiscal('revenu_categoriel_capital', period)
        rev_cat_rfon = foyer_fiscal('revenu_categoriel_foncier', period)
        rev_cat_rpns = foyer_fiscal('revenu_categoriel_non_salarial', period)
        rev_cat_pv = foyer_fiscal('revenu_categoriel_plus_values', period)

        return rev_cat_deductions + rev_cat_rvcm + rev_cat_rfon + rev_cat_rpns + rev_cat_pv


###############################################################################
# # Déroulé du calcul de l'impot_revenu_restant_a_payer
###############################################################################


class deficit_ante(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Déficit global antérieur'
    reference = 'http://impotsurlerevenu.org/declaration-de-revenus-fonciers-2044/796-deficits-anterieurs-restant-a-imputer-cadre-450.php'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Déficits antérieurs
        '''
        f6fa = foyer_fiscal('f6fa', period)
        f6fb = foyer_fiscal('f6fb', period)
        f6fc = foyer_fiscal('f6fc', period)
        f6fd = foyer_fiscal('f6fd', period)
        f6fe = foyer_fiscal('f6fe', period)
        f6fl = foyer_fiscal('f6fl', period)

        return f6fa + f6fb + f6fc + f6fd + f6fe + f6fl


class rbg(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu brut global'
    reference = 'http://www.documentissime.fr/dossiers-droit-pratique/dossier-19-l-impot-sur-le-revenu-les-modalites-generales-d-imposition/la-determination-du-revenu-imposable/le-revenu-brut-global.html'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''Revenu brut global
        '''
        revenu_categoriel = foyer_fiscal('revenu_categoriel', period)
        deficit_ante = foyer_fiscal('deficit_ante', period)
        f6gh = foyer_fiscal('f6gh', period)
        nbic_impm_i = foyer_fiscal.members('nbic_impm', period)
        nacc_pvce_i = foyer_fiscal.members('nacc_pvce', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2

        # (Total 17)
        # sans les revenus au quotient
        nacc_pvce = foyer_fiscal.sum(nacc_pvce_i)
        return max_(0,
                    revenu_categoriel + f6gh + (foyer_fiscal.sum(nbic_impm_i) + nacc_pvce) * (1 + cga) - deficit_ante)

    def formula_2023_01_01(foyer_fiscal, period, parameters):
        '''Revenu brut global
        '''
        revenu_categoriel = foyer_fiscal('revenu_categoriel', period)
        deficit_ante = foyer_fiscal('deficit_ante', period)
        f6gh = foyer_fiscal('f6gh', period)
        return max_(0, revenu_categoriel + f6gh - deficit_ante)


class csg_patrimoine_deductible_ir(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Csg déductible sur le patrimoine'
    reference = 'http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        csg_deductible = parameters(period).taxation_capital.prelevements_sociaux.csg.taux_deductible.revenus_du_patrimoine
        rbg = foyer_fiscal('rbg', period)
        f6de = foyer_fiscal('f6de', period)
        f2bh = foyer_fiscal('f2bh', period)
        f2df = foyer_fiscal('f2df', period)
        csg_deduc_patrimoine = max_(f6de, 0) + max_(csg_deductible * (f2bh + f2df), 0)

        return min_(csg_deduc_patrimoine, max_(rbg, 0))

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Si le foyer fiscal n'opte pas pour l'imposition au barème des revenus éligibles au pfu, les revenus inscrits case 2BH n'ouvrent pas droit à csg déductible
        '''
        csg_deductible = parameters(period).taxation_capital.prelevements_sociaux.csg.taux_deductible.revenus_du_patrimoine
        imposition_au_bareme = foyer_fiscal('f2op', period)
        rbg = foyer_fiscal('rbg', period)
        f6de = foyer_fiscal('f6de', period)
        f2bh = foyer_fiscal('f2bh', period)
        f2df = foyer_fiscal('f2df', period)
        f2bh = where(imposition_au_bareme, f2bh, 0)
        csg_deduc_patrimoine = max_(f6de, 0) + max_(csg_deductible * (f2bh + f2df), 0)

        return min_(csg_deduc_patrimoine, max_(rbg, 0))


class rng(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu net global'
    reference = 'http://impotsurlerevenu.org/definitions/114-revenu-net-global.php'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rbg = foyer_fiscal('rbg', period)
        csg_patrimoine_deductible_ir = foyer_fiscal('csg_patrimoine_deductible_ir', period)
        charges_deduc = foyer_fiscal('charges_deduc', period)

        return max_(0, rbg - csg_patrimoine_deductible_ir - charges_deduc)


class rni(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu net imposable'
    reference = 'http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rng = foyer_fiscal('rng', period)
        abat_spe = foyer_fiscal('abat_spe', period)

        return rng - abat_spe


class ir_brut(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt sur le revenu brut avant non imposabilité et plafonnement du quotient'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        nbptr = foyer_fiscal('nbptr', period)
        taux_effectif = foyer_fiscal('taux_effectif', period)
        rni = foyer_fiscal('rni', period)
        bareme = parameters(period).impot_revenu.bareme_ir_depuis_1945.bareme

        return (taux_effectif == 0) * nbptr * bareme.calc(rni / nbptr) + taux_effectif * rni


class ir_taux_marginal(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Taux marginal d'imposition à l'impôt sur le revenu"
    reference = 'http://impotsurlerevenu.org/fonctionnement-de-l-impot/60-calculer-le-tmi.php'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        taux_effectif = foyer_fiscal('taux_effectif', period)
        bareme = parameters(period).impot_revenu.bareme_ir_depuis_1945.bareme
        ir_tranche = foyer_fiscal('ir_tranche', period)

        return (
            (taux_effectif == 0) * bareme.rate_from_bracket_indice(ir_tranche)
            + taux_effectif
            )


class ir_tranche(Variable):
    value_type = int
    entity = FoyerFiscal
    label = 'Tranche du barème appliquée'
    reference = 'https://impots.dispofi.fr/bareme-impot/calcul-impot-par-tranche'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        nbptr = foyer_fiscal('nbptr', period)
        rni = foyer_fiscal('rni', period)
        bareme = parameters(period).impot_revenu.bareme_ir_depuis_1945.bareme

        maries_ou_pacses_ou_jeune_veuf = foyer_fiscal('maries_ou_pacses', period) | foyer_fiscal('jeune_veuf', period)
        celibataire_ou_divorce_ou_veuf = not_(maries_ou_pacses_ou_jeune_veuf)

        # Si le plafonnement des effets du quotient familial s'applique,
        # alors le nombre de parts retenu pour le calcul de l'IR (« nbptr_retenu »)
        # est égal à 1 (contribuables célibataires, divorcés ou veufs) ou 2 (contribuables mariés ou pacsés)
        # sinon le nombre de parts retenu pour le calcul de l'IR est le nombre de parts de droit commun (« nbptr »)
        plafonnement_qf = foyer_fiscal('ir_plaf_qf', period) > foyer_fiscal('ir_brut', period)
        nbptr_retenu = where(
            plafonnement_qf,
            (celibataire_ou_divorce_ou_veuf * 1) + (maries_ou_pacses_ou_jeune_veuf * 2),
            nbptr
            )

        return bareme.bracket_indices(rni / nbptr_retenu)


class ir_ss_qf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt sans quotient familial'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Impôt sans quotient familial
        '''
        rni = foyer_fiscal('rni', period)
        nb_adult = foyer_fiscal('nb_adult', period)
        bareme = parameters(period).impot_revenu.bareme_ir_depuis_1945.bareme

        A = bareme.calc(rni / nb_adult)
        return nb_adult * A


class ir_plaf_qf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt après plafonnement du quotient familial et réduction complémentaire'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Impôt après plafonnement du quotient familial et réduction complémentaire (cf. fiche calcul IR)
        '''
        ir_brut = foyer_fiscal('ir_brut', period)
        ir_ss_qf = foyer_fiscal('ir_ss_qf', period)
        nb_adult = foyer_fiscal('nb_adult', period)
        nb_pac = foyer_fiscal('nb_pac', period)
        nb_parts = foyer_fiscal('nbptr', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        veuf = foyer_fiscal('veuf', period)
        jeune_veuf = foyer_fiscal('jeune_veuf', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        caseE = foyer_fiscal('caseE', period)
        caseF = foyer_fiscal('caseF', period)
        caseG = foyer_fiscal('caseG', period)
        annee_naissance_pac_alterne = foyer_fiscal('annee_naissance_pac_alterne', period)
        caseK = foyer_fiscal('caseK', period)
        caseN = foyer_fiscal('caseN', period)
        caseP = foyer_fiscal('caseP', period)
        caseS = foyer_fiscal('caseS', period)
        caseT = foyer_fiscal('caseT', period)
        caseW = foyer_fiscal('caseW', period)
        nbF = foyer_fiscal('nbF', period)
        nbG = foyer_fiscal('nbG', period)
        nbH = foyer_fiscal('nbH', period)
        nbI = foyer_fiscal('nbI', period)
        nbR = foyer_fiscal('nbR', period)
        plafond_qf = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf

        A = ir_ss_qf
        I = ir_brut  # noqa F741

        aa0 = (nb_parts - nb_adult) * 2  # nombre de demi part excédant nbadult
        aa1 = min_((nb_parts - 1) * 2, 2)  # deux première demi part excédants une part

        B1 = plafond_qf.plafond_avantages_procures_par_demi_part.celib_enf * aa1 / 2 + plafond_qf.plafond_avantages_procures_par_demi_part.general * (aa0 - aa1)
        B2 = plafond_qf.plafond_avantages_procures_par_demi_part.general * aa0
        B3 = plafond_qf.plafond_avantages_procures_par_demi_part.celib

        condition61 = celibataire_ou_divorce & caseT
        condition63 = (celibataire_ou_divorce | (veuf & not_(jeune_veuf))) & not_(caseN) & (nb_pac == 0) & (caseK | caseE) & (annee_naissance_pac_alterne < int(period.start.year) - 25)

        B = B1 * condition61 +\
            B2 * (not_(condition61 | condition63)) +\
            B3 * (condition63 & not_(condition61))
        C = max_(0, A - B)

        IP0 = max_(I, C)  # Impôt après plafonnement

        # 6.2 réduction d'impôt pratiquée sur l'impot après plafonnement et le cas particulier des DOM
        # pas de réduction complémentaire
        condition62a = (I >= C)  # noqa F741
        # réduction complémentaire
        condition62b = (I < C)
        # celibataire_ou_divorce veuf
        condition62caa0 = (celibataire_ou_divorce | (veuf & not_(jeune_veuf)))
        condition62caa1 = (nb_pac == 0) & (caseP | caseG | caseF | caseW)
        condition62caa2 = caseP & ((nbF - nbG > 0) | (nbH - nbI > 0))
        condition62caa3 = not_(caseN) & (caseE | caseK) & (annee_naissance_pac_alterne >= 1981)
        condition62caa = condition62caa0 & (condition62caa1 | condition62caa2 | condition62caa3)
        # marié pacs
        condition62cab = (maries_ou_pacses | jeune_veuf) & caseS & not_(caseP | caseF)

        condition62ca = (condition62caa | condition62cab)

        # plus de 590 euros si on a des plus de
        condition62cb = ((nbG + nbR + nbI) > 0) | caseP | caseF
        D = plafond_qf.plafond_avantages_procures_par_demi_part.reduc_postplafond * (condition62ca + ~condition62ca * condition62cb * (
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

        return condition62a * IP0 + condition62b * IP1  # IP2 si DOM

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Impôt après plafonnement du quotient familial et réduction complémentaire (cf. fiche calcul IR)
        '''
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        ir_brut = foyer_fiscal('ir_brut', period)
        ir_ss_qf = foyer_fiscal('ir_ss_qf', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        nb_adult = foyer_fiscal('nb_adult', period)
        nb_pac = foyer_fiscal('nb_pac', period)
        nb_parts = foyer_fiscal('nbptr', period)
        residence_fiscale_guadeloupe = foyer_fiscal('residence_fiscale_guadeloupe', period)
        residence_fiscale_martinique = foyer_fiscal('residence_fiscale_martinique', period)
        residence_fiscale_guyane = foyer_fiscal('residence_fiscale_guyane', period)
        residence_fiscale_mayotte = foyer_fiscal('residence_fiscale_mayotte', period)
        residence_fiscale_reunion = foyer_fiscal('residence_fiscale_reunion', period)
        veuf = foyer_fiscal('veuf', period)

        caseF = foyer_fiscal('caseF', period)
        caseG = foyer_fiscal('caseG', period)
        caseL = foyer_fiscal('caseL', period)
        caseP = foyer_fiscal('caseP', period)
        caseS = foyer_fiscal('caseS', period)
        caseT = foyer_fiscal('caseT', period)
        caseW = foyer_fiscal('caseW', period)
        nbF = foyer_fiscal('nbF', period)  # noqa F841
        nbG = foyer_fiscal('nbG', period)
        nbH = foyer_fiscal('nbH', period)  # noqa F841
        nbI = foyer_fiscal('nbI', period)
        nbJ = foyer_fiscal('nbI', period)  # noqa F841
        nbN = foyer_fiscal('nbJ', period)  # noqa F841
        nbR = foyer_fiscal('nbR', period)

        plafond_qf = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf

        # PART1 - PLAFONNEMENT DU QF

        A = ir_ss_qf
        I = ir_brut  # noqa F741

        aa0 = (nb_parts - nb_adult) * 2
        aa1 = min_((nb_parts - 1) * 2, 2)
        B1 = plafond_qf.plafond_avantages_procures_par_demi_part.celib_enf * aa1 / 2 + plafond_qf.plafond_avantages_procures_par_demi_part.general * (aa0 - aa1)
        B2 = plafond_qf.plafond_avantages_procures_par_demi_part.general * aa0
        B3 = plafond_qf.plafond_avantages_procures_par_demi_part.celib

        condition61 = celibataire_ou_divorce & caseT
        condition63 = (celibataire_ou_divorce | veuf) & (nb_pac == 0) & caseL

        B = B1 * condition61 +\
            B2 * (not_(condition61 | condition63)) +\
            B3 * (condition63 & not_(condition61))

        C = max_(0, A - B)

        impot_apres_plaf_qf = max_(I, C)

        # PART2 - REDUCTION IR APRES PLAFONNEMENT

        # pas de réductions complémentaires
        condition62a = (I >= C)  # noqa F741

        # possible réductions complémentaires
        condition62b = (I < C)  # noqa F741

        condition62c = (caseP | caseF | caseW | caseS | caseG | (nbG > 0) | (nbI > 0) | nbR > 0)
        condition62c0 = (caseP | caseF) | (caseW | caseS) | (caseG)
        condition62c1 = (maries_ou_pacses) & (caseP & caseF)
        condition62c2 = (nbG > 0) | (nbI > 0) | (nbR > 0)
        condition62d = (nb_pac > 0) & (veuf)

        E = condition62b * condition62c * (
            plafond_qf.plafond_avantages_procures_par_demi_part.reduc_postplafond * condition62c0 * not_(condition62c1)
            + plafond_qf.plafond_avantages_procures_par_demi_part.reduc_postplafond * 2 * condition62c1
            + plafond_qf.plafond_avantages_procures_par_demi_part.reduc_postplafond * (nbG + nbI / 2 + nbR) * condition62c2
            )

        D = condition62b * condition62d * plafond_qf.plafond_avantages_procures_par_demi_part.reduc_postplafond_veuf

        F = D + E
        G = max_(0, A - I - B)
        H = F * (F <= G) + G * (G < F)
        impot_apres_reduction_complementaire = impot_apres_plaf_qf - H

        # PART3 - ABATTEMENT PARTICULIE DOM

        residence_guadeloupe_martinique_reunion = (residence_fiscale_guadeloupe | residence_fiscale_martinique | residence_fiscale_reunion)
        residence_guyane_mayotte = (residence_fiscale_guyane | residence_fiscale_mayotte)
        residence_dom = (residence_guadeloupe_martinique_reunion | residence_guyane_mayotte)

        abattement_dom = (
            residence_guadeloupe_martinique_reunion * min_(plafond_qf.abat_dom.plaf_GuadMarReu, plafond_qf.abat_dom.taux_GuadMarReu * impot_apres_reduction_complementaire)
            + residence_guyane_mayotte * min_(plafond_qf.abat_dom.plaf_GuyMay, plafond_qf.abat_dom.taux_GuyMay * impot_apres_reduction_complementaire)
            )

        impot_apres_abattement_dom = max_(0, impot_apres_reduction_complementaire - abattement_dom)

        return (
            not_(residence_dom) * (condition62a * impot_apres_plaf_qf + condition62b * impot_apres_reduction_complementaire)
            + residence_dom * impot_apres_abattement_dom
            )


class avantage_qf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Avantage quotient familial'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        ir_ss_qf = foyer_fiscal('ir_ss_qf', period)
        ir_plaf_qf = foyer_fiscal('ir_plaf_qf', period)

        return ir_ss_qf - ir_plaf_qf


class decote(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'décote'
    definition_period = YEAR

    def formula_2001_01_01(foyer_fiscal, period, parameters):
        ir_plaf_qf = foyer_fiscal('ir_plaf_qf', period)
        decote = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf.decote

        return around(max_(0, decote.seuil - ir_plaf_qf) * decote.taux)

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        ir_plaf_qf = foyer_fiscal('ir_plaf_qf', period)
        nb_adult = foyer_fiscal('nb_adult', period)
        taux_decote = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf.decote.taux
        decote_seuil_celib = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf.decote.seuil_celib
        decote_seuil_couple = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf.decote.seuil_couple
        decote_celib = max_(0, decote_seuil_celib - taux_decote * ir_plaf_qf)
        decote_couple = max_(0, decote_seuil_couple - taux_decote * ir_plaf_qf)

        return around((nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple)


class decote_gain_fiscal(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Gain fiscal de la décote/Décote au sens Dgfip tel que sur la feuille d'impôt"
    definition_period = YEAR

    def formula_1982_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie le gain fiscal du à la décote
        '''
        decote = foyer_fiscal('decote', period)
        ir_plaf_qf = foyer_fiscal('ir_plaf_qf', period)

        return around(min_(decote, ir_plaf_qf))


class reduction_ss_condition_revenus(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt sous condition de revenus, s'imputant avant toutes autres réductions"
    definition_period = YEAR
    end = '2019-12-31'
    reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000037985566&cidTexte=LEGITEXT000006069577'
    documentation = '''
    La "réfaction foyers modestes" est abrogée par la Loi de Finances 2020.
    '''

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Réduction d'impôt sous condition de revenus
        Cette réduction instaurée en 2016 vise à adoucir un effet de seuil d'assujettissement
        à l'impôt pour les foyers fiscaux les plus modestes, elle est plus à considérer comme une
        "décote bis" qu'une réduction fiscale à proprement parler.
        '''
        ir_plaf_qf = foyer_fiscal('ir_plaf_qf', period)
        decote = foyer_fiscal('decote', period)
        nb_adult = foyer_fiscal('nb_adult', period)
        nb_parts = foyer_fiscal('nbptr', period)
        rfr = foyer_fiscal('rfr', period)
        P = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf.reduction_ss_condition_revenus

        ir_apres_plaf_qf_et_decote = ir_plaf_qf - decote
        plafond1 = P.plafond_rfr_celib * nb_adult + P.majoration_plafond_par_demi_parts_supp * 2 * (nb_parts - nb_adult)
        plafond2 = P.plafond_rfr_couple * nb_adult + P.majoration_plafond_par_demi_parts_supp * 2 * (nb_parts - nb_adult)
        reduction1 = P.taux * ir_apres_plaf_qf_et_decote
        reduction2 = P.taux * ir_apres_plaf_qf_et_decote * (plafond2 - rfr) / (plafond2 - plafond1)

        reduction_sous_condition_de_ressources = (
            (rfr < plafond1) * reduction1
            + (rfr >= plafond1) * (rfr < plafond2) * reduction2
            )

        return reduction_sous_condition_de_ressources


class nat_imp(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'nat_imp'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Renvoie True si le foyer est imposable, False sinon
        '''
        iai = foyer_fiscal('iai', period)
        credits_impot = foyer_fiscal('credits_impot', period)
        contribution_exceptionnelle_hauts_revenus = foyer_fiscal('contribution_exceptionnelle_hauts_revenus', period)

        # def _nat_imp(rni, nbptr, non_imposable = law.impot_revenu.calcul_impot_revenu.non_imposable):
        # seuil = non_imposable.seuil + (nbptr - 1)*non_imposable.supp
        return (iai - credits_impot + contribution_exceptionnelle_hauts_revenus) > 0


class ip_net(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt sur le revenu après décote et réduction sous condition de revenus, avant réductions'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Impôt net avant réductions
        '''
        decote = foyer_fiscal('decote', period)
        ir_plaf_qf = foyer_fiscal('ir_plaf_qf', period)
        # N'est pas véritablement une 'réduction', cf. la définition de cette variable
        reduction_ss_condition_revenus = foyer_fiscal('reduction_ss_condition_revenus', period)

        return around(max_(0, ir_plaf_qf - decote - reduction_ss_condition_revenus))


class iaidrdi(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt après imputation des réductions d'impôt"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Impôt après imputation des réductions d'impôt
        '''
        ip_net = foyer_fiscal('ip_net', period)
        reductions = foyer_fiscal('reductions', period)

        return ip_net - reductions


class cont_rev_loc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Contribution sur les revenus locatifs'
    definition_period = YEAR

    def formula_2001_01_01(foyer_fiscal, period, parameters):
        '''
        Contribution sur les revenus locatifs
        '''
        f4bl = foyer_fiscal('f4bl', period)
        contribution_revenus_locatifs = parameters(period).impot_revenu.contributions_exceptionnelles.contribution_revenus_locatifs

        return round_(contribution_revenus_locatifs.taux * (f4bl >= contribution_revenus_locatifs.seuil) * f4bl)


class indemnite_compensatrice_agents_assurance(Variable):  # f5rm
    value_type = float
    entity = FoyerFiscal
    label = "Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance
        '''
        bareme = parameters(period).impot_revenu.contributions_exceptionnelles.indemnite_compensatrice_agents_assurance

        f5qm = foyer_fiscal.declarant_principal('f5qm', period)
        f5rm = foyer_fiscal.conjoint('f5qm', period)

        return bareme.calc(f5qm) + bareme.calc(f5rm)


class assiette_vente(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Assiette régime microsocial avec versement libératoire pour les ventes'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Assiette régime microsocial avec versement libératoire pour les ventes
        '''
        ebic_impv_i = foyer_fiscal.members('ebic_impv', period)

        return foyer_fiscal.sum(ebic_impv_i)


class assiette_service(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Assiette régime microsocial avec versement libératoire pour les prestations et services'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Assiette régime microsocial avec versement libératoire pour les prestations et services
        '''
        ebic_imps_i = foyer_fiscal.members('ebic_imps', period)

        return foyer_fiscal.sum(ebic_imps_i)

    # P = _P.impot_revenu.calcul_revenus_imposables.rpns.micro.microentreprise
    # assert (ebic_imps <= P.servi.max)


class assiette_proflib(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Assiette régime microsocial avec versement libératoire pour les professions libérales'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Assiette régime microsocial avec versement libératoire pour les professions libérales
        '''
        ebnc_impo_i = foyer_fiscal.members('ebnc_impo', period)

        # TODO: distinction RSI/CIPAV (pour les cotisations sociales)
        # http://vosdroits.service-public.fr/professionnels-entreprises/F23267.xhtml
        return foyer_fiscal.sum(ebnc_impo_i)

    # assert (ebnc_impo <= P.microentreprise.regime_micro_bnc.services.plafond)


class microsocial(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impot libératoire régime microfiscal'
    reference = 'http://fr.wikipedia.org/wiki/R%C3%A9gime_micro-social'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        assiette_service = foyer_fiscal('assiette_service', period)
        assiette_vente = foyer_fiscal('assiette_vente', period)
        assiette_proflib = foyer_fiscal('assiette_proflib', period)
        microsocial = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.microsocial

        return (
            assiette_service * microsocial.servi
            + assiette_vente * microsocial.vente
            + assiette_proflib * microsocial.bnc
            )


class microentreprise(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'microentreprise bénéfices versement libératoire'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        ebnc_impo_i = foyer_fiscal.members('ebnc_impo', period)
        ebic_imps_i = foyer_fiscal.members('ebic_imps', period)
        ebic_impv_i = foyer_fiscal.members('ebic_impv', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro
        ebnc_impo = foyer_fiscal.sum(ebnc_impo_i)
        ebic_imps = foyer_fiscal.sum(ebic_imps_i)
        ebic_impv = foyer_fiscal.sum(ebic_impv_i)
        return (
            max_(0, ebnc_impo - max_(micro.microentreprise.montant_minimum, micro.microentreprise.regime_micro_bnc.taux * ebnc_impo))
            + max_(0, ebic_imps - max_(micro.microentreprise.montant_minimum, micro.microentreprise.regime_micro_bnc.services.taux * ebic_imps))
            + max_(0, ebic_impv - max_(micro.microentreprise.montant_minimum, micro.microentreprise.regime_micro_bnc.marchandises.taux * ebic_impv))
            )


class tax_rvcm_forfaitaire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Taxation forfaitaire des revenus des valeurs et capitaux mobiliers'
    reference = 'http://bofip.impots.gouv.fr/bofip/3727-PGP.html'
    definition_period = YEAR
    end = '2017-12-31'

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Taxation des revenus des valeurs et capitaux mobiliers
        '''
        f2fa = foyer_fiscal('f2fa', period)
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rvcm

        return f2fa * P.taux_forfaitaire


class taxation_plus_values_hors_bareme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Taxation forfaitaire des plus-values'
    reference = 'http://bofip.impots.gouv.fr/bofip/6957-PGP'
    definition_period = YEAR

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Taxation des plus values
        '''
        f3sa_2012 = foyer_fiscal('f3sa_2012', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vg = foyer_fiscal('f3vg', period)
        f3vh = foyer_fiscal('f3vh', period)
        f3vl = foyer_fiscal('f3vl', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vm = foyer_fiscal('f3vm', period)
        glo_taxation_ir_forfaitaire_taux2 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux2', period)
        glo_taxation_ir_forfaitaire_taux3 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux3', period)
        glo_taxation_ir_forfaitaire_taux4 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux4', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        pv = parameters(period).impot_revenu.calcul_impot_revenu.pv

        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        return round_(
            pv.plus_values.pvce * rpns_pvce
            + pv.pv_cession_valeurs_mobilieres_pv_professionnelles.taux * max_(0, f3vg - f3vh)
            + pv.actions_gratuites.taux2 * glo_taxation_ir_forfaitaire_taux2
            + pv.pv_cession_valeurs_mobilieres_pv_professionnelles.taux * f3vl
            + pv.pea.taux_avant_2_ans * f3vm
            + pv.pea.taux_posterieur * f3vt
            + pv.plus_values.taux_pv_entrep * f3sa_2012
            + pv.actions_gratuites.taux3 * glo_taxation_ir_forfaitaire_taux3
            + pv.actions_gratuites.taux4 * glo_taxation_ir_forfaitaire_taux4
            + pv.bspce.plus_3ans.pre_2018 * f3sj
            + pv.bspce.moins_3ans * f3sk
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Taxation des plus values (hors bareme)
        '''
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vm = foyer_fiscal('f3vm', period)
        f3vt = foyer_fiscal('f3vt', period)
        glo_taxation_ir_forfaitaire_taux2 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux2', period)
        glo_taxation_ir_forfaitaire_taux3 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux3', period)
        glo_taxation_ir_forfaitaire_taux4 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux4', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)

        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)
        pv = parameters(period).impot_revenu.calcul_impot_revenu.pv

        return round_(
            pv.plus_values.pvce * rpns_pvce
            + pv.pea.taux_avant_2_ans * f3vm
            + pv.pea.taux_posterieur * f3vt
            + pv.actions_gratuites.taux2 * glo_taxation_ir_forfaitaire_taux2
            + pv.actions_gratuites.taux3 * glo_taxation_ir_forfaitaire_taux3
            + pv.actions_gratuites.taux4 * glo_taxation_ir_forfaitaire_taux4
            + pv.bspce.plus_3ans.pre_2018 * f3sj
            + pv.bspce.moins_3ans * f3sk
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Taxation des plus values (hors bareme)
        '''
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vm = foyer_fiscal('f3vm', period)
        f3vt = foyer_fiscal('f3vt', period)
        glo_taxation_ir_forfaitaire_taux2 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux2', period)
        glo_taxation_ir_forfaitaire_taux3 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux3', period)
        glo_taxation_ir_forfaitaire_taux4 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux4', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)

        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)
        pv = parameters(period).impot_revenu.calcul_impot_revenu.pv

        return round_(
            pv.plus_values.pvce * rpns_pvce
            + pv.pea.taux_avant_2_ans * f3vm
            + pv.pea.taux_posterieur * f3vt
            + pv.actions_gratuites.taux2 * glo_taxation_ir_forfaitaire_taux2
            + pv.actions_gratuites.taux3 * glo_taxation_ir_forfaitaire_taux3
            + pv.actions_gratuites.taux4 * glo_taxation_ir_forfaitaire_taux4
            + pv.bspce.plus_3ans.pre_2018 * f3sj
            + pv.bspce.moins_3ans * f3sk
            + pv.plus_values.taux_plus_values_report * f3wi
            + pv.plus_values.taux_plus_values_report_conditionnel * f3wj
            )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Taxation des plus-values (hors imposition au barÃ¨me), en excluant, à partir de 2018, celles imposées au PFU
        (qui sont à impot_revenu/prelevements_forfaitaires/ir_prelevement_forfaitaire_unique.py)
        '''
        glo_taxation_ir_forfaitaire_taux2 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux2', period)
        glo_taxation_ir_forfaitaire_taux3 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux3', period)
        glo_taxation_ir_forfaitaire_taux4 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux4', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vm = foyer_fiscal('f3vm', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        f3pi = foyer_fiscal('f3pi', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)

        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)
        pv = parameters(period).impot_revenu.calcul_impot_revenu.pv

        return round_(
            pv.plus_values.pvce * rpns_pvce
            + pv.actions_gratuites.taux2 * glo_taxation_ir_forfaitaire_taux2
            + pv.actions_gratuites.taux3 * glo_taxation_ir_forfaitaire_taux3
            + pv.actions_gratuites.taux4 * glo_taxation_ir_forfaitaire_taux4
            + pv.bspce.plus_3ans.pre_2018 * f3sj
            + pv.bspce.moins_3ans * f3sk
            + pv.pea.taux_avant_2_ans * f3vm
            + pv.pea.taux_posterieur * f3vt
            + pv.plus_values.taux_plus_values_report * f3wi
            + pv.plus_values.taux_plus_values_report_conditionnel * f3wj
            + pv.plus_values.taux_plus_values_entc * f3pi
            )

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Taxation des plus-values (hors imposition au barème), en excluant celles imposées au PFU
        (qui sont à impot_revenu/prelevements_forfaitaires/ir_prelevement_forfaitaire_unique.py)
        '''
        glo_taxation_ir_forfaitaire_taux2 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux2', period)
        glo_taxation_ir_forfaitaire_taux3 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux3', period)
        glo_taxation_ir_forfaitaire_taux4 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux4', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        rpns_info_i = foyer_fiscal.members('rpns_info', period)

        f3pi = foyer_fiscal('f3pi', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)

        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)
        rpns_info = foyer_fiscal.sum(rpns_info_i)
        pv = parameters(period).impot_revenu.calcul_impot_revenu.pv
        P = parameters(period).impot_revenu.calcul_revenus_imposables.rpns

        return round_(
            pv.plus_values.pvce * rpns_pvce
            + pv.actions_gratuites.taux2 * glo_taxation_ir_forfaitaire_taux2
            + pv.actions_gratuites.taux3 * glo_taxation_ir_forfaitaire_taux3
            + pv.actions_gratuites.taux4 * glo_taxation_ir_forfaitaire_taux4
            + P.taux10 * rpns_info
            + pv.bspce.plus_3ans.pre_2018 * f3sj
            + pv.bspce.moins_3ans * f3sk
            + pv.plus_values.taux_plus_values_report * f3wi
            + pv.plus_values.taux_plus_values_report_conditionnel * f3wj
            + pv.plus_values.taux_plus_values_entc * f3pi
            )


class rfr_plus_values_hors_rni(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Plus-values hors RNI entrant dans le calcul du revenu fiscal de référence (PV au barème, PV éxonérées ..)'
    definition_period = YEAR

    def formula_2011_01_01(foyer_fiscal, period):
        '''
        Plus-values 2011 entrant dans le calcul du revenu fiscal de référence
        '''
        f3vc = foyer_fiscal('f3vc', period)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        f3vg = foyer_fiscal('f3vg', period)
        f3vl = foyer_fiscal('f3vl', period)
        f3vm = foyer_fiscal('f3vm', period)
        f3vp = foyer_fiscal('f3vp', period)
        f3vy = foyer_fiscal('f3vy', period)
        f3vz = foyer_fiscal('f3vz', period)
        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        return f3vc + glo_taxation_ir_forfaitaire + f3vg + f3vl + f3vm + f3vp + f3vy + f3vz + rpns_pvce

    def formula_2012_01_01(foyer_fiscal, period):
        '''
        Plus-values 2012 entrant dans le calcul du revenu fiscal de référence
        '''
        f3sa_2012 = foyer_fiscal('f3sa_2012', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vc = foyer_fiscal('f3vc', period)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        f3vg = foyer_fiscal('f3vg', period)
        f3vl = foyer_fiscal('f3vl', period)
        f3vm = foyer_fiscal('f3vm', period)
        f3vp = foyer_fiscal('f3vp', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vy = foyer_fiscal('f3vy', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3we = foyer_fiscal('f3we', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        return f3sa_2012 + f3sj + f3sk + f3vc + glo_taxation_ir_forfaitaire + f3vg + f3vl + f3vm + f3vp + f3vt + f3vy + f3vz + f3we + rpns_pvce

    def formula_2013_01_01(foyer_fiscal, period):
        '''
        Plus-values 2013-2016 entrant dans le calcul du revenu fiscal de référence
        '''
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vc = foyer_fiscal('f3vc', period)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        f3vm = foyer_fiscal('f3vm', period)
        f3vp = foyer_fiscal('f3vp', period)
        f3vq = foyer_fiscal('f3vq', period)
        f3vr = foyer_fiscal('f3vr', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vy = foyer_fiscal('f3vy', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3we = foyer_fiscal('f3we', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        return f3sj + f3sk + f3vc + glo_taxation_ir_forfaitaire + f3vm + f3vp + (f3vq - f3vr) + f3vt + f3vy + f3vz + f3we + rpns_pvce

    def formula_2016_01_01(foyer_fiscal, period):
        '''
        Plus-values 2016 et + entrant dans le calcul du revenu fiscal de référence
        '''
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3tz = foyer_fiscal('f3tz', period)
        f3vc = foyer_fiscal('f3vc', period)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        f3vm = foyer_fiscal('f3vm', period)
        f3vp = foyer_fiscal('f3vp', period)
        f3vq = foyer_fiscal('f3vq', period)
        f3vr = foyer_fiscal('f3vr', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vy = foyer_fiscal('f3vy', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3we = foyer_fiscal('f3we', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        return f3sj + f3sk + f3tz + f3vc + glo_taxation_ir_forfaitaire + f3vm + f3vp + (f3vq - f3vr) + f3vt + f3vy + f3vz + f3we + f3wi + f3wj + rpns_pvce

    def formula_2017_01_01(foyer_fiscal, period):
        '''
        Plus-values 2017 et + entrant dans le calcul du revenu fiscal de référence
        '''
        f3sj = foyer_fiscal('f3sj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3tz = foyer_fiscal('f3tz', period)
        f3vc = foyer_fiscal('f3vc', period)

        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        f3vm = foyer_fiscal('f3vm', period)
        f3vp = foyer_fiscal('f3vp', period)
        f3vq = foyer_fiscal('f3vq', period)
        f3vr = foyer_fiscal('f3vr', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vy = foyer_fiscal('f3vy', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3we = foyer_fiscal('f3we', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        f3pi = foyer_fiscal('f3pi', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        return f3sj + f3sk + f3tz + f3vc + glo_taxation_ir_forfaitaire + f3vm + f3vp + (f3vq - f3vr) + f3vt + f3vy + f3vz + f3we + f3wi + f3wj + rpns_pvce + f3pi

    def formula_2018_01_01(foyer_fiscal, period):
        '''
        Plus-values réalisées sur année 2018 entrant dans le calcul du revenu fiscal de référence.
        Si on choisit l'imposition au barème pour les revenus éligibles au pfu, les plus-values réalisées éligibles au pfu (3vg, 3tj et 3ua) sont déjà comptés dans le calcul du rfr via la variable 'rni'.
        '''
        f3vg = foyer_fiscal('f3vg', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3tj = foyer_fiscal('f3tj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vc = foyer_fiscal('f3vc', period)

        imposition_au_bareme = foyer_fiscal('f2op', period)
        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        f3vm = foyer_fiscal('f3vm', period)
        f3vq = foyer_fiscal('f3vq', period)
        f3vr = foyer_fiscal('f3vr', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3we = foyer_fiscal('f3we', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        f3pi = foyer_fiscal('f3pi', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        pre_result = where(imposition_au_bareme, 0, f3vg + f3ua + f3tj)

        return f3sj + f3sk + f3vc + glo_taxation_ir_forfaitaire + f3vm + (f3vq - f3vr) + f3vt + f3vz + f3we + f3wi + f3wj + rpns_pvce + f3pi + pre_result

    def formula_2019_01_01(foyer_fiscal, period):
        '''
        Plus-values 2019 et + entrant dans le calcul du revenu fiscal de référence.
        '''
        f3vg = foyer_fiscal('f3vg', period)
        f3ua = foyer_fiscal('f3ua', period)
        f3sj = foyer_fiscal('f3sj', period)
        f3tj = foyer_fiscal('f3tj', period)
        f3sk = foyer_fiscal('f3sk', period)
        f3vc = foyer_fiscal('f3vc', period)

        imposition_au_bareme = foyer_fiscal('f2op', period)
        glo_taxation_ir_forfaitaire = foyer_fiscal('glo_taxation_ir_forfaitaire', period)

        f3vq = foyer_fiscal('f3vq', period)
        f3vr = foyer_fiscal('f3vr', period)
        f3vt = foyer_fiscal('f3vt', period)
        f3vz = foyer_fiscal('f3vz', period)
        f3we = foyer_fiscal('f3we', period)
        f3wi = foyer_fiscal('f3wi', period)
        f3wj = foyer_fiscal('f3wj', period)
        f3an = foyer_fiscal('f3an', period)
        f3pi = foyer_fiscal('f3pi', period)

        rpns_pvce_i = foyer_fiscal.members('rpns_pvce', period)
        rpns_pvce = foyer_fiscal.sum(rpns_pvce_i)

        pre_result = where(imposition_au_bareme, 0, f3vg + f3ua + f3tj + f3vt)

        return f3sj + f3sk + f3vc + glo_taxation_ir_forfaitaire + (f3vq - f3vr) + f3vz + f3we + f3wi + f3wj + rpns_pvce + f3an + f3pi + pre_result


class iai(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt avant imputations de l'impôt sur le revenu"
    reference = 'http://forum-juridique.net-iris.fr/finances-fiscalite-assurance/43963-declaration-impots.html'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        impôt sur le revenu avant imputation
        '''
        iaidrdi = foyer_fiscal('iaidrdi', period)
        taxation_plus_values_hors_bareme = foyer_fiscal('taxation_plus_values_hors_bareme', period)
        cont_rev_loc = foyer_fiscal('cont_rev_loc', period)
        indemnite_compensatrice_agents_assurance = foyer_fiscal('indemnite_compensatrice_agents_assurance', period)

        return iaidrdi + taxation_plus_values_hors_bareme + cont_rev_loc + indemnite_compensatrice_agents_assurance

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        impôt sur le revenu avant imputation
        '''
        iaidrdi = foyer_fiscal('iaidrdi', period)
        taxation_plus_values_hors_bareme = foyer_fiscal('taxation_plus_values_hors_bareme', period)
        cont_rev_loc = foyer_fiscal('cont_rev_loc', period)
        tax_rvcm_forfaitaire = foyer_fiscal('tax_rvcm_forfaitaire', period)
        indemnite_compensatrice_agents_assurance = foyer_fiscal('indemnite_compensatrice_agents_assurance', period)

        return iaidrdi + taxation_plus_values_hors_bareme + cont_rev_loc + tax_rvcm_forfaitaire + indemnite_compensatrice_agents_assurance


class contribution_exceptionnelle_hauts_revenus(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Contribution exceptionnelle sur les hauts revenus'
    reference = 'http://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006069577&idSectionTA=LEGISCTA000025049019'
    definition_period = YEAR

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Contribution exceptionnelle sur les hauts revenus
        'foy'
        '''
        rfr = foyer_fiscal('rfr', period)
        nb_adult = foyer_fiscal('nb_adult', period)
        bareme = parameters(period).impot_revenu.contributions_exceptionnelles.contribution_exceptionnelle_hauts_revenus

        return bareme.calc(rfr / nb_adult) * nb_adult
        # TODO: Gérer le II.-1 du lissage interannuel ? (problème de non recours)


class impot_revenu_restant_a_payer(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt sur le revenu des personnes physiques restant à payer, après prise en compte des éventuels acomptes'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000041464766'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Montant après seuil de recouvrement (hors ppe)
        NB : ce montant l'impôt correspond à une notion administrative :
        dans certains cas, il existe des prélèvements à la source faisant
        office d'acomptes d'impôt sur le revenu (cf. variable acomptes_ir). Ces acomptes sont comptabilisés
        dans la feuille d'impôt comme des crédits d'impôt, mais correspondent économiquement à des montants d'impôt dus.
        Le prélèvement forfaitaire libératoire a déjà été payé il ne doit donc pas être compté dans l'impôt restant à payer.
        En revanche, il compte dans le calcul du seuil de recouvrement.
        '''
        iai = foyer_fiscal('iai', period)
        credits_impot = foyer_fiscal('credits_impot', period)
        acomptes_ir = foyer_fiscal('acomptes_ir', period)
        contribution_exceptionnelle_hauts_revenus = foyer_fiscal('contribution_exceptionnelle_hauts_revenus', period)
        prelevement_forfaitaire_unique_ir = foyer_fiscal('prelevement_forfaitaire_unique_ir', period)
        prelevement_forfaitaire_liberatoire = foyer_fiscal('prelevement_forfaitaire_liberatoire', period)
        P = parameters(period).impot_revenu.calcul_impot_revenu.recouvrement

        pre_result = iai - credits_impot - acomptes_ir + contribution_exceptionnelle_hauts_revenus - prelevement_forfaitaire_unique_ir - prelevement_forfaitaire_liberatoire
        result = iai - credits_impot - acomptes_ir + contribution_exceptionnelle_hauts_revenus - prelevement_forfaitaire_unique_ir
        impots_totaux_avant_imputations = iai + contribution_exceptionnelle_hauts_revenus - prelevement_forfaitaire_unique_ir - prelevement_forfaitaire_liberatoire

        return (
            (impots_totaux_avant_imputations > P.seuil) * (
                (pre_result < P.min)
                * (result > 0)
                * result
                * 0
                + ((pre_result <= 0) + (pre_result >= P.min))
                * (- result)
                )
            + (impots_totaux_avant_imputations <= P.seuil) * (
                (pre_result < 0)
                * (-result)
                + (pre_result >= 0)
                * 0
                * result
                )
            )


class foyer_impose(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Le foyer fiscal est imposé'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        impot_revenu_restant_a_payer = foyer_fiscal('irpp_economique', period)
        return (impot_revenu_restant_a_payer < 0)

###############################################################################
# # Autres totaux utiles pour la suite
###############################################################################


class pensions_alimentaires_versees(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Pensions alimentaires versées'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2.xhtml'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f6gi = foyer_fiscal('f6gi', period)
        f6gj = foyer_fiscal('f6gj', period)
        f6el = foyer_fiscal('f6el', period)
        f6em = foyer_fiscal('f6em', period)
        f6gp = foyer_fiscal('f6gp', period)
        f6gu = foyer_fiscal('f6gu', period)

        return -(f6gi + f6gj + f6el + f6em + f6gp + f6gu)


class rfr(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu fiscal de référence'
    reference = 'http://bofip.impots.gouv.fr/bofip/5934-PGP.html?identifiant=BOI-IF-TH-10-50-30-20-20121127#5934-PGP_Calcul_du_revenu_fiscal_de__40'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Revenu fiscal de référence
        - 01/07/2022 : Ajout PPV
        '''
        abattements_plus_values = foyer_fiscal('abattements_plus_values', period)
        f2dm = foyer_fiscal('f2dm', period)
        microentreprise = foyer_fiscal('microentreprise', period)
        rfr_rev_capitaux_mobiliers = foyer_fiscal('rfr_rvcm_abattements_a_reintegrer', period)
        revenus_capitaux_prelevement_liberatoire = foyer_fiscal('revenus_capitaux_prelevement_liberatoire', period, options = [ADD])
        revenus_capitaux_prelevement_forfaitaire_unique_ir = foyer_fiscal('revenus_capitaux_prelevement_forfaitaire_unique_ir', period, options = [ADD])
        rfr_charges_deductibles = foyer_fiscal('rfr_cd', period)
        rfr_plus_values_hors_rni = foyer_fiscal('rfr_plus_values_hors_rni', period)
        rni = foyer_fiscal('rni', period)
        imposition_au_bareme = foyer_fiscal('f2op', period)
        f3sb = foyer_fiscal('f3sb', period)  # Dans le cas de l'imposition au barème des revenus éligibles au pfu, les plus-values en report d'imposition qui sont imposables pour la période concernée sont comptées dans le rni mais ne doivent pas être comptées dans le rfr.
        rpns_exon_i = foyer_fiscal.members('rpns_exon', period)
        rpns_info_i = foyer_fiscal.members('rpns_info', period)

        rpns_info = foyer_fiscal.sum(rpns_info_i)
        rpns_exon = foyer_fiscal.sum(rpns_exon_i)

        # Ajout de la PPV : Le reste de la PPV est compris dans le RNI (donc au total c'est bien
        # l'ensemble de la PPV qui est compris dans le RFR).
        prime_partage_valeur_exoneree_exceptionnelle_i = foyer_fiscal.members('prime_partage_valeur_exoneree_exceptionnelle', period)
        # TODO: On applique ici l'abattement de 10% mais idéalement il faudrait tenir compte des frais réels le cas échéant.
        prime_partage_valeur_exoneree_exceptionnelle = (foyer_fiscal.sum(prime_partage_valeur_exoneree_exceptionnelle_i) * 0.9)

        f3sb = where(imposition_au_bareme, f3sb, 0)

        return (
            max_(0, rni - f3sb)
            + rfr_charges_deductibles + rfr_plus_values_hors_rni + rfr_rev_capitaux_mobiliers + revenus_capitaux_prelevement_liberatoire + revenus_capitaux_prelevement_forfaitaire_unique_ir
            + rpns_exon + rpns_info
            + abattements_plus_values
            + f2dm + microentreprise
            + prime_partage_valeur_exoneree_exceptionnelle
            )

        # TO CHECK : f3vb after 2015 (abattements sur moins-values = interdits)


class glo_taxation_ir_forfaitaire_taux2(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        On crée cette variable étant donné que ces revenus sont renseignés jusqu'à 2014 dans des cases individuelles, et à partir de 2015 dans
        des cases à l'échelle du foyer fiscal. Créer cette variable intermédiaire permet d'alléger le code dans les formules dépendant de ces
        revenus.
        NB : la législation sur les GLO a été checkée en août 2023 à partir de 2017 seulement.
        '''
        f3vd_i = foyer_fiscal.members('f3vd_2014', period)
        f3vd = foyer_fiscal.sum(f3vd_i)

        return f3vd

    def formula_2015_01_01(foyer_fiscal, period):
        f3vd = foyer_fiscal('f3vd', period)

        return f3vd


class glo_taxation_ir_forfaitaire_taux3(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        On crée cette variable étant donné que ces revenus sont renseignés jusqu'à 2014 dans des cases individuelles, et à partir de 2015 dans
        des cases à l'échelle du foyer fiscal. Créer cette variable intermédiaire permet d'alléger le code dans les formules dépendant de ces
        revenus.
        NB : la législation sur les GLO a été checkée en août 2023 à partir de 2017 seulement.
        '''
        f3vi_i = foyer_fiscal.members('f3vi_2014', period)
        f3vi = foyer_fiscal.sum(f3vi_i)

        return f3vi

    def formula_2015_01_01(foyer_fiscal, period):
        f3vi = foyer_fiscal('f3vi', period)

        return f3vi


class glo_taxation_ir_forfaitaire_taux4(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        On crée cette variable étant donné que ces revenus sont renseignés jusqu'à 2014 dans des cases individuelles, et à partir de 2015 dans
        des cases à l'échelle du foyer fiscal. Créer cette variable intermédiaire permet d'alléger le code dans les formules dépendant de ces
        revenus.
        NB : la législation sur les GLO a été checkée en août 2023 à partir de 2017 seulement.
        '''
        f3vf_i = foyer_fiscal.members('f3vf_2014', period)
        f3vf = foyer_fiscal.sum(f3vf_i)

        return f3vf

    def formula_2015_01_01(foyer_fiscal, period):
        f3vf = foyer_fiscal('f3vf', period)

        return f3vf


class glo_taxation_ir_forfaitaire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Gains de levée d'options taxés forfaitairement à l'IR"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        NB : la législation sur les GLO a été checkée en août 2023 à partir de 2017 seulement.
        '''
        glo_taxation_ir_forfaitaire_taux2 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux2', period)
        glo_taxation_ir_forfaitaire_taux3 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux3', period)
        glo_taxation_ir_forfaitaire_taux4 = foyer_fiscal('glo_taxation_ir_forfaitaire_taux4', period)

        return glo_taxation_ir_forfaitaire_taux2 + glo_taxation_ir_forfaitaire_taux3 + glo_taxation_ir_forfaitaire_taux4


class credits_impot_sur_valeurs_etrangeres(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Avoir fiscal et crédits d'impôt"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f2ab = foyer_fiscal('f2ab', period)

        return f2ab


class rpns_pvce(Variable):
    value_type = float
    entity = Individu
    label = 'Plus values de cession nettes des moins-values - Revenu des professions non salariées'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Plus values de cession
        '''
        frag_pvce = individu('frag_pvce', period)
        arag_pvce = individu('arag_pvce', period)
        mrag_pvce = individu('mrag_pvce', period)
        mbic_pvce = individu('mbic_pvce', period)
        abic_pvce = individu('abic_pvce', period)
        macc_pvce = individu('macc_pvce', period)
        aacc_pvce = individu('aacc_pvce', period)
        mbnc_pvce = individu('mbnc_pvce', period)
        abnc_pvce = individu('abnc_pvce', period)
        mncn_pvce = individu('mncn_pvce', period)
        cncn_pvce = individu('cncn_pvce', period)
        cncn_info = individu('cncn_info', period)
        moins_values_long_terme_non_salaries = individu('moins_values_long_terme_non_salaries', period)

        return (
            frag_pvce
            + arag_pvce
            + mrag_pvce
            + mbic_pvce
            + abic_pvce
            + macc_pvce
            + aacc_pvce
            + mbnc_pvce
            + abnc_pvce
            + mncn_pvce
            + cncn_pvce
            + cncn_info
            - moins_values_long_terme_non_salaries
            )


class rpns_info(Variable):
    value_type = float
    entity = Individu
    label = 'Plus values de cession de brevets, logiciels ou inventions - Revenu des professions non salariées'
    definition_period = YEAR

    def formula_2019_01_01(individu, period, parameters):
        '''
        Plus values de cession
        '''
        cncn_info_red1 = individu('cncn_info_red1', period)
        cncn_info_red2 = individu('cncn_info_red2', period)
        arag_info = individu('arag_info', period)
        abic_info = individu('abic_info', period)
        aacc_info = individu('aacc_info', period)
        abnc_info = individu('abnc_info', period)

        return (
            cncn_info_red1
            + cncn_info_red2
            + arag_info
            + abic_info
            + aacc_info
            + abnc_info
            )


class rpns_exon(Variable):
    value_type = float
    entity = Individu
    label = 'Plus values de cession exonérées -Revenu des professions non salariées'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Plus values de cession
        '''
        frag_exon = individu('frag_exon', period)
        arag_exon = individu('arag_exon', period)
        nrag_exon = individu('nrag_exon', period)
        mbic_exon = individu('mbic_exon', period)
        abic_exon = individu('abic_exon', period)
        nbnc_proc = individu('nbnc_proc', period)
        nbic_exon = individu('nbic_exon', period)
        macc_exon = individu('macc_exon', period)
        aacc_exon = individu('aacc_exon', period)
        nacc_exon = individu('nacc_exon', period)
        mbnc_exon = individu('mbnc_exon', period)
        abnc_proc = individu('abnc_proc', period)
        nrag_pvce = individu('nrag_pvce', period)
        abnc_exon = individu('abnc_exon', period)
        nbnc_exon = individu('nbnc_exon', period)
        mncn_exon = individu('mncn_exon', period)
        cncn_jcre = individu('cncn_jcre', period)
        nbic_pvce = individu('nbic_pvce', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2

        return (
            frag_exon + arag_exon + nrag_exon + mbic_exon + abic_exon + nbnc_proc * (1 + cga)
            + nbic_exon + macc_exon + aacc_exon + nacc_exon + mbnc_exon + abnc_proc
            + abnc_exon + nbnc_exon + mncn_exon + cncn_jcre + nbic_pvce + nrag_pvce
            )

    def formula_2008_01_01(individu, period, parameters):
        '''
        Plus values de cession
        '''
        frag_exon = individu('frag_exon', period)
        arag_exon = individu('arag_exon', period)
        nrag_exon = individu('nrag_exon', period)
        mbic_exon = individu('mbic_exon', period)
        abic_exon = individu('abic_exon', period)
        nbnc_proc = individu('nbnc_proc', period)
        nbic_exon = individu('nbic_exon', period)
        macc_exon = individu('macc_exon', period)
        aacc_exon = individu('aacc_exon', period)
        nacc_exon = individu('nacc_exon', period)
        mbnc_exon = individu('mbnc_exon', period)
        abnc_proc = individu('abnc_proc', period)
        abnc_exon = individu('abnc_exon', period)
        nbnc_exon = individu('nbnc_exon', period)
        mncn_exon = individu('mncn_exon', period)
        cncn_exon = individu('cncn_exon', period)
        cncn_jcre = individu('cncn_jcre', period)
        nbic_pvce = individu('nbic_pvce', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2

        return (
            frag_exon + arag_exon + nrag_exon + mbic_exon + abic_exon + nbnc_proc * (1 + cga)
            + nbic_exon + macc_exon + aacc_exon + nacc_exon + mbnc_exon + abnc_proc
            + abnc_exon + nbnc_exon + mncn_exon + cncn_exon + cncn_jcre + nbic_pvce
            )

    def formula_2016_01_01(individu, period, parameters):
        '''
        Plus values de cession
        '''
        mrag_exon = individu('mrag_exon', period)
        arag_exon = individu('arag_exon', period)
        nrag_exon = individu('nrag_exon', period)
        mbic_exon = individu('mbic_exon', period)
        abic_exon = individu('abic_exon', period)
        nbnc_proc = individu('nbnc_proc', period)
        nbic_exon = individu('nbic_exon', period)
        macc_exon = individu('macc_exon', period)
        aacc_exon = individu('aacc_exon', period)
        nacc_exon = individu('nacc_exon', period)
        mbnc_exon = individu('mbnc_exon', period)
        abnc_proc = individu('abnc_proc', period)
        abnc_exon = individu('abnc_exon', period)
        nbnc_exon = individu('nbnc_exon', period)
        mncn_exon = individu('mncn_exon', period)
        cncn_exon = individu('cncn_exon', period)
        cncn_jcre = individu('cncn_jcre', period)
        nbic_pvce = individu('nbic_pvce', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2

        return (
            mrag_exon + arag_exon + nrag_exon + mbic_exon + abic_exon + nbnc_proc * (1 + cga)
            + nbic_exon + macc_exon + aacc_exon + nacc_exon + mbnc_exon + abnc_proc
            + abnc_exon + nbnc_exon + mncn_exon + cncn_exon + cncn_jcre + nbic_pvce
            )

    def formula_2018_01_01(individu, period, parameters):
        '''
        Plus values de cession
        '''
        mrag_exon = individu('mrag_exon', period)
        arag_exon = individu('arag_exon', period)
        nrag_exon = individu('nrag_exon', period)
        mbic_exon = individu('mbic_exon', period)
        abic_exon = individu('abic_exon', period)
        nbic_exon = individu('nbic_exon', period)
        macc_exon = individu('macc_exon', period)
        aacc_exon = individu('aacc_exon', period)
        nacc_exon = individu('nacc_exon', period)
        mbnc_exon = individu('mbnc_exon', period)
        abnc_proc = individu('abnc_proc', period)
        abnc_exon = individu('abnc_exon', period)
        nbnc_exon = individu('nbnc_exon', period)
        mncn_exon = individu('mncn_exon', period)
        cncn_exon = individu('cncn_exon', period)
        cncn_jcre = individu('cncn_jcre', period)
        nbic_pvce = individu('nbic_pvce', period)

        return (
            mrag_exon + arag_exon + nrag_exon + mbic_exon + abic_exon
            + nbic_exon + macc_exon + aacc_exon + nacc_exon + mbnc_exon + abnc_proc
            + abnc_exon + nbnc_exon + mncn_exon + cncn_exon + cncn_jcre + nbic_pvce
            )

    def formula_2023_01_01(individu, period, parameters):
        '''
        Plus values de cession
        '''
        mrag_exon = individu('mrag_exon', period)
        arag_exon = individu('arag_exon', period)
        mbic_exon = individu('mbic_exon', period)
        abic_exon = individu('abic_exon', period)
        macc_exon = individu('macc_exon', period)
        aacc_exon = individu('aacc_exon', period)
        mbnc_exon = individu('mbnc_exon', period)
        abnc_exon = individu('abnc_exon', period)
        mncn_exon = individu('mncn_exon', period)
        cncn_exon = individu('cncn_exon', period)
        cncn_jcre = individu('cncn_jcre', period)

        return (
            mrag_exon + arag_exon + mbic_exon + abic_exon
            + macc_exon + aacc_exon + mbnc_exon
            + abnc_exon + mncn_exon + cncn_exon + cncn_jcre
            )


class defrag(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Déficit agricole des années antérieures'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f5qf = foyer_fiscal('f5qf', period)
        f5qg = foyer_fiscal('f5qg', period)
        f5qn = foyer_fiscal('f5qn', period)
        f5qo = foyer_fiscal('f5qo', period)
        f5qp = foyer_fiscal('f5qp', period)
        f5qq = foyer_fiscal('f5qq', period)
        frag_impo_i = foyer_fiscal.members('frag_impo', period)
        mrag_impo_i = foyer_fiscal.members('mrag_impo', period)
        nrag_impg_i = foyer_fiscal.members('nrag_impg', period)
        frag_fore_i = foyer_fiscal.members('frag_fore', period)
        frag_pvct_i = foyer_fiscal.members('frag_pvct', period)
        arag_impg_i = foyer_fiscal.members('arag_impg', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2

        frag_fore = foyer_fiscal.sum(frag_fore_i)
        frag_impo = foyer_fiscal.sum(frag_impo_i)
        mrag_impo = foyer_fiscal.sum(mrag_impo_i)
        arag_impg = foyer_fiscal.sum(arag_impg_i)
        nrag_impg = foyer_fiscal.sum(nrag_impg_i)
        frag_pvct = foyer_fiscal.sum(frag_pvct_i)
        return min_(f5qf + f5qg + f5qn + f5qo + f5qp + f5qq, (1 + cga) * (frag_impo + nrag_impg + frag_pvct)
                    + arag_impg + frag_fore + mrag_impo)

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        # frag_fore est remplacé par coupe_bois, frag_pvct par mrag_pvct
        f5qf = foyer_fiscal('f5qf', period)
        f5qg = foyer_fiscal('f5qg', period)
        f5qn = foyer_fiscal('f5qn', period)
        f5qo = foyer_fiscal('f5qo', period)
        f5qp = foyer_fiscal('f5qp', period)
        f5qq = foyer_fiscal('f5qq', period)
        mrag_impo_i = foyer_fiscal.members('mrag_impo', period)
        nrag_impg_i = foyer_fiscal.members('nrag_impg', period)
        coupe_bois_i = foyer_fiscal.members('coupe_bois', period)
        mrag_pvct_i = foyer_fiscal.members('mrag_pvct', period)
        arag_impg_i = foyer_fiscal.members('arag_impg', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2

        coupe_bois = foyer_fiscal.sum(coupe_bois_i)
        mrag_impo = foyer_fiscal.sum(mrag_impo_i)
        arag_impg = foyer_fiscal.sum(arag_impg_i)
        nrag_impg = foyer_fiscal.sum(nrag_impg_i)
        mrag_pvct = foyer_fiscal.sum(mrag_pvct_i)
        return min_(f5qf + f5qg + f5qn + f5qo + f5qp + f5qq, (1 + cga) * (nrag_impg + mrag_pvct)
                    + arag_impg + coupe_bois + mrag_impo)

    def formula_2023_01_01(foyer_fiscal, period, parameters):
        f5qf = foyer_fiscal('f5qf', period)
        f5qg = foyer_fiscal('f5qg', period)
        f5qn = foyer_fiscal('f5qn', period)
        f5qo = foyer_fiscal('f5qo', period)
        f5qp = foyer_fiscal('f5qp', period)
        f5qq = foyer_fiscal('f5qq', period)
        mrag_impo_i = foyer_fiscal.members('mrag_impo', period)
        coupe_bois_i = foyer_fiscal.members('coupe_bois', period)
        arag_impg_i = foyer_fiscal.members('arag_impg', period)

        coupe_bois = foyer_fiscal.sum(coupe_bois_i)
        mrag_impo = foyer_fiscal.sum(mrag_impo_i)
        arag_impg = foyer_fiscal.sum(arag_impg_i)
        return min_(f5qf + f5qg + f5qn + f5qo + f5qp + f5qq, arag_impg + coupe_bois + mrag_impo)


class defacc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Déficit industriels et commerciaux non professionnels des années antérieures'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f5rn = foyer_fiscal('f5rn', period)
        f5ro = foyer_fiscal('f5ro', period)
        f5rp = foyer_fiscal('f5rp', period)
        f5rq = foyer_fiscal('f5rq', period)
        f5rr = foyer_fiscal('f5rr', period)
        f5rw = foyer_fiscal('f5rw', period)
        macc_impv_i = foyer_fiscal.members('macc_impv', period)
        macc_imps_i = foyer_fiscal.members('macc_imps', period)
        nacc_impn_i = foyer_fiscal.members('nacc_impn', period)
        macc_pvct_i = foyer_fiscal.members('macc_pvct', period)
        aacc_impn_i = foyer_fiscal.members('aacc_impn', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.plafond, rev), micro.microentreprise.montant_minimum)))

        nacc_impn = foyer_fiscal.sum(nacc_impn_i)
        macc_pvct = foyer_fiscal.sum(macc_pvct_i)
        macc_impv = foyer_fiscal.sum(macc_impv_i)
        macc_imps = foyer_fiscal.sum(macc_imps_i)
        aacc_impn = foyer_fiscal.sum(aacc_impn_i)
        macc_timp = abat_rpns(macc_impv, micro.microentreprise.regime_micro_bnc.marchandises) + abat_rpns(macc_imps, micro.microentreprise.regime_micro_bnc.services)
        return (
            min_(f5rn + f5ro + f5rp + f5rq + f5rr + f5rw, aacc_impn + macc_pvct + macc_timp + (1 + cga) * nacc_impn)
            )

    def formula_2023_01_01(foyer_fiscal, period, parameters):
        f5rn = foyer_fiscal('f5rn', period)
        f5ro = foyer_fiscal('f5ro', period)
        f5rp = foyer_fiscal('f5rp', period)
        f5rq = foyer_fiscal('f5rq', period)
        f5rr = foyer_fiscal('f5rr', period)
        f5rw = foyer_fiscal('f5rw', period)
        macc_impv_i = foyer_fiscal.members('macc_impv', period)
        macc_imps_i = foyer_fiscal.members('macc_imps', period)
        macc_pvct_i = foyer_fiscal.members('macc_pvct', period)
        aacc_impn_i = foyer_fiscal.members('aacc_impn', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.plafond, rev), micro.microentreprise.montant_minimum)))

        macc_pvct = foyer_fiscal.sum(macc_pvct_i)
        macc_impv = foyer_fiscal.sum(macc_impv_i)
        macc_imps = foyer_fiscal.sum(macc_imps_i)
        aacc_impn = foyer_fiscal.sum(aacc_impn_i)
        macc_timp = abat_rpns(macc_impv, micro.microentreprise.regime_micro_bnc.marchandises) + abat_rpns(macc_imps, micro.microentreprise.regime_micro_bnc.services)
        return (
            min_(f5rn + f5ro + f5rp + f5rq + f5rr + f5rw, aacc_impn + macc_pvct + macc_timp)
            )


class defncn(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Déficit non commerciaux non professionnels des années antérieures'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f5ht = foyer_fiscal('f5ht', period)
        f5it = foyer_fiscal('f5it', period)
        f5jt = foyer_fiscal('f5jt', period)
        f5kt = foyer_fiscal('f5kt', period)
        f5lt = foyer_fiscal('f5lt', period)
        f5mt = foyer_fiscal('f5mt', period)
        mncn_impo_i = foyer_fiscal.members('mncn_impo', period)
        mncn_pvct_i = foyer_fiscal.members('mncn_pvct', period)
        cncn_aimp_i = foyer_fiscal.members('cncn_aimp', period)
        cncn_bene_i = foyer_fiscal.members('cncn_bene', period)
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro
        specialbnc = micro.microentreprise.regime_micro_bnc

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.plafond, rev), micro.microentreprise.montant_minimum)))
        cncn_bene = foyer_fiscal.sum(cncn_bene_i)
        mncn_impo = foyer_fiscal.sum(mncn_impo_i)
        mncn_pvct = foyer_fiscal.sum(mncn_pvct_i)
        cncn_aimp = foyer_fiscal.sum(cncn_aimp_i)
        return min_(
            f5ht + f5it + f5jt + f5kt + f5lt + f5mt,
            abat_rpns(mncn_impo, specialbnc.services) + mncn_pvct + cncn_aimp + (1 + cga) * cncn_bene
            )  # TODO check !

    def formula_2023_01_01(foyer_fiscal, period, parameters):
        f5ht = foyer_fiscal('f5ht', period)
        f5it = foyer_fiscal('f5it', period)
        f5jt = foyer_fiscal('f5jt', period)
        f5kt = foyer_fiscal('f5kt', period)
        f5lt = foyer_fiscal('f5lt', period)
        f5mt = foyer_fiscal('f5mt', period)
        mncn_impo_i = foyer_fiscal.members('mncn_impo', period)
        mncn_pvct_i = foyer_fiscal.members('mncn_pvct', period)
        cncn_aimp_i = foyer_fiscal.members('cncn_aimp', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro
        specialbnc = micro.microentreprise.regime_micro_bnc

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.plafond, rev), micro.microentreprise.montant_minimum)))
        mncn_impo = foyer_fiscal.sum(mncn_impo_i)
        mncn_pvct = foyer_fiscal.sum(mncn_pvct_i)
        cncn_aimp = foyer_fiscal.sum(cncn_aimp_i)
        return min_(
            f5ht + f5it + f5jt + f5kt + f5lt + f5mt,
            abat_rpns(mncn_impo, specialbnc.services) + mncn_pvct + cncn_aimp
            )  # TODO check !


class defmeu(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Déficit des locations meublées non professionnelles des années antérieures'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        f5ga = foyer_fiscal('f5ga', period)
        f5gb = foyer_fiscal('f5gb', period)
        f5gc = foyer_fiscal('f5gc', period)
        f5gd = foyer_fiscal('f5gd', period)
        f5ge = foyer_fiscal('f5ge', period)
        f5gf = foyer_fiscal('f5gf', period)
        f5gg = foyer_fiscal('f5gg', period)
        f5gh = foyer_fiscal('f5gh', period)
        f5gi = foyer_fiscal('f5gi', period)
        f5gj = foyer_fiscal('f5gj', period)
        alnp_imps_i = foyer_fiscal.members('alnp_imps', period)
        nacc_pres_i = foyer_fiscal.members('nacc_pres', period)

        nacc_pres = foyer_fiscal.sum(nacc_pres_i)
        alnp_imps = foyer_fiscal.sum(alnp_imps_i)
        return min_(f5ga + f5gb + f5gc + f5gd + f5ge + f5gf + f5gg + f5gh + f5gi + f5gj, alnp_imps + nacc_pres)


class rpns_pvct(Variable):
    value_type = float
    entity = Individu
    label = 'Plus values de court terme -Revenu des professions non salariées'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Plus values de court terme
        '''
        frag_pvct = individu('frag_pvct', period)
        mbic_pvct = individu('mbic_pvct', period)
        macc_pvct = individu('macc_pvct', period)
        mbnc_pvct = individu('mbnc_pvct', period)
        mncn_pvct = individu('mncn_pvct', period)

        return frag_pvct + macc_pvct + mbic_pvct + mbnc_pvct + mncn_pvct

    def formula_2016_01_01(individu, period, parameters):
        '''
        Plus values de court terme
        '''
        mrag_pvct = individu('mrag_pvct', period)
        mbic_pvct = individu('mbic_pvct', period)
        macc_pvct = individu('macc_pvct', period)
        mbnc_pvct = individu('mbnc_pvct', period)
        mncn_pvct = individu('mncn_pvct', period)

        return mrag_pvct + macc_pvct + mbic_pvct + mbnc_pvct + mncn_pvct


class moins_values_court_terme_nonpro(Variable):
    value_type = float
    entity = Individu
    label = 'Moins values de court terme - Revenu des professions non salariées non professionnelles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        macc_mvct = individu.foyer_fiscal('macc_mvct', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        mncn_mvct = individu.foyer_fiscal('mncn_mvct', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return macc_mvct + mncn_mvct


class moins_values_court_terme_pro(Variable):
    value_type = float
    entity = Individu
    label = 'Moins values de court terme - Revenu des professions non salariées professionnelles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        mbic_mvct = individu.foyer_fiscal('mbic_mvct', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        mbnc_mvct = individu('mbnc_mvct', period)

        return mbic_mvct + mbnc_mvct

    def formula_2012_01_01(individu, period, parameters):
        nbic_mvct = individu('nbic_mvct', period)
        mbnc_mvct = individu('mbnc_mvct', period)

        return nbic_mvct + mbnc_mvct


class moins_values_court_terme_agr(Variable):
    value_type = float
    entity = Individu
    label = 'Moins values de court terme - Revenu des professions agricoles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        mrag_mvct = individu('mrag_mvct', period)

        return mrag_mvct


class moins_values_court_terme_non_salaries(Variable):
    value_type = float
    entity = Individu
    label = 'Moins values de court terme - Revenu des professions non salariées (toutes)'
    definition_period = YEAR

    def formula(individu, period, parameters):
        rpns_mvct_pro = individu('moins_values_court_terme_pro', period)
        rpns_mvct_nonpro = individu('moins_values_court_terme_nonpro', period)
        rpns_mvct_agr = individu('moins_values_court_terme_agr', period)

        return rpns_mvct_pro + rpns_mvct_nonpro + rpns_mvct_agr


class moins_values_long_terme_non_salaries(Variable):
    value_type = float
    entity = Individu
    label = 'Moins values de long terme - Revenu des professions non salariées'
    definition_period = YEAR

    def formula(individu, period, parameters):
        mbic_mvlt = individu('mbic_mvlt', period)
        mrag_mvlt = individu('mrag_mvlt', period)
        macc_mvlt = individu('macc_mvlt', period)
        mbnc_mvlt = individu('mbnc_mvlt', period)
        mncn_mvlt = individu('mncn_mvlt', period)

        return mbic_mvlt + macc_mvlt + mbnc_mvlt + mncn_mvlt + mrag_mvlt


class rpns_revenus_forfait_agricole(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus du forfait agricole - Revenus des professions non salariées'
    definition_period = YEAR
    end = '2015-12-31'

    def formula(individu, period, parameters):

        frag_impo = individu('frag_impo', period)

        return frag_impo


class rpns_revenus_microBA_agricole(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus agricoles imposables en régime microBA - Revenus des professions non salariées'
    # start_date = date(2016, 1, 1)
    definition_period = YEAR

    def formula_2016_01_01(individu, period, parameters):
        mrag_impo = individu('mrag_impo', period)
        frag_impo_n2 = individu('frag_impo_n2', period)
        frag_impo_n1 = individu('frag_impo_n1', period)
        arag_impo_n2 = individu('arag_impo_n2', period)
        arag_impo_n1 = individu('arag_impo_n1', period)
        date_creation = individu('date_creation', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        frag_impo_n2_maj = frag_impo_n2 * (1 + micro.microentreprise.regime_micro_ba.maj_frag)
        frag_impo_n1_maj = frag_impo_n1 * (1 + micro.microentreprise.regime_micro_ba.maj_frag)
        benefices_estimes_3 = (mrag_impo + frag_impo_n2_maj + arag_impo_n2 + frag_impo_n1_maj + arag_impo_n1) / 3
        benefices_estimes_2 = (mrag_impo + frag_impo_n1_maj + arag_impo_n1) / 2

        montant_benef = (
            (date_creation < 2015) * benefices_estimes_3
            + (date_creation == 2015) * benefices_estimes_2
            + (date_creation == 2016) * mrag_impo
            )

        return montant_benef * (1 - micro.microentreprise.regime_micro_ba.taux)

    def formula_2017_01_01(individu, period, parameters):
        mrag_impo = individu('mrag_impo', period)
        frag_impo_n2 = individu('frag_impo_n2', period)
        frag_impo_n1 = individu('frag_impo_n1', period)
        arag_impo_n2 = individu('arag_impo_n2', period)
        date_creation = individu('date_creation', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        frag_impo_n2_maj = frag_impo_n2 * (1 + micro.microentreprise.regime_micro_ba.maj_frag)
        benefices_estimes_3 = (mrag_impo + frag_impo_n2_maj + arag_impo_n2 + frag_impo_n1) / 3
        benefices_estimes_2 = (mrag_impo + frag_impo_n1) / 2

        montant_benef = (
            (date_creation < 2016) * benefices_estimes_3
            + (date_creation == 2016) * benefices_estimes_2
            + (date_creation == 2017) * mrag_impo
            )

        return montant_benef * (1 - micro.microentreprise.regime_micro_ba.taux)

    def formula_2018_01_01(individu, period, parameters):
        mrag_impo = individu('mrag_impo', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        return mrag_impo * (1 - micro.microentreprise.regime_micro_ba.taux)


class aacc_timp(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus des professions non salariées individuels avec abattement CGA'
    definition_period = YEAR

    def formula(individu, period, parameters):
        aacc_impn = individu('aacc_impn', period)
        aacc_defn = individu('aacc_defn', period)
        aacc_defs = individu('aacc_defs', period)
        aacc_timp = max_(0, aacc_impn - aacc_defn - aacc_defs)
        return aacc_timp

    def formula_2009_01_01(individu, period, parameters):
        aacc_impn = individu('aacc_impn', period)
        alnp_defs = individu('alnp_defs', period)
        aacc_defn = individu('aacc_defn', period)
        aacc_defs = individu('aacc_defs', period)
        aacc_timp = max_(0, aacc_impn + max_(0, - alnp_defs) - aacc_defn - aacc_defs)
        return aacc_timp

    def formula_2010_01_01(individu, period, parameters):
        aacc_impn = individu('aacc_impn', period)
        alnp_defs = individu('alnp_defs', period)
        aacc_defn = individu('aacc_defn', period)
        aacc_timp = max_(0, aacc_impn + max_(0, - alnp_defs) - aacc_defn)
        return aacc_timp

    def formula_2011_01_01(individu, period, parameters):
        aacc_impn = individu('aacc_impn', period)
        aacc_gits = individu('aacc_gits', period)
        aacc_imps = individu('aacc_imps', period)
        alnp_defs = individu('alnp_defs', period)
        aacc_defn = individu('aacc_defn', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro
        aacc_timp = (
            max_(
                0,
                (aacc_impn + (aacc_gits > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    aacc_gits * (1 - micro.microentreprise.regime_micro_bnc.marchandises.taux)
                    ))
                + (aacc_imps > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    aacc_imps * (1 - micro.microentreprise.regime_micro_bnc.services.taux)
                    )
                + max_(0, - alnp_defs) - aacc_defn
                )
            )
        return aacc_timp

    def formula_2012_01_01(individu, period, parameters):
        aacc_impn = individu('aacc_impn', period)
        aacc_gits = individu('aacc_gits', period)
        aacc_imps = individu('aacc_imps', period)
        nacc_meup = individu('nacc_meup', period)
        nacc_pres = individu('nacc_pres', period)
        alnp_defs = individu('alnp_defs', period)
        aacc_defn = individu('aacc_defn', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro
        aacc_timp = (
            max_(
                0,
                (aacc_impn + (aacc_gits > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    aacc_gits * (1 - micro.microentreprise.regime_micro_bnc.marchandises.taux)
                    ))
                + (aacc_imps > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    aacc_imps * (1 - micro.microentreprise.regime_micro_bnc.services.taux)
                    )
                + (nacc_meup > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    nacc_meup * (1 - micro.microentreprise.regime_micro_bnc.marchandises.taux)
                    )
                + max_(0, nacc_pres - alnp_defs) - aacc_defn
                )
            )
        return aacc_timp

    def formula_2017_01_01(individu, period, parameters):
        aacc_impn = individu('aacc_impn', period)
        aacc_gits = individu('aacc_gits', period)
        aacc_imps = individu('aacc_imps', period)
        nacc_meup = individu('nacc_meup', period)
        nacc_meuc = individu('nacc_meuc', period)
        nacc_pres = individu('nacc_pres', period)
        alnp_defs = individu('alnp_defs', period)
        aacc_defn = individu('aacc_defn', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro
        aacc_timp = (
            max_(
                0,
                (aacc_impn + (aacc_gits > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    aacc_gits * (1 - micro.microentreprise.regime_micro_bnc.marchandises.taux)
                    ))
                + (aacc_imps > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    aacc_imps * (1 - micro.microentreprise.regime_micro_bnc.services.taux)
                    )
                + (nacc_meup > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    nacc_meup * (1 - micro.microentreprise.regime_micro_bnc.marchandises.taux)
                    )
                + (nacc_meuc > 0) * max_(
                    micro.microentreprise.montant_minimum,
                    nacc_meuc * (1 - micro.microentreprise.regime_micro_bnc.services.taux)
                    )
                + max_(0, nacc_pres - alnp_defs) - aacc_defn
                )
            )
        return aacc_timp


class atimp(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus des professions non salariées individuels avec abattement'
    definition_period = YEAR

    def formula(individu, period, parameters):
        abic_impn = individu('abic_impn', period)
        abic_imps = individu('abic_imps', period)
        abic_defn = individu('abic_defn', period)
        abic_defs = individu('abic_defs', period)
        arag_impg = individu('arag_impg', period)
        abnc_impo = individu('abnc_impo', period)
        abnc_defi = individu('abnc_defi', period)
        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        aacc_timp = individu('aacc_timp', period)
        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        abic_timp = abic_impn + abic_imps - (abic_defn + abic_defs)
        # regime de la déclaration contrôlée bénéficiant de l'abattement CGA
        abnc_timp = abnc_impo - abnc_defi
        # Total
        atimp = arag_impg + abic_timp + aacc_timp + abnc_timp
        return atimp

    def formula_2010_01_01(individu, period, parameters):
        abic_impn = individu('abic_impn', period)
        abic_defn = individu('abic_defn', period)
        arag_impg = individu('arag_impg', period)
        abnc_impo = individu('abnc_impo', period)
        abnc_defi = individu('abnc_defi', period)
        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        aacc_timp = individu('aacc_timp', period)
        # Régime du bénéfice réel bénéficiant de l'abattement CGA
        abic_timp = abic_impn - abic_defn
        # regime de la déclaration contrôlée bénéficiant de l'abattement CGA
        abnc_timp = abnc_impo - abnc_defi
        # Total
        atimp = arag_impg + abic_timp + aacc_timp + abnc_timp
        return atimp


class nbnc_timp(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus des professions non salariées individuels sans abattement CGA (régime contrôlé)'
    end = '2022-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        nbnc_impo = individu('nbnc_impo', period)
        nbnc_defi = individu('nbnc_defi', period)
        # regime de la déclaration contrôlée ne bénéficiant pas de l'abattement CGA
        nbnc_timp = nbnc_impo - nbnc_defi
        return nbnc_timp


class nacc_timp(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus des professions non salariées individuels sans abattement CGA (régime réel)'
    end = '2022-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        nacc_impn = individu('nacc_impn', period)
        nacc_defn = individu('nacc_defn', period)
        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nacc_timp = max_(0, nacc_impn - nacc_defn)
        return nacc_timp


class ntimp(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus des professions non salariées individuels sans abattement'
    end = '2022-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        nbic_impn = individu('nbic_impn', period)
        nbic_imps = individu('nbic_imps', period)
        nbic_defn = individu('nbic_defn', period)
        nbic_defs = individu('nbic_defs', period)
        nacc_timp = individu('nacc_timp', period)
        nbnc_timp = individu('nbnc_timp', period)
        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)
        ntimp = nacc_timp + nbnc_timp + nbic_timp
        return ntimp

    def formula_2006_01_01(individu, period, parameters):
        nbic_impn = individu('nbic_impn', period)
        nbic_imps = individu('nbic_imps', period)
        nbic_defn = individu('nbic_defn', period)
        nbic_defs = individu('nbic_defs', period)
        nacc_timp = individu('nacc_timp', period)
        nbnc_timp = individu('nbnc_timp', period)
        cncn_bene = individu('cncn_bene', period)
        cncn_defi = individu('cncn_defi', period)
        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)
        cncn_timp = max_(0, cncn_bene - cncn_defi)
        ntimp = nbic_timp + nacc_timp + nbnc_timp + cncn_timp
        return ntimp

    def formula_2007_01_01(individu, period, parameters):
        # Moyenne triennale
        nrag_impg = individu('nrag_impg', period)
        nbic_impn = individu('nbic_impn', period)
        nbic_imps = individu('nbic_imps', period)
        nbic_defn = individu('nbic_defn', period)
        nbic_defs = individu('nbic_defs', period)
        nacc_timp = individu('nacc_timp', period)
        nbnc_timp = individu('nbnc_timp', period)
        cncn_bene = individu('cncn_bene', period)
        cncn_defi = individu('cncn_defi', period)
        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)
        cncn_timp = max_(0, cncn_bene - cncn_defi)
        ntimp = nrag_impg + nbic_timp + nacc_timp + cncn_timp + nbnc_timp
        return ntimp

    def formula_2010_01_01(individu, period, parameters):
        nrag_impg = individu('nrag_impg', period)
        nbic_impn = individu('nbic_impn', period)
        nbic_defn = individu('nbic_defn', period)
        nacc_timp = individu('nacc_timp', period)
        nbnc_timp = individu('nbnc_timp', period)
        cncn_bene = individu('cncn_bene', period)
        cncn_defi = individu('cncn_defi', period)
        # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
        nbic_timp = nbic_impn - nbic_defn
        cncn_timp = max_(0, cncn_bene - cncn_defi)
        ntimp = nrag_impg + nbic_timp + nacc_timp + cncn_timp + nbnc_timp
        return ntimp


class revenu_non_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus des professions non salariées individuels'
    definition_period = YEAR

    def formula(individu, period, parameters):
        rpns_frag = individu('rpns_revenus_forfait_agricole', period)
        frag_fore = individu('frag_fore', period)
        f5sq = individu('f5sq', period)
        arag_defi = individu('arag_defi', period)
        nrag_defi = individu('nrag_defi', period)
        atimp = individu('atimp', period)
        ntimp = individu('ntimp', period)
        cga_taux2 = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2
        majo_cga = max_(0, cga_taux2 * (ntimp + rpns_frag))  # Pour ne pas avoir à majorer les déficits
        def_agri = f5sq + arag_defi + (1 + cga_taux2) * nrag_defi
        revenus_non_salaries = rpns_frag + frag_fore + atimp + ntimp + majo_cga - def_agri
        return revenus_non_salaries

    def formula_2016_01_01(individu, period, parameters):
        rpns_mrag = individu('rpns_revenus_microBA_agricole', period)
        coupe_bois = individu('coupe_bois', period)
        arag_defi = individu('arag_defi', period)
        nrag_defi = individu('nrag_defi', period)
        atimp = individu('atimp', period)
        ntimp = individu('ntimp', period)
        cga_taux2 = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2
        majo_cga = max_(0, cga_taux2 * ntimp)  # Pour ne pas avoir à majorer les déficits
        def_agri = arag_defi + (1 + cga_taux2) * nrag_defi
        revenus_non_salaries = rpns_mrag + coupe_bois + atimp + ntimp + majo_cga - def_agri
        return revenus_non_salaries

    def formula_2023_01_01(individu, period, parameters):
        # Il n'y a plus de majoration pour absence de CGA (ntimp disparait)
        rpns_mrag = individu('rpns_revenus_microBA_agricole', period)
        coupe_bois = individu('coupe_bois', period)
        arag_defi = individu('arag_defi', period)
        atimp = individu('atimp', period)
        revenus_non_salaries = rpns_mrag + coupe_bois + atimp - arag_defi
        return revenus_non_salaries


class locations_pro(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus des locations meublées'
    definition_period = YEAR

    def formula_2009_01_01(individu, period, parameters):
        abic_impm = individu('abic_impm', period)
        abic_defm = individu('abic_defm', period)
        alnp_imps = individu('alnp_imps', period)
        return abic_impm - abic_defm + alnp_imps

    def formula_2016_01_01(individu, period, parameters):
        alnp_imps = individu('alnp_imps', period)
        return alnp_imps


class rpns_imposables(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus imposable des professions non salariées individuels'
    definition_period = YEAR

    def formula(individu, period, parameters):
        revenu_non_salarie = individu('revenu_non_salarie', period)
        nacc_timp = individu('nacc_timp', period)
        mbic_impv = individu('mbic_impv', period)
        rpns_pvct = individu('rpns_pvct', period)
        mbic_imps = individu('mbic_imps', period)
        macc_impv = individu('macc_impv', period)
        macc_imps = individu('macc_imps', period)
        mbnc_impo = individu('mbnc_impo', period)
        mncn_impo = individu('mncn_impo', period)
        cncn_aimp = individu('cncn_aimp', period)
        rpns_mvct_pro = individu('moins_values_court_terme_pro', period)
        rpns_mvct_agr = individu('moins_values_court_terme_agr', period)
        rpns_mvct_nonpro = individu('moins_values_court_terme_nonpro', period)  # noqa F841
        locations_pro = individu('locations_pro', period)
        micro = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        def abat_rpns(rev, P):
            return max_(0, rev - min_(rev, max_(P.taux * min_(P.plafond, rev), micro.microentreprise.montant_minimum)))

        # # B revenus industriels et commerciaux professionnels
        # regime micro entreprise
        mbic_timp = abat_rpns(mbic_impv, micro.microentreprise.regime_micro_bnc.marchandises) + abat_rpns(mbic_imps, micro.microentreprise.regime_micro_bnc.services)
        # regime micro entreprise
        macc_timp = abat_rpns(macc_impv, micro.microentreprise.regime_micro_bnc.marchandises) + abat_rpns(macc_imps, micro.microentreprise.regime_micro_bnc.services)
        # # D revenus non commerciaux professionnels
        # regime déclaratif special ou micro-bnc
        mbnc_timp = abat_rpns(mbnc_impo, micro.microentreprise.regime_micro_bnc.services)
        # # E revenus non commerciaux non professionnels
        # regime déclaratif special ou micro-bnc
        mncn_timp = abat_rpns(mncn_impo, micro.microentreprise.regime_micro_bnc.services)
        macc_mvct = individu.foyer_fiscal('macc_mvct', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        mncn_mvct = individu.foyer_fiscal('mncn_mvct', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        rev_ns_mi = mbic_timp + max_(0, macc_timp) + mbnc_timp + mncn_timp
        exon_acc = max_(0, macc_timp + nacc_timp - macc_mvct) - macc_timp - nacc_timp  # ajout artificiel
        exon_ncn = max_(0, mncn_timp - mncn_mvct) - mncn_timp

        return (
            revenu_non_salarie + rev_ns_mi + rpns_pvct + exon_acc + exon_ncn
            + locations_pro + cncn_aimp - rpns_mvct_pro - rpns_mvct_agr - rpns_mvct_nonpro
            )


class abat_spe(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Abattements spéciaux'
    reference = 'http://bofip.impots.gouv.fr/bofip/2036-PGP'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Abattements spéciaux pour :

        - pour personnes âges ou invalides ;
        - pour enfants à charge ayant fondé un foyer distinct.
        '''

        # Âge déclarant·e principal·e
        age_declarant = foyer_fiscal.declarant_principal('age', period.first_month)

        # Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte
        # d'invalidité d'au moins 80%
        declarant_invalide = foyer_fiscal('caseP', period)

        # Âge conjoint·e
        age_conjoint = foyer_fiscal.conjoint('age', period.first_month)

        # Conjoint·e titulaire d'une pension ou d'une carte d'invalidité (vivant ou
        # décédé l'année de perception des revenus)
        conjoint_invalide = foyer_fiscal('caseF', period)

        # Revenu net global
        revenu_net_global = foyer_fiscal('rng', period)

        # Nombre d'enfants marié·e·s/pacse·é·s et d'enfants non mari·é·s charg·é·s de
        # famille
        nombre_enfants = foyer_fiscal('nbN', period)

        # Abattements pour revenu net imposable
        abattements = parameters(period).impot_revenu.calcul_revenus_imposables.abat_rni

        # Abattement pour personnes agées de + de 65 ans ou invalide
        abattement_age_ou_invalidite = abattements.personne_agee_ou_invalide

        # Abattement pour rattachement d'enfants mari·é·s
        abattement_enfant_marie = abattements.enfant_marie

        # Vecteur de foyers eligibles aux abattements spéciaux
        foyers_eligibles = (
            (((age_declarant >= 65) | declarant_invalide) & (age_declarant > 0))
            + (((age_conjoint >= 65) | conjoint_invalide) & (age_conjoint > 0))
            )

        # Vecteur de montants d'abattement pour personnes âges ou invalides
        as_inv = (
            foyers_eligibles
            * (
                (
                    + abattement_age_ou_invalidite.montant_1
                    * (revenu_net_global <= abattement_age_ou_invalidite.plafond_1)
                    )
                + (
                    + abattement_age_ou_invalidite.montant_2
                    * (
                        (revenu_net_global > abattement_age_ou_invalidite.plafond_1)
                        & (revenu_net_global <= abattement_age_ou_invalidite.plafond_2)
                        )
                    )
                )
            )

        # Vecteur de montants d'abattement pour enfants à charge
        as_enf = (
            nombre_enfants
            * abattement_enfant_marie.montant
            )

        # Le montant total d'abattement ne peut pas être supérieur au revenu net global
        return min_(revenu_net_global, as_inv + as_enf)


class taux_effectif(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "La règle du taux effectif a pour objet de maintenir intégralement la progressivité de l'impôt"
    definition_period = YEAR
    reference = 'https://bofip.impots.gouv.fr/bofip/4616-PGP.html/identifiant=BOI-IR-LIQ-20-30-30-20120912'
    documentation = '''
        Cette règle du « taux effectif » s'applique notamment et sous certaines conditions :
        - aux salariés détachés à l'étranger
        - aux fonctionnaires des organisations internationales
        - aux contribuables soumis au régime micro-entreprise
        '''

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        rni = foyer_fiscal('rni', period)
        nbptr = foyer_fiscal('nbptr', period)
        microentreprise = foyer_fiscal('microentreprise', period)
        abnc_proc_i = foyer_fiscal.members('abnc_proc', period)
        nbnc_proc_i = foyer_fiscal.members('nbnc_proc', period)
        bareme = parameters(period).impot_revenu.bareme_ir_depuis_1945.bareme
        cga = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.cga_taux2
        abnc_proc = foyer_fiscal.sum(abnc_proc_i)
        nbnc_proc = foyer_fiscal.sum(nbnc_proc_i)
        base_fictive = rni + microentreprise + abnc_proc + nbnc_proc * (1 + cga)
        trigger = (microentreprise != 0) | (abnc_proc != 0) | (nbnc_proc != 0)
        return trigger * nbptr * bareme.calc(base_fictive / nbptr) / max_(1, base_fictive)

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        rni = foyer_fiscal('rni', period)
        nbptr = foyer_fiscal('nbptr', period)
        microentreprise = foyer_fiscal('microentreprise', period)
        abnc_proc_i = foyer_fiscal.members('abnc_proc', period)
        bareme = parameters(period).impot_revenu.bareme_ir_depuis_1945.bareme
        abnc_proc = foyer_fiscal.sum(abnc_proc_i)
        base_fictive = rni + microentreprise + abnc_proc
        trigger = (microentreprise != 0) | (abnc_proc != 0)
        return trigger * nbptr * bareme.calc(base_fictive / nbptr) / max_(1, base_fictive)


class taux_moyen_imposition(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Taux moyen d'imposition"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rni = foyer_fiscal('rni', period)
        impot_revenu_restant_a_payer = foyer_fiscal('impot_revenu_restant_a_payer', period)
        return (
            (- impot_revenu_restant_a_payer) / (rni + (rni == 0))
            ) * (rni > 0)


# Calcul du nombre de parts

class nbptr(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Nombre de parts'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2705.xhtml'
    definition_period = YEAR

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Modification de la prise en compte des enfants à charge du conjoint décédé et du veuf.
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        veuf = foyer_fiscal('veuf', period)
        jeune_veuf = foyer_fiscal('jeune_veuf', period)
        nbG = foyer_fiscal('nbG', period)
        nbH = foyer_fiscal('nbH', period)
        nbI = foyer_fiscal('nbI', period)
        nbR = foyer_fiscal('nbR', period)
        nbN = foyer_fiscal('nbN', period)  # noqa F841
        caseP = foyer_fiscal('caseP', period)
        caseW = foyer_fiscal('caseW', period)
        caseG = foyer_fiscal('caseG', period)
        caseE = foyer_fiscal('caseE', period)
        caseK = foyer_fiscal('caseK', period)
        caseN = foyer_fiscal('caseN', period)
        caseF = foyer_fiscal('caseF', period)
        caseS = foyer_fiscal('caseS', period)
        caseL = foyer_fiscal('caseL', period)
        caseT = foyer_fiscal('caseT', period)
        quotient_familial = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf.quotient_familial

        no_pac = nb_pac == 0  # Aucune personne à charge en garde exclusive
        has_pac = not_(no_pac)
        no_alt = nbH == 0  # Aucun enfant à charge en garde alternée
        has_alt = not_(no_alt)

        # nombre de parts liées aux enfants à charge

        # parts des enfants en résidence alternée quand il n'y a que des enfants en résidence alternée
        enf_a = (no_pac & has_alt) * (
            quotient_familial.enf1 * min_(nbH, 1)
            + quotient_familial.enf2 * max_(min_(nbH - 1, 1), 0)
            + quotient_familial.enf3_et_sup * max_(nbH - 2, 0)
            ) * 0.5
        # parts des enfants en résidence alternée quand il y a aussi des enfants entièrement à charge
        enf_b = (has_pac & has_alt) * (
            (nb_pac == 1) * (
                quotient_familial.enf2 * min_(nbH, 1)
                + quotient_familial.enf3_et_sup * max_(nbH - 1, 0)
                ) * 0.5
            + (nb_pac > 1) * (quotient_familial.enf3_et_sup * nbH * 0.5)
            )
        # parts des enfants entièrement à charge
        enf_c = (
            quotient_familial.enf1 * min_(nb_pac, 1)
            + quotient_familial.enf2 * max_(min_(nb_pac - 1, 1), 0)
            + quotient_familial.enf3_et_sup * max_(nb_pac - 2, 0)
            )

        enf = enf_a + enf_b + enf_c

        # # note 2 : nombre de parts liées aux invalides (enfant + adulte)
        n2 = quotient_familial.inv1 * (nbG + nbI / 2) + quotient_familial.inv2 * nbR

        # # note 3 : Pas de personne à charge
        # - invalide

        n31a = quotient_familial.sans_pers_a_charge.not31a * (no_pac & no_alt & caseP)
        # - ancien combatant
        n31b = quotient_familial.sans_pers_a_charge.not31b * (no_pac & no_alt & (caseW | caseG))
        n31 = max_(n31a, n31b)
        # - personne seule ayant élevé des enfants
        n32 = quotient_familial.sans_pers_a_charge.not32 * (no_pac & no_alt & ((caseE | caseK | caseL) & not_(caseN)))
        n3 = max_(n31, n32)
        # # note 4 Invalidité de la personne ou du conjoint pour les mariés ou
        # # jeunes veuf(ve)s
        n4 = max_(quotient_familial.not41 * (1 * caseP + 1 * caseF), quotient_familial.not42 * (caseW | caseS))

        # # note 5
        #  - enfant autre et parent isolé
        n5 = quotient_familial.isol * caseT * (((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2))) + 1 * has_pac)

        # # note 6 invalide avec personne à charge
        n6 = quotient_familial.not6 * (caseP & (has_pac | has_alt))

        # # note 7 Parent isolé
        n7 = quotient_familial.isol * caseT * ((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2)) + 1 * has_pac)

        # # Régime des mariés ou pacsés
        nb_parts_famille = 1 + quotient_familial.conj + enf + n2 + n4

        # # veufs  hors jeune_veuf
        nb_parts_veuf = 1 + quotient_familial.veuf * (has_pac | has_alt) + enf + n2 + n3 + n5 + n6

        # # celib div
        nb_parts_celib = 1 + enf + n2 + n3 + n6 + n7

        return (maries_ou_pacses | jeune_veuf) * nb_parts_famille + (veuf & not_(jeune_veuf)) * nb_parts_veuf + celibataire_ou_divorce * nb_parts_celib

    def formula(foyer_fiscal, period, parameters):
        '''
        Nombre de parts du foyer fiscal

        note 1 enfants et résidence alternée (formulaire 2041 GV page 10)

        quotient_familial.conj : nb part associées au conjoint d'un couple marié ou pacsé
        quotient_familial.enf1 : nb part premier enfant
        quotient_familial.enf2 : nb part deuxième enfant
        quotient_familial.enf3_et_sup : nb part enfants de rang 3 ou plus
        quotient_familial.inv1 : nb part supp enfants invalides (I, G)
        quotient_familial.inv2 : nb part supp adultes invalides (R)
        quotient_familial.sans_pers_a_charge.not31 : nb part supp note 3 : cases W ou G pour veuf, celib ou div
        quotient_familial.sans_pers_a_charge.not32 : nb part supp note 3 : personne seule ayant élevé des enfants
        quotient_familial.not41 : nb part supp adultes invalides (vous et/ou conjoint) note 4
        quotient_familial.not42 : nb part supp adultes anciens combattants (vous et/ou conjoint) note 4
        quotient_familial.not6 : nb part supp note 6
        quotient_familial.isol : demi-part parent isolé (T)
        quotient_familial.edcd : enfant issu du mariage avec conjoint décédé;
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        veuf = foyer_fiscal('veuf', period)
        jeune_veuf = foyer_fiscal('jeune_veuf', period)
        nbF = foyer_fiscal('nbF', period)
        nbG = foyer_fiscal('nbG', period)
        nbH = foyer_fiscal('nbH', period)
        nbI = foyer_fiscal('nbI', period)
        nbR = foyer_fiscal('nbR', period)
        nbJ = foyer_fiscal('nbJ', period)
        nbN = foyer_fiscal('nbN', period)  # noqa F841
        caseP = foyer_fiscal('caseP', period)
        caseW = foyer_fiscal('caseW', period)
        caseG = foyer_fiscal('caseG', period)
        caseE = foyer_fiscal('caseE', period)
        caseK = foyer_fiscal('caseK', period)
        caseN = foyer_fiscal('caseN', period)
        caseF = foyer_fiscal('caseF', period)
        caseS = foyer_fiscal('caseS', period)
        caseL = foyer_fiscal('caseL', period)
        caseT = foyer_fiscal('caseT', period)
        quotient_familial = parameters(period).impot_revenu.calcul_impot_revenu.plaf_qf.quotient_familial

        no_pac = nb_pac == 0  # Aucune personne à charge en garde exclusive
        has_pac = not_(no_pac)
        no_alt = nbH == 0  # Aucun enfant à charge en garde alternée
        has_alt = not_(no_alt)

        # nombre de parts liées aux enfants à charge

        # parts des enfants en résidence alternée quand il n'y a que des enfants en résidence alternée
        enf_a = (no_pac & has_alt) * (
            quotient_familial.enf1 * min_(nbH, 1)
            + quotient_familial.enf2 * max_(min_(nbH - 1, 1), 0)
            + quotient_familial.enf3_et_sup * max_(nbH - 2, 0)
            ) * 0.5
        # parts des enfants en résidence alternée quand il y a aussi des enfants entièrement à charge
        enf_b = (has_pac & has_alt) * (
            (nb_pac == 1) * (
                quotient_familial.enf2 * min_(nbH, 1)
                + quotient_familial.enf3_et_sup * max_(nbH - 1, 0)
                ) * 0.5
            + (nb_pac > 1) * (quotient_familial.enf3_et_sup * nbH * 0.5)
            )
        # parts des enfants entièrement à charge
        enf_c = (
            quotient_familial.enf1 * min_(nb_pac, 1)
            + quotient_familial.enf2 * max_(min_(nb_pac - 1, 1), 0)
            + quotient_familial.enf3_et_sup * max_(nb_pac - 2, 0)
            )

        enf = enf_a + enf_b + enf_c

        # # note 2 : nombre de parts liées aux invalides (enfant + adulte)
        n2 = quotient_familial.inv1 * (nbG + nbI / 2) + quotient_familial.inv2 * nbR

        # # note 3 : Pas de personne à charge
        # - invalide

        n31a = quotient_familial.sans_pers_a_charge.not31a * (no_pac & no_alt & caseP)
        # - ancien combatant
        n31b = quotient_familial.sans_pers_a_charge.not31b * (no_pac & no_alt & (caseW | caseG))
        n31 = max_(n31a, n31b)
        # - personne seule ayant élevé des enfants
        n32 = quotient_familial.sans_pers_a_charge.not32 * (no_pac & no_alt & ((caseE | caseK | caseL) & not_(caseN)))
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
        nb_parts_famille = 1 + quotient_familial.conj + enf + n2 + n4

        # # veufs  hors jeune_veuf
        nb_parts_veuf = 1 + enf + n2 + n3 + n5 + n6

        # # celib div
        nb_parts_celib = 1 + enf + n2 + n3 + n6 + n7

        return (maries_ou_pacses | jeune_veuf) * nb_parts_famille + (veuf & not_(jeune_veuf)) * nb_parts_veuf + celibataire_ou_divorce * nb_parts_celib


# Calcul de la prime pour l'emploi

class ppe_coef(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Coefficient de conversion - Prime pour l'emploi"
    end = '2015-12-31'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        PPE: coefficient de conversion en cas de changement en cours d'année
        '''
        jour_xyz = foyer_fiscal('jour_xyz', period)

        nb_jour = (jour_xyz == 0) + jour_xyz
        return 360 / nb_jour


class ppe_elig(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence'
    end = '2015-12-31'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence
        CF ligne 1: http://bofip.impots.gouv.fr/bofip/3913-PGP.html
        '''
        rfr = foyer_fiscal('rfr', period)
        ppe_coef = foyer_fiscal('ppe_coef', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        veuf = foyer_fiscal('veuf', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        nbptr = foyer_fiscal('nbptr', period)
        ppe = parameters(period).impot_revenu.credits_impots.ppe

        seuil = (
            (veuf | celibataire_ou_divorce) * (ppe.seuils_rfr_eligibilite.personne_seule + 2 * max_(nbptr - 1, 0) * ppe.seuils_rfr_eligibilite.increment_par_demi_part)
            + maries_ou_pacses * (ppe.seuils_rfr_eligibilite.couple_marie_pacse + 2 * max_(nbptr - 2, 0) * ppe.seuils_rfr_eligibilite.increment_par_demi_part)
            )

        return (rfr * ppe_coef) <= seuil


class ppe_rev(Variable):
    value_type = float
    entity = Individu
    label = 'Base ressource de la ppe'
    end = '2015-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        salaire_imposable = individu('salaire_imposable', period, options = [ADD])
        hsup = individu('hsup', period, options = [ADD])
        rpns = individu('rpns_imposables', period)
        ppe = parameters(period).impot_revenu.credits_impots.ppe

        # Revenu d'activité salarié
        rev_sa = salaire_imposable + hsup  # TODO: + TV + TW + TX + AQ + LZ + VJ
        # Revenu d'activité non salarié
        rev_ns = min_(0, rpns) / ppe.abatns + max_(0, rpns) * ppe.abatns
        # très bizarre la partie min(0, rpns) - après vérification c'est dans la loi
        return rev_sa + rev_ns


class ppe_coef_tp(Variable):
    value_type = float
    entity = Individu
    label = 'PPE: coefficient de conversion temps partiel'
    end = '2015-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        ppe_du_sa = individu('ppe_du_sa', period, options = [ADD])
        ppe_du_ns = individu('ppe_du_ns', period)
        ppe_tp_sa = individu('ppe_tp_sa', period)
        ppe_tp_ns = individu('ppe_tp_ns', period)
        ppe = parameters(period).impot_revenu.credits_impots.ppe

        frac_sa = ppe_du_sa / ppe.TP_nbh
        frac_ns = ppe_du_ns / ppe.TP_nbj
        tp = ppe_tp_sa | ppe_tp_ns | ((frac_sa + frac_ns) >= 1)
        return where(tp, 1.00, frac_sa + frac_ns)


class ppe_base(Variable):
    value_type = float
    entity = Individu
    label = 'Montant de base de la PPE'
    end = '2015-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        ppe_rev = individu('ppe_rev', period)
        ppe_coef_tp = individu('ppe_coef_tp', period)
        ppe_coef = individu.foyer_fiscal('ppe_coef', period)

        return ppe_rev / (ppe_coef_tp + (ppe_coef_tp == 0)) * ppe_coef


class ppe_elig_individu(Variable):
    value_type = bool
    entity = Individu
    label = 'Eligibilité individuelle à la ppe'
    end = '2015-12-31'
    definition_period = YEAR

    def formula(individu, period, parameters):
        '''
        Eligibilité individuelle à la ppe
        Attention : condition de plafonnement introduite dans ppe brute
        '''
        ppe_rev = individu('ppe_rev', period)
        ppe_coef_tp = individu('ppe_coef_tp', period)
        ppe_seuils = parameters(period).impot_revenu.credits_impots.ppe.seuils_revenu_activite

        return (ppe_rev >= ppe_seuils.minimum) & (ppe_coef_tp != 0)


class ppe_brute(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Prime pour l'emploi brute"
    end = '2015-12-31'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Prime pour l'emploi (avant éventuel dispositif de cumul avec le RSA)
        Cf. http://travail-emploi.gouv.fr/informations-pratiques,89/fiches-pratiques,91/remuneration,113/la-prime-pour-l-emploi-ppe,1034.html
        '''
        ppe_elig = foyer_fiscal('ppe_elig', period)
        ppe_coef = foyer_fiscal('ppe_coef', period)
        nb_pac = foyer_fiscal('nb_pac', period)
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        celibataire_ou_divorce = foyer_fiscal('celibataire_ou_divorce', period)
        veuf = foyer_fiscal('veuf', period)
        caseT = foyer_fiscal('caseT', period)
        caseL = foyer_fiscal('caseL', period)
        nbH = foyer_fiscal('nbH', period)
        ppe = parameters(period).impot_revenu.credits_impots.ppe
        ppe_seuils = parameters(period).impot_revenu.credits_impots.ppe.seuils_revenu_activite

        eliv = foyer_fiscal.declarant_principal('ppe_elig_individu', period)
        elic = foyer_fiscal.conjoint('ppe_elig_individu', period)
        eligible_i = foyer_fiscal.members('ppe_elig_individu', period)

        basevi = foyer_fiscal.declarant_principal('ppe_rev', period)
        baseci = foyer_fiscal.conjoint('ppe_rev', period)

        basev = foyer_fiscal.declarant_principal('ppe_base', period)
        basec = foyer_fiscal.conjoint('ppe_base', period)
        base_i = foyer_fiscal.members('ppe_base', period)

        coef_tpv = foyer_fiscal.declarant_principal('ppe_coef_tp', period)
        coef_tpc = foyer_fiscal.conjoint('ppe_coef_tp', period)
        coef_tp_i = foyer_fiscal.members('ppe_coef_tp', period)

        nb_pac_ppe = max_(0, nb_pac - foyer_fiscal.sum(eligible_i, role = FoyerFiscal.PERSONNE_A_CHARGE))

        ligne2 = maries_ou_pacses & xor_(basevi >= ppe_seuils.minimum, baseci >= ppe_seuils.minimum)
        ligne3 = (celibataire_ou_divorce | veuf) & caseT & not_(veuf & caseT & caseL)
        ligne1 = not_(ligne2) & not_(ligne3)

        base_monact = ligne2 * (eliv * basev + elic * basec)
        base_monacti = ligne2 * (eliv * basevi + elic * baseci)

        def ppe_bar1(base):
            # cond1 = ligne1 | ligne3
            # cond2 = ligne2
            # return 1 / ppe_coef * ((cond1 & (base <= ppe_seuils.pour_taux_plein_cas_general)) * (base) * ppe.taux.phase_in +
            #     (cond1 & (base > ppe_seuils.pour_taux_plein_cas_general) & (base <= ppe_seuils.maximum_cas_general)) * (ppe_seuils.maximum_cas_general - base) * ppe.taux.phase_out_cas_general +
            #     (cond2 & (base <= ppe_seuils.pour_taux_plein_cas_general)) * (base * ppe.taux.phase_in) +
            #     (cond2 & (base > ppe_seuils.pour_taux_plein_cas_general) & (base <= ppe_seuils.maximum_cas_general)) * ((ppe_seuils.maximum_cas_general - base) * ppe.taux.phase_out_cas_general) +
            #     (cond2 & (base > ppe_seuils.pour_taux_plein_couples_mono_revenus) & (base <= ppe_seuils.max_couples_mono_emploi_parents_isoles)) * (ppe_seuils.max_couples_mono_emploi_parents_isoles - base) * ppe.taux.phase_out_couples_mono_emploi)
            return (
                (base <= ppe_seuils.pour_taux_plein_cas_general) * (base) * ppe.taux.phase_in
                + (base > ppe_seuils.pour_taux_plein_cas_general) * (base <= ppe_seuils.maximum_cas_general) * (ppe_seuils.maximum_cas_general - base) * ppe.taux.phase_out_cas_general
                + ligne2 * (base > ppe_seuils.pour_taux_plein_couples_mono_revenus) * (base <= ppe_seuils.max_couples_mono_emploi_parents_isoles) * (ppe_seuils.max_couples_mono_emploi_parents_isoles - base) * ppe.taux.phase_out_couples_mono_emploi
                )

        def ppe_bar2(base):
            return (
                (base <= ppe_seuils.pour_taux_plein_cas_general) * (base) * ppe.taux.phase_in
                + ((base > ppe_seuils.pour_taux_plein_cas_general) & (base <= ppe_seuils.maximum_cas_general)) * (ppe_seuils.maximum_cas_general - base) * ppe.taux.phase_out_cas_general)

        # calcul des primes individuelles.

        ppev = eliv * (1 / ppe_coef) * ppe_bar1(basev)
        ppec = elic * (1 / ppe_coef) * ppe_bar1(basec)

        # Primes de monoactivité
        ppe_monact_vous = (eliv & ligne2 & (basevi >= ppe_seuils.minimum) & (basev <= ppe_seuils.pour_taux_plein_couples_mono_revenus)) * ppe.supplements.couples_mono_emploi
        ppe_monact_conj = (elic & ligne2 & (baseci >= ppe_seuils.minimum) & (basec <= ppe_seuils.pour_taux_plein_couples_mono_revenus)) * ppe.supplements.couples_mono_emploi

        # Primes pour enfants à charge
        maj_pac = ppe_elig * (eliv | elic) * (
            (ligne1 & maries_ou_pacses & ((ppev + ppec) != 0) & (min_(basev, basec) <= ppe_seuils.maximum_cas_general)) * ppe.supplements.par_personne_charge
            * (nb_pac_ppe + nbH * 0.5)
            + (ligne1 & (celibataire_ou_divorce | veuf) & eliv & (basev <= ppe_seuils.maximum_cas_general)) * ppe.supplements.par_personne_charge * (nb_pac_ppe + nbH * 0.5)
            + (ligne2 & (base_monacti >= ppe_seuils.minimum) & (base_monact <= ppe_seuils.maximum_cas_general)) * ppe.supplements.par_personne_charge * (nb_pac_ppe + nbH * 0.5)
            + (ligne2 & (base_monact > ppe_seuils.maximum_cas_general) & (base_monact <= ppe_seuils.max_couples_mono_emploi_parents_isoles)) * ppe.supplements.par_personne_charge
            * ((nb_pac_ppe != 0) + 0.5 * ((nb_pac_ppe == 0) & (nbH != 0)))
            + (ligne3 & (basevi >= ppe_seuils.minimum) & (basev <= ppe_seuils.maximum_cas_general)) * (
                (min_(nb_pac_ppe, 1) * 2 * ppe.supplements.par_personne_charge + max_(nb_pac_ppe - 1, 0) * ppe.supplements.par_personne_charge)
                + (nb_pac_ppe == 0) * (min_(nbH, 2) * ppe.supplements.par_personne_charge + max_(nbH - 2, 0) * ppe.supplements.par_personne_charge * 0.5))
            + (ligne3 & (basev > ppe_seuils.maximum_cas_general) & (basev <= ppe_seuils.max_couples_mono_emploi_parents_isoles)) * ppe.supplements.par_personne_charge
            * ((nb_pac_ppe != 0) * 2 + ((nb_pac_ppe == 0) & (nbH != 0))))

        def coef(coef_tp):
            return (coef_tp <= 0.5) * coef_tp * 1.45 + (coef_tp > 0.5) * (0.55 * coef_tp + 0.45)

        ppe_vous = ppe_elig * (ppev * coef(coef_tpv) + ppe_monact_vous)
        ppe_conj = ppe_elig * (ppec * coef(coef_tpc) + ppe_monact_conj)

        ppe_pac = ppe_elig * (1 / ppe_coef) * foyer_fiscal.sum(
            eligible_i * ppe_bar2(base_i) * coef(coef_tp_i),
            role = FoyerFiscal.PERSONNE_A_CHARGE)

        ppe_tot = ppe_vous + ppe_conj + ppe_pac + maj_pac

        ppe_tot = (ppe_tot != 0) * max_(ppe.montant_minimum, ppe_tot)

        return ppe_tot


class ppe(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Prime pour l'emploi"
    end = '2015-12-31'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2882.xhtml'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        PPE effectivement versée
        '''
        ppe_brute = foyer_fiscal('ppe_brute', period)

        # TODO: les foyers qui paient l'ISF n'ont pas le droit à la PPE
        rsa_act_i = foyer_fiscal.members('rsa_activite_individu', period, options = [ADD])
        rsa_act = foyer_fiscal.sum(rsa_act_i, role = FoyerFiscal.DECLARANT)

        #   On retranche le RSA activité de la PPE
        #   Dans les agrégats officiels de la DGFP, c'est à la PPE brute qu'il faut comparer
        ppe = max_(ppe_brute - rsa_act, 0)
        return ppe


class deficit_exercice(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déficit sur l'exercice"
    definition_period = YEAR
