from numpy import logical_not as not_
from openfisca_france.model.base import *
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class ars(Variable):
    value_type = float
    entity = Famille
    label = 'Allocation de rentrée scolaire'
    reference = 'http://vosdroits.service-public.fr/particuliers/F1878.xhtml'
    definition_period = YEAR

    def formula(famille, period, parameters):
        '''
        Allocation de rentrée scolaire brute de CRDS
        '''
        janvier = period.first_month
        octobre = period.start.offset('first-of', 'year').offset(9, 'month').period('month')
        decembre = period.start.offset('first-of', 'year').offset(11, 'month').period('month')
        af_nbenf = famille('af_nbenf', octobre)
        base_ressources = famille('prestations_familiales_base_ressources', janvier)
        ars = parameters(octobre).prestations_sociales.prestations_familiales.education_presence_parentale.ars
        # TODO: convention sur la mensualisation

        bmaf = parameters(octobre).prestations_sociales.prestations_familiales.bmaf.bmaf

        # Condition sur l'âge
        # Art. R543-2 :
        # "Ouvre droit à l'allocation de rentrée scolaire chaque enfant à charge qui atteindra son sixième anniversaire avant le
        # 1er février de l'année suivant celle de la rentrée scolaire."
        # "L'allocation reste due, lors de chaque rentrée scolaire, pour tout enfant qui n'a pas atteint l'âge de dix-huit ans révolus au 15 septembre de l'année considérée."
        # "Le montant de l'allocation de rentrée scolaire est majoré, d'une part, lorsque l'enfant atteint ses onze ans, et, d'autre part, lorsque l'enfant atteint ses quinze ans, au cours de l'année civile de la rentrée scolaire."
        # Ce que l'on fait :
        #   - On donne éligibilité à l'ARS aux enfants à partir de ceux ayant 6 ans au 31/12. On n'ajoute pas ceux atteingant
        #     6 ans en janvier N+1 car normalement, n'entrent en CP que les enfants atteignant 6 ans l'année de la rentrée. D'ailleurs, le site de la Cnaf évoque l'âge de six ans au 31/12 : https://www.caf.fr/allocataires/droits-et-prestations/s-informer-sur-les-aides/enfance-et-jeunesse/l-allocation-de-rentree-scolaire-ars
        #   - Les majorations dépendent de l'âge au 31/12. Donc, au total, on détermine l'éligibilité des enfants à l'ARS et leur catégorie en termes de montant en fonction de leur âge en décembre.
        #   - Exception : la fin de l'éligibilité à l'ARS intervient après 17 ans, lorsque cet âge est dépassé non pas au 31/12, mais au 15/09 de l'année de la rentrée scolaire. Condition moins restrictive. On ajoute les enfants dus à cette moindre restriction, sans prendre en compte la subtilité du 15/09 (on inclut les enfants n'ayant pas atteint 18 ans au 30/09)
        enf_primaire = nb_enf(famille, decembre, ars.ars_cond.age_entree_primaire, ars.ars_cond.age_entree_college - 1)
        enf_college = nb_enf(famille, decembre, ars.ars_cond.age_entree_college, ars.ars_cond.age_entree_lycee - 1)
        enf_lycee_moins_18_ans_decembre = nb_enf(famille, decembre, ars.ars_cond.age_entree_lycee, ars.ars_cond.age_sortie_lycee - 1)
        age_en_mois_decembre_i = famille.members('age_en_mois', decembre)
        autonomie_financiere_i = famille.members('autonomie_financiere', decembre)
        enf_lycee_eligible_18_ans_decembre = famille.sum(
            ((age_en_mois_decembre_i <= 12 * ars.ars_cond.age_sortie_lycee + 2) * (age_en_mois_decembre_i >= 12 * ars.ars_cond.age_sortie_lycee) * not_(autonomie_financiere_i)),
            role = Famille.ENFANT
            )
        enf_lycee = enf_lycee_moins_18_ans_decembre + enf_lycee_eligible_18_ans_decembre

        # Plafond en fonction du nb d'enfants A CHARGE (Cf. article R543)
        ars_plaf_res = ars.ars_plaf.plafond_ressources * (1 + af_nbenf * ars.ars_plaf.majoration_par_enf_supp)

        arsbase = bmaf * (
            ars.ars_m.taux_primaire * enf_primaire
            + ars.ars_m.taux_college * enf_college
            + ars.ars_m.taux_lycee * enf_lycee
            )

        # Montant de l'ARS, avec ARS différentielle si les ressources sont supérieures au plafond (voir art. R543-6-1 du CSS)
        ars_montant = max_(0, arsbase - max_(0, (base_ressources - ars_plaf_res)))

        return ars_montant * (ars_montant >= ars.montant_minimum_verse)
