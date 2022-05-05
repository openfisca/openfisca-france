from numpy import floor, logical_and as and_, logical_or as or_

from openfisca_france.model.base import *
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class api(Variable):
    value_type = float
    entity = Famille
    label = 'Allocation de parent isolé'
    reference = 'http://fr.wikipedia.org/wiki/Allocation_de_parent_isol%C3%A9',
    end = '2009-05-31'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula(famille, period, parameters):
        '''
        Allocation de parent isolé
        '''
        isole = not_(famille('en_couple', period))
        rsa_forfait_logement = famille('rsa_forfait_logement', period)
        rsa_base_ressources = famille('rsa_base_ressources', period)
        af_majoration = famille('af_majoration', period)
        rsa = famille('rsa', period)
        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf
        api = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.api

        # TODO:
        #    Majoration pour isolement
        #    Si vous êtes parent isolé, c’est-à-dire célibataire, divorcé(e), séparé(e) ou veuf(ve) avec des enfants
        #    à charge ou enceinte, le montant forfaitaire garanti est majoré.
        #    Ce montant forfaitaire majoré est accordé à partir du mois au cours duquel survient l'un des événements
        #    suivants :
        #    - déclaration de grossesse,
        #    - naissance d'un enfant,
        #    - prise en charge d'un enfant,
        #    - séparation, veuvage,
        #    - dépôt de la demande si l’événement est antérieur.
        #
        #    Le montant forfaitaire majoré peut être accordé pendant 12 mois, continus ou discontinus, au cours
        #    d’une période de 18 mois suivant l’événement.
        #    Si votre plus jeune enfant à charge a moins de 3 ans, le montant forfaitaire majoré vous est accordé
        #    jusqu'à ses 3 ans.
        age_en_mois_i = famille.members('age_en_mois', period)
        age_en_mois_enfant = famille.min(age_en_mois_i, role = Famille.ENFANT)
        enceinte = (age_en_mois_enfant < 0) * (age_en_mois_enfant > -6)
        # TODO: quel mois mettre ?
        # TODO: pas complètement exact
        # L'allocataire perçoit l'API :
        # jusqu'à ce que le plus jeune enfant ait 3 ans,
        # ou pendant 12 mois consécutifs si les enfants sont âgés de plus de 3 ans
        #    et s'il a présenté sa demande dans les 6 mois à partir du moment où il
        #    assure seul la charge de l'enfant.
        # TODO: API courte gens pour les gens qui ont divorcés dans l'année
        # Le droit à l'allocation est réétudié tous les 3 mois.
        # # Calcul de l'année et mois de naissance du benjamin

        condition = (floor(age_en_mois_enfant / 12) <= api.api_cond.age_limite - 1)
        eligib = isole * ((enceinte != 0) | (nb_enf(famille, period, 0, api.api_cond.age_limite - 1) > 0)) * condition

        # moins de 20 ans avant inclusion dans rsa
        # moins de 25 ans après inclusion dans rsa
        api1 = eligib * bmaf * (api.api_m.femmes_enceintes_sans_enfant_a_charge + api.api_m.supplement_par_enfant * nb_enf(famille, period, af.af_cm.age1, api.api_cond.age_pac - 1))
        rsa = (api.api_cond.age_pac >= 25)  # dummy passage au rsa majoré
        br_api = rsa_base_ressources + af_majoration * not_(rsa)
        # On pourrait mensualiser RMI, BRrmi et forfait logement
        api = max_(0, api1 - rsa_forfait_logement / 12 - br_api / 12 - rsa / 12)
        # L'API est exonérée de CRDS
        return api  # annualisé
        # TODO API: temps partiel qui modifie la base ressource
        # Cumul
        # Cumul avec un revenu
        # Si l'allocataire reprend une activité ou suit une formation professionnelle rémunérée, les revenus sont
        # cumulables intégralement au cours des 3 premiers mois de reprise d'activité.
        # Du 4e au 12e mois qui suit, le montant de l'allocation varie en fonction de la durée de l'activité
        # ou de la formation.
        # Durée d'activité de 78 heures ou plus par mois ou activité non salariée
        # Lorsque la durée d'activité est de 78 heures minimum par mois, le montant de l'API perçu par l'allocataire est
        # diminué de la totalité du salaire. Tous les revenus d'activité sont pris en compte pour le calcul de l'API,
        # sauf si l'allocataire perçoit des revenus issus d'un contrat insertion-revenu minimum d'activité (CIRMA)
        # ou d'un contrat d'avenir (CAV).
        # L'allocataire peut bénéficier, sous certaines conditions :
        # • de la prime de retour à l'emploi si son activité est d'une durée d'au moins 4 mois consécutifs,
        # sauf s'il effectue un stage de formation professionnelle,
        # • de la prime forfaitaire pendant 9 mois, sauf s'il exerce une activité salariée dans le cadre d'un CIRMA
        # ou d'un CAV.
        # Durée d'activité de moins de 78 heures par mois
        # Lorsque la durée d'activité est inférieure à 78 heures par mois, le montant de l'API perçu par l'allocataire
        # est diminué de la moitié du salaire.
        # Si l'allocataire exerce une activité dans le cadre d'un CIRMA ou d'un CAV, ses revenus d'activité ne sont pas
        # pris en compte pour le calcul de son API.


