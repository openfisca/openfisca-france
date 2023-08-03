import logging
from numpy import around
from openfisca_france.model.base import *


log = logging.getLogger(__name__)

# Certaines réductions et certains crédits d'impôt sont plafonnés. Par manque de temps, la prise en compte de ces plafonnements est pour le moment
# approximative et n'est codée qu'à compter de 2013.
# Pour connaître le plafonnement d'un dispositif il faut se référer non pas à l'année de déclaration mais à l'année de la dépense. Les
# réductions pour lesquelles le plafond est approximé sont celles pour lesquelles la réduction s'étend sur plusieurs années :
#  - les investissements dans les PME (cappme),
#  - Censi-Bouvard (location_meublee),
#  - Scellier (scelli),
#  - l'investissement pour le logement touristique (invlst),
#  - la préservation du patrimoine naturel (protection_patrimoine_naturel).
# Tous ces dispostifs ont été introduits avant 2013, or si le montant du plafonnement global est le même
# depuis 2013, il a été revu à la baisse à plusieurs occasions entre 2009 et 2013. Les dépenses réalisées avant 2013 donnent donc droit à des réductions
# d'impôts, pour les déclarations après 2013, supérieures au plafond en vigueur l'année de la déclaration. Pour le moment on leur applique le montant en vigueur
# l'année de la déclaration. L'approximation qui est faite est donc une approximation qui sousestime le montant global de ces réductions d'impôt.

# TODO: le plafonnement global des réductions d'impôts avant 2013 (et la prise en compte du plafonnement des investissements d'outremer avant 2016)
# TODO: La formule ci_investissement_forestier est à améliorer, l'ordre de priorité des variables est chronologique (en cas de dépassement du plafond, il
# faut prendre en compte les variables les plus anciennes)
# TODO: prendre en compte le plafond global en vigueur au moment de l'investisement, et non le plafond en vigueur à la date de déclaration
# TODO: Améliorer la prise en compte des plafonds pour les investissements d'outremer


class reductions_plafonnees(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réductions d'impôt sur le revenu plafonnées"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        reductions_plafonnees = [
            'ri_saldom',
            'cappme',  # Approximation
            'defense_forets_contre_incendies',  # fait partie de inv. for. ?
            'gardenf',
            'ri_investissement_forestier',
            'location_meublee',  # Censi-Bouvard, plafonnement approximatif
            'invlst',  # Approximation
            'invrev',
            'protection_patrimoine_naturel',  # Approximation
            'rehab',
            'mohist',
            'souscriptions_parts_fcpi_fip',
            'duflot_pinel_denormandie_metropole',

            # Pas clair, dans le doute compté parmi les plafonnées :
            'reduction_impot_exceptionnelle',
            ]

        P = parameters(period).impot_revenu.credits_impots.plaf_nich

        # Step 1: Apply ceiling to general reductions
        montants_plaf = sum([around(foyer_fiscal(reduction, period)) for reduction in reductions_plafonnees])
        red_plaf = min_(P.plafond, montants_plaf)

        return red_plaf


