from openfisca_france import FranceTaxBenefitSystem 
tax_benefit_system = FranceTaxBenefitSystem() 
import pandas as pd
df_ags = pd.DataFrame()
ags_list = tax_benefit_system.parameters.prelevements_sociaux.cotisations_regime_assurance_chomage.ags.employeur.ags.brackets[0].rate.values_list
for ags in ags_list:
    df_ags = df_ags.append(ags.__dict__, ignore_index=True)
df_ags.head(2)