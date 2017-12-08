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
        period = 2018,
        parent1 = dict(
            age = 40,
            salaire_de_base = 5000*12,
            ),
            
        menage = dict(loyer = 5000, # Annual basis
            statut_occupation_logement = 3,
            taxe_habitation = -600,
            ),
        )
    return scenario

##################################
# Computation with reform reforme
##################################
#Indicate that you want to perfom the reform on this scenario
reform_scenario = init_profile(reform.new_scenario())

#Simulate the reform
reform_simulation = reform_scenario.new_simulation()


# Variables after reform
taux_degrev_th_ap = reform_simulation.calculate("degrevement_taxe_habitation", "2018")
s_brut_ap = reform_simulation.calculate("salaire_de_base","2018-01")
cot_soc_ap = reform_simulation.calculate("cotisations_salariales","2018-01")
cot_cho_ap = reform_simulation.calculate("chomage_salarie","2018-01")
cot_cho_ap_oct = reform_simulation.calculate("chomage_salarie","2018-11")
csg_ap = reform_simulation.calculate("csg","2018")
csg_ded_ap = reform_simulation.calculate("csg_deductible_salaire","2018-01")
crds_ap  = reform_simulation.calculate("crds","2018")
net_ap = reform_simulation.calculate('revenu_net','2018')
ir_ap = reform_simulation.calculate('irpp', '2018')
presta_ap = reform_simulation.calculate("prestations_sociales","2018")
famille_ap = reform_simulation.calculate("prestations_familiales","2018")
minima_ap = reform_simulation.calculate("minima_sociaux","2018")
al_ap = reform_simulation.calculate("aide_logement","2018-12")
ppa_ap = reform_simulation.calculate("ppa","2018-12")
rd_ap = reform_simulation.calculate('revenu_disponible', '2018')


###################################
# Computation of th ecounterfactual
###################################
#Indicate that you want to perfom the standard system on this scenario
reference_scenario = init_profile(tax_benefit_system.new_scenario())

#Simulate the standard scenario
reference_simulation = reference_scenario.new_simulation()

# Variables in the counterfactual situation
taux_degrev_th_av = reference_simulation.calculate("degrevement_taxe_habitation", "2018")
s_brut_av = reference_simulation.calculate("salaire_de_base","2018-01")
cot_soc_av = reference_simulation.calculate("cotisations_salariales","2018-01")
cot_cho_av = reference_simulation.calculate("chomage_salarie","2018-01")
csg_av = reference_simulation.calculate("csg","2018")
csg_ded_av = reference_simulation.calculate("csg_deductible_salaire","2018-01")
crds_av  = reference_simulation.calculate("crds","2018")
net_av = reference_simulation.calculate('revenu_net','2018')
ir_av = reference_simulation.calculate('irpp', '2018')
presta_av = reference_simulation.calculate("prestations_sociales","2018")
famille_av = reference_simulation.calculate("prestations_familiales","2018")
minima_av = reference_simulation.calculate("minima_sociaux","2018")
al_av = reference_simulation.calculate("aide_logement","2018-12")
ppa_av = reference_simulation.calculate("ppa","2018-12")
rd_av = reference_simulation.calculate('revenu_disponible', '2018')



print("sal_brut")
print(s_brut_av)
print("cotsoc")
print(cot_soc_av)
print(cot_soc_ap)
print("cot_cho")
print(cot_cho_av)
print(cot_cho_ap)
print(cot_cho_ap_oct)
print("csg")
print(csg_av)
print(csg_ap)
print("crds")
print(crds_av)
print(crds_ap)
print("net")
print(net_av)
print(net_ap)
print("ir")
print(ir_av)
print(ir_ap)
print("prestations_sociales")
print(presta_av)
print(presta_ap)
print("Allocations familiales")
print(famille_av)
print(famille_ap)
print("minima sociaux")
print(minima_av)
print(minima_ap)
print("aides au logement")
print(al_av)
print(al_ap)
print("PA")
print(ppa_av)
print(ppa_ap)
print("revenu_disponible")
print(rd_av)
print(rd_ap) 
print("TH")
print(taux_degrev_th_ap)
print(taux_degrev_th_av)

# check_av_1 = s_brut_av + cot_soc_av + (csg_av-csg_ded_av*12 + crds_av -net_av)/12
# check_av_1
# s_brut_av-net_av/12
# cot_soc_av + (csg_av+crds_av)/12
# check_av_2 = net_av + presta_av - rd_av
# check_av_2
# 
# check_ap = net_av + presta_av - rd_av
# check_ap
# # 
# print(reform.parameters.prelevements_sociaux.cotisations_sociales.chomage.salarie[0].rate)
# print(reform.parameters.prelevements_sociaux.contributions.csg.activite.deductible.taux)
