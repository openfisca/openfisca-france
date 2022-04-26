import math

from openfisca_france.model.base import *
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme_for_relevant_type_sal


class ati_atiacl(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation ATI et ATIACL (contributions pour le financement de l'allocation temporaires d'invalidité)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # patronale, non-contributive

    def formula(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        _P = parameters(period)

        # ATI : pour les fonctionnaires d'Etat, hors militaires
        cotisation_etat_hors_militaires = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = 'ati',
            base = remuneration_principale,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        # ATIACL : pour les fonctionnaires territoriaux et hospitaliers
        cotisation_collectivites_locales = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = 'atiacl',
            base = remuneration_principale,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation_etat_hors_militaires + cotisation_collectivites_locales


# sft dans assiette csg et RAFP et Cotisation exceptionnelle de solidarité et taxe sur les salaires
# primes dont indemnites de residences idem sft
# avantages en nature contrib exceptionnelle de solidarite, RAFP, CSG, CRDS.


class contribution_exceptionnelle_solidarite(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation exceptionnelle au fonds de solidarité (salarié)'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2017-12-31'
    reference = 'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006072050&idArticle=LEGIARTI000006903878&dateTexte=&categorieLien=cid'

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        hsup = individu('hsup', period)
        categorie_salarie = individu('categorie_salarie', period)
        indemnite_residence = individu('indemnite_residence', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        rafp_salarie = individu('rafp_salarie', period)
        pension_salarie = individu('pension_salarie', period)
        cotisations_salariales_contributives = individu('cotisations_salariales_contributives', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        salaire_de_base = individu('salaire_de_base', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        # Assujettis
        parameters = parameters(period)
        seuil_assujettissement_fds = compute_seuil_fds(parameters.prelevements_sociaux.cotisations_secteur_public.fds.salarie)
        concernes = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)
            )
        remuneration_brute = (
            traitement_indiciaire_brut
            + salaire_de_base
            + indemnite_residence
            - hsup
            )
        assujettis = concernes * (remuneration_brute > seuil_assujettissement_fds)
        # Pour le calcul de l'assiette, on déduit de la rémunaration brute
        #  - toutes les cotisations de sécurité sociale obligatoires
        #  - les prélèvements pour pension
        #  - et, le cas échéant, les prélèvements au profit des régimes de retraite complémentaire obligatoires.
        # Soit:
        #  - pour les titutlaires, les pensions
        #  - les non titulaires, les cotisations sociales contributives (car pas de cotisations non contributives pour les non titulaires de la fonction public)
        deduction = assujettis * (
            + rafp_salarie
            + pension_salarie
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire) * cotisations_salariales_contributives
            )
        # Ces déductions sont négatives
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = parameters.cotsoc.cotisations_salarie,
            bareme_name = 'excep_solidarite',
            base = assujettis * min_(
                remuneration_brute + supplement_familial_traitement + primes_fonction_publique + deduction,
                parameters.prelevements_sociaux.cotisations_secteur_public.fds.salarie.plafond_base_solidarite,
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation


class indemnite_compensatrice_csg(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnité compensatrice créée en 2018 pour compenser les effets de la hausse de la CSG - Calcul pour les fonctionnnaires recrutés à partir de 2018'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2018_01_01(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)
        eligible = ((categorie_salarie == TypesCategorieSalarie.public_titulaire_etat) + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire) + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale) + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)) > 0
        indem = remuneration_principale * 0.0076

        return indem * eligible


class fonds_emploi_hospitalier(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation au fonds pour l'emploi hospitalier (FEH) (cotisation employeur)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        _P = parameters(period)

        # Que pour fonctionnaires hospitaliers
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = 'feh',
            base = remuneration_principale,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation


class ircantec_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Ircantec salarié'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie,
            bareme_name = 'ircantec',
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )

        return ircantec * (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)


class ircantec_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Ircantec employeur'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = 'ircantec',
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )

        return ircantec * (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)


class pension_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation au régime de base de retraite de la fonction publique - part salariale (retenue pour pension)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        nouvelle_bonification_indiciaire = individu('nouvelle_bonification_indiciaire', period)
        categorie_salarie = individu('categorie_salarie', period)
        _P = parameters(period)
        sal = _P.cotsoc.cotisations_salarie

        terr_or_hosp = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale) | (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )
        etat_militaire = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            )

        montant = (
            etat_militaire
            * sal['public_titulaire_etat']['pension'].calc(traitement_indiciaire_brut + nouvelle_bonification_indiciaire)
            + terr_or_hosp * sal['public_titulaire_territoriale']['cnracl_s_ti'].calc(traitement_indiciaire_brut)
            + terr_or_hosp * sal['public_titulaire_territoriale']['cnracl_s_nbi'].calc(nouvelle_bonification_indiciaire)
            )

        return - montant


