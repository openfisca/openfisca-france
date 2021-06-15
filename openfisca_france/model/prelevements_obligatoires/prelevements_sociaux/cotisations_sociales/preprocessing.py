import copy
import logging

from openfisca_core.parameters import ParameterNode
from openfisca_france.model.revenus.activite.salarie import TypesCategorieSalarie

DEBUG_SAL_TYPE = 'public_titulaire_etat'
log = logging.getLogger(__name__)

# TODO: contribution patronale de prévoyance complémentaire


def build_pat(node_json):  # Ici node_json c'est le dossier 'parameters'
    """Construit le dictionnaire de barèmes des cotisations employeur à partir des paramètres de parameters"""
    pat = ParameterNode("pat", data={})  # Génère pat
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
    commun.children['seuil'] = autres.construction.children['seuil']
    # Reste
    commun.children.update(chom.assedic.employeur.children)
    commun.children.update(chom.chomfg.children)
    commun.children.update(cotiz.csa.bareme.children)  # À harmoniser !
    commun.children.update(cotiz.famille.bareme.children)  # À harmoniser !
    commun.children.update(autres.fnal.children)  # À harmoniser !
    commun.children.update(autres.fin_syndic.children)  # À harmoniser !
    commun.children.update(cotiz.penibilite.bareme.children)  # À harmoniser !
    commun.children.update(cotiz.cnav.bareme.employeur.children)  # À harmoniser !
    commun.children.update(cotiz.mmid.bareme.employeur.children)  # À harmoniser ! + Créer params depuis IPP

    # Réindexation NonCadre
    # Initialisation
    noncadre = ParameterNode("noncadre", data={})
    pat.add_child('noncadre', noncadre)
    pat.children['noncadre'].children.update(retraites.employeur.noncadre.children)
    pat.children['noncadre'].children.update(commun.children)

    # Réindexation Cadre
    # Initialisation
    cadre = ParameterNode("cadre", data={})
    pat.add_child('cadre', cadre)
    pat.children['cadre'].children.update(retraites.employeur.cadre.children)
    pat.children['cadre'].children.update(commun.children)

    # Réindexation Fonc
    # Initialisation
    fonc = ParameterNode("fonc", data={})
    pat.add_child('fonc', fonc)
    fonc.add_child('colloc', ParameterNode("colloc", data={}))
    fonc.add_child('etat', ParameterNode("etat", data={}))
    fonc.add_child('contract', ParameterNode("contract", data={}))

    # Contractuel
    pat.children['fonc'].children['contract'] = public.ircantec.employeur
    pat.children['fonc'].children['contract'].children.update(commun.children)

    # Etat
    pat.children['fonc'].children['etat'].children.update(public.mmid.etat.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.ati.children)
    pat.children['fonc'].children['etat'].children.update(public.rafp.employeur.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.pension.employeur.children)

    # Collectivités Locales
    pat.children['fonc'].children['colloc'].children['hospitaliere'] = public.cnral.employeur.hospitaliere
    pat.children['fonc'].children['colloc'].children['territoriale'] = public.cnral.employeur.territoriale
    pat.children['fonc'].children['colloc'].children.update(public.cnral.employeur.children)
    pat.children['fonc'].children['colloc'].children.update(public.mmid.colloc.children)
    pat.children['fonc'].children['colloc'].children.update(public.rafp.employeur.children)

    # Renaming
    pat.children['prive_non_cadre'] = pat.children.pop('noncadre')
    pat.children['prive_cadre'] = pat.children.pop('cadre')
    print(pat.children['fonc'].children, file=open("openfisca_france/scripts/parameters/Fonc_APRES.txt", "w"))

    # Rework commun to deal with public employees
    for var in ["apprentissage", "apprentissage_add", "apprentissage_alsace_moselle", "assedic", "chomfg", "construction", "maladie", "formprof_09",
                "formprof_1019", "formprof_20", "vieillesse_deplafonnee", "vieillesse_plafonnee"]:
        del commun.children[var]
    print(commun.children, file=open("openfisca_france/scripts/parameters/Commun_APRES.txt", "w")) 

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

    print(pat.children['contract'].children, file=open("openfisca_france/scripts/parameters/Fonc_contract_APRES.txt", "w"))
    print(pat.children['etat_t'].children, file=open("openfisca_france/scripts/parameters/Fonc_etat_APRES.txt", "w"))
    print(pat.children['colloc_t'].children, file=open("openfisca_france/scripts/parameters/Fonc_colloc_APRES.txt", "w"))
    print(pat.children['fonc'].children, file=open("openfisca_france/scripts/parameters/Fonc_APRES.txt", "w"))

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

    print(pat.children['public_titulaire_hospitaliere'].children, file=open("openfisca_france/scripts/parameters/Public_host_APRES.txt", "w"))
    print(pat.children['public_titulaire_territoriale'].children, file=open("openfisca_france/scripts/parameters/Public_ter_APRES.txt", "w"))
    print(pat.children, file=open("openfisca_france/scripts/parameters/pat_children_APRES.txt", "w"))

    # TO DO ONLY ONCE, BEFORE CHANGING
    #print(pat.children, file=open("openfisca_france/scripts/parameters/pat_children_AVANT_Sorted.txt", "w"))
    return pat


