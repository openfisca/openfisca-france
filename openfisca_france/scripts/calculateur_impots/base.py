# -*- coding: utf-8 -*-

"""Tools to use income taxes calculator from finances.gouv.fr web site."""


import urllib
import urllib2

from openfisca_france import FranceTaxBenefitSystem

__all__ = [
    'call_tax_calculator',
    'general_variable_name_by_tax_calculator_code',
    'household_income_variables_to_test',
    'individual_income_variables_to_test',
    'openfisca_variable_name_by_tax_calculator_code',
    'tax_benefit_system',
    'transform_scenario_to_tax_calculator_inputs',
    ]

tax_benefit_system = FranceTaxBenefitSystem()

openfisca_variable_name_by_tax_calculator_code = dict(
    ANNEE = u'year',
    AVFISCOPTER = None,
    BCSG = None,
    BPRS = None,
    BRDS = None,
    CIADCRE = None, #saldom2
    CICA = None,
    CICORSE = None,
    CICULTUR = None, #accult
    CIDEPENV = None, #quaenv
    CIDEVDUR = None, #quaenv
    CIGARD = u'ci_garext',
    CIGE = None,
    CIHABPRIN = u'inthab',
    CILOYIMP = u'assloy',
    CIMOBIL = None,
    CIPERT = None,
    CIPRETUD = u'preetu',
    CIRCM = None,
    CIRELANCE = None,
    CITEC = u'aidper',
    DIMMENAG = u'reduction_ss_condition_revenus',
    I2DH = None,
    IAVF2 = None,
    IAVIM = u'iai',
    IDEC = u'decote_gain_fiscal',
    IDRS2 = u'ir_plaf_qf',
    IINET = None,
    IINETIR = u'irpp',
    IPROP = None,
    IREST = None,
    IRESTIR = u'irpp',
    IRETS = None,
    ITRED = u'reductions',
    NAPCR = None,
    NAPCRP = None,
    NAPCS = None,
    NAPPS = None,
    NAPRD = None,
    NBP = u'nbptr',
    NBPT = u'nbptr',
    PERPPLAFTC = None,
    PERPPLAFTP = None,
    PERPPLAFTV = None,
    PPETOT = u'ppe',
    RAA = None,
    RAH = None,
    RAIDE = None, #saldom
    RCEL = None,
    RCEL2012 = None,
    RCELCOM = None,
    RCELFABC = None,
    RCELFD = None,
    RCELHJK = None,
    RCELHL = None,
    RCELHM = None,
    RCELHNO = None,
    RCELHR = None,
    RCELJBGL = None,
    RCELJOQR = None,
    RCELJP = None,
    RCELLIER = None,
    RCELNBGL = None,
    RCELNQ = None,
    RCELREPGJ = None,
    RCELREPGK = None,
    RCELREPGL = None,
    RCELREPGP = None,
    RCELREPGS = None,
    RCELREPGT = None,
    RCELREPGU = None,
    RCELREPGV = None,
    RCELREPGW = None,
    RCELREPGX = None,
    RCELREPHA = None,
    RCELREPHB = None,
    RCELREPHD = None,
    RCELREPHE = None,
    RCELREPHF = None,
    RCELREPHG = None,
    RCELREPHH = None,
    RCELREPHR = None,
    RCELREPHS = None,
    RCELREPHT = None,
    RCELREPHU = None,
    RCELREPHV = None,
    RCELREPHW = None,
    RCELREPHX = None,
    RCELREPHZ = None,
    RCELRRED09 = None,
    RCELRREDLA = None,
    RCELRREDLB = None,
    RCELRREDLC = None,
    RCELRREDLD = None,
    RCELRREDLE = None,
    RCELRREDLF = None,
    RCELRREDLM = None,
    RCELRREDLS = None,
    RCELRREDLZ = None,
    RCELRREDMG = None,
    RCINE = u'sofica',
    RCODELOP = None,
    RCODJT = None,
    RCODJU = None,
    RCODJV = None,
    RCODJW = None,
    RCODJX = None,
    RCOLENT = u'doment',
    RCOMP = u'adhcga',
    RCONS = None,
    RCOTFOR = None,
    RDIFAGRI = u'intagr',
    RDONS = None,
    RDUFLOGIH = None,
    REI = None,
    REVKIRE = u'rfr',
    RFCPI = None,
    RFIPC = None,
    RFOR = u'invfor',
    RFORET = u'deffor',
    RHEBE = u'daepad',
    RIDOMENT = None,
    RIDOMPROE1 = None,
    RIDOMPROE2 = None,
    RIDOMPROE3 = None,
    RIDOMPROE4 = None,
    RIDOMPROE5 = None,
    RILMIA = None,
    RILMIB = None,
    RILMIC = None,
    RILMIH = None,
    RILMIX = None,
    RILMIZ = None,
    RILMJI = None,
    RILMJS = None,
    RILMJV = None,
    RILMJW = None,
    RILMJX = None,
    RINNO = None, #spfcpi
    RINVDOMTOMLG = None,
    RINVRED = None,
    RLOCIDEFG = None,
    RLOGDOM = u'domlog',
    RMEUBLE = None,
    RNI = None,
    RNICOL = u'rni',
    RNOUV = u'cappme',
    RPATNAT = u'patnat',
    RPATNATOT = u'patnat',
    RPECHE = None,
    RPRESCOMPREP = None,
    RPROREP = None,
    RRBG = u'rbg',
    RRDOM = None,
    RREDMEUB = None,
    RREDREP = None,
    RREPA = u'donapd',
    RREPMEU = None,
    RREPNPRO = None,
    RRESIMEUB = None,
    RRESINEUV = None,
    RRESIVIEU = None,
    RRESTIMO = u'resimm',
    RRETU = u'ecpess',
    RRIRENOV = u'mohist',
    RRPRESCOMP = None,
    RSOCREPR = u'repsoc',
    RSOUFIP = None,
    RSURV = u'rsceha',
    RTELEIR = None,
    RTITPRISE = u'cappme',
    RTOUHOTR = None,
    RTOUR = None,
    RTOUREPA = None,
    RTOURES = None,
    RTOURHOT = None,
    RTOURNEUF = None,
    RTOURREP = None,
    RTOURTRA = None,
    TEFF = None,
    TOTPAC = u'nb_pac',
    TXMARJ = None,
    TXMOYIMP = None,
    )


