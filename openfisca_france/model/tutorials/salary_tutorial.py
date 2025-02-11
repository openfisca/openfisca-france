from openfisca_france.model.base import *


class salary(Variable):
    value_type = float
    entity = Individu
    # defaut_value = 0
    label = u"Salary earned by a person for a given month"
    definition_period = MONTH



if __name__ == "__main__":
    print("Exécution directe du module salary_tutorial.")
else:
    print("Module salary_tutorial importé.")