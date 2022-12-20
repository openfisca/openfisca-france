from openfisca_core import periods

from openfisca_france.model.base import *

from numpy import logical_or as or_, logical_and as and_

# Les éligibilités séparées de l'indemnité inflation
#######################################################


# 1 : Non-Salariés
class eligibilite_indemnite_inflation_non_salarie(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation en tant que non-salarié"
    definition_period = YEAR

    def formula(individu, period, parameters):

        oct_2021 = periods.period('2021-10')

        # non-salarié
        eligibilite_cat_non_sal = (individu('categorie_non_salarie', oct_2021.this_year) != TypesCategorieNonSalarie.non_pertinent)

        # revenu d'activité inférieure à € 2000 nets par mois en 2020 (selon déclaration annuelle des revenus)
        annee_2020 = periods.period('2020')
        jan_sep_2021 = periods.period('month:2021-01:9')

        # chiffre d'affaires. Uniquement pour les régimes microsociaux, on ne tient pas compte de ceux qui y auraient droit (et à l'indemnite inflation) mais préféreraient le régime des bénéfices réels.
        rev_net_auto = individu('rpns_auto_entrepreneur_revenus_net', annee_2020, options = [ADD])
        rev_net_micro = individu('rpns_micro_entreprise_revenus_net', annee_2020, options = [ADD])

        rev_net = (rev_net_auto + rev_net_micro) / 12

        chiffre_d_affaires_micro = individu('rpns_micro_entreprise_chiffre_affaires', jan_sep_2021.this_year) * 9 / 12
        chiffre_d_affaires_liberatoire = individu('rpns_auto_entrepreneur_chiffre_affaires', jan_sep_2021.this_year) * 9 / 12
        chiffre_d_affaires = chiffre_d_affaires_micro + chiffre_d_affaires_liberatoire

        eligibilite_micro_artisan = and_(and_(chiffre_d_affaires >= 900, chiffre_d_affaires <= 4000), individu('categorie_non_salarie', oct_2021.this_year) == TypesCategorieNonSalarie.artisan)
        eligibilite_micro_commercant = and_(and_(chiffre_d_affaires >= 900, chiffre_d_affaires <= 6897), individu('categorie_non_salarie', oct_2021.this_year) == TypesCategorieNonSalarie.commercant)
        eligibilite_micro_prof_lib = and_(and_(chiffre_d_affaires >= 900, chiffre_d_affaires <= 3030), individu('categorie_non_salarie', oct_2021.this_year) == TypesCategorieNonSalarie.profession_liberale)

        eligibilite_micro = (eligibilite_micro_artisan + eligibilite_micro_commercant + eligibilite_micro_prof_lib) > 0

        return eligibilite_cat_non_sal * or_(and_(rev_net <= 2000, rev_net > 0),
                                             eligibilite_micro)


# 2 : Salariés
class eligibilite_indemnite_inflation_salarie_prive(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation en tant que salarié privé"
    definition_period = YEAR
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):

        # éligibilité statut
        oct_2021 = periods.period('2021-10')
        eligibilite_activite = individu('activite', oct_2021) == TypesActivite.actif
        eligibilite_alternance = individu('alternant', oct_2021) > 0
        eligibilite = (eligibilite_activite + eligibilite_alternance) > 0

        # éligibilité salaire
        # rémunération moyenne inférieure à € 2000 nets par mois travaillé avant IR
        # ou brut inférieure à € 2600 par mois
        # du janvier à octobre 2021
        rev_periods = ['2021-01',
        '2021-02',
        '2021-03',
        '2021-04',
        '2021-05',
        '2021-06',
        '2021-07',
        '2021-08',
        '2021-09',
        '2021-10']

        nsal = 0
        tsal = 0

        for rp in rev_periods:
            per = periods.period(rp)
            sal = individu('salaire_net', per, options=[ADD])

            if sal > 0:
                nsal += 1
                tsal += sal

        sal_plafond = 2000 * max(1, nsal)

        elig_sal = tsal <= sal_plafond

        # pas non-salarié :
        pas_autre = individu('eligibilite_indemnite_inflation_non_salarie', period) == 0

        return eligibilite * elig_sal * pas_autre


# 3 : Public
class eligibilite_indemnite_inflation_public(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation en tant qu'agent public"
    definition_period = YEAR

    def formula(individu, period, parameters):

        oct_2021 = periods.period('2021-10')

        # agent public
        eligibilite_public = ((individu('categorie_salarie', oct_2021) == TypesCategorieSalarie.public_titulaire_etat)
                            + (individu('categorie_salarie', oct_2021) == TypesCategorieSalarie.public_titulaire_militaire)
                            + (individu('categorie_salarie', oct_2021) == TypesCategorieSalarie.public_titulaire_territoriale)
                            + (individu('categorie_salarie', oct_2021) == TypesCategorieSalarie.public_titulaire_hospitaliere)
                            + (individu('categorie_salarie', oct_2021) == TypesCategorieSalarie.public_non_titulaire)) > 0

        # éligibilité rémuneration
        # rémunération moyenne inférieure à € 2000 nets par mois travaillé avant IR
        # ou brut inférieure à € 2600 par mois
        # du janvier à octobre 2021
        rev_periods = ['2021-01',
        '2021-02',
        '2021-03',
        '2021-04',
        '2021-05',
        '2021-06',
        '2021-07',
        '2021-08',
        '2021-09',
        '2021-10']

        nsal = 0
        tsal = 0

        for rp in rev_periods:
            per = periods.period(rp)
            sal = individu('salaire_net', per, options=[ADD])

            if sal > 0:
                nsal += 1
                tsal += sal

        sal_plafond = 2000 * max(1, nsal)

        elig_sal = tsal <= sal_plafond

        # pas non-salarié, salarié :
        pas_autre = (individu('eligibilite_indemnite_inflation_non_salarie', period)
        + individu('eligibilite_indemnite_inflation_salarie_prive', period)) == 0

        return eligibilite_public * elig_sal * pas_autre


# 4 : Retraité
class eligibilite_indemnite_inflation_retraite(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation en tant que retraité"
    definition_period = YEAR

    def formula(individu, period, parameters):

        oct_2021 = periods.period('2021-10')
        annee_2021 = periods.period('2021')

        # bénéficiaire d'une pension de retraite en octobre 2021
        eligibilite_retraite = (individu('activite', oct_2021) == TypesActivite.retraite)

        # bénéficiaire du minimum vieillesse en octobre 2021
        eligibilite_aspa = (individu.famille('aspa', oct_2021) > 0)

        # pension/aspa nette inférieur à € 2000 par mois
        pension = individu('pensions_nettes', annee_2021) / 12
        min_vi = individu.famille('aspa', annee_2021, options = [ADD]) / 12

        # pas non-salarié, salarié, agent public :
        pas_autre = (individu('eligibilite_indemnite_inflation_non_salarie', period)
                    + individu('eligibilite_indemnite_inflation_salarie_prive', period)
                    + individu('eligibilite_indemnite_inflation_public', period)) == 0

        return or_(and_(eligibilite_retraite, pension <= 2000),
                   and_(eligibilite_aspa, min_vi <= 2000)) * pas_autre


# 5 : Min Soc, Prest Soc
class eligibilite_indemnite_inflation_prest_soc(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation en tant que bénéficiaire des prestations sociales"
    definition_period = YEAR

    def formula(individu, period, parameters):

        oct_2021 = periods.period('2021-10')

        # pension d'invalidité <= 2000 par mois
        eligibilite_pension_invalidite = (individu('pensions_invalidite', oct_2021) <= 2000) * (individu('pensions_invalidite', oct_2021) > 0)

        # allocataire de l'AAH; RSA; ASI; PreParE; sans critère de montant
        eligibilite_allocations = (individu('aah', oct_2021)
                                   + individu.famille('rsa', oct_2021) * individu.has_role(Famille.PARENT)
                                   + individu('asi', oct_2021)
                                   + individu.famille('paje_prepare', oct_2021) * individu.has_role(Famille.PARENT))

        # pas non-salarié, salarié, agent public, retraité :
        pas_autre = (individu('eligibilite_indemnite_inflation_non_salarie', period)
                    + individu('eligibilite_indemnite_inflation_salarie_prive', period)
                    + individu('eligibilite_indemnite_inflation_public', period)
                    + individu('eligibilite_indemnite_inflation_retraite', period)) == 0

        return ((eligibilite_pension_invalidite + eligibilite_allocations) > 0) * pas_autre


# 6 : Jeunes
class eligibilite_indemnite_inflation_jeune(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation en tant que jeune"
    definition_period = YEAR

    def formula(individu, period, parameters):

        oct_2021 = periods.period('2021-10')

        # au moins 16 ans
        eligibilite_age = individu('age', oct_2021) >= 16

        # étudiant boursier
        eligibilite_etudiant_boursier = individu('bourse_criteres_sociaux', oct_2021) > 0

        # étudiant non-boursier & AL
        eligibilite_etudiant_nb_al = and_(and_(individu('etudiant', oct_2021), individu('bourse_criteres_sociaux', oct_2021) == 0),
                                          and_(individu.famille('aide_logement', oct_2021) > 0, individu.has_role(Famille.DEMANDEUR)))

        # apprenti ou contrat de professionnalisation
        eligibilite_apprenti = or_(and_(individu('apprenti', oct_2021), individu('remuneration_apprenti', oct_2021) <= 2000),
                                   and_(individu('professionnalisation', oct_2021), individu('professionnalisation', oct_2021) <= 2000))

        # stagiaire formation prof.
        eligibilite_stage_prof = and_(individu('revenus_stage_formation_pro', oct_2021) > 0,
        individu('revenus_stage_formation_pro', oct_2021) < 2000)

        # jeune en rechere d'emploi, pqrcours contractualisé d'accompagnement, garantie jeunes
        eligibilite_emploi_gj = individu('garantie_jeunes', oct_2021) > 0

        # pas non-salarié, salarié, agent public, retraité, MinSoc/PrestSoc :
        pas_autre = (individu('eligibilite_indemnite_inflation_non_salarie', period)
                    + individu('eligibilite_indemnite_inflation_salarie_prive', period)
                    + individu('eligibilite_indemnite_inflation_public', period)
                    + individu('eligibilite_indemnite_inflation_retraite', period)
                    + individu('eligibilite_indemnite_inflation_prest_soc', period)) == 0

        return eligibilite_age * ((eligibilite_etudiant_boursier
                                   + eligibilite_etudiant_nb_al
                                   + eligibilite_apprenti
                                   + eligibilite_stage_prof
                                   + eligibilite_emploi_gj) > 0) * pas_autre


# 7 : Demandeur d'Emploi
class eligibilite_indemnite_inflation_demandeur_emploi(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation en tant que demandeur d'emploi"
    definition_period = YEAR

    def formula(individu, period, parameters):

        oct_2021 = periods.period('2021-10')

        # chômeur en octobre 2021
        eligibilite_chomeur = (individu('activite', oct_2021) == TypesActivite.chomeur)

        allocation = individu('chomage_net', oct_2021)

        # pas non-salarié, salarié, agent public, retraité, MinSoc/PrestSoc, jeune :
        pas_autre = (individu('eligibilite_indemnite_inflation_non_salarie', period)
                    + individu('eligibilite_indemnite_inflation_salarie_prive', period)
                    + individu('eligibilite_indemnite_inflation_public', period)
                    + individu('eligibilite_indemnite_inflation_retraite', period)
                    + individu('eligibilite_indemnite_inflation_prest_soc', period)
                    + individu('eligibilite_indemnite_inflation_jeune', period)) == 0

        return eligibilite_chomeur * (allocation <= 2000) * pas_autre


# L'éligibilité finale de l'indemnité inflation
###################################################


class eligibilite_indemnite_inflation(Variable):
    entity = Individu
    value_type = bool
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    label = "Eligibilité à l'indemnité inflation"
    definition_period = YEAR

    def formula(individu, period, parameters):

        eligible_salarie_prive = individu('eligibilite_indemnite_inflation_salarie_prive', period)
        eligible_non_salarie = individu('eligibilite_indemnite_inflation_non_salarie', period)
        eligible_public = individu('eligibilite_indemnite_inflation_public', period)
        eligible_demandeur_emploi = individu('eligibilite_indemnite_inflation_demandeur_emploi', period)
        eligible_retraite = individu('eligibilite_indemnite_inflation_retraite', period)
        eligible_prest_soc = individu('eligibilite_indemnite_inflation_prest_soc', period)
        eligible_jeune = individu('eligibilite_indemnite_inflation_jeune', period)

        return (eligible_salarie_prive + eligible_non_salarie + eligible_public + eligible_demandeur_emploi + eligible_retraite + eligible_prest_soc + eligible_jeune) > 0


# L'aide finale de l'indemnité inflation
############################################

class indemnite_inflation(Variable):
    entity = Individu
    value_type = float
    label = 'Aide exceptionnelle de 100 euros pour les individus gagnant € 2000 ou moins'
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044471405'
    definition_period = YEAR
    set_input = set_input_divide_by_period
    end = '2021-12-31'

    def formula_2021_01_01(individu, period, parameters):
        montant_indemnite = parameters(period).prestations_sociales.solidarite_insertion.autre_solidarite.indemnite_inflation
        eligibilite_indemnite_inflation = individu('eligibilite_indemnite_inflation', period.this_year)

        return montant_indemnite * (eligibilite_indemnite_inflation > 0)