general_variable_name_by_tax_calculator_code = {  
    'AVFISCOPTER': u'?',
    'BCSG': u'Base CSG',
    'BPRS': u'Base prélèvement social et contributions annexes',
    'BRDS': u'Base CRDS',
    'CIADCRE': u'Crédit d\'impôt pour dépenses au titre de services à la personne à domicile',
    'CICORSE': u'Crédit d\'impôt pour investissements en Corse',
    'CICORSEAVIS': u'Crédit d\'impôt pour investissements en Corse',
    'CICULTUR': u'Réduction/Crédit (?) d\'impôt pour acquisitions de biens culturels',
    'CIDEPENV': u'Crédit d\'impôt sur dépenses en faveur de la qualité environnementale des logements en location',
    'CIDEVDUR': u'Crédit d\'impôt sur dépenses en faveur de la qualité environnementale du logement principal',
    'CIFORET': u'Crédit d\'impôt pour investissements forestiers',
    'CIGARD': u'Crédit d\'impôt pour frais de garde d\'enfants',
    'CIGE': u'Crédit aides aux personnes',
    'CIHABPRIN': u'Crédit d\'impôt au titre des intérêts d\'emprunt pour acquisition de l\'habitation principale',
    'CILOYIMP': u'Crédit d\'impôt au titre des primes d\'assurances pour loyers impayés',
    'CIMOBIL': u'Rentes de source étrangère ouvrant droit à un crédit impôt égal à l\'impôt français',
    'CIPERT': u'?',#TODO (f3vv)
    'CIPRETUD': u'Crédit d\'impôt au titre des intérêts sur prêts étudiants',
    'CIRCM': u'?',
    'CIRELANCE': u'Crédit d\'impôt exceptionnel sur les revenus 2008',
    'CITEC': u'Crédit d\'impôt sur dépenses de prévention des risques technologiques dans les locations (ou aide à la personne)',
    'DIMMENAG': u'Réduction d\'impôt sous condition de revenus 2016',
    'I2DH': u'Prélèvement libératoire de 7,5%',
    'IAVF2': u'?',#TODO (f8th)
    'IAVIM': u'Impôt avant imputations',
    'IDEC': u'Décote',
    'IDRS2': u'Droits simples',
    'IINET': u'Montant net à payer',
    'IINETIR': u'Impôt sur le revenu net',
    'IPROP': u'Impôt proportionnel',
    'IREST': u'Montant net à restituer',
    'IRESTIR': u'Impôt sur le revenu net',
    'IRETS' : u'?',
    'ITRED': u'Total des réductions d\'impôt',
    'NAPCRP': u'Montant net des prélèvements sociaux (sur revenu du patrimoine et revenus d\'activité et de remplacement',
    'NAPCS': u'Montant net CSG',
    'NAPPS': u'Montant net prélèvement social et contributions annexes',
    'NAPRD': u'Montant net CRDS',
    'NBP': u'Nombre de parts',
    'NBPT': u'Nombre de parts',
    'PERPPLAFTC': u'?',#TODO (f2ch, f2dh, maries_ou_pacses)
    'PERPPLAFTV': u'Plafond de déduction pour les revenus 2014 au titre de l\'épargne retraite, pour déclarant 1',
    'PPETOT': u'Prime pour l\'emploi',
    'RAA': u'?',
    'RAH': u'?',
    'RAIDE': u'Réduction d\'impôt pour dépenses au titre de services à la personne à domicile',
    'RCEL': u'?',#TODO (scellier)
    'RCEL2012': u'?',#TODO (7ja)
    'RCELCOM': u'?',#TODO (7np)
    'RCELFABC': u'Réduction d\'impôt Scellier : cases 7FA, 7FB, 7FC',
    'RCELFD': u'Réduction d\'impôt Scellier : case 7FD',
    'RCELHJK': u'Réduction d\'impôt Scellier : case 7HJ, 7HK',
    'RCELHL': u'Réduction d\'impôt Scellier : case 7HL',
    'RCELHM': u'Réduction d\'impôt Scellier : case 7HM',
    'RCELHNO': u'Réduction d\'impôt Scellier : case 7HN, 7HO',
    'RCELHR': u'Réduction d\'impôt Scellier : case 7HR',
    'RCELHS': u'Réduction d\'impôt Scellier : case 7HS',
    'RCELJBGL': u'Réduction d\'impôt Scellier : case ?',
    'RCELJOQR': u'Réduction d\'impôt Scellier : case ?',
    'RCELJP': u'Réduction d\'impôt Scellier : case ?',
    'RCELLIER': u'Réduction d\'impôt Scellier : case ?',
    'RCELNBGL': u'Réduction d\'impôt Scellier : case ?',
    'RCELNQ': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGJ': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGK': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGL': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGP': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGS': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGT': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGU': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGV': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGV': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGW': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPGX': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHA': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHB': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHD': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHE': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHF': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHG': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHH': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHR': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHS': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHT': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHU': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHV': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHW': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHX': u'Réduction d\'impôt Scellier : case ?',
    'RCELREPHZ': u'Réduction d\'impôt Scellier : case ?',
    'RCELRRED09': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLA': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLB': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLC': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLD': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLE': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLF': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLM': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLS': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDLZ': u'Réduction d\'impôt Scellier : case ?',
    'RCELRREDMG': u'Réduction d\'impôt Scellier : case ?',
    'RCINE': u'Réduction d\'impôt pour souscription au capital d\'une SOFICA',
    'RCODELOP': u'?',
    'RCODJT': u'Réduction d\'impôt Censi-Bouvard : case 7JT',
    'RCODJTJU': u'Réduction d\'impôt Censi-Bouvard : case 7JT, 7JU',
    'RCODJU': u'Réduction d\'impôt Censi-Bouvard : case 7JU',
    'RCODJV': u'Réduction d\'impôt Censi-Bouvard : case ?',
    'RCODJW': u'Réduction d\'impôt Censi-Bouvard : case ?',
    'RCODJX': u'Réduction d\'impôt Censi-Bouvard : case ?',
    'RCOLENT': u'Réduction d\'impôt pour investissements Outre-Mer dans le cadre d\'une entreprise',
    'RCOMP': u'Réduction d\'impôt pour frais de comptabilité et d\'adhésion à un CGA',
    'RCOTFOR': u'Réduction d\'impôt pour investissements forestiers',
    'RDIFAGRI': u'Réduction d\'impôt pour paiement différé accordé aux agriculteurs',
    'RDONS': u'Réduction d\'impôt pour dons à des oeuvres d\'intérêt général',
    'RDUFLOGIH': u'Réduction d\'impôt Duflot : cases 7GH, 7GI',
    'RDUFREPFI': u'Réduction d\'impôt Duflot : case 7FI',
    'RDUFREPFK': u'Réduction d\'impôt Duflot : case 7FK',
    'RDUFREPFR': u'Réduction d\'impôt Duflot : case 7FR',
    'REI': u'Reprise de réductions ou de crédits d\'impôt : cases 8TF, 8TP',
    'REVKIRE': u'Revenu fiscal de référence',
    'RFCPI': u'?',
    'RFIPC': u'Réduction d\'impôt pour souscription au capital de FCPI en Corse',
    'RFOR': u'Réduction d\'impôt pour investissements forestiers (jusque 2013)',
    'RFORET': u'Réduction d\'impôt pour cotisations pour la défense des forêts contre l\'incendie',
    'RHEBE': u'Réduction d\'impôt pour dépenses d\'acceuil dans un établissement pour personnes dépendantes',
    'RIDOMENT': u'?',#TODO (7ur)
    'RIDOMPROE1': u'?',
    'RIDOMPROE2': u'?',#TODO (f7qz)
    'RIDOMPROE3': u'?',#TODO (f7qz)
    'RIDOMPROE4': u'?',#TODO (f7oz)
    'RIDOMPROE5': u'?',#TODO (f7oz)
    'RILMIA': u'Réduction d\'impôt Censi-Bouvard : case 7IA',
    'RILMIB': u'Réduction d\'impôt Censi-Bouvard : case 7IB',
    'RILMIC': u'Réduction d\'impôt Censi-Bouvard : case 7IC',
    'RILMIH': u'Réduction d\'impôt Censi-Bouvard : case 7IH',
    'RILMIX': u'Réduction d\'impôt Censi-Bouvard : case 7IX',
    'RILMIZ': u'Réduction d\'impôt Censi-Bouvard : case 7IZ',
    'RILMJI': u'Réduction d\'impôt Censi-Bouvard : case 7JI',
    'RILMJS': u'Réduction d\'impôt Censi-Bouvard : case 7JS',
    'RILMJV': u'Réduction d\'impôt Censi-Bouvard : case 7JV',
    'RILMJW': u'Réduction d\'impôt Censi-Bouvard : case 7JW',
    'RILMJX': u'Réduction d\'impôt Censi-Bouvard : case 7JX',
    'RINNO': u'Réduction d\'impôt pour souscription au capital de FCPI',
    'RINVDOMTOMLG': u'?',
    'RINVRED': u'Réduction d\'impôt Censi-Bouvard : case 7IT',
    'RLOCIDEFG': u'Réduction d\'impôt Censi-Bouvard : cases 7ID, 7IE, 7IF, 7IG',
    'RLOGDOM': u'Réduction d\'impôt pour investissements Outre-Mer dans le secteur du logement',
    'RMEUBLE': u'Réduction d\'impôt Censi-Bouvard : case 7IK',
    'RNI': u'?',
    'RNICOL': u'Revenu net imposable ou déficit à reporter',
    'RNOUV': u'Réduction d\'impôt pour souscription au capital de PME',
    'RPATNAT': u'Réduction d\'impôt pour dépenses de protection du patrimoine naturel',
    'RPATNATOT': u'Réduction d\'impôt pour dépenses de protection du patrimoine naturel',
    'RPRESCOMPREP': u'Prestation compensatoire : report de l\'année précédente : case 7wp',
    'RPROREP': u'?',#TODO (7is)
    'RRBG': u'Revenu brut global ou déficit',
    'RRDOM': u'?',#TODO (7ub)
    'RREDMEUB': u'?',#TODO (7is)
    'RREDREP': u'?',#TODO (7iu)
    'RREPA': u'Réduction d\'impôt pour dons à des organismes de personnes en difficultés',
    'RREPMEU': u'Réduction d\'impôt Censi-Bouvard : case 7IP',
    'RREPNPRO': u'Réduction d\'impôt Censi-Bouvard : case 7IQ',
    'RRESIMEUB': u'?',#TODO (7io)
    'RRESINEUV': u'?',#TODO (7ij)
    'RRESIVIEU': u'?',#TODO (7im, 7iw)
    'RRESTIMO': u'Réduction d\'impôt Malraux pour travaux de restauration immobilière',
    'RRETU': u'Réduction d\'impôt pour enfants à charge poursuivant leurs études',
    'RRIRENOV': u'Réduction d\'impôt pour travaux de conservation ou restauration de monuments historiques',
    'RRPRESCOMP': u'Prestation compensatoire',
    'RSOCREPR': u'Réduction d\'impôt au titre des intérêts d\'emprunt de reprise d\'une société',
    'RSOUFIP': u'Réduction d\'impôt pour souscription au capital de FIP',
    'RSURV': u'Réduction d\'impôt sur primes des contrats de rente-survie et épargne handicap',
    'RTELEIR': u'?',
    'RTITPRISE': u'Réduction d\'impôt pour souscription au capital de PME',
    'RTOUHOTR': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : résidence hôtelière',
    'RTOUR': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : ',
    'RTOUREPA': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : ',
    'RTOURES': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : ',
    'RTOURHOT': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : ',
    'RTOURNEUF': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : ',
    'RTOURREP': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : reports (case 7XF à 7XN)',
    'RTOURTRA': u'Réduction d\'impôt pour investissements locatifs dans le secteur touristique : ',
    'TEFF': u'?',#TODO (ebnc_impo)
    'TOTPAC': u'Nombre de personnes à charge',
    'TXMARJ': u'Taux marginal d\'imposition',
    'TXMOYIMP': u'Taux moyen d\'imposition',
}

