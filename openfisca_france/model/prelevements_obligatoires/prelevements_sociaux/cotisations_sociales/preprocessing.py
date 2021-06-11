import copy
import logging

from openfisca_france.model.base import *
from openfisca_france.model.revenus.activite.salarie import TypesCategorieSalarie

DEBUG_SAL_TYPE = 'public_titulaire_etat'
log = logging.getLogger(__name__)

# TODO: contribution patronale de prévoyance complémentaire


def build_pat(node_json):  # Ici node_json c'est le dossier 'parameters'
    """Construit le dictionnaire de barèmes des cotisations employeur à partir de node_json.children['cotsoc'].children['pat']"""
    pat = copy.deepcopy(node_json.children['cotsoc'].children['pat'])  # Génère une deepcopy du parameters.cotsoc.pat (de l'arbre réel)
    commun = pat.children.pop('commun')  # Removes and returns the key "commun" of pat.children dict
    # print("Dict commun.children : \n", commun.children)

    # Réindexation: nouveaux chemins
    autres = node_json.prelevements_sociaux.autres_taxes_participations_assises_salaires
    retraites = node_json.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chom = node_json.prelevements_sociaux.cotisations_regime_assurance_chomage
    cotiz = node_json.prelevements_sociaux.cotisations_securite_sociale_regime_general
    public = node_json.prelevements_sociaux.cotisations_secteur_public

    # Réindexation Apprentissage
    # for bareme in ['apprentissage', 'apprentissage_add', 'apprentissage_alsace_moselle']:
    #     commun.children[bareme] = commun.children['apprentissage_node'].children[bareme]
    # del commun.children['apprentissage_node']

    for bareme in ['apprentissage', 'apprentissage_add', 'apprentissage_alsace_moselle']:
        apprentissages = autres.apprentissage.children[bareme]
    commun.children[bareme] = apprentissages    
    del commun.children['apprentissage_node'] # Pour debug

    # Si on decide qu'on ne s'en PAS fiche d'avoir plus de variables dans les cotsoc_virtuelles
    for bareme in ['apprentissage', 'apprentissage_add', 'apprentissage_alsace_moselle']:
        apprentissages = autres.apprentissage.children[bareme]
    commun.children[bareme] = apprentissages 
    # Et apres on remplace dans les formules ci-dessous: ex: pat.children['noncadre'].children.update(apprentissages.children)

    # Réindexation Formation
    #commun.children['formprof_09'] = commun.children['formprof_node'].children['formprof_09']
    #commun.children['formprof_1019'] = commun.children['formprof_node'].children['formprof_1019']
    #commun.children['formprof_20'] = commun.children['formprof_node'].children['formprof_20']
    #del commun.children['formprof_node']