def build_sal(node_json):
    '''
    Construit le dictionnaire de barèmes des cotisations salariales
    '''
    sal = ParameterNode("sal", data={})  # Génère sal
    commun = ParameterNode("commun", data={})  # Génère commun

    # Réindexation: nouveaux chemins
    retraites = node_json.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chom = node_json.prelevements_sociaux.cotisations_regime_assurance_chomage
    cotiz = node_json.prelevements_sociaux.cotisations_securite_sociale_regime_general
    public = node_json.prelevements_sociaux.cotisations_secteur_public
    indep = node_json.prelevements_sociaux.cotisations_taxes_independants_artisans_commercants
    liberal = node_json.prelevements_sociaux.cotisations_taxes_professions_liberales

    # Création de commun
    commun.children.update(chom.assedic.salarie.children)
    commun.children.update(cotiz.mmid.bareme.salarie.children)  # harmoniser !
    commun.children.update(cotiz.mmid_am.bareme.children)  # À harmoniser ! + Créer params depuis IPP
    commun.children.update(cotiz.cnav.bareme.salarie.children)  # À harmoniser !

    # Non Cadre
    # Initialisation
    noncadre = ParameterNode("noncadre", data={})
    sal.add_child('noncadre', noncadre)
    sal.children['noncadre'].children.update(retraites.salarie.noncadre.children)
    sal.children['noncadre'].children.update(commun.children)

    # Cadre
    cadre = ParameterNode("cadre", data={})
    sal.add_child('cadre', cadre)
    sal.children['cadre'].children.update(retraites.salarie.cadre.children)
    sal.children['cadre'].children.update(commun.children)

    # Renaming
    sal2.children['prive_non_cadre'] = sal2.children.pop('noncadre')
    sal2.children['prive_cadre'] = sal2.children.pop('cadre')
    sal2.children['public_titulaire_etat'] = sal2.children['fonc'].children['etat']

    sal2.children['public_titulaire_territoriale'] = sal2.children['fonc'].children['colloc']
    sal2.children['public_titulaire_hospitaliere'] = sal2.children['fonc'].children['colloc']
    sal2.children['public_non_titulaire'] = sal2.children['fonc'].children['contract']

    for type_sal_category in [
            'public_titulaire_etat',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire',
            ]:
        sal2.children[type_sal_category].children['excep_solidarite'] = sal2.children['fonc'].children['commun'].children['solidarite']

    # Ajoute le RAFP (Régime additionnel de la fonction publique) pour 'public_titulaire_territoriale' et 'public_titulaire_hospitaliere'
    for type_sal_category in ['public_titulaire_territoriale', 'public_titulaire_hospitaliere']:
        sal2.children[type_sal_category].children['rafp'] = sal2.children['fonc'].children['etat'].children['rafp']

    sal2.children['public_non_titulaire'].children.update(sal2.children['commun'].children)
    del sal2.children['public_non_titulaire'].children['assedic']

    # Cleaning
    del sal2.children['commun']
    del sal2.children['fonc'].children['etat']
    del sal2.children['fonc'].children['colloc']
    del sal2.children['fonc'].children['contract']


    ### REINDEXATION
    sal = ParameterNode("sal", data={}) # Génère sal
    commun = ParameterNode("commun", data={})  # Génère commun

    # Réindexation: nouveaux chemins
    #autres = node_json.prelevements_sociaux.autres_taxes_participations_assises_salaires
    retraites = node_json.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chom = node_json.prelevements_sociaux.cotisations_regime_assurance_chomage
    cotiz = node_json.prelevements_sociaux.cotisations_securite_sociale_regime_general
    #public = node_json.prelevements_sociaux.cotisations_secteur_public
    
    # Création de commun
    commun.children.update(chom.assedic.salarie.children)
    commun.children.update(cotiz.mmid.bareme.salarie.children)  # À harmoniser !
    commun.children.update(cotiz.mmid_am.bareme.children)  # À harmoniser ! + Créer params depuis IPP
    commun.children.update(cotiz.cnav.bareme.salarie.children)  # À harmoniser !
    print(commun.children, file=open("openfisca_france/scripts/parameters/SalNodes_APRES.txt", "w"))
    
    # Non Cadre
    # Initialisation
    noncadre = ParameterNode("noncadre", data={})
    sal.add_child('noncadre', noncadre)
    sal.children['noncadre'].children.update(retraites.salarie.noncadre.children)
    sal.children['noncadre'].children.update(commun.children)
    print(sal.children['noncadre'].children, file=open("openfisca_france/scripts/parameters/SalNoncadre_APRES.txt", "w"))
    # Cadre
    cadre = ParameterNode("cadre", data={})
    sal.add_child('cadre', cadre)
    sal.children['cadre'].children.update(retraites.salarie.cadre.children)
    sal.children['cadre'].children.update(commun.children)
    print(sal.children['cadre'].children, file=open("openfisca_france/scripts/parameters/SalCadre_APRES.txt", "w"))


    1/0
    # Renaming
    sal.children['prive_non_cadre'] = sal.children.pop('noncadre')
    sal.children['prive_cadre'] = sal.children.pop('cadre')

    # Réindexation Fonc
    # Initialisation
    fonc = ParameterNode("fonc", data={})
    sal.add_child('fonc', fonc)
    fonc.add_child('colloc', ParameterNode("colloc", data={}))
    fonc.add_child('etat', ParameterNode("etat", data={}))
    fonc.add_child('contract', ParameterNode("contract", data={}))
    fonc.add_child('commun', ParameterNode("commun", data={}))

    # Etat
    sal.children['fonc'].children['etat'].children.update(public.rafp.salarie.children)
    sal.children['fonc'].children['etat'].children.update(public.retraite.pension.salarie.children)
    sal.children['public_titulaire_etat'] = sal.children['fonc'].children['etat']

    # Collectivités Locales
    sal.children['fonc'].children['colloc'].children.update(public.cnral.salarie.children)
    sal.children['public_titulaire_territoriale'] = sal.children['fonc'].children['colloc']
    sal.children['public_titulaire_hospitaliere'] = sal.children['fonc'].children['colloc']

    # Contractuel
    sal.children['fonc'].children['contract'] = public.ircantec.salarie
    sal.children['public_non_titulaire'] = sal.children['fonc'].children['contract']

    # Commun
    sal.children['fonc'].children['commun'].children.update(public.fds.children)  # À harmoniser ! + Créer params depuis IPP

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
    sal.children['public_non_titulaire'].children.update(commun.children)
    del sal.children['public_non_titulaire'].children['assedic']

    # Cleaning
    del sal.children['fonc'].children['etat']
    del sal.children['fonc'].children['colloc']
    del sal.children['fonc'].children['contract']

    # Arti
    sal.add_child('arti', ParameterNode("arti", data={}))
    sal.children['arti'].children.update(indep.famille.arti.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['arti'].children.update(indep.formation.arti.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['arti'].children.update(indep.mmid.arti.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['arti'].children.update(indep.deces.arti.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['arti'].children.update(indep.retraite.arti.children)  # À harmoniser ! + Créer params depuis IPP

    # Comind
    sal.add_child('comind', ParameterNode("comind", data={}))
    sal.children['comind'].children.update(indep.famille.comind.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['comind'].children.update(indep.formation.comind.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['comind'].children.update(indep.mmid.comind.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['comind'].children.update(indep.deces.comind.children)  # À harmoniser ! + Créer params depuis IPP
    sal.children['comind'].children.update(indep.retraite.comind.children)  # À harmoniser ! + Créer params depuis IPP

    # Microsocial
    sal.add_child('microsocial', ParameterNode("microsocial", data={}))
    sal.children['microsocial'].children.update(liberal.auto_entrepreneur.children)  # À harmoniser ! + Créer params depuis IPP

    return sal


def preprocess_parameters(parameters):
    '''
    Preprocess the legislation parameters to build the cotisations sociales taxscales (barèmes)
    '''
    pat = build_pat(parameters)
    sal = build_sal(parameters)

    cotsoc = ParameterNode("cotsoc", data={})
    parameters.add_child('cotsoc', cotsoc)
    parameters.cotsoc.add_child('sal', sal)
    parameters.cotsoc.add_child('pat', pat)

    # ON GENERE LE DOSSIER COTSOC
    # Nouveaux chemins
    cotiz = parameters.prelevements_sociaux.cotisations_securite_sociale_regime_general
    autres = parameters.prelevements_sociaux.autres_taxes_participations_assises_salaires
    liberal = parameters.prelevements_sociaux.cotisations_taxes_professions_liberales
    travail = parameters.marche_travail
    pss = parameters.prelevements_sociaux.pss

    # Valeurs
    cotsoc.add_child('accident', ParameterNode("accident", data={}))
    cotsoc.accident.children.update(cotiz.accidents.bareme.children)  # À harmoniser! + Créer params depuis IPP
    cotsoc.add_child('assiette', ParameterNode("assiette", data={}))
    cotsoc.assiette.add_child('cantines_titres_restaurants', ParameterNode("cantines_titres_restaurants", data={}))
    cotsoc.assiette.cantines_titres_restaurants.children.update(cotiz.assiette.cantines_titres_restaurants.children)

    cotsoc.add_child('conge_individuel_formation', ParameterNode("conge_individuel_formation", data={}))
    cotsoc.conge_individuel_formation.children.update(autres.formation.conge_individuel_formation.children)  # À harmoniser

    cotsoc.add_child('contribution_supplementaire_apprentissage', ParameterNode("contribution_supplementaire_apprentissage", data={}))
    cotsoc.contribution_supplementaire_apprentissage.children.update(autres.apprentissage.contribution_supplementaire_apprentissage.children)  # À harmoniser

    cotsoc.add_child('gen', ParameterNode("gen", data={}))
    cotsoc.gen.children['plafond_securite_sociale'] = pss.children['plafond_securite_sociale']  # À harmoniser
    cotsoc.gen.children['plafond_securite_sociale_horaire'] = pss.children['plafond_securite_sociale_horaire']  # À harmoniser
    cotsoc.gen.children['nb_heure_travail_mensuel'] = travail.salaire_minimum.children['nb_heure_travail_mensuel']  # À harmoniser
    cotsoc.gen.children['smic_h_b'] = travail.salaire_minimum.children['smic_h_b']  # À harmoniser

    cotsoc.add_child('indemnite_fin_contrat', ParameterNode("indemnite_fin_contrat", data={}))
    cotsoc.indemnite_fin_contrat.children.update(cotiz.indemnite_fin_contrat.children)  # À harmoniser

    cotsoc.add_child('microsocial', ParameterNode("microsocial", data={}))
    cotsoc.microsocial.children.update(liberal.auto_entrepreneur.children)  # À harmoniser

    cotsoc.add_child('stage', ParameterNode("stage", data={}))
    cotsoc.stage.children['taux_gratification_min'] = travail.salaire_minimum.children['taux_gratification_min']  # À harmoniser + IPP

    cotsoc.add_child('taxes_sal', ParameterNode("taxes_sal", data={}))
    cotsoc.taxes_sal.children.update(autres.taxsal.bareme.children)  # À harmoniser

    cotsoc.add_child('versement_transport', ParameterNode("versement_transport", data={}))
    cotsoc.versement_transport.children.update(autres.versement_transport.bareme.children)  # À harmoniser

    cotsoc.children['hsup_exo'] = parameters.prelevements_sociaux.children['hsup_exo']  # À harmoniser
    cotsoc.children['tehr'] = autres.tehr.children['tehr']  # À harmoniser

    # Modifs
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
