# When using openfisca for a large population, having too many variables in cache make openfisca performances drop.
# The following variables are intermadiate results and do not need to be cached in those usecases.

cache_blacklist = set([
    'aide_logement_loyer_retenu',
    'aide_logement_charges',
    'aide_logement_R0',
    'aide_logement_taux_famille',
    'aide_logement_taux_loyer',
    'aide_logement_participation_personnelle',
    'aide_logement_loyer_seuil_degressivite',
    'aide_logement_loyer_seuil_suppression',
    'aide_logement_montant_brut_avant_degressivite',
])
