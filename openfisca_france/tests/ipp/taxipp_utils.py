# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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


import os
import pdb

from numpy import array
from pandas import DataFrame, ExcelFile, read_stata, Series

from ... import init_country
from ...surveys import SurveyScenario


current_dir = os.path.dirname(os.path.realpath(__file__))
variables_corresp = os.path.join(current_dir, 'correspondances_variables.xlsx')


def build_ipp2of_variables():
    '''
    Création du dictionnaire dont les clefs sont les noms des variables IPP
    et les arguments ceux des variables OF
    '''
    def _dic_corresp(onglet):
        names = ExcelFile(variables_corresp).parse(onglet)
        return dict(array(names.loc[names['equivalence'].isin([1, 5, 8]), ['var_TAXIPP', 'var_OF']]))

    ipp2of_input_variables = _dic_corresp('input')
    ipp2of_output_variables = _dic_corresp('output')
    return ipp2of_input_variables, ipp2of_output_variables


def compare(path_dta_output, ipp2of_output_variables, param_scenario, simulation, threshold = 1.5, verbose = True):
    '''
    Fonction qui comparent les calculs d'OF et et de TaxIPP
    Gestion des outputs
    '''
    ipp_output = read_stata(path_dta_output).sort(['id_foyf', 'id_indiv'], ascending = [True, False]).reset_index()
    if 'salbrut' in param_scenario.items():
        if param_scenario['option'] == 'brut':
            del ipp2of_output_variables['sal_brut']
            del ipp2of_output_variables['chom_brut']
            del ipp2of_output_variables['rst_brut']
    scenario = param_scenario['scenario']
    if 'activite' in param_scenario:
        act = param_scenario['activite']
    else:
        act = 0
    if 'activite_C' in param_scenario:
        act_conj = param_scenario['activite_C']
    else:
        act_conj = 0

    check_list_commun = ['isf_foy', 'irpp_tot_foy', 'irpp_bar_foy', 'ppe_brut_foy', 'ppe_net_foy', 'irpp_ds_foy',
                         'taxe_HR_foy']  # # 'decote_irpp_foy',
    check_list_minima = ['rsa_foys', 'rsa_act_foys', 'mv_foys', 'rsa_logt']  # , 'y_rmi_rsa'
    check_list_af = [
        'paje_foys', 'paje_base_foys', 'paje_clca_foys', 'af_foys', 'nenf_prest', 'biact_or_isole', 'alf_foys',
        'ars_foys', 'asf_foys', 'api', 'apje_foys',
        # 'af_diff', 'af_maj',
        ]
    check_list_sal = [
        'csp_exo', 'csg_sal_ded', 'css', 'css_co', 'css_nco', 'crds_sal', 'csg_sal_nonded', 'sal_irpp', 'sal_brut',
        'csp_mo_vt', 'csp_nco', 'csp_co', 'vtmo', 'sal_superbrut', 'sal_net', 'ts', 'tehr',
        # 'csg_sal_ded'] #, 'irpp_net_foy', 'af_foys']- cotisations salariales : 'css', 'css_nco', 'css_co',
        # 'sal_superbrut' 'csp',
        ]
    # 'decote_irpp_foy' : remarque par d'équivalence Taxipp
    check_list_chom = ['csg_chom_ded', 'chom_irpp', 'chom_brut', 'csg_chom_nonded', 'crds_chom']
    check_list_ret = ['csg_pens_ded', 'pension_irpp', 'pension_net', 'csg_pens_nonded', 'crds_pens']
    check_list_cap = ['isf_foy', 'isf_brut_foy', 'isf_net_foy', 'csg_patr_foy', 'crds_patr_foy', 'csk_patr_foy',
                      'csg_plac_foy', 'crds_plac_foy', 'csk_plac_foy']

    if 'salbrut' in param_scenario.items():
        if param_scenario['option'] == 'brut':
            check_list_sal.remove('sal_brut')
            check_list_chom.remove('chom_brut')

    id_list = act + act_conj
    lists = {
        0: check_list_sal,
        1: check_list_sal + check_list_chom,
        2: check_list_chom,
        3: check_list_sal + check_list_ret,
        4: check_list_chom + check_list_ret,
        6: check_list_ret,
        }
    check_list = lists[id_list]

    if (scenario == 'celib') & (act == 3):
        check_list = check_list_ret
    check_list += check_list_minima + check_list_commun + check_list_af + check_list_cap

    def _relevant_input_variables(simulation):
        input_variables = {'ind': list(), 'foy': list(), 'men': list()}
        len_indiv = simulation.entity_by_key_plural['individus'].count
        len_men = simulation.entity_by_key_plural['menages'].count
        for name, col in simulation.tax_benefit_system.column_by_name.iteritems():
            # print name, col
            holder = simulation.get_holder(name, default = None)
            if holder is not None and holder.array is not None:
                if not all(holder.array == col.default):
                    if len(holder.array) == len_indiv:
                        input_variables['ind'].append(name)
                    elif len(holder.array) == len_men:
                        input_variables['men'].append(name)
                    else:
                        input_variables['foy'].append(name)
        return input_variables

    def _conflict_by_entity(simulation, of_var_holder, ipp_var, pb_calcul, ipp_output = ipp_output):
        of_var_series = Series(of_var_holder.array)
        entity = of_var_holder.entity
        if entity.is_persons_entity:
            quimen_series = Series(simulation.get_holder('quimen').array)
            of_var_series = of_var_series[quimen_series.isin([0, 1])].reset_index(drop = True)
            ipp_var_series = ipp_output[ipp_var]
            # print ipp_var
            # print ipp_var_series
            # print of_var_series
            # print "\n"
        else:
            quient_series = Series(simulation.get_holder('qui' + entity.symbol).array)
            quient_0 = quient_series[quient_series == 0]
            quient_1 = quient_series[quient_series == 1]
            long = range(len(quient_0))
            if len(quient_1) > 0:
                long = [2 * x for x in long]
            ipp_var_series = ipp_output.loc[long, ipp_var].reset_index(drop = True)

        conflict = ((ipp_var_series.abs() - of_var_series.abs()).abs() > threshold)
        idmen = simulation.get_holder('idmen').array
        conflict_selection = DataFrame({'idmen': idmen, 'idfoy': simulation.get_holder('idfoy').array})
        conflict_men = conflict_selection.loc[conflict[conflict == True].index, 'idmen'].drop_duplicates().values  # noqa
        conflict_foy = conflict_selection.loc[conflict[conflict == True].index, 'idfoy'].drop_duplicates().values  # noqa
        if (len(ipp_var_series[conflict]) != 0):
            if verbose:
                print u"Le calcul de {} pose problème : ".format(of_var)
                print DataFrame({
                    "IPP": ipp_var_series[conflict],
                    "OF": of_var_series[conflict],
                    "diff.": ipp_var_series[conflict].abs() - of_var_series[conflict].abs(),
                    }).to_string()
                relevant_variables = _relevant_input_variables(simulation)
                print relevant_variables
                input = {}
                for entity in ['ind', 'men', 'foy']:
                    dic = {}
                    for variable in relevant_variables[entity]:
                        dic[variable] = simulation.get_holder(variable).array
                    input[entity] = DataFrame(dic)
                print "Variables individuelles associées à ce ménage:"
                print input['ind'].loc[input['ind']['idmen'].isin(conflict_men)].to_string()
                # .loc[conflict[conflict == True].index].to_string()
                if not input['men'].empty:
                    print "Variables associées au ménage:"
                    print input['men'].loc[conflict_men].to_string()
                if not input['foy'].empty:
                    print "Variables associées au foyer fiscal:"
                    print input['foy'].loc[conflict_foy].to_string()
            pb_calcul += [of_var]