class pension_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation au régime de base de retraite de la fonction publique - part employeur'
    reference = 'http://www.ac-besancon.fr/spip.php?article2662'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)

        terr_or_hosp = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale) | (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )
        etat = (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
        militaire = (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
        _P = parameters(period)
        pat = _P.cotsoc.cotisations_employeur

        montant = (
            etat * pat['public_titulaire_etat']['pension'].calc(remuneration_principale)
            + militaire * pat['public_titulaire_militaire']['pension'].calc(remuneration_principale)
            + terr_or_hosp * pat['public_titulaire_territoriale']['cnracl'].calc(remuneration_principale)
            )

        return - montant


class rafp_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Part salariale de la retraite additionelle de la fonction publique'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2005_01_01(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        categorie_salarie = individu('categorie_salarie', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        indemnite_residence = individu('indemnite_residence', period)
        gipa = individu('gipa', period)
        avantage_en_nature = individu('avantage_en_nature', period)

        eligible = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        parametres_rafp = parameters(period).prelevements_sociaux.cotisations_secteur_public.rafp
        taux_plafond_tib = parametres_rafp.rafp_plaf_assiette
        _P = parameters(period)
        bareme_rafp_salarie = _P.cotsoc.cotisations_salarie.public_titulaire_etat['rafp']

        base_imposable = primes_fonction_publique + supplement_familial_traitement + indemnite_residence + avantage_en_nature
        assiette = (min_(base_imposable, taux_plafond_tib * traitement_indiciaire_brut) + gipa) * eligible
        # Même régime pour les fonctions publiques d'Etat et des collectivité locales
        rafp_salarie = eligible * bareme_rafp_salarie.calc(assiette)
        return - rafp_salarie


class rafp_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Part patronale de la retraite additionnelle de la fonction publique'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2005_01_01(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        categorie_salarie = individu('categorie_salarie', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        indemnite_residence = individu('indemnite_residence', period)
        indemnite_compensatrice_csg = individu('indemnite_compensatrice_csg', period)
        gipa = individu('gipa', period)
        avantage_en_nature = individu('avantage_en_nature', period)

        eligible = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )

        parametres_rafp = parameters(period).prelevements_sociaux.cotisations_secteur_public.rafp
        taux_plafond_tib = parametres_rafp.rafp_plaf_assiette
        _P = parameters(period)
        bareme_rafp_employeur = _P.cotsoc.cotisations_employeur.public_titulaire_etat['rafp']

        base_imposable = primes_fonction_publique + supplement_familial_traitement + indemnite_residence + indemnite_compensatrice_csg + avantage_en_nature
        assiette = (min_(base_imposable, taux_plafond_tib * traitement_indiciaire_brut) + gipa) * eligible
        # Même régime pour les fonctions publiques d'Etat et des collectivité locales
        rafp_employeur = eligible * bareme_rafp_employeur.calc(assiette)
        return - rafp_employeur


def compute_seuil_fds(fds):
    '''
    Calcule le seuil mensuel d'assujetissement à la contribution au fond de solidarité
    '''
    pt_ind_mensuel = fds.pt_ind / 12
    seuil_mensuel = math.floor((pt_ind_mensuel * fds.ind_maj_ref))  # TODO improve
    return seuil_mensuel
