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



# def inverse_salaire(x):
#     pss = 3269
#     seuil_1 = pss*(1-0.2221)
#     seuil_2 = pss*(1-0.2221) + (3*pss-pss)*(1-0.2041)
#     seuil_3 = pss*(1-0.2221) + (3*pss-pss)*(1-0.2041) + (4*pss-3*pss)*(1-0.1141)
#       
#     if x < seuil_1:
#         res = x/(1-0.2221)
#     elif (x < seuil_2):
#         res = seuil_1/(1-0.2221) + (x-seuil_1)/(1-0.2041)
#     elif x < seuil_3:
#         res = seuil_1/(1-0.2221) + (seuil_2-seuil_1)/(1-0.2041) + (x-seuil_2)/(1-0.1141)
#     else: 
#         res = seuil_1/(1-0.2221) + (seuil_2-seuil_1)/(1-0.2041) + (seuil_3-seuil_2)/(1-0.1141) + (x-seuil_3)/(1-0.0901)
#     return res
#     
# def inverse_fonctionnaire(x):
#     if x < 258.072882:
#         res = x/(1-0.1056-0.0005-0.9825*0.08-0.01*(1-0.1056))-3.13*(1-0.9825*0.08)
#     elif (x < 1166):
#         res = x/(1.01*(1-0.9825*0.08)-0.1056-0.0005)
#     elif x < 10664.39332:#seuil à 4 pss pour la CSG
#         res = x/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005)
#     elif x < 11498.8564:
#         res = 10664.39332/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005) + (x-10664.39332)/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005)
#     else:
#         res = 10664.39332/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005) + (11498.8564-10664.39332)/(1.01*(1-0.9825*0.08)-0.1056-(1-0.1056)*0.01-0.0005) + (x-11498.8564)/(1.01*(1-0.08)-0.1056-0.0005)
#     return res


