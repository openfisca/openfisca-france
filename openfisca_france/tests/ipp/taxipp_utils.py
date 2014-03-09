# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os
import pdb
import sys
import time

from numpy import array
from pandas import read_stata, ExcelFile, DataFrame

import openfisca_france
# from openfisca_core import model
# from openfisca_core.simulations import SurveySimulation
# openfisca_france.init_country()

current_dir = os.path.dirname(os.path.realpath(__file__))
variables_corresp = os.path.join(current_dir, 'correspondances_variables.xlsx')


def dic_ipp2of():
    ''' 
    Création du dictionnaire dont les clefs sont les noms des variables IPP
    et les arguments ceux des variables OF 
    '''
    def _dic_corresp(onglet):
        names = ExcelFile(variables_corresp).parse(onglet)
        names = array(names.loc[names['equivalence'].isin([1, 5, 8]), ['var_TAXIPP', 'var_OF']])
        dic = {}
        for i in range(len(names)) :
            dic[names[i, 0]] = names[i, 1]
        return dic

    ipp2of_input_variables = _dic_corresp('input')
    ipp2of_output_variables = _dic_corresp('output')
    return ipp2of_input_variables, ipp2of_output_variables

def compare(path_dta_output, openfisca_output, dic_ipp2of_output_variables, param_scenario, simulation, threshold = 1.5, verbose = True):
    '''
    Fonction qui comparent les calculs d'OF et et de TaxIPP
    Gestion des outputs
    '''
    openfisca_input = simulation.input_table.table
    dta_output = path_dta_output
    ipp_output = read_stata(dta_output).sort(['id_foyf', 'id_indiv'], ascending = [True, False])
    ipp2of_output_variables = dic_ipp2of_output_variables
    if 'salbrut' in param_scenario.items() :
        if param_scenario['option'] == 'salbrut':
            del ipp2of_output_variables['sal_brut']

    scenario = param_scenario['scenario']
    if 'activite' in param_scenario.items():
        act = param_scenario['activite']
    else:
        act = 0
    if 'activite_C' in param_scenario.items():
        act_conj = param_scenario['activite_C']
    else:
        act_conj = 0

    check_list_commun = ['isf_foy', 'irpp_net_foy', 'irpp_bar_foy', 'ppe_brut_foy', 'ppe_net_foy', 'irpp_ds_foy']  # # 'decote_irpp_foy',
    check_list_minima = ['rsa_foys', 'rsa_act_foys', 'mv_foys', 'rsa_logt', 'y_rmi_rsa']
    check_list_af = ['paje_foys', 'paje_base_foys', 'paje_clca_foys', 'af_foys', 'nenf_prest', 'biact_or_isole', 'alf_foys', 'ars_foys', 'asf_foys', 'api', 'apje_foys']  # 'af_diff', 'af_maj',
    check_list_sal = ['csp_exo', 'csg_sal_ded', 'css', 'css_co', 'css_nco', 'crds_sal', 'csg_sal_nonded', 'sal_irpp', 'sal_brut', 'csp_mo_vt', 'csp_nco', 'csp_co', 'vt', 'mo', 'sal_superbrut', 'sal_net', 'ts', 'tehr']  # 'csg_sal_ded'] #, 'irpp_net_foy', 'af_foys']- cotisations salariales : 'css', 'css_nco', 'css_co', 'sal_superbrut' 'csp',
    # 'decote_irpp_foy' : remarque par d'équivalence Taxipp
    check_list_chom = ['csg_chom_ded', 'chom_irpp', 'chom_brut', 'csg_chom_nonded', 'crds_chom']
    check_list_ret = ['csg_pens_ded', 'pension_irpp', 'pension_net', 'csg_pens_nonded', 'crds_pens']
    check_list_cap = ['isf_foy', 'isf_brut_foy', 'isf_net_foy', 'csg_patr_foy', 'crds_patr_foy', 'csk_patr_foy', 'csg_plac_foy', 'crds_plac_foy', 'csk_plac_foy']

    if 'salbrut' in param_scenario.items() :
        if param_scenario['option'] == 'salbrut':
            check_list_sal.remove('sal_brut')

    id_list = act + act_conj
    lists = {0 : check_list_sal, 1: check_list_sal + check_list_chom, 2: check_list_chom, 3 : check_list_sal + check_list_ret, 4 : check_list_chom + check_list_ret, 6 : check_list_ret}
    check_list = lists[id_list]

    if (scenario == 'celib') & (act == 3):
        check_list = check_list_ret
    check_list += check_list_minima + check_list_commun + check_list_af + check_list_cap

    def _relevant_input_variables(simulation):
        dataframe = simulation.input_table.table
        input_variables = list()
        for name, col in simulation.column_by_name.iteritems():
            if not all(dataframe[name] == col._default):
                input_variables.append(name)
        return input_variables

    def _conflict_by_entity(simulation, ent, of_var, ipp_var, pb_calcul, output1 = openfisca_output, input1 = openfisca_input, output2 = ipp_output):
        output2.index = output1[input1['quimen'].isin([0, 1])].index
        if ent == 'ind':
            output1 = output1.loc[input1['quimen'].isin([0, 1]), of_var]
            output2 = output2[ipp_var]
        else :
            output1 = output1.loc[ input1['qui' + ent] == 0, of_var]
            output2 = output2.loc[ input1['qui' + ent] == 0, ipp_var]
            input1 = input1.loc[ input1['qui' + ent] == 0, :]

        conflict = ((output2.abs() - output1.abs()).abs() > threshold)
        if (len(output2[conflict]) != 0) :
            if verbose:
                print "Le calcul de " + of_var + " pose problème : "
                from pandas import DataFrame
                # print DataFrame( {"IPP": output2, "OF": output1, "diff.": output2-output1.abs()} ).to_string()
                print DataFrame({"IPP": output2[conflict], "OF": output1[conflict], "diff.": output2[conflict] - output1[conflict].abs()}).to_string()
                relevant_variables = _relevant_input_variables(simulation)
                print input1.loc[conflict[conflict == True].index, relevant_variables].to_string()
            pb_calcul += [of_var]
