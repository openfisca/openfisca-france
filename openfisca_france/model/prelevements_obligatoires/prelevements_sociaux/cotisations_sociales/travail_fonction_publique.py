import math

from openfisca_france.model.base import *
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme_for_relevant_type_sal


class cotisation_ati_atiacl(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation ATI et ATIACL (contributions pour le financement de l'allocation temporaires d'invalidité)"
    definition_period = MONTH
    # patronale, non-contributive

    def formula(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme_ati = parameters(period).cotisations_secteur_public.retraite.ati.ati
        bareme_atiacl = parameters(period).cotisations_secteur_public.cnracl.employeur.atiacl

        etat_hors_militaire = (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
        terr_hosp = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
        )

        return (
            etat_hors_militaire * bareme_ati.calc(remuneration_principale)
            + terr_hosp * bareme_atiacl.calc(remuneration_principale)
        )


# sft dans assiette csg et RAFP et Cotisation exceptionnelle de solidarité et taxe sur les salaires
# primes dont indemnites de residences idem sft
# avantages en nature contrib exceptionnelle de solidarite, RAFP, CSG, CRDS.


class contribution_exceptionnelle_solidarite(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation exceptionnelle au fonds de solidarité (salarié)"
    definition_period = MONTH
    end = '2017-12-31'
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006072050&idArticle=LEGIARTI000006903878&dateTexte=&categorieLien=cid"

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        hsup = individu('hsup', period)
        categorie_salarie = individu('categorie_salarie', period)
        indemnite_residence = individu('indemnite_residence', period)
        primes_fonction_publique = individu('primes_fonction_publique', period)
        rafp_salarie = individu('rafp_salarie', period)
        cotisation_retraite_base_public_salarie = individu('cotisation_retraite_base_public_salarie', period)
        cotisations_salariales_contributives = individu('cotisations_salariales_contributives', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        salaire_de_base = individu('salaire_de_base', period)
        supplement_familial_traitement = individu('supplement_familial_traitement', period)
        # Assujettis
        parameters = parameters(period)
        seuil_assujetissement_fds = compute_seuil_fds(parameters)
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
        assujettis = concernes * (remuneration_brute > seuil_assujetissement_fds)
        # Pour le calcul de l'assiette, on déduit de la rémunaration brute
        #  - toutes les cotisations de sécurité sociale obligatoires
        #  - les prélèvements pour pension
        #  - et, le cas échéant, les prélèvements au profit des régimes de retraite complémentaire obligatoires.
        # Soit:
        #  - pour les titutlaires, les pensions
        #  - les non titulaires, les cotisations sociales contributives (car pas de cotisations non contributives pour les non titulaires de la fonction public)
        deduction = assujettis * (
            + rafp_salarie
            + cotisation_retraite_base_public_salarie
            + (categorie_salarie == TypesCategorieSalarie.public_non_titulaire) * cotisations_salariales_contributives
            )
        # Ces déductions sont négatives
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = parameters.cotsoc.cotisations_salarie,
            bareme_name = "excep_solidarite",
            base = assujettis * min_(
                remuneration_brute + supplement_familial_traitement + primes_fonction_publique + deduction,
                parameters.prelevements_sociaux.cotisations_sociales.fds.plafond_base_solidarite,
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            categorie_salarie = categorie_salarie,
            )
        return cotisation


class cotisation_fonds_emploi_hospitalier(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation au fonds pour l'emploi hospitalier (FEH) (cotisation employeur)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme_feh = parameters(period).cotisations_secteur_public.cnracl.employeur.hospitaliere.feh
        hosp = (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)

        return (
            hosp * bareme_feh.calc(remuneration_principale)
        )


class ircantec_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Ircantec salarié"
    definition_period = MONTH

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme = parameters(period).prelevements_sociaux.cotisations_secteur_public.ircantec.salarie.ircantec
        montant = bareme.calc(
            tax_base = assiette_cotisations_sociales,
            factor = plafond_securite_sociale,
            )

        return - montant * (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)


class ircantec_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Ircantec employeur"
    definition_period = MONTH

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme = parameters(period).prelevements_sociaux.cotisations_secteur_public.ircantec.employeur.ircantec
        montant = bareme.calc(
            tax_base = assiette_cotisations_sociales,
            factor = plafond_securite_sociale,
            )

        return - montant * (categorie_salarie == TypesCategorieSalarie.public_non_titulaire)


class cotisation_retraite_base_public_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation au régime de base de retraite de la fonction publique - part salariale (retenue pour pension)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        traitement_indiciaire_brut = individu('traitement_indiciaire_brut', period)
        nouvelle_bonification_indiciaire = individu('nouvelle_bonification_indiciaire', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme_cnracl_salarie = parameters(period).prelevements_sociaux.cotisations_secteur_public.cnracl.salarie
        bareme_retraite_etat_salarie = parameters(period).prelevements_sociaux.cotisations_secteur_public.retraite_etat.pension.salarie.pension

        terr_or_hosp = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale) | (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )
        etat_militaire = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
            + (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)
            )

        montant = (
            etat_militaire * bareme_retraite_etat_salarie.calc(traitement_indiciaire_brut + nouvelle_bonification_indiciaire)
            + terr_or_hosp * bareme_cnracl_salarie.cnracl1.calc(traitement_indiciaire_brut)
            + terr_or_hosp * bareme_cnracl_salarie.cnracl2.calc(nouvelle_bonification_indiciaire)
            )

        return - montant


class cotisation_retraite_base_public_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation au régime de base de retraite de la fonction publique - part employeur"
    reference = "http://www.ac-besancon.fr/spip.php?article2662"
    definition_period = MONTH

    def formula(individu, period, parameters):
        remuneration_principale = individu('remuneration_principale', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme_cnracl_employeur = parameters(period).prelevements_sociaux.cotisations_secteur_public.cnracl.employeur
        bareme_retraite_etat_employeur = parameters(period).prelevements_sociaux.cotisations_secteur_public.retraite_etat.pension.employeur

        terr_or_hosp = (
            (categorie_salarie == TypesCategorieSalarie.public_titulaire_territoriale) | (categorie_salarie == TypesCategorieSalarie.public_titulaire_hospitaliere)
            )
        etat = (categorie_salarie == TypesCategorieSalarie.public_titulaire_etat)
        militaire = (categorie_salarie == TypesCategorieSalarie.public_titulaire_militaire)

        montant = (
            etat * bareme_retraite_etat_employeur.pension_civils.calc(remuneration_principale)
            + militaire * bareme_retraite_etat_employeur.pension_militaires.calc(remuneration_principale)
            + terr_or_hosp * bareme_cnracl_employeur.cnracl.calc(remuneration_principale)
            )

        return - montant


class rafp_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Part salariale de la retraite additionelle de la fonction publique"
    definition_period = MONTH

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
        bareme_rafp_salarie = parametres_rafp.salarie.rafp

        base_imposable = primes_fonction_publique + supplement_familial_traitement + indemnite_residence + avantage_en_nature
        assiette = (min_(base_imposable, taux_plafond_tib * traitement_indiciaire_brut) + gipa) * eligible
        # Même régime pour les fonctions publiques d'Etat et des collectivité locales
        rafp_salarie = eligible * bareme_rafp_salarie.calc(assiette)
        return - rafp_salarie


class rafp_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Part patronale de la retraite additionnelle de la fonction publique"
    definition_period = MONTH

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
        bareme_rafp_employeur = parametres_rafp.employeur.rafp

        base_imposable = primes_fonction_publique + supplement_familial_traitement + indemnite_residence + avantage_en_nature
        assiette = (min_(base_imposable, taux_plafond_tib * traitement_indiciaire_brut) + gipa) * eligible
        # Même régime pour les fonctions publiques d'Etat et des collectivité locales
        rafp_employeur = eligible * bareme_rafp_employeur.calc(assiette)
        return - rafp_employeur


def compute_seuil_fds(parameters):
    '''
    Calcule le seuil mensuel d'assujetissement à la contribution au fond de solidarité
    '''
    fds = parameters.prelevements_sociaux.cotisations_sociales.fds
    pt_ind_mensuel = fds.valeur_annuelle_point_fp / 12
    seuil_mensuel = math.floor((pt_ind_mensuel * fds.indice_majore_de_reference))  # TODO improve
    return seuil_mensuel
