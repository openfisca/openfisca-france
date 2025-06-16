import copy
import logging

from openfisca_france.model.base import *
from openfisca_france.model.revenus.activite.salarie import TypesCategorieSalarie


log = logging.getLogger(__name__)


def build_pat(parameters):
    '''Construit le dictionnaire de barèmes des cotisations employeur à partir des paramètres de parameters.'''
    # TODO: contribution patronale de prévoyance complémentaire
    pat = ParameterNode('pat', data=dict(description='Cotisations sociales employeur'))  # Génère pat
    commun = ParameterNode('commun', data=dict(
        description='Cotisations sociales employeur communes à plusieurs régimes',
        metadata=dict(order=[]),
        ))  # Génère commun

    # Réindexation : nouveaux chemins suite à l'harmonisation avec les répertoires des barèmes IPP
    autres = parameters.prelevements_sociaux.autres_taxes_participations_assises_salaires
    retraites = parameters.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chomage = parameters.prelevements_sociaux.cotisations_regime_assurance_chomage
    regime_general = parameters.prelevements_sociaux.cotisations_securite_sociale_regime_general
    public = parameters.prelevements_sociaux.cotisations_secteur_public

    # Création de commun
    # Apprentissage (avec effacement)
    commun.children.update(autres.apprentissage.children)
    if autres.apprentissage.metadata is not None and autres.apprentissage.metadata.get('order') is not None:
        commun.metadata['order'] += autres.apprentissage.metadata['order']

    del commun.children['csa']  # n'est pas un barème et est utilisé directement
    del commun.children['cotisation_supplementaire']

    # Formation
    commun.children.update(autres.formation.employeur_tout_salaire.children)
    if autres.formation.employeur_tout_salaire.metadata is not None and autres.formation.employeur_tout_salaire.metadata.get('order') is not None:
        commun.metadata['order'] += autres.formation.employeur_tout_salaire.metadata['order']

    # Construction (avec renommage et effacement)
    commun.children.update(autres.construction.children)
    commun.children['construction_plus_de_10_salaries'] = commun.children.pop('10_19_salaries')
    commun.children['construction_plus_de_20_salaries'] = commun.children.pop('plus_20_salaries')
    commun.children['construction_plus_de_50_salaries'] = commun.children.pop('plus_50_salaries')
    del commun.children['seuil']
    commun.metadata['order'] += [
        'construction_plus_de_10_salaries',
        'construction_plus_de_20_salaries',
        'construction_plus_de_50_salaries',
        ]
    # Autres thématiques
    thematiques = [
        chomage.ags.employeur,
        chomage.asf.employeur,
        chomage.chomage.employeur,
        regime_general.csa.employeur,
        regime_general.famille.employeur,
        regime_general.penibilite,
        regime_general.cnav.employeur,
        regime_general.mmid.employeur,
        ]
    for thematique in thematiques:
        if thematique.metadata is not None and thematique.metadata.get('order') is not None:
            commun.metadata['order'] += thematique.metadata['order']
        commun.children.update(thematique.children)

    # Fnal (avec renommage)
    commun.children.update(autres.fnal.children)
    fnal_keys = [
        'contribution_plus_de_10_salaries',
        'contribution_moins_de_20_salaries',
        'contribution_plus_de_20_salaries',
        'contribution_moins_de_50_salaries',
        'contribution_plus_de_50_salaries',
        'cotisation',
        ]
    for key in fnal_keys:
        commun.children[f'fnal_{key}'] = commun.children.pop(key)
    commun.metadata['order'] += [f'fnal_{key}' for key in fnal_keys]

    commun.children.update(autres.fin_syndic.children)  # À harmoniser !
    if autres.fin_syndic.metadata is not None and autres.fin_syndic.metadata.get('order') is not None:
        commun.metadata['order'] += autres.fin_syndic.metadata['order']

    # Enlève de commun.metadata['order'] les paramètres qui ne font pas partie de commun.
    for id in commun.metadata['order'].copy():
        if id not in commun.children.keys():
            commun.metadata['order'].remove(id)

    # Réindexation Non Cadre
    # Initialisation
    noncadre = ParameterNode('noncadre', data=dict(
        description='Cotisations employeur pour salarié non cadre',
        metadata=dict(order=[]),
        ))
    pat.add_child('noncadre', noncadre)
    pat.children['noncadre'].children.update(retraites.agff.employeur.noncadre.children)
    pat.children['noncadre'].children.update(retraites.arrco.taux_effectifs_salaries_employeurs.employeur.noncadre.children)
    pat.children['noncadre'].children.update(retraites.ceg.employeur.children)
    pat.children['noncadre'].children.update(retraites.cet2019.employeur.children)
    pat.children['noncadre'].children.update(retraites.agirc_arrco.employeur.children)
    pat.children['noncadre'].children.update(commun.children)
    pat.children['noncadre'].metadata['order'] += commun.metadata['order']

    # Réindexation Cadre
    # Initialisation
    cadre = ParameterNode('cadre', data=dict(
        description='Cotisations employeur pour salarié cadre',
        metadata=dict(order=[]),
        ))
    pat.add_child('cadre', cadre)
    pat.children['cadre'].children.update(retraites.agff.employeur.cadre.children)
    pat.children['cadre'].children.update(retraites.arrco.taux_effectifs_salaries_employeurs.employeur.cadre.children)
    pat.children['cadre'].children.update(retraites.agirc.taux_effectifs_salaries_employeurs.avant81.employeur.children)
    pat.children['cadre'].children.update(retraites.apec.employeur.children)
    pat.children['cadre'].children.update(retraites.ceg.employeur.children)
    pat.children['cadre'].children.update(retraites.cet2019.employeur.children)
    pat.children['cadre'].children.update(retraites.agirc_arrco.employeur.children)
    del pat.children['cadre'].children['forfait_annuel']
    pat.children['cadre'].children.update(retraites.cet.employeur.children)
    pat.children['cadre'].children.update(commun.children)
    pat.children['cadre'].metadata['order'] += commun.metadata['order']

    # Réindexation Fonc
    # Initialisation
    fonc = ParameterNode('fonc', data=dict(description='Cotisations sociales employeur du secteur public'))
    pat.add_child('fonc', fonc)
    fonc.add_child('colloc', ParameterNode('colloc', data=dict(
        description='Cotisations sociales employeur du secteur public pour les collectivités locales',
        metadata=dict(order=[]),
        )))
    fonc.add_child('etat', ParameterNode('etat', data=dict(
        description="Cotisations sociales employeur du secteur public pour les fonctions d'Etat",
        metadata=dict(order=[]),
        )))
    fonc.add_child('militaire', ParameterNode('militaire', data=dict(
        description='Cotisations sociales employeur du secteur public pour les militaires',
        metadata=dict(order=[]),
        )))
    fonc.add_child('contract', ParameterNode('contract', data=dict(
        description='Cotisations sociales employeur du secteur public pour les agents contractuels',
        metadata=dict(order=[]),
        )))

    # Contractuel
    pat.children['fonc'].children['contract'] = public.ircantec.taux_cotisations_appeles.employeur
    pat.children['fonc'].children['contract'].children.update(commun.children)
    pat.children['fonc'].children['contract'].metadata['order'] += commun.metadata['order']

    # Etat
    pat.children['fonc'].children['etat'].children.update(public.mmid.etat.tout_traitement.employeur.children)
    # pat.children['fonc'].children['etat'].children.update(public.mmid.etat.sous_plafond.employeur.children)
    pat.children['fonc'].children['etat'].children.update(public.rafp.employeur.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.ati.children)
    pat.children['fonc'].children['etat'].children.update(public.retraite.pension.employeur.civils.children)

    # Militaires
    pat.children['fonc'].children['militaire'].children.update(public.mmid.etat.tout_traitement.employeur.children)
    # pat.children['fonc'].children['militaire'].children.update(public.mmid.etat.sous_plafond.employeur.children)
    pat.children['fonc'].children['militaire'].children.update(public.rafp.employeur.children)
    pat.children['fonc'].children['militaire'].children.update(public.retraite.pension.employeur.militaires.children)

    # Collectivités Locales
    pat.children['fonc'].children['colloc'].children['hospitaliere'] = public.cnracl.employeur.hospitaliere
    pat.children['fonc'].children['colloc'].children['territoriale'] = public.cnracl.employeur.territoriale
    pat.children['fonc'].children['colloc'].children.update(public.cnracl.employeur.children)
    pat.children['fonc'].children['colloc'].children.update(public.mmid.colloc.tout_traitement.employeur.children)
    # pat.children['fonc'].children['colloc'].children.update(public.mmid.colloc.sous_plafond.employeur.children)
    pat.children['fonc'].children['colloc'].children.update(public.rafp.employeur.children)

    # Renaming
    pat.children['prive_non_cadre'] = pat.children.pop('noncadre')
    pat.children['prive_cadre'] = pat.children.pop('cadre')

    # Rework commun to deal with public employees
    for var in ['apprentissage_taxe', 'apprentissage_contribution_additionnelle', 'apprentissage_taxe_alsace_moselle', 'chomage', 'asf', 'ags',
                'construction_plus_de_10_salaries', 'construction_plus_de_20_salaries', 'construction_plus_de_50_salaries', 'maladie',
                'formprof_moins_de_10_salaries', 'formprof_moins_de_11_salaries', 'formprof_20_salaries_et_plus', 'formprof_11_salaries_et_plus', 'formprof_entre_10_et_19_salaries',
                'vieillesse_deplafonnee', 'vieillesse_plafonnee']:
        del commun.children[var]
        if var in commun.metadata['order']:
            commun.metadata['order'].remove(var)

    for var in ['apprentissage_taxe', 'apprentissage_contribution_additionnelle', 'apprentissage_taxe_alsace_moselle',
                'formprof_moins_de_10_salaries', 'formprof_moins_de_11_salaries', 'formprof_20_salaries_et_plus', 'formprof_11_salaries_et_plus', 'formprof_entre_10_et_19_salaries',
                'ags', 'construction_plus_de_10_salaries', 'construction_plus_de_20_salaries', 'construction_plus_de_50_salaries', 'chomage', 'asf']:
        del pat.children['fonc'].children['contract'].children[var]
        if var in pat.children['fonc'].children['contract'].metadata['order']:
            pat.children['fonc'].children['contract'].metadata['order'].remove(var)

    pat.children['fonc'].children['etat'].children.update(commun.children)
    pat.children['fonc'].children['etat'].metadata['order'] += commun.metadata['order']
    pat.children['fonc'].children['colloc'].children.update(commun.children)
    pat.children['fonc'].children['colloc'].metadata['order'] += commun.metadata['order']
    pat.children['fonc'].children['militaire'].children.update(commun.children)
    pat.children['fonc'].children['militaire'].metadata['order'] += commun.metadata['order']

    pat.children['etat_t'] = pat.children['fonc'].children['etat']  # Il semble que ce soient des sauvegardes temporaires ?
    pat.children['colloc_t'] = pat.children['fonc'].children['colloc']
    pat.children['contract'] = pat.children['fonc'].children['contract']
    pat.children['militaire_t'] = pat.children['fonc'].children['militaire']

    for var in ['etat', 'colloc', 'contract', 'militaire']:
        del pat.children['fonc'].children[var]

    # Renaming
    pat.children['public_titulaire_etat'] = pat.children.pop('etat_t')
    pat.children['public_titulaire_militaire'] = pat.children.pop('militaire_t')
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