#        if of_var == 'taxes_sal':
#            print "taxes_sal", output1.to_string
#                pdb.set_trace()

    pb_calcul = []
    for ipp_var in check_list:  # in ipp2of_output_variables.keys(): #
        of_var = ipp2of_output_variables[ipp_var]
        entity = simulation.prestation_by_name[of_var].entity
        _conflict_by_entity(simulation, str(entity), of_var, ipp_var, pb_calcul)
    if verbose:
        print pb_calcul
    return pb_calcul

def run_OF(dic_input, path_dta_input, param_scenario = None, dic = None, datesim = None, option = 'test_dta'):

    '''
    Lance le calculs sur OF à partir des cas-types issues de TaxIPP
    input : base .dta issue de l'étape précédente
    '''
    def _test_of_dta(dta_input, dic):
        ''' Cette fonction teste que la table .dta trouvée 
        correspond au bon scénario '''
        data = read_stata(dta_input)
        dic_dta = data.loc[0, 'dic_scenar']
        if str(dic) != str(dic_dta) :
            print "La base .dta permettant de lancer la simulation OF est absente "
            print "La base s'en rapprochant le plus a été construite avec les paramètres : ", dic_dta
            pdb.set_trace()
        else :
            data = data.drop('dic_scenar', 1).sort(['id_foyf', 'id_indiv'], ascending = [True, False])
        return data

    def _scenar_dta(dta_input) :
        ''' cette fonction identifie le scenario enregistré dans la table d'input '''
        data = read_stata(dta_input)
        dic_dta = data.loc[0, 'dic_scenar']
        data = data.drop('dic_scenar', 1).sort(['id_foyf', 'id_indiv'], ascending = [True, False])
        return dic_dta, data

    if option == 'test_dta':
        data_IPP = _test_of_dta(path_dta_input, dic)
    if option == 'list_dta':
        dic_scenar, data_IPP = _scenar_dta(path_dta_input)
        dict_scenar = dict()
        expression = "dict_scenar.update(" + dic_scenar + ")"
        eval(expression)
        datesim = dict_scenar['datesim']
        param_scenario = dict_scenar

    if 'salbrut' in param_scenario.items() :
        if param_scenario['option'] == 'salbrut':
            TaxBenefitSystem = openfisca_france.init_country(start_from = "brut")
            tax_benefit_system = TaxBenefitSystem()
            del dic_input['sal_irpp_old']
            dic_input['sal_brut'] = 'salbrut'
        else :
            TaxBenefitSystem = openfisca_france.init_country()
            tax_benefit_system = TaxBenefitSystem()

    else :
        TaxBenefitSystem = openfisca_france.init_country()
        tax_benefit_system = TaxBenefitSystem()

    openfisca_survey = build_input_OF(data_IPP, dic_input)
    openfisca_survey = openfisca_survey.fillna(0)  # .sort(['idfoy','noi'])
    simulation = SurveySimulation()
    simulation.set_config(year = datesim,
                          survey_filename = openfisca_survey,
                          param_file = os.path.join(os.path.dirname(model.PARAM_FILE), 'param.xml'))
    simulation.set_param()
    simulation.compute()

    if option == 'list_dta':
        return simulation, simulation.output_table.table, param_scenario
    else:
        return simulation, simulation.output_table.table

