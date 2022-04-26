from openfisca_france.model.base import *


DEFAULT_ROUND_BASE_DECIMALS = 2

cotisations_employeur_by_categorie_salarie = {
    'prive_cadre': [
        'agffc',
        'agirc_arrco',
        'agirc',
        'ags',
        'apec',
        'apprentissage_contribution_additionnelle',
        'apprentissage_taxe',
        'apprentissage_taxe_alsace_moselle',
        'arrco',
        'asf',
        'ceg',
        'cet',
        'cet2019',
        'chomage',
        'construction_plus_de_10_salaries',
        'construction_plus_de_20_salaries',
        'construction_plus_de_50_salaries',
        'csa',
        'famille',
        'financement_organisations_syndicales',
        'fnal_contribution_moins_de_20_salaries',
        'fnal_contribution_moins_de_50_salaries',
        'fnal_contribution_plus_de_10_salaries',
        'fnal_contribution_plus_de_20_salaries',
        'fnal_contribution_plus_de_50_salaries',
        'fnal_cotisation',
        # "forfait_annuel",  # Antérieur à 2011, pas présent sous forme de barème
        'formprof_11_salaries_et_plus',
        'formprof_20_salaries_et_plus',
        'formprof_entre_10_et_19_salaries',
        'formprof_moins_de_10_salaries',
        'formprof_moins_de_11_salaries',
        'maladie',
        'penibilite_additionnelle',
        'penibilite_base',
        'penibilite_multiplicateur_exposition_multiple',
        'vieillesse_deplafonnee',
        'vieillesse_plafonnee',
        ],
    'prive_non_cadre': [
        'agffnc',
        'agirc_arrco',
        'ags',
        'apprentissage_contribution_additionnelle',
        'apprentissage_taxe_alsace_moselle',
        'apprentissage_taxe',
        'arrco',
        'asf',
        'ceg',
        'cet2019',
        'chomage',
        'construction_plus_de_10_salaries',
        'construction_plus_de_20_salaries',
        'construction_plus_de_50_salaries',
        'csa',
        'famille',
        'financement_organisations_syndicales',
        'fnal_contribution_moins_de_20_salaries',
        'fnal_contribution_moins_de_50_salaries',
        'fnal_contribution_plus_de_10_salaries',
        'fnal_contribution_plus_de_20_salaries',
        'fnal_contribution_plus_de_50_salaries',
        'fnal_cotisation',
        'formprof_11_salaries_et_plus',
        'formprof_20_salaries_et_plus',
        'formprof_entre_10_et_19_salaries',
        'formprof_moins_de_10_salaries',
        'formprof_moins_de_11_salaries',
        'maladie',
        'penibilite_additionnelle',
        'penibilite_base',
        'penibilite_multiplicateur_exposition_multiple',
        'vieillesse_deplafonnee',
        'vieillesse_plafonnee',
        ],
    'public_non_titulaire': [
        'csa',
        'famille',
        'financement_organisations_syndicales',
        'fnal_contribution_moins_de_20_salaries',
        'fnal_contribution_moins_de_50_salaries',
        'fnal_contribution_plus_de_10_salaries',
        'fnal_contribution_plus_de_20_salaries',
        'fnal_contribution_plus_de_50_salaries',
        'fnal_cotisation',
        'ircantec',
        'maladie',
        'penibilite_additionnelle',
        'penibilite_base',
        'penibilite_multiplicateur_exposition_multiple',
        'vieillesse_deplafonnee',
        'vieillesse_plafonnee',
        ],
    'public_titulaire_etat': [
        'ati',
        'csa',
        'famille',
        'financement_organisations_syndicales',
        'fnal_contribution_moins_de_20_salaries',
        'fnal_contribution_moins_de_50_salaries',
        'fnal_contribution_plus_de_10_salaries',
        'fnal_contribution_plus_de_20_salaries',
        'fnal_contribution_plus_de_50_salaries',
        'fnal_cotisation',
        'maladie',
        'penibilite_additionnelle',
        'penibilite_base',
        'penibilite_multiplicateur_exposition_multiple',
        'pension',
        'rafp',
        ],
    'public_titulaire_hospitaliere': [
        'atiacl',
        'cnracl',
        'csa',
        'famille',
        'feh',
        'financement_organisations_syndicales',
        'fnal_contribution_moins_de_20_salaries',
        'fnal_contribution_moins_de_50_salaries',
        'fnal_contribution_plus_de_10_salaries',
        'fnal_contribution_plus_de_20_salaries',
        'fnal_contribution_plus_de_50_salaries',
        'fnal_cotisation',
        'maladie',
        'penibilite_additionnelle',
        'penibilite_base',
        'penibilite_multiplicateur_exposition_multiple',
        'rafp',
        ],
    'public_titulaire_militaire': [
        'cnracl',
        'csa',
        'famille',
        'financement_organisations_syndicales',
        'fnal_contribution_moins_de_20_salaries',
        'fnal_contribution_moins_de_50_salaries',
        'fnal_contribution_plus_de_10_salaries',
        'fnal_contribution_plus_de_20_salaries',
        'fnal_contribution_plus_de_50_salaries',
        'fnal_cotisation',
        'maladie',
        'penibilite_additionnelle',
        'penibilite_base',
        'penibilite_multiplicateur_exposition_multiple',
        'pension',
        'rafp',
        ],
    'public_titulaire_territoriale': [
        'atiacl',
        'cnracl',
        'csa',
        'famille',
        'fcppa',
        'financement_organisations_syndicales',
        'fnal_contribution_moins_de_20_salaries',
        'fnal_contribution_moins_de_50_salaries',
        'fnal_contribution_plus_de_10_salaries',
        'fnal_contribution_plus_de_20_salaries',
        'fnal_contribution_plus_de_50_salaries',
        'fnal_cotisation',
        'maladie',
        'penibilite_additionnelle',
        'penibilite_base',
        'penibilite_multiplicateur_exposition_multiple',
        'rafp',
        ],
    }


