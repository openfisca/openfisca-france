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
    CIADCRE = None,
    CICA = None,
    CICORSE = None,
    CIDEPENV = None,
    CIDEVDUR = None,
    CIGARD = None,
    CIGE = None,
    CIHABPRIN = None,
    CIMOBIL = None,
    CIPERT = None,
    CIPRETUD = None,
    CIRCM = None,
    CIRELANCE = None,
    CITEC = None,
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
    RAIDE = None,
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
    RCINE = None,
    RCODELOP = None,
    RCODJT = None,
    RCODJU = None,
    RCODJV = None,
    RCODJW = None,
    RCODJX = None,
    RCOLENT = None,
    RCONS = None,
    RCOTFOR = None,
    RDIFAGRI = None,
    RDONS = None,
    RDUFLOGIH = None,
    REI = None,
    REVKIRE = u'rfr',
    RFCPI = None,
    RFIPC = None,
    RFOR = None,
    RFORET = None,
    RHEBE = None,
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
    RINNO = None,
    RINVDOMTOMLG = None,
    RINVRED = None,
    RLOCIDEFG = None,
    RLOGDOM = None,
    RMEUBLE = None,
    RNI = None,
    RNICOL = u'rni',
    RNOUV = None,
    RPATNAT = None,
    RPATNATOT = None,
    RPECHE = None,
    RPRESCOMPREP = None,
    RPROREP = None,
    RRBG = u'rbg',
    RRDOM = None,
    RREDMEUB = None,
    RREDREP = None,
    RREPA = None,
    RREPMEU = None,
    RREPNPRO = None,
    RRESIMEUB = None,
    RRESINEUV = None,
    RRESIVIEU = None,
    RRESTIMO = None,
    RRIRENOV = None,
    RRPRESCOMP = None,
    RSOCREPR = None,
    RSOUFIP = None,
    RSURV = None,
    RTELEIR = None,
    RTITPRISE = None,
    RTOUHOTR = None,
    RTOUR = None,
    RTOUREPA = None,
    RTOURES = None,
    RTOURHOT = None,
    RTOURNEUF = None,
    RTOURREP = None,
    RTOURTRA = None,
    TEFF = None,
    TOTPAC = None,  # Nombre de personnes à charge dans le foyer fiscal
    TXMARJ = None,
    TXMOYIMP = None,
    )


