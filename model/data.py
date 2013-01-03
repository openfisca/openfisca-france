# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from src.core.description import ModelDescription
from src.core.columns import IntCol, EnumCol, BoolCol, AgesCol, FloatCol
from src.core.utils_old import Enum

QUIFOY = Enum(['vous', 'conj', 'pac1','pac2','pac3','pac4','pac5','pac6','pac7','pac8','pac9'])
QUIFAM = Enum(['chef', 'part', 'enf1','enf2','enf3','enf4','enf5','enf6','enf7','enf8','enf9'])
QUIMEN = Enum(['pref', 'cref', 'enf1','enf2','enf3','enf4','enf5','enf6','enf7','enf8','enf9'])
CAT    = Enum(['noncadre', 'cadre', 'etat_t', 'colloc_t', 'contract']) 


class InputTable(ModelDescription):
    '''
    Socio-economic data
    Données d'entrée de la simulation à fournir à partir d'une enquête ou 
    générée par le  générateur de cas type
    '''
    noi = IntCol()

    idmen   = IntCol() # 600001, 600002,
    idfoy   = IntCol() # idmen + noi du déclarant
    idfam   = IntCol() # idmen + noi du chef de famille

    quimen  = EnumCol(QUIMEN)
    quifoy  = EnumCol(QUIFOY)
    quifam  = EnumCol(QUIFAM)
    
    sali = IntCol(label="Salaire imposable", val_type="monetary") #(f1aj, f1bj, f1cj, f1dj, f1ej)
    choi = IntCol(label=u"Chômage imposable", val_type="monetary") # (f1ap, f1bp, f1cp, f1dp, f1ep)
    rsti = IntCol(label="Retraite imposable", val_type="monetary") # (f1as, f1bs, f1cs, f1ds, f1es)
    fra  = IntCol( val_type="monetary") # (f1ak, f1bk, f1ck, f1dk, f1ek)

    alr  = IntCol(label = u"Pension alimentaire reçue", val_type="monetary") # (f1ao, f1bo, f1co, f1do, f1eo)
    
    hsup = IntCol( val_type="monetary")  # f1au
    inv  = BoolCol(label = u'invalide')
    alt  = BoolCol(label = u'garde alternée')
    cho_ld = BoolCol(label = 'chômeur de longue durée') # (f1ai, f1bi, f1ci, f1di, f1ei)
    ppe_tp_sa = BoolCol() # (f1ax, f1bx, f1cx, f1dx, f1qx)
    ppe_tp_ns = BoolCol() # (f5nw, f5ow, f5pw)
    ppe_du_sa = IntCol() # (f1av, f1bv, f1cv, f1dv, f1qv)
    ppe_du_ns = IntCol() # (f5nv, f5ov, f5pv)
    jour_xyz = IntCol(default = 360)
    age = AgesCol(label = u"âge" ,  val_type="age")
    agem = AgesCol(label = u"âge (en mois)", val_type="months")
    
    zone_apl = EnumCol(label = u"zone apl", default = 2, unit= 'menage')
    loyer = IntCol(unit='men', val_type="monetary") # Loyer mensuel
    so = EnumCol(label = u"Statut d'occupation",
                 unit='men',
                 enum = Enum([u"Non renseigné",
                              u"Accédant à la propriété",
                              u"Propriétaire (non accédant) du logement",
                              u"Locataire d'un logement HLM",
                              u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
                              u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
                              u"Logé gratuitement par des parents, des amis ou l'employeur"]))
    
    activite = EnumCol(label = u'Actvité',
                       enum = Enum([u'Actif occupé',
                                    u'Chômeur',
                                    u'Étudiant, élève', 
                                    u'Retraité', 
                                    u'Autre inactif']), default = 4) 
    
    titc = EnumCol(label = u"Statut, pour les agents de l'Etat des collectivités locales, ou des hôpitaux",
                    enum = Enum([u"Sans objet ou non renseigné",
                                u"Elève fonctionnaire ou stagiaire",
                                u"Agent titulaire",
                                u"Contractuel"]))
    statut = EnumCol(label = u"Statut détaillé mis en cohérence avec la profession",
                    enum = Enum([u"Sans objet",
                                u"Indépendants",
                                u"Employeurs",
                                u"Aides familiaux",
                                u"Intérimaires",
                                u"Apprentis",
                                u"CDD (hors Etat, coll.loc.), hors contrats aides",
                                u"Stagiaires et contrats aides (hors Etat, coll.loc.)",
                                u"Autres contrats (hors Etat, coll.loc.)",
                                u"CDD (Etat, coll.loc.), hors contrats aides",
                                u"Stagiaires et contrats aides (Etat, coll.loc.)",
                                u"Autres contrats (Etat, coll.loc.)",
                                ]))

    txtppb = EnumCol(label = u"Taux du temps partiel",
                enum = Enum([u"Sans objet",
                            u"Moins d'un mi-temps (50%)",
                            u"Mi-temps (50%)",
                            u"Entre 50 et 80%",
                            u"80%",
                            u"Plus de 80%"]))


    nbsala = EnumCol(label = u"Nombre de salariés dans l'établissement de l'emploi actuel",
                    enum = Enum([u"Sans objet",
                                u"Aucun salarié",
                                u"1 à 4 salariés",
                                u"5 à 9 salariés",
                                u"10 à 19 salariés",
                                u"20 à 49 salariés",
                                u"50 à 199 salariés",
                                u"200 à 499 salariés",
                                u"500 à 999 salariés",
                                u"1000 salariés ou plus",
                                u"Ne sait pas",
                                ]))

    chpub = EnumCol(label = u"Nature de l'employeur principal",
                enum = Enum([u"Sans objet",
                            u"Etat",
                            u"Collectivités locales, HLM",
                            u"Hôpitaux publics",
                            u"Particulier",
                            u"Entreprise publique (La Poste, EDF-GDF, etc.)",
                            u"Entreprise privée, association"
                            ]))
    
    cadre = BoolCol(label = u"Cadre")
    
    
    boursier = BoolCol()
    code_postal = IntCol(unit='men')
    
    statmarit = EnumCol(label = u"Statut marital",
                          default = 2,
                          enum = Enum([u"Marié",
                                    u"Célibataire",
                                    u"Divorcé",
                                    u"Veuf",
                                    u"Pacsé",
                                    u"Jeune veuf"],start=1))
    
    nbR = IntCol(unit= 'foy')
    nbJ = IntCol(unit= 'foy')
    nbI = IntCol(unit= 'foy')
    nbH = IntCol(unit= 'foy')
    nbG = IntCol(unit= 'foy')
    nbF = IntCol(unit= 'foy')
    nbN = IntCol(unit= 'foy')
    
    caseE = BoolCol(unit= 'foy')
    caseF = BoolCol(unit= 'foy')
    caseG = BoolCol(unit= 'foy')
    caseH = IntCol(unit= 'foy')
    caseK = BoolCol(unit= 'foy')
    caseL = BoolCol(unit= 'foy')
    caseN = BoolCol(unit= 'foy')
    caseP = BoolCol(unit= 'foy')
    caseS = BoolCol(unit= 'foy')
    caseT = BoolCol(unit= 'foy')
    caseW = BoolCol(unit= 'foy')
    
    
    rfr_n_2  = IntCol(unit='foy', label = u"Revenu fiscal de référence année n-2", val_type="monetary") # TODO: provide in data
    nbptr_n_2 = IntCol(unit='foy', label = u"Nombre de parts année n-2", val_type="monetary")  # TODO: provide in data
    
    # Rentes viagères
    f1aw = IntCol(unit= 'foy', val_type="monetary")
    f1bw = IntCol(unit= 'foy', val_type="monetary")
    f1cw = IntCol(unit= 'foy', val_type="monetary")
    f1dw = IntCol(unit= 'foy', val_type="monetary")
    
    f1tv = IntCol(unit= 'foy', val_type="monetary")
    f1uv = IntCol(unit= 'foy', val_type="monetary")
    f1tw = IntCol(unit= 'foy', val_type="monetary")
    f1uw = IntCol(unit= 'foy', val_type="monetary")
    f1tx = IntCol(unit= 'foy', val_type="monetary")
    f1ux = IntCol(unit= 'foy', val_type="monetary")
    
    # RVCM
    # revenus au prélèvement libératoire
    f2da = IntCol(unit = 'foy', label = u"Revenus des actions et parts soumis au prélèvement libératoire", val_type="monetary")
    f2dh = IntCol(unit = 'foy', val_type="monetary")
    f2ee = IntCol(unit = 'foy', label = u"Revenus au prélèvement libératoire hors actions et assurance-vie", val_type="monetary")

    # revenus ouvrant droit à abattement
    f2dc = IntCol(unit = 'foy', label =u"Revenus des actions et parts donnant droit à abattement", val_type="monetary")
    f2fu = IntCol(unit = 'foy', val_type="monetary")
    f2ch = IntCol(unit = 'foy', val_type="monetary")
    
    # Revenus n'ouvrant pas droit à abattement
    f2ts = IntCol(unit = 'foy', val_type="monetary")
    f2go = IntCol(unit = 'foy', val_type="monetary")
    f2tr = IntCol(unit = 'foy', label = u"Intérêts et autres revenus assimilés", val_type="monetary")
    
    # Autres
    f2cg = IntCol(unit= 'foy', val_type="monetary")
    f2bh = IntCol(unit= 'foy', val_type="monetary")
    f2ca = IntCol(unit= 'foy', val_type="monetary")
    f2aa = IntCol(unit='foy', val_type="monetary")
    f2ab = IntCol(unit= 'foy', val_type="monetary")
    f2al = IntCol(unit= 'foy', val_type="monetary")
    f2am = IntCol(unit= 'foy', val_type="monetary")
    f2an = IntCol(unit= 'foy', val_type="monetary")
    # non accessible (from previous years)
    f2gr = IntCol(unit= 'foy', val_type="monetary") 
        
    f3vc = IntCol(unit= 'foy', val_type="monetary")
    f3vd = IntCol(unit= 'foy', val_type="monetary")
    f3ve = IntCol(unit= 'foy', val_type="monetary")
    f3vf = IntCol(unit= 'foy')    
    
    f3vl = IntCol(unit= 'foy', val_type="monetary")
    f3vi = IntCol(unit= 'foy', val_type="monetary")
    f3vm = IntCol(unit= 'foy', val_type="monetary")
    
    f3vj = IntCol(unit= 'foy', val_type="monetary")
    f3vk = IntCol(unit= 'foy', val_type="monetary")
    f3va = IntCol(unit= 'foy', val_type="monetary")
    
    # Plus values et gains taxables à 18%
    f3vg = IntCol(unit= 'foy', val_type="monetary")
    f3vh = IntCol(unit= 'foy', val_type="monetary")
    f3vt = IntCol(unit= 'foy', val_type="monetary")
    f3vu = IntCol(unit= 'foy', val_type="monetary")
    f3vv = IntCol(unit= 'foy', val_type="monetary")

    # Revenu foncier
    f4ba = IntCol(unit= 'foy', val_type="monetary")
    f4bb = IntCol(unit= 'foy', val_type="monetary")
    f4bc = IntCol(unit= 'foy', val_type="monetary")
    f4bd = IntCol(unit= 'foy', val_type="monetary")
    f4be = IntCol(unit= 'foy', val_type="monetary")
    
    # Prime d'assurance loyers impayés
    f4bf = IntCol(unit= 'foy', val_type="monetary")
    
    f4bl = IntCol(unit= 'foy', val_type="monetary")
    
    f5qm = IntCol(unit= 'foy', val_type="monetary")
    f5rm = IntCol(unit= 'foy', val_type="monetary")
    
    # Csg déductible
    f6de = IntCol(unit= 'foy', val_type="monetary")

    # Pensions alimentaires
    f6gi = IntCol(unit= 'foy', val_type="monetary")
    f6gj = IntCol(unit= 'foy', val_type="monetary")
    f6el = IntCol(unit= 'foy', val_type="monetary")
    f6em = IntCol(unit= 'foy', val_type="monetary")
    f6gp = IntCol(unit= 'foy', val_type="monetary")
    f6gu = IntCol(unit= 'foy', val_type="monetary")
    
    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    f6eu = IntCol(unit= 'foy', val_type="monetary")
    f6ev = IntCol(unit= 'foy')
    
    # Déductions diverses
    f6dd = IntCol(unit= 'foy', val_type="monetary")
    
    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    f6ps = IntCol(unit= 'foy', val_type="monetary")
    f6rs = IntCol(unit= 'foy', val_type="monetary")
    f6ss = IntCol(unit= 'foy', val_type="monetary")
    f6pt = IntCol(unit= 'foy', val_type="monetary")
    f6rt = IntCol(unit= 'foy', val_type="monetary")
    f6st = IntCol(unit= 'foy', val_type="monetary")
    f6pu = IntCol(unit= 'foy', val_type="monetary")
    f6ru = IntCol(unit= 'foy', val_type="monetary")
    f6su = IntCol(unit= 'foy', val_type="monetary")
    
    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    f6aa = IntCol(unit= 'foy', val_type="monetary")
    
    # Souscriptions au capital des SOFIPÊCHE
    f6cc = IntCol(unit= 'foy', val_type="monetary")
    
    # Investissements DOM-TOM dans le cadre d’une entreprise <= 2005
    # ou Versements sur un compte épargne codéveloppement 
    f6eh = IntCol(unit= 'foy', val_type="monetary")
    
    # Pertes en capital consécutives à la souscription au capital de sociétés 
    # nouvelles ou de sociétés en difficulté
    f6da = IntCol(unit= 'foy', val_type="monetary")
    
    
    # Dépenses de grosses réparations effectuées par les nus propriétaires
    f6cb = IntCol(unit= 'foy', val_type="monetary")
    f6hj = IntCol(unit= 'foy', val_type="monetary")
    
    # Sommes à rajouter au revenu imposable
    f6gh = IntCol(unit= 'foy', val_type="monetary")    
    
    # Deficit Antérieur
    f6fa = IntCol(unit= 'foy', val_type="monetary")
    f6fb = IntCol(unit= 'foy', val_type="monetary")
    f6fc = IntCol(unit= 'foy', val_type="monetary")
    f6fd = IntCol(unit= 'foy', val_type="monetary")
    f6fe = IntCol(unit= 'foy', val_type="monetary")
    f6fl = IntCol(unit= 'foy', val_type="monetary")
    
    # Dons
    f7ud = IntCol(unit= 'foy', val_type="monetary")
    f7uf = IntCol(unit= 'foy', val_type="monetary")
    f7xs = IntCol(unit= 'foy', val_type="monetary")
    f7xt = IntCol(unit= 'foy', val_type="monetary")
    f7xu = IntCol(unit= 'foy', val_type="monetary")
    f7xw = IntCol(unit= 'foy', val_type="monetary")
    f7xy = IntCol(unit= 'foy', val_type="monetary")
    
    # Cotisations syndicales des salariées et pensionnés
    f7ac = IntCol(unit= 'foy', val_type="monetary")
    f7ae = IntCol(unit= 'foy', val_type="monetary")
    f7ag = IntCol(unit= 'foy', val_type="monetary")

    # Salarié à domicile
    f7db = IntCol(unit= 'foy', val_type="monetary")
    f7df = IntCol(unit= 'foy', val_type="monetary")
    f7dq = IntCol(unit= 'foy', val_type="monetary")
    f7dg = BoolCol(unit= 'foy')
    f7dl = IntCol(unit= 'foy', val_type="monetary")
    
    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    f7vy = IntCol(unit= 'foy', val_type="monetary")
    f7vz = IntCol(unit= 'foy', val_type="monetary")
    f7vx = IntCol(unit= 'foy', val_type="monetary")
    f7vw = IntCol(unit= 'foy', val_type="monetary")

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    f7cd = IntCol(unit= 'foy', val_type="monetary")
    f7ce = IntCol(unit= 'foy', val_type="monetary")

    # Frais de garde des enfants de moins de 6 ans
    f7ga = IntCol(unit= 'foy', val_type="monetary")
    f7gb = IntCol(unit= 'foy', val_type="monetary")
    f7gc = IntCol(unit= 'foy', val_type="monetary")
    f7ge = IntCol(unit= 'foy', val_type="monetary")
    f7gf = IntCol(unit= 'foy', val_type="monetary")
    f7gg = IntCol(unit= 'foy', val_type="monetary")

    # Nombre d'enfants à charge poursuivant leurs études
    f7ea = IntCol(unit= 'foy')
    f7eb = IntCol(unit= 'foy')
    f7ec = IntCol(unit= 'foy')
    f7ed = IntCol(unit= 'foy')
    f7ef = IntCol(unit= 'foy')
    f7eg = IntCol(unit= 'foy')

    # Intérêts des prêts étudiants
    f7td = IntCol(unit= 'foy', val_type="monetary")
    f7vo = IntCol(unit= 'foy', val_type="monetary")
    f7uk = IntCol(unit= 'foy', val_type="monetary")
    
    # Primes de survies, contrat d'épargne handicap
    f7gz = IntCol(unit= 'foy', val_type="monetary")
    
    # Prestations compensatoires
    f7wm = IntCol(unit= 'foy', val_type="monetary")
    f7wn = IntCol(unit= 'foy', val_type="monetary")
    f7wo = IntCol(unit= 'foy', val_type="monetary")
    f7wp = IntCol(unit= 'foy', val_type="monetary")
    
    # Dépenses en faveur de la qualité environnementale
    f7we = IntCol(unit= 'foy', val_type="monetary")
    f7wq = IntCol(unit= 'foy', val_type="monetary")
    f7wh = IntCol(unit= 'foy', val_type="monetary")
    f7wk = IntCol(unit= 'foy', val_type="monetary")
    f7wf = IntCol(unit= 'foy', val_type="monetary")
    
    # Dépenses en faveur de l'aide aux personnes
    f7wi = IntCol(unit= 'foy', val_type="monetary")
    f7wj = IntCol(unit= 'foy', val_type="monetary")
    f7wl = IntCol(unit= 'foy', val_type="monetary")
    
    # Investissements dans les DOM-TOM dans le cadre d'une entrepise  TODO: RESTART FROM HERE FOR , val_type="monetary"
    f7ur = IntCol(unit= 'foy')
    f7oz = IntCol(unit= 'foy')
    f7pz = IntCol(unit= 'foy')
    f7qz = IntCol(unit= 'foy')
    f7rz = IntCol(unit= 'foy')
    f7sz = IntCol(unit= 'foy')
    
    # Aide aux créateurs et repreneurs d'entreprises
    f7fy = IntCol(unit= 'foy')
    f7gy = IntCol(unit= 'foy')
    f7jy = IntCol(unit= 'foy')
    f7hy = IntCol(unit= 'foy')
    f7ky = IntCol(unit= 'foy')
    f7iy = IntCol(unit= 'foy')
    f7ly = IntCol(unit= 'foy')
    f7my = IntCol(unit= 'foy')

    # Travaux de restauration immobilière
    f7ra = IntCol(unit= 'foy')
    f7rb = IntCol(unit= 'foy')
    
    # Assurance-vie
    f7gw = IntCol(unit= 'foy')
    f7gx = IntCol(unit= 'foy')
    # f7gy = IntCol() existe ailleurs

    # Investissements locatifs dans le secteur de touristique            
    f7xc = IntCol(unit= 'foy')
    f7xd = IntCol(unit= 'foy')
    f7xe = IntCol(unit= 'foy')
    f7xf = IntCol(unit= 'foy')
    f7xh = IntCol(unit= 'foy')
    f7xi = IntCol(unit= 'foy')
    f7xj = IntCol(unit= 'foy')
    f7xk = IntCol(unit= 'foy')
    f7xl = IntCol(unit= 'foy')
    f7xm = IntCol(unit= 'foy')
    f7xn = IntCol(unit= 'foy')
    f7xo = IntCol(unit= 'foy')
    
    # Souscriptions au capital des PME
    f7cf = IntCol(unit= 'foy')
    f7cl = IntCol(unit= 'foy')
    f7cm = IntCol(unit= 'foy')
    f7cn = IntCol(unit= 'foy')
    f7cu = IntCol(unit= 'foy')

    # Souscription au capital d’une SOFIPECHE 
    f7gs = IntCol(unit= 'foy')

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité    
    f7ua = IntCol(unit= 'foy')
    f7ub = IntCol(unit= 'foy')
    f7uc = IntCol(unit= 'foy')
    f7ui = IntCol(unit= 'foy')
    f7uj = IntCol(unit= 'foy')
    f7qb = IntCol(unit= 'foy')
    f7qc = IntCol(unit= 'foy')
    f7qd = IntCol(unit= 'foy')
    f7ql = IntCol(unit= 'foy')
    f7qt = IntCol(unit= 'foy')
    f7qm = IntCol(unit= 'foy')
    
    # Souscription de parts de fonds communs de placement dans l'innovation, 
    # de fonds d'investissement de proximité    
    f7gq = IntCol(unit= 'foy')
    f7fq = IntCol(unit= 'foy')
    f7fm = IntCol(unit= 'foy')
    f7fl = IntCol(unit= 'foy')
    
    # Souscriptions au capital de SOFICA
    f7gn = IntCol(unit= 'foy')
    f7fn = IntCol(unit= 'foy')

    # Intérèts d'emprunts pour reprises de société
    f7fh = IntCol(unit= 'foy')         

    # Frais de comptabilité et d'adhésion à un CGA ou AA         
    f7ff = IntCol(unit= 'foy')
    f7fg = IntCol(unit= 'foy')
    
    # Travaux de conservation et de restauration d’objets classés monuments historiques
    f7nz = IntCol(unit= 'foy')
    
    # Dépenses de protections du patrimoine naturel
    f7ka = IntCol(unit= 'foy')

    # Intérêts d'emprunts
    f7wg = IntCol(unit= 'foy')
    
    # Intérêts des prêts à la consommation (case UH)
    f7uh = IntCol(unit= 'foy')
    
    # Investissements forestiers
    f7un = IntCol(unit= 'foy')
    
    # Intérêts pour paiement différé accordé aux agriculteurs
    f7um = IntCol(unit= 'foy')

    # Investissements locatif neufs : Dispositif Scellier
    f7hj = IntCol(unit= 'foy')
    f7hk = IntCol(unit= 'foy')
    f7hn = IntCol(unit= 'foy')
    f7ho = IntCol(unit= 'foy')
    f7hl = IntCol(unit= 'foy')
    f7hm = IntCol(unit= 'foy')
    f7hr = IntCol(unit= 'foy')
    f7hs = IntCol(unit= 'foy')
    f7la = IntCol(unit= 'foy')

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    f7ij = IntCol(unit= 'foy')
    f7il = IntCol(unit= 'foy')
    f7im = IntCol(unit= 'foy')
    f7ik = IntCol(unit= 'foy')
    f7is = IntCol(unit= 'foy')
    
    # Investissements locatifs dans les résidences de tourisme situées dans une zone de 
    # revitalisation rurale
    f7gt = IntCol(unit= 'foy')
    f7xg = IntCol(unit= 'foy')
    f7gu = IntCol(unit= 'foy')
    f7gv = IntCol(unit= 'foy')
    
    # Avoir fiscaux et crédits d'impôt     
    # f2ab déjà disponible
    f8ta = IntCol(unit= 'foy')
    f8tb = IntCol(unit= 'foy')
    f8tf = IntCol(unit= 'foy')
    f8tg = IntCol(unit= 'foy')
    f8th = IntCol(unit= 'foy')
    f8tc = IntCol(unit= 'foy')
    f8td = IntCol(unit= 'foy')
    f8te = IntCol(unit= 'foy')
    f8to = IntCol(unit= 'foy')
    f8tp = IntCol(unit= 'foy')
    f8uz = IntCol(unit= 'foy')
    f8tz = IntCol(unit= 'foy')
    f8wa = IntCol(unit= 'foy')
    f8wb = IntCol(unit= 'foy')
    f8wc = IntCol(unit= 'foy')
    f8wd = IntCol(unit= 'foy')
    f8we = IntCol(unit= 'foy')
    f8wr = IntCol(unit= 'foy')
    f8ws = IntCol(unit= 'foy')
    f8wt = IntCol(unit= 'foy')
    f8wu = IntCol(unit= 'foy')
    f8wv = IntCol(unit= 'foy')
    f8wx = IntCol(unit= 'foy')
    f8wy = IntCol(unit= 'foy')
    
    # Acquisition de biens culturels
    f7uo = IntCol(unit= 'foy')

    
    # Mécénat d'entreprise    
    f7us = IntCol(unit= 'foy')

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    # f7wf = IntCol() déjà disponible
    # f7wh = IntCol() déjà disponible
    # f7wk = IntCol() déjà disponible
    # f7wq = IntCol() déjà disponible
    f7sb = IntCol(unit= 'foy')
    f7sd = IntCol(unit= 'foy')
    f7se = IntCol(unit= 'foy')
    f7sh = IntCol(unit= 'foy')
    # f7wg = IntCol() déjà disponible
    f7sc = IntCol(unit= 'foy')
    
    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
    f7up = IntCol(unit= 'foy')
    f7uq = IntCol(unit= 'foy')

    # Crédit d'impôt aide à la mobilité
    f1ar = IntCol(unit= 'foy')
    f1br = IntCol(unit= 'foy')
    f1cr = IntCol(unit= 'foy')
    f1dr = IntCol(unit= 'foy')
    f1er = IntCol(unit= 'foy')

    # Crédit d’impôt directive « épargne » (case 2BG)
    f2bg = IntCol(unit= 'foy')
    
    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    f4tq = IntCol(unit= 'foy')
    

    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    # f7wf
    # f7wi
    # f7wj
    # f7wl
    f7sf = IntCol(unit= 'foy')
    f7si = IntCol(unit= 'foy')
    
    # Frais de garde des enfants à l’extérieur du domicile 
    f4ga = IntCol(unit= 'foy')
    f4gb = IntCol(unit= 'foy')
    f4gc = IntCol(unit= 'foy')
    f4ge = IntCol(unit= 'foy')
    f4gf = IntCol(unit= 'foy')
    f4gg = IntCol(unit= 'foy')

    # Auto-entrepreneur : versements d’impôt sur le revenu 
    f8uy = IntCol(unit= 'foy')

    # Revenus des professions non salariées
    frag_exon = IntCol(unit= 'foy', val_type="monetary") # (f5hn, f5in, f5jn)
    frag_impo = IntCol(unit= 'foy', val_type="monetary") # (f5ho, f5io, f5jo)    
    arag_exon = IntCol(unit= 'foy', val_type="monetary") # (f5hb, f5ib, f5jb)
    arag_impg = IntCol(unit= 'foy', val_type="monetary") # (f5hc, f5ic, f5jc)
    arag_defi = IntCol(unit= 'foy', val_type="monetary") # (f5hf, f5if, f5jf)
    nrag_exon = IntCol(unit= 'foy', val_type="monetary") # (f5hh, f5ih, f5jh)
    nrag_impg = IntCol(unit= 'foy', val_type="monetary") # (f5hi, f5ii, f5ji)
    nrag_defi = IntCol(unit= 'foy', val_type="monetary") # (f5hl, f5il, f5jl)
    nrag_ajag = IntCol(unit= 'foy', val_type="monetary") # (f5hm, f5im, f5jm)

    mbic_exon = IntCol(unit= 'foy', val_type="monetary") # (f5kn, f5ln, f5mn)
    abic_exon = IntCol(unit= 'foy', val_type="monetary") # (f5kb, f5lb, f5mb)
    nbic_exon = IntCol(unit= 'foy', val_type="monetary") # (f5kh, f5lh, f5mh)
    mbic_impv = IntCol(unit= 'foy', val_type="monetary") # (f5ko, f5lo, f5mo)
    mbic_imps = IntCol(unit= 'foy', val_type="monetary") # (f5kp, f5lp, f5mp)
    abic_impn = IntCol(unit= 'foy', val_type="monetary") # (f5kc, f5lc, f5mc)
    abic_imps = IntCol(unit= 'foy', val_type="monetary") # (f5kd, f5ld, f5md)
    nbic_impn = IntCol(unit= 'foy', val_type="monetary") # (f5ki, f5li, f5mi)
    nbic_imps = IntCol(unit= 'foy', val_type="monetary") # (f5kj, f5lj, f5mj)
    abic_defn = IntCol(unit= 'foy', val_type="monetary") # (f5kf, f5lf, f5mf)
    abic_defs = IntCol(unit= 'foy', val_type="monetary") # (f5kg, f5lg, f5mg)
    nbic_defn = IntCol(unit= 'foy', val_type="monetary") # (f5kl, f5ll, f5ml)
    nbic_defs = IntCol(unit= 'foy', val_type="monetary") # (f5km, f5lm, f5mm)
    nbic_apch = IntCol(unit= 'foy', val_type="monetary") # (f5ks, f5ls, f5ms)

    macc_exon = IntCol(unit= 'foy') # (f5nn, f5on, f5pn)
    aacc_exon = IntCol(unit= 'foy') # (f5nb, f5ob, f5pb)
    nacc_exon = IntCol(unit= 'foy') # (f5nh, f5oh, f5ph)
    macc_impv = IntCol(unit= 'foy') # (f5no, f5oo, f5po)
    macc_imps = IntCol(unit= 'foy') # (f5np, f5op, f5pp)
    aacc_impn = IntCol(unit= 'foy') # (f5nc, f5oc, f5pc)
    aacc_imps = IntCol(unit= 'foy') # (f5nd, f5od, f5pd)
    aacc_defn = IntCol(unit= 'foy') # (f5nf, f5of, f5pf)
    aacc_defs = IntCol(unit= 'foy') # (f5ng, f5og, f5pg)
    nacc_impn = IntCol(unit= 'foy') # (f5ni, f5oi, f5pi)
    nacc_imps = IntCol(unit= 'foy') # (f5nj, f5oj, f5pj)
    nacc_defn = IntCol(unit= 'foy') # (f5nl, f5ol, f5pl)
    nacc_defs = IntCol(unit= 'foy') # (f5nm, f5om, f5pm)
    mncn_impo = IntCol(unit= 'foy') # (f5ku, f5lu, f5mu)
    cncn_bene = IntCol(unit= 'foy') # (f5sn, f5ns, f5os)
    cncn_defi = IntCol(unit= 'foy') # (f5sp, f5nu, f5ou, f5sr)

    mbnc_exon = IntCol(unit= 'foy') # (f5hp, f5ip, f5jp)
    abnc_exon = IntCol(unit= 'foy') # (f5qb, f5rb, f5sb)
    nbnc_exon = IntCol(unit= 'foy') # (f5qh, f5rh, f5sh)
    mbnc_impo = IntCol(unit= 'foy') # (f5hq, f5iq, f5jq)
    abnc_impo = IntCol(unit= 'foy') # (f5qc, f5rc, f5sc)
    abnc_defi = IntCol(unit= 'foy') # (f5qe, f5re, f5se)
    nbnc_impo = IntCol(unit= 'foy') # (f5qi, f5ri, f5si)
    nbnc_defi = IntCol(unit= 'foy') # (f5qk, f5rk, f5sk)

    mbic_mvct = IntCol(unit= 'foy') # (f5hu)
    macc_mvct = IntCol(unit= 'foy') # (f5iu)
    mncn_mvct = IntCol(unit= 'foy') # (f5ju)
    mbnc_mvct = IntCol(unit= 'foy') # (f5kz)

    frag_pvct = IntCol(unit= 'foy') # (f5hw, f5iw, f5jw)
    mbic_pvct = IntCol(unit= 'foy') # (f5kx, f5lx, f5mx)
    macc_pvct = IntCol(unit= 'foy') # (f5nx, f5ox, f5px)
    mbnc_pvct = IntCol(unit= 'foy') # (f5hv, f5iv, f5jv)
    mncn_pvct = IntCol(unit= 'foy') # (f5ky, f5ly, f5my)

    mbic_mvlt = IntCol(unit= 'foy') # (f5kr, f5lr, f5mr)
    macc_mvlt = IntCol(unit= 'foy') # (f5nr, f5or, f5pr)
    mncn_mvlt = IntCol(unit= 'foy') # (f5kw, f5lw, f5mw)
    mbnc_mvlt = IntCol(unit= 'foy') # (f5hs, f5is, f5js)

    frag_pvce = IntCol(unit= 'foy') # (f5hx, f5ix, f5jx)
    arag_pvce = IntCol(unit= 'foy') # (f5he, f5ie, f5je)
    nrag_pvce = IntCol(unit= 'foy') # (f5hk, f5ik, f5jk)
    mbic_pvce = IntCol(unit= 'foy') # (f5kq, f5lq, f5mq)
    abic_pvce = IntCol(unit= 'foy') # (f5ke, f5le, f5me)
    nbic_pvce = IntCol(unit= 'foy') # (f5kk, f5lk, f5mk)
    macc_pvce = IntCol(unit= 'foy') # (f5nq, f5oq, f5pq)
    aacc_pvce = IntCol(unit= 'foy') # (f5ne, f5oe, f5pe)
    nacc_pvce = IntCol(unit= 'foy') # (f5nk, f5ok, f5pk)
    mncn_pvce = IntCol(unit= 'foy') # (f5kv, f5lv, f5mv)
    cncn_pvce = IntCol(unit= 'foy') # (f5so, f5nt, f5ot)
    mbnc_pvce = IntCol(unit= 'foy') # (f5hr, f5ir, f5jr)
    abnc_pvce = IntCol(unit= 'foy') # (f5qd, f5rd, f5sd)
    nbnc_pvce = IntCol(unit= 'foy') # (f5qj, f5rj, f5sj)