#        if of_var == 'taxes_sal':
#            print "taxes_sal", output1.to_string
#                pdb.set_trace()

    pb_calcul = []
    for ipp_var in check_list:  # in ipp2of_output_variables.keys():
        of_var = ipp2of_output_variables[ipp_var]
        of_var_holder = simulation.compute(of_var)
        _conflict_by_entity(simulation, of_var_holder, ipp_var, pb_calcul)
    if verbose:
        print pb_calcul
    return pb_calcul


def run_OF(ipp2of_input_variables, path_dta_input, param_scenario = None, dic = None,
           datesim = None, option = 'test_dta'):
    '''
    Lance le calculs sur OF à partir des cas-types issues de TaxIPP
    input : base .dta issue de l'étape précédente
    '''
    def _test_of_dta(dta_input, dic):
        ''' Cette fonction teste que la table .dta trouvée
        correspond au bon scénario '''
        data = read_stata(dta_input)
        dic_dta = data.loc[0, 'dic_scenar']
        if str(dic) != str(dic_dta):
            print "La base .dta permettant de lancer la simulation OF est absente "
            print "La base s'en rapprochant le plus a été construite avec les paramètres : ", dic_dta
            pdb.set_trace()
        else:
            data = data.drop('dic_scenar', 1).sort(['id_foyf', 'id_indiv'], ascending = [True, False])
        return data

    def _scenar_dta(dta_input):
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

    if 'option' in param_scenario.keys() and param_scenario['option'] == 'brut':
        TaxBenefitSystem = init_country(start_from = "brut")
        tax_benefit_system = TaxBenefitSystem()
        del ipp2of_input_variables['sal_irpp_old']
        ipp2of_input_variables['sal_brut'] = 'salbrut'
        ipp2of_input_variables['chom_brut'] = 'chobrut'
        ipp2of_input_variables['pension_brut'] = 'rstbrut'
    else:
        tax_benefit_system_class = init_country()
        tax_benefit_system = tax_benefit_system_class()
    openfisca_survey = build_input_OF(data_IPP, ipp2of_input_variables, tax_benefit_system)
    openfisca_survey = openfisca_survey.fillna(0)  # .sort(['idfoy'])
