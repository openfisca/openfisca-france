import copy
import logging

from openfisca_core.parameters import ParameterNode
from openfisca_france.model.base import *
from openfisca_france.model.revenus.activite.salarie import TypesCategorieSalarie

DEBUG_SAL_TYPE = 'public_titulaire_etat'
log = logging.getLogger(__name__)

# TODO: contribution patronale de prévoyance complémentaire


def build_pat(node_json):  # Ici node_json c'est le dossier 'parameters'
    """Construit le dictionnaire de barèmes des cotisations employeur à partir de RIEN"""
    pat = ParameterNode("pat", data={}) # Génère pat
    commun = ParameterNode("commun", data={})  # Génère commun

    # Réindexation: nouveaux chemins
    autres = node_json.prelevements_sociaux.autres_taxes_participations_assises_salaires
    retraites = node_json.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chom = node_json.prelevements_sociaux.cotisations_regime_assurance_chomage
    cotiz = node_json.prelevements_sociaux.cotisations_securite_sociale_regime_general
    public = node_json.prelevements_sociaux.cotisations_secteur_public

    # Création de commun
    # Apprentissage
    commun.children['apprentissage'] = autres.apprentissage.children['apprentissage']
    commun.children['apprentissage_add'] = autres.apprentissage.children['apprentissage_add']
    commun.children['apprentissage'] = autres.apprentissage.children['apprentissage']
    commun.children['apprentissage_alsace_moselle'] = autres.apprentissage.children['apprentissage_alsace_moselle']
    # Formation
    commun.children['formprof_09'] = autres.formation.children['formprof_09']
    commun.children['formprof_1019'] = autres.formation.children['formprof_1019']
    commun.children['formprof_20'] = autres.formation.children['formprof_20']
    # Construction
    commun.children['construction'] = autres.construction.children['construction_20']
    # Reste
    commun.children.update(chom.assedic.children)
    commun.children.update(chom.chomfg.children)
    commun.children.update(cotiz.csa.bareme.children)  # À harmoniser !
    commun.children.update(cotiz.famille.bareme.children)  # À harmoniser !
    commun.children.update(autres.fnal.children)  # À harmoniser !
    commun.children.update(autres.fin_syndic.children)  # À harmoniser !
    commun.children.update(cotiz.penibilite.bareme.children)  # À harmoniser !
    commun.children.update(cotiz.cnav.bareme.children)  # À harmoniser !
    commun.children.update(cotiz.mmid.bareme.children)  # À harmoniser ! + Créer params depuis IPP
    #print(commun.children, file=open("openfisca_france/scripts/parameters/Nodes_APRES.txt", "w"))

    # Réindexation NonCadre
    # Initialisation
    noncadre = ParameterNode("noncadre", data={})
    pat.add_child('noncadre', noncadre)
    pat.children['noncadre'].children.update(retraites.noncadre.children)
    pat.children['noncadre'].children.update(commun.children)
    #print(pat.children['noncadre'].children, file=open("openfisca_france/scripts/parameters/Noncadre_APRES.txt", "w"))

    # Réindexation Cadre
    # Initialisation
    cadre = ParameterNode("cadre", data={})
    pat.add_child('cadre', cadre)
    pat.children['cadre'].children.update(retraites.cadre.children)
    pat.children['cadre'].children.update(commun.children)
    # commun.children
    print(pat.children['cadre'].children, file=open("openfisca_france/scripts/parameters/Cadre_APRES.txt", "w"))
    # Réindexation Fonc ??
    # Initialisation
    fonc = ParameterNode("fonc", data={})
    pat.add_child('fonc', fonc)
    fonc.add_child('colloc', ParameterNode("colloc", data={}))
    fonc.add_child('etat', ParameterNode("etat", data={}))
    fonc.add_child('contract', ParameterNode("contract", data={}))

    # Contractuel
    pat.children['fonc'].children['contract'] = public.ircantec
    pat.children['fonc'].children['contract'].children.update(commun.children)
    #print(pat.children['fonc'].children['contract'].children, file=open("openfisca_france/scripts/parameters/Fonc_contract_APRES.txt", "w"))

    # Etat
    pat.children['fonc'].children['etat'].children.update(public.mmid.etat.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.ati.children)
    pat.children['fonc'].children['etat'].children.update(public.rafp.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.pension.children)
    #print(pat.children['fonc'].children['etat'].children, file=open("openfisca_france/scripts/parameters/Fonc_etat_APRES.txt", "w"))

    # Collectivités Locales
    pat.children['fonc'].children['colloc'].children['hospitaliere'] = public.cnral.hospitaliere
    pat.children['fonc'].children['colloc'].children['territoriale'] = public.cnral.territoriale
    pat.children['fonc'].children['colloc'].children.update(public.cnral.children)
    pat.children['fonc'].children['colloc'].children.update(public.mmid.colloc.children)
    pat.children['fonc'].children['colloc'].children.update(public.rafp.children)
    #print(pat.children['fonc'].children['colloc'].children, file=open("openfisca_france/scripts/parameters/Fonc_colloc_APRES.txt", "w"))

    # Renaming
    pat.children['prive_non_cadre'] = pat.children.pop('noncadre')
    pat.children['prive_cadre'] = pat.children.pop('cadre')
    #print(pat.children['fonc'].children, file=open("openfisca_france/scripts/parameters/Fonc_APRES.txt", "w"))

    # Rework commun to deal with public employees
    for var in ["apprentissage", "apprentissage_add", "apprentissage_alsace_moselle", "assedic", "chomfg", "construction", "maladie", "formprof_09",
                "formprof_1019", "formprof_20", "vieillesse_deplafonnee", "vieillesse_plafonnee"]:
        del commun.children[var]
    #print(commun.children, file=open("openfisca_france/scripts/parameters/Commun_APRES.txt", "w")) 

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

    #print(pat.children['contract'].children, file=open("openfisca_france/scripts/parameters/Fonc_contract_APRES.txt", "w"))
    #print(pat.children['etat_t'].children, file=open("openfisca_france/scripts/parameters/Fonc_etat_APRES.txt", "w"))
    #print(pat.children['colloc_t'].children, file=open("openfisca_france/scripts/parameters/Fonc_colloc_APRES.txt", "w"))
    #print(pat.children['fonc'].children, file=open("openfisca_france/scripts/parameters/Fonc_APRES.txt", "w"))

    # Renaming
    pat.children['public_titulaire_etat'] = pat.children.pop('etat_t')
    # del pat.children['public_titulaire_etat'].children['rafp'] # DEJA COMMENTÉ !!
    pat.children['public_titulaire_territoriale'] = pat.children.pop('colloc_t')
    pat.children['public_titulaire_hospitaliere'] = copy.deepcopy(pat.children['public_titulaire_territoriale'])
    for category in ['territoriale', 'hospitaliere']:
        for name, bareme in pat.children['public_titulaire_' + category].children[category].children.items():
            pat.children['public_titulaire_{}'.format(category)].children[name] = bareme

    for category in ['territoriale', 'hospitaliere']:
        del pat.children['public_titulaire_territoriale'].children[category]
        del pat.children['public_titulaire_hospitaliere'].children[category]

    pat.children['public_non_titulaire'] = pat.children.pop('contract')

    #print(pat.children['public_titulaire_hospitaliere'].children, file=open("openfisca_france/scripts/parameters/Public_host_APRES.txt", "w"))
    #print(pat.children['public_titulaire_territoriale'].children, file=open("openfisca_france/scripts/parameters/Public_ter_APRES.txt", "w"))
    #print(pat.children, file=open("openfisca_france/scripts/parameters/pat_children_APRES.txt", "w"))

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
