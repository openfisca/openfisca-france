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


import collections
from datetime import date

from openfisca_core.columns import BoolPresta, FloatPresta, IntPresta, EnumPresta
from openfisca_core.enumerations import Enum

from .. import entities
from ..formulas import SimpleFormula
from . import calage as cl
from . import common as cm
from .cotisations_sociales import capital as cs_capital
from .cotisations_sociales import travail as cs_travail
from .cotisations_sociales import remplacement as cs_remplac
from .cotisations_sociales import lps as cs_lps  # TODO: remove frome here

from . import irpp as ir
from . import irpp_charges_deductibles as cd
from . import irpp_credits_impots as ci
from . import irpp_plus_values_immo as immo
from . import irpp_reductions_impots as ri
from . import isf as isf
from . import lgtm as lg
from . import mini as ms
from . import pfam as pf
from . import th as th
from . import inversion_revenus as inv_rev


def _noi(noi):
    return noi


def _men(idmen, _option = {'idmen': [0]}):
    return idmen


def _fam(idfam, _option = {'idfam': [0]}):
    return idfam


def _foy(idfoy, _option = {'idfoy': [0]}):
    return idfoy


def _quimen(quimen):
    return quimen


def _quifam(quifam):
    return quifam


def _quifoy(quifoy):
    return quifoy


def _wprm(wprm):
    return wprm


def build_simple_formula_couple(name, prestation):
    assert isinstance(name, basestring), name
    name = unicode(name)
    prestation.formula_constructor = type(name.encode('utf-8'), (SimpleFormula,), dict(
        calculate = staticmethod(prestation._func),
        ))
    del prestation._func
    if prestation.label is None:
        prestation.label = name
    assert prestation.name is None
    prestation.name = name

    entity_column_by_name = entities.entity_class_by_symbol[prestation.entity].column_by_name
    assert name not in entity_column_by_name, name
    entity_column_by_name[name] = prestation

    return (name, prestation)


