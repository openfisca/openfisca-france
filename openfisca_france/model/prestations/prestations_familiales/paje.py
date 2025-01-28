from numpy import round, floor, datetime64, maximum

from openfisca_france.model.base import *
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf
from openfisca_core.periods import Instant


# Prestations familiales
class inactif(Variable):
    value_type = bool
    entity = Famille
    label = 'Parent inactif (PAJE-CLCA)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class partiel1(Variable):
    value_type = bool
    entity = Famille
    label = 'Parent actif à moins de 50% (PAJE-CLCA)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class partiel2(Variable):
    value_type = bool
    entity = Famille
    label = 'Parent actif entre 50% et 80% (PAJE-CLCA)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class opt_colca(Variable):
    value_type = bool
    entity = Famille
    label = 'Opte pour le COLCA'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class empl_dir(Variable):
    value_type = bool
    entity = Famille
    label = 'Emploi direct (CLCMG)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class ass_mat(Variable):
    value_type = bool
    entity = Famille
    label = 'Assistante maternelle (CLCMG)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class gar_dom(Variable):
    value_type = bool
    entity = Famille
    label = 'Garde à domicile (CLCMG)'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class paje(Variable):
    value_type = float
    entity = Famille
    label = 'PAJE - Ensemble des prestations'
    reference = 'http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/la-prestation-d-accueil-du-jeune-enfant-paje'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2017_04(famille, period):
        '''
        Prestation d'accueil du jeune enfant
        '''
        paje_base = famille('paje_base', period)
        paje_naissance = famille('paje_naissance', period)
        paje_prepare = famille('paje_prepare', period)
        paje_cmg = famille('paje_cmg', period)

        return paje_base + (paje_naissance + paje_prepare + paje_cmg)

    def formula_2004_01_01(famille, period):
        '''
        Prestation d'accueil du jeune enfant
        '''
        paje_base = famille('paje_base', period)
        paje_naissance = famille('paje_naissance', period)
        paje_clca = famille('paje_clca', period)
        paje_cmg = famille('paje_cmg', period)
        paje_colca = famille('paje_colca', period)

        return paje_base + (paje_naissance + paje_clca + paje_cmg + paje_colca)


