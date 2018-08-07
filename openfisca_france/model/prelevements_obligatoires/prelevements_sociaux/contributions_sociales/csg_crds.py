# -*- coding: utf-8 -*-

from __future__ import division
import logging
from openfisca_france.model.base import *  # noqa analysis:ignore

log = logging.getLogger(__name__)


class csg(Variable):
    value_type = float
    entity = Individu
    label = u"Contribution sociale généralisée"
    definition_period = YEAR

    def formula(individu, period):
        csg_imposable_salaire = individu('csg_imposable_salaire', period, options = [ADD])
        csg_deductible_salaire = individu('csg_deductible_salaire', period, options = [ADD])
        csg_imposable_chomage = individu('csg_imposable_chomage', period, options = [ADD])
        csg_deductible_chomage = individu('csg_deductible_chomage', period, options = [ADD])
        csg_imposable_retraite = individu('csg_imposable_retraite', period, options = [ADD])
        csg_deductible_retraite = individu('csg_deductible_retraite', period, options = [ADD])
        # CSG sur revenus du capital, définie à l'échelle du foyer fiscal, mais projetée sur le déclarant principal
        csg_revenus_capital = individu.foyer_fiscal('csg_revenus_capital', period)
        csg_revenus_capital_projetee = csg_revenus_capital * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return (
            csg_imposable_salaire
            + csg_deductible_salaire
            + csg_imposable_chomage
            + csg_deductible_chomage
            + csg_imposable_retraite
            + csg_deductible_retraite
            + csg_revenus_capital_projetee
            )

class crds(Variable):
    value_type = float
    entity = Individu
    label = u"Contributions au remboursement de la dette sociale"
    definition_period = YEAR

    def formula(individu, period):
        # CRDS sur revenus individuels
        crds_salaire = individu('crds_salaire', period, options = [ADD])
        crds_retraite = individu('crds_retraite', period, options = [ADD])
        crds_chomage = individu('crds_chomage', period, options = [ADD])
        crds_individu = crds_salaire + crds_retraite + crds_chomage
        # CRDS sur revenus de la famille, projetés seulement sur la première personne
        crds_pfam = individu.famille('crds_pfam', period)
        crds_logement = individu.famille('crds_logement', period, options = [ADD])
        crds_mini = individu.famille('crds_mini', period, options = [ADD])
        crds_famille = crds_pfam + crds_logement + crds_mini
        crds_famille_projetes = crds_famille * individu.has_role(Famille.DEMANDEUR)
        # CRDS sur revenus du capital, définie à l'échelle du foyer fiscal, mais projetée sur le déclarant principal
        crds_revenus_capital = individu.foyer_fiscal('crds_revenus_capital', period)
        crds_revenus_capital_projetee = crds_revenus_capital * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        return crds_individu + crds_famille_projetes + crds_revenus_capital_projetee

