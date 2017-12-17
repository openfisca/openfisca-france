exit()
python

import sys
sys.path.insert(0, '/home/giuliano/Documents/openfisca/openfisca-core')
import openfisca_core
sys.path.insert(0, '/home/giuliano/Documents/openfisca/openfisca-france')
# Call module describing the French System
from openfisca_france import FranceTaxBenefitSystem

# Initialize the legislation
tax_benefit_system = FranceTaxBenefitSystem()

from openfisca_france.reforms import plf2018

reform = plf2018.plf2018(tax_benefit_system)

def init_profile(scenario):
    scenario.init_single_entity(
        period = 'year:2017:6',
        parent1 = dict(
            age = 40,
            salaire_de_base = 1480*12*6,
            categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
            statut_marital = 2,
            ),
        # parent2 = dict(
        #     age = 70,
        #     retraite_brute = 2074*12*6,
        #     # categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
        #     statut_marital = 1,
        #     ),
        # enfants = [
        #     dict(age = 9),
        #     dict(age = 10),
        #     dict(age = 10),
        #     dict(age = 14),
        # ],
        menage = dict(loyer = 5000, # Annual basis
            cotisation_taxe_habitation = -624.*6,
            ),
        # foyer_fiscal= dict(taux_csg_remplacement_2 = 3),
        )
    return scenario

##################################
# Computation with reform reforme
##################################
#Indicate that you want to perfom the reform on this scenario
reform_scenario = init_profile(reform.new_scenario())
#Simulate the reform
reform_simulation = reform_scenario.new_simulation()

###################################
# Computation of the counterfactual
###################################
#Indicate that you want to perfom the standard system on this scenario
reference_scenario = init_profile(tax_benefit_system.new_scenario())
#Simulate the standard scenario
reference_simulation = reference_scenario.new_simulation()

retraite_nette = reference_simulation.calculate("retraite_nette", "2021-01")


# Calcul des résultats
rd_av_2018 = reference_simulation.calculate('revenu_disponible', '2018')/12
rd_ap_2018 = reform_simulation.calculate('revenu_disponible', '2018')/12
gain_2018 = -(rd_av_2018-rd_ap_2018)

rd_av_2019 = reference_simulation.calculate('revenu_disponible', '2019')/12
rd_ap_2019 = reform_simulation.calculate('revenu_disponible', '2019')/12
gain_2019 = -(rd_av_2019-rd_ap_2019)

rd_av_2020 = reference_simulation.calculate('revenu_disponible', '2020')/12
rd_ap_2020 = reform_simulation.calculate('revenu_disponible', '2020')/12
gain_2020 = -(rd_av_2020-rd_ap_2020)

rd_av_2021 = reference_simulation.calculate('revenu_disponible', '2021')/12
rd_ap_2021 = reform_simulation.calculate('revenu_disponible', '2021')/12
gain_2021 = -(rd_av_2021-rd_ap_2021)

rd_av_2022 = reference_simulation.calculate('revenu_disponible', '2022')/12
rd_ap_2022 = reform_simulation.calculate('revenu_disponible', '2022')/12
gain_2022 = -(rd_av_2022-rd_ap_2022)

print(gain_2018)
print(gain_2019)
print(gain_2020)
print(gain_2021)
print(gain_2022)
# 
# # a exporter en JSON : gain_2018 et gain_2019
# 
# # Tests pour voir sir la bascule de cotisation CSG est bien faite.
# print(reform_simulation.calculate("salaire_net","2018-01")-reference_simulation.calculate("salaire_net","2018-01"))
# print(reform_simulation.calculate("salaire_net","2019-01")-reference_simulation.calculate("salaire_net","2019-01"))
# print(reform_simulation.calculate("salaire_net","2020-01")-reference_simulation.calculate("salaire_net","2020-01"))
# print(reform_simulation.calculate("salaire_net","2021-01")-reference_simulation.calculate("salaire_net","2021-01"))
# print(reform_simulation.calculate("salaire_net","2022-01")-reference_simulation.calculate("salaire_net","2022-01"))

