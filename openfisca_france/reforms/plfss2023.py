import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')

def modify_parameters(parameters):
    reform_year = 2022
    reform_period = period(reform_year)

    # Revalorisation ASF
    revalorisation = 50/100
    parameters.prestations_sociales.prestations_familiales.education_presence_parentale.asf.montant_asf.orphelin_assimile_deux_parents.update(period=reform_period, value=round( 0.375 * (1 + revalorisation)))
    parameters.prestations_sociales.prestations_familiales.education_presence_parentale.asf.montant_asf.orphelin_assimile_seul_parent.update(period=reform_period, value=round( 0.2813 * (1 + revalorisation)))
    
    # Nouveau parametre : Extension CMG
    parameters.prestations_sociales.prestations_familiales.petite_enfance.paje.paje_cmg.limite_age.reduite.update(period=reform_period, value=null)
    parameters.prestations_sociales.prestations_familiales.petite_enfance.paje.paje_cmg.limite_age.pleine.update(period=reform_period, value=6)
    parameters.prestations_sociales.prestations_familiales.petite_enfance.paje.paje_cmg.limite_age.etendue.update(period=reform_period, value=12)
    return parameters

class paje_cmg(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'PAJE - Complément de libre choix du mode de garde'
    set_input = set_input_divide_by_period
    reference = [
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=C92307A93BE5F694EB49FE51DC09602C.tplgfr29s_1?idArticle=LEGIARTI000031500755&cidTexte=LEGITEXT000006073189&categorieLien=id&dateTexte=',
        'https://www.caf.fr/allocataires/aides-et-demarches/droits-et-prestations/vie-personnelle/le-complement-de-libre-choix-du-mode-de-garde-cmg'
        ]
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2022_08_01(famille, period, parameters):
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
        parent_isole = not_(famille('en_couple', period))

        aah_i = famille.members('aah', period)
        aah = famille.sum(aah_i)

        etudiant_i = famille.members('etudiant', period)
        parent_etudiant = famille.any(etudiant_i, role = Famille.PARENT)

    # condition de revenu minimal

        # L'enfant doit avoir un age entre 0 et 12 ans
        if parent_isole:
            age_max = paje.paje_cmg.limite_age.etendue
        else:
            age_max = paje.paje_cmg.limite_age.pleine
        cond_age_enf = (nb_enf(famille, period, 0, age_max - 1) > 0)

        # TODO:    cond_rpns    =
        # TODO: RSA insertion, alloc insertion, ass
        cond_nonact = (aah > 0) | parent_etudiant  # | (ass>0)

        cond_eligibilite = cond_age_enf & (not_(inactif) | cond_nonact)

        # Si vous bénéficiez de la PreParE taux plein
        # (= vous ne travaillez plus ou interrompez votre activité professionnelle),
        # vous ne pouvez pas bénéficier du Cmg.
        paje_prepare_inactif = (paje_prepare > 0) * inactif
        eligible = cond_eligibilite * not_(paje_prepare_inactif)

    # Les plafonds de ressources
        seuil_revenus_1 = (
            (nombre_enfants == 1) * paje.plaf_cmg.premier_plafond_ne_adopte_avant_04_2014.enfant
            + (nombre_enfants >= 2) * paje.plaf_cmg.premier_plafond_ne_adopte_avant_04_2014.deux_enfants
            + max_(nombre_enfants - 2, 0) * paje.plaf_cmg.premier_plafond_ne_adopte_avant_04_2014.majoration_enfant_supp
            )

        seuil_revenus_2 = (
            (nombre_enfants == 1) * paje.plaf_cmg.deuxieme_plafond_ne_adopte_avant_04_2014.enfant
            + (nombre_enfants >= 2) * paje.plaf_cmg.deuxieme_plafond_ne_adopte_avant_04_2014.deux_enfants
            + max_(nombre_enfants - 2, 0) * paje.plaf_cmg.deuxieme_plafond_ne_adopte_avant_04_2014.majoration_enfant_supp
            )

    #        Si vous bénéficiez du PreParE taux partiel (= vous travaillez entre 50 et 80% de la durée du travail fixée
    #        dans l'entreprise), vous cumulez intégralement la PreParE et le Cmg.
    #        Si vous bénéficiez du PreParE taux partiel (= vous travaillez à 50% ou moins de la durée
    #        du travail fixée dans l'entreprise), le montant des plafonds Cmg est divisé par 2.

        paje_prepare_temps_partiel = (paje_prepare > 0) * partiel1
        seuil_revenus_1 = seuil_revenus_1 * (1 - .5 * paje_prepare_temps_partiel)
        seuil_revenus_2 = seuil_revenus_2 * (1 - .5 * paje_prepare_temps_partiel)

    # calcul du montant
        montant_cmg = (
            bmaf * (
                1.0 * (nb_enf(famille, period, 0, paje.paje_cmg.limite_age.pleine - 1) > 0)
                # + 0.5 * (nb_enf(famille, period, paje.paje_cmg.limite_age.pleine, paje.paje_cmg.limite_age.reduite - 1) > 0)
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
        # TODO: vérfiez les règles de cumul
        # TODO: le versement de la CMG est fait 'à la condition que la rémunération horaire de [la personne effectuant la garde] n’excède pas un plafond fixé par décret'
        
        # La CMG rentre dans la liste des prestations (comme les Allocations Familiales) qui sont partagées entre les 2 parents en cas de garde alternée
        coeff_garde_alternee = famille('af_coeff_garde_alternee', period)
        paje_cmg_montant = paje_cmg * coeff_garde_alternee
        
        return paje_cmg_montant


class plfss2023(Reform):
    name = 'Projet de Loi de Financement de la Sécurité Sociale 2023'

    def apply(self):
        self.update_variable(paje_cmg)
        self.modify_parameters(modifier_function = modify_parameters)