cotisations_salarie_by_categorie_salarie = {
    'prive_cadre': [
        'agff',
        'agirc_arrco',
        'agirc',
        'apec',
        'arrco',
        'asf',
        'ceg',
        'cet',
        'cet2019',
        'chomage',
        # "forfait_annuel",  # Antérieur à 2011, pas présent sous forme de barème
        'maladie_alsace_moselle',
        'maladie',
        'vieillesse_deplafonnee',
        'vieillesse_plafonnee',
        ],
    'prive_non_cadre': [
        'agff',
        'agirc_arrco',
        'asf',
        'arrco',
        'ceg',
        'cet2019',
        'chomage',
        'maladie_alsace_moselle',
        'maladie',
        'vieillesse_deplafonnee',
        'vieillesse_plafonnee',
        ],
    'public_non_titulaire': [
        'excep_solidarite',
        'ircantec',
        'maladie_alsace_moselle',
        'maladie',
        'vieillesse_deplafonnee',
        'vieillesse_plafonnee',
        ],
    'public_titulaire_etat': [
        'excep_solidarite',
        'pension',
        'rafp',
        ],
    'public_titulaire_hospitaliere': [
        'cnracl_s_ti',
        'cnracl_s_nbi',
        'excep_solidarite',
        'rafp',
        ],
    'public_titulaire_territoriale': [
        'cnracl_s_ti',
        'cnracl_s_nbi',
        'excep_solidarite',
        'rafp',
        ],
    }


# TODO: Rename bareme_by_type_sal_name to bareme_by_categorie_salarie


