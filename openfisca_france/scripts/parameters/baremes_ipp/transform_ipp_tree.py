# -*- coding: utf-8 -*-

"""
Ce fichier contient une fonction `transform_ipp_tree` appelée (indirectement) par le script
`convert_ipp_xlsx_to_openfisca_xml.py`.

Cette fonction renomme des paramètres provenant des barèmes IPP pour insertion dans l'arbre des paramètres OpenFisca.
Le script de merge éclate cet arbre cible en plusieurs fichiers XML écrits dans le répertoire `parameters`.
"""

import collections


def fixed_bases_tax_scale(base_by_slice_name, rates_tree, null_rate_base = None):
    """
    Crée un barème qui sera transformé en un élément XML <BAREME> par le script de fusion.

    Cette fonction sert essentiellement pour les barèmes des cotisations sociales
    dont les seuils s'expriment en unité du plafond de la sécurité sociale.

    Voir la fonction `tax_scale` pour une version plus simple.
    """
    first_start = UnboundLocalError
    for bracket in rates_tree.itervalues():
        if isinstance(bracket, (float, int)):
            continue
        bracket_start = bracket[0]['start']
        if first_start is UnboundLocalError or bracket_start < first_start:
            first_start = bracket_start
    assert first_start is not UnboundLocalError

    # Convert constant brackets to real brackets.
    for slice_name, bracket in rates_tree.items():
        if isinstance(bracket, (float, int)):
            rates_bracket_item = dict(
                start = first_start,
                value = str(bracket),
                )
            rates_tree[slice_name] = [rates_bracket_item]

    if null_rate_base is not None:
        # Add null slice and add missing zero values in other slices.
        for bracket in rates_tree.itervalues():
            if first_start < bracket[0]['start']:
                bracket.insert(0, dict(
                    start = first_start,
                    value = '0',
                    ))
            for item in bracket:
                if item['value'] is None:
                    item['value'] = '0'

        rates_bracket_null_item = dict(
            start = first_start,
            value = '0',
            )
        rates_tree['tranche_nulle'] = [rates_bracket_null_item]

        base_by_slice_name = base_by_slice_name.copy()
        base_by_slice_name['tranche_nulle'] = null_rate_base

    # Generate bases_tree.
    bases_tree = collections.OrderedDict()
    for slice_name, rates_bracket in sorted(rates_tree.items()):
        bases_bracket_item = dict(
            start = rates_bracket[0]['start'],
            value = str(base_by_slice_name[slice_name]),
            )
        bases_tree[slice_name] = [bases_bracket_item]

    return tax_scale(bases_tree, rates_tree)


def tax_scale(bases_tree, rates_tree):
    """Crée un barème qui sera transformé en un élément XML <BAREME> par le script de fusion."""
    return dict(
        TYPE = 'BAREME',
        SEUIL = bases_tree,
        TAUX = rates_tree,
        )


