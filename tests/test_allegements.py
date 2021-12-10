from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france import FranceTaxBenefitSystem
# from openfisca_core.model_api import ADD

tbs = FranceTaxBenefitSystem()

sb = SimulationBuilder()
simulation = sb.build_default_simulation(tbs, count=1)
simulation.trace = True
# Cas test de l'ASI après la réforme de 2020 - Célibataire (7)


#month = '2021-10'
#smic_proratise = simulation.calculate('smic_proratise', month)
#print("smic_proratise :", smic_proratise)  # 1554.6174

#year = '2021'
#smic_proratise_annuel = simulation.calculate_add('smic_proratise', '2021')
#print("smic_proratise_annuel :", smic_proratise_annuel)  # 1554.6174 * 12

period = '2021-12'
simulation.set_input('age', period,  [54])
simulation.set_input('asi_aspa_base_ressources_individu',  period, [800])
simulation.set_input('asi_eligibilite', period, [True])
#simulation.set_input('aspa_eligibilite', period, [True])

montant_asi = simulation.calculate_add('asi', period) # expected 300€
simulation.tracer.print_computation_log()

#allegement_cotisation_maladie_mode_recouvrement=simulation.calculate_add('allegement_cotisation_maladie_mode_recouvrement', period)
#cotiz_mmid = simulation.calculate_add()
print("ASI", montant_asi)  # 93.27 * 12  # 0.06 * 1554.58 * 9 mois de salaire
#print('allegement_cotisation_maladie_mode_recouvrement: ', allegement_cotisation_maladie_mode_recouvrement)
