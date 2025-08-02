from functools import partial
from numpy import busday_count as original_busday_count, datetime64, timedelta64
from openfisca_france.model.base import *
from openfisca_core.periods import Period


class chomeur_longue_duree(Variable):
    cerfa_field = {
        0: '1AI',
        1: '1BI',
        2: '1CI',
        3: '1DI',
        4: '1EI',
        }
    value_type = bool
    entity = Individu
    label = "Demandeur d'emploi inscrit depuis plus d'un an"
    definition_period = YEAR
    end = '2017-12-31'
    # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


class chomage_brut(Variable):
    value_type = float
    entity = Individu
    label = 'Chômage brut'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula(individu, period):
        return individu('are', period)


class indemnites_chomage_partiel(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités de chômage partiel'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class chomeur_au_sens_du_BIT(Variable):
    value_type = bool
    entity = Individu
    label = "Demandeur d'emploi inscrit depuis plus d'un an"
    definition_period = MONTH
    reference = [
        'INSEE - Chômeur au sens du BIT',
        'https://www.insee.fr/fr/metadonnees/definition/c1129',
        ]

    def formula(individu, period):
        # être sans emploi durant une semaine donnée
        salaire_de_base = individu('salaire_de_base', period)
        condition_salaire = (salaire_de_base == 0)
        # être disponible pour travailler dans les deux semaines à venir
        # avoir effectué, au cours des quatre dernières semaines, une démarche active de recherche d’emploi ou a trouvé un emploi qui commence dans les trois mois.
        # Critère de l'âge: être âgé de 15 ans ou plus
        age = individu('age', period)
        condition_age = age >= 15

        return condition_age * condition_salaire


class jours_travailles_chomage(Variable):
    value_type = float
    entity = Individu
    label = 'Nombre de jours travaillés pris en compte dans le calcul du salaire de référence journalier (5 au maximum par semaine civile)'
    definition_period = MONTH
    default_value = 21.75

    def formula(individu, period):
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        busday_count = partial(original_busday_count, weekmask = '1111100')
        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month'))
        jours_travailles = max_(
            busday_count(
                max_(contrat_de_travail_debut, debut_mois),
                min_(contrat_de_travail_fin, fin_mois) + timedelta64(1, 'D')
                ),
            0,
            )
        return jours_travailles


class salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire de référence (SR)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        salaire_de_reference = individu.empty_array()
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            salaire_de_reference = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'salaire_de_base',
                    Period(('month', contrat_de_travail_fin_potentiel.offset(-120), 120)),
                    options = [ADD],
                    ),
                salaire_de_reference,
                )
        return salaire_de_reference


class nombre_jours_travailles_12_derniers_mois(Variable):
    value_type = float
    entity = Individu
    label = 'Jours travaillés sur les 12 derniers mois avant la rupture de contrat'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        nombre_jours_travailles_chomage = individu.empty_array()
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            nombre_jours_travailles_chomage = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'jours_travailles_chomage',
                    Period(('month', contrat_de_travail_fin_potentiel.offset(-12), 12)),
                    options = [ADD],
                    ),
                nombre_jours_travailles_chomage,
                )
        return nombre_jours_travailles_chomage