def init_profile(scenario):
    scenario.init_single_entity(
        period = 'year:2017:6',
        parent1 = dict(
            age = 40,
            salaire_de_base = 1480*12*6,
            categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
            # taux_incapacite = ,
            statut_marital = 1,
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

        menage = dict(loyer = 1000*6, # Annual basis
            cotisation_taxe_habitation = -427.*6,
            statut_occupation_logement = 4,
            zone_apl = 2,

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


# résultats
# salaire_brut = reference_simulation.calculate("salaire_de_base", "2018-01")
# salaire_net = reference_simulation.calculate("salaire_net", "2018-01")
# indemnite_residence = reference_simulation.calculate("indemnite_residence", "2018-01")
# 
# rafp = reference_simulation.calculate("rafp_salarie", "2018-01")
# pension_civile = reference_simulation.calculate("pension_civile_salarie", "2018-01")
# contribution_exceptionnelle_solidarite = reference_simulation.calculate("contribution_exceptionnelle_solidarite", "2018-01")
# csg = reference_simulation.calculate("csg", "2018")/12
# csg = reference_simulation.calculate("csg", "2018")/12
# crds = reference_simulation.calculate("crds", "2018")/12
# 
# 
# aah_eligible = reference_simulation.calculate("aah_eligible", "2020-01")
# autonomie_financiere = reference_simulation.calculate("autonomie_financiere", "2020-01")
# nbptr = reference_simulation.calculate("nbptr", "2020")

ppa = reference_simulation.calculate("ppa", "2018-10")
ppa
al = reference_simulation.calculate("aide_logement", "2018-01")/12
al
ppa_bonification = reference_simulation.calculate("ppa_fictive", "period.last_3_months","2018-01")
salaire_net = reference_simulation.calculate("revenu_net", "2017")/12


apl = reform_simulation.calculate("apl", "2018-11")
montant_brut_al = reform_simulation.calculate("aide_logement_montant_brut_avant_degressivite", "2020-01")
csg_nimp = reference_simulation.calculate("csg_deductible_salaire", "2018-01")
assiette_abat = reference_simulation.calculate("assiette_csg_abattue", "2018-01")
assiette_non_abat = reference_simulation.calculate("assiette_csg_non_abattue", "2018-01")
assiette_abat/salaire_brut
assiette_non_abat/salaire_brut



salaire_brut
salaire_net
indemnite_residence
rafp
pension_civile
csg
crds
contribution_exceptionnelle_solidarite
cotis = pension_civile + csg + crds + contribution_exceptionnelle_solidarite + rafp
cotis
salaire_net
salaire_brut-(salaire_net-indemnite_residence)


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



cotsoc_2018_1 = reference_simulation.calculate('cotisations_salariales', '2018-04')[0] - reform_simulation.calculate('cotisations_salariales', '2018-04')[0]
cotsoc_2018_2 = reference_simulation.calculate('cotisations_salariales', '2018-11')[0] - reform_simulation.calculate('cotisations_salariales', '2018-11')[0]
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

ppa_2018_1 = reference_simulation.calculate('ppa', '2018-04')[0] - reform_simulation.calculate('ppa', '2018-04')[0]
ppa_2018_2 = reference_simulation.calculate('ppa', '2018-12')[0] - reform_simulation.calculate('ppa', '2018-12')[0]
ppa_2019 = reference_simulation.calculate('ppa', '2019-12')[0] - reform_simulation.calculate('ppa', '2019-12')[0]
ppa_2020 = reference_simulation.calculate('ppa', '2020-12')[0] - reform_simulation.calculate('ppa', '2020-12')[0]
ppa_2021 = reference_simulation.calculate('ppa', '2021-12')[0] - reform_simulation.calculate('ppa', '2021-12')[0]
ppa_2022 = reference_simulation.calculate('ppa', '2022-12')[0] - reform_simulation.calculate('ppa', '2022-12')[0]

mv_2018_1 = reference_simulation.calculate('aspa', '2018-04')[0] - reform_simulation.calculate('aspa', '2018-04')[0]
mv_2018_2 = reference_simulation.calculate('aspa', '2018-12')[0] - reform_simulation.calculate('aspa', '2018-12')[0]
mv_2019 = reference_simulation.calculate('aspa', '2019-12')[0] - reform_simulation.calculate('aspa', '2019-12')[0]
mv_2020 = reference_simulation.calculate('aspa', '2020-12')[0] - reform_simulation.calculate('aspa', '2020-12')[0]
mv_2021 = reference_simulation.calculate('aspa', '2021-12')[0] - reform_simulation.calculate('aspa', '2021-12')[0]
mv_2022 = reference_simulation.calculate('aspa', '2022-12')[0] - reform_simulation.calculate('aspa', '2022-12')[0]

aah_2018_1 = reference_simulation.calculate('aah', '2018-04')[0] - reform_simulation.calculate('aah', '2018-04')[0]
aah_2018_2 = reference_simulation.calculate('aah', '2018-12')[0] - reform_simulation.calculate('aah', '2018-12')[0]
aah_2019 = reference_simulation.calculate('aah', '2019-12')[0] - reform_simulation.calculate('aah', '2019-12')[0]
aah_2020 = reference_simulation.calculate('aah', '2020-12')[0] - reform_simulation.calculate('aah', '2020-12')[0]
aah_2021 = reference_simulation.calculate('aah', '2021-12')[0] - reform_simulation.calculate('aah', '2021-12')[0]
aah_2022 = reference_simulation.calculate('aah', '2022-12')[0] - reform_simulation.calculate('aah', '2022-12')[0]

th_2018 = (reference_simulation.calculate('taxe_habitation', '2018')[0] - reform_simulation.calculate('taxe_habitation', '2018')[0])/12
th_2019 = (reference_simulation.calculate('taxe_habitation', '2019')[0] - reform_simulation.calculate('taxe_habitation', '2019')[0])/12
th_2020 = (reference_simulation.calculate('taxe_habitation', '2020')[0] - reform_simulation.calculate('taxe_habitation', '2020')[0])/12
th_2021 = (reference_simulation.calculate('taxe_habitation', '2021')[0] - reform_simulation.calculate('taxe_habitation', '2021')[0])/12
th_2022 = (reference_simulation.calculate('taxe_habitation', '2022')[0] - reform_simulation.calculate('taxe_habitation', '2022')[0])/12

gain_2018_1 = cotsoc_2018_1 + csg_2018 + ir_2018 + ppa_2018_1 + mv_2018_1 + th_2018 
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
res[5] = np.round([0.,0.,0.,0.,0.])
res[6] = np.round([aah_2018,aah_2018,aah_2018,aah_2018,aah_2018])
res[7] = np.round([th_2018,th_2019,th_2020,th_2021,th_2022])
res[8] = np.round([gain_2018,gain_2019,gain_2020,gain_2021,gain_2022])

res2 = pd.DataFrame(res,index = ["cotsoc","csg","ir","prime_activite","minimum_vieillesse","paje","aah","taxe_habitation","total"],columns = range(2018,2023))

with open("res.json", "w") as f:
  f.write(res2.to_json())
  
  




# # a exporter en JSON : gain_2018 et gain_2019
# 
# Tests pour voir sir la bascule de cotisation CSG est bien faite.
print(reform_simulation.calculate("salaire_net","2018-12")-reference_simulation.calculate("salaire_net","2018-12"))
print(reform_simulation.calculate("salaire_net","2019-01")-reference_simulation.calculate("salaire_net","2019-01"))
print(reform_simulation.calculate("salaire_net","2020-01")-reference_simulation.calculate("salaire_net","2020-01"))
print(reform_simulation.calculate("salaire_net","2021-01")-reference_simulation.calculate("salaire_net","2021-01"))
print(reform_simulation.calculate("salaire_net","2022-01")-reference_simulation.calculate("salaire_net","2022-01"))

# Tests pour voir si la PPA est bien revalorisée
print(reform_simulation.calculate("ppa","2018-12")-reference_simulation.calculate("ppa","2018-12"))
print(reform_simulation.calculate("ppa","2019-12")-reference_simulation.calculate("ppa","2019-12"))
print(reform_simulation.calculate("ppa","2020-01")-reference_simulation.calculate("ppa","2020-01"))
print(reform_simulation.calculate("ppa","2021-01")-reference_simulation.calculate("ppa","2021-01"))
print(reform_simulation.calculate("ppa","2022-01")-reference_simulation.calculate("ppa","2022-01"))


