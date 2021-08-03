import copy
import logging

from openfisca_france.model.base import *
from openfisca_france.model.revenus.activite.salarie import TypesCategorieSalarie

DEBUG_SAL_TYPE = 'public_titulaire_etat'
log = logging.getLogger(__name__)

# TODO: contribution patronale de prévoyance complémentaire


def build_pat(node_json):  # Ici node_json c'est le dossier 'parameters'
    """Construit le dictionnaire de barèmes des cotisations employeur à partir des paramètres de parameters"""
    pat = ParameterNode("pat", data={})  # Génère pat
    commun = ParameterNode("commun", data={})  # Génère commun

    # Réindexation : nouveaux chemins suite à l'harmonisation avec les répertoires des barèmes IPP
    autres = node_json.prelevements_sociaux.autres_taxes_participations_assises_salaires
    retraites = node_json.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chomage = node_json.prelevements_sociaux.cotisations_regime_assurance_chomage
    regime_general = node_json.prelevements_sociaux.cotisations_securite_sociale_regime_general
    public = node_json.prelevements_sociaux.cotisations_secteur_public

    # Création de commun
    # Apprentissage
    commun.children['apprentissage'] = autres.apprentissage.children['apprentissage']
    commun.children['apprentissage_add'] = autres.apprentissage.children['apprentissage_add']
    commun.children['apprentissage_alsace_moselle'] = autres.apprentissage.children['apprentissage_alsace_moselle']
    # Formation
    commun.children['formprof_09'] = autres.formation.children['formprof_09']
    commun.children['formprof_1019'] = autres.formation.children['formprof_1019']
    commun.children['formprof_20'] = autres.formation.children['formprof_20']
    # Construction
    commun.children['construction'] = autres.construction.children['construction_20']
    # Autres thématiques
    commun.children.update(chomage.assedic.employeur.children)
    commun.children.update(chomage.chomfg.children)
    commun.children.update(regime_general.csa.bareme.children)  # À harmoniser !
    commun.children.update(regime_general.famille.bareme.children)  # À harmoniser !
    commun.children.update(regime_general.penibilite.bareme.children)  # À harmoniser !
    commun.children.update(regime_general.cnav.bareme.employeur.children)  # À harmoniser !
    commun.children.update(regime_general.mmid.bareme.employeur.children)  # À harmoniser ! + Créer params depuis IPP
    commun.children.update(autres.fnal.children)  # À harmoniser !
    commun.children.update(autres.fin_syndic.children)  # À harmoniser !
    commun.children.update(retraites.ceg.employeur.children)
    commun.children.update(retraites.cet2019.employeur.children)
    commun.children.update(retraites.agirc_arrco.employeur.children)

    # Réindexation NonCadre
    # Initialisation
    noncadre = ParameterNode("noncadre", data={})
    pat.add_child('noncadre', noncadre)
    pat.children['noncadre'].children.update(retraites.agff.employeur.noncadre.children)
    pat.children['noncadre'].children.update(retraites.arrco.employeur.noncadre.children)
    pat.children['noncadre'].children.update(commun.children)

    # Réindexation Cadre
    # Initialisation
    cadre = ParameterNode("cadre", data={})
    pat.add_child('cadre', cadre)
    pat.children['cadre'].children.update(retraites.agff.employeur.cadre.children)
    pat.children['cadre'].children.update(retraites.arrco.employeur.cadre.children)
    pat.children['cadre'].children.update(retraites.agirc.employeur.children)
    pat.children['cadre'].children.update(retraites.apec.employeur.children)
    pat.children['cadre'].children.update(retraites.cet.employeur.children)
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
    pat.children['fonc'].children['etat'].children.update(public.rafp.employeur.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.ati.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.pension.employeur.children)

    # Collectivités Locales
    pat.children['fonc'].children['colloc'].children['hospitaliere'] = public.cnracl.employeur.hospitaliere
    pat.children['fonc'].children['colloc'].children['territoriale'] = public.cnracl.employeur.territoriale
    pat.children['fonc'].children['colloc'].children.update(public.cnracl.employeur.children)
    pat.children['fonc'].children['colloc'].children.update(public.mmid.colloc.children)
    pat.children['fonc'].children['colloc'].children.update(public.rafp.employeur.children)

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

    pat.children['etat_t'] = pat.children['fonc'].children['etat']  # Il semble que ce soient des sauvegardes temporaires ?
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
    return pat