def build_sal(parameters):
    '''
    Construit le dictionnaire de barèmes des cotisations salariales
    '''
    sal = ParameterNode('sal', data=dict(description='Cotisations sociales salariales'))  # Génère sal
    commun = ParameterNode('commun', data=dict(
        description='Cotisations sociales salariales communes à plusieurs régimes',
        metadata=dict(order=[]),
        ))  # Génère commun

    # Réindexation: nouveaux chemins
    retraites = parameters.prelevements_sociaux.regimes_complementaires_retraite_secteur_prive
    chomage = parameters.prelevements_sociaux.cotisations_regime_assurance_chomage
    regime_general = parameters.prelevements_sociaux.cotisations_securite_sociale_regime_general
    public = parameters.prelevements_sociaux.cotisations_secteur_public
    indep = parameters.prelevements_sociaux.cotisations_taxes_independants_artisans_commercants
    liberal = parameters.prelevements_sociaux.professions_liberales

    # Création de commun
    commun.children.update(chomage.chomage.salarie.children)
    if chomage.chomage.salarie.metadata is not None and chomage.chomage.salarie.metadata.get('order') is not None:
        commun.metadata['order'] += chomage.chomage.salarie.metadata['order']

    commun.children.update(chomage.asf.salarie.children)
    if chomage.asf.salarie.metadata is not None and chomage.asf.salarie.metadata.get('order') is not None:
        commun.metadata['order'] += chomage.asf.salarie.metadata['order']

    commun.children.update(regime_general.mmid.salarie.children)
    del commun.children['reduction_plus_65_ans']
    if regime_general.mmid.salarie.metadata is not None and regime_general.mmid.salarie.metadata.get('order') is not None:
        commun.metadata['order'] += regime_general.mmid.salarie.metadata['order']

    commun.children.update(regime_general.mmid_am.children)
    del commun.children['allocations_chomage_et_preretraite']
    del commun.children['avantages_vieillesse']
    if regime_general.mmid_am.metadata is not None and regime_general.mmid_am.metadata.get('order') is not None:
        commun.metadata['order'] += regime_general.mmid_am.metadata['order']

    commun.children.update(regime_general.cnav.salarie.children)
    if regime_general.cnav.salarie.metadata is not None and regime_general.cnav.salarie.metadata.get('order') is not None:
        commun.metadata['order'] += regime_general.cnav.salarie.metadata['order']

    # Enlève de commun.metadata['order'] les paramètres qui ne font pas partie de commun.
    for id in commun.metadata['order'].copy():
        if id not in commun.children.keys():
            commun.metadata['order'].remove(id)

    # Non Cadre
    # Initialisation
    noncadre = ParameterNode('noncadre', data=dict(
        description='Cotisations salariales pour salarié non cadre',
        metadata=dict(order=[]),
        ))
    sal.add_child('noncadre', noncadre)
    sal.children['noncadre'].children.update(retraites.agff.salarie.noncadre.children)
    sal.children['noncadre'].children.update(retraites.arrco.taux_effectifs_salaries_employeurs.salarie.noncadre.children)
    sal.children['noncadre'].children.update(retraites.ceg.salarie.children)
    sal.children['noncadre'].children.update(retraites.cet2019.salarie.children)
    sal.children['noncadre'].children.update(retraites.agirc_arrco.salarie.children)
    sal.children['noncadre'].children.update(commun.children)
    sal.children['noncadre'].metadata['order'] += commun.metadata['order']

    # Cadre
    cadre = ParameterNode('cadre', data=dict(
        description='Cotisations salariales pour salarié cadre',
        metadata=dict(order=[]),
        ))
    sal.add_child('cadre', cadre)
    sal.children['cadre'].children.update(retraites.agff.salarie.cadre.children)
    sal.children['cadre'].children.update(retraites.arrco.taux_effectifs_salaries_employeurs.salarie.cadre.children)
    sal.children['cadre'].children.update(retraites.agirc.taux_effectifs_salaries_employeurs.avant81.salarie.children)
    sal.children['cadre'].children.update(retraites.apec.salarie.children)
    sal.children['cadre'].children.update(retraites.ceg.salarie.children)
    sal.children['cadre'].children.update(retraites.cet2019.salarie.children)
    sal.children['cadre'].children.update(retraites.agirc_arrco.salarie.children)
    del sal.children['cadre'].children['forfait_annuel']

    sal.children['cadre'].children.update(retraites.cet.salarie.children)
    sal.children['cadre'].children.update(commun.children)
    sal.children['cadre'].metadata['order'] += commun.metadata['order']

    # Renaming
    sal.children['prive_non_cadre'] = sal.children.pop('noncadre')
    sal.children['prive_cadre'] = sal.children.pop('cadre')

    # Réindexation Fonc
    # Initialisation
    fonc = ParameterNode('fonc', data=dict(description='Cotisations salariales du secter public'))
    sal.add_child('fonc', fonc)
    fonc.add_child('colloc', ParameterNode('colloc', data=dict(
        description='Cotisations sociales salariales du secteur public pour les collectivités locales',
        metadata=dict(order=[]),
        )))
    fonc.add_child('etat', ParameterNode('etat', data=dict(
        description="Cotisations sociales salariales du secteur public pour les fonctions d'Etat",
        metadata=dict(order=[]),
        )))
    fonc.add_child('contract', ParameterNode('contract', data=dict(
        description='Cotisations sociales salariales du secteur public pour les agents contractuels',
        metadata=dict(order=[]),
        )))
    fonc.add_child('commun', ParameterNode('commun', data=dict(
        description='Cotisations sociales salariales communes à plusieurs régimes',
        metadata=dict(order=[]),
        )))

    # Etat
    sal.children['fonc'].children['etat'].children.update(public.rafp.salarie.children)
    sal.children['fonc'].children['etat'].children.update(public.retraite.pension.salarie.children)
    # sal.children['fonc'].children['colloc'].children.update(public.mmid.etat.tout_traitement.salarie.children)
    # sal.children['fonc'].children['colloc'].children.update(public.mmid.etat.sous_plafond.salarie.children)
    sal.children['public_titulaire_etat'] = sal.children['fonc'].children['etat']

    # Collectivités Locales
    sal.children['fonc'].children['colloc'].children.update(public.cnracl.salarie.children)
    # sal.children['fonc'].children['colloc'].children.update(public.mmid.colloc.tout_traitement.salarie.children)
    # sal.children['fonc'].children['colloc'].children.update(public.mmid.colloc.sous_plafond.salarie.children)
    sal.children['public_titulaire_territoriale'] = sal.children['fonc'].children['colloc']
    sal.children['public_titulaire_hospitaliere'] = sal.children['fonc'].children['colloc']

    # Contractuel
    sal.children['fonc'].children['contract'] = public.ircantec.taux_cotisations_appeles.salarie
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
    sal.children['public_non_titulaire'].metadata['order'] += commun.metadata['order']
    for var in ['chomage', 'asf']:
        del sal.children['public_non_titulaire'].children[var]
        if sal.children['public_non_titulaire'].metadata['order']:
            sal.children['public_non_titulaire'].metadata['order'].remove(var)

    # Cleaning
    del sal.children['fonc'].children['etat']
    del sal.children['fonc'].children['colloc']
    del sal.children['fonc'].children['contract']

    # Arti
    sal.add_child('arti', ParameterNode('arti', data=dict(description='Cotisations sociales salariales des artisans')))
    sal.children['arti'].children.update(indep.famille.arti.children)
    sal.children['arti'].children.update(indep.mmid.arti.children)
    # Comind
    sal.add_child('comind', ParameterNode('comind', data=dict(description='Cotisations sociales salariales des commercants et indépendants')))
    sal.children['comind'].children.update(indep.famille.comind.children)
    sal.children['comind'].children.update(indep.mmid.comind.children)
    # Microsocial
    sal.add_child('microsocial', ParameterNode('microsocial', data=dict(description='Cotisations sociales salariales des professions libérales')))
    sal.children['microsocial'].children.update(liberal.auto_entrepreneur.children)  # À harmoniser ! + Créer params depuis IPP

    return sal


def preprocess_parameters(parameters):
    '''
    Preprocess the legislation parameters to build the cotisations sociales taxscales (barèmes)
    '''
    pat = build_pat(parameters)
    sal = build_sal(parameters)

    cotsoc = ParameterNode('cotsoc', data=dict(description='Cotisations sociales'))
    parameters.add_child('cotsoc', cotsoc)
    cotsoc.add_child('pat', pat)
    cotsoc.add_child('sal', sal)

    # Modifs
    cotsoc.add_child('cotisations_employeur', ParameterNode('cotisations_employeur_after_preprocessing', data=dict(description='Cotisations sociales employeur')))
    cotsoc.add_child('cotisations_salarie', ParameterNode('cotisations_salarie_after_preprocessing', data=dict(description='Cotisations sociales salariales')))

    for cotisation_name, baremes in (
            ('cotisations_employeur', pat.children),
            ('cotisations_salarie', sal.children),
            ):
        for category, bareme in baremes.items():
            if category in [member.name for member in TypesCategorieSalarie]:
                cotsoc.children[cotisation_name].children[category] = bareme

    return parameters