general_variable_name_by_tax_calculator_code = {  
    'AVFISCOPTER': u'?',#TODO (f8tf)
    'BCSG': u'Base CSG',
    'BPRS': u'Base prélèvement social et contributions annexes',
    'BRDS': u'Base CRDS',
    'CIADCRE': u'?',#TODO (f7dg)
    'CICA': u'?',#TODO (f4tq)
    'CICORSE': u'?',#TODO (f8to)
    'CIDEPENV': u'?',#TODO (f7sz)
    'CIDEVDUR': u'?',#TODO (f7wf)
    'CIGARD': u'?',#TODO (f7ga)
    'CIGE': u'Crédit aides aux personnes',
    'CIHABPRIN': u'?',#TODO (f7vy)
    'CIMOBIL': u'?',#TODO (f1ar)
    'CIPERT': u'?',#TODO (f3vv)
    'CIPRETUD': u'?',#TODO (f7uk)
    'CIRCM': u'?',#TODO (f2dc)
    'CIRELANCE': u'Crédit d\'impôt exceptionnel sur les revenus 2008',
    'CITEC': u'?',#TODO (f7wr)
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
    'IRETS' : u'?',#TODO
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
    'RAA': u'?',#TODO (7ud)
    'RAH': u'?',#TODO (7ce)
    'RAIDE': u'?',#TODO (7df)
    'RCEL': u'?',#TODO (scellier)
    'RCEL2012': u'?',#TODO (7ja)
    'RCELCOM': u'?',#TODO (7np)
    'RCELFABC': u'?',#TODO (7fa)
    'RCELFD': u'?',#TODO (f7fd)
    'RCELHJK': u'?',#TODO (scellier)
    'RCELHL': u'?',#TODO (7hl)
    'RCELHM': u'?',#TODO (7hm)
    'RCELHNO': u'?',#TODO (7hn)
    'RCELHR': u'?',#TODO (7hr)
    'RCELJBGL': u'?',#TODO (7jb)
    'RCELJOQR': u'?',#TODO (7jo)
    'RCELJP': u'?',#TODO (7jp)
    'RCELLIER': u'?',#TODO (7hk)
    'RCELNBGL': u'?',#TODO (7nb)
    'RCELNQ': u'?',#TODO (7nq)
    'RCELREPGJ': u'?',#TODO (7gj)
    'RCELREPGK': u'?',#TODO (7gk)
    'RCELREPGL': u'?',#TODO (7gl)
    'RCELREPGP': u'?',#TODO (7gp)
    'RCELREPGS': u'?',#TODO (7gs)
    'RCELREPGT': u'?',#TODO (7gt)
    'RCELREPGU': u'?',#TODO (7gu)
    'RCELREPGV': u'?',#TODO
    'RCELREPGV': u'?',#TODO (7gv)
    'RCELREPGW': u'?',#TODO (f7gw)
    'RCELREPGX': u'?',#TODO (f7gx)
    'RCELREPHA': u'?',#TODO (7ha)
    'RCELREPHB': u'?',#TODO (7hb)
    'RCELREPHD': u'?',#TODO (7hd)
    'RCELREPHE': u'?',#TODO (7he)
    'RCELREPHF': u'?',#TODO (7hf)
    'RCELREPHG': u'?',#TODO (7hg)
    'RCELREPHH': u'?',#TODO (7hh)
    'RCELREPHR': u'?',#TODO (scellier)
    'RCELREPHS': u'?',#TODO (7hs)
    'RCELREPHT': u'?',#TODO (7ht)
    'RCELREPHU': u'?',#TODO (7hu)
    'RCELREPHV': u'?',#TODO (7hv)
    'RCELREPHW': u'?',#TODO (7hw)
    'RCELREPHX': u'?',#TODO (7hx)
    'RCELREPHZ': u'?',#TODO (7hz)
    'RCELRRED09': u'?',#TODO (7la)
    'RCELRREDLA': u'?',#TODO (scellier)
    'RCELRREDLB': u'?',#TODO (f7lb)
    'RCELRREDLC': u'?',#TODO (f7lc)
    'RCELRREDLD': u'?',#TODO (7ld)
    'RCELRREDLE': u'?',#TODO (7le)
    'RCELRREDLF': u'?',#TODO (7lf)
    'RCELRREDLM': u'?',#TODO (7lm)
    'RCELRREDLS': u'?',#TODO (7ls)
    'RCELRREDLZ': u'?',#TODO (f7lz)
    'RCELRREDMG': u'?',#TODO (7mg)
    'RCINE': u'?',#TODO (7gn)
    'RCODELOP': u'?',#TODO (7uh)
    'RCODJT': u'?',#TODO (7jt)
    'RCODJU': u'?',#TODO (7jt)
    'RCODJV': u'?',#TODO (7jv)
    'RCODJW': u'?',#TODO (7jw)
    'RCODJX': u'?',#TODO (7jx)
    'RCOLENT': u'?',#TODO (7ls)
    'RCONS': u'?',#TODO (7uh)
    'RCOTFOR': u'?',#TODO (7ul)
    'RDIFAGRI': u'?',#TODO (7um)
    'RDONS': u'?',#TODO (7uf)
    'RDUFLOGIH': u'?',#TODO (7gh)
    'REI': u'?',#TODO (f8tf)
    'REVKIRE': u'Revenu fiscal de référence',
    'RFCPI': u'?',#TODO (7gq)
    'RFIPC': u'?',#TODO (7fm)
    'RFOR': u'?',#TODO (f7up)
    'RFORET': u'?',#TODO (f7uc)
    'RHEBE': u'?',#TODO (7ce)
    'RIDOMENT': u'?',#TODO (7ur)
    'RIDOMPROE1': u'?',#TODO (f7sz)
    'RIDOMPROE2': u'?',#TODO (f7qz)
    'RIDOMPROE3': u'?',#TODO (f7qz)
    'RIDOMPROE4': u'?',#TODO (f7oz)
    'RIDOMPROE5': u'?',#TODO (f7oz)
    'RILMIA': u'?',#TODO (7ia)
    'RILMIB': u'?',#TODO (7ib)
    'RILMIC': u'?',#TODO (7ic)
    'RILMIH': u'?',#TODO (7ih)
    'RILMIX': u'?',#TODO (7ix)
    'RILMIZ': u'?',#TODO (7iz)
    'RILMJI': u'?',#TODO (7ji)
    'RILMJS': u'?',#TODO (7ji)
    'RILMJV': u'?',#TODO
    'RILMJW': u'?',#TODO
    'RILMJX': u'?',#TODO
    'RINNO': u'?',#TODO (7gq)
    'RINVDOMTOMLG': u'?',#TODO (f7ui)
    'RINVRED': u'?',#TODO (7it)
    'RLOCIDEFG': u'?',#TODO (7id)
    'RLOGDOM': u'?',#TODO (f7qd)
    'RMEUBLE': u'?',#TODO (7ik)
    'RNI': u'?',#TODO
    'RNICOL': u'Revenu net imposable ou déficit à reporter',
    'RNOUV': u'?',#TODO (cappme)
    'RPATNAT': u'?',#TODO (7ka)
    'RPATNATOT': u'?',#TODO (7ka)
    'RPRESCOMPREP': u'?',#TODO (7wp)
    'RPROREP': u'?',#TODO (7is)
    'RRBG': u'Revenu brut global ou déficit',
    'RRDOM': u'?',#TODO (7ub)
    'RREDMEUB': u'?',#TODO (7is)
    'RREDREP': u'?',#TODO (7iu)
    'RREPA': u'?',#TODO (7ud)
    'RREPMEU': u'?',#TODO (7ip)
    'RREPNPRO': u'?',#TODO (7ir)
    'RRESIMEUB': u'?',#TODO (7io)
    'RRESINEUV': u'?',#TODO (7ij)
    'RRESIVIEU': u'?',#TODO (7im)
    'RRESTIMO': u'?',#TODO (7rd)
    'RRIRENOV': u'?',#TODO (7nz)
    'RRPRESCOMP': u'?',#TODO (7wp)
    'RSOCREPR': u'?',#TODO (7fh)
    'RSOUFIP':  u'?',#TODO (7fq)
    'RSURV': u'?',#TODO (7gz)
    'RTELEIR': u'?',#TODO (7ul)
    'RTITPRISE': u'?',#TODO (7cu)
    'RTOUHOTR': u'?', #TODO (7xk)
    'RTOUR': u'?',#TODO (f7xd)
    'RTOUREPA': u'?', #TODO (7xj)
    'RTOURES': u'?',#TODO (f7xc)
    'RTOURHOT': u'?',#TODO (f7xc)
    'RTOURNEUF': u'?', #TODO (f7xc)
    'RTOURREP': u'?', #TODO (7xi)
    'RTOURTRA': u'?',#TODO (f7xc)
    'TEFF': u'?',#TODO (ebnc_impo)
    'TOTPAC': u'Nombre de personnes à charge',
    'TXMARJ': u'Taux marginal d\'imposition',
    'TXMOYIMP': u'Taux moyen d\'imposition',
}

