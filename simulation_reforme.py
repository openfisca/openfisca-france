exit()
python

import numpy as np
import pandas as pd
import json

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


def inverse_prive(x):
    pss = 3269
    seuil_1 = pss*(1-0.2221)
    seuil_2 = pss*(1-0.2221) + (3*pss-pss)*(1-0.2041)
    seuil_3 = pss*(1-0.2221) + (3*pss-pss)*(1-0.2041) + (4*pss-3*pss)*(1-0.1141)

    if x < seuil_1:
        res = x/(1-0.2221)
    elif (x < seuil_2):
        res = seuil_1/(1-0.2221) + (x-seuil_1)/(1-0.2041)
    elif x < seuil_3:
        res = seuil_1/(1-0.2221) + (seuil_2-seuil_1)/(1-0.2041) + (x-seuil_2)/(1-0.1141)
    else:
        res = seuil_1/(1-0.2221) + (seuil_2-seuil_1)/(1-0.2041) + (seuil_3-seuil_2)/(1-0.1141) + (x-seuil_3)/(1-0.0901)
    return res

def inverse_fonctionnaire(x):
    if x < 258.072882:
        res = x/(1-0.1056-0.0005-0.9825*0.08-0.01*(1-0.1056))-3.13*(1-0.9825*0.08)
    elif (x < 1166):
        res = x/(1.01*(1-0.9825*0.08)-0.1056-0.0005)
    elif x < 10664.39332:#seuil à 4 pss pour la CSG
        res = x/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005)
    elif x < 11498.8564:
        res = 10664.39332/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005) + (x-10664.39332)/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005)
    else:
        res = 10664.39332/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005) + (11498.8564-10664.39332)/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005) + (x-11498.8564)/(1.01*(1-0.08)-0.1056-0.0005)
    return res

def inverse_salaire(x,statut):
    if statut == "public_titulaire_etat":
        res = inverse_fonctionnaire(x)
    elif statut == "prive_non_cadre":
        res = inverse_prive(x)
return res

    
def inverse_chomage(x):
    res = x/(1-0.07)
    return res

def inverse_retraite(x):
    res = x/(1-0.074)
    return res

