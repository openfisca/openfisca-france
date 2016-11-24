
# coding: utf-8

# # Getting started

# This notebook illustrates the [getting started](http://doc.openfisca.fr/getting-started.html) section of the documentation.
# 
# We explore three 

# ## Calculate a variable

# Do some imports

# In[79]:

from openfisca_france import FranceTaxBenefitSystem


# Initialize the tax and benefit system of France

# In[80]:

tax_benefit_system = FranceTaxBenefitSystem()


# Create a scenario

# In[81]:

scenario = tax_benefit_system.new_scenario()


# Initialize a test case in the scenario (with simplified syntax):
# here we have one parent and two children.

# In[82]:

scenario.init_single_entity(
    period = 2015,
    parent1 = dict(
        age = 30,
        salaire_de_base = 20000,
        ),
    enfants = [
        dict(age = 12),
        dict(age = 18),
        ],
    )


# Create a simulation

# In[83]:

simulation = scenario.new_simulation()


# Calculate a variable : `"af"` (allocations familiales) for example.

# In[84]:

simulation.calculate('af', '2015-01')


# ## Test the impact of a reform

# Import the extension corresponding to a reform of your concern.
# 
# Here we choose the fiscal reform of Landais, Piketty and Saez on the income tax (http://www.revolution-fiscale.fr/la-reforme-proposee). 
# 
# It is already implemented in OpenFisca under the name `landais_piketty_saez` .

# In[85]:

from openfisca_france.reforms import landais_piketty_saez


# Create a modified version of the tax and benefit system, affected by the changes introduced by the reform

# In[86]:

reform = landais_piketty_saez.landais_piketty_saez(tax_benefit_system)


# Create the scenario you want to test.

# In[87]:

def init_profile(scenario):
    scenario.init_single_entity(
        period = '2013',
        parent1 = dict(
            age = 40,
            salaire_de_base = 50000,
            ),
        )
    return scenario


# With the reform

# In[88]:

#Indicate that you want to perfom the reform on this scenario
reform_scenario = init_profile(reform.new_scenario())

#Simulate the reform
reform_simulation = reform_scenario.new_simulation() 

# Choose the variable you want to calcul : here the disposable income, "revdisp"
reform_simulation.calculate('revdisp', '2013')


# Without the reform: the counterfactual

# In[89]:

#Indicate that you want to perfom the standard system on this scenario
reference_scenario = init_profile(tax_benefit_system.new_scenario())

#Simulate the standard scenario
reference_simulation = reference_scenario.new_simulation()

# Choose the variable you want to calcul
reference_simulation.calculate('revdisp', '2013')


# ## Trace the calculation of a variable
# 
# Thanks to the Trace tool you can see all the details of the variable calculation depending on the scenario you made.

# In[90]:

from openfisca_core import tools
print(tools.get_trace_tool_link(scenario, variables = ['irpp'], api_url = 'http://api.openfisca.fr', trace_tool_url =  'http://www.openfisca.fr/tools/trace'))

