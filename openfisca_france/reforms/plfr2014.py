import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


# TODO: les baisses de charges n'ont pas été codées car annulées (toute ou en partie ?)
# par le Conseil constitutionnel

class plfr2014(Reform):
    name = 'Projet de Loi de Finances Rectificative 2014'

    class reduction_impot_exceptionnelle(Variable):
        definition_period = YEAR

        def formula_2013_01_01(foyer_fiscal, period, parameters):
            janvier = period.first_month

            nb_adult = foyer_fiscal('nb_adult', period)
            nb_parents = foyer_fiscal.declarant_principal.famille('nb_parents', period = janvier)
            rfr = foyer_fiscal('rfr', period)
            params = parameters(period).plfr2014.reduction_impot_exceptionnelle
            plafond = params.seuil * nb_adult + (nb_parents - nb_adult) * 2 * params.majoration_seuil
            montant = params.montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

    class reductions(Variable):
        label = "Somme des réductions d'impôt à intégrer pour l'année 2013"
        definition_period = YEAR

        def formula_2013_01_01(foyer_fiscal, period, parameters):
            accult = foyer_fiscal('accult', period)
            frais_de_comptabilite = foyer_fiscal('frais_de_comptabilite', period)
            cappme = foyer_fiscal('cappme', period)
            creaen = foyer_fiscal('creaen', period)
            accueil_dans_etablissement_personnes_agees = foyer_fiscal('accueil_dans_etablissement_personnes_agees', period)
            defense_forets_contre_incendies = foyer_fiscal('defense_forets_contre_incendies', period)
            dfppce = foyer_fiscal('dfppce', period)
            doment = foyer_fiscal('doment', period)
            domlog = foyer_fiscal('domlog', period)
            duflot = foyer_fiscal('duflot_pinel_denormandie_metropole', period)
            duflot_om = foyer_fiscal('duflot_pinel_denormandie_om', period)
            reduction_enfants_scolarises = foyer_fiscal('reduction_enfants_scolarises', period)
            gardenf = foyer_fiscal('gardenf', period)
            interets_paiements_differes_agriculteurs = foyer_fiscal('interets_paiements_differes_agriculteurs', period)
            investissement_forestier = foyer_fiscal('ri_investissement_forestier', period)
            invlst = foyer_fiscal('invlst', period)
            ip_net = foyer_fiscal('ip_net', period)
            location_meublee = foyer_fiscal('location_meublee', period)
            mecena = foyer_fiscal('mecena', period)
            mohist = foyer_fiscal('mohist', period)
            protection_patrimoine_naturel = foyer_fiscal('protection_patrimoine_naturel', period)
            prestations_compensatoires = foyer_fiscal('prestations_compensatoires', period)
            reduction_impot_exceptionnelle = foyer_fiscal('reduction_impot_exceptionnelle', period)
            interets_emprunt_reprise_societe = foyer_fiscal('interets_emprunt_reprise_societe', period)
            restauration_patrimoine_bati = foyer_fiscal('restauration_patrimoine_bati', period)
            rente_survie = foyer_fiscal('rente_survie', period)
            saldom = foyer_fiscal('ri_saldom', period)
            scelli = foyer_fiscal('scelli', period)
            sofica = foyer_fiscal('sofica', period)
            souscriptions_parts_fcpi_fip = foyer_fiscal('souscriptions_parts_fcpi_fip', period)
            total_reductions = accult + frais_de_comptabilite + cappme + creaen + accueil_dans_etablissement_personnes_agees + defense_forets_contre_incendies + dfppce + doment + domlog +\
                duflot + duflot_om + reduction_enfants_scolarises + gardenf + interets_paiements_differes_agriculteurs + investissement_forestier + invlst + location_meublee + mecena + mohist + protection_patrimoine_naturel +\
                prestations_compensatoires + interets_emprunt_reprise_societe + restauration_patrimoine_bati + rente_survie + saldom + scelli + sofica + souscriptions_parts_fcpi_fip + reduction_impot_exceptionnelle
            return min_(ip_net, total_reductions)

    def apply(self):
        for variable in [self.reduction_impot_exceptionnelle, self.reductions]:
            self.update_variable(variable)
        self.modify_parameters(modifier_function = modify_parameters)


def modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'plfr2014.yaml')
    plfr2014_parameters_subtree = load_parameter_file(name='plfr2014', file_path=file_path)

    file_path = os.path.join(dir_path, 'plfrss2014.yaml')
    plfrss2014_parameters_subtree = load_parameter_file(name='plfrss2014', file_path=file_path)

    parameters.add_child('plfr2014', plfr2014_parameters_subtree)
    parameters.add_child('plfrss2014', plfrss2014_parameters_subtree)
    return parameters