class paje_base(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Allocation de base de la PAJE'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2552.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2004(famille, period, parameters):
        couple_biactif = famille('biactivite', period)
        parent_isole = not_(famille('en_couple', period))
        nombre_enfants = famille('af_nbenf', period)
        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        # Le montant, précédemment indexé sur la BMAF, est gelé en 2013, et dégelé en 2018
        date_gel_paje = Instant((2013, 4, 1))
        date_degel_paje = Instant((2018, 4, 1))
        periode_de_gel = date_degel_paje > period.start > date_gel_paje
        indice = parameters(date_gel_paje).prestations_sociales.prestations_familiales.bmaf.bmaf if periode_de_gel else bmaf
        # Le taux ne dépend pas de l'année en cours mais de la réforme en vigueur pour l'année de naissance:
        montant_taux_plein_avant_2014 = indice * paje.paje_cm.montant.allocation_base_taux_plein.avant_2014.taux
        montant_taux_plein_2014_2018 = indice * paje.paje_cm.montant.allocation_base_taux_plein.apres_2014.taux
        montant_taux_plein_apres_2018 = indice * paje.paje_cm.montant.allocation_base_taux_plein.apres_2018.taux

        # Avant réforme d'avril 2014 (enfants nés avant avril 2014)
        def plafond_avant_avril_2014():
            if period.start >= Instant((2018, 1, 1)):
                return 0
            plafond_de_base = paje.paje_plaf.ne_adopte_avant_04_2014.plafond_ressources_0_enfant
            maj_plafond_2_premiers_enfants = paje.paje_plaf.ne_adopte_avant_04_2014.majorations_enfants.premier_2eme_enfant * plafond_de_base
            maj_plafond_par_enfant_sup = paje.paje_plaf.ne_adopte_avant_04_2014.majorations_enfants.troisieme_plus_enfant * plafond_de_base
            maj_plafond_seul_biactif = paje.paje_plaf.ne_adopte_avant_04_2014.biactifs_parents_isoles

            plafond = (
                plafond_de_base
                + min_(nombre_enfants, 2) * maj_plafond_2_premiers_enfants
                + max_(nombre_enfants - 2, 0) * maj_plafond_par_enfant_sup
                + (couple_biactif + parent_isole) * maj_plafond_seul_biactif
                )
            return plafond

        # A partir de la réforme de 2014 et jusqu'à la réforme de 2018 (enfants nés entre le 1er avril 2014 et le 1er avril 2018)
        def plafond_taux_plein_2014_2018():
            if period.start < Instant((2014, 4, 1)) or period.start >= Instant((2021, 4, 1)):
                return plafond_apres_ajustement_2014_2018(0, 0, 0)
            plafond_de_base = paje.paje_plaf.ne_adopte_04_2014_et_03_2018.taux_plein.plafond_ressources_0_enfant
            maj_plafond_seul_biactif = paje.paje_plaf.ne_adopte_04_2014_et_03_2018.taux_plein.biactifs_parents_isoles
            maj_plafond_par_enfant = plafond_de_base * paje.paje_plaf.ne_adopte_04_2014_et_03_2018.majorations_enfants.majoration_enfant_supp
            return plafond_apres_ajustement_2014_2018(plafond_de_base, maj_plafond_par_enfant, maj_plafond_seul_biactif)

        def plafond_taux_partiel_2014_2018():
            if period.start < Instant((2014, 4, 1)) or period.start >= Instant((2021, 4, 1)):
                return plafond_apres_ajustement_2014_2018(0, 0, 0)
            plafond_de_base = paje.paje_plaf.ne_adopte_04_2014_et_03_2018.taux_partiel.plafond_ressources_0_enfant
            maj_plafond_seul_biactif = paje.paje_plaf.ne_adopte_04_2014_et_03_2018.taux_partiel.biactifs_parents_isoles
            maj_plafond_par_enfant = plafond_de_base * paje.paje_plaf.ne_adopte_04_2014_et_03_2018.majorations_enfants.majoration_enfant_supp
            return plafond_apres_ajustement_2014_2018(plafond_de_base, maj_plafond_par_enfant, maj_plafond_seul_biactif)

        def plafond_apres_ajustement_2014_2018(plafond_de_base, maj_plafond_par_enfant, maj_plafond_seul_biactif):
            plafond = (
                plafond_de_base
                + nombre_enfants * maj_plafond_par_enfant
                + (couple_biactif + parent_isole) * maj_plafond_seul_biactif
                )
            return plafond

        # A partir de la réforme d'avril 2018 (enfants nés apres avril 2018)
        def plafond_taux_plein_apres_2018():
            plafond_de_base = paje.paje_plaf.ne_adopte_apres_04_2018.taux_plein.plafond_ressources_0_enfant
            maj_plafond_2_premiers_enfants = paje.paje_plaf.ne_adopte_apres_04_2018.majorations_enfants.premier_2eme_enfant * plafond_de_base
            maj_plafond_par_enfant_sup = paje.paje_plaf.ne_adopte_apres_04_2018.majorations_enfants.troisieme_plus_enfant * plafond_de_base
            maj_plafond_seul_biactif = paje.paje_plaf.ne_adopte_apres_04_2018.taux_plein.biactifs_parents_isoles

            return plafond_apres_ajustement_apres_2018(plafond_de_base, maj_plafond_2_premiers_enfants, maj_plafond_par_enfant_sup, maj_plafond_seul_biactif)

        def plafond_taux_partiel_apres_2018():
            plafond_de_base = paje.paje_plaf.ne_adopte_apres_04_2018.taux_partiel.plafond_ressources_0_enfant
            maj_plafond_2_premiers_enfants = paje.paje_plaf.ne_adopte_apres_04_2018.majorations_enfants.premier_2eme_enfant * plafond_de_base
            maj_plafond_par_enfant_sup = paje.paje_plaf.ne_adopte_apres_04_2018.majorations_enfants.troisieme_plus_enfant * plafond_de_base
            maj_plafond_seul_biactif = paje.paje_plaf.ne_adopte_apres_04_2018.taux_partiel.biactifs_parents_isoles

            return plafond_apres_ajustement_apres_2018(plafond_de_base, maj_plafond_2_premiers_enfants, maj_plafond_par_enfant_sup, maj_plafond_seul_biactif)

        def plafond_apres_ajustement_apres_2018(plafond_de_base, maj_plafond_2_premiers_enfants, maj_plafond_par_enfant_sup, maj_plafond_seul_biactif):
            plafond = (
                plafond_de_base
                + min_(nombre_enfants, 2) * maj_plafond_2_premiers_enfants
                + max_(nombre_enfants - 2, 0) * maj_plafond_par_enfant_sup
                + (couple_biactif + parent_isole) * maj_plafond_seul_biactif
                )
            return plafond

        a_un_enfant_eligible = famille.any(famille.members('enfant_eligible_paje', period))
        date_plus_jeune = famille.reduce(famille.members('date_naissance', period), maximum, datetime64('1066-01-01'))
        sujet_a_reforme_2014 = date_plus_jeune >= datetime64('2014-04-01')
        sujet_a_reforme_2018 = date_plus_jeune >= datetime64('2018-04-01')
        ne_avant_avril_2014 = True

        plafond_taux_partiel = select(
            [sujet_a_reforme_2018, sujet_a_reforme_2014, ne_avant_avril_2014],
            [plafond_taux_partiel_apres_2018(), plafond_taux_partiel_2014_2018(), plafond_avant_avril_2014()]
            )

        plafond_taux_plein = select(
            [sujet_a_reforme_2018, sujet_a_reforme_2014, ne_avant_avril_2014],
            [plafond_taux_plein_apres_2018(), plafond_taux_plein_2014_2018(), plafond_avant_avril_2014()]
            )

        montant_taux_plein = select(
            [sujet_a_reforme_2018, sujet_a_reforme_2014, ne_avant_avril_2014],
            [montant_taux_plein_apres_2018, montant_taux_plein_2014_2018, montant_taux_plein_avant_2014]
            )

        ressources = famille('prestations_familiales_base_ressources', period)
        montant_taux_partiel = montant_taux_plein / 2

        montant = (
            (ressources <= plafond_taux_plein) * montant_taux_plein
            + (ressources <= plafond_taux_partiel)
            * (ressources > plafond_taux_plein) * montant_taux_partiel
            )

        return a_un_enfant_eligible * montant


class enfant_eligible_paje(Variable):
    value_type = bool
    entity = Individu
    label = 'Enfant ouvrant droit à la PAJE de base'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        age = individu('age', period)
        autonomie_financiere = individu('autonomie_financiere', period)
        age_limite = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje.paje_cm.age_limite_enfant_adopte_non

        # L'allocation de base est versée jusqu'au dernier jour du mois civil précédant
        # celui au cours duquel l'enfant atteint l'âge de 3 ans.
        return (age < age_limite) * not_(autonomie_financiere)


class paje_naissance(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Allocation de naissance de la PAJE'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2550.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2018_04_01(famille, period, parameters):
        '''
        Prestation d'accueil du jeune enfant - Allocation de naissance
        Références législatives :git
        https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737121&dateTexte=&categorieLien=cid
        '''
        af_nbenf = famille('af_nbenf', period)
        base_ressources = famille('prestations_familiales_base_ressources', period)
        isole = not_(famille('en_couple', period))
        biactivite = famille('biactivite', period)
        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf
        prime_naissance = round(100 * paje.paje_cm2.montant.prime_naissance * bmaf) / 100

        # Versée au 7ème mois de grossesse
        diff_mois_naissance_periode_i = (famille.members('date_naissance', period).astype('datetime64[M]') - datetime64(period.start, 'M'))
        nb_enfants_eligibles = famille.sum(diff_mois_naissance_periode_i.astype('int') == 2, role = Famille.ENFANT)

        nbenf = af_nbenf + nb_enfants_eligibles  # Ajouter les enfants à naître

        taux_plafond = (
            (nbenf > 0)
            + paje.paje_plaf.ne_adopte_apres_04_2018.majorations_enfants.premier_2eme_enfant * min_(nbenf, 2)
            + paje.paje_plaf.ne_adopte_apres_04_2018.majorations_enfants.troisieme_plus_enfant * max_(nbenf - 2, 0)
            )

        majoration_isole_biactif = isole | biactivite

        plafond_de_ressources = (
            paje.paje_plaf.ne_adopte_apres_04_2018.taux_partiel.plafond_ressources_0_enfant
            * taux_plafond
            + (taux_plafond > 0)
            * paje.paje_plaf.ne_adopte_apres_04_2018.taux_partiel.biactifs_parents_isoles
            * majoration_isole_biactif
            )

        eligible_prime_naissance = (base_ressources <= plafond_de_ressources)

        return prime_naissance * eligible_prime_naissance * nb_enfants_eligibles

    def formula_2014_04_01(famille, period, parameters):
        '''
        Prestation d'accueil du jeune enfant - Allocation de naissance
        Références législatives :git
        https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006737121&dateTexte=&categorieLien=cid
        '''
        af_nbenf = famille('af_nbenf', period)
        base_ressources = famille('prestations_familiales_base_ressources', period)
        isole = not_(famille('en_couple', period))
        biactivite = famille('biactivite', period)
        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        fam_bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf

        # Le montant de la PAJE est gelé depuis avril 2013.
        date_gel_paje = Instant((2013, 4, 1))
        bmaf = fam_bmaf.bmaf if period.start < date_gel_paje else parameters(date_gel_paje).prestations_sociales.prestations_familiales.bmaf.bmaf
        prime_naissance = round(100 * paje.paje_cm2.montant.prime_naissance * bmaf) / 100

        # Versée au 7ème mois de grossesse
        diff_mois_naissance_periode_i = (famille.members('date_naissance', period).astype('datetime64[M]') - datetime64(period.start, 'M'))
        nb_enfants_eligibles = famille.sum(diff_mois_naissance_periode_i.astype('int') == 2, role = Famille.ENFANT)

        nbenf = af_nbenf + nb_enfants_eligibles  # Ajouter les enfants à naître

        majoration_isole_biactif = isole | biactivite

        plafond_de_ressources = (
            paje.paje_plaf.ne_adopte_04_2014_et_03_2018.taux_partiel.plafond_ressources_0_enfant
            + paje.paje_plaf.ne_adopte_04_2014_et_03_2018.taux_partiel.plafond_ressources_0_enfant * nbenf * paje.paje_plaf.ne_adopte_04_2014_et_03_2018.majorations_enfants.majoration_enfant_supp
            + paje.paje_plaf.ne_adopte_04_2014_et_03_2018.taux_partiel.biactifs_parents_isoles * majoration_isole_biactif
            )

        eligible_prime_naissance = (base_ressources <= plafond_de_ressources)

        return prime_naissance * eligible_prime_naissance * nb_enfants_eligibles

    def formula_2004_01_01(famille, period, parameters):
        '''
        Prestation d'accueil du jeune enfant - Allocation de naissance
        '''
        af_nbenf = famille('af_nbenf', period)
        base_ressources = famille('prestations_familiales_base_ressources', period)
        isole = not_(famille('en_couple', period))
        biactivite = famille('biactivite', period)
        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        fam_bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf

        # Le montant de la PAJE est gelé depuis avril 2013.
        date_gel_paje = Instant((2013, 4, 1))
        bmaf = fam_bmaf.bmaf if period.start < date_gel_paje else parameters(date_gel_paje).prestations_sociales.prestations_familiales.bmaf.bmaf
        nais_prime = round(100 * paje.paje_cm2.montant.prime_naissance * bmaf) / 100

        # Versée au 7ème mois de grossesse
        diff_mois_naissance_periode_i = (famille.members('date_naissance', period).astype('datetime64[M]') - datetime64(period.start, 'M'))
        nb_enfants_eligibles = famille.sum(diff_mois_naissance_periode_i.astype('int') == 2, role = Famille.ENFANT)

        nbenf = af_nbenf + nb_enfants_eligibles  # Ajouter le/les enfants à naître

        plaf_tx = (
            (nbenf > 0)
            + paje.paje_plaf.ne_adopte_avant_04_2014.majorations_enfants.premier_2eme_enfant * min_(nbenf, 2)
            + paje.paje_plaf.ne_adopte_avant_04_2014.majorations_enfants.troisieme_plus_enfant * max_(nbenf - 2, 0)
            )

        majo = isole | biactivite

        plaf = (
            paje.paje_plaf.ne_adopte_avant_04_2014.plafond_ressources_0_enfant
            * plaf_tx
            + (plaf_tx > 0)
            * paje.paje_plaf.ne_adopte_avant_04_2014.biactifs_parents_isoles
            * majo
            )

        elig = (base_ressources <= plaf)

        return nais_prime * elig * nb_enfants_eligibles


class paje_prepare(Variable):
    value_type = float
    entity = Famille
    set_input = set_input_divide_by_period
    label = 'Prestation Partagée d’éducation de l’Enfant (PreParE)'
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F32485'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class paje_cmg(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'PAJE - Complément de libre choix du mode de garde'
    set_input = set_input_divide_by_period
    reference = [
        'http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/le-complement-de-libre-choix-du-mode-de-garde',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=C92307A93BE5F694EB49FE51DC09602C.tplgfr29s_1?idArticle=LEGIARTI000031500755&cidTexte=LEGITEXT000006073189&categorieLien=id&dateTexte='
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2017_04_01(famille, period, parameters):
        '''
        Prestation d accueil du jeune enfant - Complément de libre choix du mode de garde

        Les conditions

        Vous devez :

            avoir un enfant de moins de 6 ans né, adopté ou recueilli en vue d'adoption à partir du 1er janvier 2004
            employer une assistante maternelle agréée ou une garde à domicile.

        Vous n'avez pas besoin de justifier d'une activité min_ si vous êtes :

            bénéficiaire de l'allocation aux adultes handicapés (Aah)
            au chômage et bénéficiaire de l'allocation d'insertion ou de l'allocation de solidarité spécifique
            bénéficiaire du Revenu de solidarité active (Rsa), sous certaines conditions de ressources étudiées par
            votre Caf, et inscrit dans une démarche d'insertionétudiant (si vous vivez en couple,
            vous devez être tous les deux étudiants).

        Autres conditions à remplir : Assistante maternelle agréée     Garde à domicile
        Son salaire brut ne doit pas dépasser par jour de garde et par enfant 5 fois le montant du Smic horaire brut,
        soit au max 45,00 €.
        Vous ne devez pas bénéficier de l'exonération des cotisations sociales dues pour la personne employée.
        '''
        # Récupération des données

        inactif = famille('inactif', period)
        partiel1 = famille('partiel1', period)
        nombre_enfants = famille('af_nbenf', period)
        base_ressources = famille('prestations_familiales_base_ressources', period.first_month)
        emploi_direct = famille('empl_dir', period)
        assistant_maternel = famille('ass_mat', period)
        garde_a_domicile = famille('gar_dom', period)
        paje_prepare = famille('paje_prepare', period)
        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        aah_i = famille.members('aah', period)
        aah = famille.sum(aah_i)

        etudiant_i = famille.members('etudiant', period)
        parent_etudiant = famille.any(etudiant_i, role = Famille.PARENT)

        # condition de revenu minimal

        cond_age_enf = (nb_enf(famille, period, 0, paje.paje_cmg.limite_age.reduite - 1) > 0)

        # TODO:    cond_rpns    =
        # TODO: RSA insertion, alloc insertion, ass
        cond_nonact = (aah > 0) | parent_etudiant  # | (ass>0)

        cond_eligibilite = cond_age_enf & (not_(inactif) | cond_nonact)

        # Si vous bénéficiez de la PreParE taux plein
        # (= vous ne travaillez plus ou interrompez votre activité professionnelle),
        # vous ne pouvez pas bénéficier du Cmg.
        paje_prepare_inactif = (paje_prepare > 0) * inactif
        eligible = cond_eligibilite * not_(paje_prepare_inactif)

        # Les plafonds de ressource

        seuil_revenus_1 = (
            (nombre_enfants == 1) * paje.plaf_cmg.premier_plafond_ne_adopte_apres_04_2014.enfant
            + (nombre_enfants >= 2) * paje.plaf_cmg.premier_plafond_ne_adopte_apres_04_2014.deux_enfants
            + max_(nombre_enfants - 2, 0) * paje.plaf_cmg.premier_plafond_ne_adopte_apres_04_2014.majoration_enfant_supp
            )

        seuil_revenus_2 = (
            (nombre_enfants == 1) * paje.plaf_cmg.deuxieme_plafond_ne_adopte_apres_04_2014.enfant
            + (nombre_enfants >= 2) * paje.plaf_cmg.deuxieme_plafond_ne_adopte_apres_04_2014.deux_enfants
            + max_(nombre_enfants - 2, 0) * paje.plaf_cmg.deuxieme_plafond_ne_adopte_apres_04_2014.majoration_enfant_supp
            )

        # Si vous bénéficiez du PreParE taux partiel (= vous travaillez entre 50 et 80% de la durée du travail fixée
        # dans l'entreprise), vous cumulez intégralement la PreParE et le Cmg.
        # Si vous bénéficiez du PreParE taux partiel (= vous travaillez à 50% ou moins de la durée
        # du travail fixée dans l'entreprise), le montant des plafonds Cmg est divisé par 2.

        paje_prepare_temps_partiel = (paje_prepare > 0) * partiel1
        seuil_revenus_1 = seuil_revenus_1 * (1 - .5 * paje_prepare_temps_partiel)
        seuil_revenus_2 = seuil_revenus_2 * (1 - .5 * paje_prepare_temps_partiel)

        # calcul du montant

        montant_cmg = (
            bmaf * (
                1.0 * (nb_enf(famille, period, 0, paje.paje_cmg.limite_age.pleine - 1) > 0)
                + (1 - paje.paje_cmg.taux_reduit) * (nb_enf(famille, period, paje.paje_cmg.limite_age.pleine, paje.paje_cmg.limite_age.reduite - 1) > 0)
                ) * (
                    emploi_direct * (
                        (base_ressources < seuil_revenus_1) * paje.paje_cmg.complement_libre_choix_mode_garde.revenus_inferieurs_45_plaf
                        + ((base_ressources >= seuil_revenus_1) & (base_ressources < seuil_revenus_2)) * paje.paje_cmg.complement_libre_choix_mode_garde.revenus_superieurs_45_plaf
                        + (base_ressources >= seuil_revenus_2) * paje.paje_cmg.complement_libre_choix_mode_garde.revenus_superieurs_plaf
                        )
                    + assistant_maternel * (
                        (base_ressources < seuil_revenus_1) * paje.paje_cmg.assistante_mat_asso_entreprise_microcreche.sous_premier_plafond
                        + ((base_ressources >= seuil_revenus_1) & (base_ressources < seuil_revenus_2)) * paje.paje_cmg.assistante_mat_asso_entreprise_microcreche.sous_second_plafond
                        + (base_ressources >= seuil_revenus_2) * paje.paje_cmg.assistante_mat_asso_entreprise_microcreche.apres_second_plafond
                        )
                    + garde_a_domicile * (
                        (base_ressources < seuil_revenus_1) * paje.paje_cmg.garde_domicile.sous_premier_plafond
                        + ((base_ressources >= seuil_revenus_1) & (base_ressources < seuil_revenus_2)) * paje.paje_cmg.garde_domicile.sous_second_plafond
                        + (base_ressources >= seuil_revenus_2) * paje.paje_cmg.garde_domicile.apres_second_plafond)
                    )
            )

        paje_cmg = eligible * montant_cmg
        # TODO: connecter avec le crédit d'impôt
        # TODO vérfiez les règles de cumul
        return paje_cmg

    def formula_2004_01_01(famille, period, parameters):
        '''
        Prestation d accueil du jeune enfant - Complément de libre choix du mode de garde

        Les conditions

        Vous devez :

            avoir un enfant de moins de 6 ans né, adopté ou recueilli en vue d'adoption à partir du 1er janvier 2004
            employer une assistante maternelle agréée ou une garde à domicile.
            avoir une activité professionnelle minimale
                si vous êtes salarié cette activité doit vous procurer un revenu minimum de :
                    si vous vivez seul : une fois la BMAF
                    si vous vivez en couple  soit 2 fois la BMAF
                si vous êtes non salarié, vous devez être à jour de vos cotisations sociales d'assurance vieillesse

        Vous n'avez pas besoin de justifier d'une activité min_ si vous êtes :

            bénéficiaire de l'allocation aux adultes handicapés (Aah)
            au chômage et bénéficiaire de l'allocation d'insertion ou de l'allocation de solidarité spécifique
            bénéficiaire du Revenu de solidarité active (Rsa), sous certaines conditions de ressources étudiées par
            votre Caf, et inscrit dans une démarche d'insertionétudiant (si vous vivez en couple,
            vous devez être tous les deux étudiants).

        Autres conditions à remplir : Assistante maternelle agréée     Garde à domicile
        Son salaire brut ne doit pas dépasser par jour de garde et par enfant 5 fois le montant du Smic horaire brut,
        soit au max 45,00 €.
        Vous ne devez pas bénéficier de l'exonération des cotisations sociales dues pour la personne employée.
        '''
        en_couple = famille('en_couple', period)
        af_nbenf = famille('af_nbenf', period)
        base_ressources = famille('prestations_familiales_base_ressources', period.first_month)
        empl_dir = famille('empl_dir', period)
        ass_mat = famille('ass_mat', period)
        gar_dom = famille('gar_dom', period)
        paje_clca_taux_partiel = famille('paje_clca_taux_partiel', period)
        paje_clca_taux_plein = famille('paje_clca_taux_plein', period)
        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        P_n_2_af = parameters(period.offset(-2, 'year')).prestations_sociales.prestations_familiales.bmaf
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        aah_i = famille.members('aah', period)
        aah = famille.sum(aah_i)

        etudiant_i = famille.members('etudiant', period)
        parent_etudiant = famille.any(etudiant_i, role = Famille.PARENT)

        salaire_imposable_i = famille.members('salaire_imposable', period)
        salaire_imposable = famille.sum(salaire_imposable_i, role = Famille.PARENT)

        hsup_i = famille.members('hsup', period)
        hsup = famille.sum(hsup_i, role = Famille.PARENT)

        # condition de revenu minimal

        bmaf_n_2 = P_n_2_af.bmaf
        cond_age_enf = (nb_enf(famille, period, 0, paje.paje_cmg.limite_age.reduite - 1) > 0)
        cond_sal = (salaire_imposable + hsup > 12 * bmaf_n_2 * (1 + en_couple))
    # TODO:    cond_rpns    =
        cond_act = cond_sal  # | cond_rpns

        cond_nonact = (aah > 0) | parent_etudiant  # | (ass>0)
    #  TODO: RSA insertion, alloc insertion, ass
        elig = cond_age_enf & (cond_act | cond_nonact)
        nbenf = af_nbenf

        seuil1 = (
            paje.plaf_cmg.premier_plafond_ne_adopte_avant_04_2014.enfant
            * (nbenf == 1)
            + paje.plaf_cmg.premier_plafond_ne_adopte_avant_04_2014.deux_enfants
            * (nbenf >= 2)
            + max_(nbenf - 2, 0)
            * paje.plaf_cmg.premier_plafond_ne_adopte_avant_04_2014.majoration_enfant_supp
            )

        seuil2 = (
            paje.plaf_cmg.deuxieme_plafond_ne_adopte_avant_04_2014.enfant
            * (nbenf == 1)
            + paje.plaf_cmg.deuxieme_plafond_ne_adopte_avant_04_2014.deux_enfants
            * (nbenf >= 2)
            + max_(nbenf - 2, 0)
            * paje.plaf_cmg.deuxieme_plafond_ne_adopte_avant_04_2014.majoration_enfant_supp
            )

    #        Si vous bénéficiez du Clca taux partiel (= vous travaillez entre 50 et 80% de la durée du travail fixée
    #        dans l'entreprise), vous cumulez intégralement le Clca et le Cmg.
    #        Si vous bénéficiez du Clca taux partiel (= vous travaillez à 50% ou moins de la durée
    #        du travail fixée dans l'entreprise), le montant des plafonds Cmg est divisé par 2.
        seuil1 = seuil1 * (1 - .5 * paje_clca_taux_partiel)
        seuil2 = seuil2 * (1 - .5 * paje_clca_taux_partiel)

        clmg = (
            bmaf
            * (
                1.0 * (nb_enf(famille, period, 0, paje.paje_cmg.limite_age.pleine - 1) > 0)
                + 0.5 * (nb_enf(famille, period, paje.paje_cmg.limite_age.pleine, paje.paje_cmg.limite_age.reduite - 1) > 0)
                )
            * (
                empl_dir * (
                    (base_ressources < seuil1) * paje.paje_cmg.complement_libre_choix_mode_garde.revenus_inferieurs_45_plaf
                    + ((base_ressources >= seuil1) & (base_ressources < seuil2)) * paje.paje_cmg.complement_libre_choix_mode_garde.revenus_superieurs_45_plaf
                    + (base_ressources >= seuil2) * paje.paje_cmg.complement_libre_choix_mode_garde.revenus_superieurs_plaf
                    )
                + ass_mat * (
                    (base_ressources < seuil1) * paje.paje_cmg.assistante_mat_asso_entreprise_microcreche.sous_premier_plafond
                    + ((base_ressources >= seuil1) & (base_ressources < seuil2)) * paje.paje_cmg.assistante_mat_asso_entreprise_microcreche.sous_second_plafond
                    + (base_ressources >= seuil2) * paje.paje_cmg.assistante_mat_asso_entreprise_microcreche.apres_second_plafond
                    )
                + gar_dom * (
                    (base_ressources < seuil1) * paje.paje_cmg.garde_domicile.sous_premier_plafond
                    + ((base_ressources >= seuil1) & (base_ressources < seuil2)) * paje.paje_cmg.garde_domicile.sous_second_plafond
                    + (base_ressources >= seuil2) * paje.paje_cmg.garde_domicile.apres_second_plafond
                    )
                )
            )
        # TODO: connecter avec le crédit d'impôt
        # Si vous bénéficiez du Clca taux plein
        # (= vous ne travaillez plus ou interrompez votre activité professionnelle),
        # vous ne pouvez pas bénéficier du Cmg.
        paje_cmg = elig * not_(paje_clca_taux_plein) * clmg
        # TODO vérfiez les règles de cumul
        return paje_cmg


class ape_avant_cumul(Variable):
    value_type = float
    entity = Famille
    label = "Allocation parentale d'éducation, avant prise en compte de la non-cumulabilité avec le CF et l'APJE"
    end = '2003-12-31'
    reference = "http://fr.wikipedia.org/wiki/Allocation_parentale_d'%C3%A9ducation_en_France"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        '''
        Allocation parentale d'éducation

        L’allocation parentale d’éducation s’adresse aux parents qui souhaitent arrêter ou
        réduire leur activité pour s’occuper de leurs jeunes enfants, à condition que ceux-ci
        soient nés avant le 01/01/2004. En effet, pour les enfants nés depuis cette date,
        dans le cadre de la Prestation d’Accueil du Jeune Enfant, les parents peuvent bénéficier
        du « complément de libre choix d’activité. »

        Les personnes en couple peuvent toutes deux bénéficier de l’APE à taux plein, mais pas en même temps.
        En revanche, elles peuvent cumuler deux taux partiels, à condition que leur total ne dépasse pas le montant
        du taux plein.

        TODO: cumul,  adoption, triplés,
        Cumul d'allocations : Cette allocation n'est pas cumulable pour un même ménage avec
        - une autre APE (sauf à taux partiel),
        - ou l'allocation pour jeune enfant (APJE) versée à partir de la naissance,
        - ou le complément familial,
        - ou l'allocation d’adulte handicapé (AAH).
        Enfin, il est à noter que cette allocation n’est pas cumulable avec :
        - une pension d’invalidité ou une retraite ;
        - des indemnités journalières de maladie, de maternité ou d’accident du travail ;
        - des allocations chômage. Il est tout de même possible de demander aux ASSEDIC la suspension de ces dernières
          pour percevoir l’APE.

        L'allocation parentale d'éducation n'est pas soumise à condition de ressources, sauf l’APE à taux partiel pour
        les professions non salariées.
        '''
        inactif = famille('inactif', period)
        partiel1 = famille('partiel1', period)
        partiel2 = famille('partiel2', period)
        ape = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.ape
        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af

        elig = (nb_enf(famille, period, 0, ape.age_max_enfant - 1) >= 1) & (nb_enf(famille, period, 0, af.af_cm.age2) >= 2)        # Inactif
        # Temps partiel 1
        # Salarié:
        # Temps de travail ne dépassant pas 50 % de la durée du travail fixée dans l'entreprise
        # VRP ou non salarié travaillant à temps partiel:
        # Temps de travail ne dépassant pas 76 heures par mois et un revenu professionnel mensuel inférieur ou égal à
        # (smic_8.27*169*85 %)
        # partiel1 = zeros((12,self.taille))

        # Temps partiel 2
        # Salarié:
        # Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
        # Temps de travail compris entre 77 et 122 heures par mois et un revenu professionnel mensuel ne dépassant pas
        #  (smic_8.27*169*136 %)
        ape = elig * (inactif * ape.montant_mensuel.taux_inactivite + partiel1 * ape.montant_mensuel.taux_activite_sup_50 + partiel2 * ape.montant_mensuel.taux_activite_sup_80)
        # Cummul APE APJE CF
        return ape  # annualisé


class apje_avant_cumul(Variable):
    value_type = float
    entity = Famille
    label = "Allocation pour le jeune enfant, avant prise en compte de la non-cumulabilité avec le CF et l'APE"
    end = '2003-12-31'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2552.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        '''
        Allocation pour jeune enfant
        '''
        base_ressources = famille('prestations_familiales_base_ressources', period.first_month)
        biactivite = famille('biactivite', period, options = [ADD])
        isole = not_(famille('en_couple', period))

        Papje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.apje
        Paf = parameters(period).prestations_sociales.prestations_familiales.bmaf
        P_n_2 = parameters(period.start.offset(-2, 'year')).prestations_sociales.prestations_familiales.bmaf

        # TODO: APJE courte voir doc ERF 2006
        nbenf = nb_enf(famille, period, 0, Papje.age_limite_enfants_ouvrant_droit_apje - 1)
        bmaf = Paf.bmaf
        bmaf_n_2 = P_n_2.bmaf
        base = round(Papje.apje_cm.taux_apje * bmaf, 2)
        base2 = round(Papje.apje_cm.taux_apje * bmaf_n_2, 2)
        plaf_tx = (nbenf > 0) + Papje.apje_cm.taux_apje_enfant_1_et_2 * min_(nbenf, 2) + Papje.apje_cm.taux_apje_enfant_3_et_plus * max_(nbenf - 2, 0)
        majo = isole | biactivite
        plaf = Papje.apje_plaf.plaf * plaf_tx + Papje.apje_plaf.majoration_plafond_ressources_0_enfant.plaf_maj * majo
        plaf2 = plaf + 12 * base2

        apje = (nbenf >= 1) * ((base_ressources <= plaf) * base + (base_ressources > plaf) * max_(plaf2 - base_ressources, 0) / 12.0)

        # Pour bénéficier de cette allocation, il faut que tous les enfants du foyer soient nés, adoptés, ou recueillis
        # en vue d’une adoption avant le 1er janvier 2004, et qu’au moins l’un d’entre eux ait moins de 3 ans.
        # Cette allocation est versée du 5ème mois de grossesse jusqu'au mois précédant le 3ème anniversaire de
        # l’enfant.

        # Non cumul APE APJE CF
        #  - L’allocation parentale d’éducation (APE), sauf pour les femmes enceintes.
        #    L’APJE est alors versée du 5ème mois de grossesse jusqu’à la naissance de l’enfant.
        #  - Le CF
        return apje


class ape(Variable):
    value_type = float
    entity = Famille
    label = "Allocation parentale d'éducation"
    end = '2003-12-31'
    reference = "http://fr.wikipedia.org/wiki/Allocation_parentale_d'%C3%A9ducation_en_France"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        apje_avant_cumul = famille('apje_avant_cumul', period)
        ape_avant_cumul = famille('ape_avant_cumul', period)
        cf_montant = famille('cf_montant', period)

        ape = (apje_avant_cumul < ape_avant_cumul) * (cf_montant < ape_avant_cumul) * ape_avant_cumul
        return round(ape, 2)


class crds_ape(Variable):
    value_type = float
    entity = Famille
    label = "CRDS sur l'allocation parentale d'éducation"
    definition_period = MONTH

    def formula(famille, period, parameters):
        ape = famille('ape', period)

        taux_crds = parameters(period).prelevements_sociaux.contributions_sociales.crds.taux

        return -(ape) * taux_crds


class ape_nette_crds(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "Allocation parentale d'éducation nette de CRDS"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        ape = famille('ape', period)
        crds_ape = famille('crds_ape', period)

        return ape + crds_ape


class apje(Variable):
    value_type = float
    entity = Famille
    label = 'Allocation pour le jeune enfant'
    end = '2003-12-31'
    reference = 'http://vosdroits.service-public.fr/particuliers/F2552.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        # L'APJE n'est pas cumulable avec le complément familial et l'APE
        apje_avant_cumul = famille('apje_avant_cumul', period)
        ape_avant_cumul = famille('ape_avant_cumul', period)
        cf_montant = famille('cf_montant', period)

        apje = (cf_montant < apje_avant_cumul) * (ape_avant_cumul < apje_avant_cumul) * apje_avant_cumul
        return round(apje, 2)


class crds_apje(Variable):
    value_type = float
    entity = Famille
    label = "CRDS sur l'allocation pour le jeune enfant"
    definition_period = MONTH

    def formula(famille, period, parameters):
        apje = famille('apje', period)

        taux_crds = parameters(period).prelevements_sociaux.contributions_sociales.crds.taux

        return -(apje) * taux_crds


class apje_nette_crds(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Allocation pour le jeune enfant nette de CRDS'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        apje = famille('apje', period)
        crds_apje = famille('crds_apje', period)

        return apje + crds_apje


class paje_clca(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "PAJE - Complément de libre choix d'activité - remplacée par paje_prepare à partir de 04/2017"
    reference = 'http://vosdroits.service-public.fr/particuliers/F313.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2017-04-01'

    def formula_2004(famille, period, parameters):
        '''
        Prestation d'accueil du jeune enfant - Complément de libre choix d'activité

        Parameters:
        -----------

        age :  âge en mois
        af_nbenf : nombre d'enfants aus sens des allocations familiales
        paje_base : allocation de base de la PAJE
        inactif : indicatrice d'inactivité
        partiel1 : Salarié: Temps de travail ne dépassant pas 50 % de la durée du travail fixée dans l'entreprise pour
                   les salariés VRP ou non salarié travaillant à temps partiel: Temps de travail ne dépassant pas 76
                   heures par mois et un revenu professionnel mensuel inférieur ou égal à (smic_8.27*169*85 %)
        partiel2 :  Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
                    VRP ou non salarié travaillant à temps partiel: Temps de travail compris entre 77 et 122 heures
                    par mois et un revenu professionnel mensuel ne dépassant pas (smic_8.27*169*136 %)

        http://www.caf.fr/wps/portal/particuliers/catalogue/metropole/paje
        '''
        af_nbenf = famille('af_nbenf', period)
        paje_base = famille('paje_base', period)
        inactif = famille('inactif', period)
        partiel1 = famille('partiel1', period)
        partiel2 = famille('partiel2', period)

        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        paje_non_nul = paje_base >= 0
        # durée de versement :
        # Pour un seul enfant à charge, le CLCA est versé pendant une période de 6 mois (paje.paje_clca.duree1)
        # à partir de la naissance ou de la cessation des IJ maternité et paternité.
        # A partir du 2ème enfant, il est versé jusqu’au mois précédant le 3ème anniversaire
        # de l’enfant.

        # Calcul de l'année et mois de naissance du cadet
        # TODO: ajuster en fonction de la cessation des IJ etc

        age_en_mois_i = famille.members('age_en_mois', period)
        age_m_benjamin = famille.min(age_en_mois_i, role = Famille.ENFANT)

        condition1 = (af_nbenf == 1) * (age_m_benjamin >= 0) * (age_m_benjamin < paje.paje_clca.duree1)
        age_benjamin = floor(age_m_benjamin / 12)
        condition2 = (age_benjamin <= (paje.paje_cm.age_limite_enfant_adopte_non - 1))
        condition = (af_nbenf >= 2) * condition2 + condition1

        paje_clca = (
            (condition * bmaf) * (
                not_(paje_non_nul) * (
                    inactif * paje.paje_clca.non_beneficiaires_enfant_ne_adopte_avant_04_2014.taux_plein
                    + partiel1 * paje.paje_clca.non_beneficiaires_enfant_ne_adopte_avant_04_2014.taux_partiel_50
                    + partiel2 * paje.paje_clca.non_beneficiaires_enfant_ne_adopte_avant_04_2014.taux_partiel_50_80
                    )
                + paje_non_nul * (
                    inactif * paje.paje_clca.beneficiaires_enfant_ne_adopte_apres_04_2014.taux_plein
                    + partiel1 * paje.paje_clca.beneficiaires_enfant_ne_adopte_apres_04_2014.taux_partiel_50
                    + partiel2 * paje.paje_clca.beneficiaires_enfant_ne_adopte_apres_04_2014.taux_partiel_50_80
                    )
                )
            )
        return paje_clca


class paje_clca_taux_plein(Variable):
    value_type = bool
    entity = Famille
    label = 'Indicatrice Clca taux plein'
    reference = 'http://vosdroits.service-public.fr/particuliers/F313.xhtml'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    end = '2017-04-01'

    def formula_2004_01_01(famille, period):
        paje_clca = famille('paje_clca', period)
        inactif = famille('inactif', period)

        return (paje_clca > 0) * inactif


class paje_clca_taux_partiel(Variable):
    value_type = bool
    entity = Famille
    label = 'Indicatrice Clca taux partiel'
    reference = 'http://vosdroits.service-public.fr/particuliers/F313.xhtml'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    end = '2017-04-01'

    def formula_2004_01_01(famille, period):
        paje_clca = famille('paje_clca', period)
        partiel1 = famille('partiel1', period)

        return (paje_clca > 0) * partiel1

    # TODO gérer les cumuls avec autres revenus et colca voir site caf


class paje_colca(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = "PAJE - Complément optionnel de libre choix d'activité"
    set_input = set_input_divide_by_period
    reference = 'http://vosdroits.service-public.fr/particuliers/F15110.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2017-04-01'

    def formula_2004_01_01(famille, period, parameters):
        '''
        Prestation d'accueil du jeune enfant - Complément optionnel de libre choix du mode de garde
        '''
        af_nbenf = famille('af_nbenf', period)
        opt_colca = famille('opt_colca', period)
        paje_base = famille('paje_base', period)

        paje = parameters(period).prestations_sociales.prestations_familiales.petite_enfance.paje
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        age_en_mois_i = famille.members('age_en_mois', period)
        age_m_benjamin = famille.min(age_en_mois_i, role = Famille.ENFANT)

        condition = (age_m_benjamin < 12 * paje.paje_clca.colca.age) * (age_m_benjamin >= 0)
        nbenf = af_nbenf
        paje_non_nul = (paje_base > 0)

        paje_colca = (
            opt_colca
            * condition
            * (nbenf >= 3)
            * bmaf
            * (paje_non_nul * paje.paje_clca.colca.taux_plein_duree_arret_predeterminee + not_(paje_non_nul) * paje.paje_clca.colca.sansab)
            )

        return paje_colca


class crds_paje(Variable):
    value_type = float
    entity = Famille
    label = 'CRDS sur la PAJE - Ensemble des prestations'
    definition_period = MONTH

    def formula(famille, period, parameters):
        paje = famille('paje', period)

        taux_crds = parameters(period).prelevements_sociaux.contributions_sociales.crds.taux

        return -(paje) * taux_crds


class paje_nette_crds(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'PAJE nette de CRDS'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        paje = famille('paje', period)
        crds_paje = famille('crds_paje', period)

        return paje + crds_paje
