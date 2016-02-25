# -*- coding: utf-8 -*-

from .caracteristiques_socio_demographiques import (  # noqa analysis:ignore
    demographie,
    logement,
    )

from . import (  # noqa analysis:ignore
    mesures,
    )

from .prelevements_obligatoires import(  # noqa analysis:ignore
    isf,
    taxe_habitation,
    )
from .prelevements_obligatoires.impot_revenu import (  # noqa analysis:ignore
    charges_deductibles,
    credits_impot,
    ir,
    plus_values_immobilieres,
    reductions_impot,
    variables_reductions_credits,
    )

from .prelevements_obligatoires.prelevements_sociaux.contributions_sociales import (  # noqa analysis:ignore
    activite,
    capital,
    remplacement,
    )

from .prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import (  # noqa analysis:ignore
    allegements,
    apprentissage,
    exonerations,
    # penalites,
    # remuneration_public,
    stage,
    travail_fonction_publique,
    travail_prive,
    travail_totaux,
    )

from .prelevements_obligatoires.prelevements_sociaux import taxes_salaires_main_oeuvre # noqa analysis:ignore

from .prestations import (  # noqa analysis:ignore
    aides_logement,
    education,
    )

from prestations.minima_sociaux import (  # noqa analysis:ignore
    aah,
    asi_aspa,
    ass,
    cmu,
    rsa,
    ppa,
    )

from prestations.prestations_familiales import (  # noqa analysis:ignore
    aeeh,
    af,
    ars,
    asf,
    paje,
    cf,
    )

from . import extensions

from revenus import autres

from revenus.activite import (  # noqa analysis:ignore
    non_salarie,
    salarie,
    )

from revenus.capital import (  # noqa analysis:ignore
    financier,
    foncier,
    plus_value,
    )

from revenus.remplacement import (  # noqa analysis:ignore
    chomage,
    retraite,
    indemnites_journalieres_securite_sociale,
    )
