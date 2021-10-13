from openfisca_france.model.base import *


########################################################################
#  Calcul de l'impôt sur les plus-values immobilières
# Impôt sur le revenu afférent à la plus-value immobilière (CGI, art. 150 U, 150 UC-I et 150 UD)
# Prélèvement dû par les non-résidents assujettis ou non à l’impôt sur le revenu (CGI, art. 244 bis A)
# Taxe forfaitaire sur la cession de terrains nus devenus constructibles (CGI, art. 1529)
# Taxe sur la cession à titre onéreux de terrains nus rendus constructibles (CGI, art.1605 nonies)
# 2048-IMM-SD
########################################################################
# TODO: create new function for f3VV (new legislation : non-resident_45%)

# def _plus_value_brute(prix_pv_immo, charges_pv_immo, frais_pv_immo, prix_acqu_immo,
#                       charges_aqu_immo, frais_acqu_immo, const_acqu_immo, voirie_acqu_immo):
#     """
#     Calcul de la plus-value immobilière brute
#     """
#     # CESSION
#     prix_cess_immo = 0    # 10;  PRIX DE CESSION OU INDEMNITE D’EXPROPRIATION = €
#     charges_cess_immo = 0 # 11. CHARGES ET INDEMNITES SUPPORTEES PAR L’ACQUEREUR + €
#     frais_cess_immo =0    # 12. FRAIS ET TAXES SUPPORTES PAR LE VENDEUR (NOTAMMENT FRAIS DE REPRESENTATION FISCALE) - €
#
#     # 13. PRIX DE CESSION CORRIGE (LIGNE 10 + LIGNE 11 – LIGNE 12) = = €
#     prix_cess_corr = prix_cess_immo + charges_cess_immo - frais_cess_immo
#
#     # ACQISISTION
#     prix_acqu_immo = 0   # 20. PRIX D’ACQUISITION OU VALEUR VENALE = €
#     charges_aqu_immo = 0 # 21. CHARGES ET INDEMNITES (MONTANT REEL) + €
#     frais_acqu_immo = 0  # 22. FRAIS D’ACQUISITION :
#                          # * A TITRE GRATUIT (MONTANT REEL) + €
#                          # * A TITRE ONEREUX (MONTANT REEL OU FIXE A 7,5% DU PRIX D’ACQUISITION) + €
#     const_acqu_immo = 0  # 23. DEPENSES DE CONSTRUCTION, RECONSTRUCTION, AGRANDISSEMENT OU AMELIORATION + €
#                          # (MONTANT REEL OU FIXE A 15% DU PRIX D’ACQUISITION SI IMMEUBLE BATI DETENU DEPUIS PLUS DE 5 ANS).
#     voirie_acqu_immo = 0 # 24. FRAIS DE VOIRIE, RESEAUX ET DISTRIBUTION + €
#     valeur_venale  = prix_acqu_immo + charges_aqu_immo + frais_acqu_immo + const_acqu_immo + voirie_acqu_immo # 25. PRIX D’ACQUISITION OU VALEUR VENALE CORRIGE (LIGNE 20 + LIGNE 21 + LIGNE 22 + LIGNE 23 + LIGNE 24) = - €
#     return prix_cess_corr-valeur_venale
#
#
# def _plus_value_nette(period, plus_value_brute, dur_det_immo, pv_immo = law.impot_revenu.pv_immo):
#     """
#     Calcul de la plus value immobilière nette
#     """
#     # 40. ABATTEMENT POUR DUREE DE DETENTION
#     # 41. NOMBRE D’ANNEES DE DETENTION AU-DELA DE LA 5EME ANNEE
#     if period.start:  # TODO:
#         taux_reduc = max_(dur_det_immo - pv_immo.ann_det1, 0) * pv_immo.taux1
#     else:
#         taux_reduc = (max_(dur_det_immo - pv_immo.ann_det3, 0) * pv_immo.taux3
#             + max_(min_(dur_det_immo, pv_immo.ann_det3) - pv_immo.ann_det2, 0) * pv_immo.taux2
#             + max_(min_(dur_det_immo, pv_immo.ann_det2) - pv_immo.ann_det1, 0) * pv_immo.taux1)
#
#     taux_reduc = min_(taux_reduc, 1.0)
#     pv_impos = (1 - taux_reduc) * plus_value_brute
#
#     # 45. MONTANT DE LA PLUS-VALUE BENEFICIANT, SOUS CONDITIONS, DE L’EXONERATION AU TITRE DE LA
#     # PREMIERE CESSION D’UN LOGEMENT EN VUE DE L’ACQUISITION DE LA RESIDENCE PRINCIPALE
#     # (CGI, 1° BIS DU II DE L’ARTICLE 150 U) TODO:
#     exo = 0
#
#     pv_net_impos = max_(pv_impos - exo, 0)  # 46. PLUS-VALUE NETTE IMPOSABLE [LIGNE 44 OU (LIGNE 44 – LIGNE 45)] = €
#     # 50. PLUS-VALUE NETTE IMPOSABLE GLOBALE =
#     # (LIGNE 46 OU TOTAL DES LIGNES 46 SI PLUSIEURS 2048-IMM-SD PAGE 2)
#
#     # Lorsqu’une même cession porte sur des biens pour lesquels sont prévues des règles différentes (acquisitions
#     # successives de fractions divises ou indivises notamment), il convient de remplir les lignes 10 à 46 pour chacune
#     # des fractions (utiliser plusieurs 2048-IMM-SD page 2).
#     return pv_net_impos


class ir_pv_immo(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt sur le revenu afférent à la plus-value immobilière"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042908474/"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        Impôt sur le revenu afférent à la plus-value immobilière (CGI, art. 150 U, 150 UC-I et 150 UD)
        """
        f3vz = foyer_fiscal('f3vz', period)
        pv_immo = parameters(period).impot_revenu.pv_immo
        impo = pv_immo.taux * f3vz

        return - impo