#
    commun.children['formprof_09'] = autres.formation.children['formprof_09']
    commun.children['formprof_1019'] = autres.formation.children['formprof_1019']
    commun.children['formprof_20'] = autres.formation.children['formprof_20']
    del commun.children['formprof_node']

    # Réindexation Construction
    #commun.children['construction'] = commun.children['construction_node'].children['construction_20']
    #del commun.children['construction_node']

    commun.children['construction'] = autres.construction.children['construction_20']
    del commun.children['construction_node']

    
    # Réindexation NonCadre
    # Ici on met tout (dossiers aussi) le contenu de commun dans noncadre (en gardant le previous content) 
    #pat.children['noncadre'].children.update(commun.children)
    #print(pat.children['noncadre'].children, file=open("openfisca_france/scripts/parameters/Noncadre_AVANT.txt", "w"))

    # Initialisation
    #pat.children['noncadre'].children.update(retraites.noncadre.children)
    # commun.children
    #pat.children['noncadre'].children.update(autres.apprentissage.children)
    #pat.children['noncadre'].children.update(autres.construction.children)
    #pat.children['noncadre'].children.update(autres.formation.children)
    #pat.children['noncadre'].children.update(chom.assedic.children)
    #pat.children['noncadre'].children.update(chom.chomfg.children)
    #pat.children['noncadre'].children.update(cotiz.csa.bareme.children)  # À harmoniser !
    #pat.children['noncadre'].children.update(cotiz.famille.bareme.children)  # À harmoniser !
    #pat.children['noncadre'].children.update(autres.fnal.children)  # À harmoniser !
    #pat.children['noncadre'].children.update(autres.fin_syndic.children)  # À harmoniser !
    #pat.children['noncadre'].children.update(cotiz.penibilite.bareme.children)  # À harmoniser !
    #pat.children['noncadre'].children.update(cotiz.cnav.bareme.children)  # À harmoniser !
    #pat.children['noncadre'].children.update(cotiz.mmid.bareme.children)  # À harmoniser ! + Créer params depuis IPP
    #print(pat.children['noncadre'].children, file=open("openfisca_france/scripts/parameters/Noncadre_APRES.txt", "w"))
    

    # Réindexation Cadre
    pat.children['cadre'].children.update(commun.children)
    #print(pat.children['cadre'].children, file=open("openfisca_france/scripts/parameters/Cadre_AVANT.txt", "w"))

    # Initialisation
    pat.children['cadre'].children.update(retraites.cadre.children)
    # commun.children
    pat.children['cadre'].children.update(autres.apprentissage.children)
    pat.children['cadre'].children.update(autres.construction.children)
    pat.children['cadre'].children.update(autres.formation.children)
    pat.children['cadre'].children.update(chom.assedic.children)
    pat.children['cadre'].children.update(chom.chomfg.children)
    pat.children['cadre'].children.update(cotiz.csa.bareme.children)  # À harmoniser !
    pat.children['cadre'].children.update(cotiz.famille.bareme.children)  # À harmoniser !
    pat.children['cadre'].children.update(autres.fnal.children)  # À harmoniser !
    pat.children['cadre'].children.update(autres.fin_syndic.children)  # À harmoniser !
    pat.children['cadre'].children.update(cotiz.penibilite.bareme.children)  # À harmoniser !
    pat.children['cadre'].children.update(cotiz.cnav.bareme.children)  # À harmoniser !
    pat.children['cadre'].children.update(cotiz.mmid.bareme.children)  # À harmoniser ! + Créer params depuis IPP
    #print(pat.children['cadre'].children, file=open("openfisca_france/scripts/parameters/Cadre_APRES.txt", "w"))
    
    # Réindexation Fonc ??
    #pat.children['fonc'].children['contract'].children.update(commun.children)
    #print(pat.children['fonc'].children, file=open("openfisca_france/scripts/parameters/Fonc_AVANT.txt", "w"))

    # Initialisation
    # Collectivités Locales
    pat.children['fonc'].children['colloc'].children['hospitaliere'] = public.cnral.hospitaliere
    pat.children['fonc'].children['colloc'].children['territoriale'] = public.cnral.territoriale
    pat.children['fonc'].children['colloc'].children.update(public.cnral.children)
    pat.children['fonc'].children['colloc'].children.update(public.mmid.colloc.children)
    pat.children['fonc'].children['colloc'].children.update(public.rafp.children)
    # Contractuel
    pat.children['fonc'].children['contract'] = public.ircantec
    # Etat
    pat.children['fonc'].children['etat'].children.update(public.mmid.etat.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.ati.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.pension.children)
    # commun.children
    pat.children['fonc'].children["contract"].children.update(autres.apprentissage.children)
    pat.children['fonc'].children["contract"].children.update(autres.construction.children)
    pat.children['fonc'].children["contract"].children.update(autres.formation.children)
    pat.children['fonc'].children["contract"].children.update(chom.assedic.children)
    pat.children['fonc'].children["contract"].children.update(chom.chomfg.children)
    pat.children['fonc'].children["contract"].children.update(cotiz.csa.bareme.children)  # À harmoniser !
    pat.children['fonc'].children["contract"].children.update(cotiz.famille.bareme.children)  # À harmoniser !
    pat.children['fonc'].children["contract"].children.update(autres.fnal.children)  # À harmoniser !
    pat.children['fonc'].children["contract"].children.update(autres.fin_syndic.children)  # À harmoniser !
    pat.children['fonc'].children["contract"].children.update(cotiz.penibilite.bareme.children)  # À harmoniser !
    pat.children['fonc'].children["contract"].children.update(cotiz.cnav.bareme.children)  # À harmoniser !
    pat.children['fonc'].children["contract"].children.update(cotiz.mmid.bareme.children)  # À harmoniser ! + Créer params depuis IPP
    print(pat.children['fonc'].children, file=open("openfisca_france/scripts/parameters/Fonc_APRES.txt", "w"))


    # Renaming
    pat.children['prive_non_cadre'] = pat.children.pop('noncadre')
    pat.children['prive_cadre'] = pat.children.pop('cadre')

    # Rework commun to deal with public employees
    for var in ["apprentissage", "apprentissage_add", "apprentissage_alsace_moselle", "assedic", "chomfg", "construction", "maladie", "formprof_09",
                "formprof_1019", "formprof_20", "vieillesse_deplafonnee", "vieillesse_plafonnee"]:
        del commun.children[var]

    for var in ["apprentissage", "apprentissage_add", "apprentissage_alsace_moselle", "formprof_09", "formprof_1019", "formprof_20", "chomfg",
                "construction", "assedic"]:
        del pat.children['fonc'].children['contract'].children[var]

    pat.children['fonc'].children['etat'].children.update(commun.children)
    pat.children['fonc'].children['colloc'].children.update(commun.children)

    pat.children['etat_t'] = pat.children['fonc'].children['etat']
    pat.children['colloc_t'] = pat.children['fonc'].children['colloc']
    pat.children['contract'] = pat.children['fonc'].children['contract']

    for var in ['etat', 'colloc', 'contract']:
        del pat.children['fonc'].children[var]

    # Renaming
    pat.children['public_titulaire_etat'] = pat.children.pop('etat_t')
    # del pat.children['public_titulaire_etat'].children['rafp']

    pat.children['public_titulaire_territoriale'] = pat.children.pop('colloc_t')

    pat.children['public_titulaire_hospitaliere'] = copy.deepcopy(pat.children['public_titulaire_territoriale'])
    for category in ['territoriale', 'hospitaliere']:
        for name, bareme in pat.children['public_titulaire_' + category].children[category].children.items():
            pat.children['public_titulaire_{}'.format(category)].children[name] = bareme

    for category in ['territoriale', 'hospitaliere']:
        del pat.children['public_titulaire_territoriale'].children[category]
        del pat.children['public_titulaire_hospitaliere'].children[category]

    pat.children['public_non_titulaire'] = pat.children.pop('contract')

    # TO DO ONLY ONCE, BEFORE CHANGING
    #print(pat.children, file=open("openfisca_france/scripts/parameters/pat_children_AVANT_Sorted.txt", "w"))

    return pat


