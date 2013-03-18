# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from src.lib.description import ModelDescription
from src.lib.columns import IntCol, EnumCol, BoolCol, AgesCol, FloatCol
from src.lib.utils import Enum

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
    fra  = IntCol(val_type="monetary") # (f1ak, f1bk, f1ck, f1dk, f1ek)

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
    
    zone_apl = EnumCol(label = u"zone apl", default = 2, entity= 'menage')
    loyer = IntCol(entity='men', val_type="monetary") # Loyer mensuel
    so = EnumCol(label = u"Statut d'occupation",
                 entity='men',
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
    code_postal = IntCol(entity='men')
    
    statmarit = EnumCol(label = u"Statut marital",
                          default = 2,
                          enum = Enum([u"Marié",
                                    u"Célibataire",
                                    u"Divorcé",
                                    u"Veuf",
                                    u"Pacsé",
                                    u"Jeune veuf"],start=1))
    
    nbR = IntCol(entity= 'foy')
    nbJ = IntCol(entity= 'foy')
    nbI = IntCol(entity= 'foy')
    nbH = IntCol(entity= 'foy')
    nbG = IntCol(entity= 'foy')
    nbF = IntCol(entity= 'foy')
    nbN = IntCol(entity= 'foy')
    
    caseE = BoolCol(entity= 'foy')
    caseF = BoolCol(entity= 'foy')
    caseG = BoolCol(entity= 'foy')
    caseH = IntCol(entity= 'foy')
    caseK = BoolCol(entity= 'foy')
    caseL = BoolCol(entity= 'foy')
    caseN = BoolCol(entity= 'foy')
    caseP = BoolCol(entity= 'foy')
    caseS = BoolCol(entity= 'foy')
    caseT = BoolCol(entity= 'foy')
    caseW = BoolCol(entity= 'foy')
    
    
    rfr_n_2  = IntCol(entity='foy', label = u"Revenu fiscal de référence année n-2", val_type="monetary") # TODO: provide in data
    nbptr_n_2 = IntCol(entity='foy', label = u"Nombre de parts année n-2", val_type="monetary")  # TODO: provide in data
    
    # Rentes viagères
    f1aw = IntCol(entity= 'foy', val_type="monetary")
    f1bw = IntCol(entity= 'foy', val_type="monetary")
    f1cw = IntCol(entity= 'foy', val_type="monetary")
    f1dw = IntCol(entity= 'foy', val_type="monetary")
    
    f1tv = IntCol(entity= 'foy', val_type="monetary")
    f1uv = IntCol(entity= 'foy', val_type="monetary")
    f1tw = IntCol(entity= 'foy', val_type="monetary")
    f1uw = IntCol(entity= 'foy', val_type="monetary")
    f1tx = IntCol(entity= 'foy', val_type="monetary")
    f1ux = IntCol(entity= 'foy', val_type="monetary")
    
    # RVCM
    # revenus au prélèvement libératoire
    f2da = IntCol(entity= 'foy', label = u"Revenus des actions et parts soumis au prélèvement libératoire", val_type="monetary")
    f2dh = IntCol(entity= 'foy', val_type="monetary")
    f2ee = IntCol(entity= 'foy', label = u"Revenus au prélèvement libératoire hors actions et assurance-vie", val_type="monetary")

    # revenus ouvrant droit à abattement
    f2dc = IntCol(entity= 'foy', label =u"Revenus des actions et parts donnant droit à abattement", val_type="monetary")
    f2fu = IntCol(entity= 'foy', val_type="monetary")
    f2ch = IntCol(entity= 'foy', val_type="monetary")
    
    # Revenus n'ouvrant pas droit à abattement
    f2ts = IntCol(entity= 'foy', val_type="monetary")
    f2go = IntCol(entity= 'foy', val_type="monetary")
    f2tr = IntCol(entity= 'foy', label = u"Intérêts et autres revenus assimilés", val_type="monetary")
    
    # Autres
    f2cg = IntCol(entity= 'foy', val_type="monetary")
    f2bh = IntCol(entity= 'foy', val_type="monetary")
    f2ca = IntCol(entity= 'foy', val_type="monetary")
    f2aa = IntCol(entity='foy', val_type="monetary")
    f2ab = IntCol(entity= 'foy', val_type="monetary")
    f2al = IntCol(entity= 'foy', val_type="monetary")
    f2am = IntCol(entity= 'foy', val_type="monetary")
    f2an = IntCol(entity= 'foy', val_type="monetary")
    # non accessible (from previous years)
    f2gr = IntCol(entity= 'foy', val_type="monetary") 
        
    f3vc = IntCol(entity= 'foy', val_type="monetary")
    f3vd = IntCol(entity= 'foy', val_type="monetary")
    f3ve = IntCol(entity= 'foy', val_type="monetary")
    f3vf = IntCol(entity= 'foy')    
    
    f3vl = IntCol(entity= 'foy', val_type="monetary")
    f3vi = IntCol(entity= 'foy', val_type="monetary")
    f3vm = IntCol(entity= 'foy', val_type="monetary")
    
    f3vj = IntCol(entity= 'foy', val_type="monetary")
    f3vk = IntCol(entity= 'foy', val_type="monetary")
    f3va = IntCol(entity= 'foy', val_type="monetary")
    
    # Plus values et gains taxables à 18%
    f3vg = IntCol(entity= 'foy', val_type="monetary")
    f3vh = IntCol(entity= 'foy', val_type="monetary")
    f3vt = IntCol(entity= 'foy', val_type="monetary")
    f3vu = IntCol(entity= 'foy', val_type="monetary")
    f3vv = IntCol(entity= 'foy', val_type="monetary")

    # Revenu foncier
    f4ba = IntCol(entity= 'foy', val_type="monetary")
    f4bb = IntCol(entity= 'foy', val_type="monetary")
    f4bc = IntCol(entity= 'foy', val_type="monetary")
    f4bd = IntCol(entity= 'foy', val_type="monetary")
    f4be = IntCol(entity= 'foy', val_type="monetary")
    
    # Prime d'assurance loyers impayés
    f4bf = IntCol(entity= 'foy', val_type="monetary")
    
    f4bl = IntCol(entity= 'foy', val_type="monetary")
    
    f5qm = IntCol(entity= 'foy', val_type="monetary")
    f5rm = IntCol(entity= 'foy', val_type="monetary")
    
    # Csg déductible
    f6de = IntCol(entity= 'foy', val_type="monetary")

    # Pensions alimentaires
    f6gi = IntCol(entity= 'foy', val_type="monetary")
    f6gj = IntCol(entity= 'foy', val_type="monetary")
    f6el = IntCol(entity= 'foy', val_type="monetary")
    f6em = IntCol(entity= 'foy', val_type="monetary")
    f6gp = IntCol(entity= 'foy', val_type="monetary")
    f6gu = IntCol(entity= 'foy', val_type="monetary")
    
    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    f6eu = IntCol(entity= 'foy', val_type="monetary")
    f6ev = IntCol(entity= 'foy')
    
    # Déductions diverses
    f6dd = IntCol(entity= 'foy', val_type="monetary")
    
    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    f6ps = IntCol(entity= 'foy', val_type="monetary")
    f6rs = IntCol(entity= 'foy', val_type="monetary")
    f6ss = IntCol(entity= 'foy', val_type="monetary")
    f6pt = IntCol(entity= 'foy', val_type="monetary")
    f6rt = IntCol(entity= 'foy', val_type="monetary")
    f6st = IntCol(entity= 'foy', val_type="monetary")
    f6pu = IntCol(entity= 'foy', val_type="monetary")
    f6ru = IntCol(entity= 'foy', val_type="monetary")
    f6su = IntCol(entity= 'foy', val_type="monetary")
    
    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    f6aa = IntCol(entity= 'foy', val_type="monetary")
    
    # Souscriptions au capital des SOFIPÊCHE
    f6cc = IntCol(entity= 'foy', val_type="monetary")
    
    # Investissements DOM-TOM dans le cadre d’une entreprise <= 2005
    # ou Versements sur un compte épargne codéveloppement 
    f6eh = IntCol(entity= 'foy', val_type="monetary")
    
    # Pertes en capital consécutives à la souscription au capital de sociétés 
    # nouvelles ou de sociétés en difficulté
    f6da = IntCol(entity= 'foy', val_type="monetary")
    
    
    # Dépenses de grosses réparations effectuées par les nus propriétaires
    f6cb = IntCol(entity= 'foy', val_type="monetary")
    f6hj = IntCol(entity= 'foy', val_type="monetary")
    
    # Sommes à rajouter au revenu imposable
    f6gh = IntCol(entity= 'foy', val_type="monetary")    
    
    # Deficit Antérieur
    f6fa = IntCol(entity= 'foy', val_type="monetary")
    f6fb = IntCol(entity= 'foy', val_type="monetary")
    f6fc = IntCol(entity= 'foy', val_type="monetary")
    f6fd = IntCol(entity= 'foy', val_type="monetary")
    f6fe = IntCol(entity= 'foy', val_type="monetary")
    f6fl = IntCol(entity= 'foy', val_type="monetary")
    
    # Dons
    f7ud = IntCol(entity= 'foy', val_type="monetary")
    f7uf = IntCol(entity= 'foy', val_type="monetary")
    f7xs = IntCol(entity= 'foy', val_type="monetary")
    f7xt = IntCol(entity= 'foy', val_type="monetary")
    f7xu = IntCol(entity= 'foy', val_type="monetary")
    f7xw = IntCol(entity= 'foy', val_type="monetary")
    f7xy = IntCol(entity= 'foy', val_type="monetary")
    
    # Cotisations syndicales des salariées et pensionnés
    f7ac = IntCol(entity= 'foy', val_type="monetary")
    f7ae = IntCol(entity= 'foy', val_type="monetary")
    f7ag = IntCol(entity= 'foy', val_type="monetary")

    # Salarié à domicile
    f7db = IntCol(entity= 'foy', val_type="monetary")
    f7df = IntCol(entity= 'foy', val_type="monetary")
    f7dq = IntCol(entity= 'foy', val_type="monetary")
    f7dg = BoolCol(entity= 'foy')
    f7dl = IntCol(entity= 'foy', val_type="monetary")
    
    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    f7vy = IntCol(entity= 'foy', val_type="monetary")
    f7vz = IntCol(entity= 'foy', val_type="monetary")
    f7vx = IntCol(entity= 'foy', val_type="monetary")
    f7vw = IntCol(entity= 'foy', val_type="monetary")

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    f7cd = IntCol(entity= 'foy', val_type="monetary")
    f7ce = IntCol(entity= 'foy', val_type="monetary")

    # Frais de garde des enfants de moins de 6 ans
    f7ga = IntCol(entity= 'foy', val_type="monetary")
    f7gb = IntCol(entity= 'foy', val_type="monetary")
    f7gc = IntCol(entity= 'foy', val_type="monetary")
    f7ge = IntCol(entity= 'foy', val_type="monetary")
    f7gf = IntCol(entity= 'foy', val_type="monetary")
    f7gg = IntCol(entity= 'foy', val_type="monetary")

    # Nombre d'enfants à charge poursuivant leurs études
    f7ea = IntCol(entity= 'foy')
    f7eb = IntCol(entity= 'foy')
    f7ec = IntCol(entity= 'foy')
    f7ed = IntCol(entity= 'foy')
    f7ef = IntCol(entity= 'foy')
    f7eg = IntCol(entity= 'foy')

    # Intérêts des prêts étudiants
    f7td = IntCol(entity= 'foy', val_type="monetary")
    f7vo = IntCol(entity= 'foy', val_type="monetary")
    f7uk = IntCol(entity= 'foy', val_type="monetary")
    
    # Primes de survies, contrat d'épargne handicap
    f7gz = IntCol(entity= 'foy', val_type="monetary")
    
    # Prestations compensatoires
    f7wm = IntCol(entity= 'foy', val_type="monetary")
    f7wn = IntCol(entity= 'foy', val_type="monetary")
    f7wo = IntCol(entity= 'foy', val_type="monetary")
    f7wp = IntCol(entity= 'foy', val_type="monetary")
    
    # Dépenses en faveur de la qualité environnementale
    f7we = IntCol(entity= 'foy', val_type="monetary")
    f7wq = IntCol(entity= 'foy', val_type="monetary")
    f7wh = IntCol(entity= 'foy', val_type="monetary")
    f7wk = IntCol(entity= 'foy', val_type="monetary")
    f7wf = IntCol(entity= 'foy', val_type="monetary")
    
    # Dépenses en faveur de l'aide aux personnes
    f7wi = IntCol(entity= 'foy', val_type="monetary")
    f7wj = IntCol(entity= 'foy', val_type="monetary")
    f7wl = IntCol(entity= 'foy', val_type="monetary")
    
    # Investissements dans les DOM-TOM dans le cadre d'une entrepise  TODO: RESTART FROM HERE FOR , val_type="monetary"
    f7ur = IntCol(entity= 'foy')
    f7oz = IntCol(entity= 'foy')
    f7pz = IntCol(entity= 'foy')
    f7qz = IntCol(entity= 'foy')
    f7rz = IntCol(entity= 'foy')
    f7sz = IntCol(entity= 'foy')
    
    # Aide aux créateurs et repreneurs d'entreprises
    f7fy = IntCol(entity= 'foy')
    f7gy = IntCol(entity= 'foy')
    f7jy = IntCol(entity= 'foy')
    f7hy = IntCol(entity= 'foy')
    f7ky = IntCol(entity= 'foy')
    f7iy = IntCol(entity= 'foy')
    f7ly = IntCol(entity= 'foy')
    f7my = IntCol(entity= 'foy')

    # Travaux de restauration immobilière
    f7ra = IntCol(entity= 'foy')
    f7rb = IntCol(entity= 'foy')
    
    # Assurance-vie
    f7gw = IntCol(entity= 'foy')
    f7gx = IntCol(entity= 'foy')
    # f7gy = IntCol() existe ailleurs

    # Investissements locatifs dans le secteur de touristique            
    f7xc = IntCol(entity= 'foy')
    f7xd = IntCol(entity= 'foy')
    f7xe = IntCol(entity= 'foy')
    f7xf = IntCol(entity= 'foy')
    f7xh = IntCol(entity= 'foy')
    f7xi = IntCol(entity= 'foy')
    f7xj = IntCol(entity= 'foy')
    f7xk = IntCol(entity= 'foy')
    f7xl = IntCol(entity= 'foy')
    f7xm = IntCol(entity= 'foy')
    f7xn = IntCol(entity= 'foy')
    f7xo = IntCol(entity= 'foy')
    
    # Souscriptions au capital des PME
    f7cf = IntCol(entity= 'foy')
    f7cl = IntCol(entity= 'foy')
    f7cm = IntCol(entity= 'foy')
    f7cn = IntCol(entity= 'foy')
    f7cu = IntCol(entity= 'foy')

    # Souscription au capital d’une SOFIPECHE 
    f7gs = IntCol(entity= 'foy')

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité    
    f7ua = IntCol(entity= 'foy')
    f7ub = IntCol(entity= 'foy')
    f7uc = IntCol(entity= 'foy')
    f7ui = IntCol(entity= 'foy')
    f7uj = IntCol(entity= 'foy')
    f7qb = IntCol(entity= 'foy')
    f7qc = IntCol(entity= 'foy')
    f7qd = IntCol(entity= 'foy')
    f7ql = IntCol(entity= 'foy')
    f7qt = IntCol(entity= 'foy')
    f7qm = IntCol(entity= 'foy')
    
    # Souscription de parts de fonds communs de placement dans l'innovation, 
    # de fonds d'investissement de proximité    
    f7gq = IntCol(entity= 'foy')
    f7fq = IntCol(entity= 'foy')
    f7fm = IntCol(entity= 'foy')
    f7fl = IntCol(entity= 'foy')
    
    # Souscriptions au capital de SOFICA
    f7gn = IntCol(entity= 'foy')
    f7fn = IntCol(entity= 'foy')

    # Intérèts d'emprunts pour reprises de société
    f7fh = IntCol(entity= 'foy')         

    # Frais de comptabilité et d'adhésion à un CGA ou AA         
    f7ff = IntCol(entity= 'foy')
    f7fg = IntCol(entity= 'foy')
    
    # Travaux de conservation et de restauration d’objets classés monuments historiques
    f7nz = IntCol(entity= 'foy')
    
    # Dépenses de protections du patrimoine naturel
    f7ka = IntCol(entity= 'foy')

    # Intérêts d'emprunts
    f7wg = IntCol(entity= 'foy')
    
    # Intérêts des prêts à la consommation (case UH)
    f7uh = IntCol(entity= 'foy')
    
    # Investissements forestiers
    f7un = IntCol(entity= 'foy')
    
    # Intérêts pour paiement différé accordé aux agriculteurs
    f7um = IntCol(entity= 'foy')

    # Investissements locatif neufs : Dispositif Scellier
    f7hj = IntCol(entity= 'foy')
    f7hk = IntCol(entity= 'foy')
    f7hn = IntCol(entity= 'foy')
    f7ho = IntCol(entity= 'foy')
    f7hl = IntCol(entity= 'foy')
    f7hm = IntCol(entity= 'foy')
    f7hr = IntCol(entity= 'foy')
    f7hs = IntCol(entity= 'foy')
    f7la = IntCol(entity= 'foy')

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    f7ij = IntCol(entity= 'foy')
    f7il = IntCol(entity= 'foy')
    f7im = IntCol(entity= 'foy')
    f7ik = IntCol(entity= 'foy')
    f7is = IntCol(entity= 'foy')
    
    # Investissements locatifs dans les résidences de tourisme situées dans une zone de 
    # revitalisation rurale
    f7gt = IntCol(entity= 'foy')
    f7xg = IntCol(entity= 'foy')
    f7gu = IntCol(entity= 'foy')
    f7gv = IntCol(entity= 'foy')
    
    # Avoir fiscaux et crédits d'impôt     
    # f2ab déjà disponible
    f8ta = IntCol(entity= 'foy')
    f8tb = IntCol(entity= 'foy')
    f8tf = IntCol(entity= 'foy')
    f8tg = IntCol(entity= 'foy')
    f8th = IntCol(entity= 'foy')
    f8tc = IntCol(entity= 'foy')
    f8td = IntCol(entity= 'foy')
    f8te = IntCol(entity= 'foy')
    f8to = IntCol(entity= 'foy')
    f8tp = IntCol(entity= 'foy')
    f8uz = IntCol(entity= 'foy')
    f8tz = IntCol(entity= 'foy')
    f8wa = IntCol(entity= 'foy')
    f8wb = IntCol(entity= 'foy')
    f8wc = IntCol(entity= 'foy')
    f8wd = IntCol(entity= 'foy')
    f8we = IntCol(entity= 'foy')
    f8wr = IntCol(entity= 'foy')
    f8ws = IntCol(entity= 'foy')
    f8wt = IntCol(entity= 'foy')
    f8wu = IntCol(entity= 'foy')
    f8wv = IntCol(entity= 'foy')
    f8wx = IntCol(entity= 'foy')
    f8wy = IntCol(entity= 'foy')
    
    # Acquisition de biens culturels
    f7uo = IntCol(entity= 'foy')

    
    # Mécénat d'entreprise    
    f7us = IntCol(entity= 'foy')

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    # f7wf = IntCol() déjà disponible
    # f7wh = IntCol() déjà disponible
    # f7wk = IntCol() déjà disponible
    # f7wq = IntCol() déjà disponible
    f7sb = IntCol(entity= 'foy')
    f7sd = IntCol(entity= 'foy')
    f7se = IntCol(entity= 'foy')
    f7sh = IntCol(entity= 'foy')
    # f7wg = IntCol() déjà disponible
    f7sc = IntCol(entity= 'foy')
    
    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte
    f7up = IntCol(entity= 'foy')
    f7uq = IntCol(entity= 'foy')

    # Crédit d'impôt aide à la mobilité
    f1ar = IntCol(entity= 'foy')
    f1br = IntCol(entity= 'foy')
    f1cr = IntCol(entity= 'foy')
    f1dr = IntCol(entity= 'foy')
    f1er = IntCol(entity= 'foy')

    # Crédit d’impôt directive « épargne » (case 2BG)
    f2bg = IntCol(entity= 'foy')
    
    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    f4tq = IntCol(entity= 'foy')
    

    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    # f7wf
    # f7wi
    # f7wj
    # f7wl
    f7sf = IntCol(entity= 'foy')
    f7si = IntCol(entity= 'foy')
    
    # Frais de garde des enfants à l’extérieur du domicile 
    f4ga = IntCol(entity= 'foy')
    f4gb = IntCol(entity= 'foy')
    f4gc = IntCol(entity= 'foy')
    f4ge = IntCol(entity= 'foy')
    f4gf = IntCol(entity= 'foy')
    f4gg = IntCol(entity= 'foy')

    # Auto-entrepreneur : versements d’impôt sur le revenu 
    f8uy = IntCol(entity= 'foy')

    # Revenus des professions non salariées
    frag_exon = IntCol(entity= 'foy', val_type="monetary") # (f5hn, f5in, f5jn)
    frag_impo = IntCol(entity= 'foy', val_type="monetary") # (f5ho, f5io, f5jo)    
    arag_exon = IntCol(entity= 'foy', val_type="monetary") # (f5hb, f5ib, f5jb)
    arag_impg = IntCol(entity= 'foy', val_type="monetary") # (f5hc, f5ic, f5jc)
    arag_defi = IntCol(entity= 'foy', val_type="monetary") # (f5hf, f5if, f5jf)
    nrag_exon = IntCol(entity= 'foy', val_type="monetary") # (f5hh, f5ih, f5jh)
    nrag_impg = IntCol(entity= 'foy', val_type="monetary") # (f5hi, f5ii, f5ji)
    nrag_defi = IntCol(entity= 'foy', val_type="monetary") # (f5hl, f5il, f5jl)
    nrag_ajag = IntCol(entity= 'foy', val_type="monetary") # (f5hm, f5im, f5jm)

    mbic_exon = IntCol(entity= 'foy', val_type="monetary") # (f5kn, f5ln, f5mn)
    abic_exon = IntCol(entity= 'foy', val_type="monetary") # (f5kb, f5lb, f5mb)
    nbic_exon = IntCol(entity= 'foy', val_type="monetary") # (f5kh, f5lh, f5mh)
    mbic_impv = IntCol(entity= 'foy', val_type="monetary") # (f5ko, f5lo, f5mo)
    mbic_imps = IntCol(entity= 'foy', val_type="monetary") # (f5kp, f5lp, f5mp)
    abic_impn = IntCol(entity= 'foy', val_type="monetary") # (f5kc, f5lc, f5mc)
    abic_imps = IntCol(entity= 'foy', val_type="monetary") # (f5kd, f5ld, f5md)
    nbic_impn = IntCol(entity= 'foy', val_type="monetary") # (f5ki, f5li, f5mi)
    nbic_imps = IntCol(entity= 'foy', val_type="monetary") # (f5kj, f5lj, f5mj)
    abic_defn = IntCol(entity= 'foy', val_type="monetary") # (f5kf, f5lf, f5mf)
    abic_defs = IntCol(entity= 'foy', val_type="monetary") # (f5kg, f5lg, f5mg)
    nbic_defn = IntCol(entity= 'foy', val_type="monetary") # (f5kl, f5ll, f5ml)
    nbic_defs = IntCol(entity= 'foy', val_type="monetary") # (f5km, f5lm, f5mm)
    nbic_apch = IntCol(entity= 'foy', val_type="monetary") # (f5ks, f5ls, f5ms)

    macc_exon = IntCol(entity= 'foy') # (f5nn, f5on, f5pn)
    aacc_exon = IntCol(entity= 'foy') # (f5nb, f5ob, f5pb)
    nacc_exon = IntCol(entity= 'foy') # (f5nh, f5oh, f5ph)
    macc_impv = IntCol(entity= 'foy') # (f5no, f5oo, f5po)
    macc_imps = IntCol(entity= 'foy') # (f5np, f5op, f5pp)
    aacc_impn = IntCol(entity= 'foy') # (f5nc, f5oc, f5pc)
    aacc_imps = IntCol(entity= 'foy') # (f5nd, f5od, f5pd)
    aacc_defn = IntCol(entity= 'foy') # (f5nf, f5of, f5pf)
    aacc_defs = IntCol(entity= 'foy') # (f5ng, f5og, f5pg)
    nacc_impn = IntCol(entity= 'foy') # (f5ni, f5oi, f5pi)
    nacc_imps = IntCol(entity= 'foy') # (f5nj, f5oj, f5pj)
    nacc_defn = IntCol(entity= 'foy') # (f5nl, f5ol, f5pl)
    nacc_defs = IntCol(entity= 'foy') # (f5nm, f5om, f5pm)
    mncn_impo = IntCol(entity= 'foy') # (f5ku, f5lu, f5mu)
    cncn_bene = IntCol(entity= 'foy') # (f5sn, f5ns, f5os)
    cncn_defi = IntCol(entity= 'foy') # (f5sp, f5nu, f5ou, f5sr)

    mbnc_exon = IntCol(entity= 'foy') # (f5hp, f5ip, f5jp)
    abnc_exon = IntCol(entity= 'foy') # (f5qb, f5rb, f5sb)
    nbnc_exon = IntCol(entity= 'foy') # (f5qh, f5rh, f5sh)
    mbnc_impo = IntCol(entity= 'foy') # (f5hq, f5iq, f5jq)
    abnc_impo = IntCol(entity= 'foy') # (f5qc, f5rc, f5sc)
    abnc_defi = IntCol(entity= 'foy') # (f5qe, f5re, f5se)
    nbnc_impo = IntCol(entity= 'foy') # (f5qi, f5ri, f5si)
    nbnc_defi = IntCol(entity= 'foy') # (f5qk, f5rk, f5sk)

    mbic_mvct = IntCol(entity= 'foy') # (f5hu)
    macc_mvct = IntCol(entity= 'foy') # (f5iu)
    mncn_mvct = IntCol(entity= 'foy') # (f5ju)
    mbnc_mvct = IntCol(entity= 'foy') # (f5kz)

    frag_pvct = IntCol(entity= 'foy') # (f5hw, f5iw, f5jw)
    mbic_pvct = IntCol(entity= 'foy') # (f5kx, f5lx, f5mx)
    macc_pvct = IntCol(entity= 'foy') # (f5nx, f5ox, f5px)
    mbnc_pvct = IntCol(entity= 'foy') # (f5hv, f5iv, f5jv)
    mncn_pvct = IntCol(entity= 'foy') # (f5ky, f5ly, f5my)

    mbic_mvlt = IntCol(entity= 'foy') # (f5kr, f5lr, f5mr)
    macc_mvlt = IntCol(entity= 'foy') # (f5nr, f5or, f5pr)
    mncn_mvlt = IntCol(entity= 'foy') # (f5kw, f5lw, f5mw)
    mbnc_mvlt = IntCol(entity= 'foy') # (f5hs, f5is, f5js)

    frag_pvce = IntCol(entity= 'foy') # (f5hx, f5ix, f5jx)
    arag_pvce = IntCol(entity= 'foy') # (f5he, f5ie, f5je)
    nrag_pvce = IntCol(entity= 'foy') # (f5hk, f5ik, f5jk)
    mbic_pvce = IntCol(entity= 'foy') # (f5kq, f5lq, f5mq)
    abic_pvce = IntCol(entity= 'foy') # (f5ke, f5le, f5me)
    nbic_pvce = IntCol(entity= 'foy') # (f5kk, f5lk, f5mk)
    macc_pvce = IntCol(entity= 'foy') # (f5nq, f5oq, f5pq)
    aacc_pvce = IntCol(entity= 'foy') # (f5ne, f5oe, f5pe)
    nacc_pvce = IntCol(entity= 'foy') # (f5nk, f5ok, f5pk)
    mncn_pvce = IntCol(entity= 'foy') # (f5kv, f5lv, f5mv)
    cncn_pvce = IntCol(entity= 'foy') # (f5so, f5nt, f5ot)
    mbnc_pvce = IntCol(entity= 'foy') # (f5hr, f5ir, f5jr)
    abnc_pvce = IntCol(entity= 'foy') # (f5qd, f5rd, f5sd)
    nbnc_pvce = IntCol(entity= 'foy') # (f5qj, f5rj, f5sj)

# pfam only
    inactif   = BoolCol(entity='fam')
    partiel1  = BoolCol(entity='fam')
    partiel2  = BoolCol(entity='fam') 
    categ_inv = IntCol(entity='fam')
    opt_colca = BoolCol(entity='fam')
    empl_dir  = BoolCol(entity='fam') 
    ass_mat   = BoolCol(entity='fam')
    gar_dom   = BoolCol(entity='fam')

# zones apl and calibration 
    tu99 = EnumCol(label = u"tranche d'unité urbaine",
                   entity= 'men',
                   enum=Enum([u'Communes rurales',
                         u'moins de 5 000 habitants',
                         u'5 000 à 9 999 habitants',
                         u'10 000 à 19 999 habitants',
                         u'20 000 à 49 999 habitants',
                         u'50 000 à 99 999 habitants',
                         u'100 000 à 199 999 habitants',
                         u'200 000 habitants ou plus (sauf agglomération parisienne)',
                         u'agglomération parisienne']))
    
    tau99 = EnumCol(label = u"tranche d'aire urbaine", entity='men')
    reg   = EnumCol(entity='men')
    pol99 = EnumCol(entity='men')
    cstotpragr = EnumCol(label = u"catégorie socio_professionelle agrégée de la personne de référence",
                         entity= 'men',
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
                      entity= 'men',
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
                      entity= 'men',
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
                       entity= 'men',
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
                    entity= 'men',
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
                     entity= 'men',
                     enum = Enum([u"Une personne",
                                  u"Deux personnes",
                                  u"Trois personnes",
                                  u"Quatre personnes",
                                  u"Cinq personnes",
                                  u"Six personnes et plus"], start=1))

    ddipl = EnumCol(label = u"diplôme de la personne de référence",
                    entity= 'men',
                    enum = Enum([u"Non renseigné"
                                 u"Diplôme supérieur",
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
    b1ab = IntCol(entity= 'foy') ##  valeur résidence principale avant abattement ##
    b1ac = IntCol(entity= 'foy')
## non bâtis ##
    b1bc = IntCol(entity= 'foy')
    b1be = IntCol(entity= 'foy')
    b1bh = IntCol(entity= 'foy')
    b1bk = IntCol(entity= 'foy') 
## droits sociaux- valeurs mobilières-liquidités- autres meubles ##

    b1cl = IntCol(entity= 'foy')
    b1cb = IntCol(entity= 'foy')
    b1cd = IntCol(entity= 'foy')
    b1ce = IntCol(entity= 'foy')
    b1cf = IntCol(entity= 'foy')
    b1cg = IntCol(entity= 'foy')

    b1co = IntCol(entity= 'foy')

#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réduc ##
    b2gh= IntCol(entity= 'foy')
    
## réductions ##
    b2mt = IntCol(entity= 'foy')
    b2ne = IntCol(entity= 'foy')
    b2mv = IntCol(entity= 'foy')
    b2nf = IntCol(entity= 'foy')
    b2mx = IntCol(entity= 'foy')
    b2na = IntCol(entity= 'foy')
    b2nc = IntCol(entity= 'foy')

##  montant impôt acquitté hors de France ##
    b4rs = IntCol(entity= 'foy')

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
                 entity='ind',
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