def build_input_OF(data, dic_var):

    def _qui(data, entity):
        qui = "qui" + entity
        id = "id" + entity
        data[qui] = 2
        data.loc[data['decl'] == 1, qui] = 0
        data.loc[data['conj'] == 1, qui] = 1
        if entity == "men" :
            data.loc[data['con2'] == 1, qui] = 1
        j = 2
        while any(data.duplicated([qui, id])):
            data.loc[data.duplicated([qui, id]), qui] = j + 1
            j += 1
        return data[qui]

    def _so(data):
        data["so"] = 0
        data.loc[data['proprio_empr'] == 1, 'so'] = 1
        data.loc[data['proprio'] == 1, 'so'] = 2
        data.loc[data['locat'] == 1, 'so'] = 4
        data.loc[data['loge'] == 1, 'so'] = 6
        return data['so']

    def _compl(var):
        var = 1 - var
        var = var.astype(int)
        return var

    def _count_by_entity(data, var, entity, bornes):
        ''' Compte le nombre de 'var compris entre les 'bornes' au sein de l''entity' '''
        id = 'id' + entity
        qui = 'qui' + entity
        data.index = data[id]
        cond = (bornes[0] <= data[var]) & (data[var] <= bornes[1]) & (data[qui] > 1)
        col = DataFrame(data.loc[cond, :].groupby(id).size(), index = data.index).fillna(0)
        col.reset_index()
        return col

    def _count_enf(data):
        data["f7ea"] = _count_by_entity(data, 'age', 'foy', [11, 14])  # nb enfants ff au collège (11-14)
        data["f7ec"] = _count_by_entity(data, 'age', 'foy', [15, 17])  # #nb enfants ff au lycée  15-17
        data["f7ef"] = _count_by_entity(data, 'age', 'foy', [18, 99])  # nb enfants ff enseignement sup >17
        data = data.drop(["nenf1113", "nenf1415", "nenf1617", "nenfmaj1819", "nenfmaj20", "nenfmaj21plus", "nenfnaiss", "nenf02", "nenf35", "nenf610"], axis = 1)
        data.index = range(len(data))
        return data

    def _workstate(data):
        # TODO: titc should be filled in to deal with civil servant
        data['chpub'] = 0
        data.loc[data['public'] == 1, 'chpub'] = 1
        data.loc[data['public'] == 0, 'chpub' ] = 6
        # Activité : [0'Actif occupé',  1'Chômeur', 2'Étudiant, élève', 3'Retraité', 4'Autre inactif']), default = 4)
        # act5 : [0"Salarié",1"Indépendant",2"Chômeur",3"Retraité",4"Inactif"]
        data['act5'] = 0
        data.loc[(data['activite'] == 0) & (data['stat_prof'] == 1), 'act5'] = 1
        data.loc[data['activite'] == 1, 'act5'] = 2
        data.loc[data['activite'] == 3, 'act5'] = 3
        data.loc[data['activite'].isin([2, 4]), 'act5'] = 4
        data['statut'] = 8
        data.loc[data['public'] == 1, 'statut'] = 11
        # [0"Non renseigné/non pertinent",1"Exonéré",2"Taux réduit",3"Taux plein"]
        data['csg_rempl'] = 3
        data.loc[data['csg_exo'] == 1, 'csg_rempl'] = 1
        data.loc[data['csg_part'] == 1, 'csg_rempl'] = 2
        data = data.drop(['csg_tout', 'csg_exo', 'csg_part'], axis = 1)
        # data['ebic_impv'] = 20000
        data['exposition_accident'] = 0
        return data

    def _var_to_ppe(data):
        data['ppe_du_sa'] = 0
        data.loc[data['stat_prof'] == 0, 'ppe_du_sa'] = data.loc[data['stat_prof'] == 0, 'nbh']
        data['ppe_du_ns'] = 0
        data.loc[data['stat_prof'] == 1, 'ppe_du_ns'] = data.loc[data['stat_prof'] == 1, 'nbj']

        data['ppe_tp_sa'] = 0
        data.loc[(data['stat_prof'] == 0) & (data['nbh'] >= 151.67 * 12), 'ppe_tp_sa'] = 1
        data['ppe_tp_ns'] = 0
        data.loc[(data['stat_prof'] == 1) & (data['nbj'] >= 360), 'ppe_tp_ns'] = 1
        return data

    def _var_to_pfam(data):
        data['inactif'] = 0
        data.loc[(data['activite'].isin([3, 4, 5, 6])), 'inactif'] = 1
        data.loc[(data['activite'] == 1) & (data['choi'] == 0), 'inactif'] = 1
        data.loc[(data['activite'] == 0) & (data['sali'] == 0), 'inactif'] = 1
        data['partiel1'] = 0
        data.loc[(data['nbh'] / 12 <= 77) & (data['nbh'] / 12 > 0) , 'partiel1'] = 1
        data['partiel2'] = 0
        data.loc[(data['nbh'] / 12 <= 151) & (data['nbh'] / 12 > 77), 'partiel2'] = 1
        return data

    data.rename(columns = dic_var, inplace = True)

    data["agem"] = 12 * data["age"]
    data['quifoy'] = _qui(data, 'foy')
    data['quimen'] = _qui(data, 'men')
    data["idfam"] = data["idmen"]
    data["quifam"] = data['quimen']

    # print data[['idfoy','idmen', 'quimen','quifoy', 'decl', 'conj', 'con2']].to_string()
    data['so'] = _so(data)
    data = _count_enf(data)
    data = _workstate(data)
    data["caseN"] = _compl(data["caseN"])
    data = _var_to_ppe(data)
    data = _var_to_pfam(data)

    not_in_OF = [ "p1", "nbh", "nbh_sal", "loge_proprio", "loge_locat", "loge_autr", "loyer_fictif", "loyer_verse", "loyer_marche", "pens_alim_ver_foy", "sal_brut", "sal_h_brut",
                 "bail_prive", "bail_pers_phys", "loyer_conso", "proprio_men", "locat_men", "loge_men", "proprio_empr_men", "loyer_fictif_men",
                 "bail_prive_men", "bail_pers_phys_men", "loyer_marche_men", "loyer_conso_men",
                    "nonsalexo_irpp", "nonsal_brut_cn", "nonsal_brut_cn_foy", "nonsal_brut", "nonsal_h_brut"]  # variables non-salariés, "ba_irpp",  "bic_irpp",  "bnc_irpp",
    other_vars_to_drop = ["couple", "decl", "conj", "pac", "proprio_empr", "proprio", "locat", "nonsal_irpp", "nadul",
                  "loge", "marie", "change", "pondv", "concu", "cohab", "nenf_concu", "num_indf", "npers", "age_conj", "n_foy_men", "public"]
    vars_to_drop = [var for var in (other_vars_to_drop + not_in_OF) if var in data.columns]
    data = data.drop(vars_to_drop, axis = 1)
    data.rename(columns = {"id_conj" : "conj"}, inplace = True)
    return data