#    simulation = surveys.new_simulation_from_survey_data_frame(
#        # debug = True,
#        survey = openfisca_survey,
#        tax_benefit_system = tax_benefit_system,
#        year = datesim,
#        )
    survey_scenario = SurveyScenario().init_from_data_frame(
        input_data_frame = openfisca_survey,
        tax_benefit_system_class = tax_benefit_system_class,
        year = datesim,
        )
    if option == 'list_dta':
        return survey_scenario.new_simulation(), param_scenario
    else:
        return survey_scenario.new_simulation()


def build_input_OF(data, ipp2of_input_variables, tax_benefit_system):

    def _qui(data, entity):
        qui = "qui" + entity
        id = "id" + entity
        data[qui] = 2
        data.loc[data['decl'] == 1, qui] = 0
        data.loc[data['conj'] == 1, qui] = 1
        if entity == "men":
            data.loc[data['con2'] == 1, qui] = 1
        j = 2
        while any(data.duplicated([qui, id])):
            data.loc[data.duplicated([qui, id]), qui] = j + 1
            j += 1
        return data[qui]

    def _statut_occupation(data):
        data["statut_occupation"] = 0
        data.loc[data['proprio_empr'] == 1, 'statut_occupation'] = 1
        data.loc[data['proprio'] == 1, 'statut_occupation'] = 2
        data.loc[data['locat'] == 1, 'statut_occupation'] = 4
        data.loc[data['loge'] == 1, 'statut_occupation'] = 6
        return data['statut_occupation']

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
        data["f7ef"] = _count_by_entity(data, 'age', 'foy', [18, 99])  # nb enfants ff enseignement sup > 17
        data = data.drop(["nenf1113", "nenf1415", "nenf1617", "nenfmaj1819", "nenfmaj20", "nenfmaj21plus", "nenfnaiss",
                          "nenf02", "nenf35", "nenf610"], axis = 1)
        data.index = range(len(data))
        return data

    def _workstate(data):
        # TODO: titc should be filled in to deal with civil servant
        data['chpub'] = 0
        data.loc[data['public'] == 1, 'chpub'] = 1
        data.loc[data['public'] == 0, 'chpub'] = 6
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
        data['taux_csg_remplacement'] = 3
        data.loc[data['csg_exo'] == 1, 'taux_csg_remplacement'] = 1
        data.loc[data['csg_part'] == 1, 'taux_csg_remplacement'] = 2
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
        data.loc[(data['activite'] == 0) & (data['salaire_imposable'] == 0), 'inactif'] = 1
        data['partiel1'] = 0
        data.loc[(data['nbh'] / 12 <= 77) & (data['nbh'] / 12 > 0), 'partiel1'] = 1
        data['partiel2'] = 0
        data.loc[(data['nbh'] / 12 <= 151) & (data['nbh'] / 12 > 77), 'partiel2'] = 1
        return data

    data.rename(columns = ipp2of_input_variables, inplace = True)
    data['quifoy'] = _qui(data, 'foy')
    min_idfoy = data["idfoy"].min()
    if min_idfoy > 0:
        data["idfoy"] -= min_idfoy
    data['quimen'] = _qui(data, 'men')
    min_idmen = data["idmen"].min()
    if min_idmen > 0:
        data["idmen"] -= min_idmen
    data["idfam"] = data["idmen"]
    data["quifam"] = data['quimen']

    # print data[['idfoy','idmen', 'quimen','quifoy', 'decl', 'conj', 'con2']].to_string()
    data['statut_occupation'] = _statut_occupation(data)
    data = _count_enf(data)
    data = _workstate(data)
    data["caseN"] = _compl(data["caseN"])
    data = _var_to_ppe(data)
    data = _var_to_pfam(data)
    data['invalide'] = 0

    variables_to_drop = [
        variable
        for variable in data.columns
        if variable not in tax_benefit_system.column_by_name
        ]
    data = data.drop(variables_to_drop, axis = 1)
#    data.rename(columns = {"id_conj" : "conj"}, inplace = True)
    data['age_en_mois'] = data['age'] * 12
    return data
