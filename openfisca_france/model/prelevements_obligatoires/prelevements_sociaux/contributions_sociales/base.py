

def montant_csg_crds(base_avec_abattement = None, base_sans_abattement = None, indicatrice_taux_plein = None,
        indicatrice_taux_intermediaire = None, indicatrice_taux_reduit = None, abattement_parameter = None, law_node = None, plafond_securite_sociale = None):
    assert law_node is not None
    assert plafond_securite_sociale is not None
    if base_sans_abattement is None:
        base_sans_abattement = 0
    if base_avec_abattement is None:
        base = base_sans_abattement
    else:
        assert abattement_parameter is not None
        base = base_avec_abattement - abattement_parameter.calc(
            base_avec_abattement,
            factor = plafond_securite_sociale,
            round_base_decimals = 2,
            ) + base_sans_abattement
    if indicatrice_taux_plein is None and indicatrice_taux_reduit is None and indicatrice_taux_intermediaire is None:
        return -law_node.taux * base
    elif indicatrice_taux_plein is not None and indicatrice_taux_reduit is not None and indicatrice_taux_intermediaire is None:
        return - (
            law_node.taux_plein * indicatrice_taux_plein
            + law_node.taux_reduit * indicatrice_taux_reduit
            ) * base
    else:
        assert indicatrice_taux_plein is not None
        assert indicatrice_taux_reduit is not None
        assert indicatrice_taux_intermediaire is not None
        return - (
            law_node.taux_plein * indicatrice_taux_plein
            + law_node.taux_reduit * indicatrice_taux_reduit
            + law_node.taux_median * indicatrice_taux_intermediaire
            ) * base
