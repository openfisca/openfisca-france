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
            age = 30,
            salaire_de_base = 2599*12*6,
            statut_marital = 1
            ),
        parent2 = dict(
            age = 40,
            salaire_de_base = 2599*12*6,
            statut_marital = 1
            ),
        # enfants = [
        #     dict(age = 9),
        #     dict(age = 10),
            # dict(age = 10),
            # dict(age = 14),
            # ],
            
        menage = dict(loyer = 5000, # Annual basis
            # statut_occupation_logement = 3,
            cotisation_taxe_habitation = -621.00*6,
            ),
        # foyer_fiscal = dict(statut_marital = 1),
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

rd_av_2018 = reference_simulation.calculate('revenu_disponible', '2018')/12
rd_ap_2018 = reform_simulation.calculate('revenu_disponible', '2018')/12
gain_2018 = -(rd_av_2018-rd_ap_2018)

rd_av_2019 = reference_simulation.calculate('revenu_disponible', '2019')/12
rd_ap_2019 = reform_simulation.calculate('revenu_disponible', '2019')/12
gain_2019 = -(rd_av_2019-rd_ap_2019)

print(gain_2018)
print(gain_2019)

# a exporter en JSON : gain_2018 et gain_2019


# Variables after reform
# cotis_th_ap = reform_simulation.calculate("taxe_habitation", "2019")
# th_ap = reform_simulation.calculate("taxe_habitation", "2018")
# th_ap = reform_simulation.calculate("cotisation_taxe_habitation", "2018")
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
# ir_ap = reform_simulation.calculate('irpp', '2018')
# ir_av = reference_simulation.calculate('irpp', '2018')
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


