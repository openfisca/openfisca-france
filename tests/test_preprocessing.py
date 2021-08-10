"""Teste les cotisations par catégorie de salarié produites à l'issue de l'étape preprocessing."""

from collections import OrderedDict
from .cache import tax_benefit_system


cotisations_salarie_by_name = {
    "agff": {
        "start_non_null_date": "2001-04-01",
        #"final_null_date": "2019-01-01", #TODO: update parameter from bareme IPP
        #https://framagit.org/french-tax-and-benefit-tables/baremes-ipp-yaml/-/blob/master/parameters/prelevements_sociaux/regimes_complementaires_retraite_secteur_prive/agff.yaml
    },
    "agirc_arrco": {
        "start_non_null_date": "2019-01-01",
    },
    "agirc": {
        "start_non_null_date": "1948-01-01",
        "final_null_date": "2019-01-01",
    },
    "apec": {
        "start_non_null_date": "1971-01-01",
    },
    "arrco": {
        "start_non_null_date": "1962-01-01",
        #"final_null_date": "2019-01-01", #TODO: update parameter from bareme IPP
        #https://framagit.org/french-tax-and-benefit-tables/baremes-ipp-yaml/-/blob/master/parameters/prelevements_sociaux/regimes_complementaires_retraite_secteur_prive/arrco.yaml
    },
    "assedic": {}, #TODO: add dates
    "ceg": {
        "start_non_null_date": "2019-01-01",
    },
    "cet": {
        "start_non_null_date": "1997-01-01",
        "final_null_date": "2019-01-01",
    },
    "cet2019": {
        "start_non_null_date": "2019-01-01",
    },
    "cnracl1": {
        "start_non_null_date": "1984-01-01",
        #"start_non_null_date": "1947-09-19", #TODO: update parameter from bareme IPP
        #https://framagit.org/french-tax-and-benefit-tables/baremes-ipp-yaml/-/blob/master/parameters/prelevements_sociaux/cotisations_secteur_public/cnracl.yaml
    },
    "cnracl2": {
        "start_non_null_date": "1984-01-01",
        #"start_non_null_date": "1947-09-19", #TODO: update parameter from bareme IPP
        #https://framagit.org/french-tax-and-benefit-tables/baremes-ipp-yaml/-/blob/master/parameters/prelevements_sociaux/cotisations_secteur_public/cnracl.yaml
    },
    "excep_solidarite": {}, #TODO: add dates
    "forfait_annuel": {}, #TODO: add dates; 2011 0 or null?
    "ircantec": {
        "start_non_null_date": "1971-01-01",
    },
    "maladie_alsace_moselle": {
        "start_non_null_date": "1989-09-01",
    },
    "maladie": {
        "start_non_null_date": "1993-07-01",
        #"start_non_null_date": "1967-10-01", #TODO: update parameter from bareme IPP
        #https://framagit.org/french-tax-and-benefit-tables/baremes-ipp-yaml/-/blob/master/parameters/prelevements_sociaux/cotisations_securite_sociale_ss_regime_general/mmid.yaml
        "final_null_date": "2018-01-01",
    },
    "pension": {}, #TODO: add dates
    "rafp": {
        "start_non_null_date": "2005-01-01"
    },
    "vieillesse_deplafonnee": {
        "start_non_null_date": "2004-07-01"
    },
    "vieillesse": {
        "start_non_null_date": "1993-07-01",
        #"start_non_null_date": "1967-10-01", #TODO: update parameter from bareme IPP
        #https://framagit.org/french-tax-and-benefit-tables/baremes-ipp-yaml/-/blob/master/parameters/prelevements_sociaux/cotisations_securite_sociale_ss_regime_general/cnav.yaml
    },
}


