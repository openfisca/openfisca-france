from openfisca_france.model.base import *


class LienParente(Enum):
    __order__ = 'aucun quatrieme_degre neveu fratrie arriere_petit_enfant petit_enfant enfant ascendant epoux_pacs'
    aucun = 'Aucun lien de parenté'
    quatrieme_degre = 'Parent de 4ème degré'
    neveu = 'Neveu ou Nièce'
    fratrie = 'Frère ou soeur'
    arriere_petit_enfant = 'Arrière petit enfant'
    petit_enfant = 'Petit enfant'
    enfant = 'Enfant'
    ascendant = 'Mère, père, grand-mère, grand-père'
    epoux_pacs = 'Epoux-se ou partenaire Pacs'


class lien_parente(Variable):
    value_type = Enum
    possible_values = LienParente
    default_value = LienParente.aucun
    entity = Individu
    label = 'Lien de parenté entre le donateur et le donataire'
    definition_period = YEAR


class droit_exoneration_familial(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = 'Droit à l exonération familial, True si le donateur a moins de 80 ans et le donataire plus de 18 ans'
    definition_period = YEAR


class don(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = 'Montant de donation'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030061736'


class droits_mutation(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = 'Droits de mutation à titre gratuit'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000030061736'

    def formula_2015_01_01(individu, period, parameters):
        don = individu('don', period)
        lien_parente = individu('lien_parente', period)
        droit_exoneration_familial = individu(
            'droit_exoneration_familial', period)
        param = parameters(period).taxation_capital.donation

        def calc_droits(abattement, taux, bareme):
            exoneration_familial = param.exoneration_don_familial * droit_exoneration_familial
            base_imposable = max_(don - exoneration_familial - abattement, 0)
            if bareme:
                return bareme.calc(base_imposable)
            return taux * base_imposable

        montant_droits_donation = select(
            [
                (lien_parente == LienParente.aucun),
                (lien_parente == LienParente.quatrieme_degre),
                (lien_parente == LienParente.neveu),
                (lien_parente == LienParente.fratrie),
                (lien_parente == LienParente.ascendant),
                (lien_parente == LienParente.arriere_petit_enfant),
                (lien_parente == LienParente.petit_enfant),
                (lien_parente == LienParente.enfant),
                (lien_parente == LienParente.epoux_pacs),
                ],
            [
                calc_droits(0, param.taux_sans_parente, None),
                calc_droits(0, param.taux_parent_4eme_degre, None),
                calc_droits(param.abattement_neveu, param.taux_neveu, None),
                calc_droits(param.abattement_fratrie, 0, param.bareme_fratrie),
                calc_droits(param.abattement_ascendant, 0,
                            param.bareme_ligne_directe),
                calc_droits(param.abattement_arriere_petit_enfant,
                            0, param.bareme_ligne_directe),
                calc_droits(param.abattement_petit_enfant,
                            0, param.bareme_ligne_directe),
                calc_droits(param.abattement_enfant, 0,
                            param.bareme_ligne_directe),
                calc_droits(param.abattement_epoux_pacs,
                            0, param.bareme_epoux_pacs),
                ]
            )
        return montant_droits_donation
