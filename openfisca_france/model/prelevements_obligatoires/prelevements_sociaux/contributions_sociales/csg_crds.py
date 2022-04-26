import logging
from openfisca_france.model.base import *

log = logging.getLogger(__name__)


class csg(Variable):
    value_type = float
    entity = Individu
    label = 'Contribution sociale généralisée'
    definition_period = YEAR

    def formula(individu, period):
        csg_imposable_salaire = individu('csg_imposable_salaire', period, options = [ADD])
        csg_deductible_salaire = individu('csg_deductible_salaire', period, options = [ADD])
        csg_imposable_chomage = individu('csg_imposable_chomage', period, options = [ADD])
        csg_deductible_chomage = individu('csg_deductible_chomage', period, options = [ADD])
        csg_imposable_retraite = individu('csg_imposable_retraite', period, options = [ADD])
        csg_deductible_retraite = individu('csg_deductible_retraite', period, options = [ADD])
        csg_imposable_non_salarie = individu('csg_imposable_non_salarie', period, options = [ADD])
        csg_deductible_non_salarie = individu('csg_deductible_non_salarie', period, options = [ADD])
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
            + csg_imposable_non_salarie
            + csg_deductible_non_salarie
            + csg_revenus_capital_projetee
            )

    # TODO: manque CSG sur IJ et pré-retraites


class crds(Variable):
    value_type = float
    entity = Individu
    label = 'Contributions au remboursement de la dette sociale'
    reference = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000190291/2021-10-06/'
    definition_period = YEAR

    def formula(individu, period):
        # CRDS sur revenus individuels
        crds_salaire = individu('crds_salaire', period, options = [ADD])
        crds_retraite = individu('crds_retraite', period, options = [ADD])
        crds_chomage = individu('crds_chomage', period, options = [ADD])
        crds_non_salarie = individu('crds_non_salarie', period, options = [ADD])
        crds_individu = crds_salaire + crds_retraite + crds_chomage + crds_non_salarie
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


class crds_hors_prestations(Variable):
    value_type = float
    entity = Individu
    label = 'Contributions au remboursement de la dette sociale (hors celles portant sur les prestations sociales)'
    definition_period = YEAR

    def formula(individu, period):
        # CRDS sur revenus individuels
        crds_salaire = individu('crds_salaire', period, options = [ADD])
        crds_retraite = individu('crds_retraite', period, options = [ADD])
        crds_chomage = individu('crds_chomage', period, options = [ADD])
        crds_non_salarie = individu('crds_non_salarie', period, options = [ADD])
        crds_individu = crds_salaire + crds_retraite + crds_chomage + crds_non_salarie
        # CRDS sur revenus du capital, définie à l'échelle du foyer fiscal, mais projetée sur le déclarant principal
        crds_revenus_capital = individu.foyer_fiscal('crds_revenus_capital', period)
        crds_revenus_capital_projetee = crds_revenus_capital * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return crds_individu + crds_revenus_capital_projetee