cotisations_salarie_by_categorie_salarie = {
    "prive_cadre": [
        "agff",
        "agirc_arrco",
        "agirc",
        "apec",
        "arrco",
        "assedic",
        "ceg",
        "cet",
        "cet2019",
        "forfait_annuel",
        "maladie_alsace_moselle",
        "maladie",
        "vieillesse_deplafonnee",
        "vieillesse",
        ],
    "prive_non_cadre": [
        "agff",
        "agirc_arrco",
        "arrco",
        "assedic",
        "ceg",
        "cet2019",
        "maladie_alsace_moselle",
        "maladie",
        "vieillesse_deplafonnee",
        "vieillesse",
        ],
    "public_non_titulaire": [
        "agirc_arrco",
        "ceg",
        "cet2019",
        "excep_solidarite",
        "ircantec",
        "maladie_alsace_moselle",
        "maladie",
        "vieillesse_deplafonnee",
        "vieillesse",
        ],
    "public_titulaire_etat": [
        "excep_solidarite",
        "pension",
        "rafp",
        ],
    "public_titulaire_hospitaliere": [
        "cnracl1",
        "cnracl2",
        "excep_solidarite",
        "rafp",
        ],
    "public_titulaire_territoriale": [
        "cnracl1",
        "cnracl2",
        "excep_solidarite",
        "rafp",
        ],
    }

