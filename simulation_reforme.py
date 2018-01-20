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



def init_profile(scenario):
    scenario.init_single_entity(
        period = 'year:2016:7',
        parent1 = dict(
            age = 70,
            retraite_brute = 500*12*7,
            # categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
            # taux_incapacite = 0.8,
            statut_marital = 1,
            ),
        # parent2 = dict(
        #     age = 70,
        #     retraite_brute = 4166*0.5*12*7,
        #     # categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
        #     statut_marital = 1,
        #     ),
        # enfants = [
        # dict(age = 9),
        # dict(age = 10),
        # dict(age = 10),
        # dict(age = 14),
        # ],

        menage = dict(loyer = 5000*7, # Annual basis
            cotisation_taxe_habitation = -624*7,
            statut_occupation_logement = 5,
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

# reform_simulation.calculate('taux_csg_remplacement_2',"2016")
# reform_simulation.calculate('taux_csg_remplacement_2',"2017")
# reform_simulation.calculate('taux_csg_remplacement_2',"2018")
# reference_simulation.calculate('taux_csg_remplacement_2',"2016")
# reference_simulation.calculate('taux_csg_remplacement_2',"2017")
# reference_simulation.calculate('taux_csg_remplacement_2',"2018")

csg_2018 = (reference_simulation.calculate('wrapper_csg',"2018") - reform_simulation.calculate('wrapper_csg',"2018"))[0]
csg_2019 = (reference_simulation.calculate('wrapper_csg',"2019") - reform_simulation.calculate('wrapper_csg',"2019"))[0]
csg_2020 = (reference_simulation.calculate('wrapper_csg',"2020") - reform_simulation.calculate('wrapper_csg',"2020"))[0]
csg_2021 = (reference_simulation.calculate('wrapper_csg',"2021") - reform_simulation.calculate('wrapper_csg',"2021"))[0]
csg_2022 = (reference_simulation.calculate('wrapper_csg',"2022") - reform_simulation.calculate('wrapper_csg',"2022"))[0]

cotsoc_2018 = (reference_simulation.calculate('wrapper_cotisations_salariales','2018') - reform_simulation.calculate('wrapper_cotisations_salariales_2018','2018'))[0]
cotsoc_2019 = (reference_simulation.calculate('wrapper_cotisations_salariales','2019') - reform_simulation.calculate('wrapper_cotisations_salariales','2019'))[0]
cotsoc_2020 = (reference_simulation.calculate('wrapper_cotisations_salariales','2020') - reform_simulation.calculate('wrapper_cotisations_salariales','2020'))[0]
cotsoc_2021 = (reference_simulation.calculate('wrapper_cotisations_salariales','2021') - reform_simulation.calculate('wrapper_cotisations_salariales','2021'))[0]
cotsoc_2022 = (reference_simulation.calculate('wrapper_cotisations_salariales','2022') - reform_simulation.calculate('wrapper_cotisations_salariales','2022'))[0] 

ir_2018 = (reference_simulation.calculate('irpp', '2018') - reform_simulation.calculate('irpp', '2018'))[0]
ir_2019 = (reference_simulation.calculate('irpp', '2019') - reform_simulation.calculate('irpp', '2019'))[0]
ir_2020 = (reference_simulation.calculate('irpp', '2020') - reform_simulation.calculate('irpp', '2020'))[0]
ir_2021 = (reference_simulation.calculate('irpp', '2021') - reform_simulation.calculate('irpp', '2021'))[0]
ir_2022 = (reference_simulation.calculate('irpp', '2022') - reform_simulation.calculate('irpp', '2022'))[0]

ppa_2018 = (reference_simulation.calculate('wrapper_ppa', '2018') - reform_simulation.calculate('wrapper_ppa', '2018'))[0]
ppa_2019 = (reference_simulation.calculate('wrapper_ppa', '2019') - reform_simulation.calculate('wrapper_ppa', '2019'))[0]
ppa_2020 = (reference_simulation.calculate('wrapper_ppa', '2020') - reform_simulation.calculate('wrapper_ppa', '2020'))[0]
ppa_2021 = (reference_simulation.calculate('wrapper_ppa', '2021') - reform_simulation.calculate('wrapper_ppa', '2021'))[0]
ppa_2022 = (reference_simulation.calculate('wrapper_ppa', '2022') - reform_simulation.calculate('wrapper_ppa', '2022'))[0]

mv_2018 = (reference_simulation.calculate('wrapper_aspa', '2018') - reform_simulation.calculate('wrapper_aspa', '2018'))[0]
mv_2019 = (reference_simulation.calculate('wrapper_aspa', '2019') - reform_simulation.calculate('wrapper_aspa', '2019'))[0]
mv_2020 = (reference_simulation.calculate('wrapper_aspa', '2020') - reform_simulation.calculate('wrapper_aspa', '2020'))[0]
mv_2021 = (reference_simulation.calculate('wrapper_aspa', '2021') - reform_simulation.calculate('wrapper_aspa', '2021'))[0]
mv_2022 = (reference_simulation.calculate('wrapper_aspa', '2022') - reform_simulation.calculate('wrapper_aspa', '2022'))[0]

apl_2018 = (reference_simulation.calculate('wrapper_apl', '2018') - reform_simulation.calculate('wrapper_apl', '2018'))[0]
apl_2019 = (reference_simulation.calculate('wrapper_apl', '2019') - reform_simulation.calculate('wrapper_apl', '2019'))[0]
apl_2020 = (reference_simulation.calculate('wrapper_apl', '2020') - reform_simulation.calculate('wrapper_apl', '2020'))[0]
apl_2021 = (reference_simulation.calculate('wrapper_apl', '2021') - reform_simulation.calculate('wrapper_apl', '2021'))[0]
apl_2022 = (reference_simulation.calculate('wrapper_apl', '2022') - reform_simulation.calculate('wrapper_apl', '2022'))[0]

aah_2018 = (reference_simulation.calculate('wrapper_aah', '2018') - reform_simulation.calculate('wrapper_aah', '2018'))[0]
aah_2019 = (reference_simulation.calculate('wrapper_aah', '2019') - reform_simulation.calculate('wrapper_aah', '2019'))[0]
aah_2020 = (reference_simulation.calculate('wrapper_aah', '2020') - reform_simulation.calculate('wrapper_aah', '2020'))[0]
aah_2021 = (reference_simulation.calculate('wrapper_aah', '2021') - reform_simulation.calculate('wrapper_aah', '2021'))[0]
aah_2022 = (reference_simulation.calculate('wrapper_aah', '2022') - reform_simulation.calculate('wrapper_aah', '2022'))[0]

th_2018 = (reference_simulation.calculate('taxe_habitation', '2018') - reform_simulation.calculate('taxe_habitation', '2018'))[0]
th_2019 = (reference_simulation.calculate('taxe_habitation', '2019') - reform_simulation.calculate('taxe_habitation', '2019'))[0]
th_2020 = (reference_simulation.calculate('taxe_habitation', '2020') - reform_simulation.calculate('taxe_habitation', '2020'))[0]
th_2021 = (reference_simulation.calculate('taxe_habitation', '2021') - reform_simulation.calculate('taxe_habitation', '2021'))[0]
th_2022 = (reference_simulation.calculate('taxe_habitation', '2022') - reform_simulation.calculate('taxe_habitation', '2022'))[0]

gain_2018 = cotsoc_2018 + csg_2018 + ir_2018 + ppa_2018 + mv_2018 + th_2018 + aah_2018 + apl_2018
gain_2019 = cotsoc_2019 + csg_2019 + ir_2019 + ppa_2019 + mv_2019 + th_2019 + aah_2019 + apl_2019
gain_2020 = cotsoc_2020 + csg_2020 + ir_2020 + ppa_2020 + mv_2020 + th_2020 + aah_2020 + apl_2020
gain_2021 = cotsoc_2021 + csg_2021 + ir_2021 + ppa_2021 + mv_2021 + th_2021 + aah_2021 + apl_2021
gain_2022 = cotsoc_2022 + csg_2022 + ir_2022 + ppa_2022 + mv_2022 + th_2022 + aah_2022 + apl_2022


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

res2 = -1*pd.DataFrame(res,index = ["cotsoc","csg","ir","prime_activite","minimum_vieillesse","apl","aah","taxe_habitation","total"],columns = range(2018,2023))/12
res2
# with open("res.json", "w") as f:
#   f.write(res2.to_json())
  
res2.to_csv('res.csv')
  
  