# pfam only
    inactif   = BoolCol(unit='fam')
    partiel1  = BoolCol(unit='fam')
    partiel2  = BoolCol(unit='fam') 
    categ_inv = IntCol(unit='fam')
    opt_colca = BoolCol(unit='fam')
    empl_dir  = BoolCol(unit='fam') 
    ass_mat   = BoolCol(unit='fam')
    gar_dom   = BoolCol(unit='fam')

# zones apl and calibration 
    tu99 = EnumCol(label = u"tranche d'unité urbaine",
                   unit = 'men',
                   enum=Enum([u'Communes rurales',
                         u'moins de 5 000 habitants',
                         u'5 000 à 9 999 habitants',
                         u'10 000 à 19 999 habitants',
                         u'20 000 à 49 999 habitants',
                         u'50 000 à 99 999 habitants',
                         u'100 000 à 199 999 habitants',
                         u'200 000 habitants ou plus (sauf agglomération parisienne)',
                         u'agglomération parisienne']))
    
    tau99 = EnumCol(label = u"tranche d'aire urbaine", unit='men')
    reg   = EnumCol(unit='men')
    pol99 = EnumCol(unit='men')
    cstotpragr = EnumCol(label = u"catégorie socio_professionelle agrégée de la personne de référence",
                         unit = 'men',
                         enum = Enum([u"Non renseignée",
                                      u"Agriculteurs exploitants",
                                      u"Artisans, commerçants, chefs d'entreprise",
                                      u"Cadres supérieurs",
                                      u"Professions intermédiaires",
                                      u"Employés",
                                      u"Ouvriers",
                                      u"Retraités",
                                      u"Autres inactifs"]))
    
    naf16pr = EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence",
                      unit = 'men',
                      enum = Enum([u"Sans objet",
                                   u"Non renseigné",
                                   u"Agriculture, sylviculture et pêche",
                                   u"Industries agricoles",
                                   u"Industries des biens de consommation",
                                   u"Industrie automobile",
                                   u"Industries des biens d'équipement",
                                   u"Industries des biens intermédiaires",
                                   u"Energie",
                                   u"Construction",
                                   u"Commerce et réparations",
                                   u"Transports",
                                   u"Activités financières",
                                   u"Activités immobilières",
                                   u"Services aux entreprises",
                                   u"Services aux particuliers",
                                   u"Education, santé, action sociale",
                                   u"Administrations"],start=-1)) # 17 postes + 1 (-1: sans objet, 0: nonrenseigné) 

    nafg17npr = EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence ",
                      unit = 'men',
                      enum = Enum([u"Sans objet",
                                   u"Non renseigné",
                                   u"Agriculture, sylviculture et pêche",
                                   u"Industries extractives, énergie, eau, gestion des déchets et dépollution",
                                   u"Fabrication de denrées alimentaires, de boissons et de produits à base de tabac",
                                   u"Cokéfaction et raffinage",
                                   u"Fabrication d'équipements électriques, électroniques, informatiques ; fabrication de machines",
                                   u"Fabrication de matériels de transport",
                                   u"Fabrication d'autres produits industriels",
                                   u"Construction",
                                   u"Commerce ; réparation d'automobiles et de motocycles",
                                   u"Transports et entreposage",
                                   u"Hébergement et restauration",
                                   u"Information et communication",
                                   u"Activités financières et d'assurance",
                                   u"Activités immobilières",
                                   u"Activités scientifiques et techniques ; services administratifs et de soutien",
                                   u"Administration publique, enseignement, santé humaine et action sociale",
                                   u"Autres activités de services"],start=-1)) # 17 postes + 1 (-1: sans objet, 0: nonrenseigné)
    
    
    typmen15 = EnumCol(label = u"Type de ménage",
                       unit = 'men',
                       enum = Enum([u"Personne seule active",
                                    u"Personne seule inactive",
                                    u"Familles monoparentales, parent actif",
                                    u"Familles monoparentales, parent inactif et au moins un enfant actif",
                                    u"Familles monoparentales, tous inactifs",
                                    u"Couples sans enfant, 1 actif",
                                    u"Couples sans enfant, 2 actifs",
                                    u"Couples sans enfant, tous inactifs",
                                    u"Couples avec enfant, 1 membre du couple actif",
                                    u"Couples avec enfant, 2 membres du couple actif",
                                    u"Couples avec enfant, couple inactif et au moins un enfant actif",
                                    u"Couples avec enfant, tous inactifs",
                                    u"Autres ménages, 1 actif",
                                    u"Autres ménages, 2 actifs ou plus",
                                    u"Autres ménages, tous inactifs"],start=1))
    
    ageq  = EnumCol(label = u"âge quinquennal de la personne de référence",
                    unit = 'men',
                    enum = Enum([u"moins de 25 ans",
                                 u"25 à 29 ans",
                                 u"30 à 34 ans",
                                 u"35 à 39 ans",
                                 u"40 à 44 ans",
                                 u"45 à 49 ans",
                                 u"50 à 54 ans",
                                 u"55 à 59 ans",
                                 u"60 à 64 ans",
                                 u"65 à 69 ans",
                                 u"70 à 74 ans",
                                 u"75 à 79 ans",
                                 u"80 ans et plus"]))

                                 
    nbinde = EnumCol(label = u"taille du ménage",
                     unit = 'men',
                     enum = Enum([u"Une personne",
                                  u"Deux personnes",
                                  u"Trois personnes",
                                  u"Quatre personnes",
                                  u"Cinq personnes",
                                  u"Six personnes et plus"], start=1))

    ddipl = EnumCol(label = u"diplôme de la personne de référence",
                    unit = 'men',
                    enum = Enum([u"Diplôme supérieur",
                                 u"Baccalauréat + 2 ans",
                                 u"Baccalauréat ou brevet professionnel ou autre diplôme de ce niveau",
                                 u"CAP, BEP ou autre diplôme de ce niveau",
                                 u"Brevet des collèges",
                                 u"Aucun diplôme ou CEP"],start=1)) 
    
    act5 = EnumCol(label = u"activité",
                     enum = Enum([u"Salarié",
                                  u"Indépendant",
                                  u"Chômeur",
                                  u"Retraité",
                                  u"Inactif"],start=1)) # 5 postes normalement TODO; check=0
    wprm_init = FloatCol()