household_income_variables_to_test = [ # NB: taken from input variables of FELIN-ERFS Survey Scenario (TAXIPP) 2014
    # TODO : fix following errors
    # 'f2ab', 'f2bg', CREDIT D'IMPOT (2AB) > 80 EUROS SANS REVENU CORRESPONDANT
    # 'f2bh', LE MONTANT 2BH NE PEUT ETRE > AU TOTAL 2DC + 2CH + 2TS + 2TR</UL>
    # 'f2tr', LE MONTANT 7UM NE PEUT ETRE SUPERIEUR AU REVENU 2TR
    # 'f2ck', CREDIT D'IMPOT 2CK > 80 E SANS REVENU CORRESPONDANT</UL>
    # 'f3ve', MONTANT LIGNE 3VE POUR UN CONTRIBUABLE NON DOMICILIE DANS UN DOM</UL>
    # 'f4be', LE MONTANT PORTE LIGNE 4BE NE PEUT DEPASSER 15000
    # 'f4bf', MONTANT PORTE LIGNE 4BF SANS REVENU OU DEFICIT FONCIER CORRESPONDANT
    # 'f7uo', LA LIGNE 7UO EST REMPLIE SANS REVENU CORRESPONDANT
    # 'f3sa',
    # 'f7ea', 'f7eb','f7ec', 'f7ef', 'f7eg', 'f7ed', TODO: to test these => need to adjust scenario (nbpac)
    # 'f7ff', 'f7fg', TODO: f7fg = number of exploitations (must be < 10) (not an income)
    # 'f7fl', TODO: to test this => need to be living in the DOMs
    # 'f7is', 'f7iu', 'f7ix', 'f7iy',
    # 'f7jy', TODO: f7jy must be < 16
    # 'f7ly', 'f7my', => number of conventions d'aides aux créateurs d'entreprises (not an income)
    # 'f7nx', 'f7ny', TODO : to test this => f7ny must be < f7nx
    # 'f7qh', 'f7qi', TODO : to test this => f7qi must be < f7qh
    # 'f7qr', 'f7qq', TODO : to test this => f7qr must be < f7qq
    # 'f7ri', 'f7rh', TODO : to test this => f7ri must be < f7rh
    # 'f7ro', 'f7rn', idem
    # 'f7rt', 'f7rs', idem
    # 'f7ry', 'f7rx', idem
    # 'f7sh', 'f7sd', 'f7se', 'f7sg', TODO: to check
    # 'f7sj', 'f7sk', 'f7sl',
    # 'f7um', LE MONTANT 7UM NE PEUT ETRE SUPERIEUR AU REVENU 2TR
    # 'f7uk', CREDIT INTERETS PRET ETUDIANT (7UK,7TD) AVEC VOUS ET CONJOINT NES AVANT 1979
    # 'f7us', LA LIGNE 7US EST REMPLIE SANS REVENU CORRESPONDANT
    # 'f7ut', CASE 7 UT COCHEE SANS PRISE EN CHARGE MONTANT LIGNE 7 UP
    # 'f7vo', 'f7td',  SAISIE DU CODE 7VO SANS PRISE EN CHARGE DE MONTANT LIGNE 7TD ET INVERSEMENT
    # 'f7vg', CASE 7VG COCHEE SANS MONTANT LIGNE 7SH
    # 'f7wc', CASE 7WC COCHEE SANS MONTANT LIGNE 7SG<
    # 'f7we', 'f7wg', CASE 7WE OU 7WG COCHEE SANS PRISE EN CHARGE LIGNES 7WH, 7WK, 7WF, 7WQ, 7WR
    # 'f7wh', CASE 7WH COCHEE SANS MONTANT LIGNE 7SD A 7ST
    # 'f7wk', CASE 7WK COCHEE SANS MONTANT LIGNE 7SD A 7SW
    # 'f7wm', LE MONTANT 7WM EST INFERIEUR AU MONTANT 7WN
    # 'f7wn', 'f7wo', PRESENCE D UN MONTANT LIGNE 7WN SANS MONTANT 7WO OU RECIPROQUEMENT
    # 'f8tb', LES LIGNES 8TB, 8TC SONT REMPLIES SANS REVENU CORRESPONDANT
    # 'f8te', 'f8tg', 'f8ts', 'f8uy', 'f8wa', 'f8we', 'f8wd', 'f8wc', 'f8wb', 'f8wt', 'f8wr', LA LIGNE 8TE EST REMPLIE SANS REVENU CORRESPONDANT
    # 'f8tk', LA LIGNE 8TK EST REMPLIE SANS PRISE EN CHARGE DE 8XR, 8XP OU 8XQ
    # 'f7sb', LIGNE 7 SB, 7 SH, 7 SD, 7 SE, 7 SG SANS PRISE EN CHARGE DU CHIFFRE 7 SA
    # 'f7wv', CASE 7WU 7WV COCHEE SANS MONTANT LIGNE 7SK ET RECIPROQUEMENT
    # 'f7ww', CASE 7WW 7WX COCHEE SANS MONTANT LIGNE 7SL ET RECIPROQUEMENT
    # ES LIGNES 8TL, 8UW SONT REMPLIES SANS REVENU CORRESPONDANT
    'f1ar', 'f1br', 'f1cr', 'f1dr', 'f1er', 'f1aw', 'f1bw', 'f1cw', 'f1dw',
    'f2aa', 'f2al', 'f2am', 'f2an', 'f2aq', 'f2ar', 'f2dm',
    'f2ch', 'f2cg', 'f2dc', 'f2ts', 'f2ca', 'f2fu', 'f2go', 'f2gr', 'f2da', 'f2dh', 'f2ee',
    'f3vg', 'f3vh', 'f3vm', 'f3vt', 'f3vc', 'f3vf', 'f3vi', 'f3vj', 'f3vz', 'f3vp', 'f3vy',
    'f3sg', 'f3sh', 'f3sl', 'f3sm',
    'f4ba', 'f4bb', 'f4bc', 'f4bd', 'f4tq',
    'f5ga', 'f5gb', 'f5gc', 'f5gd', 'f5ge', 'f5gf', 'f5gg', 'f5gh', 'f5gi', 'f5gj',
    'f5ht', 'f5it', 'f5jt', 'f5kt', 'f5lt', 'f5mt', 
    'f5qf', 'f5qg', 'f5qn', 'f5qo', 'f5qp', 'f5qq',
    'f5rn', 'f5rn', 'f5rp', 'f5rq', 'f5rr', 'f5rw',
    'f7wj', 'f7wl', 'f7wr', 'f7ga', 'f7gb', 'f7gc', 'f7ge', 'f7gf', 'f7gg', 'f7bm', 'f7cb',
    'f7ah', 'f7tn', 'f7bc', 'f7vh', 'f7sa', 'f7qb', 'f7ql', 'f7pi', 
    'f7ui', 'f7pa', 'f7cy', 'f7dy', 'f7ey', 'f7yz', 'f7ym', 'f7lt',
    'f7rr', 'f7rq', 'f7rp', 'f7rw', 'f7rv', 'f7ru', 'f7rc', 'f7rb', 'f7ra', 'f7rg', 'f7rf', 'f7re', 'f7rd', 'f7rk', 'f7rj', 'f7rm', 'f7rl', 'f6fl', 'f6fb', 'f6fc', 'f6fa', 'f6fd', 'f6fe', 'f6ps', 'f7gx', 'f7gz', 'f7gt', 'f7gu', 'f7gv', 'f7gw', 'f7gp', 'f7gq', 'f7gs', 'f7gl', 'f7gn', 'f7gh', 'f7gi', 'f7gj', 'f7gk', 'f7ge', 'f7gf', 'f7gg', 'f7gc', 'f8tz', 'f8tp', 'f8th', 'f8ti', 'f8to', 'f8ta', 'f8tf', 'f8td', 'f7ng', 'f7nf', 'f7ne', 'f7nd', 'f7nc', 'f7nb', 'f7na', 'f7no', 'f7nn', 'f7nm', 'f7nl', 'f7nk', 'f7nj', 'f7ni', 'f7nh', 'f7nw', 'f7nv', 'f7nu', 'f7nt', 'f7ns', 'f7nr', 'f7nq', 'f7np', 'f7nz',  'f7uh', 'f7un', 'f7ul', 'f7uc', 'f7uf', 'f7uz', 'f7ux', 'f7uy', 'f7up', 'f7uq', 'f7uv', 'f7uw', 'f7uu', 'f7jk', 'f7jj', 'f7ji', 'f7jh', 'f7jo', 'f7jn', 'f7jm', 'f7jl', 'f7jc', 'f7jb', 'f7ja', 'f7jg', 'f7jf', 'f7je', 'f7jd', 'f7jx', 'f7js', 'f7jr', 'f7jq', 'f7jp', 'f7jw', 'f7jv', 'f7ju', 'f7jt', 'f7cc', 'f7cd', 'f7ce', 'f7cf', 'f7cl', 'f7cm', 'f7cn', 'f7cq', 'f7cu', 'f7xf', 'f7xi', 'f7xk', 'f7xj', 'f7xm', 'f7xo', 'f7xn', 'f7xq', 'f7xp', 'f7xs', 'f7xr', 'f7xu', 'f7xt', 'f7xw', 'f7xv', 'f7xy', 'f7xz', 'f6hj', 'f6hk', 'f6hl', 'f6hm', 'f7qx', 'f7qw', 'f7qu', 'f7qs', 'f7qj', 'f7qf', 'f7qg', 'f6gi', 'f6gh', 'f6gj', 'f6gu', 'f6gp', 'f7ma', 'f7mg', 'f7fq', 'f7fn', 'f7fm', 'f7fh', 'f7fd', 'f7fc', 'f7fb', 'f7fa', 'f7te', 'f7tg', 'f7th', 'f6dd', 'f6de', 'f6cb', 'f7iv', 'f7iw', 'f7it', 'f7ir', 'f7ip', 'f7iq', 'f7iz', 'f7if', 'f7ig', 'f7id', 'f7ie', 'f7ib', 'f7ic', 'f7ia', 'f7in', 'f7io', 'f7il', 'f7im', 'f7ij', 'f7ik', 'f7ih', 'f7py', 'f7wl', 'f7wj', 'f7wp', 'f7wr', 'f6eu', 'f6em', 'f6el', 'f7lm', 'f7li', 'f7le', 'f7ld', 'f7lg', 'f7lf', 'f7la', 'f7lc', 'f7lb', 'f7lz', 'f7ls', 'f8wu', 'f7sp', 'f7sq', 'f7sr', 'f7ss', 'f7st', 'f7su', 'f7sv', 'f7sw', 'f7sx', 'f7sy', 'f7sz', 'f7sf',  'f7si', 'f7sm', 'f7sn', 'f7so', 'f7oa', 'f7ob', 'f7oc', 'f7ol', 'f7om', 'f7on', 'f7oo', 'f7oh', 'f7oi', 'f7oj', 'f7ok', 'f7ot', 'f7ou', 'f7ov', 'f7ow', 'f7op', 'f7oq', 'f7or', 'f7os', 'f7hs', 'f7hr', 'f7hu', 'f7ht', 'f7hw', 'f7hv', 'f7hx', 'f7hz', 'f7ha', 'f7hb', 'f7he', 'f7hd', 'f7hg', 'f7hf', 'f7hh', 'f7hk', 'f7hj', 'f7hm', 'f7hl', 'f7ho', 'f7hn', 'f7ac', 'f7vc', 'f7va', 'f7vz', 'f7vy', 'f7vx', 'f7vw', 'f7vv', 'f7vu', 'f7vt', 'f7kh', 'f7ki', 'f7ka', 'f7kb', 'f7kc', 'f7kd', 'f7ks', 'f7df', 'f7db',  
    'f8ta', 'f8vl', 'f8vm', 'f8uz', 
]