class reductions_plafonnees_om_sofica(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réductions d'impôt sur le revenu plafonnées, DOM et SOFICA"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):

        reductions_om_sofica = [
            'sofica',
            'duflot_pinel_denormandie_om',
            'scelli',  # Approximation (dispositif qui se termine en 2012, soumis à des plafonds supérieurs à 18 000€)
            ]

        P = parameters(period).impot_revenu.credits_impots.plaf_nich

        red_plaf = foyer_fiscal('reductions_plafonnees', period)
        reste_gen = P.plafond - red_plaf

        # Step 2: Get additional reductions DOM-TOM and SOFICA
        # NB: Assuming the specific additional allowance is used first, and remaining general allowance is saved by preference for other reductions
        montants_om_sofica = sum([around(foyer_fiscal(reduction, period)) for reduction in reductions_om_sofica])
        red_om_sofica = min_(P.plafonnement_des_niches.majoration_om + reste_gen, montants_om_sofica)

        return red_om_sofica


class reductions_plafonnees_esus_sfs(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réductions d'impôt sur le revenu plafonnées, ESUS et SFS"
    definition_period = YEAR
    end = '2021-12-31'

    def formula_2021_01_01(foyer_fiscal, period, parameters):

        reductions_esus_sfs = [
            'cappme_esus_sfs'
            ]

        P = parameters(period).impot_revenu.credits_impots.plaf_nich

        red_plaf = foyer_fiscal('reductions_plafonnees', period)
        red_plaf_om = foyer_fiscal('reductions_plafonnees_om_sofica', period)
        reste_gen = P.plafond - red_plaf - max_(0, red_plaf_om - P.plafonnement_des_niches.majoration_om)

        # Step 3: Get additional reductions ESUS and SFS
        # NB: Assuming the specific additional allowance is used first, and remaining general allowance is saved by preference for other reductions
        montants_esus_sfs = sum([around(foyer_fiscal(reduction, period)) for reduction in reductions_esus_sfs])
        red_esus_sfs = min_(P.plafonnement_des_niches.majoration_esus_sfs + reste_gen, montants_esus_sfs)

        return red_esus_sfs


class reductions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réductions d'impôt sur le revenu"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt en prenant en compte les plafonds applicables.

        Il y a 5 catégories de réductions :
            - réductions générales soumises au plafond de 10K
            - réductions inv. outre-mer/SOFICA avec majoration de 8K
            - réductions ESUS/SFS avec majoration de 3K (2021)
            - réductions sans plafond
            - réductions d'outremer de la brochure 2042 IOM plafonnées avec des règles spécifiques supplémentaires

        Un tel plafond, avec un seuil différent, existe depuis 2008, mais n'est pour l'instant pas codé ici.
        La version codée là-dessous est celle de 2013 qui est encore valable pour l'imposition des revenus
        de 2021. Il faut insister sur le point que la version codée en bas est aussi une approximation,
        parce que pour l'imposition des revenus de l'année N, ce sont les plafonds de N, N-1, N-2, etc.
        qui s'appliquent selon l'année de l'initialisation de la réduction ou du crédit d'impôt, mais ici
        on prend juste le plafond de l'année N pour toutes les RI/CI.

        Beaucoup des dispositifs figurant parmi les réductions et crédits plafonnées
        sont dénombrés dans la loi et les brochures pratiques de l'IR, mais pas tous.
        Une règle qui peut être appliquée dans le doute, c'est que chaque dispositif est
        soumis au plafond sauf si exclu par la loi, et que souvent les dispositifs exclus
        sont ceux qui n'ont pas de contrepartie (par ex. un don ou un mécénat).
        '''

        impot_net = foyer_fiscal('ip_net', period)

        red_plaf = foyer_fiscal('reductions_plafonnees', period)
        red_plaf_om_sofica = foyer_fiscal('reductions_plafonnees_om_sofica', period)
        red_plaf_esus_sfs = foyer_fiscal('reductions_plafonnees_esus_sfs', period)
        red_deplaf = foyer_fiscal('reductions_deplafonnees', period)
        red_iom = foyer_fiscal('reductions_iom', period)

        total_reduction = red_plaf + red_plaf_om_sofica + red_plaf_esus_sfs + red_deplaf + red_iom

        return min_(impot_net, total_reduction)

    def formula(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt
        '''
        reductions = [
            # Depuis 2002
            'accult', 'frais_de_comptabilite', 'assvie', 'cappme', 'cappme_esus_sfs',
            'reduction_cotisations_syndicales',
            'accueil_dans_etablissement_personnes_agees', 'dfppce', 'doment', 'domlog',
            'reduction_enfants_scolarises', 'gardenf', 'intemp', 'ri_investissement_forestier', 'invrev',
            'prestations_compensatoires', 'rente_survie', 'ri_saldom', 'souscriptions_parts_fcpi_fip',
            # Introduites en 2003
            'mecena', 'interets_emprunt_reprise_societe',
            # Introduites en 2004
            'interets_prets_consommation', 'invlst',
            # Introduites en 2005
            'interets_paiements_differes_agriculteurs',
            # Introduites en 2006
            'creaen', 'defense_forets_contre_incendies', 'sofica',
            # Introduites en 2008
            'mohist',
            # Introduites en 2009
            'domsoc', 'codev', 'location_meublee', 'restauration_patrimoine_bati', 'scelli',
            'sofipe',
            # Introduites en 2010
            'protection_patrimoine_naturel',
            # Introduites en 2013
            'reduction_impot_exceptionnelle',
            'duflot_pinel_denormandie_metropole',
            'duflot_pinel_denormandie_om',
            # Introduites en 2017
            'rehab',
            ]

        impot_net = foyer_fiscal('ip_net', period)
        montants = [around(foyer_fiscal(reduction, period)) for reduction in reductions]
        total_reductions = sum(montants)
        return min_(impot_net, total_reductions)


class duflot_pinel_denormandie_metropole(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt Duflot - Pinel - Denormandie"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        # Duflot année N, 2013
        f7gh = foyer_fiscal('f7gh', period)  # Métropole
        f7gi = foyer_fiscal('f7gi', period)  # Outre-Mer

        inv_om = min_(P.plafond, f7gi)
        inv_metro = min_(P.plafond - inv_om, f7gh)

        ri_metro = around(inv_metro * P.taux_duflot_metro / 9)

        return ri_metro

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel
        NB: I count the reports of past Duflot investments towards Métropole,
        even though they may contain OM investments as well (only relevant after 2015,
        but since there are no separate cases, nothing one can potentially do).
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        # Duflot année N, 2013
        f7gh = foyer_fiscal('f7gh', period)  # Métropole
        f7gi = foyer_fiscal('f7gi', period)  # Outre-Mer

        # Duflot année N, 2014
        f7ek = foyer_fiscal('f7ek', period)  # Métropole
        f7el = foyer_fiscal('f7el', period)  # Outre-Mer

        # Duflot reports
        f7fi = foyer_fiscal('f7fi', period)  # 2013

        # Pinel année N, 2014
        f7qa = foyer_fiscal('f7qa_2018', period)  # Métropole, 6 ans
        f7qb = foyer_fiscal('f7qb_2018', period)  # Métropole, 9 ans
        f7qc = foyer_fiscal('f7qc_2018', period)  # Outre-Mer, 6 ans
        f7qd = foyer_fiscal('f7qd_2018', period)  # Outre-Mer, 9 ans

        # Duflot 2013

        reduc_2013 = around(P.taux_duflot_metro * min_(P.plafond - f7gi, f7gh) / 9)

        # Duflot et Pinel 2014
        max1 = max_(0, P.plafond - f7el - f7qd - f7qc)  # 2014 : plafond commun 'duflot' et 'rpinel'

        reduc_2014 = (around(P.taux_duflot_metro * min_(max1, f7ek + f7qb) / 9)
            + around(P.taux_pinel_denormandie_metro_6ans * min_(max1 - f7ek - f7qb, f7qa) / 6))

        ri_metro = reduc_2013 + reduc_2014 + f7fi

        return ri_metro

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement locatif privé - Dispositif Pinel
        De 2015 à 2018
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        # Duflot année N, 2013
        f7gh = foyer_fiscal('f7gh', period)  # Métropole
        f7gi = foyer_fiscal('f7gi', period)  # Outre-Mer

        # Duflot année N, 2014
        f7ek = foyer_fiscal('f7ek', period)  # Métropole
        f7el = foyer_fiscal('f7el', period)  # Outre-Mer

        # Duflot reports
        f7fi = foyer_fiscal('f7fi', period)  # 2013
        f7fk = foyer_fiscal('f7fk', period)  # 2014
        f7fr = foyer_fiscal('f7fr', period)  # 2015
        f7fv = foyer_fiscal('f7fv', period)  # 2016
        f7fw = foyer_fiscal('f7fw', period)  # 2017

        # Pinel année N, 2014
        f7qa = foyer_fiscal('f7qa_2018', period)  # Métropole, 6 ans
        f7qb = foyer_fiscal('f7qb_2018', period)  # Métropole, 9 ans
        f7qc = foyer_fiscal('f7qc_2018', period)  # Outre-Mer, 6 ans
        f7qd = foyer_fiscal('f7qd_2018', period)  # Outre-Mer, 9 ans

        cases_investissement = {
            2015: [
                ('f7qh', 9, 'outremer'),
                ('f7qg', 6, 'outremer'),
                ('f7qf', 9, 'metropole'),
                ('f7qe', 6, 'metropole')],
            2016: [
                ('f7ql_2019', 9, 'outremer'),
                ('f7qk_2019', 6, 'outremer'),
                ('f7qj_2019', 9, 'metropole'),
                ('f7qi_2019', 6, 'metropole')],
            2017: [
                ('f7qp', 9, 'outremer'),
                ('f7qo', 6, 'outremer'),
                ('f7qn', 9, 'metropole'),
                ('f7qm', 6, 'metropole')],
            2018: [
                ('f7qu', 9, 'outremer'),
                ('f7qt', 6, 'outremer'),
                ('f7qs', 9, 'metropole'),
                ('f7qr', 6, 'metropole')],
            }

        cases_report = {
            2014: ['f7ai', 'f7bi'],
            2015: ['f7bz', 'f7cz'],
            2016: ['f7qz', 'f7rz'],
            2017: ['f7ra', 'f7rb'],
            }

        # Duflot 2013
        reduc_2013 = around(P.taux_duflot_metro * min_(P.plafond - f7gi, f7gh) / 9)

        # Duflot et Pinel 2014
        max1 = max_(0, P.plafond - f7el - f7qd - f7qc)  # 2014 : plafond commun 'duflot' et 'rpinel'

        reduc_2014 = (around(P.taux_duflot_metro * min_(max1, f7ek + f7qb) / 9)
            + around(P.taux_pinel_denormandie_metro_6ans * min_(max1 - f7ek - f7qb, f7qa) / 6))

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'metropole':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_metro_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_metro_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2015, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        return reduction_cumulee + report + reduc_2013 + reduc_2014 + f7fi + f7fk + f7fr + f7fv + f7fw

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel + Denormandie
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        cases_investissement = {
            2019: [  # A compter de 2019, le plafonnement de la base de calcul est commun à tous les investissements réalisés
                ('f7ql_2019', 9, 'outremer'),  # Pinel 2016
                ('f7qp', 9, 'outremer'),  # Pinel 2017
                ('f7qu', 9, 'outremer'),  # Pinel 2018
                ('f7qq', 9, 'outremer'),  # Pinel 2019
                ('f7nd', 9, 'outremer'),  # Denormandie
                ('f7qk_2019', 6, 'outremer'),  # Pinel 2016
                ('f7qo', 6, 'outremer'),  # Pinel 2017
                ('f7qt', 6, 'outremer'),  # Pinel 2018
                ('f7qy', 6, 'outremer'),  # Pinel
                ('f7nc', 6, 'outremer'),  # Denormandie
                ('f7qj_2019', 9, 'metropole'),  # Pinel 2016
                ('f7qn', 9, 'metropole'),  # Pinel 2017
                ('f7qs', 9, 'metropole'),  # Pinel 2018
                ('f7qx', 9, 'metropole'),  # Pinel 2019
                ('f7nb', 9, 'metropole'),  # Denormandie
                ('f7qi_2019', 6, 'metropole'),  # Pinel 2016
                ('f7qm', 6, 'metropole'),  # Pinel 2017
                ('f7qr', 6, 'metropole'),  # Pinel 2018
                ('f7qw', 6, 'metropole'),  # Pinel 2019
                ('f7na', 6, 'metropole')],  # Denormandie
            }

        cases_report = {
            2014: ['f7ai', 'f7bi'],
            2015: ['f7bz', 'f7cz'],
            2016: ['f7qz', 'f7rz'],
            2017: ['f7ra', 'f7rb'],
            2018: ['f7re', 'f7rf']
            }

        # Duflot reports
        f7fi = foyer_fiscal('f7fi', period)  # 2013
        f7fk = foyer_fiscal('f7fk', period)  # 2014
        f7fr = foyer_fiscal('f7fr', period)  # 2015
        f7fv = foyer_fiscal('f7fv', period)  # 2016
        f7fw = foyer_fiscal('f7fw', period)  # 2017
        f7fx = foyer_fiscal('f7fx', period)  # 2018

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'metropole':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_metro_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_metro_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2016, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        return reduction_cumulee + report + f7fi + f7fk + f7fr + f7fv + f7fw + f7fx

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel + Denormandie
        NB: it is not clear whether the extension of the Pinel investment should also
        count towards the ceiling of € 300K. I will assume it does.
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie
        cases_investissement = {
            2019: [  # A compter de 2019, le plafonnement de la base de calcul est commun à tous les investissements réalisés
                ('f7qp', 9, 'outremer'),  # Pinel 2017
                ('f7qu', 9, 'outremer'),  # Pinel 2018
                ('f7qq', 9, 'outremer'),  # Pinel 2019
                ('f7nd', 9, 'outremer'),  # Denormandie 2019
                ('f7qd', 9, 'outremer'),  # Pinel 2020
                ('f7nh', 9, 'outremer'),  # Denormandie 2020
                ('f7qo', 6, 'outremer'),  # Pinel 2017
                ('f7qt', 6, 'outremer'),  # Pinel 2018
                ('f7qy', 6, 'outremer'),  # Pinel 2019
                ('f7nc', 6, 'outremer'),  # Denormandie 2019
                ('f7qc', 6, 'outremer'),  # Pinel 2020
                ('f7ng', 6, 'outremer'),  # Denormandie 2020
                ('f7qn', 9, 'metropole'),  # Pinel 2017
                ('f7qs', 9, 'metropole'),  # Pinel 2018
                ('f7qx', 9, 'metropole'),  # Pinel 2019
                ('f7nb', 9, 'metropole'),  # Denormandie 2019
                ('f7qb', 9, 'metropole'),  # Pinel 2020
                ('f7nf', 9, 'metropole'),  # Denormandie 2020
                ('f7qm', 6, 'metropole'),  # Pinel 2017
                ('f7qr', 6, 'metropole'),  # Pinel 2018
                ('f7qw', 6, 'metropole'),  # Pinel 2019
                ('f7na', 6, 'metropole'),  # Denormandie 2019
                ('f7qa', 6, 'metropole'),  # Pinel 2020
                ('f7ne', 6, 'metropole')],  # Denormandie 2020
            }

        cases_report = {
            2014: ['f7bi'],
            2015: ['f7bz', 'f7cz'],
            2016: ['f7qz', 'f7rz'],
            2017: ['f7ra', 'f7rb'],
            2018: ['f7re', 'f7rf'],
            2019: ['f7jm', 'f7km', 'f7ja', 'f7jb']  # reports Pinel et denormandie
            }

        # Duflot reports
        f7fi = foyer_fiscal('f7fi', period)  # 2013
        f7fk = foyer_fiscal('f7fk', period)  # 2014
        f7fr = foyer_fiscal('f7fr', period)  # 2015
        f7fv = foyer_fiscal('f7fv', period)  # 2016
        f7fw = foyer_fiscal('f7fw', period)  # 2017
        f7fx = foyer_fiscal('f7fx', period)  # 2018

        # Première prorogation, 6 ans, 2014
        f7rr = foyer_fiscal('f7rr', period)  # Métropole, 6 ans
        f7rs = foyer_fiscal('f7rs', period)  # Outre-Mer, 6 ans

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'metropole':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_metro_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_metro_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2018, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        prorogation = around(min_(P.plafond - f7rs, f7rr) * P.taux_prolong1_6ans / 3)

        return reduction_cumulee + report + f7fi + f7fk + f7fr + f7fv + f7fw + f7fx + prorogation

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel + Denormandie
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie
        cases_investissement = {
            2019: [  # A compter de 2019, le plafonnement de la base de calcul est commun à tous les investissements réalisés
                ('f7qu', 9, 'outremer'),
                ('f7qq', 9, 'outremer'),  # Pinel 2019
                ('f7nd', 9, 'outremer'),  # Denormandie 2019
                ('f7qd', 9, 'outremer'),  # Pinel 2020
                ('f7nh', 9, 'outremer'),  # Denormandie 2020
                ('f7ql', 9, 'outremer'),  # Pinel 2021
                ('f7nl', 9, 'outremer'),  # Denormandie 2021
                ('f7qt', 6, 'outremer'),  # Pinel 2018
                ('f7qy', 6, 'outremer'),  # Pinel 2019
                ('f7nc', 6, 'outremer'),  # Denormandie 2019
                ('f7qc', 6, 'outremer'),  # Pinel 2020
                ('f7ng', 6, 'outremer'),  # Denormandie 2020
                ('f7qk', 6, 'outremer'),  # Pinel 2021
                ('f7nk', 6, 'outremer'),  # Denormandie 2021
                ('f7qs', 9, 'metropole'),  # Pinel 2018
                ('f7qx', 9, 'metropole'),  # Pinel 2019
                ('f7nb', 9, 'metropole'),  # Denormandie 2019
                ('f7qb', 9, 'metropole'),  # Pinel 2020
                ('f7nf', 9, 'metropole'),  # Denormandie 2020
                ('f7qj', 9, 'metropole'),  # Pinel 2021
                ('f7nj', 9, 'metropole'),  # Denormandie 2021
                ('f7qr', 6, 'metropole'),  # Pinel 2018
                ('f7qw', 6, 'metropole'),  # Pinel 2019
                ('f7na', 6, 'metropole'),  # Denormandie 2019
                ('f7qa', 6, 'metropole'),  # Pinel 2020
                ('f7ne', 6, 'metropole'),  # Denormandie 2020
                ('f7qi', 6, 'metropole'),  # Pinel 2021
                ('f7ni', 6, 'metropole')],  # Denormandie 2021
            }

        cases_report = {
            2014: ['f7bi'],
            2015: ['f7cz'],
            2016: ['f7qz', 'f7rz'],
            2017: ['f7ra', 'f7rb'],
            2018: ['f7re', 'f7rf'],
            2019: ['f7jm', 'f7km', 'f7ja', 'f7jb'],  # reports Pinel et denormandie
            2020: ['f7jn', 'f7jo', 'f7jr', 'f7js']  # reports Pinel et denormandie
            }

        # Duflot reports
        f7fi = foyer_fiscal('f7fi', period)  # 2013
        f7fk = foyer_fiscal('f7fk', period)  # 2014
        f7fr = foyer_fiscal('f7fr', period)  # 2015
        f7fv = foyer_fiscal('f7fv', period)  # 2016
        f7fw = foyer_fiscal('f7fw', period)  # 2017
        f7fx = foyer_fiscal('f7fx', period)  # 2018

        # Première prorogation, 6 ans
        f7rr = foyer_fiscal('f7rr', period)  # Métropole, 6 ans 2014
        f7rs = foyer_fiscal('f7rs', period)  # Outre-Mer, 6 ans 2014
        f7rx = foyer_fiscal('f7rx', period)  # Métropole, 2015
        f7ry = foyer_fiscal('f7ry', period)  # Outre-Mer, 2015

        # Prorogation reports, 6 ans
        f7sx = foyer_fiscal('f7sx', period)  # Métropole, 2014

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'metropole':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_metro_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_metro_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2018, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        prorogation = (around(min_(P.plafond - f7rs, f7rr) * P.taux_prolong1_6ans / 3)
            + around(min_(P.plafond - f7ry, f7rx) * P.taux_prolong1_6ans / 3))

        return reduction_cumulee + report + f7fi + f7fk + f7fr + f7fv + f7fw + f7fx + prorogation + f7sx


class duflot_pinel_denormandie_om(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt Duflot - Pinel - Denormandie"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        # Duflot année N, 2013
        f7gi = foyer_fiscal('f7gi', period)  # Outre-Mer

        inv_om = min_(P.plafond, f7gi)

        ri_om = around(inv_om * P.taux_duflot_om / 9)

        return ri_om

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel
        NB: I count the reports of past Duflot investments towards Métropole,
        even though they may contain OM investments as well (only relevant after 2015,
        but since there are no separate cases, nothing one can potentially do).
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        # Duflot année N, 2013
        f7gi = foyer_fiscal('f7gi', period)  # Outre-Mer

        # Duflot année N, 2014
        f7el = foyer_fiscal('f7el', period)  # Outre-Mer

        # Pinel année N, 2014
        f7qc = foyer_fiscal('f7qc_2018', period)  # Outre-Mer, 6 ans
        f7qd = foyer_fiscal('f7qd_2018', period)  # Outre-Mer, 9 ans

        # Duflot 2013
        reduc_2013 = around(P.taux_duflot_om * min_(P.plafond, f7gi) / 9)

        # Duflot et Pinel 2014
        inv_29_om = min_(P.plafond, f7el + f7qd)
        inv_23_om = min_(P.plafond - inv_29_om, f7qc)

        reduc = (around((inv_29_om * P.taux_duflot_om / 9)
            + around(inv_23_om * P.taux_pinel_denormandie_om_6ans / 6))) + reduc_2013

        return reduc

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        # Duflot année N, 2013
        f7gi = foyer_fiscal('f7gi', period)  # Outre-Mer

        # Duflot année N, 2014
        f7el = foyer_fiscal('f7el', period)  # Outre-Mer

        # Pinel année N, 2014
        f7qc = foyer_fiscal('f7qc_2018', period)  # Outre-Mer, 6 ans
        f7qd = foyer_fiscal('f7qd_2018', period)  # Outre-Mer, 9 ans

        # Duflot 2013
        reduc_2013 = P.taux_duflot_om * min_(P.plafond, f7gi) / 9

        # Duflot et Pinel 2014
        reduc_2014 = (around(P.taux_duflot_om * min_(P.plafond, f7el + f7qd) / 9)
            + around(P.taux_pinel_denormandie_om_6ans * min_(P.plafond - f7el - f7qd, f7qc) / 6))

        cases_investissement = {
            2015: [
                ('f7qh', 9, 'outremer'),
                ('f7qg', 6, 'outremer'),
                ('f7qf', 9, 'metropole'),
                ('f7qe', 6, 'metropole')],
            2016: [
                ('f7ql_2019', 9, 'outremer'),
                ('f7qk_2019', 6, 'outremer'),
                ('f7qj_2019', 9, 'metropole'),
                ('f7qi_2019', 6, 'metropole')],
            2017: [
                ('f7qp', 9, 'outremer'),
                ('f7qo', 6, 'outremer'),
                ('f7qn', 9, 'metropole'),
                ('f7qm', 6, 'metropole')],
            2018: [
                ('f7qu', 9, 'outremer'),
                ('f7qt', 6, 'outremer'),
                ('f7qs', 9, 'metropole'),
                ('f7qr', 6, 'metropole')],
            }

        cases_report = {
            2014: ['f7ci_2019', 'f7di'],
            2015: ['f7dz', 'f7ez'],
            2016: ['f7sz', 'f7tz'],
            2017: ['f7rc', 'f7rd'],
            }

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'outremer':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_om_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_om_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2015, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        return reduction_cumulee + report + reduc_2013 + reduc_2014

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel + Denormandie
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        cases_investissement = {
            2019: [  # A compter de 2019, le plafonnement de la base de calcul est commun à tous les investissements réalisés
                ('f7ql_2019', 9, 'outremer'),  # Pinel 2016
                ('f7qp', 9, 'outremer'),  # Pinel 2017
                ('f7qu', 9, 'outremer'),  # Pinel 2018
                ('f7qq', 9, 'outremer'),  # Pinel 2019
                ('f7nd', 9, 'outremer'),  # Denormandie
                ('f7qk_2019', 6, 'outremer'),  # Pinel 2016
                ('f7qo', 6, 'outremer'),  # Pinel 2017
                ('f7qt', 6, 'outremer'),  # Pinel 2018
                ('f7qy', 6, 'outremer'),  # Pinel
                ('f7nc', 6, 'outremer'),  # Denormandie
                ('f7qj_2019', 9, 'metropole'),  # Pinel 2016
                ('f7qn', 9, 'metropole'),  # Pinel 2017
                ('f7qs', 9, 'metropole'),  # Pinel 2018
                ('f7qx', 9, 'metropole'),  # Pinel 2019
                ('f7nb', 9, 'metropole'),  # Denormandie
                ('f7qi_2019', 6, 'metropole'),  # Pinel 2016
                ('f7qm', 6, 'metropole'),  # Pinel 2017
                ('f7qr', 6, 'metropole'),  # Pinel 2018
                ('f7qw', 6, 'metropole'),  # Pinel 2019
                ('f7na', 6, 'metropole')],  # Denormandie
            }

        cases_report = {
            2014: ['f7ci_2019', 'f7di'],
            2015: ['f7dz', 'f7ez'],
            2016: ['f7sz', 'f7tz'],
            2017: ['f7rc', 'f7rd'],
            2018: ['f7rg', 'f7rh'],
            }

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'outremer':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_om_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_om_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2016, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        return reduction_cumulee + report

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel + Denormandie
        NB: it is not clear whether the extension of the Pinel investment should also
        count towards the ceiling of € 300K. I will assume it does.
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        cases_investissement = {
            2019: [  # A compter de 2019, le plafonnement de la base de calcul est commun à tous les investissements réalisés
                ('f7qp', 9, 'outremer'),  # Pinel 2017
                ('f7qu', 9, 'outremer'),  # Pinel 2018
                ('f7qq', 9, 'outremer'),  # Pinel 2019
                ('f7nd', 9, 'outremer'),  # Denormandie 2019
                ('f7qd', 9, 'outremer'),  # Pinel 2020
                ('f7nh', 9, 'outremer'),  # Denormandie 2020
                ('f7qo', 6, 'outremer'),  # Pinel 2017
                ('f7qt', 6, 'outremer'),  # Pinel 2018
                ('f7qy', 6, 'outremer'),  # Pinel 2019
                ('f7nc', 6, 'outremer'),  # Denormandie 2019
                ('f7qc', 6, 'outremer'),  # Pinel 2020
                ('f7ng', 6, 'outremer'),  # Denormandie 2020
                ('f7qn', 9, 'metropole'),  # Pinel 2017
                ('f7qs', 9, 'metropole'),  # Pinel 2018
                ('f7qx', 9, 'metropole'),  # Pinel 2019
                ('f7nb', 9, 'metropole'),  # Denormandie 2019
                ('f7qb', 9, 'metropole'),  # Pinel 2020
                ('f7nf', 9, 'metropole'),  # Denormandie 2020
                ('f7qm', 6, 'metropole'),  # Pinel 2017
                ('f7qr', 6, 'metropole'),  # Pinel 2018
                ('f7qw', 6, 'metropole'),  # Pinel 2019
                ('f7na', 6, 'metropole'),  # Denormandie 2019
                ('f7qa', 6, 'metropole'),  # Pinel 2020
                ('f7ne', 6, 'metropole')],  # Denormandie 2020
            }

        cases_report = {
            2014: ['f7di'],
            2015: ['f7dz', 'f7ez'],
            2016: ['f7sz', 'f7tz'],
            2017: ['f7rc', 'f7rd'],
            2018: ['f7rg', 'f7rh'],
            2019: ['f7lm', 'f7mm', 'f7jc', 'f7jd'],  # Pinel et Denormandie
            }

        # Première prorogation, 6 ans, 2014
        f7rs = foyer_fiscal('f7rs', period)  # Outre-Mer, 6 ans

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'outremer':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_om_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_om_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2016, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        prorogation = around(min_(P.plafond, f7rs) * P.taux_prolong1_6ans / 3)

        return reduction_cumulee + report + prorogation

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Duflot + Pinel + Denormandie
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.duflot_pinel_denormandie

        cases_investissement = {
            2019: [  # A compter de 2019, le plafonnement de la base de calcul est commun à tous les investissements réalisés
                ('f7qq', 9, 'outremer'),  # Pinel 2019
                ('f7nd', 9, 'outremer'),  # Denormandie 2019
                ('f7qd', 9, 'outremer'),  # Pinel 2020
                ('f7nh', 9, 'outremer'),  # Denormandie 2020
                ('f7ql', 9, 'outremer'),  # Pinel 2021
                ('f7nl', 9, 'outremer'),  # Denormandie 2021
                ('f7qt', 6, 'outremer'),  # Pinel 2018
                ('f7qy', 6, 'outremer'),  # Pinel 2019
                ('f7nc', 6, 'outremer'),  # Denormandie 2019
                ('f7qc', 6, 'outremer'),  # Pinel 2020
                ('f7ng', 6, 'outremer'),  # Denormandie 2020
                ('f7qk', 6, 'outremer'),  # Pinel 2021
                ('f7nk', 6, 'outremer'),  # Denormandie 2021
                ('f7qs', 9, 'metropole'),  # Pinel 2018
                ('f7qx', 9, 'metropole'),  # Pinel 2019
                ('f7nb', 9, 'metropole'),  # Denormandie 2019
                ('f7qb', 9, 'metropole'),  # Pinel 2020
                ('f7nf', 9, 'metropole'),  # Denormandie 2020
                ('f7qj', 9, 'metropole'),  # Pinel 2021
                ('f7nj', 9, 'metropole'),  # Denormandie 2021
                ('f7qr', 6, 'metropole'),  # Pinel 2018
                ('f7qw', 6, 'metropole'),  # Pinel 2019
                ('f7na', 6, 'metropole'),  # Denormandie 2019
                ('f7qa', 6, 'metropole'),  # Pinel 2020
                ('f7ne', 6, 'metropole'),  # Denormandie 2020
                ('f7qi', 6, 'metropole'),  # Pinel 2021
                ('f7ni', 6, 'metropole')],  # Denormandie 2021
            }

        cases_report = {
            2014: ['f7di'],
            2015: ['f7ez'],
            2016: ['f7sz', 'f7tz'],
            2017: ['f7rc', 'f7rd'],
            2018: ['f7rg', 'f7rh'],
            2019: ['f7lm', 'f7mm', 'f7jc', 'f7jd'],  # Pinel et Denormandie
            2020: ['f7jp', 'f7jq', 'f7jt', 'f7ju'],  # Pinel et Denormandie
            }

        # Première prorogation, 6 ans
        f7rs = foyer_fiscal('f7rs', period)  # Outre-Mer, 2014
        f7ry = foyer_fiscal('f7ry', period)  # Outre-Mer, 2015

        # Prorogation reports, 6 ans
        f7sy = foyer_fiscal('f7sy', period)  # Outre-Mer, 2014

        def calcul_reduction_investissement(cases):
            reduction = foyer_fiscal.empty_array()
            depenses_cumulees = foyer_fiscal.empty_array()
            for case in cases:
                variable, duree, zone = case
                depense = foyer_fiscal(variable, period)
                if zone == 'outremer':
                    if duree == 9:
                        reduction += around(P.taux_pinel_denormandie_om_9ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                    elif duree == 6:
                        reduction += around(P.taux_pinel_denormandie_om_6ans * min_(max_(0, P.plafond - depenses_cumulees), depense) / duree)
                depenses_cumulees += depense
            return reduction

        annee_fiscale = period.start.year
        range_year_investissement = list(set([year for year in range(2016, annee_fiscale + 1)]) & set([year for year in cases_investissement.keys()]))
        range_year_report = list(set([year for year in range(2014, annee_fiscale)]) & set([year for year in cases_report.keys()]))

        reduction_cumulee = sum([calcul_reduction_investissement(cases_investissement[year]) for year in range_year_investissement])
        report = sum([foyer_fiscal(case, period) for year in range_year_report for case in cases_report[year]])

        prorogation = (around(min_(P.plafond, f7rs) * P.taux_prolong1_6ans / 3)
            + around(min_(P.plafond, f7ry) * P.taux_prolong1_6ans / 3))

        return reduction_cumulee + report + prorogation + f7sy


class cappme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt au titre des souscriptions en numéraire au capital de PME non côtées"
    reference = 'http://bofip.impots.gouv.fr/bofip/4374-PGP'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2002
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        base = f7cf
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2003
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        base = f7cf + f7cl
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2004
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        base = f7cf + f7cl + f7cm
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2005-2008
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        base = f7cf + f7cl + f7cm + f7cn
        seuil = P.seuil * (maries_ou_pacses + 1)
        return P.taux * min_(base, seuil)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2009-2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        base = f7cf + f7cl + f7cm + f7cn + f7cu
        seuil = P.seuil * (maries_ou_pacses + 1)
        seuil = P.seuil_tpe * (maries_ou_pacses + 1) * (f7cu > 0) + P.seuil * (maries_ou_pacses + 1) * (f7cu <= 0)
        return P.taux * min_(base, seuil)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        base = f7cl + f7cm + f7cn + f7cq
        seuil = P.seuil_tpe * (maries_ou_pacses + 1) * (f7cu > 0) + P.seuil * (maries_ou_pacses + 1) * (f7cu <= 0)
        max0 = max_(seuil - base, 0)
        return max_(P.taux25 * min_(base, seuil), P.taux * min_(max0, f7cf + f7cu))

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2012 cf. 2041 GR
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        # TODO: gérer les changements de situation familiale
        base = f7cl + f7cm + f7cn
        seuil1 = P.seuil * (maries_ou_pacses + 1)
        seuil2 = max_(0, P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cq, seuil1) - min_(f7cu, seuil1))
        seuil3 = min_(P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cq, seuil1), seuil1)

        return (
            P.taux25 * min_(base, seuil1)
            + P.taux * min_(f7cq, seuil1)
            + P.taux18 * (min_(f7cf, seuil3) + mini(f7cu, seuil2, seuil1))
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2013
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cc = foyer_fiscal('f7cc', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cu = foyer_fiscal('f7cu', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        base = f7cl + f7cm
        seuil1 = P.seuil * (maries_ou_pacses + 1)
        seuil2 = max_(0, P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cn, seuil1) - min_(f7cu, seuil1))
        seuil3 = min_(P.seuil_tpe * (maries_ou_pacses + 1) - min_(base, seuil1) - min_(f7cq, seuil1), seuil1)

        return (
            P.taux25 * min_(base, seuil1)
            + P.taux22 * min_(f7cn, seuil1)
            + P.taux18 * (min_(f7cf + f7cc, seuil3) + min_(f7cu + f7cq, seuil2))
            )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2014
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cc = foyer_fiscal('f7cc', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cu = foyer_fiscal('f7cu', period)
        report_cappme_2013_plaf_general = foyer_fiscal('f7cy', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        seuil1 = P.seuil * (maries_ou_pacses + 1)
        seuil2 = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement PME : imputation du plus ancien au plus récent
        base_report_cappme_2010_PME = min_(f7cl, seuil1)
        base_report_cappme_2011_PME = max_(0, min_(f7cm, seuil1) - base_report_cappme_2010_PME)
        base_report_cappme_2012_PME = max_(0, min_(f7cn, seuil1 - base_report_cappme_2010_PME - base_report_cappme_2011_PME))
        base_report_cappme_2013_PME = max_(0, min_(f7cc, seuil1 - base_report_cappme_2010_PME - base_report_cappme_2011_PME - base_report_cappme_2012_PME))
        base_cappme_2014_PME = max_(0, min_(f7cu, seuil1 - base_report_cappme_2010_PME - base_report_cappme_2011_PME - base_report_cappme_2012_PME - base_report_cappme_2013_PME))

        # Réduction investissement TPE : imputation du plus ancien au plus récent
        base_report_cappme_2012_TPE = min_(f7cq, seuil2)
        base_report_cappme_2013_TPE = max_(0, min_(f7cr, seuil2 - base_report_cappme_2012_TPE))
        base_cappme_2014_TPE = max_(0, min_(f7cf, seuil2 - base_report_cappme_2012_TPE - base_report_cappme_2013_TPE))

        seuil3 = seuil2 - min_(seuil2, base_report_cappme_2010_PME)
        seuil4 = seuil3 - min_(seuil3, base_report_cappme_2010_PME + base_report_cappme_2011_PME)

        return (
            report_cappme_2013_plaf_general
            + min_(seuil2, base_report_cappme_2010_PME) * P.taux25
            + min_(seuil3, base_report_cappme_2011_PME) * P.taux22
            + min_(
                seuil4,
                base_report_cappme_2012_PME
                + base_report_cappme_2013_PME
                + base_cappme_2014_PME
                + base_report_cappme_2012_TPE
                + base_report_cappme_2013_TPE
                + base_cappme_2014_TPE
                ) * P.taux18
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2015
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7cc = foyer_fiscal('f7cc', period)
        f7cf = foyer_fiscal('f7cf', period)
        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cu = foyer_fiscal('f7cu', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cy = foyer_fiscal('f7cy', period)
        f7dy = foyer_fiscal('f7dy', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        seuil1 = P.seuil * (maries_ou_pacses + 1)
        seuil2 = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement PME : imputation du plus ancien au plus récent
        base_report_cappme_2011_PME = min_(f7cl, seuil1)
        base_report_cappme_2012_PME = max_(0, min_(f7cm, seuil1) - base_report_cappme_2011_PME)
        base_report_cappme_2013_PME = max_(0, min_(f7cn, seuil1 - base_report_cappme_2011_PME - base_report_cappme_2012_PME))
        base_report_cappme_2014_PME = max_(0, min_(f7cc, seuil1 - base_report_cappme_2011_PME - base_report_cappme_2012_PME - base_report_cappme_2013_PME))
        base_cappme_2015_PME = max_(0, min_(f7cu, seuil1 - base_report_cappme_2011_PME - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME))

        # Réduction investissement TPE : imputation du plus ancien au plus récent
        base_report_cappme_2012_TPE = min_(f7cq, seuil2)
        base_report_cappme_2013_TPE = max_(0, min_(f7cr, seuil2 - base_report_cappme_2012_TPE))
        base_report_cappme_2014_TPE = max_(0, min_(f7cv, seuil2 - base_report_cappme_2012_TPE - base_report_cappme_2013_TPE))
        base_cappme_2015_TPE = max_(0, min_(f7cf, seuil2 - base_report_cappme_2012_TPE - base_report_cappme_2013_TPE - base_report_cappme_2014_TPE))

        report_cappme_2013_plaf_general = f7cy
        report_cappme_2014_plaf_general = f7dy

        seuil3 = seuil2 - min_(seuil2, base_report_cappme_2011_PME)

        return (
            report_cappme_2013_plaf_general
            + report_cappme_2014_plaf_general
            + P.taux22 * min_(seuil2, base_report_cappme_2011_PME)
            + P.taux18 * min_(
                seuil3,
                base_report_cappme_2012_PME
                + base_report_cappme_2013_PME
                + base_report_cappme_2014_PME
                + base_cappme_2015_PME
                + base_report_cappme_2012_TPE
                + base_report_cappme_2013_TPE
                + base_report_cappme_2014_TPE
                + base_cappme_2015_TPE
                )
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2016
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7cf = foyer_fiscal('f7cf', period)

        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cc = foyer_fiscal('f7cc', period)
        f7cu = foyer_fiscal('f7cu', period)

        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cx = foyer_fiscal('f7cx', period)

        f7cy = foyer_fiscal('f7cy', period)
        f7dy = foyer_fiscal('f7dy', period)
        f7ey = foyer_fiscal('f7ey', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        seuil1 = P.seuil * (maries_ou_pacses + 1)
        seuil2 = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement PME : imputation du plus ancien au plus récent
        base_report_cappme_2012_PME = min_(f7cl, seuil1)
        base_report_cappme_2013_PME = max_(0, min_(f7cm, seuil1 - base_report_cappme_2012_PME))
        base_report_cappme_2014_PME = max_(0, min_(f7cn, seuil1 - base_report_cappme_2012_PME - base_report_cappme_2013_PME))
        base_report_cappme_2015_PME = max_(0, min_(f7cc, seuil1 - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME))
        base_cappme_2016_PME = max_(0, min_(f7cu, seuil1 - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME))

        # Réduction investissement TPE : imputation du plus ancien au plus récent
        base_report_cappme_2012_TPE = min_(f7cq, seuil2 - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME)
        base_report_cappme_2013_TPE = max_(0, min_(f7cr, seuil2 - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2012_TPE))
        base_report_cappme_2014_TPE = max_(0, min_(f7cv, seuil2 - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2012_TPE - base_report_cappme_2013_TPE))
        base_report_cappme_2015_TPE = max_(0, min_(f7cx, seuil2 - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2012_TPE - base_report_cappme_2013_TPE - base_report_cappme_2014_TPE))
        base_cappme_2016_TPE = max_(0, min_(f7cf, seuil2 - base_report_cappme_2012_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2012_TPE - base_report_cappme_2013_TPE - base_report_cappme_2014_TPE - base_report_cappme_2015_TPE))

        reports_plaf_general = f7cy + f7dy + f7ey

        return (
            reports_plaf_general
            + P.taux18 * (base_report_cappme_2012_PME
                + base_report_cappme_2013_PME
                + base_report_cappme_2014_PME
                + base_report_cappme_2015_PME
                + base_cappme_2016_PME
                + base_report_cappme_2012_TPE
                + base_report_cappme_2013_TPE
                + base_report_cappme_2014_TPE
                + base_report_cappme_2015_TPE
                + base_cappme_2016_TPE)
            )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2017
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7cf = foyer_fiscal('f7cf', period)

        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)
        f7cc = foyer_fiscal('f7cc', period)

        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cx = foyer_fiscal('f7cx', period)

        f7cy = foyer_fiscal('f7cy', period)
        f7dy = foyer_fiscal('f7dy', period)
        f7ey = foyer_fiscal('f7ey', period)
        f7fy = foyer_fiscal('f7fy', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        plafond_PME = P.seuil * (maries_ou_pacses + 1)
        plafond_TPE = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement PME (souscription avant 2012) : imputation du plus ancien au plus récent
        base_report_cappme_2013_PME = min_(f7cl, plafond_PME)
        base_report_cappme_2014_PME = max_(0, min_(f7cm, plafond_PME - base_report_cappme_2013_PME))
        base_report_cappme_2015_PME = max_(0, min_(f7cn, plafond_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME))
        base_report_cappme_2016_PME = max_(0, min_(f7cc, plafond_PME - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME))

        # Réduction investissement TPE (souscription à partir de 2012) : imputation du plus ancien au plus récent
        base_report_cappme_2013_TPE = min_(f7cq, plafond_TPE)
        base_report_cappme_2014_TPE = max_(0, min_(f7cr, plafond_TPE - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2013_TPE))
        base_report_cappme_2015_TPE = max_(0, min_(f7cv, plafond_TPE - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2013_TPE - base_report_cappme_2014_TPE))
        base_report_cappme_2016_TPE = max_(0, min_(f7cx, plafond_TPE - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2013_TPE - base_report_cappme_2014_TPE - base_report_cappme_2015_TPE))

        # Réduction investissements de l'année courante
        base_cappme_2017 = max_(0, min_(f7cf, plafond_TPE - base_report_cappme_2013_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2013_TPE - base_report_cappme_2014_TPE - base_report_cappme_2015_TPE - base_report_cappme_2016_TPE))

        reports_plaf_general = f7cy + f7dy + f7ey + f7fy

        return (
            reports_plaf_general
            + P.taux18 * (base_cappme_2017
                + base_report_cappme_2013_PME
                + base_report_cappme_2014_PME
                + base_report_cappme_2015_PME
                + base_report_cappme_2016_PME
                + base_report_cappme_2013_TPE
                + base_report_cappme_2014_TPE
                + base_report_cappme_2015_TPE
                + base_report_cappme_2016_TPE)
            )

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2018
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7cf = foyer_fiscal('f7cf', period)

        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)
        f7cn = foyer_fiscal('f7cn', period)

        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cx = foyer_fiscal('f7cx', period)

        f7cy = foyer_fiscal('f7cy', period)
        f7dy = foyer_fiscal('f7dy', period)
        f7ey = foyer_fiscal('f7ey', period)
        f7fy = foyer_fiscal('f7fy', period)
        f7gy = foyer_fiscal('f7gy', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        plafond_PME = P.seuil * (maries_ou_pacses + 1)
        plafond_TPE = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement PME (souscription avant 2012) : imputation du plus ancien au plus récent
        base_report_cappme_2014_PME = min_(f7cl, plafond_PME)
        base_report_cappme_2015_PME = max_(0, min_(f7cm, plafond_PME - base_report_cappme_2014_PME))
        base_report_cappme_2016_PME = max_(0, min_(f7cn, plafond_PME - base_report_cappme_2014_PME - base_report_cappme_2015_PME))

        # Réduction investissement TPE (souscription à partir de 2012) : imputation du plus ancien au plus récent
        base_report_cappme_2014_TPE = min_(f7cq, plafond_TPE - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME)
        base_report_cappme_2015_TPE = max_(0, min_(f7cr, plafond_TPE - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2014_TPE))
        base_report_cappme_2016_TPE = max_(0, min_(f7cv, plafond_TPE - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2014_TPE - base_report_cappme_2015_TPE))
        base_report_cappme_2017_TPE = max_(0, min_(f7cx, plafond_TPE - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2014_TPE - base_report_cappme_2015_TPE - base_report_cappme_2016_TPE))

        # Réduction investissements de l'année courante
        base_cappme_2018 = max_(0, min_(f7cf, plafond_TPE - base_report_cappme_2014_PME - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2014_TPE - base_report_cappme_2015_TPE - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE))

        reports_plaf_general = f7cy + f7dy + f7ey + f7fy + f7gy

        return (
            reports_plaf_general
            + P.taux18 * (base_cappme_2018
                + base_report_cappme_2014_PME
                + base_report_cappme_2015_PME
                + base_report_cappme_2016_PME
                + base_report_cappme_2014_TPE
                + base_report_cappme_2015_TPE
                + base_report_cappme_2016_TPE
                + base_report_cappme_2017_TPE)
            )

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2019
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7cf = foyer_fiscal('f7cf', period)

        f7cl = foyer_fiscal('f7cl', period)
        f7cm = foyer_fiscal('f7cm', period)

        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cx = foyer_fiscal('f7cx', period)

        f7cy = foyer_fiscal('f7cy', period)
        f7dy = foyer_fiscal('f7dy', period)
        f7ey = foyer_fiscal('f7ey', period)
        f7fy = foyer_fiscal('f7fy', period)
        f7gy = foyer_fiscal('f7gy', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        plafond_PME = P.seuil * (maries_ou_pacses + 1)
        plafond_TPE = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement PME (souscription avant 2012) : imputation du plus ancien au plus récent
        base_report_cappme_2015_PME = min_(f7cl, plafond_PME)
        base_report_cappme_2016_PME = max_(0, min_(f7cm, plafond_PME - base_report_cappme_2015_PME))

        # Réduction investissement TPE (souscription à partir de 2012) : imputation du plus ancien au plus récent
        base_report_cappme_2015_TPE = min_(f7cq, plafond_TPE - base_report_cappme_2015_PME - base_report_cappme_2016_PME)
        base_report_cappme_2016_TPE = max_(0, min_(f7cr, plafond_TPE - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2015_TPE))
        base_report_cappme_2017_TPE = max_(0, min_(f7cv, plafond_TPE - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2015_TPE - base_report_cappme_2016_TPE))
        base_report_cappme_2018_TPE = max_(0, min_(f7cx, plafond_TPE - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2015_TPE - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE))

        # Réduction investissements de l'année courante
        base_cappme_2019 = max_(0, min_(f7cf, plafond_TPE - base_report_cappme_2015_PME - base_report_cappme_2016_PME - base_report_cappme_2015_TPE - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE - base_report_cappme_2018_TPE))

        reports_plaf_general = f7cy + f7dy + f7ey + f7fy + f7gy

        return (
            reports_plaf_general
            + P.taux18 * (base_cappme_2019
                + base_report_cappme_2015_PME
                + base_report_cappme_2016_PME
                + base_report_cappme_2015_TPE
                + base_report_cappme_2016_TPE
                + base_report_cappme_2017_TPE
                + base_report_cappme_2018_TPE)
            )

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2020
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7cf = foyer_fiscal('f7cf', period)
        f7ch = foyer_fiscal('f7ch', period)
        f7gw = foyer_fiscal('f7gw', period)

        f7cl = foyer_fiscal('f7cl', period)

        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cx = foyer_fiscal('f7cx', period)

        f7cy = foyer_fiscal('f7cy', period)
        f7dy = foyer_fiscal('f7dy', period)
        f7ey = foyer_fiscal('f7ey', period)
        f7fy = foyer_fiscal('f7fy', period)
        f7gy = foyer_fiscal('f7gy', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        plafond_PME = P.seuil * (maries_ou_pacses + 1)
        plafond_TPE = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement PME (souscription avant 2012) : imputation du plus ancien au plus récent
        base_report_cappme_2016_PME = min_(f7cl, plafond_PME)

        # Réduction investissement TPE (souscription à partir de 2012) : imputation du plus ancien au plus récent,
        # en prenant en compte les versement avant 2012 qui seront pris en compte pour le seuil
        base_report_cappme_2016_TPE = min_(f7cq, plafond_TPE - base_report_cappme_2016_PME)
        base_report_cappme_2017_TPE = max_(0, min_(f7cr, plafond_TPE - base_report_cappme_2016_PME - base_report_cappme_2016_TPE))
        base_report_cappme_2018_TPE = max_(0, min_(f7cv, plafond_TPE - base_report_cappme_2016_PME - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE))
        base_report_cappme_2019_TPE = max_(0, min_(f7cx, plafond_TPE - base_report_cappme_2016_PME - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE - base_report_cappme_2018_TPE))

        # Réduction investissements de l'année courante
        # on applique les investissements en commençant avec les plus anciennes
        base_cappme_2020_avant0908 = max_(0, min_(f7cf, plafond_TPE - base_report_cappme_2016_PME - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE - base_report_cappme_2018_TPE - base_report_cappme_2019_TPE))
        base_cappme_2020_apres0908 = max_(0, min_(f7ch, plafond_TPE - base_report_cappme_2016_PME - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE - base_report_cappme_2018_TPE - base_report_cappme_2019_TPE - base_cappme_2020_avant0908))
        base_sfs_2020 = max_(0, min_(f7gw, plafond_TPE - plafond_TPE - base_report_cappme_2016_PME - base_report_cappme_2016_TPE - base_report_cappme_2017_TPE - base_report_cappme_2018_TPE - base_report_cappme_2019_TPE - base_cappme_2020_avant0908 - base_cappme_2020_apres0908))

        reports_plaf_general = f7cy + f7dy + f7ey + f7fy + f7gy

        return (
            reports_plaf_general
            + P.taux18 * (base_report_cappme_2016_PME
                + base_report_cappme_2016_TPE
                + base_report_cappme_2017_TPE
                + base_report_cappme_2018_TPE
                + base_report_cappme_2019_TPE
                + base_cappme_2020_avant0908)
            + P.taux25 * (base_cappme_2020_apres0908
                + base_sfs_2020)
            )

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des PME
        2021
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7cf = foyer_fiscal('f7cf', period)
        f7ch = foyer_fiscal('f7ch', period)

        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cx = foyer_fiscal('f7cx', period)
        f7cs = foyer_fiscal('f7cs', period)
        f7bs = foyer_fiscal('f7bs', period)

        f7cy = foyer_fiscal('f7cy', period)
        f7dy = foyer_fiscal('f7dy', period)
        f7ey = foyer_fiscal('f7ey', period)
        f7fy = foyer_fiscal('f7fy', period)
        f7gy = foyer_fiscal('f7gy', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        plafond_TPE = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement TPE (souscription à partir de 2012) : imputation du plus ancien au plus récent,
        # dans l'ordre PME/ESUS > SFS
        base_report_pme_2017_TPE = min_(f7cq, plafond_TPE)
        base_report_pme_2018_TPE = max_(0, min_(f7cr, plafond_TPE - base_report_pme_2017_TPE))
        base_report_pme_2019_TPE = max_(0, min_(f7cv, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE))
        base_pme_2020_avant0908 = max_(0, min_(f7cx, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE))
        base_pme_2020_apres0908 = max_(0, min_(f7cs, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908))
        base_sfs_2020 = max_(0, min_(f7bs, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908))

        # Réduction investissements de l'année courante
        # on applique les investissements en commençant avec les plus anciennes
        base_pme_esus_2021_avant0805 = max_(0, min_(f7cf, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908 - base_sfs_2020))
        base_pme_2021_apres0805 = max_(0, min_(f7ch, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908 - base_sfs_2020 - base_pme_esus_2021_avant0805))

        reports_plaf_general = f7cy + f7dy + f7ey + f7fy + f7gy

        return (
            reports_plaf_general
            + P.taux18 * (base_report_pme_2017_TPE
                + base_report_pme_2018_TPE
                + base_report_pme_2019_TPE
                + base_pme_2020_avant0908
                + base_pme_esus_2021_avant0805)
            + P.taux25 * (base_pme_2020_apres0908
                + base_sfs_2020
                + base_pme_2021_apres0805))


class cappme_esus_sfs(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt au titre des souscriptions en numéraire au capital des ESUS et SFS"
    reference = 'http://bofip.impots.gouv.fr/bofip/4374-PGP'
    definition_period = YEAR

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital des ESUS/SFS applicable au plafond special augmenté de € 3K
        2021
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7cf = foyer_fiscal('f7cf', period)
        f7ch = foyer_fiscal('f7ch', period)
        f7ci = foyer_fiscal('f7ci', period)
        f7gw = foyer_fiscal('f7gw', period)

        f7cq = foyer_fiscal('f7cq', period)
        f7cr = foyer_fiscal('f7cr', period)
        f7cv = foyer_fiscal('f7cv', period)
        f7cx = foyer_fiscal('f7cx', period)
        f7cs = foyer_fiscal('f7cs', period)
        f7bs = foyer_fiscal('f7bs', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.pme.souscription_capital

        plafond_TPE = P.seuil_tpe * (maries_ou_pacses + 1)

        # Réduction investissement TPE (souscription à partir de 2012) : imputation du plus ancien au plus récent,
        # dans l'ordre PME/ESUS > SFS
        base_report_pme_2017_TPE = min_(f7cq, plafond_TPE)
        base_report_pme_2018_TPE = max_(0, min_(f7cr, plafond_TPE - base_report_pme_2017_TPE))
        base_report_pme_2019_TPE = max_(0, min_(f7cv, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE))
        base_pme_2020_avant0908 = max_(0, min_(f7cx, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE))
        base_pme_2020_apres0908 = max_(0, min_(f7cs, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908))
        base_sfs_2020 = max_(0, min_(f7bs, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908))

        # Réduction investissements de l'année courante
        # on applique les investissements en commençant avec les plus anciennes
        base_pme_esus_2021_avant0805 = max_(0, min_(f7cf, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908 - base_sfs_2020))
        base_pme_2021_apres0805 = max_(0, min_(f7ch, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908 - base_sfs_2020 - base_pme_esus_2021_avant0805))
        base_esus_2021_apres0805 = max_(0, min_(f7ci, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908 - base_sfs_2020 - base_pme_esus_2021_avant0805 - base_pme_2021_apres0805))
        base_sfs_2021 = max_(0, min_(f7gw, plafond_TPE - base_report_pme_2017_TPE - base_report_pme_2018_TPE - base_report_pme_2019_TPE - base_pme_2020_avant0908 - base_pme_2020_apres0908 - base_sfs_2020 - base_pme_esus_2021_avant0805 - base_pme_2021_apres0805 - base_esus_2021_apres0805))

        # ESUS/SFS majoration du plafonnement des niches fiscales
        base_esus_sfs = P.taux25 * (base_esus_2021_apres0805 + base_sfs_2021)

        return base_esus_sfs


class defense_forets_contre_incendies(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'defense_forets_contre_incendies'
    definition_period = YEAR

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Défense des forêts contre l'incendie
        2006-
        '''
        f7uc = foyer_fiscal('f7uc', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.defense_forets_contre_incendies

        return P.taux * min_(f7uc, P.plafond)


class codev(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'codev'
    end = '2009-12-31'
    definition_period = YEAR
    # Avant 2009, il s'agissait d'un montant déductible : voir charges_deductibles.py

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées sur un compte épargne codéveloppement (case 7UH)
        2009
        '''
        f7uh = foyer_fiscal('f7uh_2009', period)
        rbg_int = foyer_fiscal('rbg_int', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.compte_epargne_co_developpement

        return min_(f7uh * P.taux, min_(P.plafond.plafond_en_revenu_net_global * rbg_int, P.plafond.plafond_par_personne))  # page3 ligne 18


class gardenf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt en faveur des dépenses de frais de garde des jeunes enfants"
    reference = 'http://bofip.impots.gouv.fr/bofip/865-PGP?datePubl=13/04/2013#'
    definition_period = YEAR
    end = '2004-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
        et GE, GF, GG
        2002
        '''
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        P = parameters(period).impot_revenu.credits_impots.gardenf

        max1 = P.plafond
        return P.taux * (min_(f7ga, max1) + min_(f7gb, max1) + min_(f7gc, max1))

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
        et GE, GF, GG
        2003-2004
        '''
        f7ga = foyer_fiscal('f7ga', period)
        f7gb = foyer_fiscal('f7gb', period)
        f7gc = foyer_fiscal('f7gc', period)
        f7ge = foyer_fiscal('f7ge', period)
        f7gf = foyer_fiscal('f7gf', period)
        f7gg = foyer_fiscal('f7gg', period)
        P = parameters(period).impot_revenu.credits_impots.gardenf

        max1 = P.plafond
        max2 = P.plafond / 2

        return P.taux * (
            min_(f7ga, max1)
            + min_(f7gb, max1)
            + min_(f7gc, max1)
            + min_(f7ge, max2)
            + min_(f7gf, max2)
            + min_(f7gg, max2)
            )


class interets_prets_consommation(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Intérêts prêts consommation'
    end = '2005-12-31'
    definition_period = YEAR

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Intérêts des prêts à la consommation (case UH)
        2004-2005
        '''
        f7uh = foyer_fiscal('f7uh_2004', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.interets_prets_consommation

        max1 = P.plafond
        return P.taux * min_(f7uh, max1)


class intemp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'intemp'
    end = '2003-12-31'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Intérêts d'emprunts
        2002-2003
        '''
        nb_pac = foyer_fiscal('nb_pac', period)
        f7wg = foyer_fiscal('f7wg_2003', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.intemp

        max1 = P.max + P.pac * nb_pac
        return P.taux * min_(f7wg, max1)


class ri_investissement_forestier(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Crédit d'impôt au titre des investissements forestiers"
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2002-2005
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7un = foyer_fiscal('f7un', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        seuil = P.acquisition.plafond * (maries_ou_pacses + 1)
        return P.acquisition.taux * min_(f7un, seuil)

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2006-2008
        '''
        f7un = foyer_fiscal('f7un', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        return P.acquisition.taux * f7un

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2009
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        return P.acquisition.taux * (
            min_(f7un, P.acquisition.plafond * (maries_ou_pacses + 1))
            + min_(f7up, P.travaux.plafond * (maries_ou_pacses + 1))
            + min_(f7uq, P.plafond_cga * (maries_ou_pacses + 1))
            )

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        return P.acquisition.taux * (
            min_(f7un, P.acquisition.plafond * (maries_ou_pacses + 1))
            + min_(f7up + f7uu + f7te, P.travaux.plafond * (maries_ou_pacses + 1))
            + min_(f7uq, P.plafond_cga * (maries_ou_pacses + 1))
            )

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2011 cf. 2041 GK
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        f7uv = foyer_fiscal('f7uv_2016', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        max0 = max_(0, P.travaux.plafond * (maries_ou_pacses + 1) - f7ul)
        max1 = max_(0, max0 - f7uu - f7te - f7uv - f7tf)
        return (
            P.acquisition.taux * (
                min_(f7un, P.acquisition.plafond * (maries_ou_pacses + 1))
                + min_(f7up, max1)
                + min_(f7uq, P.plafond_cga * (maries_ou_pacses + 1))
                )
            + P10.acquisition.taux * min_(f7uu + f7te + f7uv + f7tf, max0)
            + P.assurance.taux * min_(f7ul, P.travaux.plafond * (maries_ou_pacses + 1))
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2012
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        f7uv = foyer_fiscal('f7uv_2016', period)
        f7uw = foyer_fiscal('f7uw_2015', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        report_depenses_2009 = f7uu + f7te
        report_depenses_2010 = f7uv + f7tf
        report_depenses_2011 = f7uw + f7tg

        max0 = max_(0, P.travaux.plafond * (maries_ou_pacses + 1) - f7ul)
        max1 = max_(0, max0 - report_depenses_2009 - report_depenses_2010)
        max2 = max_(0, max1 - report_depenses_2011)

        return (
            P.acquisition.taux * (
                min_(f7un, P.acquisition.plafond * (maries_ou_pacses + 1))
                + min_(f7uq, P.plafond_cga * (maries_ou_pacses + 1))
                + min_(f7up, max2)
                )
            + P.assurance.taux * min_(f7ul, P.travaux.plafond * (maries_ou_pacses + 1))
            + P10.acquisition.taux * min_(report_depenses_2009 + report_depenses_2010, max0) +
            + P11.acquisition.taux * min_(report_depenses_2011, max1)
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2013
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7th = foyer_fiscal('f7th', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7un = foyer_fiscal('f7un', period)
        f7up = foyer_fiscal('f7up', period)
        f7uq = foyer_fiscal('f7uq', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        f7uv = foyer_fiscal('f7uv_2016', period)
        f7uw = foyer_fiscal('f7uw_2015', period)
        f7ux = foyer_fiscal('f7ux_2018', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P12 = parameters('2012-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        report_depenses_2009 = f7uu + f7te
        report_depenses_2010 = f7uv + f7tf
        report_depenses_2011 = f7uw + f7tg
        report_depenses_2012 = f7ux + f7th

        max0 = max_(0, P.travaux.plafond * (maries_ou_pacses + 1) - f7ul)
        max1 = max_(0, max0 - report_depenses_2009 - report_depenses_2010)
        max2 = max_(0, max1 - report_depenses_2011)
        max3 = max_(0, max2 - report_depenses_2012)

        return (
            P.acquisition.taux * (
                min_(f7un, P.acquisition.plafond * (maries_ou_pacses + 1))
                + min_(f7uq, P.plafond_cga * (maries_ou_pacses + 1))
                + min_(f7up, max3)
                )
            + P.assurance.taux * min_(f7ul, P.travaux.plafond * (maries_ou_pacses + 1))
            + P10.acquisition.taux * min_(report_depenses_2009 + report_depenses_2010, max0)
            + P11.acquisition.taux * min_(report_depenses_2011, max1)
            + P12.acquisition.taux * min_(report_depenses_2012, max2)
            )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2014
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7te = foyer_fiscal('f7te', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7uv = foyer_fiscal('f7uv_2016', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7uw = foyer_fiscal('f7uw_2015', period)
        f7th = foyer_fiscal('f7th', period)
        f7ux = foyer_fiscal('f7ux_2018', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        rep_avant_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7te + f7tf + f7uu)
        rep_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011, f7uv + f7tg)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011 - rep_2011, f7ul + f7uw + f7th + f7ux + f7ti)

        ri_ass_rep = (rep_avant_2011 * P10.acquisition.taux
            + rep_2011 * P11.acquisition.taux
            + ass_rep_2012 * P.acquisition.taux)

        return ri_acq + ri_ass_rep

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2015
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7uv = foyer_fiscal('f7uv_2016', period)
        f7th = foyer_fiscal('f7th', period)
        f7uw = foyer_fiscal('f7uw_2015', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        rep_avant_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7te + f7tf)
        rep_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011, f7uu + f7tg)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011 - rep_2011, f7ul + f7uv + f7th + f7uw + f7ti)

        ri_ass_rep = (rep_avant_2011 * P10.acquisition.taux
            + rep_2011 * P11.acquisition.taux
            + ass_rep_2012 * P.acquisition.taux)

        return ri_acq + ri_ass_rep

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2016
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        f7th = foyer_fiscal('f7th', period)
        f7uv = foyer_fiscal('f7uv_2016', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        rep_avant_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7te + f7tf)
        rep_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011, f7tg)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011 - rep_2011, f7ul + f7uu + f7th + f7uv + f7ti)

        ri_ass_rep = (rep_avant_2011 * P10.acquisition.taux
            + rep_2011 * P11.acquisition.taux
            + ass_rep_2012 * P.acquisition.taux)

        return ri_acq + ri_ass_rep

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2017
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7te = foyer_fiscal('f7te', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7th = foyer_fiscal('f7th', period)
        f7uu = foyer_fiscal('f7uu_2017', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        rep_avant_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7te + f7tf)
        rep_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011, f7tg)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011 - rep_2011, f7ul + f7uu + f7th + f7ti)

        ri_ass_rep = (rep_avant_2011 * P10.acquisition.taux
            + rep_2011 * P11.acquisition.taux
            + ass_rep_2012 * P.acquisition.taux)

        return ri_acq + ri_ass_rep

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2018
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7tf = foyer_fiscal('f7tf', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7th = foyer_fiscal('f7th', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P10 = parameters('2010-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        rep_avant_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7tf)
        rep_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011, f7tg)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_avant_2011 - rep_2011, f7ul + f7th + f7ti)

        ri_ass_rep = (rep_avant_2011 * P10.acquisition.taux
            + rep_2011 * P11.acquisition.taux
            + ass_rep_2012 * P.acquisition.taux)

        return ri_acq + ri_ass_rep

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2019
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7tg = foyer_fiscal('f7tg', period)
        f7th = foyer_fiscal('f7th', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        rep_2011 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7tg)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1) - rep_2011, f7ul + f7th + f7ti)

        ri_ass_rep = (rep_2011 * P11.acquisition.taux
            + ass_rep_2012 * P.acquisition.taux)

        return ri_acq + ri_ass_rep

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2020
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7th = foyer_fiscal('f7th', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7ul + f7th + f7ti)
        ri_ass_rep = ass_rep_2012 * P.acquisition.taux

        return ri_acq + ri_ass_rep

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements forestiers pour 2021
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)

        f7un = foyer_fiscal('f7un', period)
        f7ul = foyer_fiscal('f7ul', period)
        f7ti = foyer_fiscal('f7ti', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissement_forestier.depenses_investissement_forestier

        # acquisition
        ri_acq = min_(P.acquisition.plafond * (maries_ou_pacses + 1), f7un)

        # assurance + reports des travaux (même plafond)
        ass_rep_2012 = min_(P.assurance.plafond * (maries_ou_pacses + 1), f7ul + f7ti)
        ri_ass_rep = ass_rep_2012 * P.acquisition.taux

        return ri_acq + ri_ass_rep


class invlst(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt en faveur des investissements dans le secteur touristique"
    reference = 'http://bofip.impots.gouv.fr/bofip/6265-PGP'
    definition_period = YEAR

    def formula_2004_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2004
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xc = foyer_fiscal('f7xc_2012', period)
        f7xd = foyer_fiscal('f7xd', period)
        f7xe = foyer_fiscal('f7xe', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh_2012', period)
        f7xi = foyer_fiscal('f7xi_2015', period)
        f7xj = foyer_fiscal('f7xj_2015', period)
        f7xk = foyer_fiscal('f7xk_2014', period)
        f7xl = foyer_fiscal('f7xl_2012', period)
        f7xm = foyer_fiscal('f7xm_2013', period)
        f7xn = foyer_fiscal('f7xn_2017', period)
        f7xo = foyer_fiscal('f7xo_2013', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)
        seuil3 = P.seuil3 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 4)
        xd = P.taux_xd * f7xd
        xe = P.taux_xe * min_(f7xe, seuil1 / 6)
        xf = P.taux_xf * f7xf
        xg = P.taux_xg * min_(f7xg, seuil2)
        xh = P.taux_xh * min_(f7xh, seuil3)
        xi = P.taux_xi * min_(f7xi, seuil1 / 4)
        xj = P.taux_xj * f7xj
        xk = P.taux_xk * f7xk
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xm = P.taux_xm * f7xm
        xn = P.taux_xn * min_(f7xn, seuil1 / 6)
        xo = P.taux_xo * f7xo

        return around(xc + xd + xe + xf + xg + xh + xi + xj + xk + xl + xm + xn + xo)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2005-2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xc = foyer_fiscal('f7xc_2012', period)
        f7xd = foyer_fiscal('f7xd', period)
        f7xe = foyer_fiscal('f7xe', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh_2012', period)
        f7xi = foyer_fiscal('f7xi_2015', period)
        f7xj = foyer_fiscal('f7xj_2015', period)
        f7xk = foyer_fiscal('f7xk_2014', period)
        f7xl = foyer_fiscal('f7xl_2012', period)
        f7xm = foyer_fiscal('f7xm_2013', period)
        f7xn = foyer_fiscal('f7xn_2017', period)
        f7xo = foyer_fiscal('f7xo_2013', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 6)
        xd = P.taux_xd * f7xd
        xe = P.taux_xe * min_(f7xe, seuil1 / 6)
        xf = P.taux_xf * f7xf
        xg = P.taux_xg * min_(f7xg, seuil2)
        xh = P.taux_xh * min_(f7xh, seuil2 - f7xg)
        xi = P.taux_xi * f7xi
        xj = P.taux_xj * f7xj
        xk = P.taux_xk * f7xk
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xm = P.taux_xm * f7xm
        xn = P.taux_xn * min_(f7xn, seuil1 / 6)
        xo = P.taux_xo * f7xo

        return around(xc + xd + xe + xf + xg + xh + xi + xj + xk + xl + xm + xn + xo)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xa = foyer_fiscal('f7xa_2012', period)
        f7xb = foyer_fiscal('f7xb_2012', period)
        f7xc = foyer_fiscal('f7xc_2012', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh_2012', period)
        f7xi = foyer_fiscal('f7xi_2015', period)
        f7xj = foyer_fiscal('f7xj_2015', period)
        f7xk = foyer_fiscal('f7xk_2014', period)
        f7xl = foyer_fiscal('f7xl_2012', period)
        f7xm = foyer_fiscal('f7xm_2013', period)
        f7xo = foyer_fiscal('f7xo_2013', period)
        f7xp = foyer_fiscal('f7xp_2016', period)
        f7xq = foyer_fiscal('f7xq_2016', period)
        f7xr = foyer_fiscal('f7xr', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 6)
        xa = P.taux_xa * min_(f7xa, seuil2)
        xg = P.taux_xg * min_(f7xg, seuil2 - f7xa)
        xb = P.taux_xb * min_(f7xb, seuil2 - f7xa - f7xg)
        xh = P.taux_xh * min_(f7xh, seuil2 - f7xa - f7xg - f7xb)
        xi = P.taux_xi * (f7xf + f7xi + f7xp)
        xj = P.taux_xj * (f7xm + f7xj + f7xq)
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xo = P.taux_xo * (f7xk + f7xo + f7xr)

        return around(xc + xa + xg + xb + xh + xi + xj + xl + xo)

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2012
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7xa = foyer_fiscal('f7xa_2012', period)
        f7xb = foyer_fiscal('f7xb_2012', period)
        f7xc = foyer_fiscal('f7xc_2012', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xg = foyer_fiscal('f7xg', period)
        f7xh = foyer_fiscal('f7xh_2012', period)
        f7xi = foyer_fiscal('f7xi_2015', period)
        f7xj = foyer_fiscal('f7xj_2015', period)
        f7xk = foyer_fiscal('f7xk_2014', period)
        f7xl = foyer_fiscal('f7xl_2012', period)
        f7xm = foyer_fiscal('f7xm_2013', period)
        f7xn = foyer_fiscal('f7xn_2017', period)
        f7xo = foyer_fiscal('f7xo_2013', period)
        f7xp = foyer_fiscal('f7xp_2016', period)
        f7xq = foyer_fiscal('f7xq_2016', period)
        f7xr = foyer_fiscal('f7xr', period)
        f7xv = foyer_fiscal('f7xv', period)
        f7xx = foyer_fiscal('f7xx_2012', period)
        f7xz = foyer_fiscal('f7xz', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        seuil1 = P.seuil1 * (1 + maries_ou_pacses)
        seuil2 = P.seuil2 * (1 + maries_ou_pacses)

        xc = P.taux_xc * min_(f7xc, seuil1 / 6)
        xa = P.taux_xa * min_(f7xa, seuil2)
        xg = P.taux_xg * min_(f7xg, seuil2 - f7xa)
        xx = P.taux_xx * min_(f7xx, seuil2 - f7xa - f7xg)
        xb = P.taux_xb * min_(f7xb, seuil2 - f7xa - f7xg - f7xx)
        xh = P.taux_xh * min_(f7xh, seuil2 - f7xa - f7xg - f7xb - f7xx)
        xz = P.taux_xz * min_(f7xz, seuil2 - f7xa - f7xg - f7xb - f7xx - f7xh)
        xi = P.taux_xi * (f7xf + f7xi + f7xp + f7xn)
        xj = P.taux_xj * (f7xm + f7xj + f7xq + f7xv)
        xl = P.taux_xl * min_(f7xl, seuil1 / 6)
        xo = P.taux_xo * (f7xk + f7xo + f7xr)

        return around(xc + xa + xg + xx + xb + xz + xh + xi + xj + xl + xo)

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2013
        '''
        f7uy = foyer_fiscal('f7uy', period)
        f7uz = foyer_fiscal('f7uz', period)
        f7xf = foyer_fiscal('f7xf', period)
        f7xi = foyer_fiscal('f7xi_2015', period)
        f7xj = foyer_fiscal('f7xj_2015', period)
        f7xk = foyer_fiscal('f7xk_2014', period)
        f7xm = foyer_fiscal('f7xm_2013', period)
        f7xn = foyer_fiscal('f7xn_2017', period)
        f7xo = foyer_fiscal('f7xo_2013', period)
        f7xp = foyer_fiscal('f7xp_2016', period)
        f7xq = foyer_fiscal('f7xq_2016', period)
        f7xr = foyer_fiscal('f7xr', period)
        f7xv = foyer_fiscal('f7xv', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        xi = P.taux_xi * (f7xf + f7xi + f7xp + f7xn + f7uy)
        xj = P.taux_xj * (f7xm + f7xj + f7xq + f7xv + f7uz)
        xo = P.taux_xo * (f7xk + f7xo + f7xr)

        return around(xi + xj + xo)

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2014
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)  # noqa F841
        report_logement_neuf_2009 = foyer_fiscal('f7xi_2015', period)
        report_logement_neuf_2010 = foyer_fiscal('f7xp_2016', period)
        report_logement_neuf_2011 = foyer_fiscal('f7xn_2017', period)
        report_logement_neuf_2012 = foyer_fiscal('f7uy', period)
        report_rehabilitation_2009 = foyer_fiscal('f7xj_2015', period)
        report_rehabilitation_2010 = foyer_fiscal('f7xq_2016', period)
        report_rehabilitation_2011 = foyer_fiscal('f7xv', period)
        report_rehabilitation_2012 = foyer_fiscal('f7uz', period)
        report_residence_sociale_2009 = foyer_fiscal('f7xk_2014', period)
        report_residence_sociale_2010 = foyer_fiscal('f7xr', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        red_neuf = min_(P.seuil1 * (1 + maries_ou_pacses), report_logement_neuf_2009 + report_logement_neuf_2010 + report_logement_neuf_2011 + report_logement_neuf_2012)
        red_rehab = min_(P.seuil1 * (1 + maries_ou_pacses) - red_neuf, report_rehabilitation_2009 + report_rehabilitation_2010 + report_rehabilitation_2011 + report_rehabilitation_2012)

        reduction_logement_neuf = P.taux_xi * red_neuf
        reduction_rehabilitation = P.taux_xj * red_rehab

        reduction_residence_sociale = P.taux_xo * min_(P.seuil1, report_residence_sociale_2009 + report_residence_sociale_2010)

        return around(max_(reduction_logement_neuf + reduction_rehabilitation, reduction_residence_sociale))

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique OU DANS UNE RÉSIDENCE HÔTELIÈRE À VOCATION SOCIALE
        mais pas les deux à la fois
        2015
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)  # noqa F841
        report_logement_neuf_2009 = foyer_fiscal('f7xi_2015', period)
        report_logement_neuf_2010 = foyer_fiscal('f7xp_2016', period)
        report_logement_neuf_2011 = foyer_fiscal('f7xn_2017', period)
        report_logement_neuf_2012 = foyer_fiscal('f7uy', period)
        report_rehabilitation_2009 = foyer_fiscal('f7xj_2015', period)
        report_rehabilitation_2010 = foyer_fiscal('f7xq_2016', period)
        report_rehabilitation_2011 = foyer_fiscal('f7xv', period)
        report_rehabilitation_2012 = foyer_fiscal('f7uz', period)
        report_residence_sociale_2010 = foyer_fiscal('f7xr', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        red_neuf = min_(P.seuil1 * (1 + maries_ou_pacses), report_logement_neuf_2009 + report_logement_neuf_2010 + report_logement_neuf_2011 + report_logement_neuf_2012)
        red_rehab = min_(P.seuil1 * (1 + maries_ou_pacses) - red_neuf, report_rehabilitation_2009 + report_rehabilitation_2010 + report_rehabilitation_2011 + report_rehabilitation_2012)

        reduction_logement_neuf = P.taux_xi * red_neuf
        reduction_rehabilitation = P.taux_xj * red_rehab

        reduction_residence_sociale = P.taux_xo * min_(P.seuil1, report_residence_sociale_2010)

        return around(max_(reduction_logement_neuf + reduction_rehabilitation, reduction_residence_sociale))

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2016
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)  # noqa F841
        report_logement_neuf_2010 = foyer_fiscal('f7xp_2016', period)
        report_logement_neuf_2011 = foyer_fiscal('f7xn_2017', period)
        report_logement_neuf_2012 = foyer_fiscal('f7uy', period)
        report_rehabilitation_2010 = foyer_fiscal('f7xq_2016', period)
        report_rehabilitation_2011 = foyer_fiscal('f7xv', period)
        report_rehabilitation_2012 = foyer_fiscal('f7uz', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        red_neuf = min_(P.seuil1 * (1 + maries_ou_pacses), report_logement_neuf_2010 + report_logement_neuf_2011 + report_logement_neuf_2012)
        red_rehab = min_(P.seuil1 * (1 + maries_ou_pacses) - red_neuf, report_rehabilitation_2010 + report_rehabilitation_2011 + report_rehabilitation_2012)

        reduction_logement_neuf = P.taux_xi * red_neuf
        reduction_rehabilitation = P.taux_xj * red_rehab

        return around(reduction_logement_neuf + reduction_rehabilitation)

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2017
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)  # noqa F841
        report_logement_neuf_2011 = foyer_fiscal('f7xn_2017', period)
        report_logement_neuf_2012 = foyer_fiscal('f7uy', period)
        report_rehabilitation_2011 = foyer_fiscal('f7xv', period)
        report_rehabilitation_2012 = foyer_fiscal('f7uz', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        red_neuf = min_(P.seuil1 * (1 + maries_ou_pacses), report_logement_neuf_2011 + report_logement_neuf_2012)
        red_rehab = min_(P.seuil1 * (1 + maries_ou_pacses) - red_neuf, report_rehabilitation_2011 + report_rehabilitation_2012)

        reduction_logement_neuf = P.taux_xi * red_neuf
        reduction_rehabilitation = P.taux_xj * red_rehab

        return around(reduction_logement_neuf + reduction_rehabilitation)

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans le secteur touristique
        2018
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)  # noqa F841
        report_logement_neuf_2012 = foyer_fiscal('f7uy', period)
        report_rehabilitation_2012 = foyer_fiscal('f7uz', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invlst

        red_neuf = min_(P.seuil1 * (1 + maries_ou_pacses), report_logement_neuf_2012)
        red_rehab = min_(P.seuil1 * (1 + maries_ou_pacses) - red_neuf, report_rehabilitation_2012)

        reduction_logement_neuf = P.taux_xi * red_neuf
        reduction_rehabilitation = P.taux_xj * red_rehab

        return around(reduction_logement_neuf + reduction_rehabilitation)

    # TODO : verrifier la formule de cette réduction pour les années 2004-2013, les cases changent de signification d'une année à l'autre, cela ne semble pas pris en compte dans le calcul (ex: f7xd)


class invrev(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt en faveur des investissements dans les résidences de tourisme"
    reference = 'http://bofip.impots.gouv.fr/bofip/6266-PGP'
    end = '2003-12-31'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatifs dans les résidences de tourisme situées dans une zone de
        revitalisation rurale (cases GS, GT, XG, GU et GV)
        2002-2003
        TODO 1/4 codé en dur
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gs = foyer_fiscal('f7gs_2003', period)
        f7gt = foyer_fiscal('f7gt_2003', period)
        f7xg = foyer_fiscal('f7xg_2002', period)
        f7gu = foyer_fiscal('f7gu_2003', period)
        f7gv = foyer_fiscal('f7gv_2003', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.invrev

        return (
            P.taux_gs * min_(f7gs, P.seuil_gs * (1 + maries_ou_pacses)) / 4
            + P.taux_gu * min_(f7gu, P.seuil_gu * (1 + maries_ou_pacses)) / 4
            + P.taux_xg * min_(f7xg, P.seuil_xg * (1 + maries_ou_pacses)) / 4
            + P.taux_gt * f7gt + P.taux_gt * f7gv
            )


class location_meublee(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt en faveur de l'acquisition de logements destinés à la location meublée non professionnelle - Dispositif Censi-Bouvard"
    reference = 'http://bofip.impots.gouv.fr/bofip/4885-PGP'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2009
        '''
        f7ij = foyer_fiscal('f7ij', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        return P.taux * min_(P.plafond, f7ij) / 9

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2010
        '''
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7is = foyer_fiscal('f7is_2015', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        return ((min_(P.plafond, max_(f7ij, f7il)) + min_(P.plafond, f7im)) / 9 + f7ik) * P.taux + f7is

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2011
        '''
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io_2015', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7is = foyer_fiscal('f7is_2015', period)
        f7it = foyer_fiscal('f7it_2016', period)
        f7iu = foyer_fiscal('f7iu_2016', period)
        f7iv = foyer_fiscal('f7iv_2016', period)
        f7iw = foyer_fiscal('f7iw_2016', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        majoration_taux_invest_2011 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        taux_reduc_2009_2010 = P.taux
        taux_reduc_2011 = P.taux20 * majoration_taux_invest_2011 + P.taux18 * not_(majoration_taux_invest_2011)
        report = P.taux * max_(f7ik, f7ip + f7ir + f7iq) + f7is + f7iu + f7it

        return (
            (
                (min_(P.plafond, max_(f7im, f7iw)) + min_(P.plafond, f7io)) * taux_reduc_2009_2010
                + min_(P.plafond, maxi(f7ij, f7il, f7in, f7iv)) * taux_reduc_2011
                ) / 9
            + report
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2012
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7id = foyer_fiscal('f7id', period)
        f7ie = foyer_fiscal('f7ie_2016', period)
        f7if = foyer_fiscal('f7if_2016', period)
        f7ig = foyer_fiscal('f7ig_2016', period)
        f7ih = foyer_fiscal('f7ih_2017', period)
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io_2015', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7is = foyer_fiscal('f7is_2015', period)
        f7it = foyer_fiscal('f7it_2016', period)
        f7iu = foyer_fiscal('f7iu_2016', period)
        f7iv = foyer_fiscal('f7iv_2016', period)
        f7iw = foyer_fiscal('f7iw_2016', period)
        f7ix = foyer_fiscal('f7ix_2017', period)
        f7iz = foyer_fiscal('f7iz_2017', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        majoration_taux_invest_2011 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        majoration_taux_invest_2012 = (maxi(f7id, f7ie, f7if, f7ig) == max_(f7ie, f7if))
        taux_reduc_2009_2010 = P.taux
        taux_reduc_2011 = P.taux20 * majoration_taux_invest_2011 + P.taux18 * not_(majoration_taux_invest_2011)
        taux_reduc_2012 = P.taux18 * majoration_taux_invest_2012 + P.taux11 * not_(majoration_taux_invest_2012)
        report = P.taux * max_(f7ik + f7ip, f7ir + f7iq) + f7ia + f7ib + f7ic + f7ih + f7is + f7iu + f7it + f7ix + f7iz

        return (
            (
                (min_(P.plafond, max_(f7im, f7iw)) + min_(P.plafond, f7io)) * taux_reduc_2009_2010
                + min_(P.plafond, maxi(f7ij, f7il, f7in, f7iv)) * taux_reduc_2011
                + min_(P.plafond, maxi(f7id, f7ie, f7if, f7ig)) * taux_reduc_2012
                ) / 9
            + report
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2013
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7id = foyer_fiscal('f7id', period)
        f7ie = foyer_fiscal('f7ie_2016', period)
        f7if = foyer_fiscal('f7if_2016', period)
        f7ig = foyer_fiscal('f7ig_2016', period)
        f7ih = foyer_fiscal('f7ih_2017', period)
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io_2015', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7is = foyer_fiscal('f7is_2015', period)
        f7it = foyer_fiscal('f7it_2016', period)
        f7iu = foyer_fiscal('f7iu_2016', period)
        f7iv = foyer_fiscal('f7iv_2016', period)
        f7iw = foyer_fiscal('f7iw_2016', period)
        f7ix = foyer_fiscal('f7ix_2017', period)
        f7iy = foyer_fiscal('f7iy_2018', period)
        f7iz = foyer_fiscal('f7iz_2017', period)
        f7jc = foyer_fiscal('f7jc_2018', period)
        f7ji = foyer_fiscal('f7ji_2018', period)
        f7js = foyer_fiscal('f7js_2018', period)
        f7jt = foyer_fiscal('f7jt_2019', period)
        f7ju = foyer_fiscal('f7ju_2016', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        majoration_taux_invest_2011 = (maxi(f7ij, f7il, f7in, f7iv) == max_(f7il, f7in))
        majoration_taux_invest_2012 = (maxi(f7id, f7ie, f7if, f7ig) == max_(f7ie, f7if))
        taux_reduc_2009_2010 = P.taux
        taux_reduc_2011 = P.taux20 * majoration_taux_invest_2011 + P.taux18 * not_(majoration_taux_invest_2011)
        taux_reduc_2012 = P.taux18 * majoration_taux_invest_2012 + P.taux11 * not_(majoration_taux_invest_2012)
        taux_reduc_2013 = P.taux11

        report = (
            P.taux * max_(f7ik + f7ip, f7ir + f7iq)
            + f7ia + f7ib + f7ic + f7ih + f7is + f7iu + f7it + f7ix + f7iy + f7iz
            + f7jv + f7jw + f7jx + f7jy + f7jc + f7ji + f7js
            )

        return (
            (
                (min_(P.plafond, max_(f7im, f7iw)) + min_(P.plafond, f7io)) * taux_reduc_2009_2010
                + min_(P.plafond, maxi(f7ij, f7il, f7in, f7iv)) * taux_reduc_2011
                + min_(P.plafond, maxi(f7id, f7ie, f7if, f7ig)) * taux_reduc_2012
                + min_(P.plafond, f7jt + f7ju) * taux_reduc_2013
                ) / 9
            + report
            )

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2014
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7id = foyer_fiscal('f7id', period)
        f7ie = foyer_fiscal('f7ie_2016', period)
        f7if = foyer_fiscal('f7if_2016', period)
        f7ig = foyer_fiscal('f7ig_2016', period)
        f7ih = foyer_fiscal('f7ih_2017', period)
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io_2015', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7is = foyer_fiscal('f7is_2015', period)
        f7it = foyer_fiscal('f7it_2016', period)
        f7iu = foyer_fiscal('f7iu_2016', period)
        f7iv = foyer_fiscal('f7iv_2016', period)
        f7iw = foyer_fiscal('f7iw_2016', period)
        f7ix = foyer_fiscal('f7ix_2017', period)
        f7iy = foyer_fiscal('f7iy_2018', period)
        f7iz = foyer_fiscal('f7iz_2017', period)
        f7jc = foyer_fiscal('f7jc_2018', period)
        f7ji = foyer_fiscal('f7ji_2018', period)
        f7js = foyer_fiscal('f7js_2018', period)
        f7jt = foyer_fiscal('f7jt_2019', period)
        f7ju = foyer_fiscal('f7ju_2016', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7od = foyer_fiscal('f7od', period)
        f7oe = foyer_fiscal('f7oe', period)
        f7ou = foyer_fiscal('f7ou', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pc = foyer_fiscal('f7pc_2019', period)
        f7pd = foyer_fiscal('f7pd_2019', period)
        f7pe = foyer_fiscal('f7pe_2019', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        reduction_investissements_acheve_2014_realise_2009 = P.taux * min_(P.plafond, f7io)
        reduction_investissements_acheve_2014_realise_2010 = P.taux * min_(P.plafond, f7im + f7iw)
        reduction_investissements_acheve_2014_realise_2011 = P.taux20 * min_(P.plafond, f7il + f7in) + P.taux18 * min_(max_(0, P.plafond - f7il - f7in), f7ij + f7iv)
        reduction_investissements_acheve_2014_realise_2012 = P.taux18 * min_(P.plafond, f7ie + f7if) + P.taux11 * min_(max_(0, P.plafond - f7ie - f7if), f7id + f7ig)
        reduction_investissements_acheve_2014_realise_2013 = P.taux11 * min_(P.plafond, f7jt + f7ju)
        reduction_investissements_acheve_2014_realise_2014 = P.taux11 * min_(P.plafond, f7ou)

        report_invest_anterieur = (
            P.taux * min_(P.plafond, f7ik)
            + P.taux * min_(P.plafond, f7ip + f7ir + f7iq)
            + f7ia + f7ib + f7ic
            + f7jv + f7jw + f7jx + f7jy
            + f7oa + f7ob + f7oc + f7od + f7oe
            )

        report_non_impute = (
            f7is + f7iu + f7ix + f7iy + f7pa
            + f7it + f7ih + f7jc + f7pb
            + f7iz + f7ji + f7pc
            + f7js + f7pd
            + f7pe
            )

        return (
            (
                around(reduction_investissements_acheve_2014_realise_2009 / 9)
                + around(reduction_investissements_acheve_2014_realise_2010 / 9)
                + around(reduction_investissements_acheve_2014_realise_2011 / 9)
                + around(reduction_investissements_acheve_2014_realise_2012 / 9)
                + around(reduction_investissements_acheve_2014_realise_2013 / 9)
                + around(reduction_investissements_acheve_2014_realise_2014 / 9)
                )
            + report_invest_anterieur
            + report_non_impute
            )

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2015
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7id = foyer_fiscal('f7id', period)
        f7ie = foyer_fiscal('f7ie_2016', period)
        f7if = foyer_fiscal('f7if_2016', period)
        f7ig = foyer_fiscal('f7ig_2016', period)
        f7ih = foyer_fiscal('f7ih_2017', period)
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7io = foyer_fiscal('f7io_2015', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7is = foyer_fiscal('f7is_2015', period)
        f7it = foyer_fiscal('f7it_2016', period)
        f7iu = foyer_fiscal('f7iu_2016', period)
        f7iv = foyer_fiscal('f7iv_2016', period)
        f7iw = foyer_fiscal('f7iw_2016', period)
        f7ix = foyer_fiscal('f7ix_2017', period)
        f7iy = foyer_fiscal('f7iy_2018', period)
        f7iz = foyer_fiscal('f7iz_2017', period)
        f7jc = foyer_fiscal('f7jc_2018', period)
        f7ji = foyer_fiscal('f7ji_2018', period)
        f7js = foyer_fiscal('f7js_2018', period)
        f7jt = foyer_fiscal('f7jt_2019', period)
        f7ju = foyer_fiscal('f7ju_2016', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7od = foyer_fiscal('f7od', period)
        f7oe = foyer_fiscal('f7oe', period)
        f7of = foyer_fiscal('f7of', period)
        f7og = foyer_fiscal('f7og', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ou = foyer_fiscal('f7ou', period)
        f7ov = foyer_fiscal('f7ov', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pc = foyer_fiscal('f7pc_2019', period)
        f7pd = foyer_fiscal('f7pd_2019', period)
        f7pe = foyer_fiscal('f7pe_2019', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7pg = foyer_fiscal('f7pg', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        reduction_investissements_acheve_2015_realise_2009 = P.taux * min_(P.plafond, f7io)
        reduction_investissements_acheve_2015_realise_2010 = P.taux * min_(P.plafond, f7im + f7iw)
        reduction_investissements_acheve_2015_realise_2011 = P.taux20 * min_(P.plafond, f7il + f7in) + P.taux18 * min_(max_(0, P.plafond - f7il - f7in), f7ij + f7iv)
        reduction_investissements_acheve_2015_realise_2012 = P.taux18 * min_(P.plafond, f7ie + f7if) + P.taux11 * min_(max_(0, P.plafond - f7ie - f7if), f7id + f7ig)
        reduction_investissements_acheve_2015_realise_2013 = P.taux11 * min_(P.plafond, f7jt + f7ju)
        reduction_investissements_acheve_2015_realise_2014 = P.taux11 * min_(P.plafond, f7ou)
        reduction_investissements_acheve_2015_realise_2015 = P.taux11 * min_(P.plafond, f7ov)

        report_invest_anterieur = (
            P.taux * min_(P.plafond, f7ik)
            + P.taux * min_(P.plafond, f7ip + f7ir + f7iq)
            + f7ia + f7ib + f7ic
            + f7jv + f7jw + f7jx + f7jy
            + f7oa + f7ob + f7oc + f7od + f7oe
            + f7of + f7og + f7oh + f7oi + f7oj
            )

        report_non_impute = (
            f7is + f7iu + f7ix + f7iy + f7pa + f7pf
            + f7it + f7ih + f7jc + f7pb + f7pg
            + f7iz + f7ji + f7pc + f7ph
            + f7js + f7pd + f7pi
            + f7pe + f7pj
            )

        return (
            (
                around(reduction_investissements_acheve_2015_realise_2009 / 9)
                + around(reduction_investissements_acheve_2015_realise_2010 / 9)
                + around(reduction_investissements_acheve_2015_realise_2011 / 9)
                + around(reduction_investissements_acheve_2015_realise_2012 / 9)
                + around(reduction_investissements_acheve_2015_realise_2013 / 9)
                + around(reduction_investissements_acheve_2015_realise_2014 / 9)
                + around(reduction_investissements_acheve_2015_realise_2015 / 9)
                )
            + report_invest_anterieur
            + report_non_impute
            )

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2016
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7id = foyer_fiscal('f7id', period)
        f7ie = foyer_fiscal('f7ie_2016', period)
        f7if = foyer_fiscal('f7if_2016', period)
        f7ig = foyer_fiscal('f7ig_2016', period)
        f7ih = foyer_fiscal('f7ih_2017', period)
        f7ij = foyer_fiscal('f7ij', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7im = foyer_fiscal('f7im', period)
        f7in = foyer_fiscal('f7in', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7it = foyer_fiscal('f7it_2016', period)
        f7iu = foyer_fiscal('f7iu_2016', period)
        f7iv = foyer_fiscal('f7iv_2016', period)
        f7iw = foyer_fiscal('f7iw_2016', period)
        f7ix = foyer_fiscal('f7ix_2017', period)
        f7iy = foyer_fiscal('f7iy_2018', period)
        f7iz = foyer_fiscal('f7iz_2017', period)
        f7jc = foyer_fiscal('f7jc_2018', period)
        f7ji = foyer_fiscal('f7ji_2018', period)
        f7js = foyer_fiscal('f7js_2018', period)
        f7jt = foyer_fiscal('f7jt_2019', period)
        f7ju = foyer_fiscal('f7ju_2016', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7od = foyer_fiscal('f7od', period)
        f7oe = foyer_fiscal('f7oe', period)
        f7of = foyer_fiscal('f7of', period)
        f7og = foyer_fiscal('f7og', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ok = foyer_fiscal('f7ok', period)
        f7ol = foyer_fiscal('f7ol', period)
        f7om = foyer_fiscal('f7om', period)
        f7on = foyer_fiscal('f7on', period)
        f7oo = foyer_fiscal('f7oo', period)
        f7ou = foyer_fiscal('f7ou', period)
        f7ov = foyer_fiscal('f7ov', period)
        f7ow = foyer_fiscal('f7ow', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pc = foyer_fiscal('f7pc_2019', period)
        f7pd = foyer_fiscal('f7pd_2019', period)
        f7pe = foyer_fiscal('f7pe_2019', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7pg = foyer_fiscal('f7pg', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)
        f7pk = foyer_fiscal('f7pk', period)
        f7pl = foyer_fiscal('f7pl', period)
        f7pm = foyer_fiscal('f7pm', period)
        f7pn = foyer_fiscal('f7pn', period)
        f7po = foyer_fiscal('f7po', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        reduction_investissements_acheve_2016_realise_2010 = P.taux * min_(P.plafond, f7im + f7iw)
        reduction_investissements_acheve_2016_realise_2011 = P.taux20 * min_(P.plafond, f7il + f7in) + P.taux18 * min_(max_(0, P.plafond - f7il - f7in), f7ij + f7iv)
        reduction_investissements_acheve_2016_realise_2012 = P.taux18 * min_(P.plafond, f7ie + f7if) + P.taux11 * min_(max_(0, P.plafond - f7ie - f7if), f7id + f7ig)
        reduction_investissements_acheve_2016_realise_2013 = P.taux11 * min_(P.plafond, f7jt + f7ju)
        reduction_investissements_acheve_2016_realise_2014 = P.taux11 * min_(P.plafond, f7ou)
        reduction_investissements_acheve_2016_realise_2015 = P.taux11 * min_(P.plafond, f7ov)
        reduction_investissements_acheve_2016_realise_2016 = P.taux11 * min_(P.plafond, f7ow)

        report_invest_anterieur = (
            P.taux * min_(P.plafond, f7ik)
            + P.taux * min_(P.plafond, f7ip + f7ir + f7iq)
            + f7ia + f7ib + f7ic
            + f7jv + f7jw + f7jx + f7jy
            + f7oa + f7ob + f7oc + f7od + f7oe
            + f7of + f7og + f7oh + f7oi + f7oj
            + f7ok + f7ol + f7om + f7on + f7oo
            )

        report_non_impute = (
            f7iu + f7ix + f7iy + f7pa + f7pf + f7pk
            + f7it + f7ih + f7jc + f7pb + f7pg + f7pl
            + f7iz + f7ji + f7pc + f7ph + f7pm
            + f7js + f7pd + f7pi + f7pn
            + f7pe + f7pj + f7po
            )

        return (
            (
                around(reduction_investissements_acheve_2016_realise_2010 / 9)
                + around(reduction_investissements_acheve_2016_realise_2011 / 9)
                + around(reduction_investissements_acheve_2016_realise_2012 / 9)
                + around(reduction_investissements_acheve_2016_realise_2013 / 9)
                + around(reduction_investissements_acheve_2016_realise_2014 / 9)
                + around(reduction_investissements_acheve_2016_realise_2015 / 9)
                + around(reduction_investissements_acheve_2016_realise_2016 / 9)
                )
            + report_invest_anterieur
            + report_non_impute
            )

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2017
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7ih = foyer_fiscal('f7ih_2017', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7ix = foyer_fiscal('f7ix_2017', period)
        f7iy = foyer_fiscal('f7iy_2018', period)
        f7iz = foyer_fiscal('f7iz_2017', period)
        f7jc = foyer_fiscal('f7jc_2018', period)
        f7ji = foyer_fiscal('f7ji_2018', period)
        f7js = foyer_fiscal('f7js_2018', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7od = foyer_fiscal('f7od', period)
        f7oe = foyer_fiscal('f7oe', period)
        f7of = foyer_fiscal('f7of', period)
        f7og = foyer_fiscal('f7og', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ok = foyer_fiscal('f7ok', period)
        f7ol = foyer_fiscal('f7ol', period)
        f7om = foyer_fiscal('f7om', period)
        f7on = foyer_fiscal('f7on', period)
        f7oo = foyer_fiscal('f7oo', period)
        f7op = foyer_fiscal('f7op', period)
        f7oq = foyer_fiscal('f7oq', period)
        f7or = foyer_fiscal('f7or', period)
        f7os = foyer_fiscal('f7os', period)
        f7ot = foyer_fiscal('f7ot', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pc = foyer_fiscal('f7pc_2019', period)
        f7pd = foyer_fiscal('f7pd_2019', period)
        f7pe = foyer_fiscal('f7pe_2019', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7pg = foyer_fiscal('f7pg', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)
        f7pk = foyer_fiscal('f7pk', period)
        f7pl = foyer_fiscal('f7pl', period)
        f7pm = foyer_fiscal('f7pm', period)
        f7pn = foyer_fiscal('f7pn', period)
        f7po = foyer_fiscal('f7po', period)
        f7pp = foyer_fiscal('f7pp', period)
        f7pq = foyer_fiscal('f7pq', period)
        f7pr = foyer_fiscal('f7pr', period)
        f7ps = foyer_fiscal('f7ps', period)
        f7pt = foyer_fiscal('f7pt', period)
        invest_2011_acheves_2017 = foyer_fiscal('f7ij', period)
        invest_2012_acheves_2017 = foyer_fiscal('f7id', period)
        invest_2013_acheves_2017 = foyer_fiscal('f7jt_2019', period)
        invest_2014_acheves_2017 = foyer_fiscal('f7ou', period)
        invest_2015_acheves_2017 = foyer_fiscal('f7ov', period)
        invest_2016_acheves_2017 = foyer_fiscal('f7ow', period)
        invest_2017_acheves_2017 = foyer_fiscal('f7ox', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        # Calcul de la réduction sur investissements antérieurs non imputés (si dépassement du plafond de la base)

        report_reduc_invest_2009 = P.taux * min_(P.plafond, f7ik)  # avant 2011, report de l'investissement et non de la réduction
        report_reduc_invest_2010 = P.taux * min_(P.plafond, f7ip + f7ir + f7iq)  # avant 2011, report de l'investissement et non de la réduction
        report_reduc_invest_2011 = f7ia + f7ib + f7ic
        report_reduc_invest_2012 = f7jv + f7jw + f7jx + f7jy
        report_reduc_invest_2013 = f7oa + f7ob + f7oc + f7od + f7oe
        report_reduc_invest_2014 = f7of + f7og + f7oh + f7oi + f7oj
        report_reduc_invest_2015 = f7ok + f7ol + f7om + f7on + f7oo
        report_reduc_invest_2016 = f7op + f7oq + f7or + f7os + f7ot

        report_reduc_invest_anterieur = (
            report_reduc_invest_2009
            + report_reduc_invest_2010
            + report_reduc_invest_2011
            + report_reduc_invest_2012
            + report_reduc_invest_2013
            + report_reduc_invest_2014
            + report_reduc_invest_2015
            + report_reduc_invest_2016
            )

        # Calcul de la réduction antérieure non imputée (si réduction excède l'impôt dû de l'année)

        report_reduc_2011 = f7ix + f7ih + f7iz
        report_reduc_2012 = f7iy + f7jc + f7ji + f7js
        report_reduc_2013 = f7pa + f7pb + f7pc + f7pd + f7pe
        report_reduc_2014 = f7pf + f7pg + f7ph + f7pi + f7pj
        report_reduc_2015 = f7pk + f7pl + f7pm + f7pn + f7po
        report_reduc_2016 = f7pp + f7pq + f7pr + f7ps + f7pt

        report_reduc_non_impute = (
            report_reduc_2011
            + report_reduc_2012
            + report_reduc_2013
            + report_reduc_2014
            + report_reduc_2015
            + report_reduc_2016
            )

        # Calcul de la réduction concernant les investissements achevés ou réalisés l'année courante

        reduc_invest_acheves_2017 = (
            around(P.taux18 * min_(P.plafond, invest_2011_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2012_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2013_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2014_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2015_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2016_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2017_acheves_2017) / 9)
            )

        return (
            reduc_invest_acheves_2017
            + report_reduc_invest_anterieur
            + report_reduc_non_impute
            )

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2018
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7ip = foyer_fiscal('f7ip_2018', period)
        f7iq = foyer_fiscal('f7iq_2018', period)
        f7ir = foyer_fiscal('f7ir_2018', period)
        f7iy = foyer_fiscal('f7iy_2018', period)
        f7jc = foyer_fiscal('f7jc_2018', period)
        f7ji = foyer_fiscal('f7ji_2018', period)
        f7js = foyer_fiscal('f7js_2018', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7od = foyer_fiscal('f7od', period)
        f7oe = foyer_fiscal('f7oe', period)
        f7of = foyer_fiscal('f7of', period)
        f7og = foyer_fiscal('f7og', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ok = foyer_fiscal('f7ok', period)
        f7ol = foyer_fiscal('f7ol', period)
        f7om = foyer_fiscal('f7om', period)
        f7on = foyer_fiscal('f7on', period)
        f7oo = foyer_fiscal('f7oo', period)
        f7op = foyer_fiscal('f7op', period)
        f7oq = foyer_fiscal('f7oq', period)
        f7or = foyer_fiscal('f7or', period)
        f7os = foyer_fiscal('f7os', period)
        f7ot = foyer_fiscal('f7ot', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pc = foyer_fiscal('f7pc_2019', period)
        f7pd = foyer_fiscal('f7pd_2019', period)
        f7pe = foyer_fiscal('f7pe_2019', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7pg = foyer_fiscal('f7pg', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)
        f7pk = foyer_fiscal('f7pk', period)
        f7pl = foyer_fiscal('f7pl', period)
        f7pm = foyer_fiscal('f7pm', period)
        f7pn = foyer_fiscal('f7pn', period)
        f7po = foyer_fiscal('f7po', period)
        f7pp = foyer_fiscal('f7pp', period)
        f7pq = foyer_fiscal('f7pq', period)
        f7pr = foyer_fiscal('f7pr', period)
        f7ps = foyer_fiscal('f7ps', period)
        f7pt = foyer_fiscal('f7pt', period)
        f7pu = foyer_fiscal('f7pu', period)
        f7pv = foyer_fiscal('f7pv', period)
        f7pw = foyer_fiscal('f7pw', period)
        f7px = foyer_fiscal('f7px', period)
        f7py = foyer_fiscal('f7py', period)
        f7sa = foyer_fiscal('f7sa', period)
        f7sb = foyer_fiscal('f7sb', period)
        f7sc = foyer_fiscal('f7sc', period)
        invest_2012_acheves_2017 = foyer_fiscal('f7id', period)
        invest_2013_acheves_2017 = foyer_fiscal('f7jt_2019', period)
        invest_2014_acheves_2017 = foyer_fiscal('f7ou', period)
        invest_2015_acheves_2017 = foyer_fiscal('f7ov', period)
        invest_2016_acheves_2017 = foyer_fiscal('f7ow', period)
        invest_2017_acheves_2017 = foyer_fiscal('f7ox', period)
        invest_2018_acheves_2018 = foyer_fiscal('f7oy', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        # Calcul de la réduction sur investissements antérieurs non imputés (si dépassement du plafond de la base)

        report_reduc_invest_2010 = P.taux * min_(P.plafond, f7ip + f7ir + f7iq)  # avant 2011, report de l'investissement et non de la réduction
        report_reduc_invest_2011 = f7ia + f7ib + f7ic
        report_reduc_invest_2012 = f7jv + f7jw + f7jx + f7jy
        report_reduc_invest_2013 = f7oa + f7ob + f7oc + f7od + f7oe
        report_reduc_invest_2014 = f7of + f7og + f7oh + f7oi + f7oj
        report_reduc_invest_2015 = f7ok + f7ol + f7om + f7on + f7oo
        report_reduc_invest_2016 = f7op + f7oq + f7or + f7os + f7ot
        report_reduc_invest_2017 = f7sa + f7sb + f7sc

        report_reduc_invest_anterieur = (
            report_reduc_invest_2010
            + report_reduc_invest_2011
            + report_reduc_invest_2012
            + report_reduc_invest_2013
            + report_reduc_invest_2014
            + report_reduc_invest_2015
            + report_reduc_invest_2016
            + report_reduc_invest_2017
            )

        # Calcul de la réduction antérieure non imputée (si réduction excède l'impôt dû de l'année)

        report_reduc_2012 = f7iy + f7jc + f7ji + f7js
        report_reduc_2013 = f7pa + f7pb + f7pc + f7pd + f7pe
        report_reduc_2014 = f7pf + f7pg + f7ph + f7pi + f7pj
        report_reduc_2015 = f7pk + f7pl + f7pm + f7pn + f7po
        report_reduc_2016 = f7pp + f7pq + f7pr + f7ps + f7pt
        report_reduc_2017 = f7pu + f7pv + f7pw + f7px + f7py

        report_reduc_non_impute = (
            report_reduc_2012
            + report_reduc_2013
            + report_reduc_2014
            + report_reduc_2015
            + report_reduc_2016
            + report_reduc_2017
            )

        # Calcul de la réduction concernant les investissements achevés ou réalisés l'année courante

        reduc_invest_acheves_2018 = (
            around(P.taux11 * min_(P.plafond, invest_2012_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2013_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2014_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2015_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2016_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2017_acheves_2017) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2018_acheves_2018) / 9)
            )

        return (
            reduc_invest_acheves_2018
            + report_reduc_invest_anterieur
            + report_reduc_non_impute
            )

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2019
        '''
        f7ia = foyer_fiscal('f7ia_2019', period)
        f7ib = foyer_fiscal('f7ib_2019', period)
        f7ic = foyer_fiscal('f7ic_2019', period)
        f7jv = foyer_fiscal('f7jv', period)
        f7jw = foyer_fiscal('f7jw', period)
        f7jx = foyer_fiscal('f7jx', period)
        f7jy = foyer_fiscal('f7jy', period)
        f7oa = foyer_fiscal('f7oa', period)
        f7ob = foyer_fiscal('f7ob', period)
        f7oc = foyer_fiscal('f7oc', period)
        f7od = foyer_fiscal('f7od', period)
        f7oe = foyer_fiscal('f7oe', period)
        f7of = foyer_fiscal('f7of', period)
        f7og = foyer_fiscal('f7og', period)
        f7oh = foyer_fiscal('f7oh', period)
        f7oi = foyer_fiscal('f7oi', period)
        f7oj = foyer_fiscal('f7oj', period)
        f7ok = foyer_fiscal('f7ok', period)
        f7ol = foyer_fiscal('f7ol', period)
        f7om = foyer_fiscal('f7om', period)
        f7on = foyer_fiscal('f7on', period)
        f7oo = foyer_fiscal('f7oo', period)
        f7op = foyer_fiscal('f7op', period)
        f7oq = foyer_fiscal('f7oq', period)
        f7or = foyer_fiscal('f7or', period)
        f7os = foyer_fiscal('f7os', period)
        f7ot = foyer_fiscal('f7ot', period)
        f7pa = foyer_fiscal('f7pa', period)
        f7pb = foyer_fiscal('f7pb', period)
        f7pc = foyer_fiscal('f7pc_2019', period)
        f7pd = foyer_fiscal('f7pd_2019', period)
        f7pe = foyer_fiscal('f7pe_2019', period)
        f7pf = foyer_fiscal('f7pf', period)
        f7pg = foyer_fiscal('f7pg', period)
        f7ph = foyer_fiscal('f7ph', period)
        f7pi = foyer_fiscal('f7pi', period)
        f7pj = foyer_fiscal('f7pj', period)
        f7pk = foyer_fiscal('f7pk', period)
        f7pl = foyer_fiscal('f7pl', period)
        f7pm = foyer_fiscal('f7pm', period)
        f7pn = foyer_fiscal('f7pn', period)
        f7po = foyer_fiscal('f7po', period)
        f7pp = foyer_fiscal('f7pp', period)
        f7pq = foyer_fiscal('f7pq', period)
        f7pr = foyer_fiscal('f7pr', period)
        f7ps = foyer_fiscal('f7ps', period)
        f7pt = foyer_fiscal('f7pt', period)
        f7ho = foyer_fiscal('f7ho', period)
        f7hp = foyer_fiscal('f7hp', period)
        f7hq = foyer_fiscal('f7hq', period)
        f7hr = foyer_fiscal('f7hr', period)
        f7hs = foyer_fiscal('f7hs', period)
        f7pu = foyer_fiscal('f7pu', period)
        f7pv = foyer_fiscal('f7pv', period)
        f7pw = foyer_fiscal('f7pw', period)
        f7px = foyer_fiscal('f7px', period)
        f7py = foyer_fiscal('f7py', period)
        f7sa = foyer_fiscal('f7sa', period)
        f7sb = foyer_fiscal('f7sb', period)
        f7sc = foyer_fiscal('f7sc', period)
        f7so = foyer_fiscal('f7so', period)
        f7sn = foyer_fiscal('f7sn', period)
        invest_2013_acheves_2019 = foyer_fiscal('f7jt_2019', period)
        invest_2014_acheves_2019 = foyer_fiscal('f7ou', period)
        invest_2015_acheves_2019 = foyer_fiscal('f7ov', period)
        invest_2016_acheves_2019 = foyer_fiscal('f7ow', period)
        invest_2017_acheves_2019 = foyer_fiscal('f7ox', period)
        invest_2018_acheves_2019 = foyer_fiscal('f7oz', period)
        invest_2019_acheves_2019 = foyer_fiscal('f7pz', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        # Calcul de la réduction sur investissements antérieurs non imputés (si dépassement du plafond de la base)

        report_reduc_invest_2011 = f7ia + f7ib + f7ic
        report_reduc_invest_2012 = f7jv + f7jw + f7jx + f7jy
        report_reduc_invest_2013 = f7oa + f7ob + f7oc + f7od + f7oe
        report_reduc_invest_2014 = f7of + f7og + f7oh + f7oi + f7oj
        report_reduc_invest_2015 = f7ok + f7ol + f7om + f7on + f7oo
        report_reduc_invest_2016 = f7op + f7oq + f7or + f7os + f7ot
        report_reduc_invest_2017 = f7sa + f7sb + f7sc
        report_reduc_invest_2018 = f7so + f7sn

        report_reduc_invest_anterieur = (
            report_reduc_invest_2011
            + report_reduc_invest_2012
            + report_reduc_invest_2013
            + report_reduc_invest_2014
            + report_reduc_invest_2015
            + report_reduc_invest_2016
            + report_reduc_invest_2017
            + report_reduc_invest_2018
            )

        # Calcul de la réduction antérieure non imputée (si réduction excède l'impôt dû de l'année)

        report_reduc_2013 = f7pa + f7pb + f7pc + f7pd + f7pe
        report_reduc_2014 = f7pf + f7pg + f7ph + f7pi + f7pj
        report_reduc_2015 = f7pk + f7pl + f7pm + f7pn + f7po
        report_reduc_2016 = f7pp + f7pq + f7pr + f7ps + f7pt
        report_reduc_2017 = f7pu + f7pv + f7pw + f7px + f7py
        report_reduc_2018 = f7ho + f7hp + f7hq + f7hr + f7hs

        report_reduc_non_impute = (
            report_reduc_2013
            + report_reduc_2014
            + report_reduc_2015
            + report_reduc_2016
            + report_reduc_2017
            + report_reduc_2018
            )

        # Calcul de la réduction concernant les investissements achevés ou réalisés l'année courante

        reduc_invest_acheves_2019 = (
            around(P.taux11 * min_(P.plafond, invest_2013_acheves_2019) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2014_acheves_2019) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2015_acheves_2019) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2016_acheves_2019) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2017_acheves_2019) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2018_acheves_2019) / 9)
            + around(P.taux11 * min_(P.plafond, invest_2019_acheves_2019) / 9)
            )

        return (
            reduc_invest_acheves_2019
            + report_reduc_invest_anterieur
            + report_reduc_non_impute
            )

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2020
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        inv = ['f7ou',
            'f7ov',
            'f7ow',
            'f7ox',
            'f7oy',
            'f7pz',
            'f7mz']

        rep = ['f7sp', 'f7sn', 'f7so', 'f7sa',
            'f7sb', 'f7sc', 'f7oa', 'f7ob',
            'f7oc', 'f7od', 'f7oe', 'f7of',
            'f7og', 'f7oh', 'f7oi', 'f7oj',
            'f7ok', 'f7ol', 'f7om', 'f7on',
            'f7oo', 'f7op', 'f7oq', 'f7or',
            'f7os', 'f7ot', 'f7jv', 'f7jw',
            'f7jx', 'f7jy', 'f7pf', 'f7pg',
            'f7ph', 'f7pi', 'f7pj', 'f7pk',
            'f7pl', 'f7pm', 'f7pn', 'f7po',
            'f7pp', 'f7pq', 'f7pr', 'f7ps',
            'f7pt', 'f7pu', 'f7pv', 'f7pw',
            'f7px', 'f7py', 'f7ho', 'f7hp',
            'f7hq', 'f7hr', 'f7hs', 'f7ht',
            'f7hu', 'f7hv', 'f7hw', 'f7hx']

        rep_ri = sum([foyer_fiscal(r, period) for r in rep])
        inv_ri = sum([(P.taux11 * min_(P.plafond, foyer_fiscal(r, period)) / 9) for r in inv])

        return rep_ri + inv_ri

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
        2021
        '''
        P = parameters(period).impot_revenu.calcul_reductions_impots.location_meublee

        inv = ['f7ov',
            'f7ow',
            'f7ox',
            'f7oy',
            'f7pz',
            'f7mz',
            'f7mw']

        rep = ['f7sm', 'f7sp', 'f7sn', 'f7so', 'f7sa',
            'f7sb', 'f7sc', 'f7oa', 'f7ob',
            'f7oc', 'f7od', 'f7oe', 'f7of',
            'f7og', 'f7oh', 'f7oi', 'f7oj',
            'f7ok', 'f7ol', 'f7om', 'f7on',
            'f7oo', 'f7op', 'f7oq', 'f7or',
            'f7os', 'f7ot', 'f7jv', 'f7jw',
            'f7jx', 'f7jy', 'f7pf', 'f7pg',
            'f7ph', 'f7pi', 'f7pj', 'f7pk',
            'f7pl', 'f7pm', 'f7pn', 'f7po',
            'f7pp', 'f7pq', 'f7pr', 'f7ps',
            'f7pt', 'f7pu', 'f7pv', 'f7pw',
            'f7px', 'f7py', 'f7ho', 'f7hp',
            'f7hq', 'f7hr', 'f7hs', 'f7ht',
            'f7hu', 'f7hv', 'f7hw', 'f7hx']

        rep_ri = sum([foyer_fiscal(r, period) for r in rep])
        inv_ri = sum([(P.taux11 * min_(P.plafond, foyer_fiscal(r, period)) / 9) for r in inv])

        return rep_ri + inv_ri


class mohist(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'mohist'
    definition_period = YEAR

    def formula_2008_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de conservation et de restauration d’objets classés monuments historiques (case NZ)
        2008-
        '''
        f7nz = foyer_fiscal('f7nz', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.restauration_monuments_historiques

        return P.taux * min_(f7nz, P.plafond)


class protection_patrimoine_naturel(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt en faveur des dépenses de préservation du patrimoine naturel"
    reference = 'http://bofip.impots.gouv.fr/bofip/6240-PGP'
    definition_period = YEAR
    end = '2019-12-31'

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA)
        2010
        '''
        f7ka = foyer_fiscal('f7ka_2013', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.protection_patrimoine_naturel

        max1 = P.plafond
        return P.taux * min_(f7ka, max1)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB)
        2011
        '''
        f7ka = foyer_fiscal('f7ka_2013', period)
        f7kb = foyer_fiscal('f7kb_2016', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.protection_patrimoine_naturel

        max1 = P.plafond
        return P.taux * min_(f7ka, max1) + f7kb

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB, 7KC)
        2012
        '''
        f7ka = foyer_fiscal('f7ka_2013', period)
        f7kb = foyer_fiscal('f7kb_2016', period)
        f7kc = foyer_fiscal('f7kc_2017', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.protection_patrimoine_naturel

        max1 = P.plafond
        return P.taux * min_(f7ka, max1) + f7kb + f7kc

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KA, 7KB, 7KC)
        2013
        '''
        f7ka = foyer_fiscal('f7ka_2013', period)
        f7kb = foyer_fiscal('f7kb_2016', period)
        f7kc = foyer_fiscal('f7kc_2017', period)
        f7kd = foyer_fiscal('f7kd_2018', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.protection_patrimoine_naturel

        max1 = P.plafond
        return P.taux * min_(f7ka, max1) + f7kb + f7kc + f7kd

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KB, 7KC, 7KD, 7KE)
        2014-2016
        '''
        f7kb = foyer_fiscal('f7kb_2016', period)
        f7kc = foyer_fiscal('f7kc_2017', period)
        f7kd = foyer_fiscal('f7kd_2018', period)
        f7ke = foyer_fiscal('f7ke', period)

        return f7kb + f7kc + f7kd + f7ke

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KC, 7KD, 7KE)
        2017
        '''
        f7kc = foyer_fiscal('f7kc_2017', period)
        f7kd = foyer_fiscal('f7kd_2018', period)
        f7ke = foyer_fiscal('f7ke', period)

        return f7kc + f7kd + f7ke

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KD, 7KE)
        2018
        '''
        f7kd = foyer_fiscal('f7kd_2018', period)
        f7ke = foyer_fiscal('f7ke', period)

        return f7kd + f7ke

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Dépenses de protections du patrimoine naturel (case 7KE)
        2019
        '''
        f7ke = foyer_fiscal('f7ke', period)

        return f7ke


class reduction_impot_exceptionnelle(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt exceptionnelle"
    end = '2013-12-31'
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        nb_adult = foyer_fiscal('nb_adult', period)
        nbptr = foyer_fiscal('nbptr', period)
        rfr = foyer_fiscal('rfr', period)
        params = parameters(period).impot_revenu.calcul_reductions_impots.reduction_impot_exceptionnelle
        plafond = params.seuil * nb_adult + (nbptr - nb_adult) * 2 * params.majoration_seuil
        montant = params.montant_plafond * nb_adult
        return min_(max_(plafond + montant - rfr, 0), montant)


class rehab(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt pour travaux de réhabilitation des résidences de tourisme"
    reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000033781921&cidTexte=LEGITEXT000006069577&categorieLien=id&dateTexte=20170101'
    definition_period = YEAR

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Travaux de réhabilitation des résidences de tourisme
        (2017 -)
        '''
        f7xx = foyer_fiscal('f7xx', period)  # TO DO: Coder le plafond glissant sur 3 années

        P = parameters(period).impot_revenu.calcul_reductions_impots.divers.rehabilitation_residences_touristiques
        depenses_2017 = min_(P.plafond, f7xx)

        return (P.taux * depenses_2017)


class ri_saldom(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt au titre des sommes versées pour l'emploi d'un salarié à domicile"
    reference = 'http://bofip.impots.gouv.fr/bofip/3968-PGP.html?identifiant=BOI-IR-RICI-150-20-20150515#'
    definition_period = YEAR
    end = '2016-12-31'

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à domicile
        2002-2004
        '''
        f7df = foyer_fiscal('f7df', period)
        invalide = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        plafond = P.plafond * not_(invalide) + P.plafond_invalides * invalide
        return P.taux * min_(f7df, plafond)

    def formula_2005_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à domicile
        2005-2006
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7df = foyer_fiscal('f7df', period)
        f7dl = foyer_fiscal('f7dl', period)
        invalide = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        nbpacmin = nb_pac_majoration_plafond + f7dl
        max_base = P.plafond
        max_du_max_non_inv = P.plafond_maximum
        max_non_inv = min_(max_base + P.increment_plafond * nbpacmin, max_du_max_non_inv)
        plafond = max_non_inv * not_(invalide) + P.plafond_invalides * invalide
        return P.taux * min_(f7df, plafond)

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à domicile (à partir de 2007, 7DB donne droit à un crédit et 7DF à une réduction)
        2007-2008
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7df = foyer_fiscal('f7df', period)
        f7dl = foyer_fiscal('f7dl', period)
        invalide = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        nbpacmin = nb_pac_majoration_plafond + f7dl
        max_base = P.plafond
        max_du_max_non_inv = P.plafond_maximum
        max_non_inv = min_(max_base + P.increment_plafond * nbpacmin, max_du_max_non_inv)
        max_effectif = max_non_inv * not_(invalide) + P.plafond_invalides * invalide
        plafond = max_effectif - min_(f7db, max_effectif)
        return P.taux * min_(f7df, plafond)

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salarié à domicile
        2009-2011
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)
        f7db = foyer_fiscal('f7db', period)
        f7df = foyer_fiscal('f7df', period)
        f7dl = foyer_fiscal('f7dl', period)
        annee1 = foyer_fiscal('f7dq', period)
        invalide = foyer_fiscal('f7dg', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        nbpacmin = nb_pac_majoration_plafond + f7dl
        max_base = P.plafond * not_(annee1) + P.plafond_1ere_annee * annee1
        max_du_max_non_inv = P.plafond_maximum * not_(annee1) + P.plafond_invalides_1ere_annee * annee1
        max_non_inv = min_(max_base + P.increment_plafond * nbpacmin, max_du_max_non_inv)
        max_non_inv2 = min_(max_base + P.increment_plafond * nb_pac_majoration_plafond, max_du_max_non_inv)
        max_effectif = max_non_inv * not_(invalide) + P.plafond_invalides * invalide
        max_effectif2 = max_non_inv2 * not_(invalide) + P.plafond_invalides * invalide
        plafond = max_effectif - min_(f7db, max_effectif2)
        return P.taux * min_(f7df, plafond)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Sommes versées pour l'emploi d'un salariés à domicile
        2011 - 2016
        NB: Normalement, le plafond est aussi augmenté pour chaque personne
        agée de plus de 65 ans dans le foyer (en plus des PACs et des
        ascendants de 65 ans remplissant les conditions de l'APA). On ne
        prend pas en compte le nombre de ces individus ici.
        '''
        nb_pac_majoration_plafond = foyer_fiscal('nb_pac2', period)

        f7db = foyer_fiscal('f7db', period)
        f7dd = foyer_fiscal('f7dd', period)
        f7df = foyer_fiscal('f7df', period)
        f7dl = foyer_fiscal('f7dl', period)

        annee1 = foyer_fiscal('f7dq', period)
        invalide = foyer_fiscal('f7dg', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.emploi_salarie_domicile

        # détérminer le plafond

        if invalide.any():
            plaf = P.plafond_invalides
        else:
            if annee1.any():
                plaf = min_(P.plafond_invalides_1ere_annee, P.plafond_1ere_annee + P.increment_plafond * (nb_pac_majoration_plafond + f7dl))
            else:
                plaf = min_(P.plafond_maximum, P.plafond + P.increment_plafond * (nb_pac_majoration_plafond + f7dl))

        # calcul de la RI et du CI

        base_ci = min_(plaf, f7db)
        base_ri = min_(plaf - base_ci, f7df + f7dd)

        ri = base_ri * P.taux

        return ri


class scelli(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Réduction d'impôt au titre des investissements locatifs - Dispositif Scellier"
    reference = 'http://bofip.impots.gouv.fr/bofip/4951-PGP'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier (cases 7HJ et 7HK)
        2009
        '''
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        return max_(P.taux25 * min_(P.max, f7hj), P.taux40 * min_(P.max, f7hk)) / 9

    def formula_2010_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2010
        '''
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho_2016', period)
        f7hl = foyer_fiscal('f7hl_2010', period)
        f7hm = foyer_fiscal('f7hm_2010', period)
        f7hr = foyer_fiscal('f7hr_2017', period)
        f7hs = foyer_fiscal('f7hs_2017', period)
        f7la = foyer_fiscal('f7la', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        return (
            max_(
                max_(P.taux25 * min_(P.max, f7hj), P.taux40 * min_(P.max, f7hk)),
                max_(P.taux25 * min_(P.max, f7hn), P.taux40 * min_(P.max, f7ho))
                ) / 9
            + max_(
                P.taux25 * min_(P.max, f7hl),
                P.taux40 * min_(P.max, f7hm)
                ) / 9
            + max_(P.taux25 * f7hr, P.taux40 * f7hs)
            + f7la)

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2011
        '''
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl_2010', period)
        f7hm = foyer_fiscal('f7hm_2010', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho_2016', period)
        f7hr = foyer_fiscal('f7hr_2017', period)
        f7hs = foyer_fiscal('f7hs_2017', period)
        f7ht = foyer_fiscal('f7ht_2018', period)
        f7hu = foyer_fiscal('f7hu_2018', period)
        f7hv = foyer_fiscal('f7hv_2018', period)
        f7hw = foyer_fiscal('f7hw_2018', period)
        f7hx = foyer_fiscal('f7hx_2018', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7la = foyer_fiscal('f7la', period)
        f7lb = foyer_fiscal('f7lb', period)
        f7lc = foyer_fiscal('f7lc', period)
        f7na = foyer_fiscal('f7na_2017', period)
        f7nb = foyer_fiscal('f7nb_2016', period)
        f7nc = foyer_fiscal('f7nc_2017', period)
        f7nd = foyer_fiscal('f7nd_2017', period)
        f7ne = foyer_fiscal('f7ne_2017', period)
        f7nf = foyer_fiscal('f7nf_2017', period)
        f7ng = foyer_fiscal('f7ng_2016', period)
        f7nh = foyer_fiscal('f7nh_2017', period)
        f7ni = foyer_fiscal('f7ni_2017', period)
        f7nj = foyer_fiscal('f7nj_2017', period)
        f7nk = foyer_fiscal('f7nk_2017', period)
        f7nl = foyer_fiscal('f7nl_2016', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        return (
            min_(P.max, maxi(
                P.taux13 * max_(f7nf, f7nj) / 9,
                P.taux15 * max_(f7ng, f7ni) / 9,
                P.taux22 * max_(f7na, f7ne) / 9,
                P.taux25 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
                P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
                P.taux40 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5)
                ))
            + min_(P.max, maxi(P.taux25 * max_(f7hj, f7hn), P.taux40 * max_(f7hk, f7ho))) / 9
            + min_(P.max, max_(P.taux25 * f7hl, P.taux40 * f7hm)) / 9
            + min_(P.max, maxi(P.taux25 * f7hv, P.taux25 * f7hx, P.taux40 * f7hw, P.taux40 * f7hz))
            + min_(P.max, max_(P.taux25 * f7ht, P.taux40 * f7hu))
            + min_(P.max, max_(P.taux25 * f7hr, P.taux40 * f7hs))
            + f7la + f7lb + f7lc
            )

    def formula_2012_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2012
        '''
        f7ha = foyer_fiscal('f7ha', period)
        f7hb = foyer_fiscal('f7hb', period)
        f7hg = foyer_fiscal('f7hg', period)
        f7hh = foyer_fiscal('f7hh', period)
        f7hd = foyer_fiscal('f7hd', period)
        f7he = foyer_fiscal('f7he', period)
        f7hf = foyer_fiscal('f7hf', period)
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl_2010', period)
        f7hm = foyer_fiscal('f7hm_2010', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho_2016', period)
        f7hr = foyer_fiscal('f7hr_2017', period)
        f7hs = foyer_fiscal('f7hs_2017', period)
        f7ht = foyer_fiscal('f7ht_2018', period)
        f7hu = foyer_fiscal('f7hu_2018', period)
        f7hv = foyer_fiscal('f7hv_2018', period)
        f7hw = foyer_fiscal('f7hw_2018', period)
        f7hx = foyer_fiscal('f7hx_2018', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7ja = foyer_fiscal('f7ja_2017', period)
        f7jb = foyer_fiscal('f7jb_2016', period)
        f7jd = foyer_fiscal('f7jd_2017', period)
        f7je = foyer_fiscal('f7je', period)
        f7jf = foyer_fiscal('f7jf', period)
        f7jg = foyer_fiscal('f7jg', period)
        f7jh = foyer_fiscal('f7jh', period)
        f7jj = foyer_fiscal('f7jj', period)
        f7jk = foyer_fiscal('f7jk', period)
        f7jl = foyer_fiscal('f7jl', period)
        f7jm = foyer_fiscal('f7jm_2017', period)
        f7jn = foyer_fiscal('f7jn_2017', period)
        f7jo = foyer_fiscal('f7jo_2017', period)
        f7jp = foyer_fiscal('f7jp_2016', period)
        f7jq = foyer_fiscal('f7jq_2017', period)
        f7jr = foyer_fiscal('f7jr_2017', period)
        f7la = foyer_fiscal('f7la', period)
        f7lb = foyer_fiscal('f7lb', period)
        f7lc = foyer_fiscal('f7lc', period)
        f7ld = foyer_fiscal('f7ld', period)
        f7le = foyer_fiscal('f7le', period)
        f7lf = foyer_fiscal('f7lf', period)
        f7na = foyer_fiscal('f7na_2017', period)
        f7nb = foyer_fiscal('f7nb_2016', period)
        f7nc = foyer_fiscal('f7nc_2017', period)
        f7nd = foyer_fiscal('f7nd_2017', period)
        f7ne = foyer_fiscal('f7ne_2017', period)
        f7nf = foyer_fiscal('f7nf_2017', period)
        f7ng = foyer_fiscal('f7ng_2016', period)
        f7nh = foyer_fiscal('f7nh_2017', period)
        f7ni = foyer_fiscal('f7ni_2017', period)
        f7nj = foyer_fiscal('f7nj_2017', period)
        f7nk = foyer_fiscal('f7nk_2017', period)
        f7nl = foyer_fiscal('f7nl_2016', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        return (
            min_(P.max, maxi(
                P.taux13 * max_(f7nf, f7nj) / 9,
                P.taux15 * max_(f7ng, f7ni) / 9,
                P.taux22 * max_(f7na, f7ne) / 9,
                P.taux25 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
                P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
                P.taux40 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5)
                ))
            + min_(P.max, maxi(P.taux25 * max_(f7hj, f7hn), P.taux40 * max_(f7hk, f7ho))) / 9
            + min_(P.max, max_(P.taux25 * f7hl, P.taux40 * f7hm)) / 9
            + min_(P.max, maxi(P.taux25 * f7hv, P.taux25 * f7hx, P.taux40 * f7hw, P.taux40 * f7hz))
            + min_(P.max, max_(P.taux25 * f7ht, P.taux40 * f7hu))
            + min_(P.max, max_(P.taux25 * f7hr, P.taux40 * f7hs))
            + f7la + f7lb + f7lc + f7ld + f7le + f7lf
            + f7ha + f7hb + f7hg + f7hh + f7hd + f7he + f7hf
            + min_(P.max, maxi(
                P09.taux_prorogation * max_(f7jf, f7jj) / 9,
                P.taux13 * maxi(f7ja, f7je, f7jg, f7jh) / 9,
                P.taux22 * maxi(f7jb, f7jd) / 9,
                P.taux24 * maxi(f7jk / 9, f7jn / 9, f7jo / 5, f7jr / 5),
                P.taux36 * maxi(f7jl / 9, f7jm / 9, f7jp / 5, f7jq / 5)
                ))
            )

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2013
        '''
        f7fa = foyer_fiscal('f7fa', period)
        f7fb = foyer_fiscal('f7fb', period)
        f7fc = foyer_fiscal('f7fc', period)
        f7fd = foyer_fiscal('f7fd', period)
        f7gj = foyer_fiscal('f7gj', period)
        f7gk = foyer_fiscal('f7gk', period)
        f7gl = foyer_fiscal('f7gl', period)
        f7gp = foyer_fiscal('f7gp', period)
        f7gs = foyer_fiscal('f7gs', period)
        f7gt = foyer_fiscal('f7gt', period)
        f7gu = foyer_fiscal('f7gu', period)
        f7gv = foyer_fiscal('f7gv', period)
        f7gw = foyer_fiscal('f7gw_2016', period)
        f7gx = foyer_fiscal('f7gx', period)
        f7ha = foyer_fiscal('f7ha', period)
        f7hb = foyer_fiscal('f7hb', period)
        f7hg = foyer_fiscal('f7hg', period)
        f7hh = foyer_fiscal('f7hh', period)
        f7hd = foyer_fiscal('f7hd', period)
        f7he = foyer_fiscal('f7he', period)
        f7hf = foyer_fiscal('f7hf', period)
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl_2010', period)
        f7hm = foyer_fiscal('f7hm_2010', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho_2016', period)
        f7hr = foyer_fiscal('f7hr_2017', period)
        f7hs = foyer_fiscal('f7hs_2017', period)
        f7ht = foyer_fiscal('f7ht_2018', period)
        f7hu = foyer_fiscal('f7hu_2018', period)
        f7hv = foyer_fiscal('f7hv_2018', period)
        f7hw = foyer_fiscal('f7hw_2018', period)
        f7hx = foyer_fiscal('f7hx_2018', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7ja = foyer_fiscal('f7ja_2017', period)
        f7jb = foyer_fiscal('f7jb_2016', period)
        f7jd = foyer_fiscal('f7jd_2017', period)
        f7je = foyer_fiscal('f7je', period)
        f7jf = foyer_fiscal('f7jf', period)
        f7jg = foyer_fiscal('f7jg', period)
        f7jh = foyer_fiscal('f7jh', period)
        f7jj = foyer_fiscal('f7jj', period)
        f7jk = foyer_fiscal('f7jk', period)
        f7jl = foyer_fiscal('f7jl', period)
        f7jm = foyer_fiscal('f7jm_2017', period)
        f7jn = foyer_fiscal('f7jn_2017', period)
        f7jo = foyer_fiscal('f7jo_2017', period)
        f7jp = foyer_fiscal('f7jp_2016', period)
        f7jq = foyer_fiscal('f7jq_2017', period)
        f7jr = foyer_fiscal('f7jr_2017', period)
        f7la = foyer_fiscal('f7la', period)
        f7lb = foyer_fiscal('f7lb', period)
        f7lc = foyer_fiscal('f7lc', period)
        f7ld = foyer_fiscal('f7ld', period)
        f7le = foyer_fiscal('f7le', period)
        f7lf = foyer_fiscal('f7lf', period)
        f7lm = foyer_fiscal('f7lm_2018', period)
        f7ls = foyer_fiscal('f7ls', period)
        f7lz = foyer_fiscal('f7lz', period)
        f7mg = foyer_fiscal('f7mg', period)
        f7na = foyer_fiscal('f7na_2017', period)
        f7nb = foyer_fiscal('f7nb_2016', period)
        f7nc = foyer_fiscal('f7nc_2017', period)
        f7nd = foyer_fiscal('f7nd_2017', period)
        f7ne = foyer_fiscal('f7ne_2017', period)
        f7nf = foyer_fiscal('f7nf_2017', period)
        f7ng = foyer_fiscal('f7ng_2016', period)
        f7nh = foyer_fiscal('f7nh_2017', period)
        f7ni = foyer_fiscal('f7ni_2017', period)
        f7nj = foyer_fiscal('f7nj_2017', period)
        f7nk = foyer_fiscal('f7nk_2017', period)
        f7nl = foyer_fiscal('f7nl_2016', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        reductions = (min_(P.max, maxi(
            P.taux13 * max_(f7nf, f7nj) / 9,
            P.taux15 * max_(f7ng, f7ni) / 9,
            P.taux22 * max_(f7na, f7ne) / 9,
            P.taux25 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
            P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
            P.taux40 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5)
            ))
            + min_(P.max, maxi(P.taux25 * max_(f7hj, f7hn), P.taux40 * max_(f7hk, f7ho))) / 9
            + min_(P.max, max_(P.taux25 * f7hl, P.taux40 * f7hm)) / 9
            + min_(P.max, maxi(P.taux25 * f7hv, P.taux25 * f7hx, P.taux40 * f7hw, P.taux40 * f7hz))
            + min_(P.max, max_(P.taux25 * f7ht, P.taux40 * f7hu))
            + min_(P.max, max_(P.taux25 * f7hr, P.taux40 * f7hs))
            + min_(P.max, maxi(
                P09.taux_prorogation * maxi(f7jf, f7jj, f7fb) / 9,
                P.taux13 * maxi(f7ja, f7je, f7jg, f7jh, f7fa) / 9,
                P.taux22 * maxi(f7jb, f7jd) / 9,
                P.taux24 * maxi(f7jk / 9, f7jn / 9, f7jo / 5, f7jr / 5, f7fc / 9, f7fd / 5),
                P.taux36 * maxi(f7jl / 9, f7jm / 9, f7jp / 5, f7jq / 5)
                ))
            + f7la + f7lb + f7lc + f7ld + f7le + f7lf + f7lm + f7ls + f7lz
            + f7mg
            + f7ha + f7hb + f7hg + f7hh + f7hd + f7he + f7hf
            + f7gj + f7gk + f7gl + f7gp + f7gs + f7gt + f7gu + f7gv + f7gx + f7gw
            )

        return reductions

    def formula_2014_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2014
        '''
        f7fa = foyer_fiscal('f7fa', period)
        f7fb = foyer_fiscal('f7fb', period)
        f7fc = foyer_fiscal('f7fc', period)
        f7fd = foyer_fiscal('f7fd', period)
        f7gj = foyer_fiscal('f7gj', period)
        f7gk = foyer_fiscal('f7gk', period)
        f7gl = foyer_fiscal('f7gl', period)
        f7gp = foyer_fiscal('f7gp', period)
        f7gs = foyer_fiscal('f7gs', period)
        f7gt = foyer_fiscal('f7gt', period)
        f7gu = foyer_fiscal('f7gu', period)
        f7gv = foyer_fiscal('f7gv', period)
        f7gw = foyer_fiscal('f7gw_2016', period)
        f7gx = foyer_fiscal('f7gx', period)
        f7ha = foyer_fiscal('f7ha', period)
        f7hb = foyer_fiscal('f7hb', period)
        f7hg = foyer_fiscal('f7hg', period)
        f7hh = foyer_fiscal('f7hh', period)
        f7hd = foyer_fiscal('f7hd', period)
        f7he = foyer_fiscal('f7he', period)
        f7hf = foyer_fiscal('f7hf', period)
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl_2010', period)
        f7hm = foyer_fiscal('f7hm_2010', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho_2016', period)
        f7hr = foyer_fiscal('f7hr_2017', period)
        f7hs = foyer_fiscal('f7hs_2017', period)
        f7ht = foyer_fiscal('f7ht_2018', period)
        f7hu = foyer_fiscal('f7hu_2018', period)
        f7hv = foyer_fiscal('f7hv_2018', period)
        f7hw = foyer_fiscal('f7hw_2018', period)
        f7hx = foyer_fiscal('f7hx_2018', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7ja = foyer_fiscal('f7ja_2017', period)
        f7jb = foyer_fiscal('f7jb_2016', period)
        f7jd = foyer_fiscal('f7jd_2017', period)
        f7je = foyer_fiscal('f7je', period)
        f7jf = foyer_fiscal('f7jf', period)
        f7jg = foyer_fiscal('f7jg', period)
        f7jh = foyer_fiscal('f7jh', period)
        f7jj = foyer_fiscal('f7jj', period)
        f7jk = foyer_fiscal('f7jk', period)
        f7jl = foyer_fiscal('f7jl', period)
        f7jm = foyer_fiscal('f7jm_2017', period)
        f7jn = foyer_fiscal('f7jn_2017', period)
        f7jo = foyer_fiscal('f7jo_2017', period)
        f7jp = foyer_fiscal('f7jp_2016', period)
        f7jq = foyer_fiscal('f7jq_2017', period)
        f7jr = foyer_fiscal('f7jr_2017', period)
        f7la = foyer_fiscal('f7la_2016', period)
        f7lb = foyer_fiscal('f7lb_2016', period)
        f7lc = foyer_fiscal('f7lc_2016', period)
        f7ld = foyer_fiscal('f7ld', period)
        f7le = foyer_fiscal('f7le', period)
        f7lf = foyer_fiscal('f7lf', period)
        f7lm = foyer_fiscal('f7lm_2018', period)
        f7ln = foyer_fiscal('f7ln', period)
        f7ls = foyer_fiscal('f7ls', period)
        f7lt = foyer_fiscal('f7lt', period)
        f7lx = foyer_fiscal('f7lx', period)
        f7lz = foyer_fiscal('f7lz', period)
        f7mg = foyer_fiscal('f7mg', period)
        f7mh = foyer_fiscal('f7mh', period)
        f7na = foyer_fiscal('f7na_2017', period)
        f7nb = foyer_fiscal('f7nb_2016', period)
        f7nc = foyer_fiscal('f7nc_2017', period)
        f7nd = foyer_fiscal('f7nd_2017', period)
        f7ne = foyer_fiscal('f7ne_2017', period)
        f7nf = foyer_fiscal('f7nf_2017', period)
        f7ng = foyer_fiscal('f7ng_2016', period)
        f7nh = foyer_fiscal('f7nh_2017', period)
        f7ni = foyer_fiscal('f7ni_2017', period)
        f7nj = foyer_fiscal('f7nj_2017', period)
        f7nk = foyer_fiscal('f7nk_2017', period)
        f7nl = foyer_fiscal('f7nl_2016', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        f7ya = foyer_fiscal('f7ya', period)
        f7yb = foyer_fiscal('f7yb', period)
        f7yc = foyer_fiscal('f7yc', period)
        f7yd = foyer_fiscal('f7yd', period)
        f7ye = foyer_fiscal('f7ye', period)
        f7yf = foyer_fiscal('f7yf', period)
        f7yg = foyer_fiscal('f7yg', period)
        f7yh = foyer_fiscal('f7yh', period)
        f7yi = foyer_fiscal('f7yi', period)
        f7yj = foyer_fiscal('f7yj', period)
        f7yk = foyer_fiscal('f7yk', period)
        f7yl = foyer_fiscal('f7yl', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        report_reduc_scelli_non_impute = f7la + f7lb + f7lc + f7ld + f7le + f7lf + f7lm + f7ls + f7lz + f7mg + f7mh + f7lx + f7lt + f7ln

        report_scelli_2009 = min_(P.max, max_(P.taux25 * f7hr, P.taux40 * f7hs))
        report_scelli_2010 = min_(P.max, P.taux25 * f7hv + P.taux25 * f7hx + P.taux40 * f7hw + P.taux40 * f7hz) + min_(P.max, P.taux25 * f7ht + P.taux40 * f7hu)
        report_scelli_2011 = f7ha + f7hb + f7hg + f7hh + f7hd + f7he + f7hf
        report_scelli_2012 = f7gj + f7gk + f7gl + f7gp + f7gs + f7gt + f7gu + f7gv + f7gx + f7gw
        report_scelli_2013 = f7ya + f7yb + f7yc + f7yd + f7ye + f7yf + f7yg + f7yh + f7yi + f7yj + f7yk + f7yl

        reduc_scelli_2014_invest_2009 = min_(P.max, max_(P.taux25 * f7hl, P.taux40 * f7hm)) / 9

        reduc_scelli_2014_invest_2010 = min_(P.max, maxi(
            P.taux25 * max_(f7hj, f7hn) / 9,
            P.taux40 * max_(f7hk, f7ho) / 9))

        reduc_scelli_2014_invest_2011 = min_(P.max, maxi(
            P.taux13 * max_(f7nf, f7nj) / 9,
            P.taux15 * max_(f7ng, f7ni) / 9,
            P.taux22 * max_(f7na, f7ne) / 9,
            P.taux25 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
            P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
            P.taux40 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5)))

        reduc_scelli_2014_invest_2012 = min_(P.max, maxi(
            P09.taux_prorogation * maxi(f7jf, f7jj) / 9,
            P.taux13 * maxi(f7ja, f7je, f7jg, f7jh) / 9,
            P.taux22 * maxi(f7jb, f7jd) / 9,
            P.taux24 * maxi(f7jk / 9, f7jn / 9, f7jo / 5, f7jr / 5),
            P.taux36 * maxi(f7jl / 9, f7jm / 9, f7jp / 5, f7jq / 5)))

        reduc_scelli_2014_invest_mars_2013 = min_(P.max, maxi(
            P09.taux_prorogation * f7fb / 9,
            P.taux13 * f7fa / 9,
            P.taux24 * maxi(f7fc / 9, f7fd / 5)))

        reductions = (
            reduc_scelli_2014_invest_2009
            + reduc_scelli_2014_invest_2010
            + reduc_scelli_2014_invest_2011
            + reduc_scelli_2014_invest_2012
            + reduc_scelli_2014_invest_mars_2013
            + report_reduc_scelli_non_impute
            + report_scelli_2009
            + report_scelli_2010
            + report_scelli_2011
            + report_scelli_2012
            + report_scelli_2013
            )

        return reductions

    def formula_2015_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2015
        '''
        f7fa = foyer_fiscal('f7fa', period)
        f7fb = foyer_fiscal('f7fb', period)
        f7fc = foyer_fiscal('f7fc', period)
        f7fd = foyer_fiscal('f7fd', period)
        f7gj = foyer_fiscal('f7gj', period)
        f7gl = foyer_fiscal('f7gl', period)
        f7gs = foyer_fiscal('f7gs', period)
        f7gu = foyer_fiscal('f7gu', period)
        f7gv = foyer_fiscal('f7gv', period)
        f7gw = foyer_fiscal('f7gw_2016', period)
        f7gx = foyer_fiscal('f7gx', period)
        f7ha = foyer_fiscal('f7ha', period)
        f7hg = foyer_fiscal('f7hg', period)
        f7hh = foyer_fiscal('f7hh', period)
        f7hd = foyer_fiscal('f7hd', period)
        f7hf = foyer_fiscal('f7hf', period)
        f7hj = foyer_fiscal('f7hj', period)
        f7hk = foyer_fiscal('f7hk', period)
        f7hl = foyer_fiscal('f7hl_2010', period)
        f7hm = foyer_fiscal('f7hm_2010', period)
        f7hn = foyer_fiscal('f7hn', period)
        f7ho = foyer_fiscal('f7ho_2016', period)
        f7hr = foyer_fiscal('f7hr_2017', period)
        f7hs = foyer_fiscal('f7hs_2017', period)
        f7ht = foyer_fiscal('f7ht_2018', period)
        f7hu = foyer_fiscal('f7hu_2018', period)
        f7hv = foyer_fiscal('f7hv_2018', period)
        f7hw = foyer_fiscal('f7hw_2018', period)
        f7hx = foyer_fiscal('f7hx_2018', period)
        f7hz = foyer_fiscal('f7hz', period)
        f7ja = foyer_fiscal('f7ja_2017', period)
        f7jb = foyer_fiscal('f7jb_2016', period)
        f7jd = foyer_fiscal('f7jd_2017', period)
        f7je = foyer_fiscal('f7je', period)
        f7jf = foyer_fiscal('f7jf', period)
        f7jg = foyer_fiscal('f7jg', period)
        f7jh = foyer_fiscal('f7jh', period)
        f7jj = foyer_fiscal('f7jj', period)
        f7jk = foyer_fiscal('f7jk', period)
        f7jl = foyer_fiscal('f7jl', period)
        f7jm = foyer_fiscal('f7jm_2017', period)
        f7jn = foyer_fiscal('f7jn_2017', period)
        f7jo = foyer_fiscal('f7jo_2017', period)
        f7jp = foyer_fiscal('f7jp_2016', period)
        f7jq = foyer_fiscal('f7jq_2017', period)
        f7jr = foyer_fiscal('f7jr_2017', period)
        f7la = foyer_fiscal('f7la_2016', period)
        f7lb = foyer_fiscal('f7lb_2016', period)
        f7lc = foyer_fiscal('f7lc_2016', period)
        f7ld = foyer_fiscal('f7ld', period)
        f7le = foyer_fiscal('f7le', period)
        f7lf = foyer_fiscal('f7lf', period)
        f7lg = foyer_fiscal('f7lg', period)
        f7lh = foyer_fiscal('f7lh', period)
        f7li = foyer_fiscal('f7li', period)
        f7lj = foyer_fiscal('f7lj', period)
        f7lm = foyer_fiscal('f7lm_2018', period)
        f7ln = foyer_fiscal('f7ln', period)
        f7ls = foyer_fiscal('f7ls', period)
        f7lt = foyer_fiscal('f7lt', period)
        f7lx = foyer_fiscal('f7lx', period)
        f7lz = foyer_fiscal('f7lz', period)
        f7mg = foyer_fiscal('f7mg', period)
        f7mh = foyer_fiscal('f7mh', period)
        f7na = foyer_fiscal('f7na_2017', period)
        f7nb = foyer_fiscal('f7nb_2016', period)
        f7nc = foyer_fiscal('f7nc_2017', period)
        f7nd = foyer_fiscal('f7nd_2017', period)
        f7ne = foyer_fiscal('f7ne_2017', period)
        f7nf = foyer_fiscal('f7nf_2017', period)
        f7ng = foyer_fiscal('f7ng_2016', period)
        f7nh = foyer_fiscal('f7nh_2017', period)
        f7ni = foyer_fiscal('f7ni_2017', period)
        f7nj = foyer_fiscal('f7nj_2017', period)
        f7nk = foyer_fiscal('f7nk_2017', period)
        f7nl = foyer_fiscal('f7nl_2016', period)
        f7nm = foyer_fiscal('f7nm', period)
        f7nn = foyer_fiscal('f7nn', period)
        f7no = foyer_fiscal('f7no', period)
        f7np = foyer_fiscal('f7np', period)
        f7nq = foyer_fiscal('f7nq', period)
        f7nr = foyer_fiscal('f7nr', period)
        f7ns = foyer_fiscal('f7ns', period)
        f7nt = foyer_fiscal('f7nt', period)
        f7yb = foyer_fiscal('f7yb', period)
        f7yd = foyer_fiscal('f7yd', period)
        f7yf = foyer_fiscal('f7yf', period)
        f7yh = foyer_fiscal('f7yh', period)
        f7yj = foyer_fiscal('f7yj', period)
        f7yk = foyer_fiscal('f7yk', period)
        f7yl = foyer_fiscal('f7yl', period)
        f7ym = foyer_fiscal('f7ym', period)
        f7yn = foyer_fiscal('f7yn', period)
        f7yo = foyer_fiscal('f7yo', period)
        f7yp = foyer_fiscal('f7yp', period)
        f7yq = foyer_fiscal('f7yq', period)
        f7yr = foyer_fiscal('f7yr', period)
        f7ys = foyer_fiscal('f7ys', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        report_reduc_scelli_non_impute = f7la + f7lb + f7lc + f7ld + f7le + f7lf + f7lm + f7ls + f7lz + f7mg + f7mh + f7lx + f7lt + f7ln + f7lg + f7lh + f7li + f7lj

        report_scelli_2009 = min_(P.max, max_(P.taux25 * f7hr, P.taux40 * f7hs))
        report_scelli_2010 = min_(P.max, P.taux25 * f7hv + P.taux25 * f7hx + P.taux40 * f7hw + P.taux40 * f7hz) + min_(P.max, P.taux25 * f7ht + P.taux40 * f7hu)
        report_scelli_2011 = f7ha + f7hg + f7hh + f7hd + f7hf
        report_scelli_2012 = f7gj + f7gl + f7gs + f7gu + f7gv + f7gx + f7gw
        report_scelli_2013 = f7yb + f7yd + f7yf + f7yh + f7yj + f7yk + f7yl
        report_scelli_2014 = f7ym + f7yn + f7yo + f7yp + f7yq + f7yr + f7ys

        reduc_scelli_2015_invest_2009 = min_(P.max, max_(P.taux25 * f7hl, P.taux40 * f7hm)) / 9

        reduc_scelli_2015_invest_2010 = min_(P.max, maxi(
            P.taux25 * max_(f7hj, f7hn) / 9,
            P.taux40 * max_(f7hk, f7ho) / 9))

        reduc_scelli_2015_invest_2011 = min_(P.max, maxi(
            P.taux13 * max_(f7nf, f7nj) / 9,
            P.taux15 * max_(f7ng, f7ni) / 9,
            P.taux22 * max_(f7na, f7ne) / 9,
            P.taux25 * maxi(f7nb, f7nc, f7nd, f7nh) / 9,
            P.taux36 * maxi(f7nk / 9, f7no / 9, f7np / 5, f7nt / 5),
            P.taux40 * maxi(f7nl / 9, f7nm / 9, f7nn / 9, f7nq / 5, f7nr / 5, f7ns / 5)))

        reduc_scelli_2015_invest_2012 = min_(P.max, maxi(
            P09.taux_prorogation * maxi(f7jf, f7jj) / 9,
            P.taux13 * maxi(f7ja, f7je, f7jg, f7jh) / 9,
            P.taux22 * maxi(f7jb, f7jd) / 9,
            P.taux24 * maxi(f7jk / 9, f7jn / 9, f7jo / 5, f7jr / 5),
            P.taux36 * maxi(f7jl / 9, f7jm / 9, f7jp / 5, f7jq / 5)))

        reduc_scelli_2015_invest_mars_2013 = min_(P.max, maxi(
            P09.taux_prorogation * f7fb / 9,
            P.taux13 * f7fa / 9,
            P.taux24 * maxi(f7fc / 9, f7fd / 5)))

        reductions = (
            reduc_scelli_2015_invest_2009
            + reduc_scelli_2015_invest_2010
            + reduc_scelli_2015_invest_2011
            + reduc_scelli_2015_invest_2012
            + reduc_scelli_2015_invest_mars_2013
            + report_reduc_scelli_non_impute
            + report_scelli_2009
            + report_scelli_2010
            + report_scelli_2011
            + report_scelli_2012
            + report_scelli_2013
            + report_scelli_2014
            )

        return reductions

    def formula_2016_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2016

        NB: Formulas prior to 2016 need to be checked.
        '''
        reports = [
            'f7ym', 'f7yt',
            'f7yn', 'f7yu',
            'f7yo', 'f7yv',
            'f7yp', 'f7yw',

            'f7yq', 'f7yx',
            'f7yr', 'f7yy',
            'f7ys', 'f7yz',

            'f7gj', 'f7yb',
            'f7gl', 'f7yd',
            'f7gs', 'f7yf',
            'f7gu', 'f7yh',

            'f7gv', 'f7yj', 'f7gw_2016', 'f7yk', 'f7gx', 'f7yl',
            'f7ha', 'f7hd', 'f7hf',

            'f7lb_2016', 'f7le', 'f7lm_2018', 'f7ln', 'f7lg', 'f7lk',
            'f7lc_2016', 'f7ld', 'f7ls', 'f7lt', 'f7lh', 'f7ll',
            'f7lf', 'f7lz', 'f7lx', 'f7li', 'f7lo',
            'f7mg', 'f7mh', 'f7lj', 'f7lp',
            ]

        reports_base_25 = [
            'f7hv_2018', 'f7hx_2018', 'f7ht_2018', 'f7hr_2017'
            ]

        reports_base_40 = [
            'f7hw_2018', 'f7hz', 'f7hu_2018', 'f7hs_2017',
            ]

        inv_5_40 = ['f7nq', 'f7nr', 'f7ns', 'f7nt']
        inv_5_36 = ['f7jp_2016', 'f7jq_2017', 'f7np']
        inv_5_24 = ['f7fd', 'f7jo_2017', 'f7jr_2017']
        inv_9_40 = ['f7nl_2016', 'f7nm', 'f7nn', 'f7no', 'f7hk', 'f7ho_2016']
        inv_9_36 = ['f7jl', 'f7jm_2017', 'f7nk_2017']
        inv_9_25 = ['f7nb_2016', 'f7nc_2017', 'f7nh_2017', 'f7nd_2017', 'f7hj', 'f7hn']
        inv_9_24 = ['f7fc', 'f7jk', 'f7jn_2017']
        inv_9_22 = ['f7jb_2016', 'f7jd_2017', 'f7na_2017', 'f7ne_2017']
        inv_9_15 = ['f7ni_2017', 'f7ng_2016']
        inv_9_13 = ['f7fa', 'f7ja_2017', 'f7jg', 'f7jh', 'f7je', 'f7nf_2017', 'f7nj_2017']
        inv_9_6 = ['f7fb', 'f7jf', 'f7jj']
        inv_3_6 = ['f7zb', 'f7zc']
        inv_3_5 = ['f7za', 'f7zd']

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        ri_rep = sum([foyer_fiscal(rep, period) for rep in reports])

        ri_rep = ri_rep + min_(P.max, sum([foyer_fiscal(r, period) for r in reports_base_40]) * P.taux40)
        ri_rep = ri_rep + min_(P.max, sum([foyer_fiscal(r, period) for r in reports_base_25]) * P.taux25)

        base_inv_5_40 = min_(sum([foyer_fiscal(i, period) for i in inv_5_40]), P.max)
        base_inv_5_36 = min_(sum([foyer_fiscal(i, period) for i in inv_5_36]), P.max - base_inv_5_40)
        base_inv_5_24 = min_(sum([foyer_fiscal(i, period) for i in inv_5_24]), P.max - base_inv_5_40 - base_inv_5_36)
        base_inv_9_40 = min_(sum([foyer_fiscal(i, period) for i in inv_9_40]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24)
        base_inv_9_36 = min_(sum([foyer_fiscal(i, period) for i in inv_9_36]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40)
        base_inv_9_25 = min_(sum([foyer_fiscal(i, period) for i in inv_9_25]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36)
        base_inv_9_24 = min_(sum([foyer_fiscal(i, period) for i in inv_9_24]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25)
        base_inv_9_22 = min_(sum([foyer_fiscal(i, period) for i in inv_9_22]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24)
        base_inv_9_15 = min_(sum([foyer_fiscal(i, period) for i in inv_9_15]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22)
        base_inv_9_13 = min_(sum([foyer_fiscal(i, period) for i in inv_9_13]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15)
        base_inv_9_6 = min_(sum([foyer_fiscal(i, period) for i in inv_9_6]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15 - base_inv_9_13)
        base_inv_3_6 = min_(sum([foyer_fiscal(i, period) for i in inv_3_6]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15 - base_inv_9_13 - base_inv_9_6)
        base_inv_3_5 = min_(sum([foyer_fiscal(i, period) for i in inv_3_5]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15 - base_inv_9_13 - base_inv_9_6 - base_inv_3_6)

        red_inv_5_40 = base_inv_5_40 * P.taux40 / 5
        red_inv_5_36 = base_inv_5_36 * P.taux36 / 5
        red_inv_5_24 = base_inv_5_24 * P.taux24 / 5
        red_inv_9_40 = base_inv_9_40 * P.taux40 / 9
        red_inv_9_36 = base_inv_9_36 * P.taux36 / 9
        red_inv_9_25 = base_inv_9_25 * P.taux25 / 9
        red_inv_9_24 = base_inv_9_24 * P.taux24 / 9
        red_inv_9_22 = base_inv_9_22 * P.taux22 / 9
        red_inv_9_15 = base_inv_9_15 * P.taux15 / 9
        red_inv_9_13 = base_inv_9_13 * P.taux13 / 9
        red_inv_9_6 = base_inv_9_6 * P09.taux_prorogation / 9
        red_inv_3_6 = base_inv_3_6 * P09.taux_prorogation / 3
        red_inv_3_5 = base_inv_3_5 * P11.taux_prorogation / 3

        reductions = ri_rep + red_inv_5_40 + red_inv_5_36 + red_inv_5_24 + red_inv_9_40 + red_inv_9_36 + red_inv_9_25 + red_inv_9_24 + red_inv_9_22 + red_inv_9_15 + red_inv_9_13 + red_inv_9_6 + red_inv_3_6 + red_inv_3_5

        return reductions

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2017
        '''

        reports = [
            'f7ym', 'f7yt', 'f7wt',
            'f7yn', 'f7yu', 'f7wu',
            'f7yo', 'f7yv', 'f7wv',
            'f7yp', 'f7yw', 'f7ww',
            'f7yq', 'f7yx', 'f7wx',
            'f7yr', 'f7yy', 'f7wy',
            'f7ys', 'f7yz', 'f7wz',
            'f7gj', 'f7yb',
            'f7ha', 'f7gl', 'f7yd',
            'f7hd', 'f7gs', 'f7yf',
            'f7hf', 'f7gu', 'f7yh',
            'f7yj', 'f7yk', 'f7yl',
            'f7le', 'f7lm_2018', 'f7ln', 'f7lg', 'f7lk', 'f7lq',
            'f7ld', 'f7ls', 'f7lt', 'f7lh', 'f7ll', 'f7lr',
            'f7lf', 'f7lz', 'f7lx', 'f7li', 'f7lo', 'f7lu',
            'f7mg', 'f7mh', 'f7lj', 'f7lp', 'f7lv',
            'f7zm', 'f7zn', 'f7zp', 'f7zo']

        reports_base_25 = [
            'f7hv_2018', 'f7hx_2018', 'f7ht_2018', 'f7hr_2017']

        reports_base_40 = [
            'f7hw_2018', 'f7hz', 'f7hu_2018', 'f7hs_2017'
            ]

        inv_5_40 = ['f7nr', 'f7ns', 'f7nt']
        inv_5_36 = ['f7jq_2017', 'f7np']
        inv_5_24 = ['f7fd', 'f7jo_2017', 'f7jr_2017']
        inv_9_40 = ['f7nm', 'f7nn', 'f7no']
        inv_9_36 = ['f7jm_2017', 'f7nk_2017']
        inv_9_25 = ['f7nc_2017', 'f7nh_2017', 'f7nd_2017']
        inv_9_24 = ['f7fc', 'f7jk', 'f7jn_2017']
        inv_9_22 = ['f7jd_2017', 'f7na_2017', 'f7ne_2017']
        inv_9_15 = ['f7ni_2017']
        inv_9_13 = ['f7fa', 'f7ja_2017', 'f7jh', 'f7je', 'f7nf_2017', 'f7nj_2017']
        inv_9_6 = ['f7fb', 'f7jf', 'f7jj']
        inv_3_6 = ['f7zb', 'f7zc', 'f7zf', 'f7zg']
        inv_3_5 = ['f7za', 'f7zd', 'f7ze', 'f7zh', 'f7zj', 'f7zk']
        inv_3_4 = ['f7zi', 'f7zl']

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P12 = parameters('2012-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        ri_rep = sum([foyer_fiscal(rep, period) for rep in reports])

        ri_rep = ri_rep + min_(P.max, sum([foyer_fiscal(r, period) for r in reports_base_40]) * P.taux40)
        ri_rep = ri_rep + min_(P.max, sum([foyer_fiscal(r, period) for r in reports_base_25]) * P.taux25)

        base_inv_5_40 = min_(sum([foyer_fiscal(i, period) for i in inv_5_40]), P.max)
        base_inv_5_36 = min_(sum([foyer_fiscal(i, period) for i in inv_5_36]), P.max - base_inv_5_40)
        base_inv_5_24 = min_(sum([foyer_fiscal(i, period) for i in inv_5_24]), P.max - base_inv_5_40 - base_inv_5_36)
        base_inv_9_40 = min_(sum([foyer_fiscal(i, period) for i in inv_9_40]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24)
        base_inv_9_36 = min_(sum([foyer_fiscal(i, period) for i in inv_9_36]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40)
        base_inv_9_25 = min_(sum([foyer_fiscal(i, period) for i in inv_9_25]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36)
        base_inv_9_24 = min_(sum([foyer_fiscal(i, period) for i in inv_9_24]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25)
        base_inv_9_22 = min_(sum([foyer_fiscal(i, period) for i in inv_9_22]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24)
        base_inv_9_15 = min_(sum([foyer_fiscal(i, period) for i in inv_9_15]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22)
        base_inv_9_13 = min_(sum([foyer_fiscal(i, period) for i in inv_9_13]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15)
        base_inv_9_6 = min_(sum([foyer_fiscal(i, period) for i in inv_9_6]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15 - base_inv_9_13)
        base_inv_3_6 = min_(sum([foyer_fiscal(i, period) for i in inv_3_6]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15 - base_inv_9_13 - base_inv_9_6)
        base_inv_3_5 = min_(sum([foyer_fiscal(i, period) for i in inv_3_5]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15 - base_inv_9_13 - base_inv_9_6 - base_inv_3_6)
        base_inv_3_4 = min_(sum([foyer_fiscal(i, period) for i in inv_3_4]), P.max - base_inv_5_40 - base_inv_5_36 - base_inv_5_24 - base_inv_9_40 - base_inv_9_36 - base_inv_9_25 - base_inv_9_24 - base_inv_9_22 - base_inv_9_15 - base_inv_9_13 - base_inv_9_6 - base_inv_3_6 - base_inv_3_5)

        red_inv_5_40 = base_inv_5_40 * P.taux40 / 5
        red_inv_5_36 = base_inv_5_36 * P.taux36 / 5
        red_inv_5_24 = base_inv_5_24 * P.taux24 / 5
        red_inv_9_40 = base_inv_9_40 * P.taux40 / 9
        red_inv_9_36 = base_inv_9_36 * P.taux36 / 9
        red_inv_9_25 = base_inv_9_25 * P.taux25 / 9
        red_inv_9_24 = base_inv_9_24 * P.taux24 / 9
        red_inv_9_22 = base_inv_9_22 * P.taux22 / 9
        red_inv_9_15 = base_inv_9_15 * P.taux15 / 9
        red_inv_9_13 = base_inv_9_13 * P.taux13 / 9
        red_inv_9_6 = base_inv_9_6 * P09.taux_prorogation / 9
        red_inv_3_6 = base_inv_3_6 * P09.taux_prorogation / 3
        red_inv_3_5 = base_inv_3_5 * P11.taux_prorogation / 3
        red_inv_3_4 = base_inv_3_4 * P12.taux_prorogation / 3

        reductions = ri_rep + red_inv_5_40 + red_inv_5_36 + red_inv_5_24 + red_inv_9_40 + red_inv_9_36 + red_inv_9_25 + red_inv_9_24 + red_inv_9_22 + red_inv_9_15 + red_inv_9_13 + red_inv_9_6 + red_inv_3_6 + red_inv_3_5 + red_inv_3_4

        return reductions

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2018
        '''

        reports = [
            'f7rt', 'f7ru', 'f7rv', 'f7rw',

            'f7ym', 'f7yt', 'f7wt',
            'f7yn', 'f7yu', 'f7wu',
            'f7yo', 'f7yv', 'f7wv',
            'f7yp', 'f7yw', 'f7ww',

            'f7yq', 'f7yx', 'f7wx',
            'f7yr', 'f7yy', 'f7wy',
            'f7ys', 'f7yz', 'f7wz',

            'f7gj', 'f7yb',
            'f7ha', 'f7gl', 'f7yd',
            'f7hd', 'f7gs', 'f7yf',
            'f7hf', 'f7gu', 'f7yh',

            'f7lm_2018', 'f7ln', 'f7lg', 'f7lk', 'f7lq', 'f7la',
            'f7ls', 'f7lt', 'f7lh', 'f7ll', 'f7lr', 'f7lb',
            'f7lz', 'f7lx', 'f7li', 'f7lo', 'f7lu', 'f7lc',
            'f7mg', 'f7mh', 'f7lj', 'f7lp', 'f7lv', 'f7ly',

            'f7zm', 'f7zn',
            'f7zq', 'f7zr',
            'f7zs',
            'f7zu', 'f7zt',

            'f7zp', 'f7xp',
            'f7zo', 'f7xo',
            'f7xq',
            ]

        reports_base_25 = [
            'f7hv_2018', 'f7hx_2018', 'f7ht_2018',
            ]

        reports_base_40 = [
            'f7hw_2018', 'f7hz', 'f7hu_2018',
            ]

        inv_6 = [
            'f7zv', 'f7zf',
            'f7zg', 'f7sf',
            'f7sg',
            ]

        inv_5 = [
            'f7ze', 'f7zh',
            'f7zj', 'f7zk',
            'f7se', 'f7sh',
            'f7sj', 'f7sk',
            ]

        inv_4 = [
            'f7zi', 'f7zl',
            'f7sl', 'f7sm_2019',
            ]

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P12 = parameters('2012-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        ri_rep = sum([foyer_fiscal(rep, period) for rep in reports])

        ri_rep = ri_rep + min_(P.max, sum([foyer_fiscal(r, period) for r in reports_base_40]) * P.taux40)
        ri_rep = ri_rep + min_(P.max, sum([foyer_fiscal(r, period) for r in reports_base_25]) * P.taux25)

        base_ri_6 = min_(P.max, sum([foyer_fiscal(inv, period) for inv in inv_6]))
        base_ri_5 = min_(P.max - base_ri_6, sum([foyer_fiscal(inv, period) for inv in inv_5]))
        base_ri_4 = min_(P.max - base_ri_6 - base_ri_5, sum([foyer_fiscal(inv, period) for inv in inv_4]))

        ri_6 = base_ri_6 * P09.taux_prorogation / 3
        ri_5 = base_ri_5 * P11.taux_prorogation / 3
        ri_4 = base_ri_4 * P12.taux_prorogation / 3

        reductions = ri_rep + ri_6 + ri_5 + ri_4

        return reductions

    def formula_2019_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2019
        '''

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P12 = parameters('2012-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        reports = [
            'f7rt', 'f7ru', 'f7rv', 'f7rw',

            'f7ym', 'f7yt', 'f7wt', 'f7yn',
            'f7yu', 'f7wu', 'f7yo', 'f7yv',
            'f7wv', 'f7yp', 'f7yw', 'f7ww',

            'f7yx', 'f7wx', 'f7yy', 'f7wy',
            'f7yz', 'f7wz',

            'f7gj', 'f7yb', 'f7ha', 'f7gl',
            'f7yd', 'f7hd', 'f7gs', 'f7yf',
            'f7hf', 'f7gu', 'f7yh',

            'f7ln', 'f7lg', 'f7lk', 'f7lq',
            'f7la', 'f7ms', 'f7lt', 'f7lh',
            'f7ll', 'f7lr', 'f7lb', 'f7mt',
            'f7lx', 'f7li', 'f7lo', 'f7lu',
            'f7lc', 'f7mu', 'f7mh', 'f7lj',
            'f7lp', 'f7lv', 'f7ly', 'f7mv',

            'f7zq', 'f7zr', 'f7zs', 'f7zu',
            'f7zt', 'f7wa', 'f7wb', 'f7wc',
            'f7wd', 'f7we', 'f7wf', 'f7wg',

            'f7yi', 'f7zp', 'f7xp', 'f7yj',
            'f7zo', 'f7xo', 'f7yk', 'f7xq',
            'f7yl']

        inv_6 = [
            'f7zv', 'f7za',
            'f7zb', 'f7sf',
            'f7sg', 'f7rj',
            'f7rk', 'f7xi',
            'f7xj',
            ]

        inv_5 = [
            'f7se', 'f7sh',
            'f7sj', 'f7sk',
            'f7ri', 'f7rl',
            'f7rn', 'f7ro',
            'f7xh', 'f7xk',
            ]

        inv_4 = [
            'f7sl', 'f7sm_2019',
            'f7rm', 'f7rp',
            'f7rq',
            ]

        ri_rep = sum([foyer_fiscal(rep, period) for rep in reports])

        base_ri_6 = min_(P.max, sum([foyer_fiscal(inv, period) for inv in inv_6]))
        base_ri_5 = min_(P.max - base_ri_6, sum([foyer_fiscal(inv, period) for inv in inv_5]))
        base_ri_4 = min_(P.max - base_ri_6 - base_ri_5, sum([foyer_fiscal(inv, period) for inv in inv_4]))

        ri_6 = base_ri_6 * P09.taux_prorogation / 3
        ri_5 = base_ri_5 * P11.taux_prorogation / 3
        ri_4 = base_ri_4 * P12.taux_prorogation / 3

        reductions = ri_rep + ri_6 + ri_5 + ri_4

        return reductions

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2020
        '''

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P12 = parameters('2012-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        reports = [
            'f7rt', 'f7ru', 'f7rv', 'f7rw',

            'f7ym', 'f7yt', 'f7wt', 'f7yn',
            'f7yu', 'f7wu', 'f7yo', 'f7yv',
            'f7wv', 'f7yp', 'f7yw', 'f7ww',

            'f7wx', 'f7wy', 'f7wz',

            'f7gj', 'f7yb', 'f7gl',
            'f7yd', 'f7gs', 'f7yf',
            'f7gu', 'f7yh',

            'f7lg', 'f7lk', 'f7lq', 'f7la', 'f7ms', 'f7mo',
            'f7lh', 'f7ll', 'f7lr', 'f7lb', 'f7mt', 'f7mp',
            'f7li', 'f7lo', 'f7lu', 'f7lc', 'f7mu', 'f7mq',
            'f7lj', 'f7lp', 'f7lv', 'f7ly', 'f7mv', 'f7mr',

            'f7wa', 'f7wb', 'f7wc',
            'f7wd', 'f7we', 'f7wf', 'f7wg',
            'f7no', 'f7np', 'f7nq',
            'f7nr', 'f7ns', 'f7nt',
            'f7nu', 'f7nv', 'f7nw',

            'f7yi', 'f7zi',
            'f7zp', 'f7xp', 'f7yj', 'f7zj',
            'f7zo', 'f7xo', 'f7yk', 'f7zk',
            'f7xq', 'f7yl', 'f7zl',

            'f7ka', 'f7kb', 'f7kc', 'f7kd',
            ]

        inv_6 = [
            'f7za', 'f7zb', 'f7zm', 'f7zd',
            'f7ze', 'f7zg', 'f7zh', 'f7zn',
            'f7rj', 'f7rk', 'f7is', 'f7it',
            'f7xi', 'f7xj', 'f7jf', 'f7jg',
            ]

        inv_5 = [
            'f7zc', 'f7zf', 'f7ri', 'f7rl',
            'f7rn', 'f7ro', 'f7ir', 'f7iu',
            'f7iw', 'f7ix', 'f7xh', 'f7xk',
            'f7je', 'f7jh', 'f7jj', 'f7jk',
            ]

        inv_4 = [
            'f7rm', 'f7rp', 'f7rq', 'f7iv',
            'f7iy', 'f7iz', 'f7ji', 'f7jl',
            ]

        ri_rep = sum([foyer_fiscal(rep, period) for rep in reports])

        base_ri_6 = min_(P.max, sum([foyer_fiscal(inv, period) for inv in inv_6]))
        base_ri_5 = min_(P.max - base_ri_6, sum([foyer_fiscal(inv, period) for inv in inv_5]))
        base_ri_4 = min_(P.max - base_ri_6 - base_ri_5, sum([foyer_fiscal(inv, period) for inv in inv_4]))

        ri_6 = base_ri_6 * P09.taux_prorogation / 3
        ri_5 = base_ri_5 * P11.taux_prorogation / 3
        ri_4 = base_ri_4 * P12.taux_prorogation / 3

        reductions = ri_rep + ri_6 + ri_5 + ri_4

        return reductions

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Investissements locatif neufs : Dispositif Scellier
        2021
        '''

        P = parameters(period).impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P09 = parameters('2009-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P11 = parameters('2011-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli
        P12 = parameters('2012-01-01').impot_revenu.calcul_reductions_impots.investissements_immobiliers.scelli

        reports = [
            'f7rt', 'f7ru', 'f7rv', 'f7rw',

            'f7ym', 'f7yt', 'f7wt',
            'f7yn', 'f7yu', 'f7wu',
            'f7yo', 'f7yv', 'f7wv',
            'f7yp', 'f7yw', 'f7ww',

            'f7wx', 'f7wy', 'f7wz',

            'f7yb', 'f7yd', 'f7yf', 'f7yh',

            'f7lk', 'f7lq', 'f7la', 'f7ms', 'f7mo', 'f7ma',
            'f7ll', 'f7lr', 'f7lb', 'f7mt', 'f7mp', 'f7mb',
            'f7lo', 'f7lu', 'f7lc', 'f7mu', 'f7mq', 'f7mc',
            'f7lp', 'f7lv', 'f7ly', 'f7mv', 'f7mr', 'f7md',
            'f7no', 'f7np', 'f7nq',
            'f7nr', 'f7ns', 'f7nt',
            'f7nu', 'f7nv', 'f7nw',

            'f7xa', 'f7xb',
            'f7ys', 'f7xc', 'f7xl',
            'f7xm', 'f7xn', 'f7ya',
            'f7yc', 'f7yg', 'f7yr',

            'f7yi', 'f7zi', 'f7uu',
            'f7zp', 'f7xp', 'f7yj', 'f7zj', 'f7uv',
            'f7zo', 'f7xo', 'f7yk', 'f7zk', 'f7uw',
            'f7xq', 'f7yl', 'f7zl', 'f7ux',

            'f7ka', 'f7kb',
            'f7ha', 'f7hj', 'f7hk', 'f7hn', 'f7hy',

            'f7kc', 'f7pc',
            'f7kd', 'f7pd',
            'f7pe',
            ]

        inv_6 = [
            'f7zd', 'f7ze', 'f7zg', 'f7zh',
            'f7zn', 'f7si', 'f7sj', 'f7sl',
            'f7sq', 'f7sr', 'f7is', 'f7it',
            'f7ib', 'f7ic', 'f7iq', 'f7jf',
            'f7jg', 'f7le', 'f7lf',
            ]

        inv_5 = [
            'f7zc', 'f7zf', 'f7se', 'f7sf',
            'f7sh', 'f7sk', 'f7ir', 'f7iu',
            'f7iw', 'f7ix', 'f7ia', 'f7ie',
            'f7ig', 'f7ih', 'f7je', 'f7jh',
            'f7jj', 'f7jk', 'f7ld', 'f7ln',
            'f7lx', 'f7lz',
            ]

        inv_4 = [
            'f7sd', 'f7sg', 'f7iv', 'f7iy',
            'f7iz', 'f7if', 'f7io', 'f7ip',
            'f7ji', 'f7jl', 'f7lt', 'f7mg',
            'f7mh',
            ]

        ri_rep = sum([foyer_fiscal(rep, period) for rep in reports])

        base_ri_6 = min_(P.max, sum([foyer_fiscal(inv, period) for inv in inv_6]))
        base_ri_5 = min_(P.max - base_ri_6, sum([foyer_fiscal(inv, period) for inv in inv_5]))
        base_ri_4 = min_(P.max - base_ri_6 - base_ri_5, sum([foyer_fiscal(inv, period) for inv in inv_4]))

        ri_6 = base_ri_6 * P09.taux_prorogation / 3
        ri_5 = base_ri_5 * P11.taux_prorogation / 3
        ri_4 = base_ri_4 * P12.taux_prorogation / 3

        reductions = ri_rep + ri_6 + ri_5 + ri_4

        return reductions


class sofica(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'sofica'
    definition_period = YEAR

    def formula_2006_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital de SOFICA
        2006-2016
        '''
        f7gn = foyer_fiscal('f7gn', period)
        f7fn = foyer_fiscal('f7fn', period)
        rng = foyer_fiscal('rng', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.sofica

        max0 = min_(P.plafond_revenu_net_global * max_(rng, 0), P.plafond)
        max1 = max_(0, max0 - f7gn)

        return P.taux_1 * min_(f7gn, max0) + P.taux_2 * min_(f7fn, max1)

    def formula_2017_01_01(foyer_fiscal, period, parameters):
        '''
        Souscriptions au capital de SOFICA
        2017-
        '''
        f7gn = foyer_fiscal('f7gn', period)
        f7fn = foyer_fiscal('f7fn', period)
        f7en = foyer_fiscal('f7en', period)
        rng = foyer_fiscal('rng', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.sofica

        max0 = min_(P.plafond_revenu_net_global * max_(rng, 0), P.plafond)
        max1 = max_(0, max0 - f7en)
        max2 = max_(0, max0 - f7gn)

        return (
            P.taux_3 * min_(f7en, max0)
            + P.taux_1 * min_(f7gn, max1)
            + P.taux_2 * min_(f7fn, max2)
            )


class sofipe(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'sofipe'
    end = '2011-01-01'
    definition_period = YEAR

    def formula_2009_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription au capital d’une SOFIPECHE (case 7GS)
        2009-2011
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        rbg_int = foyer_fiscal('rbg_int', period)
        f7gs = foyer_fiscal('f7gs_2009', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.sofipeche

        max1 = min_(P.plafond * (maries_ou_pacses + 1), P.plafond_revenu_net_global * rbg_int)  # page3 ligne 18
        return P.taux * min_(f7gs, max1)


class souscriptions_parts_fcpi_fip(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'souscriptions_parts_fcpi_fip'
    reference = 'http://bofip.impots.gouv.fr/bofip/5321-PGP'
    definition_period = YEAR

    def formula_2002_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2002
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)
        return P.taux * min_(f7gq, max1)

    def formula_2003_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2003-2006
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7fq = foyer_fiscal('f7fq', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)
        return (P.taux * min_(f7gq, max1) + P.taux * min_(f7fq, max1))

    def formula_2007_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2007-2010
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7fq = foyer_fiscal('f7fq', period)
        f7fm = foyer_fiscal('f7fm', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)

        return (P.taux * min_(f7gq, max1)
            + P.taux * min_(f7fq, max1)
            + P.taux_corse * min_(f7fm, max1))

    def formula_2011_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2011-2019
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7fq = foyer_fiscal('f7fq', period)
        f7fm = foyer_fiscal('f7fm', period)
        f7fl = foyer_fiscal('f7fl', period)
        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)

        return (P.taux * min_(f7gq, max1)
            + P.taux * min_(f7fq, max1)
            + P.taux_corse * min_(f7fm, max1)
            + P.taux_outre_mer * min_(f7fl, max1))

    def formula_2020_08_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2020
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7gr = foyer_fiscal('f7gr', period)
        f7fq = foyer_fiscal('f7fq', period)
        f7ft = foyer_fiscal('f7ft', period)
        f7fm = foyer_fiscal('f7fm', period)
        f7hm = foyer_fiscal('f7hm', period)
        f7fl = foyer_fiscal('f7fl', period)
        f7hl = foyer_fiscal('f7hl', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip
        P1 = parameters('2020-08-01').impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip
        P2 = parameters('2020-08-31').impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)

        mon_7gr = min_(max1, f7gr)
        mon_7gq = min_(max1 - mon_7gr, f7gq)

        mon_7ft = min_(max1, f7ft)
        mon_7fq = min_(max1 - mon_7ft, f7fq)

        mon_7fm = min_(max1, f7fm)
        mon_7hm = min_(max1 - mon_7fm, f7hm)

        mon_7fl = min_(max1, f7fl)
        mon_7hl = min_(max1 - mon_7fl, f7hl)

        return (P.taux * (mon_7gq + mon_7fq)
            + P1.taux_corse * mon_7fm
            + P1.taux_outre_mer * mon_7fl
            + P.taux_special * (mon_7gr + mon_7ft)
            + P2.taux_corse * mon_7hm + P2.taux_outre_mer * mon_7hl)

    def formula_2021_01_01(foyer_fiscal, period, parameters):
        '''
        Souscription de parts de fonds communs de placement dans l'innovation,
        de fonds d'investissement de proximité
        2021
        '''
        maries_ou_pacses = foyer_fiscal('maries_ou_pacses', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7gr = foyer_fiscal('f7gr', period)
        f7fq = foyer_fiscal('f7fq', period)
        f7ft = foyer_fiscal('f7ft', period)
        f7fm = foyer_fiscal('f7fm', period)
        f7fl = foyer_fiscal('f7fl', period)

        P = parameters(period).impot_revenu.calcul_reductions_impots.souscriptions.souscriptions_parts_fcpi_fip

        max1 = P.plafond_celibataire * (maries_ou_pacses + 1)

        mon_7gr = min_(max1, f7gr)
        mon_7gq = min_(max1 - mon_7gr, f7gq)

        mon_7ft = min_(max1, f7ft)
        mon_7fq = min_(max1 - mon_7ft, f7fq)

        mon_7fm = min_(max1, f7fm)

        mon_7fl = min_(max1, f7fl)

        return (P.taux * (mon_7gq + mon_7fq)
            + P.taux_corse * mon_7fm
            + P.taux_outre_mer * mon_7fl
            + P.taux_special * (mon_7gr + mon_7ft))


def mini(a, b, *args):
    if not args:
        return min_(a, b)
    else:
        return min_(a, mini(b, *args))


def maxi(a, b, *args):
    if not args:
        return max_(a, b)
    else:
        return max_(a, maxi(b, *args))