## ISF ##
    
## Immeubles bâtis ##
    b1ab = IntCol(unit= 'foy') ##  valeur résidence principale avant abattement ##
    b1ac = IntCol(unit= 'foy')
## non bâtis ##
    b1bc = IntCol(unit= 'foy')
    b1be = IntCol(unit= 'foy')
    b1bh = IntCol(unit= 'foy')
    b1bk = IntCol(unit= 'foy') 
## droits sociaux- valeurs mobilières-liquidités- autres meubles ##

    b1cl = IntCol(unit= 'foy')
    b1cb = IntCol(unit= 'foy')
    b1cd = IntCol(unit= 'foy')
    b1ce = IntCol(unit= 'foy')
    b1cf = IntCol(unit= 'foy')
    b1cg = IntCol(unit= 'foy')

    b1co = IntCol(unit= 'foy')

#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réduc ##
    b2gh= IntCol(unit= 'foy')
    
## réductions ##
    b2mt = IntCol(unit= 'foy')
    b2ne = IntCol(unit= 'foy')
    b2mv = IntCol(unit= 'foy')
    b2nf = IntCol(unit= 'foy')
    b2mx = IntCol(unit= 'foy')
    b2na = IntCol(unit= 'foy')
    b2nc = IntCol(unit= 'foy')

##  montant impôt acquitté hors de France ##
    b4rs = IntCol(unit= 'foy')

## BOUCLIER FISCAL ##

    rev_or= IntCol()
    rev_exo= IntCol()

    tax_fonc= IntCol()
    restit_imp= IntCol()
        
    # to remove
    champm = BoolCol()
    wprm = FloatCol()
    etr = IntCol()     
    coloc = BoolCol()
    csg_rempl = EnumCol(label = u"Taux retenu sur la CSG des revenus de remplacment",
                 unit='ind',
                 enum = Enum([u"Non renseigné/non pertinent",
                              u"Exonéré",
                              u"Taux réduit",
                              u"Taux plein"]),
                default = 3)
                        
    aer = IntCol()
    ass = IntCol()
    f5sq = IntCol()
    
    m_afeamam = IntCol()
    m_agedm   = IntCol()
    m_clcam   = IntCol()
    m_colcam  = IntCol()
    m_mgamm   = IntCol()
    m_mgdomm  = IntCol()
    zthabm    = IntCol()  # Devrait être renommée tax
    # tax_hab= IntCol()    