def build_sal(node_json):
    '''
    Construit le dictionnaire de barèmes des cotisations salariales
    '''
    sal = ParameterNode("sal", data={})  # Génère sal
    commun = ParameterNode("commun", data={})  # Génère commun

    # Réindexation: nouveaux chemins
    retraites = node_json.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chomage = node_json.prelevements_sociaux.cotisations_regime_assurance_chomage
    regime_general = node_json.prelevements_sociaux.cotisations_securite_sociale_regime_general
    public = node_json.prelevements_sociaux.cotisations_secteur_public
    indep = node_json.prelevements_sociaux.cotisations_taxes_independants_artisans_commercants
    liberal = node_json.prelevements_sociaux.cotisations_taxes_professions_liberales

    # Création de commun
    commun.children.update(chomage.assedic.salarie.children)
    commun.children.update(regime_general.mmid.bareme.salarie.children)  # harmoniser !
    commun.children.update(regime_general.mmid_am.bareme.children)  # À harmoniser ! + Créer params depuis IPP
    commun.children.update(regime_general.cnav.bareme.salarie.children)  # À harmoniser !
    commun.children.update(retraites.ceg.salarie.children)
    commun.children.update(retraites.cet2019.salarie.children)
    commun.children.update(retraites.agirc_arrco.salarie.children)

    # Non Cadre
    # Initialisation
    noncadre = ParameterNode("noncadre", data={})
    sal.add_child('noncadre', noncadre)
    sal.children['noncadre'].children.update(retraites.agff.salarie.noncadre.children)
    sal.children['noncadre'].children.update(retraites.arrco.salarie.noncadre.children)
    sal.children['noncadre'].children.update(commun.children)

    # Cadre
    cadre = ParameterNode("cadre", data={})
    sal.add_child('cadre', cadre)
    sal.children['cadre'].children.update(retraites.agff.salarie.cadre.children)
    sal.children['cadre'].children.update(retraites.arrco.salarie.cadre.children)
    sal.children['cadre'].children.update(retraites.agirc.salarie.children)
    sal.children['cadre'].children.update(retraites.apec.salarie.children)
    sal.children['cadre'].children.update(retraites.cet.salarie.children)
    sal.children['cadre'].children.update(commun.children)

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
    sal.children['fonc'].children['colloc'].children.update(public.cnracl.salarie.children)
    sal.children['public_titulaire_territoriale'] = sal.children['fonc'].children['colloc']
    sal.children['public_titulaire_hospitaliere'] = sal.children['fonc'].children['colloc']

    # Contractuel
    sal.children['fonc'].children['contract'] = public.ircantec.salarie
    sal.children['public_non_titulaire'] = sal.children['fonc'].children['contract']

    # Commun
    sal.children['fonc'].children['commun'].children.update(public.fds.salarie.children)  # À harmoniser ! + Créer params depuis IPP

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
    cotsoc.add_child('pat', pat)
    cotsoc.add_child('sal', sal)

    # Ajout de paramètres
    # Nouveaux chemins
    regime_general = parameters.prelevements_sociaux.cotisations_securite_sociale_regime_general
    autres = parameters.prelevements_sociaux.autres_taxes_participations_assises_salaires
    liberal = parameters.prelevements_sociaux.cotisations_taxes_professions_liberales
    travail = parameters.marche_travail
    pss = parameters.prelevements_sociaux.pss

    # Valeurs
    cotsoc.add_child('accident', ParameterNode("accident", data={}))
    cotsoc.accident.children.update(regime_general.accidents.bareme.children)  # À harmoniser! + Créer params depuis IPP
    cotsoc.add_child('assiette', ParameterNode("assiette", data={}))
    cotsoc.assiette.add_child('cantines_titres_restaurants', ParameterNode("cantines_titres_restaurants", data={}))
    cotsoc.assiette.cantines_titres_restaurants.children.update(regime_general.assiette.cantines_titres_restaurants.children)

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
    cotsoc.indemnite_fin_contrat.children.update(regime_general.indemnite_fin_contrat.children)  # À harmoniser

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
    return parameters