class salaire_de_reference_mensuel(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire de référence mensuel (SRM)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        nombre_jours_travailles_12_derniers_mois = individu('nombre_jours_travailles_12_derniers_mois', period)
        salaire_de_reference = individu('salaire_de_reference', period)
        salaire_de_reference_mensuel = where(
            nombre_jours_travailles_12_derniers_mois > 0,
            (
                30
                * salaire_de_reference
                / (nombre_jours_travailles_12_derniers_mois * 1.4)
                ),
            0
            )
        return salaire_de_reference_mensuel


class are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        are_eligibilite_individu = individu('are_eligibilite_individu', period)
        salaire_de_reference_mensuel = individu('salaire_de_reference_mensuel', period)
        duree_versement_are = individu('duree_versement_are', period.offset(-1))
        duree_maximale_versement_are = individu('duree_maximale_versement_are', period)

        are = parameters(period).are
        montant_mensuel = max_(
            are.are_partie_fixe * 30 + are.pourcentage_du_sjr_complement * salaire_de_reference_mensuel,
            are.pourcentage_du_sjr_seul * salaire_de_reference_mensuel
            )
        montant_plancher = max_(
            are.are_min * 30,
            montant_mensuel
            )
        montant_plafond = min_(
            montant_plancher,
            are.max_en_pourcentage_sjr * salaire_de_reference_mensuel
            )

        # busday_count = partial(original_busday_count, weekmask = "1111100")

        return (
            montant_plafond
            * are_eligibilite_individu
            * min_(
                1,
                max_(
                    0,
                    (duree_maximale_versement_are - (duree_versement_are))
                    ) / 30
                )
            )


class are_eligibilite_individu(Variable):
    value_type = bool
    label = "Éligibilité individuelle à l'ARE"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'Unédic - Règlement général annexé à la convention du 6 mai 2011',
        'https://www.unedic.org/sites/default/files/regulations/RglACh11.pdf',
        ]

    def formula_2017_11(individu, period, parameters):
        # il faut résider en France, être involontairement privé d'emploi, être inscrit comme demandeur d'emploi,
        # être à la recherche active et permanente d'un emploi,
        # être physiquement apte à l'exercice d'un emploi.
        # Critère de l'âge: ARE non versé si l'âge de départ à la retraite atteint, sauf en cas de taux plein non atteint.
        # Pour simplifier, on stipule qu'on ne peut plus toucher d'ARE dès lors l'âge légal de départ à la retraite atteint.
        are = parameters(period).are
        age = individu('age', period)
        condition_age = age < are.age_legal_retraite

        # Critère d'affiliation : avoir travaillé un certain nombre de jours
        # dans les derniers mois avant la date de fin de contrat.
        # Le nombre de mois diffère selon qu'on ait plus ou moins de 53 ans.
        periode_affiliation = individu('nombre_jours_travailles_dans_les_x_derniers_mois', period)
        condition_affiliation = select(
            [
                age < 53,
                age >= 53
                ],
            [
                periode_affiliation >= are.periode_minimale_affiliation_moins_53_ans,
                periode_affiliation >= are.periode_minimale_affiliation_53_ans_et_plus
                ],
            )
        return condition_age * condition_affiliation


class nombre_jours_travailles_dans_les_x_derniers_mois(Variable):
    value_type = float
    entity = Individu
    label = 'Nombre de jours travaillés sur les x derniers mois avant la rupture de contrat pour les moins de 53 ans'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2017_11(individu, period, parameters):
        are = parameters(period).are
        age = individu('age', period)
        # Moins de 53 ans
        periode_reference_moins_53 = are.periode_de_reference_affiliation_moins_53_ans
        nombre_jours_travailles_reference_moins_53 = individu.empty_array()
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            nombre_jours_travailles_reference_moins_53 = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'jours_travailles_chomage',
                    Period(('month', contrat_de_travail_fin_potentiel.offset(-periode_reference_moins_53), periode_reference_moins_53)),
                    options = [ADD],
                    ),
                nombre_jours_travailles_reference_moins_53,
                )
        # Plus de 53 ans
        nombre_jours_travailles_reference_plus_53 = individu.empty_array()
        periode_reference_plus_53 = are.periode_de_reference_affiliation_53_ans_et_plus
        for months in range(0, 72):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            nombre_jours_travailles_reference_plus_53 = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'jours_travailles_chomage',
                    Period(('month', contrat_de_travail_fin_potentiel.offset(-periode_reference_plus_53), periode_reference_plus_53)),
                    options = [ADD],
                    ),
                nombre_jours_travailles_reference_plus_53,
                )

        nombre_jours_travailles_reference = select(
            [age < 53, age >= 53],
            [nombre_jours_travailles_reference_moins_53, nombre_jours_travailles_reference_plus_53],
            )
        return nombre_jours_travailles_reference


class duree_versement_are(Variable):
    value_type = int
    entity = Individu
    label = "Nombre  de jours indemnisés par l'ARE"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        are = individu('are', period)
        duree_versement_are = individu('duree_versement_are', period.offset(-1))
        busday_count = partial(original_busday_count, weekmask = '1' * 7)
        duree_versement_are = (
            duree_versement_are
            + (
                (are > 0)
                * busday_count(datetime64(period.start), datetime64(period.offset(1).start))
                )
            )
        return duree_versement_are