def apply_bareme_for_relevant_type_sal(
        bareme_by_type_sal_name,
        bareme_name,
        categorie_salarie,
        base,
        plafond_securite_sociale,
        round_base_decimals = DEFAULT_ROUND_BASE_DECIMALS,
        ):
    '''Apply bareme corresponding to bareme_name to the relevant categorie_salarie.'''
    assert bareme_by_type_sal_name is not None
    assert bareme_name is not None
    assert categorie_salarie is not None
    assert base is not None
    assert plafond_securite_sociale is not None
    TypesCategorieSalarie = categorie_salarie.possible_values

    def iter_cotisations():
        for categorie_salarie_type in TypesCategorieSalarie:
            if categorie_salarie_type == TypesCategorieSalarie.non_pertinent:
                continue

            if bareme_by_type_sal_name._name == 'cotisations_employeur_after_preprocessing':
                cotisations_by_categorie_salarie = cotisations_employeur_by_categorie_salarie
            elif bareme_by_type_sal_name._name == 'cotisations_salarie_after_preprocessing':
                cotisations_by_categorie_salarie = cotisations_salarie_by_categorie_salarie
            else:
                NameError()

            try:
                categorie_salarie_baremes = bareme_by_type_sal_name[categorie_salarie_type.name]
            except KeyError as e:
                # FIXME: dirty fix since public_titulaire_militaire does not exist
                if categorie_salarie_type.name == 'public_titulaire_militaire':
                    continue
                raise(e)

            if bareme_name in cotisations_by_categorie_salarie[categorie_salarie_type.name]:
                bareme = categorie_salarie_baremes[bareme_name]
            else:
                KeyError(f'{bareme_name} not in {bareme_by_type_sal_name._name} for {categorie_salarie_type.name}')
                continue

            yield bareme.calc(
                base * (categorie_salarie == categorie_salarie_type),
                factor = plafond_securite_sociale,
                round_base_decimals = round_base_decimals,
                )

    return - sum(iter_cotisations())


def apply_bareme(individu, period, parameters, cotisation_type = None, bareme_name = None, variable_name = None):
    cotisation_mode_recouvrement = individu('cotisation_sociale_mode_recouvrement', period)
    TypesCotisationSocialeModeRecouvrement = cotisation_mode_recouvrement.possible_values
    cotisation = (
        # anticipé (mensuel avec recouvrement en fin d'année)
        cotisation_mode_recouvrement == TypesCotisationSocialeModeRecouvrement.mensuel) * (
            compute_cotisation_anticipee(
                individu,
                period,
                parameters,
                cotisation_type = cotisation_type,
                bareme_name = bareme_name,
                variable_name = variable_name,
                )
            ) + (
        # en fin d'année
        cotisation_mode_recouvrement == TypesCotisationSocialeModeRecouvrement.annuel) * (
            compute_cotisation_annuelle(
                individu,
                period,
                parameters,
                cotisation_type = cotisation_type,
                bareme_name = bareme_name,
                )
            ) + (
        # mensuel strict
        cotisation_mode_recouvrement == TypesCotisationSocialeModeRecouvrement.mensuel_strict) * (
            compute_cotisation(
                individu,
                period,
                parameters,
                cotisation_type = cotisation_type,
                bareme_name = bareme_name,
                )
            )
    return cotisation


def compute_cotisation(individu, period, parameters, cotisation_type = None, bareme_name = None):
    assert cotisation_type is not None
    if cotisation_type == 'employeur':
        bareme_by_type_sal_name = parameters(period).cotsoc.cotisations_employeur
    elif cotisation_type == 'salarie':
        bareme_by_type_sal_name = parameters(period).cotsoc.cotisations_salarie
    assert bareme_name is not None

    assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period, options = [ADD])
    plafond_securite_sociale = individu('plafond_securite_sociale', period, options = [ADD])
    categorie_salarie = individu('categorie_salarie', period.first_month)

    cotisation = apply_bareme_for_relevant_type_sal(
        bareme_by_type_sal_name = bareme_by_type_sal_name,
        bareme_name = bareme_name,
        base = assiette_cotisations_sociales,
        plafond_securite_sociale = plafond_securite_sociale,
        categorie_salarie = categorie_salarie,
        )
    return cotisation


def compute_cotisation_annuelle(individu, period, parameters, cotisation_type = None, bareme_name = None):
    if period.start.month < 12:
        return 0
    if period.start.month == 12:
        return compute_cotisation(
            individu,
            period.this_year,
            parameters,
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            )


def compute_cotisation_anticipee(individu, period, parameters, cotisation_type = None, bareme_name = None, variable_name = None):
    if period.start.month < 12:
        return compute_cotisation(
            individu,
            period.first_month,
            parameters,
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            )
    if period.start.month == 12:
        cumul = individu(variable_name, period.start.offset('first-of', 'month').offset(
            -11, 'month').period('month', 11), options = [ADD])
        # December variable_name depends on variable_name in the past 11 months.
        # We need to explicitely allow this recursion.

        return compute_cotisation(
            individu,
            period.this_year,
            parameters,
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            ) - cumul