class psa(Variable):
    value_type = float
    entity = Famille
    label = 'Prime de solidarité active'
    end = '2009-04-30'
    reference = 'http://www.service-public.fr/actualites/001077.html'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2009_04(famille, period, parameters):
        '''
        Prime de solidarité active (exceptionnelle, 200€ versés une fois en avril 2009)
        Versement en avril 2009 d’une prime de solidarité active (Psa) aux familles modestes qui ont bénéficié
        en janvier, février ou mars 2009 du Rmi, de l’Api (du Rsa expérimental, du Cav ou du Rma pour
        les ex-bénéficiaires du Rmi ou de l’Api), de la prime forfaitaire mensuelle au titre du Rmi ou de l’Api
        ou enfin d’une aide au logement (à condition d’exercer une activité professionnelle et
        d’être âgé de plus de 25 ans ou d’avoir au moins un enfant à charge).
        La Psa, prime exceptionnelle, s’élève à 200 euros par foyer bénéficiaire.
        '''
        rmi = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.rmi
        api = famille('api', period)
        rsa = famille('rsa', period)
        af_nbenf = famille('af_nbenf', period)
        aide_logement = famille('aide_logement', period)

        personne_en_activite_i = (famille.members('activite', period) == TypesActivite.actif)
        parent_en_activite = famille.any(personne_en_activite_i, role = Famille.PARENT)

        dummy_api = api > 0
        dummy_rmi = rsa > 0
        dummy_al = and_(aide_logement > 0, or_(af_nbenf > 0, parent_en_activite))
        condition = (dummy_api + dummy_rmi + dummy_al > 0)
        psa = condition * rmi.psa
        return psa


class rmi(Variable):
    value_type = float
    entity = Famille
    label = "Revenu Minimum d'Insertion"
    end = '2009-05-31'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_1988_12(famille, period):
        activite_i = famille.members('activite', period)
        condition_activite_i = (
            (activite_i != TypesActivite.actif)
            * (activite_i != TypesActivite.etudiant)
            * (activite_i != TypesActivite.retraite)
            )
        condition_activite = famille.any(condition_activite_i)

        rsa_base_ressources = famille('rsa_base_ressources', period)
        rsa_socle = famille('rsa_socle', period)
        rsa_forfait_logement = famille('rsa_forfait_logement', period)

        return condition_activite * max_(0, rsa_socle - rsa_forfait_logement - rsa_base_ressources)
        # TODO: Migré lors de la mensualisation. Probablement faux


class rsa_activite(Variable):
    value_type = float
    entity = Famille
    label = 'Revenu de solidarité active - activité'
    end = '2015-12-31'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2009_06_01(famille, period):
        rsa = famille('rsa', period)
        rsa_base_ressources = famille('rsa_base_ressources', period)
        rsa_socle = famille('rsa_socle', period)
        rsa_forfait_logement = famille('rsa_forfait_logement', period)
        rmi = max_(0, rsa_socle - rsa_forfait_logement - rsa_base_ressources)
        return max_(rsa - rmi, 0)


class rsa_activite_individu(Variable):
    value_type = float
    entity = Individu
    label = "Revenu de solidarité active - activité au niveau de l'individu"
    end = '2015-12-31'
    definition_period = YEAR

    def formula_2009_06_01(individu, period):
        '''
        Note: le partage en moitié est un point de législation, pas un choix arbitraire
        '''
        janvier = period.first_month

        rsa_activite = individu.famille('rsa_activite', period, options = [ADD])
        marie = individu('statut_marital', janvier) == 1
        en_couple = individu.famille('en_couple', janvier)

        # On partage le rsa_activite entre les parents. Si la personne est mariée et qu'aucun conjoint n'a été déclaré,
        # on divise par 2.
        partage_rsa = or_(marie, en_couple)

        return where(partage_rsa, rsa_activite / 2, rsa_activite)