class duree_maximale_versement_are(Variable):
    value_type = int
    entity = Individu
    label = "Nombre maximal de jours indemnisés par l'ARE"
    definition_period = MONTH

    def formula(individu, period):
        age = individu('age', period)
        nombre_jours_travailles_dans_la_periode_reference_affiliation = individu('nombre_jours_travailles_dans_les_x_derniers_mois', period)
        nombre_jours_indemnises = nombre_jours_travailles_dans_la_periode_reference_affiliation * 1.4

        return select(
            [age < 53, (53 <= age) & (age <= 54), age >= 55],
            [min_(nombre_jours_indemnises, 730), min_(nombre_jours_indemnises, 913), min_(nombre_jours_indemnises, 1095)],
            )


class eligibilite_cumul_are_salaire(Variable):
    value_type = bool
    entity = Individu
    label = "Eligibilité de l'individu au cumul des allocations de chômage et de la rémunération provenant d'une activité professionnelle"
    definition_period = MONTH

    def formula(individu, period):
        cumul_are_salaire = individu('cumul_are_salaire', period)
        salaire_de_reference_mensuel = individu('salaire_de_reference_mensuel', period)
        condition_cumul = cumul_are_salaire <= salaire_de_reference_mensuel
        return condition_cumul


class cumul_are_salaire(Variable):
    value_type = float
    entity = Individu
    label = "Revenus totaux d'un individu cumulant ARE et revenus issus d'une activité professionnelle"
    definition_period = MONTH

    def formula(individu, period):
        are_activite_reduite = individu('are_activite_reduite', period)
        salaire_de_base = individu('salaire_de_base', period)

        return are_activite_reduite + salaire_de_base