prestation_by_name = collections.OrderedDict((
    ############################################################
    # Reproduction des identifiants
    ############################################################
    build_simple_formula_couple('noi_ind', FloatPresta(_noi)),
    build_simple_formula_couple('idmen_ind', FloatPresta(_men)),
    build_simple_formula_couple('idmen_foy', EnumPresta(_men, entity = "foy")),
    build_simple_formula_couple('idmen_men', EnumPresta(_men, entity = "men")),
    build_simple_formula_couple('idmen_fam', EnumPresta(_men, entity = "fam")),
    build_simple_formula_couple('idfam_ind', FloatPresta(_fam)),
    build_simple_formula_couple('idfam_foy', EnumPresta(_fam, entity = "foy")),
    build_simple_formula_couple('idfam_men', EnumPresta(_fam, entity = "men")),
    build_simple_formula_couple('idfam_fam', EnumPresta(_fam, entity = "fam")),
    build_simple_formula_couple('idfoy_ind', FloatPresta(_foy)),
    build_simple_formula_couple('idfoy_foy', EnumPresta(_foy, entity = "foy")),
    build_simple_formula_couple('idfoy_men', EnumPresta(_foy, entity = "men")),
    build_simple_formula_couple('idfoy_fam', EnumPresta(_foy, entity = "fam")),

    build_simple_formula_couple('quimen_ind', EnumPresta(_quimen)),
    build_simple_formula_couple('quifam_ind', EnumPresta(_quifam)),
    build_simple_formula_couple('quifoy_ind', EnumPresta(_quifoy)),

    ############################################################
    # Reproduction des pondérations
    ############################################################
    build_simple_formula_couple('wprm_ind', FloatPresta(_wprm, entity = "ind", label = u"Effectifs", survey_only = True,)),
    build_simple_formula_couple('wprm_fam', FloatPresta(_wprm, entity = "fam", label = u"Effectifs", survey_only = True,)),
    build_simple_formula_couple('wprm_foy', FloatPresta(_wprm, entity = "foy", label = u"Effectifs", survey_only = True,)),

    build_simple_formula_couple('mhsup', FloatPresta(cs_travail._mhsup)),
    build_simple_formula_couple('alv', FloatPresta(ir._alv)),

    ############################################################
    # Cotisations sociales
    ############################################################

    # Salaires
    build_simple_formula_couple('type_sal', EnumPresta(cs_travail._type_sal, label = u"Catégorie de salariés")),
    build_simple_formula_couple('salbrut', FloatPresta(inv_rev._salbrut, label = u"Salaire brut ou traitement indiciaire brut")),
    build_simple_formula_couple('primes', FloatPresta(cs_travail._primes, label = u"Primes et indemnités des fonctionnaires")),
    build_simple_formula_couple('sal_h_b', FloatPresta(cs_travail._sal_h_b, label = u"Salaire horaire brut")),
    build_simple_formula_couple('taille_entreprise', EnumPresta(cs_travail._taille_entreprise,
                                    label = u"Catégorie de taille d'entreprise (pour calcul des cotisations sociales)",
                                    enum = Enum([u"Non pertienent",
                                                 u"Moins de 10 salariés",
                                                 u"De 10 à 19 salariés",
                                                 u"De 20 à 249 salariés",
                                                 u"Plus de 250 salariés"]))),

    build_simple_formula_couple('cotpat_contrib', FloatPresta(cs_travail._cotpat_contrib, label = u"Cotisations sociales patronales contributives")),
    build_simple_formula_couple('taux_accident_travail', FloatPresta(cs_travail._taux_accident_travail, label = u"Cotisations sociales patronales : accident du travail et maladies professionnelles")),
    build_simple_formula_couple('cotpat_accident', FloatPresta(cs_travail._cotpat_accident, label = u"Cotisations sociales patronales : accident du travail et maladies professionnelles")),
    build_simple_formula_couple('cotpat_noncontrib', FloatPresta(cs_travail._cotpat_noncontrib, label = u"Cotisations sociales patronales non contributives")),
    build_simple_formula_couple('cotpat_main_d_oeuvre', FloatPresta(cs_travail._cotpat_main_d_oeuvre, label = u"Cotisations sociales patronales main d'oeuvre")),
    build_simple_formula_couple('cotpat_transport', FloatPresta(cs_travail._cotpat_transport, label = u"Cotisations sociales patronales: versement transport")),
    build_simple_formula_couple('cotpat', FloatPresta(cs_travail._cotpat, label = u"Cotisations sociales patronales")),
    build_simple_formula_couple('alleg_fillon', FloatPresta(cs_travail._alleg_fillon, label = u"Allègements Fillon sur les bas salaires")),
    build_simple_formula_couple('alleg_cice', FloatPresta(cs_travail._alleg_cice, label = u"Crédit d'impôt compétitivité emploi")),
    build_simple_formula_couple('taxes_sal', FloatPresta(cs_travail._taxes_sal, label = u"Taxes sur les salaires pour les employeurs non soumis à la TVA")),
    build_simple_formula_couple('tehr', FloatPresta(cs_travail._tehr, label = u"Taxes exceptionnelles sur les hauts revenus")),
    build_simple_formula_couple('salsuperbrut', FloatPresta(cs_travail._salsuperbrut, label = u"Salaires super bruts")),

    build_simple_formula_couple('cotsal_contrib', FloatPresta(cs_travail._cotsal_contrib, label = u"Cotisations sociales salariales contributives")),
    build_simple_formula_couple('cotsal_noncontrib', FloatPresta(cs_travail._cotsal_noncontrib, label = u"Cotisations sociales non salariales non-contributives")),
    build_simple_formula_couple('cotsal', FloatPresta(cs_travail._cotsal, label = u"Cotisations sociales salariales")),

    build_simple_formula_couple('csgsald', FloatPresta(cs_travail._csgsald, label = u"CSG déductible sur les salaires")),
    build_simple_formula_couple('csgsali', FloatPresta(cs_travail._csgsali, label = u"CSG imposables sur les salaires")),
    build_simple_formula_couple('crdssal', FloatPresta(cs_travail._crdssal, label = u"CRDS sur les salaires")),
    build_simple_formula_couple('sal', FloatPresta(cs_travail._sal, label = u"Salaires imposables")),
    build_simple_formula_couple('salnet', FloatPresta(cs_travail._salnet, label = u"Salaires nets d'après définition INSEE")),

    # Fonctionnaires
    build_simple_formula_couple('indemnite_residence', FloatPresta(cs_travail._indemnite_residence, label = u"Indemnité de résidence (fonction publique)")),
    build_simple_formula_couple('supp_familial_traitement', FloatPresta(cs_travail._supp_familial_traitement,
        label = u"Supplément familial de traitement (fonction publique)", start = date(2011, 1, 1))),  # TODO: check this curious starting date
    build_simple_formula_couple('cot_pat_pension_civile', FloatPresta(cs_travail._cot_pat_pension_civile, label = u"Cotisation patronale pension civile")),
    build_simple_formula_couple('cot_sal_pension_civile', FloatPresta(cs_travail._cot_sal_pension_civile, label = u"Cotisation salariale pension civile")),
    build_simple_formula_couple('cot_pat_rafp', FloatPresta(cs_travail._cot_pat_rafp, label = u"Cotisation patronale RAFP")),
    build_simple_formula_couple('cot_sal_rafp', FloatPresta(cs_travail._cot_sal_rafp, label = u"Cotisation salariale RAFP")),

    # Revenus non-salariés
    build_simple_formula_couple('rev_microsocial', FloatPresta(cs_travail._rev_microsocial,
        label = u"Revenu net des cotisations sociales pour le régime microsocial", start = date(2009, 1, 1))),

    # Allocations chômage
    build_simple_formula_couple('chobrut', FloatPresta(inv_rev._chobrut, label = u"Allocations chômage brutes")),
    build_simple_formula_couple('csgchod', FloatPresta(cs_remplac._csgchod, label = u"CSG déductible sur les allocations chômage")),
    build_simple_formula_couple('csgchoi', FloatPresta(cs_remplac._csgchoi, label = u"CSG imposable sur les allocations chômage")),
    build_simple_formula_couple('crdscho', FloatPresta(cs_remplac._crdscho, label = u"CRDS sur les allocations chômage")),
    build_simple_formula_couple('cho', FloatPresta(cs_remplac._cho, label = u"Allocations chômage imposables")),
    build_simple_formula_couple('chonet', FloatPresta(cs_remplac._chonet, label = u"Allocations chômage nettes")),

    # Pensions
    build_simple_formula_couple('rstbrut', FloatPresta(cs_remplac._rstbrut, label = u"Pensions de retraite brutes")),
    build_simple_formula_couple('csgrstd', FloatPresta(cs_remplac._csgrstd, label = u"CSG déductible sur les pensions de retraite")),
    build_simple_formula_couple('csgrsti', FloatPresta(cs_remplac._csgrsti, label = u"CSG imposable sur les pensions de retraite")),
    build_simple_formula_couple('crdsrst', FloatPresta(cs_remplac._crdsrst, label = u"CRDS sur les pensions de retraite")),
    build_simple_formula_couple('rst', FloatPresta(cs_remplac._rst, label = u"Pensions de retraite imposables")),
    build_simple_formula_couple('rstnet', FloatPresta(cs_remplac._rstnet, label = u"Pensions de retraite nettes")),
    build_simple_formula_couple('casa', FloatPresta(cs_remplac._casa, label = u"Contribution additionnelle de solidarité et d'autonomie", start = date(2013, 4, 1))),

    # Revenus du capital soumis au prélèvement libératoire
    build_simple_formula_couple('csg_cap_lib', FloatPresta(cs_capital._csg_cap_lib, label = u"CSG sur les revenus du capital soumis au prélèvement libératoire")),
    build_simple_formula_couple('crds_cap_lib', FloatPresta(cs_capital._crds_cap_lib, label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire")),
    build_simple_formula_couple('prelsoc_cap_lib', FloatPresta(cs_capital._prelsoc_cap_lib, label = u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire")),

    # Revenus du capital soumis au barème
    build_simple_formula_couple('csg_cap_bar', FloatPresta(cs_capital._csg_cap_bar, label = u"CSG sur les revenus du capital soumis au barème")),
    build_simple_formula_couple('crds_cap_bar', FloatPresta(cs_capital._crds_cap_bar, label = u"CRDS sur les revenus du capital soumis au barème")),
    build_simple_formula_couple('prelsoc_cap_bar', FloatPresta(cs_capital._prelsoc_cap_bar, label = u"Prélèvements sociaux sur les revenus du capital soumis au barème")),

    # Revenus fonciers (sur les foyers)
    build_simple_formula_couple('csg_fon', FloatPresta(cs_capital._csg_fon, entity = "foy", label = u"CSG sur les revenus fonciers")),
    build_simple_formula_couple('crds_fon', FloatPresta(cs_capital._crds_fon, entity = "foy", label = u"CRDS sur les revenus fonciers")),
    build_simple_formula_couple('prelsoc_fon', FloatPresta(cs_capital._prelsoc_fon, entity = "foy", label = u"Prélèvements sociaux sur les revenus fonciers")),

    # Plus values de cessions de valeurs mobilières
    build_simple_formula_couple('csg_pv_mo', FloatPresta(cs_capital._csg_pv_mo, entity = "foy", label = u"CSG sur les plus-values de cession de valeurs mobilières")),
    build_simple_formula_couple('crds_pv_mo', FloatPresta(cs_capital._crds_pv_mo, entity = "foy", label = u"CRDS sur les plus-values de cession de valeurs mobilières")),
    build_simple_formula_couple('prelsoc_pv_mo', FloatPresta(cs_capital._prelsoc_pv_mo, entity = "foy", label = u"Prélèvements sociaux sur les plus-values de cession de valeurs mobilières")),

    # Plus-values immobilières
    build_simple_formula_couple('csg_pv_immo', FloatPresta(cs_capital._csg_pv_immo, entity = "foy", label = u"CSG sur les plus-values immobilières")),
    build_simple_formula_couple('crds_pv_immo', FloatPresta(cs_capital._crds_pv_immo, entity = "foy", label = u"CRDS sur les plus-values immobilières")),
    build_simple_formula_couple('prelsoc_pv_immo', FloatPresta(cs_capital._prelsoc_pv_immo, entity = "foy", label = u"Prélèvements sociaux sur les plus-values immobilières")),

    # Réforme Landais-Pikettty-Saez TODO: move out form here
    build_simple_formula_couple('base_csg', FloatPresta(cs_lps._base_csg)),
    build_simple_formula_couple('ir_lps', FloatPresta(cs_lps._ir_lps, start = date(2010, 1, 1))),

    ############################################################
    # Impôt sur le revenu
    ############################################################

    build_simple_formula_couple('marpac', BoolPresta(ir._marpac, entity = 'foy')),
    build_simple_formula_couple('celdiv', BoolPresta(ir._celdiv, entity = 'foy')),
    build_simple_formula_couple('veuf', BoolPresta(ir._veuf, entity = 'foy')),
    build_simple_formula_couple('jveuf', BoolPresta(ir._jveuf, entity = 'foy')),
    build_simple_formula_couple('nbptr', FloatPresta(ir._nbptr, entity = 'foy', label = u"Nombre de parts")),
    build_simple_formula_couple('rbg', FloatPresta(ir._rbg, entity = 'foy', label = u"Revenu brut global")),

    # charges déductibles
    build_simple_formula_couple('cd_penali', FloatPresta(cd._cd_penali, entity = 'foy')),
    build_simple_formula_couple('cd_acc75a', FloatPresta(cd._cd_acc75a, entity = 'foy')),
    build_simple_formula_couple('cd_percap', FloatPresta(cd._cd_percap, entity = 'foy', start = date(2002, 1, 1), end = date(2006, 12, 31))),
    build_simple_formula_couple('cd_deddiv', FloatPresta(cd._cd_deddiv, entity = 'foy')),
    build_simple_formula_couple('cd_doment', FloatPresta(cd._cd_doment, entity = 'foy', start = date(2002, 1, 1), end = date(2005, 12, 31))),
    build_simple_formula_couple('cd_eparet', FloatPresta(cd._cd_eparet, entity = 'foy', start = date(2004, 1, 1))),
    build_simple_formula_couple('cd_sofipe', FloatPresta(cd._cd_sofipe, entity = 'foy', start = date(2002, 1, 1), end = date(2006, 12, 31))),
    build_simple_formula_couple('cd_cinema', FloatPresta(cd._cd_cinema, entity = 'foy', start = date(2002, 1, 1), end = date(2005, 12, 31))),
    build_simple_formula_couple('cd_ecodev', FloatPresta(cd._cd_ecodev, entity = 'foy', start = date(2007, 1, 1), end = date(2008, 12, 31))),
    build_simple_formula_couple('cd_grorep', FloatPresta(cd._cd_grorep, entity = 'foy', start = date(2009, 1, 1))),

    build_simple_formula_couple('charges_deduc_reforme', FloatPresta(cd._charges_deduc_reforme, entity = 'foy')),
    build_simple_formula_couple('charge_loyer', FloatPresta(cd._charge_loyer, entity = 'foy')),

    build_simple_formula_couple('rbg_int', FloatPresta(cd._rbg_int, entity = 'foy', label = u"Revenu brut global intermédiaire")),
    build_simple_formula_couple('cd1', FloatPresta(cd._cd1, entity = 'foy', label = u"Charges déductibles non plafonnées")),
    build_simple_formula_couple('cd2', FloatPresta(cd._cd2, entity = 'foy', label = u"Charges déductibles plafonnées", start = date(2002, 1, 1), end = date(2008, 12, 31))),
    build_simple_formula_couple('charges_deduc', FloatPresta(cd._charges_deduc, entity = 'foy', label = u"Charges déductibles")),

    build_simple_formula_couple('rfr_cd', FloatPresta(cd._rfr_cd, entity = 'foy', label = u"Charges déductibles entrant dans le revenus fiscal de référence")),  # TODO:

    build_simple_formula_couple('rng', FloatPresta(ir._rng, entity = 'foy', label = u"Revenu net global")),
    build_simple_formula_couple('rni', FloatPresta(ir._rni, entity = 'foy', label = u"Revenu net imposable")),

    build_simple_formula_couple('abat_spe', FloatPresta(ir._abat_spe, entity = 'foy', label = u"Abattements spéciaux")),
    build_simple_formula_couple('alloc', FloatPresta(ir._alloc, entity = 'foy', label = u"Allocation familiale pour l'ir")),
    build_simple_formula_couple('deficit_ante', FloatPresta(ir._deficit_ante, entity = 'foy', label = u"Déficit global antérieur")),

    build_simple_formula_couple('rev_sal', FloatPresta(ir._rev_sal)),
    build_simple_formula_couple('salcho_imp', FloatPresta(ir._salcho_imp)),
    build_simple_formula_couple('rev_pen', FloatPresta(ir._rev_pen)),
    build_simple_formula_couple('pen_net', FloatPresta(ir._pen_net)),
    build_simple_formula_couple('indu_plaf_abat_pen', FloatPresta(ir._indu_plaf_abat_pen, entity = 'foy')),
    build_simple_formula_couple('abat_sal_pen', FloatPresta(ir._abat_sal_pen, start = date(2002, 1, 1), end = date(2005, 12, 31))),
    build_simple_formula_couple('sal_pen_net', FloatPresta(ir._sal_pen_net)),
    build_simple_formula_couple('rto', FloatPresta(ir._rto, label = u'Rentes viagères (rentes à titre onéreux)')),
    build_simple_formula_couple('rto_net', FloatPresta(ir._rto_net, label = u'Rentes viagères après abattements')),
    build_simple_formula_couple('tspr', FloatPresta(ir._tspr)),

    build_simple_formula_couple('rev_cat_tspr', FloatPresta(ir._rev_cat_tspr, entity = 'foy', label = u"Revenu catégoriel - Salaires, pensions et rentes")),
    build_simple_formula_couple('rev_cat_rvcm', FloatPresta(ir._rev_cat_rvcm, entity = 'foy', label = u'Revenu catégoriel - Capitaux')),
    build_simple_formula_couple('rev_cat_rpns', FloatPresta(ir._rev_cat_rpns, entity = 'foy', label = u'Revenu catégoriel - Rpns')),
    build_simple_formula_couple('rev_cat_rfon', FloatPresta(ir._rev_cat_rfon, entity = 'foy', label = u'Revenu catégoriel - Foncier')),
    build_simple_formula_couple('rev_cat_pv', FloatPresta(ir._rev_cat_pv, entity = 'foy', label = u'Revenu catégoriel - Plus-values', start = date(2013, 1, 1))),
    build_simple_formula_couple('rev_cat', FloatPresta(ir._rev_cat, entity = 'foy', label = u"Revenus catégoriels")),

    build_simple_formula_couple('deficit_rcm', FloatPresta(ir._deficit_rcm, entity = 'foy', label = u'Deficit capitaux mobiliers')),
    build_simple_formula_couple('csg_deduc_patrimoine_simulated', FloatPresta(ir._csg_deduc_patrimoine_simulated, entity = 'foy',
        label = u'Csg déductible sur le patrimoine simulée')),
    build_simple_formula_couple('csg_deduc_patrimoine', FloatPresta(ir._csg_deduc_patrimoine, entity = 'foy', label = u'Csg déductible sur le patrimoine')),
    build_simple_formula_couple('csg_deduc', FloatPresta(ir._csg_deduc, entity = 'foy', label = u'Csg déductible sur le patrimoine')),

    build_simple_formula_couple('plus_values', FloatPresta(ir._plus_values, entity = 'foy')),
    build_simple_formula_couple('ir_brut', FloatPresta(ir._ir_brut, entity = 'foy')),
    build_simple_formula_couple('nb_pac', FloatPresta(ir._nb_pac, entity = 'foy')),
    build_simple_formula_couple('nb_adult', FloatPresta(ir._nb_adult, entity = 'foy')),
    build_simple_formula_couple('ir_ss_qf', FloatPresta(ir._ir_ss_qf, entity = 'foy')),
    build_simple_formula_couple('ir_plaf_qf', FloatPresta(ir._ir_plaf_qf, entity = 'foy')),
    build_simple_formula_couple('avantage_qf', FloatPresta(ir._avantage_qf, entity = 'foy')),
    build_simple_formula_couple('nat_imp', FloatPresta(ir._nat_imp, entity = 'foy')),
    build_simple_formula_couple('decote', FloatPresta(ir._decote, entity = 'foy')),

    # réductions d'impots
    build_simple_formula_couple('donapd', FloatPresta(ri._donapd, entity = 'foy')),
    build_simple_formula_couple('dfppce', FloatPresta(ri._dfppce, entity = 'foy')),
    build_simple_formula_couple('cotsyn', FloatPresta(ri._cotsyn, entity = 'foy')),
    build_simple_formula_couple('resimm', FloatPresta(ri._resimm, entity = 'foy', start = date(2009, 1, 1))),
    build_simple_formula_couple('patnat', FloatPresta(ri._patnat, entity = 'foy', start = date(2010, 1, 1))),
    build_simple_formula_couple('sofipe', FloatPresta(ri._sofipe, entity = 'foy', start = date(2009, 1, 1))),
    build_simple_formula_couple('saldom', FloatPresta(ri._saldom, entity = 'foy', start = date(2007, 1, 1))),
    build_simple_formula_couple('intagr', FloatPresta(ri._intagr, entity = 'foy', start = date(2005, 1, 1))),
    build_simple_formula_couple('prcomp', FloatPresta(ri._prcomp, entity = 'foy')),
    build_simple_formula_couple('spfcpi', FloatPresta(ri._spfcpi, entity = 'foy')),
    build_simple_formula_couple('mohist', FloatPresta(ri._mohist, entity = 'foy', start = date(2008, 1, 1))),
    build_simple_formula_couple('sofica', FloatPresta(ri._sofica, entity = 'foy', start = date(2006, 1, 1))),
    build_simple_formula_couple('cappme', FloatPresta(ri._cappme, entity = 'foy')),
    build_simple_formula_couple('repsoc', FloatPresta(ri._repsoc, entity = 'foy', start = date(2003, 1, 1))),
    build_simple_formula_couple('invfor', FloatPresta(ri._invfor, entity = 'foy')),
    build_simple_formula_couple('deffor', FloatPresta(ri._deffor, entity = 'foy', start = date(2006, 1, 1))),
    build_simple_formula_couple('daepad', FloatPresta(ri._daepad, entity = 'foy')),
    build_simple_formula_couple('rsceha', FloatPresta(ri._rsceha, entity = 'foy')),
    build_simple_formula_couple('invlst', FloatPresta(ri._invlst, entity = 'foy', start = date(2004, 1, 1))),
    build_simple_formula_couple('domlog', FloatPresta(ri._domlog, entity = 'foy', start = date(2002, 1, 1), end = date(2009, 12, 31))),
    build_simple_formula_couple('adhcga', FloatPresta(ri._adhcga, entity = 'foy')),
    build_simple_formula_couple('creaen', FloatPresta(ri._creaen, entity = 'foy', start = date(2006, 1, 1))),
    build_simple_formula_couple('ecpess', FloatPresta(ri._ecpess, entity = 'foy')),
    build_simple_formula_couple('scelli', FloatPresta(ri._scelli, entity = 'foy', start = date(2009, 1, 1), end = date(2010, 12, 31))),
    build_simple_formula_couple('locmeu', FloatPresta(ri._locmeu, entity = 'foy', start = date(2009, 1, 1), end = date(2010, 12, 31))),
    build_simple_formula_couple('doment', FloatPresta(ri._doment, entity = 'foy')),
    build_simple_formula_couple('domsoc', FloatPresta(ri._domsoc, entity = 'foy')),
    build_simple_formula_couple('intemp', FloatPresta(ri._intemp, entity = 'foy', start = date(2002, 1, 1), end = date(2003, 12, 31))),
    build_simple_formula_couple('garext', FloatPresta(ri._garext, entity = 'foy', start = date(2002, 1, 1), end = date(2005, 12, 31))),
    build_simple_formula_couple('assvie', FloatPresta(ri._assvie, entity = 'foy', start = date(2002, 1, 1), end = date(2004, 12, 31))),
    build_simple_formula_couple('invrev', FloatPresta(ri._invrev, entity = 'foy', start = date(2002, 1, 1), end = date(2003, 12, 31))),
    build_simple_formula_couple('intcon', FloatPresta(ri._intcon, entity = 'foy', start = date(2004, 1, 1), end = date(2005, 12, 31))),
    build_simple_formula_couple('ecodev', FloatPresta(ri._ecodev, entity = 'foy', start = date(2009, 1, 1), end = date(2009, 12, 31))),

    build_simple_formula_couple('nb_pac2', FloatPresta(ci._nb_pac2, entity = 'foy')),

    build_simple_formula_couple('ip_net', FloatPresta(ir._ip_net, entity = 'foy')),
    build_simple_formula_couple('reductions', FloatPresta(ri._reductions, entity = 'foy')),
    build_simple_formula_couple('iaidrdi', FloatPresta(ir._iaidrdi, entity = 'foy')),
    build_simple_formula_couple('teicaa', FloatPresta(ir._teicaa, entity = 'foy')),
    build_simple_formula_couple('cont_rev_loc', FloatPresta(ir._cont_rev_loc, entity = 'foy', start = date(2001, 1, 1))),
    build_simple_formula_couple('iai', FloatPresta(ir._iai, entity = 'foy')),
    build_simple_formula_couple('cehr', FloatPresta(ir._cehr, entity = 'foy', label = u"Contribution exceptionnelle sur les hauts revenus")),
 #   build_simple_formula_couple('cesthra', FloatPresta(ir._cesthra, entity = 'foy', start = date(2013, 1, 1))), PLF 2013, amendement rejeté
    build_simple_formula_couple('imp_lib', FloatPresta(ir._imp_lib, entity = 'foy', end = date(2012, 12, 31)),),  # TODO: Check - de 2000euros
    build_simple_formula_couple('assiette_vente', FloatPresta(ir._micro_social_vente, entity = 'foy', start = date(2009, 1, 1))),
    build_simple_formula_couple('assiette_service', FloatPresta(ir._micro_social_service, entity = 'foy', start = date(2009, 1, 1))),
    build_simple_formula_couple('assiette_proflib', FloatPresta(ir._micro_social_proflib, entity = 'foy', start = date(2009, 1, 1))),
    build_simple_formula_couple('microsocial', FloatPresta(ir._micro_social, entity = 'foy')),

    # Prime pour l'emploi
    build_simple_formula_couple('ppe_coef', FloatPresta(ir._ppe_coef, entity = 'foy')),
    build_simple_formula_couple('ppe_base', FloatPresta(ir._ppe_base)),
    build_simple_formula_couple('ppe_coef_tp', FloatPresta(ir._ppe_coef_tp)),
    build_simple_formula_couple('ppe_elig', BoolPresta(ir._ppe_elig, entity = 'foy')),
    build_simple_formula_couple('ppe_elig_i', BoolPresta(ir._ppe_elig_i)),
    build_simple_formula_couple('ppe_rev', FloatPresta(ir._ppe_rev)),
    build_simple_formula_couple('ppe_brute', FloatPresta(ir._ppe_brute, entity = 'foy', label = u"Prime pour l'emploi brute")),
    build_simple_formula_couple('ppe', FloatPresta(ir._ppe, entity = 'foy', label = u"Prime pour l'emploi")),

    # Autres crédits d'impôts
    build_simple_formula_couple('creimp', FloatPresta(ci._creimp, entity = 'foy')),
    build_simple_formula_couple('accult', FloatPresta(ci._accult, entity = 'foy')),
    build_simple_formula_couple('percvm', FloatPresta(ci._percvm, entity = 'foy', start = date(2010, 1, 1))),
    build_simple_formula_couple('direpa', FloatPresta(ci._direpa, entity = 'foy')),
    build_simple_formula_couple('mecena', FloatPresta(ci._mecena, entity = 'foy', start = date(2003, 1, 1))),
    build_simple_formula_couple('prlire', FloatPresta(ci._prlire, entity = 'foy', label = u"Prélèvement libératoire à restituer (case 2DH)", end = date(2012, 12, 31))),
    build_simple_formula_couple('aidper', FloatPresta(ci._aidper, entity = 'foy')),
    build_simple_formula_couple('quaenv', FloatPresta(ci._quaenv, entity = 'foy', start = date(2005, 1, 1))),
    build_simple_formula_couple('drbail', FloatPresta(ci._drbail, entity = 'foy')),
    build_simple_formula_couple('ci_garext', FloatPresta(ci._ci_garext, entity = 'foy', start = date(2005, 1, 1))),
    build_simple_formula_couple('preetu', FloatPresta(ci._preetu, entity = 'foy', start = date(2005, 1, 1))),
    build_simple_formula_couple('saldom2', FloatPresta(ci._saldom2, entity = 'foy', start = date(2007, 1, 1))),
    build_simple_formula_couple('inthab', FloatPresta(ci._inthab, entity = 'foy', start = date(2007, 1, 1))),
    build_simple_formula_couple('assloy', FloatPresta(ci._assloy, entity = 'foy', start = date(2005, 1, 1))),
    build_simple_formula_couple('autent', FloatPresta(ci._autent, entity = 'foy', start = date(2009, 1, 1))),
    build_simple_formula_couple('acqgpl', FloatPresta(ci._acqgpl, entity = 'foy', start = date(2002, 1, 1), end = date(2007, 12, 31))),
    build_simple_formula_couple('divide', FloatPresta(ci._divide, entity = 'foy', start = date(2005, 1, 1), end = date(2009, 12, 31))),
    build_simple_formula_couple('aidmob', FloatPresta(ci._aidmob, entity = 'foy', start = date(2005, 1, 1), end = date(2008, 12, 31))),

    build_simple_formula_couple('jeunes', FloatPresta(ci._jeunes, entity = 'foy', start = date(2005, 1, 1), end = date(2008, 12, 31))),

    build_simple_formula_couple('credits_impot', FloatPresta(ci._credits_impot, entity = 'foy')),

    build_simple_formula_couple('irpp', FloatPresta(ir._irpp, entity = 'foy', label = u"Impôt sur le revenu des personnes physiques")),

    build_simple_formula_couple('rfr', FloatPresta(ir._rfr, entity = 'foy')),
    build_simple_formula_couple('rfr_rvcm', FloatPresta(ir._rfr_rvcm, entity = 'foy')),

#    build_simple_formula_couple('alv', FloatPresta(ir._alv)),
    build_simple_formula_couple('glo', FloatPresta(ir._glo)),
    build_simple_formula_couple('rag', FloatPresta(ir._rag)),
    build_simple_formula_couple('ric', FloatPresta(ir._ric)),
    build_simple_formula_couple('rac', FloatPresta(ir._rac)),
    build_simple_formula_couple('rnc', FloatPresta(ir._rnc)),
    build_simple_formula_couple('rpns', FloatPresta(ir._rpns)),
    build_simple_formula_couple('fon', FloatPresta(ir._fon, entity = 'foy')),

    build_simple_formula_couple('rpns_mvct', FloatPresta(ir._rpns_mvct)),
    build_simple_formula_couple('rpns_pvct', FloatPresta(ir._rpns_pvct)),
    build_simple_formula_couple('rpns_mvlt', FloatPresta(ir._rpns_mvlt)),
    build_simple_formula_couple('rpns_pvce', FloatPresta(ir._rpns_pvce)),
    build_simple_formula_couple('rpns_exon', FloatPresta(ir._rpns_exon)),
    build_simple_formula_couple('rpns_i', FloatPresta(ir._rpns_i)),

    build_simple_formula_couple('rev_cap_bar', FloatPresta(ir._rev_cap_bar, entity = 'foy')),
    build_simple_formula_couple('rev_cap_lib', FloatPresta(ir._rev_cap_lib, entity = 'foy')),
    build_simple_formula_couple('avf', FloatPresta(ir._avf, entity = 'foy')),

    ###########################################################
    # Impôt sur le revenu afférent à la plus-value immobilière
    ###########################################################

    build_simple_formula_couple('ir_pv_immo', FloatPresta(immo._ir_pv_immo,
                              entity = 'foy',
                              label = u"Impôt sur le revenu afférent à la plus-value immobilière")),

    ############################################################
    # Impôt de solidarité sur la fortune
    ############################################################
    build_simple_formula_couple('isf_imm_bati', FloatPresta(isf._isf_imm_bati, entity = 'foy')),
    build_simple_formula_couple('isf_imm_non_bati', FloatPresta(isf._isf_imm_non_bati, entity = 'foy')),
    build_simple_formula_couple('isf_actions_sal', FloatPresta(isf._isf_actions_sal, entity = 'foy', start = date(2006, 1, 1))),
    build_simple_formula_couple('isf_droits_sociaux', FloatPresta(isf._isf_droits_sociaux, entity = 'foy')),
    build_simple_formula_couple('ass_isf', FloatPresta(isf._ass_isf, entity = 'foy')),

    build_simple_formula_couple('isf_iai', FloatPresta(isf._isf_iai, entity = 'foy')),
    build_simple_formula_couple('tot_impot', FloatPresta(isf._tot_impot, entity = 'foy')),
    build_simple_formula_couple('isf_avant_plaf', FloatPresta(isf._isf_avant_plaf, entity = 'foy')),
    build_simple_formula_couple('isf_avant_reduction', FloatPresta(isf._isf_avant_reduction, entity = 'foy')),
    build_simple_formula_couple('isf_reduc_pac', FloatPresta(isf._isf_reduc_pac, entity = 'foy')),
    build_simple_formula_couple('isf_inv_pme', FloatPresta(isf._isf_inv_pme, entity = 'foy', start = date(2008, 1, 1))),
    build_simple_formula_couple('isf_org_int_gen', FloatPresta(isf._isf_org_int_gen, entity = 'foy')),
    build_simple_formula_couple('revetproduits', FloatPresta(isf._revetproduits, entity = 'foy')),
    build_simple_formula_couple('isf_apres_plaf', FloatPresta(isf._isf_apres_plaf, entity = 'foy')),
    build_simple_formula_couple('decote_isf', FloatPresta(isf._decote_isf, entity = 'foy', start = date(2013, 1, 1))),
    build_simple_formula_couple('isf_tot', FloatPresta(isf._isf_tot, entity = 'foy')),

    ############################################################
    #                            Bouclier Fiscal
    ############################################################
    build_simple_formula_couple('rvcm_plus_abat', FloatPresta(isf._rvcm_plus_abat, entity = 'foy')),
    build_simple_formula_couple('maj_cga_i', FloatPresta(isf._maj_cga_i)),
    build_simple_formula_couple('maj_cga', FloatPresta(isf._maj_cga, entity = 'foy')),

    build_simple_formula_couple('bouclier_rev', FloatPresta(isf._bouclier_rev,
                                entity = 'foy',
                                start = date(2006, 1, 1),
                                end = date(2010, 12, 31))),
    build_simple_formula_couple('bouclier_imp_gen', FloatPresta(isf._bouclier_imp_gen,
                                    entity = 'foy',
                                    start = date(2006, 1, 1),
                                    end = date(2010, 12, 31))),
    build_simple_formula_couple('restitutions', FloatPresta(isf._restitutions,
                                entity = 'foy',
                                start = date(2006, 1, 1),
                                end = date(2010, 12, 31))),
    build_simple_formula_couple('bouclier_sumimp', FloatPresta(isf._bouclier_sumimp,
                                   entity = 'foy',
                                   start = date(2006, 1, 1),
                                   end = date(2010, 12, 31))),
    build_simple_formula_couple('bouclier_fiscal', FloatPresta(isf._bouclier_fiscal,
                                   entity = 'foy',
                                   start = date(2006, 1, 1),
                                   end = date(2010, 12, 31))),

    # TODO: inclure aussi les dates si nécessaire start = date(2007,1,1)

    ############################################################
    # Prestations familiales
    ############################################################

    build_simple_formula_couple('etu', BoolPresta(pf._etu, label = u"Indicatrice individuelle étudiant")),
    build_simple_formula_couple('biact', BoolPresta(pf._biact, entity = 'fam', label = u"Indicatrice de biactivité")),
    build_simple_formula_couple('concub', BoolPresta(pf._concub, entity = 'fam', label = u"Indicatrice de vie en couple")),
    build_simple_formula_couple('maries', BoolPresta(pf._maries, entity = 'fam')),
    build_simple_formula_couple('nb_par', FloatPresta(pf._nb_par, entity = 'fam', label = u"Nombre de parents")),
    build_simple_formula_couple('smic55', BoolPresta(pf._smic55, label = u"Indicatrice individuelle d'un salaire supérieur à 55% du smic")),
    build_simple_formula_couple('isol', BoolPresta(pf._isol, entity = 'fam')),

    build_simple_formula_couple('div', FloatPresta(pf._div)),
    build_simple_formula_couple('rev_coll', FloatPresta(pf._rev_coll)),
    build_simple_formula_couple('br_pf_i', FloatPresta(pf._br_pf_i, label = 'Base ressource individuele des prestations familiales')),
    build_simple_formula_couple('br_pf', FloatPresta(pf._br_pf, entity = 'fam', label = 'Base ressource des prestations familiales')),

    build_simple_formula_couple('af_nbenf', FloatPresta(pf._af_nbenf, entity = 'fam', label = u"Nombre d'enfant au sens des AF")),
    build_simple_formula_couple('af_base', FloatPresta(pf._af_base, entity = 'fam', label = 'Allocations familiales - Base')),
    build_simple_formula_couple('af_majo', FloatPresta(pf._af_majo, entity = 'fam', label = 'Allocations familiales - Majoration pour age')),
    build_simple_formula_couple('af_forf', FloatPresta(pf._af_forf, entity = 'fam', label = 'Allocations familiales - Forfait 20 ans', start = date(2003, 7, 1))),
    build_simple_formula_couple('af', FloatPresta(pf._af, entity = 'fam', label = u"Allocations familiales")),

    build_simple_formula_couple('cf_temp', FloatPresta(pf._cf, entity = 'fam', label = u"Complément familial avant d'éventuels cumuls")),
    build_simple_formula_couple('asf_elig', BoolPresta(pf._asf_elig, entity = 'fam')),
    build_simple_formula_couple('asf', FloatPresta(pf._asf, entity = 'fam', label = u"Allocation de soutien familial")),

    build_simple_formula_couple('ars', FloatPresta(pf._ars, entity = 'fam', label = u"Allocation de rentrée scolaire")),


    build_simple_formula_couple('paje_base_temp', FloatPresta(pf._paje_base, entity = 'fam', label = u"Allocation de base de la PAJE sans tenir compte d'éventuels cumuls", start = date(2004, 1, 1))),
    build_simple_formula_couple('paje_base', FloatPresta(pf._paje_cumul, entity = 'fam', label = u"Allocation de base de la PAJE", start = date(2004, 1, 1))),

    build_simple_formula_couple('paje_nais', FloatPresta(pf._paje_nais, entity = 'fam', label = u"Allocation de naissance de la PAJE", start = date(2004, 1, 1))),
    build_simple_formula_couple('paje_clca', FloatPresta(pf._paje_clca, entity = 'fam', label = u"PAJE - Complément de libre choix d'activité", start = date(2004, 1, 1))),
    build_simple_formula_couple('paje_clca_taux_plein', BoolPresta(pf._paje_clca_taux_plein, entity = 'fam', label = u"Indicatrice Clca taux plein", start = date(2004, 1, 1))),
    build_simple_formula_couple('paje_clca_taux_partiel', BoolPresta(pf._paje_clca_taux_partiel, entity = 'fam', label = u"Indicatrice Clca taux partiel", start = date(2004, 1, 1))),
    build_simple_formula_couple('paje_colca', FloatPresta(pf._paje_colca, entity = 'fam', label = u"PAJE - Complément optionnel de libre choix d'activité", start = date(2004, 1, 1))),
    build_simple_formula_couple('paje_clmg', FloatPresta(pf._paje_clmg, entity = 'fam', label = u"PAJE - Complément de libre choix du mode de garde", start = date(2004, 1, 1))),
    build_simple_formula_couple('paje', FloatPresta(pf._paje, entity = 'fam', label = u"PAJE - Ensemble des prestations", start = date(2004, 1, 1))),


    build_simple_formula_couple('cf', FloatPresta(pf._cf_cumul, entity = 'fam', label = u"Complément familial")),
    build_simple_formula_couple('aeeh', FloatPresta(pf._aeeh, entity = 'fam', label = u"Allocation d'éducation de l'enfant handicapé")),

    build_simple_formula_couple('ape_temp', FloatPresta(pf._ape, entity = 'fam', label = u"Allocation parentale d'éducation", end = date(2004, 1, 1))),
    build_simple_formula_couple('apje_temp', FloatPresta(pf._apje, entity = 'fam', label = u"Allocation pour le jeune enfant", end = date(2004, 1, 1))),
    build_simple_formula_couple('ape', FloatPresta(pf._ape_cumul, entity = 'fam', label = u"Allocation parentale d'éducation", end = date(2004, 1, 1))),
    build_simple_formula_couple('apje', FloatPresta(pf._apje_cumul, entity = 'fam', label = u"Allocation pour le jeune enfant", end = date(2004, 1, 1))),

    build_simple_formula_couple('crds_pfam', FloatPresta(pf._crds_pfam, entity = 'fam', label = u"CRDS (prestations familiales)")),

    # En fait en vigueur pour les enfants nés avant 2004 ...
    # TODO Gestion du cumul apje ape
    ############################################################
    # Allocations logement
    ############################################################

    build_simple_formula_couple('br_al', FloatPresta(lg._br_al, entity = 'fam', label = u"Base ressource des allocations logement")),
    build_simple_formula_couple('al_pac', FloatPresta(lg._al_pac, entity = 'fam', label = u"Nombre de personnes à charge au sens des allocations logement")),
    build_simple_formula_couple('al', FloatPresta(lg._al, entity = 'fam', label = u"Allocation logement (indifferrenciée)")),
    build_simple_formula_couple('alf', FloatPresta(lg._alf, entity = 'fam', label = u"Allocation logement familiale")),
    build_simple_formula_couple('als', FloatPresta(lg._als, entity = 'fam', label = u"Allocation logement sociale")),
    build_simple_formula_couple('als_nonet', FloatPresta(lg._als_nonet, entity = 'fam', label = u"Allocation logement sociale (non étudiant)")),
    build_simple_formula_couple('alset', FloatPresta(lg._alset, entity = 'fam', label = u"Allocation logement sociale étudiante")),
    build_simple_formula_couple('apl', FloatPresta(lg._apl, entity = 'fam', label = u"Aide personalisée au logement")),
    build_simple_formula_couple('crds_lgtm', FloatPresta(lg._crds_lgtm, entity = 'fam', label = u"CRDS (allocation logement)")),

    ############################################################
    # RSA/RMI
    ############################################################

    build_simple_formula_couple('div_ms', FloatPresta(ms._div_ms)),
    build_simple_formula_couple('rfon_ms', FloatPresta(ms._rfon_ms)),

    build_simple_formula_couple('ra_rsa', FloatPresta(ms._ra_rsa, label = u"Revenus d'activité du Rsa")),
    build_simple_formula_couple('br_rmi_i', FloatPresta(ms._br_rmi_i)),
    build_simple_formula_couple('br_rmi_ms', FloatPresta(ms._br_rmi_ms)),
    build_simple_formula_couple('br_rmi_pf', FloatPresta(ms._br_rmi_pf)),
    build_simple_formula_couple('br_rmi', FloatPresta(ms._br_rmi, entity = 'fam', label = u"Base ressources du Rmi/Rsa")),

    build_simple_formula_couple('rmi_nbp', FloatPresta(ms._rmi_nbp, entity = 'fam', label = u"Nombre de personne à charge au sens du Rmi/Rsa")),
    build_simple_formula_couple('forf_log', FloatPresta(ms._forf_log, entity = 'fam')),
    build_simple_formula_couple('rsa_socle', FloatPresta(ms._rsa_socle, entity = 'fam', label = u"RSA socle")),
    build_simple_formula_couple('rmi', FloatPresta(ms._rmi, entity = 'fam', label = u"Revenu de solidarité active - socle")),
    build_simple_formula_couple('rsa', FloatPresta(ms._rsa, entity = 'fam', label = u"Revenu de solidarité active")),
    build_simple_formula_couple('majo_rsa', FloatPresta(ms._majo_rsa, entity = 'fam',
        label = u"Majoration pour parent isolé du Revenu de solidarité active socle", start = date(2009, 7, 1))),
    build_simple_formula_couple('rsa_act', FloatPresta(ms._rsa_act, entity = 'fam', label = u"Revenu de solidarité active - activité", start = date(2009, 7, 1))),
    build_simple_formula_couple('rsa_act_i', FloatPresta(ms._rsa_act_i)),
    build_simple_formula_couple('psa', FloatPresta(ms._psa, entity = 'fam', label = u"Prime de solidarité active", start = date(2009, 1, 1), end = date(2009, 12, 31))),
    build_simple_formula_couple('api', FloatPresta(ms._api, entity = 'fam', end = date(2009, 7, 1), label = u"Allocation de parent isolé")),
    build_simple_formula_couple('crds_mini', FloatPresta(ms._crds_mini, entity = 'fam', start = date(2009, 7, 1))),
    build_simple_formula_couple('aefa', FloatPresta(ms._aefa, entity = 'fam', label = u"Allocation exceptionnelle de fin d'année")),

    ############################################################
    # ASPA/ASI, Minimum vieillesse
    ############################################################

    build_simple_formula_couple('br_mv_i', FloatPresta(ms._br_mv_i, label = u"Base ressources du minimum vieillesse/ASPA")),
    build_simple_formula_couple('br_mv', FloatPresta(ms._br_mv, entity = 'fam', label = u"Base ressources du minimum vieillesse/ASPA")),

    build_simple_formula_couple('asi_aspa_nb_alloc', FloatPresta(ms._asi_aspa_nb_alloc, entity = 'fam')),
    build_simple_formula_couple('asi_aspa_elig', BoolPresta(ms._asi_aspa_elig, entity = 'fam')),
    build_simple_formula_couple('asi_elig', BoolPresta(ms._asi_elig, label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité")),
    build_simple_formula_couple('asi_coexist_aspa', FloatPresta(ms._asi_coexist_aspa, entity = 'fam', label = u"Allocation supplémentaire d'invalidité quand un adulte de la famille perçoit l'ASPA")),
    build_simple_formula_couple('asi_pure', FloatPresta(ms._asi_pure, entity = 'fam', label = u"Allocation supplémentaire d'invalidité quand aucun adulte de la famille ne perçoit l'ASPA")),
    build_simple_formula_couple('asi', FloatPresta(ms._asi, entity = 'fam', label = u"Allocation supplémentaire d'invalidité", start = date(2007, 1, 1))),
        # En 2007, Transformation du MV et de L'ASI en ASPA et ASI. La prestation ASPA calcule bien l'ancien MV
        # mais TODO manque l'ancienne ASI

    build_simple_formula_couple('aspa_elig', BoolPresta(ms._aspa_elig, label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées")),
    build_simple_formula_couple('aspa_coexist_asi', FloatPresta(ms._aspa_coexist_asi, entity = 'fam', label = u"Allocation de solidarité aux personnes agées quand un adulte de la famille perçoit l'ASI")),
    build_simple_formula_couple('aspa_pure', FloatPresta(ms._aspa_pure, entity = 'fam', label = u"Allocation de solidarité aux personnes agées quand aucun adulte de la famille ne perçoit l'ASI")),
    build_simple_formula_couple('aspa', FloatPresta(ms._aspa, entity = 'fam', label = u"Allocation de solidarité aux personnes agées")),

    ############################################################
    # Allocation adulte handicapé
    ############################################################

    build_simple_formula_couple('br_aah', FloatPresta(ms._br_aah, entity = 'fam', label = u"Base ressources de l'allocation adulte handicapé")),
    build_simple_formula_couple('aah', FloatPresta(ms._aah, entity = 'fam', label = u"Allocation adulte handicapé")),
    build_simple_formula_couple('caah', FloatPresta(ms._caah, entity = 'fam', label = u"Complément de l'allocation adulte handicapé")),

    ############################################################
    # Taxe d'habitation
    ############################################################

    build_simple_formula_couple('tax_hab', FloatPresta(th._tax_hab, entity = 'men', label = u"Taxe d'habitation")),

    ############################################################
    # Unité de consommation du ménage
    ############################################################
    build_simple_formula_couple('uc', FloatPresta(cm._uc, entity = 'men', label = u"Unités de consommation")),

    ############################################################
    # Catégories
    ############################################################

    build_simple_formula_couple('typ_men', IntPresta(cm._typ_men, entity = 'men', label = u"Type de ménage")),
    build_simple_formula_couple('nb_ageq0', IntPresta(cl._nb_ageq0,
                           entity = 'men',
                           label = u"Effectifs des tranches d'âge quiquennal",
                           survey_only = True,
                           )),

    build_simple_formula_couple('nbinde', EnumPresta(cl._nbinde,
                          label = u"Nombre d'individus dans le ménage", entity = 'men',
                          enum = Enum([u"Une personne",
                                       u"Deux personnes",
                                       u"Trois personnes",
                                       u"Quatre personnes",
                                       u"Cinq personnes",
                                       u"Six personnes et plus"], start = 1))),

     build_simple_formula_couple('cplx', BoolPresta(cl._cplx, entity = 'men', label = u"Indicatrice de ménage complexe")),

     build_simple_formula_couple('act_cpl', IntPresta(cl._act_cpl,
                           entity = 'men',
                           label = u"Nombre d'actifs parmi la personne de référence du méange et son conjoint")),

     build_simple_formula_couple('cohab', BoolPresta(cl._cohab,
                          entity = 'men',
                          label = u"Vie en couple")),

     build_simple_formula_couple('act_enf', IntPresta(cl._act_enf, entity = 'men',
                           label = u"Nombre d'enfants actifs")),

     build_simple_formula_couple('typmen15', EnumPresta(cl._typmen15, label = u"Type de ménage", entity = 'men',
                           enum = Enum([u"Personne seule active",
                                        u"Personne seule inactive",
                                        u"Familles monoparentales, parent actif",
                                        u"Familles monoparentales, parent inactif et au moins un enfant actif",
                                        u"Familles monoparentales, tous inactifs",
                                        u"Couples sans enfant, 1 actif",
                                        u"Couples sans enfant, 2 actifs",
                                        u"Couples sans enfant, tous inactifs",
                                        u"Couples avec enfant, 1 membre du couple actif",
                                        u"Couples avec enfant, 2 membres du couple actif",
                                        u"Couples avec enfant, couple inactif et au moins un enfant actif",
                                        u"Couples avec enfant, tous inactifs",
                                        u"Autres ménages, 1 actif",
                                        u"Autres ménages, 2 actifs ou plus",
                                        u"Autres ménages, tous inactifs"], start = 1))),

     build_simple_formula_couple('decile', EnumPresta(cm._decile,
                           entity = 'men',
                           label = u"Décile de niveau de vie disponible",
                           enum = Enum([u"Hors champ"
                                          u"1er décile",
                                          u"2nd décile",
                                          u"3e décile",
                                          u"4e décile",
                                          u"5e décile",
                                          u"6e décile",
                                          u"7e décile",
                                          u"8e décile",
                                          u"9e décile",
                                          u"10e décile"]),
                           survey_only = True,
                           )),

     build_simple_formula_couple('decile_net', EnumPresta(cm._decile_net,
                               entity = 'men',
                               label = u"Décile de niveau de vie net",
                               enum = Enum([u"Hors champ"
                                            u"1er décile",
                                            u"2nd décile",
                                            u"3e décile",
                                            u"4e décile",
                                            u"5e décile",
                                            u"6e décile",
                                            u"7e décile",
                                            u"8e décile",
                                            u"9e décile",
                                            u"10e décile"]),
                               survey_only = True,
                               )),

     build_simple_formula_couple('pauvre40', EnumPresta(cm._pauvre40,
                             entity = 'men',
                             label = u"Pauvreté monétaire au seuil de 40%",
                             enum = Enum([u"Ménage au dessus du seuil de pauvreté à 40%",
                                          u"Ménage en dessous du seuil de pauvreté à 40%"]),
                             survey_only = True,
                             )),

     build_simple_formula_couple('pauvre50', EnumPresta(cm._pauvre50,
                             entity = 'men',
                             label = u"Pauvreté monétaire au seuil de 50%",
                             enum = Enum([u"Ménage au dessus du seuil de pauvreté à 50%",
                                          u"Ménage en dessous du seuil de pauvreté à 50%"]),
                             survey_only = True,
                             )),

     build_simple_formula_couple('pauvre60', EnumPresta(cm._pauvre60,
                             entity = 'men',
                             label = u"Pauvreté monétaire au seuil de 60%",
                             enum = Enum([u"Ménage au dessus du seuil de pauvreté à 50%",
                                          u"Ménage en dessous du seuil de pauvreté à 50%"]),
                             survey_only = True,
                             )),

    ############################################################
    # Totaux
    ############################################################

    build_simple_formula_couple('revdisp_i', FloatPresta(cm._revdisp_i, label = u"Revenu disponible individuel")),
    build_simple_formula_couple('revdisp', FloatPresta(cm._revdisp, entity = 'men', label = u"Revenu disponible du ménage")),
    build_simple_formula_couple('nivvie', FloatPresta(cm._nivvie, entity = 'men', label = u"Niveau de vie du ménage")),

    build_simple_formula_couple('revnet_i', FloatPresta(cm._revnet_i, label = u"Revenu net individuel")),
    build_simple_formula_couple('revnet', FloatPresta(cm._revnet, entity = 'men', label = u"Revenu net du ménage")),
    build_simple_formula_couple('nivvie_net', FloatPresta(cm._nivvie_net, entity = 'men', label = u"Niveau de vie net du ménage")),

    build_simple_formula_couple('revini_i', FloatPresta(cm._revini_i, label = u"Revenu initial individuel")),
    build_simple_formula_couple('revini', FloatPresta(cm._revini, entity = 'men', label = u"Revenu initial du ménage")),
    build_simple_formula_couple('nivvie_ini', FloatPresta(cm._nivvie_ini, entity = 'men', label = u"Niveau de vie initial du ménage")),

    build_simple_formula_couple('rev_trav', FloatPresta(cm._rev_trav, label = u"Revenus du travail (salariés et non salariés)")),
    build_simple_formula_couple('pen', FloatPresta(cm._pen, label = u"Total des pensions et revenus de remplacement")),
    build_simple_formula_couple('cotsoc_bar', FloatPresta(cm._cotsoc_bar, label = u"Cotisations sociales sur les revenus du capital imposés au barème")),
    build_simple_formula_couple('cotsoc_lib', FloatPresta(cm._cotsoc_lib, label = u"Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire")),
    build_simple_formula_couple('rev_cap', FloatPresta(cm._rev_cap, label = u"Revenus du patrimoine")),
    build_simple_formula_couple('psoc', FloatPresta(cm._psoc, label = u"Total des prestations sociales")),
    build_simple_formula_couple('prelsoc_cap', FloatPresta(cm._prelsoc_cap, label = u"Prélèvements sociaux sur les revenus du capital")),
    build_simple_formula_couple('pfam', FloatPresta(cm._pfam, label = u"Total des prestations familiales")),
    build_simple_formula_couple('mini', FloatPresta(cm._mini, entity = 'fam', label = u"Minima sociaux")),
    build_simple_formula_couple('logt', FloatPresta(cm._logt, label = u"Allocations logements")),
    build_simple_formula_couple('impo', FloatPresta(cm._impo, label = u"Impôts sur le revenu")),
    build_simple_formula_couple('crds', FloatPresta(cm._crds, label = u"Total des contributions au remboursement de la dette sociale")),
    build_simple_formula_couple('csg', FloatPresta(cm._csg, label = u"Total des contributions sociale généralisée")),
    build_simple_formula_couple('cotsoc_noncontrib', FloatPresta(cm._cotsoc_noncontrib, label = u"Cotisations sociales non contributives")),
    build_simple_formula_couple('check_csk', FloatPresta(cm._check_csk)),
    build_simple_formula_couple('check_csg', FloatPresta(cm._check_csg)),
    build_simple_formula_couple('check_crds', FloatPresta(cm._check_crds)),

    ))