household_income_variables_to_test = [ # NB: taken from input variables of FELIN-ERFS Survey Scenario (TAXIPP) 2014
    # TODO : fix following errors
    # 'f2ab', 'f2bg', CREDIT D'IMPOT (2AB) > 80 EUROS SANS REVENU CORRESPONDANT
    # 'f2ck', CREDIT D'IMPOT 2CK > 80 E SANS REVENU CORRESPONDANT</UL>
    # 'f7is', 'f7iu', 'f7ix', 'f7iy',
    # 'f3ve', 'f7fl', MONTANT LIGNE 3VE POUR UN CONTRIBUABLE NON DOMICILIE DANS UN DOM</UL>
    # 'f4bf', MONTANT PORTE LIGNE 4BF SANS REVENU OU DEFICIT FONCIER CORRESPONDANT
    # 'f7jy', f7jy must be < 16
    # 'f7ly', 'f7my', => number of conventions d'aides aux créateurs d'entreprises (not an income)
    # 'f7qh', 'f7qi', to test this => f7qi must be < f7qh
    # 'f7qr', 'f7qq', to test this => f7qr must be < f7qq
    # 'f7ri', 'f7rh', to test this => f7ri must be < f7rh
    # 'f7ro', 'f7rn', idem
    # 'f7rt', 'f7rs', idem
    # 'f7ry', 'f7rx', idem
    # 'f7sb', 'f7sa', LIGNE 7 SB, 7 SH, 7 SD, 7 SE, 7 SG SANS PRISE EN CHARGE DU CHIFFRE 7 SA
    # 'f7sh', 'f7sd', 'f7se', 'f7sg', to check
    # 'f7sj', 'f7sk', 'f7sl',
    # 'f7vg', CASE 7VG COCHEE SANS MONTANT LIGNE 7SH
    # 'f7wc', CASE 7WC COCHEE SANS MONTANT LIGNE 7SG<
    # 'f7wv', CASE 7WU 7WV COCHEE SANS MONTANT LIGNE 7SK ET RECIPROQUEMENT
    # 'f7ww', CASE 7WW 7WX COCHEE SANS MONTANT LIGNE 7SL ET RECIPROQUEMENT
    # 'f8ti', LA LIGNE 8TK EST REMPLIE SANS PRISE EN CHARGE DE 8XR, 8XP OU 8XQ
    # 'f8tk', LA LIGNE 8TK EST REMPLIE SANS PRISE EN CHARGE DE 8XR, 8XP OU 8XQ
    # cerdit quaenv : 'f7wh', CASE 7WH COCHEE SANS MONTANT LIGNE 7SD A 7ST
    # credit accult : 'f7uo', LA LIGNE 7UO EST REMPLIE SANS REVENU CORRESPONDANT
    # credit mecena : 'f7us', LA LIGNE 7US EST REMPLIE SANS REVENU CORRESPONDANT
    # credit quaenv : 'f7we', 'f7wg', CASE 7WE OU 7WG COCHEE SANS PRISE EN CHARGE LIGNES 7WH, 7WK, 7WF, 7WQ, 7WR
    # credit quaenv : 'f7wk', CASE 7WK COCHEE SANS MONTANT LIGNE 7SD A 7SW
    # prestation_compensatoire : 'f7wm', LE MONTANT 7WM EST INFERIEUR AU MONTANT 7WN
    # prestation_compensatoire : 'f7wn', 'f7wo', PRESENCE D UN MONTANT LIGNE 7WN SANS MONTANT 7WO OU RECIPROQUEMENT
    # reduc invfor : 'f7ut', CASE 7 UT COCHEE SANS PRISE EN CHARGE MONTANT LIGNE 7 UP
    # reduc_malraux 'f7nx', 'f7ny', to test this => f7ny must be < f7nx
    'f1ar', 'f1br', 'f1cr', 'f1dr', 'f1er', 'f1aw', 'f1bw', 'f1cw', 'f1dw',
    'f2aa', 'f2al', 'f2am', 'f2an', 'f2aq', 'f2ar', 'f2dm',
    'f2ch', 'f2cg', 'f2dc', 'f2ts', 'f2ca', 'f2fu', 'f2go', 'f2gr', 'f2da', 'f2dh', 'f2ee', 'f2tr',
    'f3sa', 'f3sg', 'f3sh', 'f3sl', 'f3sm',
    'f3vg', 'f3vh', 'f3vm', 'f3vt', 'f3vc', 'f3vf', 'f3vi', 'f3vj', 'f3vz', 'f3vp', 'f3vy',
    'f4ba', 'f4bb', 'f4bc', 'f4bd', 'f4tq',
    'f5ga', 'f5gb', 'f5gc', 'f5gd', 'f5ge', 'f5gf', 'f5gg', 'f5gh', 'f5gi', 'f5gj',
    'f5ht', 'f5it', 'f5jt', 'f5kt', 'f5lt', 'f5mt', 
    'f5qf', 'f5qg', 'f5qn', 'f5qo', 'f5qp', 'f5qq',
    'f5rn', 'f5rn', 'f5rp', 'f5rq', 'f5rr', 'f5rw',
    'f7ah', 'f7tn', 'f7bc', 'f7vh', 'f7qb', 'f7ql', 'f7pi', 
    'f7rr', 'f7rq', 'f7rp', 'f7rw', 'f7rv', 'f7ru', 'f7rc', 'f7rb', 'f7ra', 'f7rg', 'f7rf', 'f7re', 'f7rd', 'f7rk', 'f7rj', 'f7rm', 'f7rl', 'f6fl', 'f6fb', 'f6fc', 'f6fa', 'f6fd', 'f6fe', 'f6ps', 'f7gx', 'f7gz', 'f7gt', 'f7gu', 'f7gv', 'f7gw', 'f7gp', 'f7gq', 'f7gs', 'f7gl', 'f7gn', 'f7gh', 'f7gi', 'f7gj', 'f7gk', 'f7ge', 'f7gf', 'f7gg', 'f7gc', 'f8tp', 'f8th', 'f8to', 'f8ta', 'f8tf', 'f8td', 'f7ng', 'f7nf', 'f7ne', 'f7nd', 'f7nc', 'f7nb', 'f7na', 'f7no', 'f7nn', 'f7nm', 'f7nl', 'f7nk', 'f7nj', 'f7ni', 'f7nh', 'f7nw', 'f7nv', 'f7nu', 'f7nt', 'f7ns', 'f7nr', 'f7nq', 'f7np', 'f7nz',  'f7uh', 'f7un', 'f7ul', 'f7uc', 'f7uf', 'f7uz', 'f7ux', 'f7uy', 'f7up', 'f7uq', 'f7uv', 'f7uw', 'f7uu', 'f7jk', 'f7jj', 'f7ji', 'f7jh', 'f7jo', 'f7jn', 'f7jm', 'f7jl', 'f7jc', 'f7jb', 'f7ja', 'f7jg', 'f7jf', 'f7je', 'f7jd', 'f7jx', 'f7js', 'f7jr', 'f7jq', 'f7jp', 'f7jw', 'f7jv', 'f7ju', 'f7jt', 'f7cc', 'f7cd', 'f7ce', 'f7cf', 'f7cl', 'f7cm', 'f7cn', 'f7cq', 'f7cu', 'f7xf', 'f7xi', 'f7xk', 'f7xj', 'f7xm', 'f7xo', 'f7xn', 'f7xq', 'f7xp', 'f7xs', 'f7xr', 'f7xu', 'f7xt', 'f7xw', 'f7xv', 'f7xy', 'f7xz', 'f6hj', 'f6hk', 'f6hl', 'f6hm', 'f7qx', 'f7qw', 'f7qu', 'f7qs', 'f7qj', 'f7qf', 'f7qg', 'f6gi', 'f6gh', 'f6gj', 'f6gu', 'f6gp', 'f7ma', 'f7mg', 'f7fq', 'f7fn', 'f7fm', 'f7fh', 'f7fd', 'f7fc', 'f7fb', 'f7fa', 'f7te', 'f7tg', 'f7th', 'f6dd', 'f6de', 'f6cb', 'f7iv', 'f7iw', 'f7it', 'f7ir', 'f7ip', 'f7iq', 'f7iz', 'f7if', 'f7ig', 'f7id', 'f7ie', 'f7ib', 'f7ic', 'f7ia', 'f7in', 'f7io', 'f7il', 'f7im', 'f7ij', 'f7ik', 'f7ih', 'f7py', 'f7wl', 'f7wj', 'f7wp', 'f7wr', 'f6eu', 'f6em', 'f6el', 'f7lm', 'f7li', 'f7le', 'f7ld', 'f7lg', 'f7lf', 'f7la', 'f7lc', 'f7lb', 'f7lz', 'f7ls', 'f7sp', 'f7sq', 'f7sr', 'f7ss', 'f7st', 'f7su', 'f7sv', 'f7sw', 'f7sx', 'f7sy', 'f7sz', 'f7sf',  'f7si', 'f7sm', 'f7sn', 'f7so', 'f7oa', 'f7ob', 'f7oc', 'f7ol', 'f7om', 'f7on', 'f7oo', 'f7oh', 'f7oi', 'f7oj', 'f7ok', 'f7ot', 'f7ou', 'f7ov', 'f7ow', 'f7op', 'f7oq', 'f7or', 'f7os', 'f7hs', 'f7hr', 'f7hu', 'f7ht', 'f7hw', 'f7hv', 'f7hx', 'f7hz', 'f7ha', 'f7hb', 'f7he', 'f7hd', 'f7hg', 'f7hf', 'f7hh', 'f7hk', 'f7hj', 'f7hm', 'f7hl', 'f7ho', 'f7hn', 'f7ac', 'f7vc', 'f7va', 'f7vz', 'f7vy', 'f7vx', 'f7vw', 'f7vv', 'f7vu', 'f7vt', 'f7kh', 'f7ki', 'f7ka', 'f7kb', 'f7kc', 'f7kd', 'f7ks', 'f7df', 'f7db',  
    'f7ui', 'f7pa', 'f7cy', 'f7dy', 'f7ey', 'f7yz', 'f7ym', 'f7lt',
    'f7wj', 'f7wl', 'f7wr', 'f7ga', 'f7gb', 'f7gc', 'f7ge', 'f7gf', 'f7gg', 'f7bm', 'f7cb',
    'f8ta', 'f8vl', 'f8vm',
]

