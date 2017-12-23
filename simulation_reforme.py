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
        period = 2017,
        parent1 = dict(
            age = 40,
            salaire_de_base = 1671*12,
            categorie_salarie = "prive_non_cadre", # prive_non_cadre ou public_titulaire_etat
            # taux_incapacite = ,
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
        menage = dict(loyer = 1000*12, # Annual basis
            # cotisation_taxe_habitation = -427.*6,
            statut_occupation_logement = 4,
            ),
        # foyer_fiscal= dict(taux_csg_remplacement_2 = 3),
        )
    return scenario


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
ppa = reference_simulation.famille("ppa", "2017-04")
ppa = reference_simulation.calculate("ppa_fictive",last_3_months,"2017-04")
# salaire_net = reference_simulation.calculate("revenu_net", "2018")/12
ppa
ppa_bonification = reference_simulation.calculate("ppa_fictive", "period.last_3_months","2018-01")

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