cotisations_employeur_by_categorie_salarie = {
    "prive_cadre": [
        "agffc",
        "agirc_arrco",
        "agirc",
        "apec",
        "apprentissage_contribution_additionnelle", ###
        "apprentissage_taxe", ###
        "apprentissage_taxe_alsace_moselle", ###
        "arrco",
        "assedic",
        "ceg",
        "cet",
        "cet2019",
        "chomfg", ###
        "construction_plus_de_10_salaries", ###
        "construction_plus_de_20_salaries", ###
        "construction_plus_de_50_salaries", ###
        "contribution_moins_de_20_salaries", ###
        "contribution_moins_de_50_salaries", ###
        "contribution_plus_de_10_salaries", ###
        "contribution_plus_de_20_salaries", ###
        "contribution_plus_de_50_salaries", ###
        "cotisation", ###
        "csa", ###
        "famille", ###
        "financement_organisations_syndicales", ###
        "fnal_cont_moins_de_20_salaries", ###
        "fnal_cont_moins_de_50_salaries", ###
        "fnal_cont_plus_de_10_salaries", ###
        "fnal_cont_plus_de_20_salaries", ###
        "fnal_cont_plus_de_50_salaries", ###
        "fnal_cotisation", ###
        "forfait_annuel",
        "formprof_11_salaries_et_plus", ###
        "formprof_20_salaries_et_plus", ###
        "formprof_entre_10_et_19_salaries", ###
        "formprof_moins_de_10_salaries", ###
        "formprof_moins_de_11_salaries", ###
        "maladie",
        "penibilite_additionnelle", ###
        "penibilite_base", ###
        "penibilite_multiplicateur_exposition_multiple", ###
        "vieillesse_deplafonnee",
        "vieillesse_plafonnee", ###
        ],
    "prive_non_cadre": [
        "agffnc", ###
        "agirc_arrco",
        "apprentissage_contribution_additionnelle", 
        "apprentissage_taxe", 
        "apprentissage_taxe_alsace_moselle", 
        "arrco",
        "assedic",
        "ceg",
        "cet2019",
        "chomfg",
        "construction_plus_de_10_salaries", 
        "construction_plus_de_20_salaries", 
        "construction_plus_de_50_salaries", 
        "contribution_moins_de_20_salaries", 
        "contribution_moins_de_50_salaries", 
        "contribution_plus_de_10_salaries", 
        "contribution_plus_de_20_salaries", 
        "contribution_plus_de_50_salaries", 
        "cotisation", 
        "csa", 
        "famille", 
        "financement_organisations_syndicales", 
        "fnal_cont_moins_de_20_salaries", 
        "fnal_cont_moins_de_50_salaries", 
        "fnal_cont_plus_de_10_salaries", 
        "fnal_cont_plus_de_20_salaries", 
        "fnal_cont_plus_de_50_salaries", 
        "fnal_cotisation", 
        "formprof_11_salaries_et_plus", 
        "formprof_20_salaries_et_plus", 
        "formprof_entre_10_et_19_salaries", 
        "formprof_moins_de_10_salaries", 
        "formprof_moins_de_11_salaries", 
        "maladie",
        "penibilite_additionnelle", 
        "penibilite_base", 
        "penibilite_multiplicateur_exposition_multiple", 
        "vieillesse_deplafonnee",
        "vieillesse_plafonnee", 
        ],
    "public_non_titulaire": [
        "agirc_arrco",
        "ceg",
        "cet2019",
        "contribution_moins_de_20_salaries", 
        "contribution_moins_de_50_salaries", 
        "contribution_plus_de_10_salaries", 
        "contribution_plus_de_20_salaries", 
        "contribution_plus_de_50_salaries",
        "cotisation" ,
        "csa",
        "famille",
        "financement_organisations_syndicales", 
        "fnal_cont_moins_de_20_salaries", 
        "fnal_cont_moins_de_50_salaries", 
        "fnal_cont_plus_de_10_salaries", 
        "fnal_cont_plus_de_20_salaries", 
        "fnal_cont_plus_de_50_salaries", 
        "fnal_cotisation", 
        "ircantec",
        "maladie",
        "penibilite_additionnelle", 
        "penibilite_base", 
        "penibilite_multiplicateur_exposition_multiple", 
        "vieillesse_deplafonnee",
        "vieillesse_plafonnee",
        ],
    "public_titulaire_etat": [
        "agirc_arrco",
        "ati", ###
        "ceg",
        "cet2019",
        "contribution_moins_de_20_salaries", 
        "contribution_moins_de_50_salaries", 
        "contribution_plus_de_10_salaries", 
        "contribution_plus_de_20_salaries", 
        "contribution_plus_de_50_salaries",
        "cotisation" ,
        "csa",
        "famille",
        "financement_organisations_syndicales", 
        "fnal_cont_moins_de_20_salaries", 
        "fnal_cont_moins_de_50_salaries", 
        "fnal_cont_plus_de_10_salaries", 
        "fnal_cont_plus_de_20_salaries", 
        "fnal_cont_plus_de_50_salaries", 
        "fnal_cotisation", 
        "maladie",
        "penibilite_additionnelle", 
        "penibilite_base", 
        "penibilite_multiplicateur_exposition_multiple", 
        "pension",
        "rafp",
        ],
    "public_titulaire_hospitaliere": [
        "agirc_arrco",
        "atiacl", ###
        "ceg",
        "cet2019",
        "cnracl", ###
        "contribution_moins_de_20_salaries", 
        "contribution_moins_de_50_salaries", 
        "contribution_plus_de_10_salaries", 
        "contribution_plus_de_20_salaries", 
        "contribution_plus_de_50_salaries",
        "cotisation" ,
        "csa",
        "famille",
        "feh", ###
        "financement_organisations_syndicales", 
        "fnal_cont_moins_de_20_salaries", 
        "fnal_cont_moins_de_50_salaries", 
        "fnal_cont_plus_de_10_salaries", 
        "fnal_cont_plus_de_20_salaries", 
        "fnal_cont_plus_de_50_salaries", 
        "fnal_cotisation", 
        "maladie",
        "penibilite_additionnelle", 
        "penibilite_base", 
        "penibilite_multiplicateur_exposition_multiple", 
        "rafp",
        ],
    "public_titulaire_militaire": [
        "agirc_arrco",
        "ceg",
        "cet2019",
        "cnracl", ###
        "contribution_moins_de_20_salaries", 
        "contribution_moins_de_50_salaries", 
        "contribution_plus_de_10_salaries", 
        "contribution_plus_de_20_salaries", 
        "contribution_plus_de_50_salaries",
        "cotisation" ,
        "csa",
        "famille",
        "financement_organisations_syndicales", 
        "fnal_cont_moins_de_20_salaries", 
        "fnal_cont_moins_de_50_salaries", 
        "fnal_cont_plus_de_10_salaries", 
        "fnal_cont_plus_de_20_salaries", 
        "fnal_cont_plus_de_50_salaries", 
        "fnal_cotisation", 
        "maladie",
        "penibilite_additionnelle", 
        "penibilite_base", 
        "penibilite_multiplicateur_exposition_multiple",
        "pension",  
        "rafp",
        ],
    "public_titulaire_territoriale": [
        "agirc_arrco",
        "atiacl", 
        "ceg",
        "cet2019",
        "cnracl",
        "contribution_moins_de_20_salaries", 
        "contribution_moins_de_50_salaries", 
        "contribution_plus_de_10_salaries", 
        "contribution_plus_de_20_salaries", 
        "contribution_plus_de_50_salaries",
        "cotisation" ,
        "csa",
        "famille",
        "fcppa", ###
        "financement_organisations_syndicales", 
        "fnal_cont_moins_de_20_salaries", 
        "fnal_cont_moins_de_50_salaries", 
        "fnal_cont_plus_de_10_salaries", 
        "fnal_cont_plus_de_20_salaries", 
        "fnal_cont_plus_de_50_salaries", 
        "fnal_cotisation", 
        "maladie",
        "penibilite_additionnelle", 
        "penibilite_base", 
        "penibilite_multiplicateur_exposition_multiple",
        "rafp",
        ],
    }