# taux_csg_remplacement

# Variables after reform
# cotis_th_ap = reform_simulation.calculate("taxe_habitation", "2019")
# traitement_indiciaire_brut = reform_simulation.calculate("traitement_indiciaire_brut", "2019")

mv_av = reference_simulation.calculate("aspa", "2021-01")
mv_ap = reform_simulation.calculate("aspa", "2021-01")
mv_av
mv_ap
th_av = reference_simulation.calculate("taxe_habitation", "2021")
exo_th = reference_simulation.calculate("exonere_taxe_habitation", "2021")
th_av
# th_ap = reform_simulation.calculate("taxe_habitation", "2021")
# taux_degrev_th_ap = reform_simulation.calculate("degrevement_taxe_habitation", "2018")
# s_brut_ap = reform_simulation.calculate("salaire_de_base","2018-01")
# cot_soc_ap = reform_simulation.calculate("cotisations_salariales","2018-12")
# cot_cho_ap = reform_simulation.calculate("chomage_salarie","2019-01")
# cot_cho_ap_oct = reform_simulation.calculate("chomage_salarie","2018-11")
# csg_ap = reform_simulation.calculate("csg","2018")
# csg_ded_ap = reform_simulation.calculate("csg_deductible_salaire","2018-01")
# crds_ap  = reform_simulation.calculate("crds","2018")
# net_ap = reform_simulation.calculate('salaire_net','2018-12')
# rfr_ap = reform_simulation.calculate('rfr','2018')
# ir_ap = reform_simulation.calculate('impots_directs', '2019')
# ir_av = reference_simulation.calculate('impots_directs', '2019')
# ir_ap = reform_simulation.calculate('salaire_imposable', '2018-01')
# ir_av = reference_simulation.calculate('salaire_imposable', '2018-01')
# presta_ap = reform_simulation.calculate("prestations_sociales","2018")
# famille_ap = reform_simulation.calculate("prestations_familiales","2018")
# minima_ap = reform_simulation.calculate("minima_sociaux","2018")
# al_ap = reform_simulation.calculate("aide_logement","2018-12")

# ppa_ap = reform_simulation.calculate("ppa","2018-10")
# ppa_av = reference_simulation.calculate("ppa","2018-10")
# ppa_ap = reform_simulation.calculate("ppa","2020-10")

# sur_bonification_ppa_ap = reform_simulation.calculate("ppa_bonification","2018-12")
# rd_ap = reform_simulation.calculate('revenu_disponible', '2018')/12




# Variables in the counterfactual situation
# th_av = reference_simulation.calculate("cotisation_taxe_habitation", "2017")
# taux_degrev_th_av = reference_simulation.calculate("degrevement_taxe_habitation", "2018")
# s_brut_av = reference_simulation.calculate("salaire_de_base","2018-01")
# cot_soc_av = reference_simulation.calculate("cotisations_salariales","2018-12")
# cot_cho_av = reference_simulation.calculate("chomage_salarie","2018-01")
# csg_av = reference_simulation.calculate("csg","2018")
# csg_ded_av = reference_simulation.calculate("csg_deductible_salaire","2018-01")
# crds_av  = reference_simulation.calculate("crds","2018")
# net_av = reference_simulation.calculate('salaire_net','2018-12')
# rfr_av = reference_simulation.calculate('rfr','2018')
# ir_av = reference_simulation.calculate('irpp', '2018')
# presta_av = reference_simulation.calculate("prestations_sociales","2018")
# famille_av = reference_simulation.calculate("prestations_familiales","2018")
# minima_av = reference_simulation.calculate("minima_sociaux","2018")
# al_av = reference_simulation.calculate("aide_logement","2018-12")
# ppa_av = reference_simulation.calculate("ppa","2018-11")


