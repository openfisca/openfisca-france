from openfisca_france.model.base import *


class LienParente(Enum):
    __order__ = 'aucun quatrieme_degre neveu fratrie arriere_petit_enfant petit_enfant enfant epoux_pacs'
    aucun = 'Aucun lien de parenté'
    quatrieme_degre = 'Parent de 4ème degré'
    neveu = 'Neveu ou Nièce'
    fratrie = 'Frère ou soeur'
    arriere_petit_enfant = 'Arrière petit enfant'
    petit_enfant = 'Petit enfant'
    enfant = 'Enfant'
    epoux_pacs = 'Epoux-se ou partenaire Pacs'


class lien_parente(Variable):
    value_type = Enum
    possible_values = LienParente
    default_value = LienParente.aucun
    entity = Individu
    label = 'Lien de parenté entre les individus'
    definition_period = YEAR


class don_precedent(Variable):
    value_type = float
    default_value = 0.0
    entity = Individu
    label = 'Montant des dons déjà reçu de ce donateur sur les 15 dernières années'
    definition_period = YEAR
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033809289'


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
        don_precedent = individu('don_precedent', period)
        param = parameters(period).taxation_capital.donation
        montant_droits_donation = select(
            [
                (lien_parente == LienParente.aucun),
                (lien_parente == LienParente.quatrieme_degre),
                (lien_parente == LienParente.neveu),
                (lien_parente == LienParente.fratrie),
                (lien_parente == LienParente.arriere_petit_enfant),
                (lien_parente == LienParente.petit_enfant),
                (lien_parente == LienParente.enfant),
                (lien_parente == LienParente.epoux_pacs),
                ],
            [
                param.taux_sans_parente * don,
                param.taux_parent_4eme_degre * don,
                param.taux_neveu * max_(
                    don - max_(param.exoneration_don_familial + param.abattement_neveu - don_precedent, 0), 0),
                param.bareme_fratrie.calc(max_(
                    don - max_(param.abattement_fratrie - don_precedent, 0), 0)),
                param.bareme_ligne_directe.calc(max_(
                    don - max_(param.exoneration_don_familial + param.abattement_arriere_petit_enfant - don_precedent, 0), 0)),
                param.bareme_ligne_directe.calc(max_(
                    don - max_(param.exoneration_don_familial + param.abattement_petit_enfant - don_precedent, 0), 0)),
                param.bareme_ligne_directe.calc(max_(
                    don - max_(param.exoneration_don_familial + param.abattement_enfant - don_precedent, 0), 0)),
                param.bareme_epoux_pacs.calc(max_(
                    don - max_(param.abattement_epoux_pacs - don_precedent, 0), 0)),
                ]
            )
        return montant_droits_donation
