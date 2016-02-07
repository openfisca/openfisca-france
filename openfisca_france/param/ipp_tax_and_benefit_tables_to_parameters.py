# -*- coding: utf-8 -*-


import collections
import datetime


def fixed_bases_tax_scale(base_by_slice_name, null_rate_base = None, rates_tree = None):
    first_start = UnboundLocalError
    last_stop = UnboundLocalError
    for bracket in rates_tree.itervalues():
        if isinstance(bracket, (float, int)):
            continue
        bracket_start = bracket[0]['start']
        if first_start is UnboundLocalError or bracket_start < first_start:
            first_start = bracket_start
        bracket_stop = bracket[-1].get('stop')
        if last_stop is UnboundLocalError or \
                last_stop is not None and (bracket_stop is None or last_stop < bracket_stop):
            last_stop = bracket_stop
    assert first_start is not UnboundLocalError
    assert last_stop is not UnboundLocalError

    # Convert constant brackets to real brackets.
    for slice_name, bracket in rates_tree.iteritems():
        if isinstance(bracket, (float, int)):
            rates_bracket_item = dict(
                start = first_start,
                value = str(bracket),
                )
            if last_stop is not None:
                rates_bracket_item['stop'] = last_stop
            rates_tree[slice_name] = [rates_bracket_item]

    if null_rate_base is not None:
        # Add null slice and add missing zero values in other slices.
        for bracket in rates_tree.itervalues():
            if first_start < bracket[0]['start']:
                bracket.insert(0, dict(
                    start = first_start,
                    stop = bracket[0]['start'] - datetime.timedelta(days = 1),
                    value = '0',
                    ))
            stop = bracket[-1].get('stop')
            if stop is not None and (last_stop is None or stop < last_stop):
                bracket_last_item = dict(
                    start = stop + datetime.timedelta(days = 1),
                    value = '0',
                    )
                if last_stop is not None:
                    bracket_last_item['stop'] = last_stop
                bracket.append(bracket_last_item)
            for item in bracket:
                if item['value'] is None:
                    item['value'] = '0'

        rates_bracket_null_item = dict(
            start = first_start,
            value = '0',
            )
        if last_stop is not None:
            rates_bracket_null_item['stop'] = last_stop
        rates_tree['tranche_nulle'] = [rates_bracket_null_item]

        base_by_slice_name = base_by_slice_name.copy()
        base_by_slice_name['tranche_nulle'] = null_rate_base

    # Generate bases_tree.
    bases_tree = collections.OrderedDict()
    for slice_name, rates_bracket in sorted(rates_tree.iteritems()):
        bases_bracket_item = dict(
            start = rates_bracket[0]['start'],
            value = str(base_by_slice_name[slice_name]),
            )
        stop = rates_bracket[-1].get('stop')
        if stop is not None:
            bases_bracket_item['stop'] = stop
        bases_tree[slice_name] = [bases_bracket_item]

    return dict(
        TYPE = 'BAREME',
        SEUIL = bases_tree,
        TAUX = rates_tree,
        )


def tax_scale(bases_tree, rates_tree = None):
    assert rates_tree is not None, 'TODO'
    return dict(
        TYPE = 'BAREME',
        SEUIL = bases_tree,
        TAUX = rates_tree,
        )