def test_preprocessing():
    """Tests the result of parameters preprocessing."""
    parameters = tax_benefit_system.parameters
    assert set(parameters.cotsoc.cotisations_employeur.children.keys()) == set([
        'prive_cadre',
        'prive_non_cadre',
        'public_non_titulaire',
        'public_titulaire_etat',
        'public_titulaire_hospitaliere',
        'public_titulaire_militaire',
        'public_titulaire_territoriale',
        ]), "Les barèmes de cotisations employeur de certaines catégories de salariés sont manquants"

    assert set(parameters.cotsoc.cotisations_salarie.children.keys()) == set([
        'prive_cadre',
        'prive_non_cadre',
        'public_non_titulaire',
        'public_titulaire_etat',
        'public_titulaire_hospitaliere',
        # 'public_titulaire_militaire',  FIXME Il y en a sûrement mais pas actuellement
        'public_titulaire_territoriale',
        ]), "Les barèmes de cotisations salarié de certaines catégories instant_sde salariés sont manquants"

    categorie_salaries = [
        "prive_cadre",
        "prive_non_cadre",
        "public_non_titulaire",
        "public_titulaire_etat",
        "public_titulaire_hospitaliere",
        "public_titulaire_territoriale",
        ]

    for categorie_salarie in categorie_salaries:
        test = parameters.cotsoc.cotisations_salarie.children[categorie_salarie].children.keys()
        target = cotisations_salarie_by_categorie_salarie[categorie_salarie]
        assert set(test) == set(target), "Les barèmes de cotisations salarié {} ne sont pas les bons".format(
            categorie_salarie)

        test = parameters.cotsoc.cotisations_employeur.children[categorie_salarie].children.keys()
        target = cotisations_employeur_by_categorie_salarie[categorie_salarie]
        assert set(test) == set(target), "Les barèmes de cotisations employeur {} ne sont pas les bons".format(
            categorie_salarie)

    for categorie_salarie in categorie_salaries:
        cotisations_salaries = set(cotisations_salarie_by_categorie_salarie[categorie_salarie])
        for cotisation_salarie in sorted(cotisations_salaries):
            bareme = parameters.cotsoc.cotisations_salarie.children[categorie_salarie].children[cotisation_salarie]
            
            final_null_date = cotisations_salarie_by_name[cotisation_salarie].get("final_null_date")
            if final_null_date:
                thresholds = [
                    dict(
                        (parameter_at_instant.instant_str, parameter_at_instant.value)
                        for parameter_at_instant in bracket.threshold.values_list
                        )
                    for bracket in bareme.brackets
                    ]
                final_thresholds_by_instant_str = OrderedDict(sorted(threshold.items(), reverse = True)[0] for threshold in thresholds)
                assert all([final_threshold is None for final_threshold in final_thresholds_by_instant_str.values()]), "Barème salarié {} ne s'éteint pas (il devrait en {})".format(
                    cotisation_salarie,
                    final_null_date,
                    )
                assert max(final_thresholds_by_instant_str.keys()) == final_null_date, "Barème salarié {} ne s'éteint pas en {}".format(
                    cotisation_salarie,
                    final_null_date,
                    )

            start_non_null_date = cotisations_salarie_by_name[cotisation_salarie].get("start_non_null_date")
            if start_non_null_date:
                thresholds = [
                    dict(
                        (parameter_at_instant.instant_str, parameter_at_instant.value)
                        for parameter_at_instant in bracket.threshold.values_list
                        )
                    for bracket in bareme.brackets
                    ]
                start_thresholds_by_instant_str = OrderedDict(sorted(threshold.items())[0] for threshold in thresholds)
                assert all([start_threshold is not None for start_threshold in start_thresholds_by_instant_str.values()]), "Barème salarié {} ne commence pas à la bonne date (il devrait en {})".format(
                    cotisation_salarie,
                    start_non_null_date,
                    )
                assert min(start_thresholds_by_instant_str.keys()) == start_non_null_date, "Barème salarié {} ne commence pas en {}".format(
                    cotisation_salarie,
                    start_non_null_date,
                    )
