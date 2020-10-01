from openfisca_france.model.base import Variable, FoyerFiscal, MONTH, YEAR, max_


class taxe_fonciere_sur_avis(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Taxe foncière sur les propriétés bâties (TFPB)"
    reference = [
        "https://www.service-public.fr/particuliers/vosdroits/F59"
        ]
    definition_period = YEAR


class taxe_fonciere_degrevement(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Montant du dégrèvement applicable pour la taxe foncière sur les propriétés bâties"
    reference = [
        "Article 1391 B ter du Code général des impôts",
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000036427299/2020-12-31#linkLEGIARTI000036427299-7"
        ]
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        ressources = foyer_fiscal('rfr', period)
        tf_base = foyer_fiscal('taxe_fonciere_sur_avis', period)
        montant = max_(0, tf_base - 0.50 * ressources)
        return (15 < montant) * montant


class taxe_fonciere_degrevement_montant(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Montant du dégrèvement applicable pour la taxe foncière sur les propriétés bâties"
    definition_period = MONTH

    def formula(foyer_fiscal, period, parameters):
        return foyer_fiscal('taxe_fonciere_degrevement', period.n_2)