individual_income_variables_to_test = [ # NB: taken from input variables of FELIN-ERFS Survey Scenario (TAXIPP) 2014
    # 'f1tv', 'f1tw', 'f1tx',  => individual incomes but not with this name.. TO CHECK
    # 'revimpres', "REVENUS A IMPOSER AUX CONTRIBUTIONS SOCIALES SANS REVENU CORRESPONDANT"
    #'f6ev', 'f6rs', 'f6ss', 'f7dg', 'f7dl', 'f7dq', 
    #'ppe_tp_ns', # WARNING : DGFiP calculator does not like this one
    'aacc_defn',
    'aacc_defs',
    'aacc_exon',
    'aacc_gits',
    'aacc_impn', 
    'aacc_imps',
    'aacc_pvce', 
    'abic_defm', 
    'abic_defn', 
    'abic_defs',
    'abic_exon', 
    'abic_impm', 
    'abic_impn', 
    'abic_imps',
    'abic_pvce', 
    'abnc_defi', 
    'abnc_exon', 
    'abnc_impo', 
    'abnc_proc', 
    'abnc_pvce', 
    'alnp_defs',
    'alnp_imps', 
    'arag_defi', 
    'arag_exon', 
    'arag_impg', 
    'arag_pvce', 
    'cbnc_assc',  
    'chomage_imposable',
    'cncn_aimp', 
    'cncn_bene', 
    'cncn_defi',
    'cncn_exon', 
    'cncn_info', 
    'cncn_jcre', 
    'cncn_pvce', 
    'ebic_imps',
    'ebic_impv',
    'ebnc_impo',
    'f3vd', 'f3vl',
    'frag_exon', 
    'frag_fore', 
    'frag_impo', 
    'frag_pvce', 
    'frag_pvct', 
    'macc_exon', 
    'macc_imps', 
    'macc_impv', 
    'macc_mvct', 
    'macc_pvce', 
    'macc_pvct', 
    'mbic_exon', 
    'mbic_imps', 
    'mbic_impv', 
    'mbic_mvct', 
    'mbic_pvce', 
    'mbic_pvct', 
    'mbnc_exon', 
    'mbnc_impo', 
    'mbnc_mvct', 
    'mbnc_mvlt', 
    'mbnc_pvce', 
    'mbnc_pvct', 
    'mncn_exon', 
    'mncn_impo', 
    'mncn_mvct', 
    'mncn_pvce', 
    'mncn_pvct', 
    'nacc_defn', 
    'nacc_defs', 
    'nacc_exon', 
    'nacc_impn', 
    'nacc_meup',
    'nacc_pvce',
    'nbic_apch', 
    'nbic_defn', 
    'nbic_defs',
    'nbic_exon', 
    'nbic_impm', 
    'nbic_impn', 
    'nbic_imps',
    'nbic_mvct', 
    'nbic_pvce', 
    'nbnc_defi', 
    'nbnc_exon', 
    'nbnc_impo', 
    'nbnc_proc', 
    'nbnc_pvce', 
    'nrag_ajag', 
    'nrag_defi', 
    'nrag_exon', 
    'nrag_impg', 
    'nrag_pvce',
    'pensions_alimentaires_percues',
    'pensions_invalidite',
    'ppe_du_ns',
    'ppe_du_sa',
    'pveximpres',  
    'retraite_imposable',
    ]


