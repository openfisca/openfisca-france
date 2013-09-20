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


class InputDescription(ModelDescription):
    '''
    Socio-economic data
    Données d'entrée de la simulation à fournir à partir d'une enquête ou 
    générée par le  générateur de cas type
    '''
    noi = IntCol(label="Numéro d'ordre individuel")

    idmen   = IntCol(label="Identifiant du ménage") # 600001, 600002,
    idfoy   = IntCol(label="Identifiant du foyer") # idmen + noi du déclarant
    idfam   = IntCol(label="Identifiant de la famille") # idmen + noi du chef de famille

    quimen  = EnumCol(QUIMEN)
    quifoy  = EnumCol(QUIFOY)
    quifam  = EnumCol(QUIFAM)
    
    sali = IntCol(label="Salaire imposable", val_type="monetary") #(f1aj, f1bj, f1cj, f1dj, f1ej)
    choi = IntCol(label=u"Chômage imposable", val_type="monetary") # (f1ap, f1bp, f1cp, f1dp, f1ep)
    rsti = IntCol(label="Retraite imposable", val_type="monetary") # (f1as, f1bs, f1cs, f1ds, f1es)
    fra  = IntCol(label="Frais réels",val_type="monetary") # (f1ak, f1bk, f1ck, f1dk, f1ek)

    alr  = IntCol(label = u"Pension alimentaire reçue", val_type="monetary") # (f1ao, f1bo, f1co, f1do, f1eo)
    
    hsup = IntCol( label = "Heures supplémentaires", val_type="monetary")  # (f1au, f1bu, f1cu, f1du, f1eu)
    inv  = BoolCol(label = u'Invalide')
    alt  = BoolCol(label = u'Garde alternée')
    cho_ld = BoolCol(label = 'Chômeur de longue durée') # (f1ai, f1bi, f1ci, f1di, f1ei)
    ppe_tp_sa = BoolCol(label = "Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière") # (f1ax, f1bx, f1cx, f1dx, f1qx)
    ppe_tp_ns = BoolCol(label = "Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière") # (f5nw, f5ow, f5pw)
    ppe_du_sa = IntCol(label = "Prime pour l'emploi des salariés: nombre d'heures payées dans l'année") # (f1av, f1bv, f1cv, f1dv, f1qv)
    ppe_du_ns = IntCol(label = "Prime pour l'emploi des non-salariés:nombre de jours travaillés dans l'année") # (f5nv, f5ov, f5pv)
    jour_xyz = IntCol(default = 360, entity="foy")
    age = AgesCol(label = u"âge" ,  val_type="age")
    agem = AgesCol(label = u"âge (en mois)", val_type="months")
    
    zone_apl = EnumCol(label = u"zone apl", default = 2, entity= 'men')
    loyer = IntCol(label = "Loyer mensuel", entity='men', val_type="monetary") # Loyer mensuel
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
    code_postal = IntCol(label = "Code postal du lieu de résidence", entity='men')
    
    statmarit = EnumCol(label = u"Statut marital",
                          default = 2,
                          enum = Enum([u"Marié",
                                    u"Célibataire",
                                    u"Divorcé",
                                    u"Veuf",
                                    u"Pacsé",
                                    u"Jeune veuf"],start=1))
    
    nbR = IntCol(label="Nombre de titulaires de la carte invalidité d'au moins 80 %", entity= 'foy')
    nbJ = IntCol(label="Nombre d'enfants majeurs célibataires sans enfant", entity= 'foy')
    nbI = IntCol(label="Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité", entity= 'foy')
    nbH = IntCol(label="Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de l'année n-1, ou nés en n-1 ou handicapés quel que soit l'âge", entity= 'foy')
