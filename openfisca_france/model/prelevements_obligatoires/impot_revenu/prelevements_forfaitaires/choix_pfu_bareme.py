import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)

# Choix prélèvement forfaitaire unique (pfu) ou imposition au barème pour les revenus de capitaux mobiliers et gains de cession de valeurs mobilières


class f2op(Variable):
    cerfa_field = '2OP'
    value_type = bool
    entity = FoyerFiscal
    label = 'Le foyer fiscal choisit l imposition au barème plutôt que le pfu si il coche la case 2op'
    definition_period = YEAR
