from openfisca_france.model.base import *


class housing_tax(Variable):
    value_type = float
    entity = Menage
    definition_period = MONTH
    label = u"Tax paid by each household proportionnally to the size of its accommodation"

    def formula(household, period, legislation):
        accommodation_size = household('accomodation_size', period)
        housing_occupancy_status = household('housing_occupancy_status', period)
        HousingOccupancyStatus = housing_occupancy_status.possible_values  # "Import" the enum type. Careful: do not use python imports accross variables files: comparisons would not work!
        tenant = (housing_occupancy_status == HousingOccupancyStatus.tenant)
        owner = (housing_occupancy_status == HousingOccupancyStatus.owner)

        # The tax is applied only if the household owns or rents its main residency
        return (owner + tenant) * accommodation_size * 10