def transform_ipp_tree(root):
    """
    root est la racine de l'arbre construit depuis les fichiers XLSX de l'IPP.
    """
    del root['baremes_ipp_tarification_energie_logement']
    del root['baremes_ipp_chomage_unemployment']
    # root['chomage'] = root.pop('baremes_ipp_chomage_unemployment')

    root['impot_revenu'] = impot_revenu = root.pop('baremes_ipp_impot_revenu_income_tax')
    #
    impot_revenu['tspr'] = tspr = impot_revenu.pop('deductions')
    tspr['abatsalpen'] = abatsalpen = tspr.pop('deduction_supplementaire')
    abatsalpen['max'] = abatsalpen.pop('abattement_maximal')
    # TODO: gérer plaf_ab_dedsal
    tspr['abatpen'] = abatpen = {}
    tspr['abatpro'] = abatpro = tspr.pop(
        'abattement_forfaitaire_pour_frais_professionnels_sur_les_salaires_et_pensions')
    maximum_de_l_abattement_pour_frais_professionnels = tspr.pop('maximum_de_l_abattement_pour_frais_professionnels')
    abatpen['max'] = maximum_de_l_abattement_pour_frais_professionnels.pop('pensions')
    abatpro['max'] = maximum_de_l_abattement_pour_frais_professionnels.pop('salaires')
    minimum_de_l_abattement_pour_frais_professionnels = tspr.pop('minimum_de_l_abattement_pour_frais_professionnels')
    abatpen['min'] = minimum_de_l_abattement_pour_frais_professionnels.pop('pensions')
    abatpro['min'] = minimum_de_l_abattement_pour_frais_professionnels.pop('salaires')
    abatpro['min2'] = minimum_de_l_abattement_pour_frais_professionnels.pop('allocations_chomage')
    assert not maximum_de_l_abattement_pour_frais_professionnels, maximum_de_l_abattement_pour_frais_professionnels
    assert not minimum_de_l_abattement_pour_frais_professionnels, minimum_de_l_abattement_pour_frais_professionnels
    #
    impot_revenu['abattements_rni'] = abattements_rni = impot_revenu.pop('abat_rni')
    abattements_rni['enfant_marie'] = abattements_rni.pop('abattement_pour_rattachement_d_enfants_maries')
    abattements_rni['personne_agee_ou_invalide'] = personne_agee_ou_invalide = abattements_rni.pop(
        'abattement_pour_personnes_agees_de_de_65_ans_ou_invalide_4')
    personne_agee_ou_invalide['montant'] = personne_agee_ou_invalide.pop('montant_1')
    del personne_agee_ou_invalide['montant_2']  # montant_2 = montant_1 / 2
    #
    bareme_ir = impot_revenu.pop('bareme_ir')
    impot_revenu['bareme'] = tax_scale(
        bases_tree = bareme_ir.pop('seuils_inferieurs_des_tranches'),
        rates_tree = bareme_ir.pop('taux_marginaux_des_tranches'),
        )
    del bareme_ir['nombre_de_tranches']
    impot_revenu['taxe_complementaire_tc'] = bareme_ir.pop('taxe_complementaire_tc')
    impot_revenu['taxe_proportionnelle_tp'] = bareme_ir.pop('taxe_proportionnelle_tp')
    assert not bareme_ir, bareme_ir
    #
    impot_revenu['charges_deductibles'] = charges_deductibles = impot_revenu.pop('charg_deduc')
    charges_deductibles['accueil_personne_agee'] = charges_deductibles.pop(
        'deduction_pour_frais_d_accueil_d_une_personne_de_plus_de_75_ans')
    charges_deductibles['compte_epargne_codev'] = compte_epargne_codev = charges_deductibles.pop(
        'reduction_pour_versement_compte_epargne_codev')
    compte_epargne_codev['plafond_pct_rng'] = compte_epargne_codev.pop('plafond_en_du_revenu_net_global')
    charges_deductibles['grosses_reparations'] = charges_deductibles.pop('deductions_pour_grosses_reparations')
    charges_deductibles['pensions_alimentaires'] = charges_deductibles.pop('deduction_pour_pensions_alimentaires')
    charges_deductibles['pertes_en_capital_societes_nouvelles'] = pertes_en_capital_societes_nouvelles = \
        charges_deductibles.pop('deductions_pour_pertes_en_capital_societes_nouvelles')
    pertes_en_capital_societes_nouvelles['plafond_cb'] = pertes_en_capital_societes_nouvelles.pop('plafond_1')
    pertes_en_capital_societes_nouvelles['plafond_da'] = pertes_en_capital_societes_nouvelles.pop('plafond_2')
    charges_deductibles['sofipeche'] = sofipeche = charges_deductibles.pop(
        'deductions_pour_souscription_parts_sofipeche')
    sofipeche['plafond_pct_rng'] = sofipeche.pop('plafond_en_du_revenu_net_global')
    charges_deductibles['versements_perp'] = versements_perp = charges_deductibles.pop(
        'deduction_pour_versements_sur_perp')
    versements_perp['max'] = versements_perp.pop('maximum')
    versements_perp['min'] = versements_perp.pop('minimum')
    del charges_deductibles['deductions_investissement_dom_tom']
    #
    micro = impot_revenu.pop('micro')
    impot_revenu['rpns'] = dict(micro = micro)
    micro['microentreprise'] = micro.pop('abattement_sur_recettes_des_microentreprises')
    micro['microfoncier'] = microfoncier = micro.pop('abattement_pour_le_regime_microfoncier')
    microfoncier['max'] = microfoncier.pop('plafond_de_recettes')
    micro['specialbnc'] = specialbnc = micro.pop('abattement_pour_le_regime_micro_bnc')
    specialbnc['marchandises'] = dict(max = specialbnc.pop('plafond_de_recettes_marchandises'))
    specialbnc['services'] = dict(max = specialbnc.pop('plafond_de_recettes_services'))

    # pierre
    impot_revenu['rvcm'] = rvcm = impot_revenu.pop('rcm')
    rvcm = impot_revenu['rvcm']
    produits_des_assurances_vies_et_assimiles = rvcm['produits_des_assurances_vies_et_assimiles']
    rvcm['abat_assvie'] = abat_assvie = produits_des_assurances_vies_et_assimiles.pop('abattement')
    revenus_de_capitaux_mobiliers_dividendes = rvcm['revenus_de_capitaux_mobiliers_dividendes']
    rvcm['abatmob'] = abatmob = revenus_de_capitaux_mobiliers_dividendes.pop('abattement_forfaitaire')
    impot_revenu['rvcm'].update(rvcm.pop('revenus_de_capitaux_mobiliers_dividendes'))
    rvcm['taux_abattement_capitaux_mobiliers'] = taux_abattement_capitaux_mobiliers = rvcm.pop('taux_de_l_abattement')
    impot_revenu['reductions_impots'] = reductions_impots = dict()
    reductions_impots = impot_revenu['reductions_impots']
    reductions_impots['salarie_domicile'] = salarie_domicile = impot_revenu.pop('sal_dom')
    # Plus-values
    impot_revenu['plus_values'] = plus_values = impot_revenu.pop('pv')
    impot_revenu['plus_values'].update(plus_values.pop(
        'imposition_des_plus_values_de_cession_de_valeurs_mobilieres_et_des_plus_values_professionnelles'))
    # plus_values['taux1'] = taux1 = plus_values.pop('taux')

    reductions_impots['dons'] = dons = impot_revenu.pop('dons')
    dons_aux_oeuvres = dons['dons_aux_oeuvres']
    dons['taux_dons_oeuvres'] = taux_dons_oeuvres = dons_aux_oeuvres.pop('taux')
    dons_aux_partis_politiques = dons['dons_aux_partis_politiques']
    dons['taux_max_dons_partipo'] = taux_max_dons_partipo = dons_aux_partis_politiques.pop('plafond')
    reductions_impots['spfcpi'] = spfcpi = impot_revenu.pop('fcp')
    reductions_impots['spfcpi'].update(spfcpi.pop('reduction_d_impot_pour_souscriptions_de_parts_de_fcpi_ou_fip'))
    spfcpi['taux1'] = taux1 = spfcpi.pop('taux')

    impot_revenu['credits_impot'] = credits_impot = dict()
    credits_impot['ppe'] = ppe = impot_revenu.pop('ppe')
    credits_impot['ppe'].update(ppe.pop('seuil_de_rfr_pour_etre_eligibilite_a_la_ppe'))
    ppe['eligi1'] = eligi1 = ppe.pop('personne_seule')
    ppe['eligi2'] = eligi2 = ppe.pop('couple_marie_ou_pacse')
    ppe['eligi3'] = eligi3 = ppe.pop('increment_par_demi_part_de_qf_au_dela_de_1_ou_2')
    ppe['seuil1'] = seuil1 = ppe.pop('revenu_d_activite_individuel_minimum')
    ppe['seuil2'] = seuil2 = ppe.pop('revenu_d_activite_individuel_permettant_d_obtenir_la_ppe_a_taux_plein_cas_general')
    ppe['seuil3'] = seuil3 = ppe.pop('revenu_d_activite_individuel_maximum_cas_general')
    ppe['seuil4'] = seuil4 = ppe.pop('revenu_d_activite_individuel_permettant_d_obtenir_la_ppe_a_taux_plein_couples_mono_revenus')
    ppe['seuil5'] = seuil5 = ppe.pop('revenu_d_activite_individuel_maximum_couples_mono_emploi_et_parents_isoles')
    credits_impot['ppe'].update(ppe.pop('supplements'))
    ppe['monact'] = monact = ppe.pop('couples_mono_emploi')
    ppe['pac'] = pac = ppe.pop('par_personne_a_charge')
    credits_impot['ppe'].update(ppe.pop('taux_de_la_ppe'))
    ppe['taux1'] = taux1 = ppe.pop('phase_in')
    ppe['taux2'] = taux2 = ppe.pop('phase_out_cas_general')
    ppe['taux3'] = taux3 = ppe.pop('phase_out_couples_mono_emploi')
    minimun_de_ppe = ppe['minimun_de_ppe']
    ppe['versmin'] = versmin = minimun_de_ppe.pop('montant')

    impot_revenu['plafond_qf'] = plafond_qf = impot_revenu.pop('plaf_qf')
    impot_revenu['plafond_qf'].update(plafond_qf.pop('plafond_des_avantages_procures_par_demi_part_de_qf'))
    plafond_qf['veuf'] = plafond_qf.pop('veuf_avec_un_ou_plusieurs_enfants_a_charge')
    plafond_qf['celib'] = plafond_qf.pop('personnes_seules_ayant_eus_des_enfants')
    plafond_qf['celib_enf'] = plafond_qf.pop('part_pour_le_1er_enfant_des_parents_isoles')
    plafond_qf['reduc_postplafond'] = plafond_qf.pop('invalidite_ancien_combattant')

    # garde enfant
    credits_impot['garext'] = garext = impot_revenu.pop('gardenf')
    credit_d_impot_pour_frais_de_garde_d_enfants = garext['credit_d_impot_pour_frais_de_garde_d_enfants']
    credits_impot['garext'].update(garext.pop('credit_d_impot_pour_frais_de_garde_d_enfants'))

    # contribution haut revenus
    taxe_hr = impot_revenu['taxe_hr']
    impot_revenu['taxe_hr'].update(taxe_hr.pop('contribution_exceptionnelle_sur_les_hauts_revenus'))
    impot_revenu['cehr_ipp'] = cehr_ipp = impot_revenu.pop('taxe_hr')

    impot_revenu['cehr_ipp'] = tax_scale(
        bases_tree = dict(
            tranche1 = cehr_ipp.pop('seuil_de_la_1ere_tranche'),
            tranche2 = cehr_ipp.pop('seuil_de_la_2eme_tranche'),
            ),
        rates_tree = dict(
            tranche1 = cehr_ipp.pop('taux_marginal_de_la_1ere_tranche'),
            tranche2 = cehr_ipp.pop('taux_marginal_de_la_2eme_tranche'),
            ),
        )

    reductions_impots['ecodev'] = ecodev = impot_revenu.pop('codev')
    compte_epargne_co_developpement = ecodev['compte_epargne_co_developpement']
    reductions_impots['ecodev'].update(ecodev.pop('compte_epargne_co_developpement'))
    ecodev['taux_plafond'] = taux_plafond = ecodev.pop('plafond_en_du_revenu_net_global')

    # reduction impot emprunt
    reductions_impots['intemp'] = intemp = impot_revenu.pop('habitat_princ_reduc')
    reduction_d_impot_pour_interets_d_emprunt_habitat = intemp['reduction_d_impot_pour_interets_d_emprunt_habitat']
    reduction_d_impot_pour_interets_d_emprunt_habitat['taux1'] = reduction_d_impot_pour_interets_d_emprunt_habitat.pop(
        'taux')
    reductions_impots['intemp'].update(intemp.pop('reduction_d_impot_pour_interets_d_emprunt_habitat'))
    intemp['pac'] = intemp.pop('increment_du_plafond')
    intemp['max'] = intemp.pop('plafond_1')

    # accueil personne agée
    reductions_impots['daepad'] = daepad = impot_revenu.pop('heberg_sante')
    reductions_impots['daepad'].update(daepad.pop(
        'reductions_d_impot_pour_depenses_d_accueil_dans_etablissement_pour_les_personnes_agees'))
    daepad['max'] = daepad.pop('plafond')

    # enfant scolarisé
    reductions_impots['ecpess'] = ecpess = impot_revenu.pop('enfscol')
    reductions_impots['ecpess'].update(ecpess.pop('reduction_pour_enfants_scolarises'))
    ecpess['col'] = ecpess.pop('college')
    ecpess['lyc'] = ecpess.pop('lycee')
    ecpess['sup'] = ecpess.pop('universite')

    # investissement foret
    reductions_impots['invfor'] = invfor = impot_revenu.pop('foret')
    depenses_d_investissement_forestier = invfor.pop('depenses_d_investissement_forestier')
    invfor.update({
        'taux': depenses_d_investissement_forestier['taux'],
        'seuil': depenses_d_investissement_forestier['plafond_de_depenses'],
        })

    # prestations compensatoires
    reductions_impots['prcomp'] = prcomp = impot_revenu.pop('prest_compen')
    reductions_impots['prcomp'].update(prcomp.pop('prestations_compensatoires'))
    prcomp['seuil'] = prcomp.pop('plafond')

    del root['baremes_ipp_marche_du_travail_labour_market']
    # root['marche_du_travail'] = root.pop('baremes_ipp_marche_du_travail_labour_market')

    root['prelevements_sociaux'] = prelevements_sociaux = root.pop(
        'baremes_ipp_prelevements_sociaux_social_security_contributions')
    prelevements_sociaux['cotisations_sociales'] = cotisations_sociales = {}
    # TODO: abat_red non modifié
    #
    # TODO: accidents (AT-MP) non modifié
    cotisations_sociales['agff'] = agff = prelevements_sociaux.pop('agff')
    tranche_1_a = agff.pop('tranche_1_a')
    tranche_2 = agff.pop('tranche_2')
    tranche_b = agff.pop('tranche_b')
    tranche_1_a_employeur = tranche_1_a.pop('employeur')
    tranche_1_a_salarie = tranche_1_a.pop('salarie')
    agff['employeur'] = dict()
    agff['employeur']['non_cadre'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_1 = 0,
            tranche_2 = 1,
            ),
        null_rate_base = 3,
        rates_tree = dict(
            tranche_1 = tranche_1_a_employeur,
            tranche_2 = tranche_2.pop('employeur'),
            ),
        )
    agff['employeur']['cadre'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_1 = 0,
            tranche_2 = 1,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_1 = tranche_1_a_employeur,
            tranche_2 = tranche_b.pop('employeur'),
            ),
        )
    agff['salarie'] = dict()
    agff['salarie']['non_cadre'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_1 = 0,
            tranche_2 = 1,
            ),
        null_rate_base = 3,
        rates_tree = dict(
            tranche_1 = tranche_1_a_salarie,
            tranche_2 = tranche_2.pop('salarie'),
            ),
        )
    agff['salarie']['cadre'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_1 = 0,
            tranche_2 = 1,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_1 = tranche_1_a_salarie,
            tranche_2 = tranche_b.pop('salarie'),
            ),
        )

    cotisations_sociales['agirc'] = agirc = prelevements_sociaux.pop('agirc')
    taux_effectifs_salaries_employeurs = agirc.pop('taux_effectifs_salaries_employeurs')
    tranche_b_avant_81 = taux_effectifs_salaries_employeurs.pop('tranche_b_avant_81')
    tranche_b_depuis_81 = taux_effectifs_salaries_employeurs.pop('tranche_b_depuis_81')
    tranche_c_avant_81 = taux_effectifs_salaries_employeurs.pop('tranche_c_avant_81')
    tranche_c_apres_81 = taux_effectifs_salaries_employeurs.pop('tranche_c_apres_81')
    agirc['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            tranche_c = 4,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_a = 0,
            tranche_b = tranche_b_avant_81.pop('employeur'),
            tranche_c = tranche_c_avant_81.pop('employeur'),
            ),
        )
    agirc['employeur_depuis_81'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            tranche_c = 4,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_a = 0,
            tranche_b = tranche_b_depuis_81.pop('employeur'),
            tranche_c = tranche_c_apres_81.pop('employeur'),
            ),
        )
    agirc['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            tranche_c = 4,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_a = 0,
            tranche_b = tranche_b_avant_81.pop('salarie'),
            tranche_c = tranche_c_avant_81.pop('salarie'),
            ),
        )
    agirc['salarie_depuis_81'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            tranche_c = 4,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_a = 0,
            tranche_b = tranche_b_depuis_81.pop('salarie'),
            tranche_c = tranche_c_apres_81.pop('salarie'),
            ),
        )
    assert not tranche_b_avant_81, tranche_b_avant_81
    assert not tranche_b_depuis_81, tranche_b_depuis_81
    assert not tranche_c_avant_81, tranche_c_avant_81
    assert not tranche_c_apres_81, tranche_c_apres_81
    assert not taux_effectifs_salaries_employeurs, taux_effectifs_salaries_employeurs
    del agirc['taux_contractuels']
    del agirc['taux_d_appel']
    del agirc['taux_effectifs']
    #
    cotisations_sociales['ags'] = ags = prelevements_sociaux.pop('ags')
    employeurs = ags.pop('employeurs')
    ags['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a_b = 0,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_a_b = employeurs.pop('sous_4_pss'),
            ),
        )
    assert not employeurs, employeurs
    #
    # alleg_gen allégements généraux de cotisations sociales (ristourne Juppé)
    # apec-f et apec traité ci dessous
    cotisations_sociales['apec'] = apec = prelevements_sociaux.pop('apec_f')
    apec_baremes = prelevements_sociaux.pop('apec')
    tranche_b = apec_baremes.pop('tranche_b_de_1_a_4_pss')
    tranche_a_b = apec_baremes.pop('sous_4_pss')
    apec['employeur_avant_2011'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_a = 0,
            tranche_b = tranche_b.pop('employeur'),
            ),
        )
    apec['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a_b = 0,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_a_b = tranche_a_b.pop('employeur'),
            ),
        )
    apec['salarie_avant_2011'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_a = 0,
            tranche_b = tranche_b.pop('salarie'),
            ),
        )
    apec['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a_b = 0,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_a_b = tranche_a_b.pop('salarie'),
            ),
        )
    assert not tranche_b, tranche_b
    assert not tranche_a_b, tranche_a_b
    #
    cotisations_sociales['apprentissage'] = apprentissage = prelevements_sociaux.pop('apprentissage')
    employeur_tout_salaire = apprentissage.pop('employeur_tout_salaire')
    apprentissage['taxe_apprentissage'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = employeur_tout_salaire.pop('taxe_d_apprentissage'),
            ),
        )
    # assert not employeur_tout_salaire
    del employeur_tout_salaire
    #
    cotisations_sociales['arrco'] = arrco = prelevements_sociaux.pop('arrco')
    taux_effectifs_salaries_employeurs = arrco.pop('taux_effectifs_salaries_employeurs')
    arrco_taux_effectifs_tranche_1 = taux_effectifs_salaries_employeurs.pop('tranche_1')
    arrco_taux_effectifs_tranche_2 = taux_effectifs_salaries_employeurs.pop('tranche_2_apres_1997')
    arrco['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_1 = 0,
            tranche_2 = 1,
            ),
        null_rate_base = 3,
        rates_tree = dict(
            tranche_1 = arrco_taux_effectifs_tranche_1.pop('employeur'),
            tranche_2 = arrco_taux_effectifs_tranche_2.pop('employeur'),
            )
        )
    arrco['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_1 = 0,
            tranche_2 = 1,
            ),
        null_rate_base = 3,
        rates_tree = dict(
            tranche_1 = arrco_taux_effectifs_tranche_1.pop('salarie'),
            tranche_2 = arrco_taux_effectifs_tranche_2.pop('salarie'),
            )
        )
    assert not arrco_taux_effectifs_tranche_1
    assert not arrco_taux_effectifs_tranche_2
    #
    # TODO asf 1984-2001
    # TODO aubry
    # TODO auto_entrepreneur
    #
    prelevements_sociaux['contributions'] = contributions = dict()
    contributions['casa'] = casa = prelevements_sociaux.pop('casa')
    contributions['casa'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = casa.pop('pensions_de_retraite_de_preretraite_et_d_invalidite'),
            )
        )
    #
    cotisations_sociales['cet'] = cet = prelevements_sociaux.pop('cet')
    salaire_sous_8_pss = cet.pop('salaire_sous_8_pss')
    cet['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            salaire_sous_8_pss = 0,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            salaire_sous_8_pss = salaire_sous_8_pss.pop('employeur'),
            )
        )
    cet['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            salaire_sous_8_pss = 0,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            salaire_sous_8_pss = salaire_sous_8_pss.pop('salarie'),
            )
        )
    assert not salaire_sous_8_pss
    #
    # TODO chômage
    cotisations_sociales['chomage'] = chomage = prelevements_sociaux.pop('chomage')
    chomage['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_a = chomage['employeurs'].pop('tranche_a'),
            tranche_b = chomage['employeurs'].pop('tranche_b'),
            )
        )
    chomage['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b = 1,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_a = chomage['salaries'].pop('tranche_a'),
            tranche_b = chomage['salaries'].pop('tranche_b'),
            )
        )
    #
    # CICE unchanged done
    #
    vieillesse = prelevements_sociaux.pop('cnav')
    cotisations_sociales['vieillesse_deplafonnee'] = vieillesse_deplafonnee = vieillesse.pop('sur_tout_salaire')
    cotisations_sociales['vieillesse_plafonnee'] = vieillesse_plafonnee = vieillesse.pop('salaire_sous_plafond')
    vieillesse_deplafonnee['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = vieillesse_deplafonnee.pop('employeurs'),
            )
        )
    vieillesse_deplafonnee['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = vieillesse_deplafonnee.pop('salaries'),
            )
        )
    vieillesse_plafonnee['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        null_rate_base = 1,
        rates_tree = dict(
            tranche_unique = vieillesse_plafonnee.pop('employeurs'),
            )
        )
    vieillesse_plafonnee['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        null_rate_base = 1,
        rates_tree = dict(
            tranche_unique = vieillesse_plafonnee.pop('salaries'),
            )
        )
    # assert not vieillesse_deplafonnee
    # assert not vieillesse_plafonnee
    #
    # cnracl
    cotisations_sociales['cnracl'] = cnracl_node = prelevements_sociaux.pop('cnracl')
    cnracl_node['cnracl'] = cnracl = cnracl_node.pop('cnracl')
    cnracl['salarie'] = cnracl_salarie = cnracl.pop('agents')
    cnracl_salarie['hors_nbi'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = cnracl_salarie.pop('hors_nbi'),
            )
        )
    cnracl_salarie['nbi'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = cnracl_salarie.pop('nbi'),
            )
        )
    cnracl['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = cnracl.pop('employeurs'),
            )
        )
    cnracl_node['atiacl'] = atiacl = cnracl_node.pop('atiacl')
    atiacl['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = atiacl.pop('hors_nbi'),
            )
        )
    # TODO: FCPPA
    cnracl_node['feh'] = feh = cnracl_node.pop('feh')
    feh['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = feh.pop('hors_cl'),
            )
        )
    #
    cotisations_sociales['construction'] = construction = prelevements_sociaux.pop('construction')
    construction_employeur_sur_tout_salaire = construction.pop('employeur_sur_tout_salaire')
    construction['construction_10_19'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = construction_employeur_sur_tout_salaire.pop('de_10_a_19_salaries'),
            ),
        )
    construction['construction_20'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = construction_employeur_sur_tout_salaire.pop('plus_de_20_salaries'),
            ),
        )
    assert not construction_employeur_sur_tout_salaire
    #
    contributions['csg'] = csg = prelevements_sociaux.pop('csg_activite')
    csg['activite'] = csg_activite = csg.pop('revenus_d_activite')
    csg_activite['deductible'] = csg_activite_deductible = dict()
    csg_activite_deductible['taux'] = csg_activite.pop('taux_csg_deductible')
    csg_activite['taux_global'] = csg_activite.pop('taux_global_csg')

    csg['remplacement'] = csg_remplacement = prelevements_sociaux.pop('csg_remplacement')

    contributions['crds'] = crds = prelevements_sociaux.pop('crds')

    #
    deces_ac = prelevements_sociaux['deces_ac']
    commercants_industriels = deces_ac['commercants_industriels']
    del commercants_industriels['deces']
    del commercants_industriels['invalidite']
    #
    # TODO css-chom
    #
    # TODO: famille-ind
    #
    famille = prelevements_sociaux.pop('famille')
    famille_sur_tout_salaire = famille.pop('sur_tout_salaire')
    cotisations_sociales['famille'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = famille_sur_tout_salaire.pop('employeurs'),
            ),
        )
    assert not famille_sur_tout_salaire
    #
    cotisations_sociales['fds'] = fds = prelevements_sociaux.pop('fds')
    fds['cotisation_exceptionnelle_solidarite'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        null_rate_base = 4,
        rates_tree = dict(
            tranche_unique = fds.pop('taux'),
            ),
        )
    #
    fillon = prelevements_sociaux['fillon']
    # Deleted, because value must be a float.
    del fillon['ensemble_des_entreprises']['salaire_de_reference']
    del fillon['entreprises_restees_aux_39_heures_hebdomadaires_au_30_06_2003']['salaire_de_reference']
    del fillon['entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003']['salaire_de_reference']
    #
    cotisations_sociales['fnal'] = fnal = prelevements_sociaux.pop('fnal')
    tout_employeur = fnal.pop('tout_employeur')
    fnal['tout_employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            sous_pss = 0,
            ),
        null_rate_base = 1,
        rates_tree = dict(
            sous_pss = tout_employeur.pop('sous_pss'),
            ),
        )
    # TODO date mismatch debug wth test_legislation
    # entreprises_de_plus_de_20_salaries = fnal.pop('entreprises_de_plus_de_20_salaries')
    # fnal['entreprises_de_plus_de_20_salaries'] = fixed_bases_tax_scale(
    #     base_by_slice_name = dict(
    #         sous_pss = 0,
    #         au_dessus_du_pss = 1
    #         ),
    #     rates_tree = dict(
    #         sous_pss = entreprises_de_plus_de_20_salaries.pop('sous_pss'),
    #         au_dessus_du_pss = entreprises_de_plus_de_20_salaries.pop('au_dessus_du_pss'),
    #         ),
    #     )
    # forfait_social already ok
    #
    cotisations_sociales['formation'] = formation = prelevements_sociaux.pop('formation')
    formation['employeur'] = employeur = formation.pop('employeur_tout_salaire')
    employeur['moins_de_10_salaries'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tout_salaire = 0,
            ),
        rates_tree = dict(
            tout_salaire = employeur.pop('moins_de_10_salaries'),
            ),
        )
    employeur['de_10_a_19_salaries'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tout_salaire = 0,
            ),
        rates_tree = dict(
            tout_salaire = employeur.pop('de_10_a_19_salaries'),
            ),
        )
    employeur['20_salaries_et_plus'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tout_salaire = 0,
            ),
        rates_tree = dict(
            tout_salaire = employeur.pop('20_salaries_et_plus'),
            ),
        )
    # TODO atlerannce, cdd, DIF
    # TODO formation-ac et formation-pl
    # gmp no need to change anything here
    cotisations_sociales['ircantec'] = ircantec = prelevements_sociaux.pop('ircantec')
    taux_effectifs = ircantec.pop('taux_de_cotisations_effectifs')
    ircantec['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b_1_4_75_puis_1_a_8_pss = 1,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_a = taux_effectifs['tranche_a'].pop('employeur'),
            tranche_b_1_4_75_puis_1_a_8_pss = taux_effectifs['tranche_b_1_4_75_puis_1_a_8_pss'].pop('employeur'),
            )
        )
    ircantec['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            tranche_b_1_4_75_puis_1_a_8_pss = 1,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_a = taux_effectifs['tranche_a'].pop('agent'),
            tranche_b_1_4_75_puis_1_a_8_pss = taux_effectifs['tranche_b_1_4_75_puis_1_a_8_pss'].pop('agent'),
            )
        )
    # TODO tranche à 4.75
    del taux_effectifs
    #
    cotisations_sociales['mmid'] = mmid = prelevements_sociaux.pop('mmid')
    salaire_sous_plafond = mmid.pop('salaire_sous_plafond')
    sur_tout_salaire = mmid.pop('sur_tout_salaire')
    mmid['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            ),
        rates_tree = dict(
            tranche_a = sur_tout_salaire.pop('employeurs'),
            ),
        )
    mmid['employeur2'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            ),
        null_rate_base = 1,
        rates_tree = dict(
            tranche_a = salaire_sous_plafond.pop('employeurs'),
            ),
        )
    mmid['reduction_65_ans'] = salaire_sous_plafond.pop('reduction_65_ans')
    mmid['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tout_salaire = 0,
            ),
        rates_tree = dict(
            tout_salaire = sur_tout_salaire.pop('salaries'),
            ),
        )
    mmid['salarie2'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            ),
        null_rate_base = 1,
        rates_tree = dict(
            tranche_a = salaire_sous_plafond.pop('salaries'),
            ),
        )
    assert not sur_tout_salaire, sur_tout_salaire
    assert not salaire_sous_plafond, salaire_sous_plafond
    # TODO: mmid-ac.yaml, mmid-am.yaml, mmid-cl.yaml, mmid-etat.yaml, mmid-ret.yaml, mm-pl
    #
    # TODO: prévoyance
    cotisations_sociales['rafp'] = rafp = prelevements_sociaux.pop('rafp')
    taux_de_cotisation = rafp.pop('taux_de_cotisation')
    rafp['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            ),
        rates_tree = dict(
            tranche_a = taux_de_cotisation.pop('etat'),
            ),
        )
    rafp['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_a = 0,
            ),
        rates_tree = dict(
            tranche_a = taux_de_cotisation.pop('agent'),
            ),
        )
    del taux_de_cotisation
    #
    # TODO red-a, red-j, red-m
    prelevements_sociaux['allegement_cotisation_allocations_familiales'] = prelevements_sociaux.pop('reduc_famille')
    # TODO ret-ac.yaml, ret-comp-ac.yaml, ret-comp-pl.yaml, ret-pl.yaml, ret-etat.yaml
    # TODO retraite chapeau

    root['prestations'] = prestations = root.pop('baremes_ipp_prestations_sociales_social_benefits')
    prestations['prestations_familiales'] = prestations_familiales = dict()
    # aeeh
    prestations_familiales['aeeh'] = aeeh = prestations.pop('aeeh')
    # aeeh['age'] = aeeh.pop('age_maximum_de_l_enfant')  TODO: problem with start date
    aeeh['base'] = aeeh.pop('montant_de_bmaf')
    # af
    prestations_familiales['af'] = af = prestations.pop('af_cm')
    modulation_ipp = prestations.pop('af_cond')
    modulation = af['modulation']
    modulation['taux_tranche_1'] = modulation.pop('tranche_1_en_de_la_bmaf')
    modulation['taux_tranche_2'] = modulation.pop('tranche_2_en_de_la_bmaf')
    modulation['taux_tranche_3'] = modulation.pop('tranche_3_en_de_la_bmaf')
    modulation['majoration_plafond_par_enfant_supplementaire'] = modulation_ipp.pop(
        'majoration_ressource_par_enfant_supplementaire')
    modulation['plafond_tranche_1'] = modulation_ipp.pop('plafond_de_ressources_tranche_1')
    modulation['plafond_tranche_2'] = modulation_ipp.pop('plafond_de_ressources_tranche_2')
    af['majoration'] = prestations.pop('af_maj')
    af['plafond_1998'] = af_plaf = prestations.pop('af_plaf')
    af['taux'] = taux = dict()
    taux['enf3'] = af.pop('par_enfant_supplementaire')
    af = prestations_familiales['af']
    af['af_dom'] = af_dom = prestations.pop('af_maj_dom')
    af_dom = af['af_dom']
    majoration_pour_le_premier_enfant_en_de_la_bmaf_dom = af_dom['majoration_pour_le_premier_enfant_en_de_la_bmaf_dom']
    tranches_d_age = af_dom['tranches_d_age']
    af_dom['taux_1er_enf_tranche_2_dom'] = taux_1er_enf_tranche_2_dom = majoration_pour_le_premier_enfant_en_de_la_bmaf_dom.pop('taux_de_la_tranche_2')
    af_dom['taux_1er_enf_tranche_1_dom'] = taux_1er_enf_tranche_1_dom = majoration_pour_le_premier_enfant_en_de_la_bmaf_dom.pop('taux_de_la_tranche_1')
    af_dom['age_1er_enf_tranche_1_dom'] = age_1er_enf_tranche_1_dom = tranches_d_age.pop(
        'age_debut_de_la_premiere_tranche')
    af_dom['age_1er_enf_tranche_2_dom'] = age_1er_enf_tranche_2_dom = tranches_d_age.pop(
        'age_debut_de_la_deuxieme_tranche')
    af_dom['taux_enfant_seul'] = taux_enfant_seul = af_dom.pop(
        'les_allocations_familiales_pour_un_enfant_en_de_la_bmaf')
    prestations_familiales['af'].update(af.pop('majoration'))
    af['majoration_enfants'] = majoration_enfants = af.pop('majoration_pour_les_enfants_en_de_la_bmaf')
    majoration_enfants = af['majoration_enfants']
    af['majoration_enfants'].update(majoration_enfants.pop('allocation_forfaitaire'))
    majoration_enfants['age_minimal_forfait'] = age_minimal_forfait = majoration_enfants.pop('age_minimum')
    majoration_enfants['taux_allocation_forfaitaire'] = taux_allocation_forfaitaire = majoration_enfants.pop('taux')

    del prestations['aa_plaf']
    #   aa_plaf:
    #     Plafonds de ressources: null  # Value must be a float
    #   aes:
    #     Complément d'allocation:
    #       3e catégorie: null  # Changement d'unité de FRF à %
    #  On retire l'élément qui pose problème
    prestations['aes']['complement_d_allocation']['3e_categorie'] = [
        element for element in prestations['aes']['complement_d_allocation']['3e_categorie']
        if element['value'] is None or element['value'].endswith('%')
        ]
    prestations_familiales['aes'] = aes = prestations.pop('aes')
    aes['base'] = aes.pop('montant_de_bmaf_ou_en_euros')
    # AL
    prestations['aides_logement'] = aides_logement = dict()
    aides_logement['al_charge'] = al_charge = prestations.pop('al_charge')
    aides_logement['forfait_charges'] = forfait_charges = dict()
    forfait_charges['cas_general'] = al_charge['personne_isolee_ou_menage_seul'].pop('cas_general')
    forfait_charges['majoration_par_enfant'] = al_charge.pop('majoration_par_enfant_de_la_majoration_pour_charges_2')

    # prestations['al_charge']
    #   al_charge:
    #     Cas des colocataires ou des propriétaires (1):
    #       Isolé ou couple avec un enfant ou une personne à charge: null  # Value must be a float
    #       Majoration par enfant de la majoration pour charges: null  # Value must be a float
    aides_logement['al_pac'] = al_pac = prestations.pop('al_pac')
    # prestations['al_pac']
    #   al_pac:
    #     Âge limite pour les enfants à charge: null  # Value must be a float
    #     Plafonds de ressources que les potentiels personnes à charge autre que les enfants doivent respecter:
    #       null  # Value must be a float
    del prestations['al_plaf_acc'][
        'intervalle_de_date_du_certificat_d_emprunt_correspondant_aux_plafonds_d_accession_a_la_propriete']
    #   al_plaf_acc:
    #     Intervalle de date du certificat d'emprunt correspondant aux plafonds d'accession à la propriété:
    #       null  # Value must be a float

    aides_logement['al_param2'] = al_param2 = prestations.pop('al_param2')
    al_param2['r1_en_du_rsa_socle'] = r1_en_du_rsa_socle = al_param2.pop('r1_en_du_rsa_socle_1')
    r1_en_du_rsa_socle = al_param2['r1_en_du_rsa_socle']
    r1_en_du_rsa_socle['personne_isolee'] = personnes_isolees = r1_en_du_rsa_socle.pop(
        'personnes_isolees_en_du_rmi_de_base')
    r1_en_du_rsa_socle['majoration_enfant_a_charge_supp'] = majoration_enfant_a_charge_supp = r1_en_du_rsa_socle.pop(
        'majoration_par_enfant_a_charge_supplementaire_en_du_rmi_de_base')
    r1_en_du_rsa_socle['couple_sans_enf'] = couple_sans_enf = r1_en_du_rsa_socle.pop('couples_en_du_rmi_de_base')
    r1_en_du_rsa_socle['personne_isolee_ou_couple_avec_1_enf'] = personne_isolee_ou_couple_avec_1_enf = r1_en_du_rsa_socle.pop('personnes_isolees_ou_couples_avec_1_enfant_en_du_rmi_de_base')
    r1_en_du_rsa_socle['personne_isolee_ou_couple_avec_2_enf'] = personne_isolee_ou_couple_avec_2_enf = r1_en_du_rsa_socle.pop('personnes_isolees_ou_couples_avec_2_enfants_en_du_rmi_de_base')
    aides_logement['r1'] = r1 = al_param2.pop('r1_en_du_rsa_socle')

    al_param2['r2_ipp'] = r2_ipp = al_param2.pop('r2_en_de_la_bmaf_1')
    r2_ipp['majoration_par_enf_supp_a_charge'] = majoration_par_enf_supp_a_charge = r2_ipp.pop(
        'majoration_par_enfant_a_charge_supplementaire_en_de_la_bmaf_au_01_01_n_2')
    r2_ipp['personnes_isolees_ou_couples_avec_2_enf'] = personnes_isolees_ou_couples_avec_2_enf = r2_ipp.pop(
        'personnes_isolees_ou_couples_avec_2_enfants_en_de_la_bmaf_au_01_01_n_2')
    aides_logement['r2'] = r2 = al_param2.pop('r2_ipp')

    del prestations['al_plaf_loc2']['loyer_de_reference']

    aides_logement['al_plaf_loc2'] = al_plaf_loc2 = prestations.pop('al_plaf_loc2')
    al_plaf_loc2['taux_participation_fam_ipp'] = taux_participation_fam_ipp = al_plaf_loc2.pop('tf')
    taux_participation_fam_ipp = al_plaf_loc2['taux_participation_fam_ipp']
    taux_participation_fam_ipp['taux_1_adulte'] = taux_1_adulte = taux_participation_fam_ipp.pop('personnes_isolees')
    taux_participation_fam_ipp['taux_2_adulte'] = taux_2_adulte = taux_participation_fam_ipp.pop('couples_sans_enfant')
    taux_participation_fam_ipp['taux_1_enf'] = taux_1_enf = taux_participation_fam_ipp.pop(
        'personnes_seules_et_couples_avec_1_enfant')
    taux_participation_fam_ipp['taux_2_enf'] = taux_2_enf = taux_participation_fam_ipp.pop(
        'personnes_seules_et_couples_avec_2_enfants')
    taux_participation_fam_ipp['taux_3_enf'] = taux_3_enf = taux_participation_fam_ipp.pop(
        'personnes_seules_et_couples_avec_3_enfants')
    taux_participation_fam_ipp['taux_4_enf'] = taux_4_enf = taux_participation_fam_ipp.pop(
        'personnes_seules_et_couples_avec_4_enfants')
    taux_participation_fam_ipp['taux_enf_supp'] = taux_enf_supp = taux_participation_fam_ipp.pop(
        'variation_de_tf_par_enfant_supplementaire')
    aides_logement['taux_participation_fam'] = taux_participation_fam = al_plaf_loc2.pop('taux_participation_fam_ipp')
    del taux_participation_fam_ipp
    al_plaf_loc2['taux_participation_loyer_ipp'] = taux_participation_loyer_ipp = al_plaf_loc2.pop('tl')
    taux_participation_loyer_ipp['taux_tranche_1'] = taux_tranche_1 = taux_participation_loyer_ipp.pop(
        'tl_pour_la_1ere_tranche')
    taux_participation_loyer_ipp['taux_tranche_2'] = taux_tranche_2 = taux_participation_loyer_ipp.pop(
        'tl_pour_la_2eme_tranche')
    taux_participation_loyer_ipp['taux_tranche_3'] = taux_tranche_3 = taux_participation_loyer_ipp.pop(
        'tl_pour_la_3eme_tranche')
    aides_logement['taux_participation_loyer'] = taux_participation_loyer = al_plaf_loc2.pop(
        'taux_participation_loyer_ipp')
    # par zone
    aides_logement['loyers_plafond'] = loyers_plafond = dict()
    loyers_plafond['zone1'] = zone1 = dict()
    plafond_de_loyers_zone_1 = al_plaf_loc2['plafond_de_loyers_zone_1']
    zone1['personnes_seules'] = plafond_de_loyers_zone_1.pop('personnes_seules')
    zone1['couples'] = plafond_de_loyers_zone_1.pop('couples')
    zone1['un_enfant'] = plafond_de_loyers_zone_1.pop('personnes_seules_ou_couples_avec_1_enfant')
    zone1['majoration_par_enf_supp'] = plafond_de_loyers_zone_1.pop('majoration_par_enfant_supplementaire')

    loyers_plafond['zone2'] = zone2 = dict()
    plafond_de_loyers_zone_2 = al_plaf_loc2['plafond_de_loyers_zone_2']
    zone2['personnes_seules'] = plafond_de_loyers_zone_2.pop('personnes_seules')
    zone2['couples'] = plafond_de_loyers_zone_2.pop('couples')
    zone2['un_enfant'] = plafond_de_loyers_zone_2.pop('personnes_seules_ou_couples_avec_1_enfant')
    zone2['majoration_par_enf_supp'] = plafond_de_loyers_zone_2.pop('majoration_par_enfant_supplementaire')

    loyers_plafond['zone3'] = zone3 = dict()
    plafond_de_loyers_zone_3 = al_plaf_loc2['plafond_de_loyers_zone_3']
    zone3['personnes_seules'] = plafond_de_loyers_zone_3.pop('personnes_seules')
    zone3['couples'] = plafond_de_loyers_zone_3.pop('couples')
    zone3['un_enfant'] = plafond_de_loyers_zone_3.pop('personnes_seules_ou_couples_avec_1_enfant')
    zone3['majoration_par_enf_supp'] = plafond_de_loyers_zone_3.pop('majoration_par_enfant_supplementaire')

    del taux_participation_loyer_ipp
    aides_logement['al_min'] = al_min = prestations.pop('al_min')
    al_min['montant_min_mensuel'] = montant_min_mensuel = al_min.pop('montant_minimal_mensuel')
    montant_min_mensuel['montant_min_apl_al'] = montant_min_apl_al = montant_min_mensuel.pop('apl_ou_al')

    aides_logement['participation_min'] = participation_min = dict()
    aides_logement['montant_forfaitaire'] = montant_forfaitaire = al_plaf_loc2.pop(
        'montant_forfaitaire_de_la_participation_minimale_po')
    aides_logement['taux'] = taux = al_plaf_loc2.pop('montant_proportionnel_de_la_participation_minimale_po')
    participation_min['montant_forfaitaire'] = aides_logement.pop('montant_forfaitaire')
    participation_min['taux'] = aides_logement.pop('taux')

    del prestations['api_fl']
    #   api_fl:
    #     Forfait logement:
    #       Couple, 1 enfant (1): null  # Value must be a float
    #       couples_2_enfants_ou_plus_1: null  # Value must be a float
    #       Femmes enceintes (1): null  # Value must be a float
    prestations_familiales['ars'] = ars = dict()
    ars['ars_cond'] = ars_cond = prestations.pop('ars_cond')
    ars_m = prestations.pop('ars_m')
    ars_maj = prestations.pop('ars_maj')
    ars_min = prestations.pop('ars_min')
    ars_plaf = prestations.pop('ars_plaf')
    ars_cond['age_entree_primaire'] = age_entree_primaire = ars_cond.pop('age_minimal_de_l_enfant_1')
    ars_cond['age_sortie_lycee'] = age_sortie_lycee = ars_cond.pop('age_maximal_de_l_enfant_2')
    ars['age_entree_primaire'] = age_entree_primaire = ars_cond.pop('age_entree_primaire')
    ars['age_sortie_lycee'] = age_sortie_lycee = ars_cond.pop('age_sortie_lycee')
    ars['majoration_par_enf_supp'] = majoration_par_enf_supp = ars_plaf.pop(
        'majoration_par_enfant_en_du_plafond_de_ressources_avec_0_enfant')
    ars['montant_seuil_non_versement'] = montant_seuil_non_versement = ars_min.pop('montant_minimum_verse')
    ars['plafond_ressources'] = plafond_ressources = ars_plaf.pop('plafond_de_ressources_0_enfant')
    ars['taux_primaire'] = taux_primaire = ars_m.pop('enfants_entre_6_et_10_ans_en_de_la_bmaf_1')
    ars['taux_college'] = taux_college = ars_m.pop('enfants_entre_11_et_14_ans_en_de_la_bmaf_2')
    ars['taux_lycee'] = taux_lycee = ars_m.pop('enfants_15_ans_et_en_de_la_bmaf_3')

    prestations_familiales['cf'] = cf = dict()
    cf = prestations_familiales['cf']
    prestations_familiales['cf'].update(prestations.pop('cf_maj'))
    prestations_familiales['cf'].update(prestations.pop('cf_plaf'))
    prestations_familiales['cf'].update(prestations.pop('cf_cm'))
    cf['age_min'] = age_min = cf.pop('age_minimal_des_enfants_pris_en_compte')
    cf['age_max'] = age_max = cf.pop('age_maximal_des_enfants_pris_en_compte')
    majoration = cf['majoration']
    cf['majoration_plafond_biact_isole'] = majoration_plafond_biact_isole = majoration.pop(
        'biactifs_et_parents_isoles')
    cf['majoration_plafond_2_premiers_enf'] = majoration_plafond_2_premiers_enf = majoration.pop(
        '1er_et_2eme_enfants_en_du_plafond_de_ressources_avec_0_enfant')
    cf['majoration_plafond_3eme_enf_et_plus'] = majoration_plafond_3eme_enf_et_plus = majoration.pop(
        '3eme_enfant_et_plus_en_du_plafond_de_ressources_avec_0_enfant')
    complement_familial_en_de_la_bmaf_en_de_la_bmaf = cf['complement_familial_en_de_la_bmaf_en_de_la_bmaf']
    cf['taux_cf_base'] = taux_cf_base = complement_familial_en_de_la_bmaf_en_de_la_bmaf.pop('montant_de_base')
    cf['taux_cf_majore'] = taux_cf_majore = complement_familial_en_de_la_bmaf_en_de_la_bmaf.pop('montant_majore')
    prestations_familiales['cf'].update(prestations.pop('cf_cm_dom'))
    cf['age_maximal_dom'] = age_maximal_dom = cf.pop('age_maximal')
    cf['age_minimal_dom'] = age_minimal_dom = cf.pop('age_minimal')
    complement_familial_en_de_la_bmaf_dom = cf['complement_familial_en_de_la_bmaf_dom']
    cf['taux_base_dom'] = taux_base_dom = complement_familial_en_de_la_bmaf_dom.pop('montant_de_base')
    cf['taux_majore_dom'] = taux_majore_dom = complement_familial_en_de_la_bmaf_dom.pop('montant_majore')
    cf['nombre_enfant_minimum_dom'] = nombre_enfant_minimum_dom = cf.pop('nombre_d_enfant_minimum')
    cf['age_en_dessous_duquel_l_enfant_prive_la_famille_du_cf_dom'] = age_en_dessous_duquel_l_enfant_prive_la_famille_du_cf_dom = cf.pop('age_en_dessous_duquel_l_enfant_prive_la_famille_du_complement_familiale')

    # ape
    prestations_familiales['ape'] = ape = dict()
    prestations_familiales['ape'] = ape = prestations.pop('ape')
    ape = prestations_familiales['ape']
    ape['age_max_enfant'] = age_max_enfant = ape.pop('age_maximal_de_l_enfant_1')
    montant_mensuel_en_de_la_base_de_calcul = ape['montant_mensuel_en_de_la_base_de_calcul']
    ape['taux_activite_sup_50'] = taux_activite_sup_50 = montant_mensuel_en_de_la_base_de_calcul.pop(
        'pour_une_activite_de_plus_de_85h_mois_50_duree_legale')
    ape['taux_activite_sup_80'] = taux_activite_sup_80 = montant_mensuel_en_de_la_base_de_calcul.pop(
        'pour_une_activite_ou_formation_comprise_entre_50_et_80_de_la_duree_legale')
    ape['taux_inactivite'] = taux_inactivite = montant_mensuel_en_de_la_base_de_calcul.pop('a_taux_plein')
    # apje
    prestations_familiales['apje'] = apje = dict()
    prestations_familiales['apje'].update(prestations.pop('apje_cm'))
    prestations_familiales['apje'].update(prestations.pop('apje_plaf'))
    apje = prestations_familiales['apje']
    apje['age_max_dernier_enf'] = age_max_dernier_enf = apje.pop('age_limite_des_enfants_ouvrant_droit_a_l_apje_2')
    majoration_en_ou_en_en_du_plafond_de_ressources_avec_0_enfant = apje[
        'majoration_en_ou_en_en_du_plafond_de_ressources_avec_0_enfant']
    apje['taux_enfant_1_et_2'] = taux_enfant_1_et_2 = majoration_en_ou_en_en_du_plafond_de_ressources_avec_0_enfant.pop('1er_et_2eme_enfant')
    apje['taux_enfant_3_et_plus'] = taux_enfant_3_et_plus = majoration_en_ou_en_en_du_plafond_de_ressources_avec_0_enfant.pop('3eme_enfant_et_plus')
    apje['taux'] = taux = apje.pop('montant_de_l_apje_en_de_la_bmaf')

    del prestations['paje_cm2']['conditions_pour_qu_un_enfant_adopte_ouvre_droit_a_la_prime_a_son_arrivee']
    prestations_familiales['paje'] = paje = dict()
    paje['clmg'] = clmg = dict()
    paje.update(prestations.pop('paje_cm'))
    paje.update(prestations.pop('paje_cm2'))
    paje.update(prestations.pop('plaf_cmg'))
    paje.update(prestations.pop('paje_clca'))
    paje.update(prestations.pop('paje_prepare'))
    paje['paje_plaf'] = paje_plaf = prestations.pop('paje_plaf')
    paje['clmg'].update(prestations.pop('paje_cmg'))
    paje['base'] = base = dict()
    paje['clca'] = clca = dict()
    paje['colca'] = colca = dict()
    paje['prime_naissance'] = prime_naissance = dict()
    base = paje['base']
    clca = paje['clca']
    clmg = paje['clmg']
    colca = paje['colca']
    prime_naissance = paje['prime_naissance']
    paje['base'].update(paje.pop('paje'))
    base['taux_allocation_base'] = base.pop('allocation_de_base_en_de_la_bmaf')
    paje['clca'].update(paje.pop(
        'complement_de_libre_choix_d_activite_clca_pour_les_beneficiaires_de_l_allocation_de_base_enfant_ne_ou_adopte_apres_avril_2014'))
    clca['avecab_tx_inactif'] = clca.pop('taux_plein')
    clca['avecab_tx_partiel2'] = clca.pop('taux_partiel_entre_50_et_80')
    clca['avecab_tx_partiel1'] = clca.pop('taux_partiel_50')
    paje['clca'].update(
        paje.pop(
            'complement_de_libre_choix_d_activite_clca_pour_les_non_beneficiaires_de_l_allocation_de_base_enfant_ne_ou_adopte_avant_avril_2014'))
    clca['sansab_tx_inactif'] = clca.pop('taux_plein')
    clca['sansab_tx_partiel1'] = clca.pop('taux_partiel_50')
    clca['sansab_tx_partiel2'] = clca.pop('taux_partiel_entre_50_et_80')

    base['avant_2014'] = avant_2014 = dict()
    avant_2014 = base['avant_2014']
    avant_2014['plafond_ressources_0_enf'] = paje_plaf \
        .pop('premier_plafond_ne_ou_adopte_avant_le_1er_avril_2014') \
        .pop('plafond_de_ressources_0_enfant')
    paje_plaf.update(paje_plaf.pop('majoration_en_ou_en_du_plafond_de_ressources_avec_0_enfant'))
    avant_2014['majoration_biact_parent_isoles'] = paje_plaf.pop('biactifs_et_parents_isoles_1')
    avant_2014['taux_majoration_2_premiers_enf'] = paje_plaf.pop('1er_et_2eme_enfant')
    avant_2014['taux_majoration_3eme_enf_et_plus'] = paje_plaf.pop('3eme_enfant_et_plus')
    paje['clmg'].update(clmg.pop('complement_libre_choix_du_mode_de_garde_en_de_la_bmaf_1'))
    clmg['taux_recours_emploi_1er_plafond'] = clmg.pop('revenus_inferieurs_a_45_du_plafond_d_allocation')
    clmg['taux_recours_emploi_2e_plafond'] = clmg.pop('revenus_superieurs_a_45_du_plafond_d_allocation')
    clmg['taux_recours_emploi_supp_2e_plafond'] = clmg.pop('revenus_superieurs_au_plafond_d_allocation')

    # plaf_cmg
    premier_plafond_ne_ou_adopte_avant_le_1er_avril_2014 = paje['premier_plafond_ne_ou_adopte_avant_le_1er_avril_2014']
    deuxieme_plafond_ne_ou_adopte_avant_le_1er_avril_2014 = paje[
        'deuxieme_plafond_ne_ou_adopte_avant_le_1er_avril_2014']
    clmg['seuil11'] = premier_plafond_ne_ou_adopte_avant_le_1er_avril_2014.pop('un_enfant')
    clmg['seuil12'] = premier_plafond_ne_ou_adopte_avant_le_1er_avril_2014.pop('deux_enfants')
    clmg['seuil1sup'] = premier_plafond_ne_ou_adopte_avant_le_1er_avril_2014.pop(
        'majoration_pour_un_enfant_supplementaire')
    clmg['seuil21'] = deuxieme_plafond_ne_ou_adopte_avant_le_1er_avril_2014.pop('un_enfant')
    clmg['seuil22'] = deuxieme_plafond_ne_ou_adopte_avant_le_1er_avril_2014.pop('deux_enfants')
    clmg['seuil2sup'] = deuxieme_plafond_ne_ou_adopte_avant_le_1er_avril_2014.pop(
        'majoration_pour_un_enfant_supplementaire')
    # cmg taux
    taux_pour_recours_a_une_assistante_maternelle_une_association_une_entreprise_ou_une_microcreche_en_de_la_bmaf = clmg['taux_pour_recours_a_une_assistante_maternelle_une_association_une_entreprise_ou_une_microcreche_en_de_la_bmaf']
    taux_pour_recours_a_une_garde_a_domicile_en_de_la_bmaf = clmg[
        'taux_pour_recours_a_une_garde_a_domicile_en_de_la_bmaf']
    clmg['ass_mat1'] = taux_pour_recours_a_une_assistante_maternelle_une_association_une_entreprise_ou_une_microcreche_en_de_la_bmaf.pop('sous_le_premier_plafond')
    clmg['ass_mat2'] = taux_pour_recours_a_une_assistante_maternelle_une_association_une_entreprise_ou_une_microcreche_en_de_la_bmaf.pop('sous_le_second_plafond')
    clmg['ass_mat3'] = taux_pour_recours_a_une_assistante_maternelle_une_association_une_entreprise_ou_une_microcreche_en_de_la_bmaf.pop('apres_le_second_plafond')
    clmg['domi1'] = taux_pour_recours_a_une_garde_a_domicile_en_de_la_bmaf.pop('sous_le_premier_plafond')
    clmg['domi2'] = taux_pour_recours_a_une_garde_a_domicile_en_de_la_bmaf.pop('sous_le_second_plafond')
    clmg['domi3'] = taux_pour_recours_a_une_garde_a_domicile_en_de_la_bmaf.pop('apres_le_second_plafond')
    # colca
    complement_optionnel_de_libre_choix_d_activite = paje.pop('complement_optionnel_de_libre_choix_d_activite')
    colca['avecab'] = complement_optionnel_de_libre_choix_d_activite.pop('taux_plein_duree_de_l_arret_predeterminee')

    base['age_max_enfant'] = paje['age_limite_de_l_enfant_adopte_ou_non']
    clca['age_max_enfant'] = paje.pop('age_limite_de_l_enfant_adopte_ou_non')
    base['apres_2014'] = apres_2014 = dict()
    apres_2014['plaf_tx_par_enf'] = paje.pop('majoration_du_plafond_par_enfant_a_charge')
    paje['prime_naissance'] = prime_naissance = dict()
    montant_en_de_la_bmaf = paje['montant_en_de_la_bmaf']
    prime_naissance['prime_tx'] = montant_en_de_la_bmaf.pop('prime_a_la_naissance_de_la_paje_1')

    #autres
    def_pac = prestations['def_pac']
    af['seuil_rev_taux'] = def_pac.pop('revenu_plafond_pour_les_personnes_a_charge_n_etant_plus_sous_l_obligation_scolaire_en_du_smic_2')
    bmaf = prestations['bmaf']
    af['bmaf_ipp'] = bmaf_ipp =prestations.pop('bmaf')
    af['bmaf'] = bmaf_ipp.pop('base_mensuelle_de_calcul_des_allocations_familiales_bmaf')
    af['taux'] = taux = dict()
    taux['enf2'] = af.pop('2_enfants')

    prestations['minima_sociaux'] = minima_sociaux = dict()
    minima_sociaux['ada'] = ada = dict()
    minima_sociaux['ada'].update(prestations.pop('ada'))
    ada['majoration_pers_supp'] = majoration_pers_supp = ada.pop(
        'majoration_par_personne_supplementaire_maximum_10_par_famille')
    ada['supplement_non_hebergement'] = supplement_non_hebergement = ada.pop(
        'supplement_si_non_heberge_dans_centres_d_accueil_ou_hebergement_d_urgence')

    del prestations['asi_cond']['condition_d_age_et_de_ressources']
    del prestations['asi_cond']['age_minimal']
    minima_sociaux['asi'] = prestations.pop('asi_cond')
    minima_sociaux['asi'].update(prestations.pop('asi_m_plaf'))
    asi = minima_sociaux['asi']
    montant = asi['montant']
    plafond_de_ressources = asi['plafond_de_ressources']
    asi['plafond_ressource_seul'] = plafond_ressource_seul = plafond_de_ressources.pop('personnes_seules')
    asi['plafond_ressource_couple'] = plafond_ressource_couple = plafond_de_ressources.pop('couples')
    asi['montant_seul'] = montant_seul = montant.pop('1_allocataire')
    asi['montant_couple'] = montant_couple = montant.pop('2_allocataires')

    prestations_familiales['asf'] = prestations.pop('asf')
    asf = prestations_familiales['asf']
    montant_de_l_asf_en_de_la_bmaf = asf['montant_de_l_asf_en_de_la_bmaf']
    asf['taux_1_parent'] = taux_1_parent = montant_de_l_asf_en_de_la_bmaf.pop('orphelin_ou_assimile_d_un_seul_parent')
    asf['taux_2_parents'] = taux_2_parents = montant_de_l_asf_en_de_la_bmaf.pop('orphelin_ou_assimile_des_deux_parents')

    minima_sociaux['rmi'] = rmi = dict()
    rmi = minima_sociaux['rmi']
    minima_sociaux['rmi'].update(prestations.pop('rmi_cond'))
    minima_sociaux['rmi'].update(prestations.pop('rmi_fl'))
    minima_sociaux['rmi'].update(prestations.pop('rmi_m'))
    minima_sociaux['rmi'].update(prestations.pop('rmi_maj'))


    minima_sociaux['rsa'] = rsa = dict()
    rsa = minima_sociaux['rsa']
    minima_sociaux['rsa'].update(prestations.pop('rsa_m'))
    minima_sociaux['rsa'].update(prestations.pop('rsa_maj'))
    minima_sociaux['rsa'].update(prestations.pop('rsa_fl'))
    minima_sociaux['rsa'].update(prestations.pop('rsa_cond'))
    rsa['duree_min_titre_sejour'] = duree_min_titre_sejour = rsa.pop('duree_minimum_du_titre_de_sejour_annee')
    rsa['majoration_parent_isole'] = majoration_parent_isole = rsa.pop('majoration_pour_isolement_en_mois')
    majoration_parent_isole = rsa['majoration_parent_isole']
    majoration_parent_isole['age_limite_enfant'] = age_limite_enfant = majoration_parent_isole.pop(
        'age_limite_de_l_enfant_3_en_annee')
    rsa['majoration_rsa'] = majoration_rsa = rsa.pop('majoration_montant_maximal_en_de_la_base_rsa')
    majoration_rsa['taux_deuxieme_personne'] = taux_deuxieme_personne = majoration_rsa.pop(
        'couples_ou_celibataire_avec_un_enfant')
    majoration_rsa['taux_troisieme_personne'] = taux_troisieme_personne = majoration_rsa.pop(
        'couple_1_enfant_ou_pour_le_deuxieme_enfant_1')
    majoration_rsa['taux_personne_supp'] = taux_personne_supp = majoration_rsa.pop('par_enfant_supplementaire')
    rsa['forfait_logement'] = forfait_logement = rsa.pop('forfait_logement_en_du_montant_forfaitaire_du_rsa')
    forfait_logement = rsa['forfait_logement']
    forfait_logement['taux_1_personne'] = taux_1_personne = forfait_logement.pop('1_personne')
    forfait_logement['taux_2_personnes'] = taux_2_personnes = forfait_logement.pop('2_personnes')
    forfait_logement['taux_3_personnes_ou_plus'] = taux_3_personnes_ou_plus = forfait_logement.pop(
        '3_personnes_ou_plus')

    minima_sociaux['api'] = api = dict()
    minima_sociaux['api'].update(prestations.pop('api_cond'))
    minima_sociaux['api'].update(prestations.pop('api_m'))
    api = minima_sociaux['api']
    api['age_limite'] = age_limite = api.pop('age_limite_de_l_enfant_en_annee_2')
    montant_en_de_la_bmaf = api['montant_en_de_la_bmaf']
    minima_sociaux['api'].update(api.pop('montant_en_de_la_bmaf'))

    minima_sociaux['ppa'] = ppa = dict()
    ppa = minima_sociaux['ppa']
    minima_sociaux['ppa'].update(prestations.pop('pa_fl'))
    minima_sociaux['ppa'].update(prestations.pop('pa_m'))
    ppa['pente'] = pente = ppa.pop('majoration_des_ressources_sur_les_revenus_d_activite')
    majoration_isolement_en_de_la_base_rsa = ppa['majoration_isolement_en_de_la_base_rsa']
    ppa['majoration_isolement_femme_enceinte'] = majoration_isolement_femme_enceinte = majoration_isolement_en_de_la_base_rsa.pop(
        'femmes_enceintes')
    ppa['majoration_isolement_enf_charge'] = majoration_isolement_enf_charge = majoration_isolement_en_de_la_base_rsa.pop(
        'par_enfant_a_charge')
    bonification = ppa['bonification']
    bonification['seuil_bonification'] = seuil_bonification = bonification.pop(
        'seuil_de_salaire_minimum_pour_beneficier_de_la_bonification_en_multiple_du_smic_horaire_brut')
    bonification['seuil_max_bonification'] = seuil_max_bonification = bonification.pop(
        'seuil_de_salaire_pour_beneficier_de_la_bonification_maximale_en_multiple_du_smic_horaire_brut')
    bonification['taux_bonification_max'] = taux_bonification_max = bonification.pop(
        'montant_maximal_de_la_bonification_en_de_la_base_rsa')
    ppa['seuil_non_versement'] = seuil_non_versement = ppa.pop('montant_minimum_verse')
    minima_sociaux['ppa'].update(ppa.pop('majoration_montant_maximal_en_de_la_base_rsa'))
    ppa['taux_deuxieme_personne'] = taux_deuxieme_personne = ppa.pop('couples_ou_seul_avec_un_enfant')
    ppa['taux_troisieme_personne'] = taux_troisieme_personne = ppa.pop('couple_1_enfant_ou_pour_le_deuxieme_enfant_1')
    ppa['taux_personne_supp'] = taux_personne_supp = ppa.pop('par_enfant_supplementaire')

    minima_sociaux['aah'] = aah = dict()
    aah = minima_sociaux['aah']
    minima_sociaux['aah'].update(prestations.pop('aah'))
    aah['tx_plaf_supp'] = tx_plaf_supp = aah.pop('majoration_par_enfant_supplementaire')

    minima_sociaux['caah'] = caah = dict()
    caah = minima_sociaux['caah']
    minima_sociaux['caah'].update(prestations.pop('caah'))
    caah['garantie_ressources'] = garantie_ressources = caah.pop(
        'montant_mensuel_de_la_garantie_de_ressources_pour_les_personnes_handicapees')
    caah['majoration_vie_autonome'] = majoration_vie_autonome = caah.pop('majoration_pour_la_vie_autonome')
    caah['montant_complement_ressources'] = montant_complement_ressources = caah.pop(
        'montant_mensuel_du_complement_de_ressources_aux_adultes_handicapes_1')

    # Aefa
    minima_sociaux['aefa'] = prestations.pop('aefa')
    aefa = minima_sociaux['aefa']
    aefa['mon_seul'] = aefa.pop('montant_de_la_prime')
    taux_de_majoration_selon_la_taille_du_foyer_1 = aefa['taux_de_majoration_selon_la_taille_du_foyer_1']
    aefa['tx_2p'] = taux_de_majoration_selon_la_taille_du_foyer_1.pop('deux_personnes')
    aefa['tx_3pac'] = taux_de_majoration_selon_la_taille_du_foyer_1.pop(
        'taux_au_dela_de_la_troisieme_personne_a_charge_incluse')
    aefa['tx_supp'] = taux_de_majoration_selon_la_taille_du_foyer_1.pop('personne_supplementaire_si_conjoint')

    #   cf_maj:
    #     Majoration:
    #        1er et 2ème enfants (en % du plafond de ressources avec 0 enfant): null  # Value must be a float
    #        3ème enfant et plus (en % du plafond de ressources avec 0 enfant): null  # Value must be a float
    #        Biactifs et parents isolés:
    #     Plafond de ressources _ 0 enfant: null  # Value must be a float
    #   paje_cm:

    del prestations['pjm_prets']
    #   pjm_prets:
    #     cumul_de_prets: null  # Value must be a float
    #     pret_maximum:
    #       pour_l_accession_a_la_propriete_d_un_logement_neuf_ou_ancien: null  # Value must be a float
    #       pour_l_equipement_mobilier_et_menager: null  # Value must be a float
    #       pour_les_premiers_frais_de_location: null  # Value must be a float

    del root['baremes_ipp_retraites_pensions']

    minima_sociaux['aspa'] = aspa = dict()
    minima_sociaux['aspa'].update(prestations.pop('aspa'))
    aspa = minima_sociaux['aspa']
    minima_sociaux['aspa'].update(aspa.pop('montant_maximum_annuel'))
    aspa['montant_annuel_couple'] = montant_annuel_couple = aspa.pop(
        'couple_ou_lorsqu_un_seul_conjoint_est_beneficiaire_de_l_aspa_et_l_autre_de_l_allocation_supplementaire_d_invalidite')
    aspa['montant_annuel_seul'] = montant_annuel_seul = aspa.pop(
        'personnes_seules_ou_lorsque_un_seul_des_conjoints_beneficie_de_l_aspa')
    minima_sociaux['aspa'].update(aspa.pop('plafond_de_ressources'))
    aspa['plafond_ressources_couple'] = plafond_ressources_couple = aspa.pop('couples')
    # aspa['plafond_ressources_seul'] = plafond_ressources_seul = aspa.pop('personnes_seules') TODO: modifier aspa.py pour que ça passe en 2005 avec le merge

    # root['retraites'] = root.pop('baremes_ipp_retraites_pensions')
    # baremes_ipp_retraites_pensions:
    #   RENAME: retraite
    #   aad_fp:
    #     age_d_annulation_de_la_decote_selon_l_annee_d_ouverture_des_droits: null  # Value must be a float
    #   aad_rg:
    #     age_d_annulation_de_la_decote_en_fonction_de_la_date_de_naissance: null  # Value must be a float
    #   aod_fp_a:
    #     age_d_ouverture_des_droits_pour_la_fonction_publique_active_selon_l_annee_de_naissance:
    #       null  # Value must be a float
    #   aod_fp_s:
    #     age_d_ouverture_des_droits_pour_la_fonction_publique_sedentaire_selon_l_annee_de_naissance:
    #       null  # Value must be a float
    #   aod_rg:
    #     age_d_ouverture_des_droits_ou_age_legal_en_fonction_de_la_date_de_naissance: null  # Value must be a float
    #   as:
    #     plafond_de_ressources_menages: null  # Value must be a float
    #   la_fp_a:
    #     age_limite_fonction_publique_active_selon_l_annee_de_naissance: null  # Value must be a float
    #   la_fp_s:
    #     age_limite_fonction_publique_sedentaire_selon_l_annee_de_naissance: null  # Value must be a float
    #   salval:
    #     salaire_validant_un_trimestre:
    #       metropole: null  # Value must be a float

    root['taxation_capital'] = taxation_capital = root.pop('baremes_ipp_taxation_capital')
    taxation_capital['isf'] = isf = taxation_capital.pop('bareme_isf')
    seuils_des_tranches_du_bareme_de_l_isf = isf['seuils_des_tranches_du_bareme_de_l_isf']
    taux_marginaux_des_tranches_du_bareme_de_l_isf = isf['taux_marginaux_des_tranches_du_bareme_de_l_isf']
    isf['seuils_des_tranches_du_bareme_de_l_isf'] = tax_scale(
        bases_tree = isf.pop('seuils_des_tranches_du_bareme_de_l_isf'),
        rates_tree = isf.pop('taux_marginaux_des_tranches_du_bareme_de_l_isf'),
        )

    isf['bareme'] = bareme = isf.pop('seuils_des_tranches_du_bareme_de_l_isf')
    isf['decote'] = decote = taxation_capital.pop('decote')
    decote = isf['decote']
    decote['isf_taux_decote'] = isf_taux_decote = decote.pop('taux_de_la_decote_isf')
    decote['isf_base_decote'] = isf_base_decote = decote.pop('parametre_de_calcul_de_la_decote_isf')
    decote['isf_borne_sup_decote'] = isf_borne_sup_decote = decote.pop('borne_superieure_de_la_decote')
    decote['isf_borne_min_decote'] = isf_borne_min_decote = decote.pop('borne_inferieure_de_la_decote')

    taxation_capital['isf'].update(taxation_capital.pop('plaf'))
    taxation_capital['isf'].update(taxation_capital.pop('reduc_exo'))
    taxation_capital['isf'].update(taxation_capital.pop('isf_reduc_impot'))
    isf['reduc_invest_don'] = reduc_invest_don = isf.pop('reduction_pour_investissements_au_capital_de_pme')
    reduc_invest_don = isf['reduc_invest_don']
    reduc_invest_don['plafond_invest_pme'] = plafond_invest_pme = reduc_invest_don.pop(
        'plafond_pour_investissement_dans_les_pme')
    reduc_invest_don['taux_invest_direct_soc_holding'] = taux_invest_direct_soc_holding = reduc_invest_don.pop(
        'taux_pour_investissement_direct_soc_holdings_fip_fcpi')
    isf['reduc_invest_don'].update(isf.pop('reduction_pour_dons_a_certains_organismes_d_interet_general'))
    reduc_invest_don['taux_don_interet_general'] = taux_don_interet_general = reduc_invest_don.pop(
        'taux_pour_dons_a_certains_organismes_d_interet_general')
    isf['reduc_pac'] = reduc_pac = dict()
    reduc_pac = isf['reduc_pac']
    reduc_pac['reduc_enf_garde'] = reduc_enf_garde = isf.pop('reduction_isf_enfant_a_charge')
    isf['res_princ'] = res_princ = dict()
    res_princ = isf['res_princ']
    res_princ['abattement_sur_residence_principale'] = abattement_sur_residence_principale = isf.pop(
        'abattement_sur_residence_principale')
    #
    taxation_capital['prelevements_sociaux'] = prelevements_sociaux = taxation_capital.pop('ps')
    prelevements_sociaux['caps'] = caps = {}
    caps['produits_de_placement'] = prelevements_sociaux.pop('caps_sur_les_produits_de_placement')
    caps['revenus_du_patrimoine'] = prelevements_sociaux.pop('caps_sur_les_revenus_du_patrimoine')
    caps['rsa'] = prelevements_sociaux.pop('caps_rsa')
    prelevements_sociaux['prelevement_social'] = prelevement_social = {}
    prelevement_social['produits_de_placement'] = prelevements_sociaux.pop(
        'prelevement_social_sur_les_produits_de_placement')
    prelevement_social['revenus_du_patrimoine'] = prelevements_sociaux.pop(
        'prelevement_social_sur_les_revenus_du_patrimoine')
    prelevements_sociaux['prelevements_solidarite'] = prelevements_solidarite = {}
    prelevements_solidarite['produits_de_placement'] = prelevements_sociaux.pop(
        'prelevements_de_solidarite_sur_les_produits_de_placement')
    prelevements_solidarite['revenus_du_patrimoine'] = prelevements_sociaux.pop(
        'prelevements_de_solidarite_sur_les_revenus_du_patrimoine')
    #
    taxation_capital['prelevements_sociaux'].update(taxation_capital.pop('csg'))

    del root['baremes_ipp_taxation_indirecte']
    del root['baremes_ipp_autonomie_autonomy']
