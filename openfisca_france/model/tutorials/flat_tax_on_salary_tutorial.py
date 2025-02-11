from openfisca_france.model.base import *
#from openfisca_france.model.tutorials.salary_tutorial import salary

class flat_tax_on_salary(Variable):
    value_type = float
    entity = Individu
    #default_value = 0.
    definition_period = MONTH
    label = u"Individualized and monthly paid tax on salaries"

    def formula(individu, period):
        salary = individu('salary', period)
        return salary * 0.25
    

# class flat_tax_on_salary(Variable):
#     value_type = float
#     entity = Person
#     definition_period = MONTH
#     label = u"Individualized and monthly paid tax on salaries"

#     def formula(person, period):
#         salary = person('salary', period)
#         return salary * 0.25

if __name__ == "__main__":
    print("Exécution directe du module flat_tax_on_salary_tutorial.")
else:
    print("Module flat_tax_on_salary_tutorial importé.")