individual_income_variables_to_test = [ # NB: taken from input variables of FELIN-ERFS Survey Scenario (TAXIPP) 2014
    # 'f1tv', 'f1tw', 'f1tx',  => individual incomes but not with this name.. TO CHECK
    #'f6ev', 'f6rs', 'f6ss', 'f7dg', 'f7dl', 'f7dq', 
    #'ppe_tp_ns',  # TODO , update OpenFisca-france def of ppe_tp_ns (wrong stop_date) # WARNING : DGFiP calculator does not like this one
    #'ppe_tp_sa', # WARNING : DGFiP calculator does not like this one
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
    'alnp_defs',  # TODO , update OpenFisca-france def of alnp_defs (wrong stop_date)
    'alnp_imps', 
    'arag_defi', 
    'arag_exon', 
    'arag_impg', 
    'arag_pvce', 
    'cbnc_assc',  
    'chomage_imposable',
    'cncn_aimp', 
    'cncn_bene', 
    'cncn_defi',  # TODO, check (f5nr)
    'cncn_exon', 
    'cncn_info', 
    'cncn_jcre', 
    'cncn_pvce', 
    'ebic_imps',  # TODO , update OpenFisca-france def of ebic_imps (wrong stop_date)
    'ebic_impv',  # TODO , update OpenFisca-france def of ebic_impv (wrong stop_date)
    'ebnc_impo',  # TODO , update OpenFisca-france def of ebnc_impo (wrong stop_date)
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
    'nacc_meup',  #TODO , check
    'nacc_pvce',  # TODO , update OpenFisca-france def of nacc_pvce (wrong stop_date)
    'nbic_apch', 
    'nbic_defn', 
    'nbic_defs',
    'nbic_exon', 
    'nbic_impm', 
    'nbic_impn', 
    'nbic_imps',  # TODO , wrong 2014 definition
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
    'nrag_pvce',  # WARNING , 5hk, 5ik, 5jk can be either (nrag_pvce) either (cncn_exon) depending on the year => TODO, handle this
    'pensions_alimentaires_percues',
    'pensions_invalidite',
    'ppe_du_ns',  # TODO , update OpenFisca-france def of ppe_du_ns (wrong stop_date)
    'ppe_du_sa',
    'pveximpres',  
    'retraite_imposable',
    'retraite_titre_onereux',
    'revimpres',
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

        if foyer_fiscal.pop('caseT', False):
            impots_arguments['0BT'] = '1'

        for column_code, value in foyer_fiscal.iteritems():
            if column_code == 'id':
                continue
            if column_code == 'f7uf':
                impots_arguments['7UG'] = str(value)  # bug dans le site des impots
            if column_code == 'f7ud':
                impots_arguments['7UE'] = str(value)  # bug dans le site des impots
            if column_code == 'f7vc':
                impots_arguments['7VD'] = str(value)  # bug dans le site des impots
            column = tax_benefit_system.variables[column_code]
            cerfa_field = column.cerfa_field
            assert cerfa_field is not None and isinstance(cerfa_field, basestring), column_code
            impots_arguments[cerfa_field] = int(value) if isinstance(value, bool) else value

    return impots_arguments