class are_activite_reduite(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'allocation chomage lorqu'un individu exerce une activité réduite (à faibles revenus professionels"
    definition_period = MONTH

    def formula(individu, period):
        salaire_de_base = individu('salaire_de_base', period)
        are = individu('are', period)
        eligibilite_cumul_are_salaire = individu('eligibilite_cumul_are_salaire', period)
        are_eligibilite_individu = individu('are_eligibilite_individu', period)
        nombre_jours_indemnisables_are = (are - 0.7 * salaire_de_base) / (are / 30)

        return nombre_jours_indemnisables_are * are * eligibilite_cumul_are_salaire * are_eligibilite_individu


class csg_chomage_deductible(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG déductible sur les allocations chômage'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH

    def formula(individu, period, parameters):
        chomage_brut = individu('chomage_brut', period)
        taux_csg_deductible = parameters(period).prelevements_sociaux.contributions.csg.chomage.deductible
        csg_deductible = taux_csg_deductible.taux_plein * 0.9825 * chomage_brut

        return - csg_deductible


class csg_chomage_imposable(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CSG imposable sur les allocations chômage'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH

    def formula(individu, period, parameters):
        chomage_brut = individu('chomage_brut', period)
        taux_csg_imposable = parameters(period).prelevements_sociaux.contributions.csg.chomage.imposable
        csg_imposable = taux_csg_imposable.taux * 0.9825 * chomage_brut

        return - csg_imposable


class csg_are(Variable):
    value_type = float
    entity = Individu
    label = 'CSG imposable et déductible sur les allocations chômage'
    definition_period = MONTH

    def formula(individu, period, parameters):
        csg_chomage_deductible = individu('csg_chomage_deductible', period)
        csg_chomage_imposable = individu('csg_chomage_imposable', period)
        csg = csg_chomage_deductible + csg_chomage_imposable
        are = individu('are', period)
        smic_horaire = parameters(period).cotsoc.gen.smic_h_b
        smic_mensuel = [(smic_horaire * 35 / 7) * 30]

        csg_montant = select(
            [are + csg > smic_mensuel, are + csg <= smic_mensuel],
            [csg, 0],
            )

        return csg_montant


class are_nette_csg(Variable):
    value_type = float
    entity = Individu
    label = "Allocation de retour à l'emploi nette déduite de la CSG"
    definition_period = MONTH

    def formula(individu, period, parameters):
        csg_are = individu('csg_are', period)
        are = individu('are', period)

        return are + csg_are


class crds_are(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Individu
    label = 'CRDS imposable sur les allocations chômage'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2329.xhtml'
    definition_period = MONTH

    def formula(individu, period, parameters):
        are = individu('are', period)
        taux_crds = parameters(period).prelevements_sociaux.contributions.crds
        crds = taux_crds.taux * 0.9825 * are
        smic_horaire = parameters(period).cotsoc.gen.smic_h_b
        smic_mensuel = [(smic_horaire * 35 / 7) * 30]

        crds_montant = select(
            [are - crds > smic_mensuel, are - crds <= smic_mensuel],
            [crds, 0],
            )

        return - crds_montant


class are_nette_crds(Variable):
    value_type = float
    entity = Individu
    label = "Allocation de retour à l'emploi nette déduite de la CRDS"
    definition_period = MONTH

    def formula(individu, period, parameters):
        crds_are = individu('crds_are', period)
        are = individu('are', period)

        return are + crds_are


class are_nette_contributions_sociales(Variable):
    value_type = float
    entity = Individu
    label = "Allocation de retour à l'emploi nette déduite des contributions sociales"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are = individu('are', period)
        csg_are = individu('csg_are', period)
        crds_are = individu('crds_are', period)

        return are + csg_are + crds_are


class retraite_complementaire_chomage(Variable):
    value_type = float
    entity = Individu
    label = "Retenue sociale de la retraite complémentaire sur l'allocation chômage"
    definition_period = MONTH

    def formula(individu, period, parameters):
        salaire_de_reference_mensuel = individu('salaire_de_reference_mensuel', period)
        seuil_exoneration_retraite_complementaire = parameters(period).are.are_min
        are = individu('are', period)
        retraite_complementaire = 0.03 * salaire_de_reference_mensuel
        montant_retenue_retraite_complementaire = select(
            [are - retraite_complementaire > (seuil_exoneration_retraite_complementaire * 30), are - retraite_complementaire <= (seuil_exoneration_retraite_complementaire * 30)],
            [retraite_complementaire, 0],
            )

        return - montant_retenue_retraite_complementaire


class are_nette(Variable):
    value_type = float
    entity = Individu
    label = "Allocation de retour à l'emploi nette déduite des contributions et des cotisations"
    set_input = set_input_divide_by_period
    definition_period = MONTH

    def formula(individu, period, parameters):
        are = individu('are', period)
        csg_are = individu('csg_are', period)
        crds_are = individu('crds_are', period)
        retraite_complementaire_chomage = individu('retraite_complementaire_chomage', period)

        return are + csg_are + crds_are + retraite_complementaire_chomage


class are_imposable(Variable):
    value_type = float
    entity = Individu
    label = "Allocation de retour à l'emploi imposable"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are = individu('are', period)
        csg_chomage_deductible = individu('csg_chomage_deductible', period)

        return are + csg_chomage_deductible


class cumul_are_nette_rsa(Variable):
    value_type = float
    entity = Individu
    label = "Cumul de l'ARE et du RSA"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are_nette = individu('are_nette', period)
        rsa = individu.famille('rsa', period)

        return are_nette + rsa


class cumul_are_nette_apl(Variable):
    value_type = float
    entity = Individu
    label = "Cumul de l'ARE et des APL"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are_nette = individu('are_nette', period)
        apl = individu.famille('apl', period)

        return are_nette + apl


class cumul_are_nette_rsa_apl(Variable):
    value_type = float
    entity = Individu
    label = "Cumul de l'ARE, du RSA et des APL"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are_nette = individu('are_nette', period)
        rsa = individu.famille('rsa', period)
        apl = individu.famille('apl', period)

        return are_nette + rsa + apl


class cumul_are_nette_rsa_ass_apl(Variable):
    value_type = float
    entity = Individu
    label = "Cumul de l'ARE, du RSA et des APL"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are_nette = individu('are_nette', period)
        rsa = individu.famille('rsa', period)
        apl = individu.famille('apl', period)
        ass = individu('ass', period)

        return are_nette + rsa + apl + ass


class cumul_prestations_familiales(Variable):
    value_type = float
    entity = Famille
    label = 'Cumul des prestations familiales : AF, ASF, CF'
    definition_period = MONTH

    def formula(famille, period, parameters):
        af = famille('af', period)
        asf = famille('asf', period)
        cf = famille('cf', period)

        return af + asf + cf


class cumul_are_nette_rsa_ass_apl_prestations_familiales(Variable):
    value_type = float
    entity = Individu
    label = "Cumul de l'ARE, du RSA, de l'ASS, des APL et des prestations familiales"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are_nette = individu('are_nette', period)
        rsa = individu.famille('rsa', period)
        apl = individu.famille('apl', period)
        ass = individu('ass', period)
        prestations_familiales = individu.famille('cumul_prestations_familiales', period)

        return are_nette + rsa + apl + ass + prestations_familiales


class revenu_disponible_mensuel(Variable):
    value_type = float
    entity = Menage
    label = 'Revenu disponible du ménage'
    reference = 'http://fr.wikipedia.org/wiki/Revenu_disponible'
    definition_period = MONTH

    def formula(menage, period, parameters):
        revenu_disponible_month = menage('revenu_disponible', period, options= [DIVIDE])

        return revenu_disponible_month


class prestations_familiales_mensuelles(Variable):
    value_type = float
    entity = Famille
    label = 'Prestations familiales mensuelles'
    reference = 'http://www.social-sante.gouv.fr/informations-pratiques,89/fiches-pratiques,91/prestations-familiales,1885/les-prestations-familiales,12626.html'
    definition_period = MONTH

    def formula(famille, period, parameters):
        prestations_familiales_month = famille('prestations_familiales', period, options= [DIVIDE])

        return prestations_familiales_month


class minima_sociaux_mensuel(Variable):
    value_type = float
    entity = Famille
    label = 'Minima sociaux mensuel'
    reference = 'http://fr.wikipedia.org/wiki/Minima_sociaux'
    definition_period = MONTH

    def formula(famille, period, parameters):
        aah_i = famille.members('aah', period)
        caah_i = famille.members('caah', period)
        aah = famille.sum(aah_i)
        caah = famille.sum(caah_i)
        aefa = famille('aefa', period, options = [DIVIDE])
        api = famille('api', period)
        ass_i = famille.members('ass', period)
        ass = famille.sum(ass_i)
        minimum_vieillesse = famille('minimum_vieillesse', period, options = [DIVIDE])
        # Certaines réformes ayant des effets de bords nécessitent que le rsa soit calculé avant la ppa
        rsa = famille('rsa', period)
        ppa = famille('ppa', period)
        psa = famille('psa', period)
        crds_mini = famille('crds_mini', period)

        return aah + caah + minimum_vieillesse + rsa + aefa + api + ass + psa + ppa + crds_mini


class prestations_sociales_mensuelles(Variable):
    value_type = float
    entity = Famille
    label = 'Prestations sociales mensuelles'
    reference = 'http://fr.wikipedia.org/wiki/Prestation_sociale'
    definition_period = MONTH

    def formula(famille, period, parameters):
        prestations_familiales = famille('prestations_familiales_mensuelles', period)
        minima_sociaux = famille('minima_sociaux_mensuel', period)
        aide_logement = famille('aide_logement', period)
        reduction_loyer_solidarite = famille('reduction_loyer_solidarite', period)
        aide_exceptionnelle_covid = famille('covid_aide_exceptionnelle_famille_montant', period)
        fse_i = famille.members('covid_aide_exceptionnelle_tpe_montant', period)
        fse = famille.sum(fse_i)

        return prestations_familiales + minima_sociaux + aide_logement + reduction_loyer_solidarite + aide_exceptionnelle_covid + fse


class aefa_mensuel(Variable):
    '''
    Aide exceptionelle de fin d'année (prime de Noël)
    Instituée en 1998
    Apparaît sous le nom de complément de rmi dans les ERF
    Le montant de l’aide mentionnée à l’article 1er versée aux bénéficiaires de l’allocation de solidarité
    spécifique à taux majoré servie aux allocataires âgés de cinquante-cinq ans ou plus justifiant de vingt années
    d’activité salariée, aux allocataires âgés de cinquante-sept ans et demi ou plus justifiant de dix années d’activité
    salariée ainsi qu’aux allocataires justifiant d’au moins 160 trimestres validés dans les régimes d’assurance
    vieillesse ou de périodes reconnues équivalentes est égal à
    Pour bénéficier de la Prime de Noël 2011, vous devez être éligible pour le compte du mois de novembre 2011
    ou au plus de décembre 2011, soit d’une allocation de solidarité spécifique (ASS), de la prime forfaitaire mensuelle
    de reprise d'activité, de l'allocation équivalent retraite (allocataire AER), du revenu de solidarité active
    (Bénéficiaires RSA), de l'allocation de parent isolé (API), du revenu minimum d'insertion (RMI), de l’Allocation
    pour la Création ou la Reprise d'Entreprise (ACCRE-ASS) ou encore allocation chômage.
    '''
    value_type = float
    entity = Famille
    label = "Aide exceptionelle de fin d'année (prime de Noël)"
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F1325'
    definition_period = MONTH

    def formula(famille, period, parameters):
        aefa_month = famille('aefa', period, options= [DIVIDE])

        return aefa_month


class minimum_vieillesse_mensuel(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Minimum vieillesse (ASI + ASPA)'
    definition_period = MONTH

    def formula(famille, period, parameters):
        minimum_vieillesse_month = famille('minimum_vieillesse', period, options= [DIVIDE])

        return minimum_vieillesse_month


class pensions_nettes_mensuelles(Variable):
    value_type = float
    entity = Individu
    label = 'Pensions et revenus de remplacement'
    reference = 'http://fr.wikipedia.org/wiki/Rente'
    definition_period = MONTH

    def formula(famille, period, parameters):
        pensions_nettes_month = famille('pensions_nettes', period, options= [DIVIDE])

        return pensions_nettes_month


class revenu_disponible_avec_impots(Variable):
    value_type = float
    entity = Famille
    label = "Revenu disponible ne déduisant pas l'impôt sur le revenu"
    definition_period = MONTH

    def formula(famille, period, parameters):
        revenus_nets_du_travail_i = famille.members('salaire_net', period)
        revenus_nets_du_travail = famille.sum(revenus_nets_du_travail_i)
        revenus_nets_du_capital_i = famille.members('revenus_nets_du_capital', period, options= [DIVIDE])
        revenus_nets_du_capital = famille.sum(revenus_nets_du_capital_i)
        pensions_nettes_i = famille.members('pensions_nettes_mensuelles', period)
        pensions_nettes = famille.sum(pensions_nettes_i)
        ppe_i = famille.members.foyer_fiscal('ppe', period, options= [DIVIDE])
        ppe = famille.sum(ppe_i)
        prestations_sociales = famille('prestations_sociales_mensuelles', period)

        return (
            revenus_nets_du_travail
            + revenus_nets_du_capital
            + pensions_nettes
            + ppe
            + prestations_sociales
            )


class niveau_de_vie_avec_impots(Variable):
    value_type = float
    entity = Famille
    label = 'Niveau de vie du ménage en prenant le revenu disponible qui ne déduit pas les impôts'
    definition_period = MONTH

    def formula(famille, period):
        revenu_disponible_avec_impots = famille('revenu_disponible_avec_impots', period)
        uc = famille('unites_consommation_mensuel', period)
        return revenu_disponible_avec_impots / uc


class unites_consommation_mensuel(Variable):
    value_type = float
    entity = Famille
    label = "Unités de consommation du ménage, selon l'échelle de l'INSEE"
    reference = 'https://insee.fr/fr/metadonnees/definition/c1802'
    definition_period = MONTH

    def formula(menage, period, parameters):
        age_individu = menage.members('age', period.first_month)
        uc_individu = 0.5 * (age_individu >= 14) + 0.3 * (age_individu < 14)
        return 0.5 + menage.sum(uc_individu)  # 1 uc pour la personne de référence