#   vérifier si c'est bien ça pour la nbH et la caseH qui suit 
    nbG = IntCol(label="Nombre d'enfants à charge titulaires de la carte d'invalidité", entity= 'foy')
    nbF = IntCol(label="Nombre d'enfants à charge  non mariés de moins de 18 ans au 1er janvier de l'année n-1, ou nés en n-1 ou handicapés quel que soit l'âge", entity= 'foy')
    nbN = IntCol(label="Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille", entity= 'foy')
    
    caseE = BoolCol(label="Situation pouvant donner droit à une demi-part supplémentaire: enfant élevé seul pendant moins de 5 ans", entity= 'foy')
    caseF = BoolCol(label="Situation pouvant donner droit à une demi-part supplémentaire: conjoint titulaire d'une pension ou d'une carte d'invalidité(vivant ou décédé l'année précédente", entity= 'foy')
    caseG = BoolCol(label="Titulaire d'une pension de veuve de guerre", entity= 'foy')
    caseH = IntCol(label="Année de naissance des enfants à charge en garde alternée", entity= 'foy')
    caseK = BoolCol(label="Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre", entity= 'foy')
    caseL = BoolCol(label="Situation pouvant donner droit à une demi-part supplémentaire: enfant élevé seul pendant plus de 5 ans", entity= 'foy')
    caseN = BoolCol(label="Vous ne vivez pas seul au 1er janvier de l'année n-1", entity= 'foy')
    caseP = BoolCol(label="Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%", entity= 'foy')
    caseS = BoolCol(label="Vous ou votre conjoint êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre", entity= 'foy')
    caseT = BoolCol(label="Vous êtes parent isolé au 1er janvier de l'année n-1", entity= 'foy')
    caseW = BoolCol(label="Votre conjoint âgé de plus de 75 ans, décédé en n-1 était titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre", entity= 'foy')
    
    
    rfr_n_2  = IntCol(entity='foy', label = u"Revenu fiscal de référence année n-2", val_type="monetary") # TODO: provide in data
    nbptr_n_2 = IntCol(entity='foy', label = u"Nombre de parts année n-2", val_type="monetary")  # TODO: provide in data
    
    # Rentes viagères
    f1aw = IntCol(label ="Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : Moins de 50 ans", entity= 'foy', val_type="monetary")
    f1bw = IntCol(label ="Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : De 50 à 59 ans", entity= 'foy', val_type="monetary")
    f1cw = IntCol(label ="Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : De 60 à 69 ans", entity= 'foy', val_type="monetary")
    f1dw = IntCol(label ="Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : A partir de 70 ans", entity= 'foy', val_type="monetary")
    
    # Gain de levée d'option
    #TODO: j'ai changé là mais pas dans le code, il faut chercher les f1uv 
    # et les mettre en f1tvm comme pour sali
    # Il faut aussi le faire en amont dans les tables
    f1tv = IntCol(label="", entity= 'ind') # (f1tv,f1uv)
    f1tw = IntCol(label="", entity= 'ind') # (f1tw,f1uw)
    f1tx = IntCol(label="", entity= 'ind') # (f1tx,f1ux)
 
    
    # RVCM
    # revenus au prélèvement libératoire
    f2da = IntCol(entity= 'foy', label = u"Revenus des actions et parts soumis au prélèvement libératoire", val_type="monetary")
    f2dh = IntCol(entity= 'foy', label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire", val_type="monetary")
    f2ee = IntCol(entity= 'foy', label = u"Revenus au prélèvement libératoire hors actions et assurance-vie", val_type="monetary")

    # revenus ouvrant droit à abattement
    f2dc = IntCol(entity= 'foy', label =u"Revenus des actions et parts donnant droit à abattement", val_type="monetary")
    f2fu = IntCol(entity= 'foy', label =u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement", val_type="monetary")
    f2ch = IntCol(entity= 'foy', label =u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement", val_type="monetary")
    
    # Revenus n'ouvrant pas droit à abattement
    f2ts = IntCol(entity= 'foy', label=u"Revenus de valeurs mobilières et distributions", val_type="monetary")
    f2go = IntCol(entity= 'foy', label= u"Autres revenus distribués et revenus des structures soumiseshors de France à un régime fiscal privilégié", val_type="monetary")
    f2tr = IntCol(entity= 'foy', label = u"Intérêts et autres revenus assimilés", val_type="monetary")
    
    # Autres
    f2cg = IntCol(entity= 'foy', label =u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible", val_type="monetary")
    f2bh = IntCol(entity= 'foy', label =u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible", val_type="monetary")
    f2ca = IntCol(entity= 'foy', label =u"Frais venant en déduction", val_type="monetary")
    f2aa = IntCol(entity='foy', label =u"Déficits des années antérieures non encore déduits: année 2006", val_type="monetary")
    f2ab = IntCol(entity= 'foy', label =u"Crédits d'impôt sur valeurs étrangères", val_type="monetary")
    f2al = IntCol(entity= 'foy', label =u"Déficits des années antérieures non encore déduits: année 2007", val_type="monetary")
    f2am = IntCol(entity= 'foy', label =u"Déficits des années antérieures non encore déduits: année 2008", val_type="monetary")
    f2an = IntCol(entity= 'foy', label =u"Déficits des années antérieures non encore déduits: année 2009", val_type="monetary")
    f2aq = IntCol(entity= 'foy', label =u"Déficits des années antérieures non encore déduits: année 2010", val_type="monetary")
    f2ar = IntCol(entity= 'foy', label =u"Déficits des années antérieures non encore déduits: année 2011", val_type="monetary")
    
    # non accessible (from previous years)
    f2gr = IntCol(entity= 'foy') 
        
    f3vc = IntCol(entity= 'foy', label =u"Produits et plus-values exonérés provenant de structure de capital-risque", val_type="monetary")
    f3vd = IntCol(entity= 'foy', label =u"Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 18 %", val_type="monetary")
    f3ve = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f3vf = IntCol(entity= 'foy', label =u"Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 41 %", val_type="monetary")
    
    f3vl = IntCol(entity= 'foy', label =u"Distributions par des sociétés de capital-risque taxables à 24 %", val_type="monetary")
    f3vi = IntCol(entity= 'foy', label =u"Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 30 %", val_type="monetary")
    f3vm = IntCol(entity= 'foy', label =u"Clôture du PEA : avant l'expiration de la 2e année", val_type="monetary")
    
    f3vj = IntCol(entity= 'foy', label =u"Gains imposables sur option dans la catégorie des salaires: déclarant 1", val_type="monetary")
    f3vk = IntCol(entity= 'foy', label =u"Gains imposables sur option dans la catégorie des salaires: déclarant 2", val_type="monetary")
    f3va = IntCol(entity= 'foy', label =u"Abattement net pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values", val_type="monetary")
    
    # Plus values et gains taxables à des taux forfaitaires
    f3vg = IntCol(entity= 'foy', label=u"Plus-values de cession de valeurs mobilières, droits sociaux et gains assimilés", val_type="monetary")
    f3vh = IntCol(entity= 'foy', label =u"Perte de l'année n-1", val_type="monetary")
    f3vt = IntCol(entity= 'foy', label = u"Clôture du PEA : entre la 2e et la 5e année", val_type="monetary")
    f3vu = IntCol(entity= 'foy')
    f3vv = IntCol(entity= 'foy')

    f3vz = IntCol(entity= 'foy', label=u"Plus-values imposables de cession d’immeubles ou de biens meubles", val_type="monetary") # Revenus 2011


    # Revenu foncier
    f4ba = IntCol(entity= 'foy', label="Revenus fonciers imposables", val_type="monetary")
    f4bb = IntCol(entity= 'foy', label =u"Déficit imputable sur les revenus fonciers", val_type="monetary")
    f4bc = IntCol(entity= 'foy', label =u"Déficit imputable sur le revenu global", val_type="monetary")
    f4bd = IntCol(entity= 'foy', label =u"Déficits antérieurs non encore imputés", val_type="monetary")
    f4be = IntCol(entity= 'foy', label =u"Micro foncier: recettes brutes sans abattement", val_type="monetary")
    
    # Prime d'assurance loyers impayés
    f4bf = IntCol(entity= 'foy', label =u"Primes d'assurance pour loyers impayés des locations conventionnées", val_type="monetary")
    
    f4bl = IntCol(entity= 'foy', label =u"")
    
    f5qm = IntCol(entity= 'foy', label =u"Agents généraux d’assurances: indemnités de cessation d’activité, déclarant 1", val_type="monetary")
    f5rm = IntCol(entity= 'foy', label =u"Agents généraux d’assurances: indemnités de cessation d’activité, déclarant 2", val_type="monetary")
    
    # Csg déductible
    f6de = IntCol(entity= 'foy', label =u"CSG déductible calculée sur les revenus du patrimoine", val_type="monetary")

    # Pensions alimentaires
    f6gi = IntCol(entity= 'foy', label =u"Pensions alimentaires versées à des enfants majeurs: 1er enfant", val_type="monetary")
    f6gj = IntCol(entity= 'foy', label =u"Pensions alimentaires versées à des enfants majeurs: 2eme enfant", val_type="monetary")
    f6el = IntCol(entity= 'foy', label =u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant", val_type="monetary")
    f6em = IntCol(entity= 'foy', label =u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant", val_type="monetary")
    f6gp = IntCol(entity= 'foy', label =u"Autres pensions alimentaires versées (mineurs, ascendants)", val_type="monetary")
    f6gu = IntCol(entity= 'foy', label =u"Autres pensions alimentaires versées (mineurs, ascendants)", val_type="monetary")
    
    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    f6eu = IntCol(entity= 'foy', label =u"Frais d'accueil de personnes de plus de 75 ans dans le besoin", val_type="monetary")
    f6ev = IntCol(entity= 'foy', label =u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit")
    
    # Déductions diverses
    f6dd = IntCol(entity= 'foy',label =u"Déductions diverses", val_type="monetary")
    
    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    f6ps = IntCol(entity= 'foy', label =u"Plafond de déduction: déclarant 1", val_type="monetary")
    f6rs = IntCol(entity= 'foy', label =u"Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: déclarant 1", val_type="monetary")
    f6ss = IntCol(entity= 'foy', label =u"Rachat de cotisations PREFON, COREM et C.G.O.S: déclarant 1", val_type="monetary")
    f6pt = IntCol(entity= 'foy', label =u"Plafond de déduction: déclarant 2", val_type="monetary")
    f6rt = IntCol(entity= 'foy', label =u"Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: déclarant 2", val_type="monetary")
    f6st = IntCol(entity= 'foy', label =u"Rachat de cotisations PREFON, COREM et C.G.O.S: déclarant 2", val_type="monetary")
    f6pu = IntCol(entity= 'foy', label =u"Plafond de déduction: personne à charge", val_type="monetary")
    f6ru = IntCol(entity= 'foy', label =u"Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: personne à charge", val_type="monetary")
    f6su = IntCol(entity= 'foy', label =u"Rachat de cotisations PREFON, COREM et C.G.O.S: personne à charge", val_type="monetary")
    
    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    f6aa = IntCol(entity= 'foy', label =u"Souscriptions en faveur du cinéma ou de l’audiovisuel", val_type="monetary")
    
    # Souscriptions au capital des SOFIPÊCHE
    f6cc = IntCol(entity= 'foy', label =u"Souscriptions au capital des SOFIPÊCHE", val_type="monetary")
    
    # Investissements DOM-TOM dans le cadre d’une entreprise <= 2005
    # ou Versements sur un compte épargne codéveloppement 
    f6eh = IntCol(entity= 'foy', label =u"", val_type="monetary")
    
    # Pertes en capital consécutives à la souscription au capital de sociétés 
    # nouvelles ou de sociétés en difficulté
    f6da = IntCol(entity= 'foy', label =u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté", val_type="monetary")
    
    
    # Dépenses de grosses réparations effectuées par les nus propriétaires
    f6cb = IntCol(entity= 'foy', label =u"Dépenses de grosses réparations effectuées par les nus-propriétaires", val_type="monetary")
    f6hj = IntCol(entity= 'foy', label =u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures", val_type="monetary")
    
    # Sommes à rajouter au revenu imposable
    f6gh = IntCol(entity= 'foy', label =u"Sommes à ajouter au revenu imposable", val_type="monetary")    
    
    # Deficits antérieurs
    f6fa = IntCol(entity= 'foy', label =u"Deficits globaux des années antérieures non encore déduits: année n-7", val_type="monetary")
    f6fb = IntCol(entity= 'foy', label =u"Deficits globaux des années antérieures non encore déduits: année n-6", val_type="monetary")
    f6fc = IntCol(entity= 'foy', label =u"Deficits globaux des années antérieures non encore déduits: année n-5", val_type="monetary")
    f6fd = IntCol(entity= 'foy', label =u"Deficits globaux des années antérieures non encore déduits: année n-4", val_type="monetary")
    f6fe = IntCol(entity= 'foy', label =u"Deficits globaux des années antérieures non encore déduits: année n-3", val_type="monetary")
    f6fl = IntCol(entity= 'foy', label =u"Deficits globaux des années antérieures non encore déduits: année n-2", val_type="monetary")
    
    # Dons
    f7ud = IntCol(entity= 'foy', label =u"Dons à des organismes d'aide aux personnes en difficulté", val_type="monetary")
    f7uf = IntCol(entity= 'foy', label =u"Autres dons", val_type="monetary")
    f7xs = IntCol(entity= 'foy', label =u"Report des années antérieures des réductions et crédits d'impôt: année n-6", val_type="monetary")
    f7xt = IntCol(entity= 'foy', label =u"Report des années antérieures des réductions et crédits d'impôt: année n-5", val_type="monetary")
    f7xu = IntCol(entity= 'foy', label =u"Report des années antérieures des réductions et crédits d'impôt: année n-4", val_type="monetary")
    f7xw = IntCol(entity= 'foy', label =u"Report des années antérieures des réductions et crédits d'impôt: année n-3", val_type="monetary")
    f7xy = IntCol(entity= 'foy', label =u"Report des années antérieures des réductions et crédits d'impôt: année n-2", val_type="monetary")
    
    # Cotisations syndicales des salariées et pensionnés
    f7ac = IntCol(entity= 'foy', label =u"Cotisations syndicales des salariées et pensionnés: déclarant 1", val_type="monetary")
    f7ae = IntCol(entity= 'foy', label =u"Cotisations syndicales des salariées et pensionnés: déclarant 2", val_type="monetary")
    f7ag = IntCol(entity= 'foy', label =u"Cotisations syndicales des salariées et pensionnés: personne à charge", val_type="monetary")

    # Salarié à domicile
    f7db = IntCol(entity= 'foy', label =u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi en n-1", val_type="monetary")
    f7df = IntCol(entity= 'foy', label =u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives en n-1", val_type="monetary")
    f7dq = BoolCol(entity= 'foy', label =u"Emploi direct pour la première fois d'un salarié à domicile en n-1")
    f7dg = BoolCol(entity= 'foy', label =u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'aumoins 80 % en n-1")
    f7dl = IntCol(entity= 'foy', label =u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées en n-1")
    
    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    f7vy = IntCol(entity= 'foy', label =u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité", val_type="monetary")
    f7vz = IntCol(entity= 'foy', label =u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première suivante", val_type="monetary")
    f7vx = IntCol(entity= 'foy', label =u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011", val_type="monetary")
    f7vw = IntCol(entity= 'foy', label =u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010", val_type="monetary")

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    f7cd = IntCol(entity= 'foy', label =u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne", val_type="monetary")
    f7ce = IntCol(entity= 'foy', label =u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne", val_type="monetary")

    # Frais de garde des enfants de moins de 6 ans au 01/01/n-1
    f7ga = IntCol(entity= 'foy', label =u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 1er enfant à charge", val_type="monetary")
    f7gb = IntCol(entity= 'foy', label =u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 2ème enfant à charge", val_type="monetary")
    f7gc = IntCol(entity= 'foy', label =u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 3ème enfant à charge", val_type="monetary")
    f7ge = IntCol(entity= 'foy', label =u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 1er enfant à charge en résidence alternée", val_type="monetary")
    f7gf = IntCol(entity= 'foy', label =u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 2ème enfant à charge en résidence alternée", val_type="monetary")
    f7gg = IntCol(entity= 'foy', label =u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 3ème enfant à charge en résidence alternée", val_type="monetary")

    # Nombre d'enfants à charge poursuivant leurs études
    f7ea = IntCol(entity= 'foy', label =u"Nombre d'enfants à charge poursuivant leurs études au collège")
    f7eb = IntCol(entity= 'foy', label =u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège")
    f7ec = IntCol(entity= 'foy', label =u"Nombre d'enfants à charge poursuivant leurs études au lycée")
    f7ed = IntCol(entity= 'foy', label =u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée")
    f7ef = IntCol(entity= 'foy', label =u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur")
    f7eg = IntCol(entity= 'foy', label =u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur")

    # Intérêts des prêts étudiants
    f7td = IntCol(entity= 'foy', label =u"Intérêts des prêts étudiants versés avant l'année n-1", val_type="monetary")
    f7vo = IntCol(entity= 'foy', label =u"Nombre d'années de remboursement du prêt étudiant avant l'année n-1")
    f7uk = IntCol(entity= 'foy', label =u"Intérêts des prêts étudiants versés en n-1", val_type="monetary")
    
    # Primes de rente survie, contrats d'épargne handicap
    f7gz = IntCol(entity= 'foy', label =u"Primes de rente survie, contrats d'épargne handicap", val_type="monetary")
    
    # Prestations compensatoires
    f7wm = IntCol(entity= 'foy', label =u"Prestations compensatoires: Capital fixé en substitution de rente", val_type="monetary")
    f7wn = IntCol(entity= 'foy', label =u"Prestations compensatoires: Sommes versées en n-1", val_type="monetary")
    f7wo = IntCol(entity= 'foy', label =u"Prestations compensatoires: Sommes totales décidées par jugement en n-1 ou capital reconstitué", val_type="monetary")
    f7wp = IntCol(entity= 'foy', label =u"Prestations compensatoires: Report des sommes décidées en n-2", val_type="monetary")
    
    # Dépenses en faveur de la qualité environnementale de l'habitation principale
    f7we = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise en n-1")
    f7wq = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées")
    f7wh = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale de l'habitation principale: bouquet de travaux")
    f7wk = BoolCol(entity= 'foy', label =u"Votre habitation principale est une maison individuelle")
    f7wf = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1")
    
    # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
    f7wi = IntCol(entity= 'foy', label =u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction", val_type="monetary")
    f7wj = IntCol(entity= 'foy', label =u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées", val_type="monetary")
    f7wl = IntCol(entity= 'foy', label =u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques", val_type="monetary")
    
    # Investissements dans les DOM-TOM dans le cadre d'une entrepise  
    f7ur = IntCol(entity= 'foy', label =u"Investissements réalisés en n-1, total réduction d’impôt", val_type="monetary")
    f7oz = IntCol(entity= 'foy', label =u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6", val_type="monetary")
    f7pz = IntCol(entity= 'foy', label =u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-5", val_type="monetary")
    f7qz = IntCol(entity= 'foy', label =u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-4", val_type="monetary")
    f7rz = IntCol(entity= 'foy', label =u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3", val_type="monetary")
    f7sz = IntCol(entity= 'foy', label =u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-2", val_type="monetary")
    
    # Aide aux créateurs et repreneurs d'entreprises
    f7fy = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1")
    f7gy = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1")
    f7jy = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et ayant pris fin en n-1")
    f7hy = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1")
    f7ky = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1")
    f7iy = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et n'ayant pas pris fin en n-1")
    f7ly = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-2 et ayant pas pris fin en n-1")
    f7my = IntCol(entity= 'foy', label =u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-2 et ayant pas pris fin en n-1 ")

    # Travaux de restauration immobilière
    f7ra = IntCol(entity= 'foy', label =u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbail et paysager", val_type="monetary")
    f7rb = IntCol(entity= 'foy', label =u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé", val_type="monetary")
    
    # Assurance-vie
    f7gw = IntCol(entity= 'foy', label =u"")
    f7gx = IntCol(entity= 'foy', label =u"")
    # f7gy = IntCol() existe ailleurs

    # Investissements locatifs dans le secteur de touristique            
    f7xc = IntCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1", val_type="monetary")
    f7xd = BoolCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans")
    f7xe = BoolCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans")
    f7xf = IntCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures", val_type="monetary")
    f7xh = IntCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme", val_type="monetary")
    f7xi = IntCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures", val_type="monetary")
    f7xj = IntCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures", val_type="monetary")
    f7xk = IntCol(entity= 'foy', label =u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures", val_type="monetary")
    f7xl = IntCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans", val_type="monetary")
    f7xm = IntCol(entity= 'foy', label =u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures", val_type="monetary")
    f7xn = IntCol(entity= 'foy', label =u"Investissements locatifs dans une résidence hôtelière à vocation sociale: investissement réalisé en n-1", val_type="monetary")
    f7xo = IntCol(entity= 'foy', label =u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures", val_type="monetary")
    
    # Souscriptions au capital des PME
    f7cf = IntCol(entity= 'foy', label =u"Souscriptions au capital des PME non cotées, montant versé en n-1", val_type="monetary")
    f7cl = IntCol(entity= 'foy', label =u"Souscriptions au capital des PME non cotées, report de versement de l'année n-4", val_type="monetary")
    f7cm = IntCol(entity= 'foy', label =u"Souscriptions au capital des PME non cotées, report de versement de l'année n-3", val_type="monetary")
    f7cn = IntCol(entity= 'foy', label =u"Souscriptions au capital des PME non cotées, report de versement de l'année n-2", val_type="monetary")
    f7cu = IntCol(entity= 'foy', label =u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures", val_type="monetary")

    # Souscription au capital d’une SOFIPECHE 
    f7gs = IntCol(entity= 'foy', label =u"Souscription au capital d’une SOFIPECHE", val_type="monetary")

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité    
    f7ua = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7ub = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7uc = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7ui = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7uj = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7qb = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7qc = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7qd = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7ql = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7qt = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7qm = IntCol(entity= 'foy', label =u"", val_type="monetary")
    
    # Souscription de parts de fonds communs de placement dans l'innovation, 
    # de fonds d'investissement de proximité    
    f7gq = IntCol(entity= 'foy', label =u"Souscription de parts de fonds communs de placement dans l'innovation", val_type="monetary")
    f7fq = IntCol(entity= 'foy', label =u"Souscription de parts de fonds d'investissement de proximité", val_type="monetary")
    f7fm = IntCol(entity= 'foy', label =u"Souscription de parts de fonds d'investissement de proximité investis en Corse", val_type="monetary")
    f7fl = IntCol(entity= 'foy', label =u"")
    
    # Souscriptions au capital de SOFICA
    f7gn = IntCol(entity= 'foy', label =u"Souscriptions au capital de SOFICA 48 %", val_type="monetary")
    f7fn = IntCol(entity= 'foy', label =u"Souscriptions au capital de SOFICA 40 %", val_type="monetary")

    # Intérêts d'emprunt pour reprise de société
    f7fh = IntCol(entity= 'foy', label =u"Intérêts d'emprunt pour reprise de société", val_type="monetary")         

    # Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)        
    f7ff = IntCol(entity= 'foy', label =u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)", val_type="monetary")
    f7fg = IntCol(entity= 'foy', label =u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations")
    
    # Travaux de conservation et de restauration d’objets classés monuments historiques
    f7nz = IntCol(entity= 'foy', label =u"Travaux de conservation et de restauration d’objets classés monuments historiques", val_type="monetary")
    
    # Dépenses de protection du patrimoine naturel
    f7ka = IntCol(entity= 'foy', label =u"Dépenses de protection du patrimoine naturel", val_type="monetary")

    # Intérêts d'emprunts
    f7wg = IntCol(entity= 'foy', label =u"Intérêts d'emprunts", val_type="monetary")
    
    # Intérêts des prêts à la consommation (case UH)
    f7uh = IntCol(entity= 'foy', label =u"", val_type="monetary")
    
    # Investissements forestiers
    f7un = IntCol(entity= 'foy', label =u"Investissements forestiers: acquisition", val_type="monetary")
    
    # Intérêts pour paiement différé accordé aux agriculteurs
    f7um = IntCol(entity= 'foy', label =u"Intérêts pour paiement différé accordé aux agriculteurs", val_type="monetary")

    # Investissements locatifs neufs : Dispositif Scellier:
    f7hj = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole", val_type="monetary")
    f7hk = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM", val_type="monetary")
    f7hn = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier", val_type="monetary")
    f7ho = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier", val_type="monetary")
    f7hl = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)", val_type="monetary")
    f7hm = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds", val_type="monetary")
    f7hr = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 (métropole et DOM ne respectant pas les plafonds)", val_type="monetary")
    f7hs = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM et respectant les plafonds", val_type="monetary")
    f7la = IntCol(entity= 'foy', label =u"Investissements locatifs neufs dispositif Scellier: report du solde de réduction d'impôt non encore imputé", val_type="monetary")

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    f7ij = IntCol(entity= 'foy', label =u"Investissement destinés à la location meublée non professionnelle: engagement de réalisation de l'investissement en n-1", val_type="monetary")
    f7il = IntCol(entity= 'foy', label =u"Investissement destinés à la location meublée non professionnelle: promesse d'achat en n-2", val_type="monetary")
    f7im = IntCol(entity= 'foy', label =u"Investissement destinés à la location meublée non professionnelle: promesse d'achat en n-3", val_type="monetary")
    f7ik = IntCol(entity= 'foy', label =u"Reports de 1/9 de l'investissement réalisé et achevé au cours de l'année n-4", val_type="monetary")
    f7is = IntCol(entity= 'foy', label =u"Report du solde de réduction d'impôt non encor imputé: année  n-4", val_type="monetary")
    
    # Investissements locatifs dans les résidences de tourisme situées dans une zone de 
    # revitalisation rurale
    f7gt = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7xg = IntCol(entity= 'foy', label =u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme", val_type="monetary")
    f7gu = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7gv = IntCol(entity= 'foy', label =u"", val_type="monetary")
    
    # Avoir fiscaux et crédits d'impôt     
    # f2ab déjà disponible
    f8ta = IntCol(entity= 'foy', label =u"Retenue à la source en France ou impôt payé à l'étranger", val_type="monetary")
    f8tb = IntCol(entity= 'foy', label =u"Crédit d'impôt recherche non encore remboursé", val_type="monetary")
    f8tf = IntCol(entity= 'foy', label =u"Reprises de réductions ou de crédits d'impôt", val_type="monetary")
    f8tg = IntCol(entity= 'foy', label =u"Crédits d'impôt en faveur des entreprises: Investissement en Corse", val_type="monetary")
    f8th = IntCol(entity= 'foy', label =u"Retenue à la source élus locaux", val_type="monetary")
    f8tc = IntCol(entity= 'foy', label =u"Crédit d'impôt recherche non encore remboursé (années antérieures)", val_type="monetary")
    f8td = IntCol(entity= 'foy', label =u"Contribution exceptionnelle sur les hauts revenus")
    f8te = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé", val_type="monetary")
    f8to = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures", val_type="monetary")
    f8tp = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt", val_type="monetary")
    f8uz = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Famille", val_type="monetary")
    f8tz = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Apprentissage", val_type="monetary")
    f8wa = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Agriculture biologique", val_type="monetary")
    f8wb = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Prospection commerciale", val_type="monetary")
    f8wc = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Nouvelles technologies", val_type="monetary")
    f8wd = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise", val_type="monetary")
    f8we = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Intéressement", val_type="monetary")
    f8wr = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Métiers d'art", val_type="monetary")
    f8ws = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes", val_type="monetary")
    f8wt = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs", val_type="monetary")
    f8wu = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Maître restaurateur", val_type="monetary")
    f8wv = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Débitants de tabac", val_type="monetary")
    f8wx = IntCol(entity= 'foy', label =u"Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise", val_type="monetary")
    f8wy = IntCol(entity= 'foy', label =u"", val_type="monetary")
    
    # Acquisition de biens culturels
    f7uo = IntCol(entity= 'foy', label =u"Acquisition de biens culturels", val_type="monetary")

    
    # Mécénat d'entreprise    
    f7us = IntCol(entity= 'foy', label =u"Réduction d'impôt mécénat d'entreprise", val_type="monetary")

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    # f7wf = IntCol() déjà disponible
    # f7wh = IntCol() déjà disponible
    # f7wk = IntCol() déjà disponible
    # f7wq = IntCol() déjà disponible
    f7sb = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %", val_type="monetary")
    f7sd = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 40 %", val_type="monetary")
    f7se = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 50 %", val_type="monetary")
    f7sh = IntCol(entity= 'foy', label =u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 15 %", val_type="monetary")
    # f7wg = IntCol() déjà disponible
    f7sc = IntCol(entity= 'foy', label =u"", val_type="monetary")
    
    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???
    f7up = IntCol(entity= 'foy', label =u"Crédit d'impôt", val_type="monetary")
    f7uq = IntCol(entity= 'foy', label =u"Crédit d'impôt", val_type="monetary")

    # Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
    f1ar = IntCol(entity= 'foy', label =u"Crédit d'impôt aide à la mobilité")
    f1br = IntCol(entity= 'foy', label =u"Crédit d'impôt aide à la mobilité")
    f1cr = IntCol(entity= 'foy', label =u"Crédit d'impôt aide à la mobilité")
    f1dr = IntCol(entity= 'foy', label =u"Crédit d'impôt aide à la mobilité")
    f1er = IntCol(entity= 'foy', label =u"Crédit d'impôt aide à la mobilité")

    # Crédit d’impôt directive « épargne » (case 2BG)
    f2bg = IntCol(entity= 'foy', label =u"Crédit d’impôt directive « épargne »", val_type="monetary")
    
    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    f4tq = IntCol(entity= 'foy', label =u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail", val_type="monetary")
    

    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    # f7wf
    # f7wi
    # f7wj
    # f7wl
    f7sf = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f7si = IntCol(entity= 'foy', label =u"", val_type="monetary")
    
    # Frais de garde des enfants à l’extérieur du domicile 
    """ là je ne sais pas à quoi cela correspond, les frais de garde des enfants sont en 7ga etc..., 
    en 4 ce sont les revenus fonciers depuis un certain nb d'années, et ce n'est pas du g... 
    en plus les f4ga..ne sont pas utilisées dans les prog (sauf un commentaire dans 08_final), moi, je supprimerais ça!
    """
    f4ga = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f4gb = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f4gc = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f4ge = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f4gf = IntCol(entity= 'foy', label =u"", val_type="monetary")
    f4gg = IntCol(entity= 'foy', label =u"", val_type="monetary")


    # Auto-entrepreneur : versements libératoires d’impôt sur le revenu 
    f8uy = IntCol(entity= 'foy', label =u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu", val_type="monetary")


    # Revenus des professions non salariées
    
    frag_exon = IntCol(entity= 'ind', label =u"Revenus agricoles exonérés (régime du forfait)", val_type="monetary") # (f5hn, f5in, f5jn)
    frag_impo = IntCol(entity= 'ind', label =u"Revenus agricoles imposables (régime du forfait)", val_type="monetary") # (f5ho, f5io, f5jo)    
    arag_exon = IntCol(entity= 'ind', label =u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type="monetary") # (f5hb, f5ib, f5jb)
    arag_impg = IntCol(entity= 'ind', label =u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",val_type="monetary") # (f5hc, f5ic, f5jc)
    arag_defi = IntCol(entity= 'ind', label =u"Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type="monetary") # (f5hf, f5if, f5jf)
    nrag_exon = IntCol(entity= 'ind', label =u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)", val_type="monetary") # (f5hh, f5ih, f5jh)
    nrag_impg = IntCol(entity= 'ind', label =u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)", val_type="monetary") # (f5hi, f5ii, f5ji)
    nrag_defi = IntCol(entity= 'ind', label =u"Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)", val_type="monetary") # (f5hl, f5il, f5jl)
    nrag_ajag = IntCol(entity= 'ind', label =u"Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type="monetary") # (f5hm, f5im, f5jm)

    mbic_exon = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)", val_type="monetary") # (f5kn, f5ln, f5mn)
    abic_exon = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5kb, f5lb, f5mb)
    nbic_exon = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5kh, f5lh, f5mh)
    mbic_impv = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)", val_type="monetary") # (f5ko, f5lo, f5mo)
    mbic_imps = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)", val_type="monetary") # (f5kp, f5lp, f5mp)
    abic_impn = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5kc, f5lc, f5mc)
    abic_imps = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5kd, f5ld, f5md)
    nbic_impn = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5ki, f5li, f5mi)
    nbic_imps = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux imposables: régime simplifié sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5kj, f5lj, f5mj)
    abic_defn = IntCol(entity= 'ind', label=u"Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5kf, f5lf, f5mf)
    abic_defs = IntCol(entity= 'ind', label=u"Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5kg, f5lg, f5mg)
    nbic_defn = IntCol(entity= 'ind', label=u"Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5kl, f5ll, f5ml)
    nbic_defs = IntCol(entity= 'ind', label=u"Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5km, f5lm, f5mm)
    nbic_apch = IntCol(entity= 'ind', label=u"Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5ks, f5ls, f5ms)
    
    macc_exon = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)", val_type="monetary") # (f5nn, f5on, f5pn)
    aacc_exon = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5nb, f5ob, f5pb)
    nacc_exon = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5nh, f5oh, f5ph)
    macc_impv = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)", val_type="monetary") # (f5no, f5oo, f5po)
    macc_imps = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)", val_type="monetary") # (f5np, f5op, f5pp)
    aacc_impn = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5nc, f5oc, f5pc)
    aacc_imps = IntCol(entity= 'ind', label=u"Locations meublées non professionnelles (régime micro entreprise)", val_type="monetary") # (f5nd, f5od, f5pd)
    aacc_defn = IntCol(entity= 'ind', label=u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5nf, f5of, f5pf)
    aacc_defs = IntCol(entity= 'ind', label=u"Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)", val_type="monetary") # (f5ng, f5og, f5pg)
    nacc_impn = IntCol(entity= 'ind', label=u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5ni, f5oi, f5pi)
    nacc_imps = IntCol(entity= 'ind', label=u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)", val_type="monetary") # (f5nj, f5oj, f5pj)
    nacc_defn = IntCol(entity= 'ind', label=u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5nl, f5ol, f5pl)
    nacc_defs = IntCol(entity= 'ind', label=u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5nm, f5om, f5pm)
    mncn_impo = IntCol(entity= 'ind', label=u"Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5ku, f5lu, f5mu)
    cncn_bene = IntCol(entity= 'ind', label=u"Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)", val_type="monetary") # (f5sn, f5ns, f5os)
    cncn_defi = IntCol(entity= 'ind', label=u"Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)", val_type="monetary") # (f5sp, f5nu, f5ou, f5sr)

    mbnc_exon = IntCol(entity= 'ind', label=u"Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5hp, f5ip, f5jp)
    abnc_exon = IntCol(entity= 'ind', label=u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type="monetary") # (f5qb, f5rb, f5sb)
    nbnc_exon = IntCol(entity= 'ind', label=u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)", val_type="monetary") # (f5qh, f5rh, f5sh)
    mbnc_impo = IntCol(entity= 'ind', label=u"Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5hq, f5iq, f5jq)
    abnc_impo = IntCol(entity= 'ind', label=u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type="monetary") # (f5qc, f5rc, f5sc)
    abnc_defi = IntCol(entity= 'ind', label=u"Déficits non commerciaux professionnels (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type="monetary") # (f5qe, f5re, f5se)
    nbnc_impo = IntCol(entity= 'ind', label=u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)", val_type="monetary") # (f5qi, f5ri, f5si)
    nbnc_defi = IntCol(entity= 'ind', label=u"Déficits non commerciaux professionnels (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)", val_type="monetary") # (f5qk, f5rk, f5sk)

    mbic_mvct = IntCol(entity= 'foy', label=u"Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)", val_type="monetary") # (f5hu)
    macc_mvct = IntCol(entity= 'foy', label=u"Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)", val_type="monetary") # (f5iu)
    mncn_mvct = IntCol(entity= 'foy', label=u"Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5ju)
    mbnc_mvct = IntCol(entity= 'foy', label=u"Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5kz
    
    frag_pvct = IntCol(entity= 'ind', label=u"Plus-values agricoles  à court terme (régime du forfait)", val_type="monetary") # (f5hw, f5iw, f5jw)
    mbic_pvct = IntCol(entity= 'ind', label=u"Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)", val_type="monetary") # (f5kx, f5lx, f5mx)
    macc_pvct = IntCol(entity= 'ind', label=u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)", val_type="monetary") # (f5nx, f5ox, f5px)
    mbnc_pvct = IntCol(entity= 'ind', label=u"Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5hv, f5iv, f5jv)
    mncn_pvct = IntCol(entity= 'ind', label=u"Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5ky, f5ly, f5my)
  
    mbic_mvlt = IntCol(entity= 'ind', label=u"Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)", val_type="monetary") # (f5kr, f5lr, f5mr)
    macc_mvlt = IntCol(entity= 'ind', label=u"Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)", val_type="monetary") # (f5nr, f5or, f5pr)
    mncn_mvlt = IntCol(entity= 'ind', label=u"Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5kw, f5lw, f5mw)
    mbnc_mvlt = IntCol(entity= 'ind', label=u"Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5hs, f5is, f5js)

    frag_pvce = IntCol(entity= 'ind', label=u"Plus-values agricoles de cession taxables à 16% (régime du forfait)", val_type="monetary") # (f5hx, f5ix, f5jx)
    arag_pvce = IntCol(entity= 'ind', label=u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type="monetary") # (f5he, f5ie, f5je)
    nrag_pvce = IntCol(entity= 'ind', label=u"Revenus non commerciaux non professionnels exonérés avec AA ou viseur (régime de la déclaration controlée)", val_type="monetary") # (f5hk, f5lk, f5jk)
    mbic_pvce = IntCol(entity= 'ind', label=u"Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)", val_type="monetary") # (f5kq, f5lq, f5mq)
    abic_pvce = IntCol(entity= 'ind', label=u"Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5ke, f5le, f5me)
    nbic_pvce = IntCol(entity= 'ind', label=u"Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)", val_type="monetary") # (f5kk, f5ik, f5mk)
    macc_pvce = IntCol(entity= 'ind', label=u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)", val_type="monetary") # (f5nq, f5oq, f5pq)
    aacc_pvce = IntCol(entity= 'ind', label=u"Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)", val_type="monetary") # (f5ne, f5oe, f5pe)
    nacc_pvce = IntCol(entity= 'ind', label=u"Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5nk, f5ok, f5pk)
    mncn_pvce = IntCol(entity= 'ind', label=u"Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5kv, f5lv, f5mv)
    cncn_pvce = IntCol(entity= 'ind', label=u"Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)", val_type="monetary") # (f5so, f5nt, f5ot)
    mbnc_pvce = IntCol(entity= 'ind', label=u"Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)", val_type="monetary") # (f5hr, f5ir, f5jr)
    abnc_pvce = IntCol(entity= 'ind', label=u"Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type="monetary") # (f5qd, f5rd, f5sd)
    nbnc_pvce = IntCol(entity= 'ind', label=u"Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)", val_type="monetary") # (f5qj, f5rj, f5sj)

# pfam only
    inactif   = BoolCol(entity='fam')
    partiel1  = BoolCol(entity='fam')
    partiel2  = BoolCol(entity='fam') 
    categ_inv = IntCol()
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
    
    tau99 = EnumCol(label = u"tranche d'aire urbaine",
                    entity='men',
                    enum = Enum([u'Communes hors aire urbaine',
                                 u'Aire urbaine de moins de 15 000 habitants',
                                 u'Aire urbaine de 15 000 à 19 999 habitants',
                                 u'Aire urbaine de 20 000 à 24 999 habitants',
                                 u'Aire urbaine de 25 000 à 34 999 habitants',
                                 u'Aire urbaine de 35 000 à 49 999 habitants',
                                 u'Aire urbaine de 50 000 à 99 999 habitants',
                                 u'Aire urbaine de 100 000 à 199 999 habitants',
                                 u'Aire urbaine de 200 000 à 499 999 habitants',
                                 u'Aire urbaine de 500 000 à 9 999 999 habitants',
                                 u'Aire urbaine de Paris']))
    reg   = EnumCol(label = u"Région",
                    entity='men',
                    enum = Enum([u'Ile-de-France',
                                 u'Champagne-Ardenne',
                                 u'Picardie',
                                 u'Haute-Normandie',
                                 u'Centre',
                                 u'Basse-Normandie',
                                 u'Bourgogne',
                                 u'Nord-Pas de Calais',
                                 u'Lorraine',
                                 u'Alsace',
                                 u'Franche-Comté',
                                 u'Pays de la Loire',
                                 u'Bretagne',
                                 u'Poitou-Charentes',
                                 u'Aquitaine',
                                 u'Midi-Pyrénées',
                                 u'Limousin',
                                 u'Rhône-Alpes',
                                 u'Auvergne',
                                 u'Languedoc-Roussillon',
                                 u"Provence-Alpes-Côte-d'Azur",
                                 u'Corse' ]))
    pol99 = EnumCol(label = u"Catégorie de la commune au sein du découpage en aires et espaces urbains", 
                    entity='men',
                    enum = Enum([ u"Commune appartenant à un pôle urbain",
                                 u"Commune monopolarisée (appartenant à une couronne périurbaine",
                                 u"Commune monopolarisée",
                                 u"Espace à dominante rurale"]))

    
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
    
    
#    typmen15 = EnumCol(label = u"Type de ménage",
#                       entity= 'men',
#                       enum = Enum([u"Personne seule active",
#                                    u"Personne seule inactive",
#                                    u"Familles monoparentales, parent actif",
#                                    u"Familles monoparentales, parent inactif et au moins un enfant actif",
#                                    u"Familles monoparentales, tous inactifs",
#                                    u"Couples sans enfant, 1 actif",
#                                    u"Couples sans enfant, 2 actifs",
#                                    u"Couples sans enfant, tous inactifs",
#                                    u"Couples avec enfant, 1 membre du couple actif",
#                                    u"Couples avec enfant, 2 membres du couple actif",
#                                    u"Couples avec enfant, couple inactif et au moins un enfant actif",
#                                    u"Couples avec enfant, tous inactifs",
#                                    u"Autres ménages, 1 actif",
#                                    u"Autres ménages, 2 actifs ou plus",
#                                    u"Autres ménages, tous inactifs"],start=1))
    
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

                                 
#    nbinde = EnumCol(label = u"taille du ménage",
#                     entity= 'men',
#                     enum = Enum([u"Une personne",
#                                  u"Deux personnes",
#                                  u"Trois personnes",
#                                  u"Quatre personnes",
#                                  u"Cinq personnes",
#                                  u"Six personnes et plus"], start=1))

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
                                  u"Inactif"],start=1)) # 5 postes normalement TODO: check=0
    wprm_init = FloatCol(label="Effectifs")


## ISF ##
    
## Immeubles bâtis ##
    b1ab = IntCol(entity= 'ind', label =u"valeur résidence principale avant abattement", val_type="monetary") ##  valeur résidence principale avant abattement ##
    b1ac = IntCol(entity= 'foy', label =u"valeur autres immeubles avant abattement", val_type="monetary")
## non bâtis ##
    b1bc = IntCol(entity= 'foy', label =u"Immeubles non bâtis: bois, fôrets et parts de groupements forestiers", val_type="monetary")
    b1be = IntCol(entity= 'foy', label =u"Immeubles non bâtis: biens ruraux loués à long termes", val_type="monetary")
    b1bh = IntCol(entity= 'foy', label =u"Immeubles non bâtis: parts de groupements fonciers agricoles et de groupements agricoles fonciers", val_type="monetary")
    b1bk = IntCol(entity= 'foy', label =u"Immeubles non bâtis: autres biens", val_type="monetary") 

## droits sociaux- valeurs mobilières-liquidités- autres meubles ##
    b1cl = IntCol(entity= 'foy', label =u"Parts et actions détenues par les salariés et mandataires sociaux", val_type="monetary")
    b1cb = IntCol(entity= 'foy', label =u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum", val_type="monetary")
    b1cd = IntCol(entity= 'foy', label =u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité", val_type="monetary")
    b1ce = IntCol(entity= 'foy', label =u"Autres valeurs mobilières", val_type="monetary")
    b1cf = IntCol(entity= 'foy', label =u"Liquidités", val_type="monetary")
    b1cg = IntCol(entity= 'foy', label =u"Autres biens meubles", val_type="monetary")

    b1co = IntCol(entity= 'foy', label =u"Autres biens meubles: contrats d'assurance-vie", val_type="monetary")

#    b1ch
#    b1ci
#    b1cj
#    b1ck


## passifs et autres réduc ##
    b2gh= IntCol(entity= 'foy', label =u"Total du passif et autres déductions", val_type="monetary")
    
## réductions ##
    b2mt = IntCol(entity= 'foy', label =u"Réductions pour investissements directs dans une société", val_type="monetary")
    b2ne = IntCol(entity= 'foy', label =u"Réductions pour investissements directs dans une société", val_type="monetary")
    b2mv = IntCol(entity= 'foy', label =u"Réductions pour investissements par sociétés interposées, holdings" , val_type="monetary")
    b2nf = IntCol(entity= 'foy', label =u"Réductions pour investissements par sociétés interposées, holdings", val_type="monetary")
    b2mx = IntCol(entity= 'foy', label =u"Réductions pour investissements par le biais de FIP", val_type="monetary")
    b2na = IntCol(entity= 'foy', label =u"Réductions pour investissements par le biais de FCPI ou FCPR", val_type="monetary")
    b2nc = IntCol(entity= 'foy', label =u"Réductions pour dons à certains organismes d'intérêt général", val_type="monetary")

##  montant impôt acquitté hors de France ##
    b4rs = IntCol(entity= 'foy', label =u"Montant de l'impôt acquitté hors de France", val_type="monetary")

## BOUCLIER FISCAL ##

    rev_or= IntCol(entity= 'foy', label =u"", val_type="monetary")
    rev_exo= IntCol(entity= 'foy', label =u"", val_type="monetary")

    tax_fonc= IntCol(entity= 'foy', label =u"",val_type="monetary")
    restit_imp= IntCol(entity= 'foy', label =u"", val_type="monetary")
        
    # to remove
    champm = BoolCol(entity='men', default = True)
    wprm = FloatCol(entity='men', default = 1,label="Effectifs")
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
    
    m_afeamam = IntCol(entity='men')
    m_agedm   = IntCol(entity='men')
    m_clcam   = IntCol(entity='men')
    m_colcam  = IntCol(entity='men')
    m_mgamm   = IntCol(entity='men')
    m_mgdomm  = IntCol(entity='men')
    zthabm    = IntCol(entity='men')  # Devrait être renommée tax
    
    adoption    = BoolCol(entity="ind",
                        label=u"Enfant adopté")

    # tax_hab= IntCol()    