def transform_ipp_tree(root):
    del root['baremes_ipp_chomage_unemployment']
    # root['chomage'] = root.pop('baremes_ipp_chomage_unemployment')

    root['impot_revenu'] = impot_revenu = root.pop('baremes_ipp_impot_revenu_income_tax')
    #
    impot_revenu['tspr'] = tspr = impot_revenu.pop('deductions')
    tspr['abat_sal_pen'] = abat_sal_pen = tspr.pop('deduction_supplementaire')
    abat_sal_pen['max'] = abat_sal_pen.pop('abattement_maximal')
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
    cotisations_sociales['casa'] = casa = prelevements_sociaux.pop('casa')
    casa['pension'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_unique = 0,
            ),
        rates_tree = dict(
            tranche_unique = casa.pop('pensions_de_retraite_de_preretraite_et_d_invalidite'),
            )
        )
    #
    cotisations_sociales['cet'] = cet = prelevements_sociaux.pop('cet')
    tranche_c_salaire_sous_8_pss = cet.pop('tranche_c_salaire_sous_8_pss')
    cet['employeur'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_c = 0,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_c = tranche_c_salaire_sous_8_pss.pop('employeur'),
            )
        )
    cet['salarie'] = fixed_bases_tax_scale(
        base_by_slice_name = dict(
            tranche_c = 0,
            ),
        null_rate_base = 8,
        rates_tree = dict(
            tranche_c = tranche_c_salaire_sous_8_pss.pop('salarie'),
            )
        )
    assert not tranche_c_salaire_sous_8_pss
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
    # cice unchaged done
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
    # TODO CNRACL 
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
            tranche_a = 0,
            ),
        rates_tree = dict(
            tranche_a = sur_tout_salaire.pop('salaries'),
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
    #
    prelevements_sociaux['csg'] = csg = prelevements_sociaux.pop('csg_1')
    csg['activite'] = csg.pop('revenus_d_activite')
    csg['remplacement'] = prelevements_sociaux.pop('csg_2')
    #
    deces_ac = prelevements_sociaux['deces_ac']
    commercants_industriels = deces_ac['commercants_industriels']
    del commercants_industriels['deces']
    del commercants_industriels['invalidite']
    #
    fillon = prelevements_sociaux['fillon']
    # Deleted, because value must be a float.
    del fillon['ensemble_des_entreprises']['salaire_de_reference']
    del fillon['entreprises_restees_aux_39_heures_hebdomadaires_au_30_06_2003']['salaire_de_reference']
    del fillon['entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003']['salaire_de_reference']

    del root['baremes_ipp_prestations_sociales_social_benefits']
    # root['prestations'] = root.pop('baremes_ipp_prestations_sociales_social_benefits')
    # baremes_ipp_prestations_sociales_social_benefits:
    #   RENAME: prestations
    #   aa_plaf:
    #     Plafonds de ressources: null  # Value must be a float
    #   aes:
    #     Complément d'allocation:
    #       3e catégorie: null  # Changement d'unité de FRF à %
    #   al_charge:
    #     Cas des colocataires ou des propriétaires (1):
    #       Isolé ou couple avec un enfant ou une personne à charge: null  # Value must be a float
    #       Majoration par enfant de la majoration pour charges: null  # Value must be a float
    #   al_pac:
    #     Âge limite pour les enfants à charge: null  # Value must be a float
    #     Plafonds de ressources que les potentiels personnes à charge autre que les enfants doivent respecter:
    #       null  # Value must be a float
    #   al_plaf_acc:
    #     Intervalle de date du certificat d'emprunt correspondant aux plafonds d'accession à la propriété:
    #       null  # Value must be a float
    #   al_plaf_loc2:
    #     Loyer de référence: null  # Value must be a float
    #   api_fl:
    #     Forfait logement:
    #       Couple, 1 enfant (1): null  # Value must be a float
    #       couples_2_enfants_ou_plus_1: null  # Value must be a float
    #       Femmes enceintes (1): null  # Value must be a float
    #   asi_cond:
    #     Âge minimal: null  # Value must be a float
    #     Condition d'âge et de ressources: null  # Value must be a float
    #   cf_maj:
    #     Majoration:
    #        1er et 2ème enfants (en % du plafond de ressources avec 0 enfant): null  # Value must be a float
    #        3ème enfant et plus (en % du plafond de ressources avec 0 enfant): null  # Value must be a float
    #        Biactifs et parents isolés:
    #     Plafond de ressources _ 0 enfant: null  # Value must be a float
    #   paje_cm:
    #     age_limite:
    #       pour_les_enfants_adoptes: null  # Value must be a float
    #   paje_cm2:
    #     conditions_pour_qu_un_enfant_adopte_ouvre_droit_a_la_prime_a_son_arrivee: null  # Value must be a float
    #   pjm_prets:
    #     cumul_de_prets: null  # Value must be a float
    #     pret_maximum:
    #       pour_l_accession_a_la_propriete_d_un_logement_neuf_ou_ancien: null  # Value must be a float
    #       pour_l_equipement_mobilier_et_menager: null  # Value must be a float
    #       pour_les_premiers_frais_de_location: null  # Value must be a float

    del root['baremes_ipp_retraites_pensions']
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
    # root['taxation_indirecte'] = root.pop('baremes_ipp_taxation_indirecte')