def init_profile(scenario):
    scenario.init_single_entity(
        period = 'year:2017:6',
        parent1 = dict(
            age = 40,
            chomage_brut = 500*12*6,
            # categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
            # taux_incapacite = 0.8,
            statut_marital = 2,
            ),
        # parent2 = dict(
        #     age = 70,
        #     retraite_brute = 2074*12*6,
        #     # categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
        #     statut_marital = 1,
        #     ),
        # enfants = [
        # dict(age = 9),
        # dict(age = 10),
        # dict(age = 10),
        # dict(age = 14),
        # ],

        menage = dict(loyer = 5000*6, # Annual basis
            cotisation_taxe_habitation = -427.*6,
            statut_occupation_logement = 3,
            zone_apl = 1,

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


# brut = reference_simulation.calculate('chomage_brut', '2017-12')
# net = reference_simulation.calculate('chomage_net', '2017-12')
# casa = reference_simulation.calculate('casa', '2017-12')
# crds = reference_simulation.calculate('crds_chomage', '2017-12')
# csg_ded = reference_simulation.calculate('csg_deductible_chomage', '2017-12')
# csg_nod = reference_simulation.calculate('csg_imposable_chomage', '2017-12')
# # rfr = reference_simulation.calculate('rfr', '2018')
# brut
# net
# casa
# crds
# csg_ded
# csg_nod
# rfr/12/0.9
# 1-net/brut



cotsoc_2018 = reference_simulation.calculate('cotisations_salariales', '2018-11')[0] - reform_simulation.calculate('cotisations_salariales', '2018-11')[0]
cotsoc_2019 = reference_simulation.calculate('cotisations_salariales', '2019-11')[0] - reform_simulation.calculate('cotisations_salariales', '2019-11')[0]
cotsoc_2020 = reference_simulation.calculate('cotisations_salariales', '2020-11')[0] - reform_simulation.calculate('cotisations_salariales', '2020-11')[0]
cotsoc_2021 = reference_simulation.calculate('cotisations_salariales', '2021-11')[0] - reform_simulation.calculate('cotisations_salariales', '2021-11')[0]
cotsoc_2022 = reference_simulation.calculate('cotisations_salariales', '2022-11')[0] - reform_simulation.calculate('cotisations_salariales', '2022-11')[0]

csg_2018 = (reference_simulation.calculate('csg', '2018')[0] - reform_simulation.calculate('csg', '2018')[0])/12
csg_2019 = (reference_simulation.calculate('csg', '2019')[0] - reform_simulation.calculate('csg', '2019')[0])/12
csg_2020 = (reference_simulation.calculate('csg', '2020')[0] - reform_simulation.calculate('csg', '2020')[0])/12
csg_2021 = (reference_simulation.calculate('csg', '2021')[0] - reform_simulation.calculate('csg', '2021')[0])/12
csg_2022 = (reference_simulation.calculate('csg', '2022')[0] - reform_simulation.calculate('csg', '2022')[0])/12

ir_2018 = (reference_simulation.calculate('irpp', '2018')[0] - reform_simulation.calculate('irpp', '2018')[0])/12
ir_2019 = (reference_simulation.calculate('irpp', '2019')[0] - reform_simulation.calculate('irpp', '2019')[0])/12
ir_2020 = (reference_simulation.calculate('irpp', '2020')[0] - reform_simulation.calculate('irpp', '2020')[0])/12
ir_2021 = (reference_simulation.calculate('irpp', '2021')[0] - reform_simulation.calculate('irpp', '2021')[0])/12
ir_2022 = (reference_simulation.calculate('irpp', '2022')[0] - reform_simulation.calculate('irpp', '2022')[0])/12

# ppa_2018_1 = reference_simulation.calculate('ppa', '2018-04')[0] - reform_simulation.calculate('ppa', '2018-04')[0]
ppa_2018 = reference_simulation.calculate('ppa', '2018-12')[0] - reform_simulation.calculate('ppa', '2018-12')[0]
ppa_2019 = reference_simulation.calculate('ppa', '2019-12')[0] - reform_simulation.calculate('ppa', '2019-12')[0]
ppa_2020 = reference_simulation.calculate('ppa', '2020-12')[0] - reform_simulation.calculate('ppa', '2020-12')[0]
ppa_2021 = reference_simulation.calculate('ppa', '2021-12')[0] - reform_simulation.calculate('ppa', '2021-12')[0]
ppa_2022 = reference_simulation.calculate('ppa', '2022-12')[0] - reform_simulation.calculate('ppa', '2022-12')[0]

# mv_2018_1 = reference_simulation.calculate('aspa', '2018-04')[0] - reform_simulation.calculate('aspa', '2018-04')[0]
mv_2018 = reference_simulation.calculate('aspa', '2018-12')[0] - reform_simulation.calculate('aspa', '2018-12')[0]
mv_2019 = reference_simulation.calculate('aspa', '2019-12')[0] - reform_simulation.calculate('aspa', '2019-12')[0]
mv_2020 = reference_simulation.calculate('aspa', '2020-12')[0] - reform_simulation.calculate('aspa', '2020-12')[0]
mv_2021 = reference_simulation.calculate('aspa', '2021-12')[0] - reform_simulation.calculate('aspa', '2021-12')[0]
mv_2022 = reference_simulation.calculate('aspa', '2022-12')[0] - reform_simulation.calculate('aspa', '2022-12')[0]

apl_2018 = reference_simulation.calculate('apl', '2018-10')[0] - reform_simulation.calculate('apl', '2018-08')[0]
apl_2019 = reference_simulation.calculate('apl', '2019-12')[0] - reform_simulation.calculate('apl', '2019-09')[0]
apl_2020 = reference_simulation.calculate('apl', '2020-12')[0] - reform_simulation.calculate('apl', '2020-12')[0]
apl_2021 = reference_simulation.calculate('apl', '2021-12')[0] - reform_simulation.calculate('apl', '2021-12')[0]
apl_2022 = reference_simulation.calculate('apl', '2022-12')[0] - reform_simulation.calculate('apl', '2022-12')[0]

# aah_2018_1 = reference_simulation.calculate('aah', '2018-04')[0] - reform_simulation.calculate('aah', '2018-04')[0]
aah_2018 = reference_simulation.calculate('aah', '2018-12')[0] - reform_simulation.calculate('aah', '2018-12')[0]
aah_2019 = reference_simulation.calculate('aah', '2019-12')[0] - reform_simulation.calculate('aah', '2019-12')[0]
aah_2020 = reference_simulation.calculate('aah', '2020-12')[0] - reform_simulation.calculate('aah', '2020-12')[0]
aah_2021 = reference_simulation.calculate('aah', '2021-12')[0] - reform_simulation.calculate('aah', '2021-12')[0]
aah_2022 = reference_simulation.calculate('aah', '2022-12')[0] - reform_simulation.calculate('aah', '2022-12')[0]

th_2018 = (reference_simulation.calculate('taxe_habitation', '2018')[0] - reform_simulation.calculate('taxe_habitation', '2018')[0])/12
th_2019 = (reference_simulation.calculate('taxe_habitation', '2019')[0] - reform_simulation.calculate('taxe_habitation', '2019')[0])/12
th_2020 = (reference_simulation.calculate('taxe_habitation', '2020')[0] - reform_simulation.calculate('taxe_habitation', '2020')[0])/12
th_2021 = (reference_simulation.calculate('taxe_habitation', '2021')[0] - reform_simulation.calculate('taxe_habitation', '2021')[0])/12
th_2022 = (reference_simulation.calculate('taxe_habitation', '2022')[0] - reform_simulation.calculate('taxe_habitation', '2022')[0])/12

gain_2018 = cotsoc_2018 + csg_2018 + ir_2018 + ppa_2018 + mv_2018 + th_2018 
gain_2019 = cotsoc_2019 + csg_2019 + ir_2019 + ppa_2019 + mv_2019 + th_2019 
gain_2020 = cotsoc_2020 + csg_2020 + ir_2020 + ppa_2020 + mv_2020 + th_2020 
gain_2021 = cotsoc_2021 + csg_2021 + ir_2021 + ppa_2021 + mv_2021 + th_2021 
gain_2022 = cotsoc_2022 + csg_2022 + ir_2022 + ppa_2022 + mv_2022 + th_2022 


res = np.zeros((9, 5), dtype=float)
res[0] = np.round([cotsoc_2018,cotsoc_2019,cotsoc_2020,cotsoc_2021,cotsoc_2022])
res[1] = np.round([csg_2018,csg_2019,csg_2020,csg_2021,csg_2022])
res[2] = np.round([ir_2018,ir_2019,ir_2020,ir_2021,ir_2022])
res[3] = np.round([ppa_2018,ppa_2019,ppa_2020,ppa_2021,ppa_2022])
res[4] = np.round([mv_2018,mv_2019,mv_2020,mv_2021,mv_2022])
res[5] = np.round([apl_2018,apl_2019,apl_2020,apl_2021,apl_2022])
res[6] = np.round([aah_2018,aah_2019,aah_2020,aah_2021,aah_2022])
res[7] = np.round([th_2018,th_2019,th_2020,th_2021,th_2022])
res[8] = np.round([gain_2018,gain_2019,gain_2020,gain_2021,gain_2022])

res2 = -1*pd.DataFrame(res,index = ["cotsoc","csg","ir","prime_activite","minimum_vieillesse","apl","aah","taxe_habitation","total"],columns = range(2018,2023))
res2
with open("res.json", "w") as f:
  f.write(res2.to_json())
  
  