def call_tax_calculator(year, inputs):
    """
    Function that calls the DGFiP income tax simulator's webpage
    """
    url = 'https://www3.impots.gouv.fr/simulateur/cgi-bin/calc-{}.cgi'.format(year + 1)
    request = urllib2.Request(url, headers = {
        'User-Agent': 'OpenFisca-Script',
        })
    response = urllib2.urlopen(request, urllib.urlencode(inputs))
    response_html = response.read()
    if 'Erreur' in response_html:
        raise Exception(u"Erreur : {}".format(response_html.decode('iso-8859-1')).encode('utf-8'))
    return response_html


def transform_scenario_to_tax_calculator_inputs(scenario):
    tax_benefit_system = scenario.tax_benefit_system
    test_case = scenario.test_case
    impots_arguments = {
        'pre_situation_residence': 'M',  # Métropole
        }
    individu_by_id = {
        individu['id']: individu
        for individu in test_case['individus']
        }
    for foyer_fiscal in test_case['foyers_fiscaux']:
        foyer_fiscal = foyer_fiscal.copy()

        for declarant_index, declarant_id in enumerate(foyer_fiscal.pop('declarants')):
            declarant = individu_by_id[declarant_id].copy()

            date_naissance = declarant.pop('date_naissance')
            impots_arguments['0D{}'.format(chr(ord('A') + declarant_index))] = date_naissance.year

            statut_marital = declarant.pop('statut_marital', None)
            column = tax_benefit_system.variables['statut_marital']
            if statut_marital is None:
                statut_marital = column.enum._vars[column.default_value]
            pre_situation_famille = {
                u"Marié": 'M',
                u"Célibataire": 'C',
                u"Divorcé": 'D',
                u"Veuf": 'V',
                u"Pacsé": 'O',
                # u"Jeune veuf": TODO
                }[statut_marital if isinstance(statut_marital, basestring) else column.possible_values._vars[statut_marital]]
            assert 'pre_situation_famille' not in impots_arguments \
                or impots_arguments['pre_situation_famille'] == pre_situation_famille, str((impots_arguments,
                    pre_situation_famille))
            impots_arguments['pre_situation_famille'] = pre_situation_famille

            for column_code, value in declarant.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        'id',
                        ):
                    continue
                column = tax_benefit_system.variables[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[declarant_index]] = int(value) if isinstance(value, float) else value

        impots_arguments['0CF'] = len(foyer_fiscal['personnes_a_charge'])
        for personne_a_charge_index, personne_a_charge_id in enumerate(foyer_fiscal.pop('personnes_a_charge')):
            personne_a_charge = individu_by_id[personne_a_charge_id].copy()

            date_naissance = personne_a_charge.pop('date_naissance')
            impots_arguments['0F{}'.format(personne_a_charge_index)] = date_naissance.year

            personne_a_charge.pop('statut_marital', None)

            for column_code, value in personne_a_charge.iteritems():
                if column_code in (
                        'activite',
                        'cadre',
                        'id',
                        ):
                    continue
                column = tax_benefit_system.variables[column_code]
                cerfa_field = column.cerfa_field
                assert cerfa_field is not None and isinstance(cerfa_field, dict), column_code
                impots_arguments[cerfa_field[personne_a_charge_index]] = value
        
        
        for column_code, value in foyer_fiscal.iteritems():
            if column_code == 'id':
                continue
            if column_code == 'f7uf':
                impots_arguments['7UG'] = str(value)  # bug dans le site des impots
            if column_code == 'f7ud':
                impots_arguments['7UE'] = str(value)  # bug dans le site des impots
            if column_code == 'f7vc':
                impots_arguments['7VD'] = str(value)  # bug dans le site des impots
            if column_code == 'nbF':
                impots_arguments['0CF'] = int(value)
            if column_code == 'nbG':
                impots_arguments['0CG'] = int(value)
            if column_code == 'nbH':
                impots_arguments['0CH'] = int(value)
            if column_code == 'nbI':
                impots_arguments['0CI'] = int(value)
            if column_code == 'nbR':
                impots_arguments['0CR'] = int(value)
            if column_code == 'nbJ':
                impots_arguments['0DJ'] = int(value)
            if column_code == 'nbN':
                impots_arguments['0DN'] = int(value)
            if (column_code == 'caseF') & (value == 1):
                impots_arguments['0AF'] = '1'
            if (column_code == 'caseG') & (value == 1):
                impots_arguments['0AG'] = '1'
            if (column_code == 'caseL') & (value == 1):
                impots_arguments['0AL'] = '1'
            if (column_code == 'caseP') & (value == 1):
                impots_arguments['0AP'] = '1'
            if (column_code == 'caseS') & (value == 1):
                impots_arguments['0AS'] = '1'
            if (column_code == 'caseW') & (value == 1):
                impots_arguments['0AW'] = '1'
            if (column_code == 'caseT') & (value == 1):
                impots_arguments['0BT'] = '1'
            column = tax_benefit_system.variables[column_code]
            cerfa_field = column.cerfa_field
            assert cerfa_field is not None and isinstance(cerfa_field, basestring), column_code
            if ("nb" not in column_code) and ("case" not in column_code):
                impots_arguments[cerfa_field] = int(value) if isinstance(value, bool) else value

    return impots_arguments