def build_sal(node_json):
    '''
    Construit le dictionnaire de barèmes des cotisations salariales
    à partir des informations contenues dans node_json.children['cotsoc'].children['sal']
    '''
    sal = copy.deepcopy(node_json.children['cotsoc'].children['sal'])
    sal.children['noncadre'].children.update(sal.children['commun'].children)
    sal.children['cadre'].children.update(sal.children['commun'].children)

    # Renaming
    sal.children['prive_non_cadre'] = sal.children.pop('noncadre')
    sal.children['prive_cadre'] = sal.children.pop('cadre')
    sal.children['public_titulaire_etat'] = sal.children['fonc'].children['etat']

    sal.children['public_titulaire_territoriale'] = sal.children['fonc'].children['colloc']
    sal.children['public_titulaire_hospitaliere'] = sal.children['fonc'].children['colloc']
    sal.children['public_non_titulaire'] = sal.children['fonc'].children['contract']

    for type_sal_category in [
            'public_titulaire_etat',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire',
            ]:
        sal.children[type_sal_category].children['excep_solidarite'] = sal.children['fonc'].children['commun'].children['solidarite']

    # Ajoute le RAFP (Régime additionnel de la fonction publique) pour 'public_titulaire_territoriale' et 'public_titulaire_hospitaliere'
    for type_sal_category in ['public_titulaire_territoriale', 'public_titulaire_hospitaliere']:
        sal.children[type_sal_category].children['rafp'] = sal.children['fonc'].children['etat'].children['rafp']

    sal.children['public_non_titulaire'].children.update(sal.children['commun'].children)
    del sal.children['public_non_titulaire'].children['assedic']

    # Cleaning
    del sal.children['commun']
    del sal.children['fonc'].children['etat']
    del sal.children['fonc'].children['colloc']
    del sal.children['fonc'].children['contract']

    # TO DO ONLY ONCE, BEFORE CHANGING V2
    # print(sal.children, file=open("openfisca_france/scripts/parameters/sal_children_AVANT.txt", "w"))

    return sal


def preprocess_parameters(parameters):
    '''
    Preprocess the legislation parameters to build the cotisations sociales taxscales (barèmes)
    '''
    pat = build_pat(parameters)
    sal = build_sal(parameters)

    cotsoc = parameters.children["cotsoc"]  # Ici on va chercher l'arbre réel

    cotsoc.children["cotisations_employeur"] = ParameterNode('cotisations_employeur_after_preprocessing', data = {})
    cotsoc.children["cotisations_salarie"] = ParameterNode('cotisations_salarie_after_preprocessing', data = {})

    for cotisation_name, baremes in (
            ('cotisations_employeur', pat.children),
            ('cotisations_salarie', sal.children),
            ):
        for category, bareme in baremes.items():
            if category in [member.name for member in TypesCategorieSalarie]:
                cotsoc.children[cotisation_name].children[category] = bareme

    # TO DO ONLY ONCE, BEFORE CHANGING V2
    print(cotsoc, file=open("openfisca_france/scripts/parameters/preprocessed_parameters_AVANT.txt", "w"))

    return parameters
