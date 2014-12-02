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


# TODO: actualiser la date des end (c'est souvent 2014 ou 2015)


from datetime import date
from functools import partial

from openfisca_core.columns import AgeCol, BoolCol, EnumCol, FloatCol, PeriodSizeIndependentIntCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import (
    build_alternative_formula,
    build_dated_formula,
    build_select_formula,
    build_simple_formula,
    )

from .. import entities
# Import new syntax-based output variables.
from . import (  # noqa
    inversion_revenus,
    travailleurs_non_salaries,
    )

from .cotisations_sociales import remplacement

# Import model modules.
from . import calage as cl
from . import cmu as cmu
from . import common as cm
from .cotisations_sociales import capital as cs_capital

from .cotisations_sociales import remplacement as cs_remplac

from . import irpp as ir
from . import irpp_charges_deductibles as cd
from . import irpp_credits_impots as ci
from . import irpp_plus_values_immo as immo
from . import irpp_reductions_impots as ri
from . import isf as isf
#from . import lgtm as lg
# from .minima_sociaux import aah
from .minima_sociaux import asi_aspa
from .minima_sociaux import ass
from .minima_sociaux import rsa
from .prestations_familiales import aeeh
from .prestations_familiales import af
from .prestations_familiales import ars
from .prestations_familiales import asf
from .prestations_familiales import paje
from .prestations_familiales import cf
from . import pfam as pf
from . import th as th

from .input_variables import travail_base  # noqa
from .cotisations_sociales import travail_prive
from .cotisations_sociales import travail_verification

from .cotisations_sociales import travail_fonction_publique
from .cotisations_sociales import travail_totaux
from . import lgtm


build_alternative_formula = partial(
    build_alternative_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_dated_formula = partial(
    build_dated_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_select_formula = partial(
    build_select_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_simple_formula = partial(
    build_simple_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )


############################################################
# Cotisations sociales
############################################################

# Salaires
#build_simple_formula(
#    'type_sal',
#    EnumCol(
#        function = cs_travail._type_sal,
#        label = u"Catégorie de salarié",
#        enum = Enum([
#            u"prive_non_cadre",
#            u"prive_cadre",
#            u"public_titulaire_etat",
#            u"public_titulaire_militaire",
#            u"public_titulaire_territoriale",
#            u"public_titulaire_hospitaliere",
#            u"public_non_titulaire",

#<<<<<<< HEAD
#            ]),
#        url = u"http://fr.wikipedia.org/wiki/Professions_et_cat%C3%A9gories_socioprofessionnelles_en_France",
#        )
#    )

#build_simple_formula(
#    'primes',
#    FloatCol(
#        function = cs_travail._primes,
#        label = u"Primes et indemnités des fonctionnaires",
#        url = u"http://vosdroits.service-public.fr/particuliers/F465.xhtml",
#    ))
#build_simple_formula(
#    'sal_h_b',
#    FloatCol(
#        function = cs_travail._sal_h_b,
#        label = u"Salaire horaire brut",
#        url = u"http://www.les-horaires.fr/pratique/smic-horaire.php",
#    ))
#
##    build_simple_formula('taille_entreprise', EnumCol(function = cs_travail._taille_entreprise,
##        enum = Enum([
##            u"Non pertinent",
##            u"Moins de 10 salariés",
##            u"De 10 à 19 salariés",
##            u"De 20 à 249 salariés",
##            u"Plus de 250 salariés",
##            ]),
##        label = u"Catégorie de taille d'entreprise (pour calcul des cotisations sociales)",
##        url = u"http://www.insee.fr/fr/themes/document.asp?ref_id=ip1321",
##        ))
#
#build_simple_formula('cotpat_contrib', FloatCol(function = cs_travail._cotpat_contrib,
#    label = u"Cotisations sociales patronales contributives",
#    url = u"http://fr.wikipedia.org/wiki/Cotisations_sociales",
#    ))
#build_simple_formula('taux_accident_travail', FloatCol(function = cs_travail._taux_accident_travail,
#    label = u"Cotisations sociales patronales : accident du travail et maladies professionnelles",
#    url = u"http://www.lesclesdelabanque.com/Web/Cdb/Entrepreneurs/Content.nsf/DocumentsByIDWeb/7APJB8?OpenDocument",
#    ))
#build_simple_formula('cotpat_accident', FloatCol(function = cs_travail._cotpat_accident,
#    label = u"Cotisations sociales patronales : accident du travail et maladies professionnelles",
#    url = u"http://www.lesclesdelabanque.com/Web/Cdb/Entrepreneurs/Content.nsf/DocumentsByIDWeb/7APJB8?OpenDocument",
#    ))
#build_simple_formula('cotpat_noncontrib', FloatCol(function = cs_travail._cotpat_noncontrib,
#    label = u"Cotisations sociales patronales non contributives",
#    url = u"http://www.lesclesdelabanque.com/Web/Cdb/Entrepreneurs/Content.nsf/DocumentsByIDWeb/7APJB8?OpenDocument",
#    ))
#build_simple_formula('cotpat_main_d_oeuvre', FloatCol(function = cs_travail._cotpat_main_d_oeuvre,
#    label = u"Cotisations sociales patronales main d'oeuvre",
#    url = u"http://www.lesclesdelabanque.com/Web/Cdb/Entrepreneurs/Content.nsf/DocumentsByIDWeb/7APJB8?OpenDocument",
#    ))
#build_simple_formula('cotpat_transport', FloatCol(function = cs_travail._cotpat_transport,
#    label = u"Cotisations sociales patronales: versement transport",
#    url = u"http://www.lesclesdelabanque.com/Web/Cdb/Entrepreneurs/Content.nsf/DocumentsByIDWeb/7APJB8?OpenDocument",
#    ))
#build_simple_formula('cotpat', FloatCol(function = cs_travail._cotpat,
#    label = u"Cotisations sociales patronales",
#    url = u"http://www.editions-tissot.fr/droit-travail/dictionnaire-droit-travail-definition.aspx?idDef=254&definition=Cotisations+patronales",
#    ))
#build_simple_formula('alleg_fillon', FloatCol(function = cs_travail._alleg_fillon,
#    label = u"Allègements Fillon sur les bas salaires",
#    url = u"http://travail-emploi.gouv.fr/informations-pratiques,89/fiches-pratiques,91/remuneration,113/l-allegement-de-charges-patronales,1031.html",
#    ))
#build_simple_formula('alleg_cice', FloatCol(function = cs_travail._alleg_cice,
#    label = u"Crédit d'impôt compétitivité emploi",
#    url = u"http://www.economie.gouv.fr/ma-competitivite/quest-que-credit-dimpot-pour-competitivite-et-lemploi",
#    ))
#build_simple_formula('taxes_sal', FloatCol(function = cs_travail._taxes_sal,
#    label = u"Taxes sur les salaires pour les employeurs non soumis à la TVA",
#    url = u"http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&impot=TS&pageId=prof_ts&sfid=50",
#    ))
#build_simple_formula('tehr', FloatCol(function = cs_travail._tehr,
#    label = u"taxe exceptionnelle de solidarité sur les très hautes rémunérations",
#    url = u"http://vosdroits.service-public.fr/particuliers/F31130.xhtml",
#    ))
#build_simple_formula('salsuperbrut', FloatCol(function = cs_travail._salsuperbrut,
#    label = u"Salaires super bruts",
#    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/cout-salarial.htm"
#    ))
#
#build_simple_formula('cotsal_contrib', FloatCol(function = cs_travail._cotsal_contrib,
#    label = u"Cotisations sociales salariales contributives",
#    url = u"http://www.editions-tissot.fr/droit-travail/dictionnaire-droit-travail-definition.aspx?idDef=255&definition=Cotisations+salariales",
#    ))
#build_simple_formula('cotsal_noncontrib', FloatCol(function = cs_travail._cotsal_noncontrib,
#    label = u"Cotisations sociales non salariales non-contributives",
#    ))
#build_simple_formula('cotsal', FloatCol(function = cs_travail._cotsal,
#    label = u"Cotisations sociales salariales",
#    url = u"http://vosdroits.service-public.fr/particuliers/F2302.xhtml#N100F8",
#    ))
#
#build_simple_formula('csgsald', FloatCol(function = cs_travail._csgsald,
#    label = u"CSG déductible sur les salaires",
#    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml",
#    ))
#build_simple_formula('csgsali', FloatCol(function = cs_travail._csgsali,
#    label = u"CSG imposables sur les salaires",
#    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml",
#    ))
#build_simple_formula('crdssal', FloatCol(function = cs_travail._crdssal,
#    label = u"CRDS sur les salaires",
#    url = u"http://vosdroits.service-public.fr/particuliers/N17580.xhtml",
#    ))
#build_simple_formula('sal', FloatCol(function = cs_travail._sal,
#    label = u"Salaires imposables",
#    url = u"http://www.jureka.fr/dico-francais-droit/lettre-s/definition-salaire-imposable",
#    ))
#build_simple_formula('salnet', FloatCol(function = cs_travail._salnet,
#    label = u"Salaires nets d'après définition INSEE",
#    url = u"http://www.trader-finance.fr/lexique-finance/definition-lettre-S/Salaire-net.html",
#    ))
#
## Fonctionnaires
#build_simple_formula('indemnite_residence', FloatCol(function = cs_travail._indemnite_residence,
#    label = u"Indemnité de résidence (fonction publique)",
#    url = u"http://www.fonction-publique.gouv.fr/fonction-publique/statut-et-remunerations-48",
#    ))
#build_simple_formula('supp_familial_traitement', FloatCol(function = cs_travail._supp_familial_traitement,
#    label = u"Supplément familial de traitement (fonction publique)",
#    start = date(2011, 1, 1),  # TODO: check this curious starting date
#    url= u"http://www.fonction-publique.gouv.fr/fonction-publique/statut-et-remunerations-48",
#    ))
#build_simple_formula('cot_pat_pension_civile', FloatCol(function = cs_travail._cot_pat_pension_civile,
#    label = u"Cotisation patronale pension civile",
#    url = u"http://www.ac-besancon.fr/spip.php?article2662",
#    ))
#build_simple_formula('cot_sal_pension_civile', FloatCol(function = cs_travail._cot_sal_pension_civile,
#    label = u"Cotisation salariale pension civile",
#    url = u"http://www.ac-besancon.fr/spip.php?article2662",
#    ))
#build_simple_formula('cot_pat_rafp', FloatCol(function = cs_travail._cot_pat_rafp, TODO: REMOVEME
#    label = u"Cotisation patronale RAFP",
#    url = u"http://www.rafp.fr/Cotisations-et-autres-types-dabondement-CET-fr-ru99/Les-cotisations-ar223",
#    ))
#build_simple_formula('cot_sal_rafp', FloatCol(function = cs_travail._cot_sal_rafp,
#    label = u"Cotisation salariale RAFP",
#    url = u"http://www.rafp.fr/Cotisations-et-autres-types-dabondement-CET-fr-ru99/Les-cotisations-ar223",
#    ))
#=======
#             ]),
#         url = u"http://fr.wikipedia.org/wiki/Professions_et_cat%C3%A9gories_socioprofessionnelles_en_France",
#         ))
#
#build_simple_formula(
#    'primes',
#    FloatCol(
#        function = cs_travail._primes,
#        label = u"Primes et indemnités des fonctionnaires",
#        url = u"http://vosdroits.service-public.fr/particuliers/F465.xhtml",
#    ))
#build_simple_formula(
#    'sal_h_b',
#    FloatCol(
#        function = cs_travail._sal_h_b,
#        label = u"Salaire horaire brut",
#        url = u"http://www.les-horaires.fr/pratique/smic-horaire.php",
#    ))
#
##    build_simple_formula('taille_entreprise', EnumCol(function = cs_travail._taille_entreprise,
##        enum = Enum([
##            u"Non pertinent",
##            u"Moins de 10 salariés",
##            u"De 10 à 19 salariés",
##            u"De 20 à 249 salariés",
##            u"Plus de 250 salariés",
##            ]),
##        label = u"Catégorie de taille d'entreprise (pour calcul des cotisations sociales)",
##        url = u"http://www.insee.fr/fr/themes/document.asp?ref_id=ip1321",
##        ))
#
#build_simple_formula('taux_accident_travail', FloatCol(function = cs_travail._taux_accident_travail,
#    label = u"Cotisations sociales patronales : accident du travail et maladies professionnelles",
#    url = u"http://www.lesclesdelabanque.com/Web/Cdb/Entrepreneurs/Content.nsf/DocumentsByIDWeb/7APJB8?OpenDocument",
#    ))
#build_simple_formula('cotpat_accident', FloatCol(function = cs_travail._cotpat_accident,
#    label = u"Cotisations sociales patronales : accident du travail et maladies professionnelles",
#    url = u"http://www.lesclesdelabanque.com/Web/Cdb/Entrepreneurs/Content.nsf/DocumentsByIDWeb/7APJB8?OpenDocument",
#    ))
#build_simple_formula('alleg_fillon', FloatCol(function = cs_travail._alleg_fillon,
#    label = u"Allègements Fillon sur les bas salaires",
#    url = u"http://travail-emploi.gouv.fr/informations-pratiques,89/fiches-pratiques,91/remuneration,113/l-allegement-de-charges-patronales,1031.html",
#    ))
#build_simple_formula('alleg_cice', FloatCol(function = cs_travail._alleg_cice,
#    label = u"Crédit d'impôt compétitivité emploi",
#    url = u"http://www.economie.gouv.fr/ma-competitivite/quest-que-credit-dimpot-pour-competitivite-et-lemploi",
#    ))
#build_simple_formula('taxes_sal', FloatCol(function = cs_travail._taxes_sal,
#    label = u"Taxes sur les salaires pour les employeurs non soumis à la TVA",
#    url = u"http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&impot=TS&pageId=prof_ts&sfid=50",
#    ))
#build_simple_formula('tehr', FloatCol(function = cs_travail._tehr,
#    label = u"taxe exceptionnelle de solidarité sur les très hautes rémunérations",
#    url = u"http://vosdroits.service-public.fr/particuliers/F31130.xhtml",
#    ))
#build_simple_formula('salsuperbrut', FloatCol(function = cs_travail._salsuperbrut,
#    label = u"Salaires super bruts",
#    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/cout-salarial.htm"
#    ))
#
## Fonctionnaires
#build_simple_formula('indemnite_residence', FloatCol(function = cs_travail._indemnite_residence,
#    label = u"Indemnité de résidence (fonction publique)",
#    url = u"http://www.fonction-publique.gouv.fr/fonction-publique/statut-et-remunerations-48",
#    ))
#build_simple_formula('supp_familial_traitement', FloatCol(function = cs_travail._supp_familial_traitement,
#    label = u"Supplément familial de traitement (fonction publique)",
#    start = date(2011, 1, 1),  # TODO: check this curious starting date
#    url= u"http://www.fonction-publique.gouv.fr/fonction-publique/statut-et-remunerations-48",
#    ))
#build_simple_formula('cot_sal_rafp', FloatCol(function = cs_travail._cot_sal_rafp,
#    label = u"Cotisation salariale RAFP",
#    url = u"http://www.rafp.fr/Cotisations-et-autres-types-dabondement-CET-fr-ru99/Les-cotisations-ar223",
#    ))
#>>>>>>> openfisca/master

# Revenus non-salariés
# build_simple_formula('rev_microsocial', FloatCol(function = cs_travail._rev_microsocial,
#     label = u"Revenu net des cotisations sociales pour le régime microsocial",
#     start = date(2009, 1, 1),
#     url = u"http://www.apce.com/pid6137/regime-micro-social.html",
#     ))

# Revenus du capital soumis au prélèvement libératoire
# build_simple_formula('csg_cap_lib', FloatCol(function = cs_capital._csg_cap_lib,
#     label = u"CSG sur les revenus du capital soumis au prélèvement libératoire",
#     url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e",
#     ))
# build_simple_formula('crds_cap_lib', FloatCol(function = cs_capital._crds_cap_lib,
#     label = u"CRDS sur les revenus du capital soumis au prélèvement libératoire",
#     url = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale",
#     ))
# build_simple_formula('prelsoc_cap_lib', FloatCol(function = cs_capital._prelsoc_cap_lib, entity = 'foy',
#     label = u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire",
#     url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS",
#     ))

# Revenus du capital soumis au barème
# build_simple_formula('csg_cap_bar', FloatCol(function = cs_capital._csg_cap_bar,
#     label = u"CSG sur les revenus du capital soumis au barème",
#     url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e",
#     ))
# build_simple_formula('crds_cap_bar', FloatCol(function = cs_capital._crds_cap_bar,
#     label = u"CRDS sur les revenus du capital soumis au barème",
#     url = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale",
#     ))
# build_dated_formula('prelsoc_cap_bar',
#     [
#         dict(start = date(2002, 1, 1),
#           end = date(2005, 12, 31),
#           function = cs_capital._prelsoc_cap_bar__2005,
#          ),
#         dict(start = date(2006, 1, 1),
#           end = date(2008, 12, 31),
#           function = cs_capital._prelsoc_cap_bar_2006_2008,
#          ),
#         dict(start = date(2009, 1, 1),
#           end = date(2015, 12, 31),
#           function = cs_capital._prelsoc_cap_bar_2009_,
#          ),
#     ],
#     FloatCol(entity='ind',
#     label = u"Prélèvements sociaux sur les revenus du capital soumis au barème",
#     url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"))

# Revenus fonciers (sur les foyers)
build_simple_formula('csg_fon', FloatCol(function = cs_capital._csg_fon,
    entity = "foy",
    label = u"CSG sur les revenus fonciers",
    url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e",
    ))
build_simple_formula('crds_fon', FloatCol(function = cs_capital._crds_fon,
    entity = "foy",
    label = u"CRDS sur les revenus fonciers",
    url = u"http://vosdroits.service-public.fr/particuliers/F2329.xhtml",
    ))
build_dated_formula('prelsoc_fon',
    [
        dict(start = date(2002, 1, 1),
          end = date(2005, 12, 31),
          function = cs_capital._prelsoc_fon__2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = cs_capital._prelsoc_fon_2006_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2015, 12, 31),
          function = cs_capital._prelsoc_fon_2009_,
         ),
    ],
    FloatCol(entity="foy",
    label = u"Prélèvements sociaux sur les revenus fonciers",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS",
    ))

# Plus values de cessions de valeurs mobilières
build_simple_formula('csg_pv_mo', FloatCol(function = cs_capital._csg_pv_mo,
    entity = "foy",
    label = u"CSG sur les plus-values de cession de valeurs mobilières",
    url = u"http://vosdroits.service-public.fr/particuliers/F21618.xhtml",
    ))
build_simple_formula('crds_pv_mo', FloatCol(function = cs_capital._crds_pv_mo,
    entity = "foy",
    label = u"CRDS sur les plus-values de cession de valeurs mobilières",
    url = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale",
    ))
build_dated_formula('prelsoc_pv_mo',
    [
        dict(start = date(2002, 1, 1),
          end = date(2005, 12, 31),
          function = cs_capital._prelsoc_pv_mo__2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = cs_capital._prelsoc_pv_mo_2006_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2015, 12, 31),
          function = cs_capital._prelsoc_pv_mo_2009_,
         ),
    ],
    FloatCol(entity="foy",
    label = u"Prélèvements sociaux sur les plus-values de cession de valeurs mobilières",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"))
# Plus-values immobilières
build_simple_formula('csg_pv_immo', FloatCol(function = cs_capital._csg_pv_immo,
    entity = "foy",
    label = u"CSG sur les plus-values immobilières",
    url = u"http://fr.wikipedia.org/wiki/Contribution_sociale_g%C3%A9n%C3%A9ralis%C3%A9e",
    ))
build_simple_formula('crds_pv_immo', FloatCol(function = cs_capital._crds_pv_immo,
    entity = "foy",
    label = u"CRDS sur les plus-values immobilières",
    url = u"http://fr.wikipedia.org/wiki/Contribution_pour_le_remboursement_de_la_dette_sociale",
    ))
build_dated_formula('prelsoc_pv_immo',
    [
        dict(start = date(2002, 1, 1),
          end = date(2005, 12, 31),
          function = cs_capital._prelsoc_pv_immo__2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = cs_capital._prelsoc_pv_immo_2006_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2015, 12, 31),
          function = cs_capital._prelsoc_pv_immo_2009_,
         ),
    ],
    FloatCol(entity="foy",
    label = u"Prélèvements sociaux sur les plus-values immobilières",
    url = u"http://www.pap.fr/argent/impots/les-plus-values-immobilieres/a1314/l-imposition-de-la-plus-value-immobiliere",
    ))

############################################################
# Impôt sur le revenu
############################################################
#build_alternative_formula(  TODO: REMOVEME new syntax in irpp.py
#    'age',
#    [
#        ir._age_from_birth,
#        ir._age_from_agem,
#        ],
#    AgeCol(label = u"Âge (en années)", val_type = "age"),
#    )

build_alternative_formula(
    'agem',
    [
        ir._agem_from_birth,
        ir._agem_from_age,
        ],
    AgeCol(label = u"Âge (en mois)", val_type = "months"),
    )

# build_simple_formula('nbF', PeriodSizeIndependentIntCol(function = ir._nbF,
#     cerfa_field = u'F',
#     entity = 'foy',
#     label = u"Nombre d'enfants à charge  non mariés de moins de 18 ans au 1er janvier de l'année de perception des"
#         u" revenus, ou nés en durant la même année ou handicapés quel que soit leur âge",
#     ))
# build_simple_formula('nbG', PeriodSizeIndependentIntCol(function = ir._nbG,
#     cerfa_field = u'G',
#     entity = 'foy',
#     label = u"Nombre d'enfants à charge titulaires de la carte d'invalidité",
#     ))
# TODO: vérifier si c'est bien ça pour la nbH et la caseH qui suit
# build_simple_formula('nbH', PeriodSizeIndependentIntCol(function = ir._nbH,
#     cerfa_field = u'H',
#     entity = 'foy',
#     label = u"Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de"
#         u" l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge",
#     ))
# build_simple_formula('nbI', PeriodSizeIndependentIntCol(function = ir._nbI,
#     cerfa_field = u'I',
#     entity = 'foy',
#     label = u"Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité",
#     ))
# build_simple_formula('nbJ', PeriodSizeIndependentIntCol(function = ir._nbJ,
#     cerfa_field = u'J',
#     entity = 'foy',
#     label = u"Nombre d'enfants majeurs célibataires sans enfant",
#     ))
#    build_simple_formula('nbN', PeriodSizeIndependentIntCol(function = ir._nbN,
#        cerfa_field = u'N',
#        entity = 'foy',
#        label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille",
#        ))
#    build_simple_formula('nbR', PeriodSizeIndependentIntCol(function = ir._nbR,
#        cerfa_field = u'R',
#        entity = 'foy',
#        label = u"Nombre de titulaires de la carte invalidité d'au moins 80 %",
#        ))

build_simple_formula('marpac', BoolCol(function = ir._marpac,
    entity = 'foy'))
build_simple_formula('celdiv', BoolCol(function = ir._celdiv,
    entity = 'foy'))
build_simple_formula('veuf', BoolCol(function = ir._veuf,
    entity = 'foy'))
build_simple_formula('jveuf', BoolCol(function = ir._jveuf,
    entity = 'foy'))
build_simple_formula('nbptr', FloatCol(function = ir._nbptr,
    entity = 'foy',
    label = u"Nombre de parts",
    url = u"http://vosdroits.service-public.fr/particuliers/F2705.xhtml",
    ))
build_simple_formula('rbg', FloatCol(function = ir._rbg,
    entity = 'foy',
    label = u"Revenu brut global",
    url = u"http://www.documentissime.fr/dossiers-droit-pratique/dossier-19-l-impot-sur-le-revenu-les-modalites-generales-d-imposition/la-determination-du-revenu-imposable/le-revenu-brut-global.html",
    ))

# charges déductibles
build_simple_formula('cd_penali', FloatCol(function = cd._cd_penali,
    entity = 'foy',
    url = u"http://frederic.anne.free.fr/Cours/ITV.htm",
    ))
build_simple_formula('cd_acc75a', FloatCol(function = cd._cd_acc75a,
    entity = 'foy'))
build_dated_formula('cd_percap',
    [
        dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = cd._cd_percap_2002,
         ),
        dict(start = date(2003, 1, 1),
          end = date(2006, 12, 31),
          function = cd._cd_percap_2003_2006,
         ),
    ],
    FloatCol(entity='foy'))
build_simple_formula('cd_deddiv', FloatCol(function = cd._cd_deddiv,
    entity = 'foy'))
build_simple_formula('cd_doment', FloatCol(function = cd._cd_doment,
    entity = 'foy',
    start = date(2002, 1, 1),
    end = date(2005, 12, 31)))
build_simple_formula('cd_eparet', FloatCol(function = cd._cd_eparet,
    entity = 'foy',
    start = date(2004, 1, 1)))
build_simple_formula('cd_sofipe', FloatCol(function = cd._cd_sofipe,
    entity = 'foy',
    start = date(2002, 1, 1),
    end = date(2006, 12, 31)))
build_simple_formula('cd_cinema', FloatCol(function = cd._cd_cinema,
    entity = 'foy',
    start = date(2002, 1, 1),
    end = date(2005, 12, 31)))
build_simple_formula('cd_ecodev', FloatCol(function = cd._cd_ecodev,
    entity = 'foy',
    start = date(2007, 1, 1),
    end = date(2008, 12, 31)))
build_simple_formula('cd_grorep', FloatCol(function = cd._cd_grorep,
    entity = 'foy',
    start = date(2009, 1, 1)))

build_simple_formula('charges_deduc_reforme', FloatCol(function = cd._charges_deduc_reforme,
    entity = 'foy',
    url = u"http://www.bfmtv.com/economie/reforme-fiscale-csg-bientot-plus-deductible-l-impot-revenu-700700.html",
    ))
build_simple_formula('charge_loyer', FloatCol(function = cd._charge_loyer,
    entity = 'foy',
    url = u"http://vosdroits.service-public.fr/particuliers/F1991.xhtml",
    ))

build_simple_formula('rbg_int', FloatCol(function = cd._rbg_int,
    entity = 'foy',
    label = u"Revenu brut global intermédiaire",
    ))

build_dated_formula(
    'cd1',
    [dict(start = date(2002, 1, 1),
         end = date(2003, 12, 31),
         function = cd._cd1_2002_2003,
         ),
     dict(start = date(2004, 1, 1),
         end = date(2005, 12, 31),
         function = cd._cd1_2004_2005,
         ),
     dict(start = date(2006, 1, 1),
         end = date(2006, 12, 31),
         function = cd._cd1_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2008, 12, 31),
         function = cd._cd1_2007_2008,
         ),
     dict(start = date(2009, 1, 1),
         end = date(2013, 12, 31),
         function = cd._cd1_2009_2013,
         ),
     dict(start = date(2014, 1, 1),
         end = date(2014, 12, 31),
         function = cd._cd1_2014,
         ),
    ],
    FloatCol(entity = 'foy',
    label = u"Charges déductibles non plafonnées",
    url = u"http://impotsurlerevenu.org/definitions/215-charge-deductible.php"))

build_dated_formula(
    'cd2',
    [dict(start = date(2002, 1, 1),
         end = date(2005, 12, 31),
         function = cd._cd2_2002_2005,
         ),
     dict(start = date(2006, 1, 1),
         end = date(2006, 12, 31),
         function = cd._cd2_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2008, 12, 31),
         function = cd._cd2_2007_2008,
         ),
    ],
    FloatCol(entity = 'foy',
    label = u"Charges déductibles plafonnées",
    url = u"http://impotsurlerevenu.org/definitions/215-charge-deductible.php"))

build_simple_formula('charges_deduc', FloatCol(function = cd._charges_deduc,
    entity = 'foy',
    label = u"Charges déductibles",
    url = u"http://impotsurlerevenu.org/definitions/215-charge-deductible.php",
    ))

build_simple_formula('defrag', FloatCol(function = ir._defrag,
    entity = 'foy',
    label = u"Déficit agricole des années antérieures",
    ))

build_simple_formula('defacc', FloatCol(function = ir._defacc,
    entity = 'foy',
    label = u"Déficit industriels et commerciaux non professionnels des années antérieures",
    ))

build_simple_formula('defmeu', FloatCol(function = ir._defmeu,
    entity = 'foy',
    label = u"Déficit des locations meublées non professionnelles des années antérieures",
    ))

build_simple_formula('defncn', FloatCol(function = ir._defncn,
    entity = 'foy',
    label = u"Déficit non commerciaux non professionnels des années antérieures",
    ))

build_simple_formula('rfr_cd', FloatCol(function = cd._rfr_cd,
    entity = 'foy',
    label = u"Charges déductibles entrant dans le revenus fiscal de référence",
    url = u"http://impotsurlerevenu.org/definitions/215-charge-deductible.php",
    ))  # TODO

build_simple_formula('rng', FloatCol(function = ir._rng,
    entity = 'foy',
    label = u"Revenu net global",
    url = u"http://impotsurlerevenu.org/definitions/114-revenu-net-global.php",
    ))
build_simple_formula('rni', FloatCol(function = ir._rni,
    entity = 'foy',
    label = u"Revenu net imposable",
    url = u"http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php",
    ))

build_simple_formula('abat_spe', FloatCol(function = ir._abat_spe,
    entity = 'foy',
    label = u"Abattements spéciaux",
    url = u"http://bofip.impots.gouv.fr/bofip/2036-PGP",
    ))
build_simple_formula('deficit_ante', FloatCol(function = ir._deficit_ante,
    entity = 'foy',
    label = u"Déficit global antérieur",
    url = u"http://impotsurlerevenu.org/declaration-de-revenus-fonciers-2044/796-deficits-anterieurs-restant-a-imputer-cadre-450.php",
    ))

build_simple_formula('rev_sal', FloatCol(function = ir._rev_sal))
build_simple_formula('salcho_imp', FloatCol(function = ir._salcho_imp))
build_simple_formula('rev_pen', FloatCol(function = ir._rev_pen))
build_simple_formula('pen_net', FloatCol(function = ir._pen_net))
build_simple_formula('indu_plaf_abat_pen', FloatCol(function = ir._indu_plaf_abat_pen,
    entity = 'foy'))
build_simple_formula('abat_sal_pen', FloatCol(function = ir._abat_sal_pen,
    start = date(2002, 1, 1),
    end = date(2005, 12, 31)))
build_simple_formula('sal_pen_net', FloatCol(function = ir._sal_pen_net))
# build_simple_formula('rto', FloatCol(function = ir._rto,
#     label = u'Rentes viagères (rentes à titre onéreux)',
#     url = u"http://fr.wikipedia.org/wiki/Rente_viag%C3%A8re",
#     ))
# build_simple_formula('rto_net', FloatCol(function = ir._rto_net,
#     label = u'Rentes viagères après abattements',
#     url = u"http://www.lafinancepourtous.fr/Vie-professionnelle-et-retraite/Retraite/Epargne-retraite/La-rente-viagere/La-fiscalite-de-la-rente-viagere",
#     ))
build_simple_formula('tspr', FloatCol(function = ir._tspr))

build_simple_formula('rev_cat_tspr', FloatCol(function = ir._rev_cat_tspr,
    entity = 'foy',
    label = u"Revenu catégoriel - Salaires, pensions et rentes",
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm",
    ))
build_dated_formula('rev_cat_rvcm',
    [
        dict(start = date(2002, 1, 1),
          end = date(2004, 12, 31),
          function = ir._rev_cat_rvcm__2004,
         ),
        dict(start = date(2005, 1, 1),
          end = date(2012, 12, 31),
          function = ir._rev_cat_rvcm_2005_2012,
         ),
        dict(start = date(2013, 1, 1),
          end = date(2015, 12, 31),
          function = ir._rev_cat_rvcm_2013_,
         ),
    ],
    FloatCol(entity='foy',
    label = u'Revenu catégoriel - Capitaux',
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm"))
build_simple_formula('rev_cat_rpns', FloatCol(function = ir._rev_cat_rpns,
    entity = 'foy',
    label = u'Revenu catégoriel - Rpns',
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm",
    ))
build_simple_formula('rev_cat_rfon', FloatCol(function = ir._rev_cat_rfon,
    entity = 'foy',
    label = u'Revenu catégoriel - Foncier',
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm",
    ))
build_simple_formula('rev_cat_pv', FloatCol(function = ir._rev_cat_pv,
    entity = 'foy',
    label = u'Revenu catégoriel - Plus-values',
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm",
    start = date(2013, 1, 1)))
build_simple_formula('rev_cat', FloatCol(function = ir._rev_cat,
    entity = 'foy',
    label = u"Revenus catégoriels",
    url = u"http://www.insee.fr/fr/methodes/default.asp?page=definitions/revenus-categoriesl.htm",
    ))
build_simple_formula('deficit_rcm', FloatCol(function = ir._deficit_rcm,
    entity = 'foy',
    label = u'Deficit capitaux mobiliers',
    url = u"http://www.lefigaro.fr/impots/2008/04/25/05003-20080425ARTFIG00254-les-subtilites-des-revenus-de-capitaux-mobiliers-.php",
    start = date(2009,1,1)))
build_simple_formula('csg_deduc_patrimoine_simulated', FloatCol(function = ir._csg_deduc_patrimoine_simulated,
    entity = 'foy',
    label = u'Csg déductible sur le patrimoine simulée',
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS",
    ))
build_simple_formula('csg_deduc_patrimoine', FloatCol(function = ir._csg_deduc_patrimoine,
    entity = 'foy',
    label = u'Csg déductible sur le patrimoine',
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS",
    ))
build_simple_formula('csg_deduc', FloatCol(function = ir._csg_deduc,
    entity = 'foy',
    label = u'Csg déductible sur le patrimoine',
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&typePage=cpr02&sfid=503&espId=1&communaute=1&impot=CS",
    ))

build_dated_formula('plus_values',
    [
        dict(start = date(2007, 1, 1),
          end = date(2007, 12, 31),
          function = ir._plus_values__2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2011, 12, 31),
          function = ir._plus_values_2008_2011,
         ),
        dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ir._plus_values_2012,
         ),
        dict(start = date(2013, 1, 1),
          end = date(2015, 12, 31),
          function = ir._plus_values_2013_,
         ),
    ],
    FloatCol(entity='foy'))
build_simple_formula('ir_brut', FloatCol(function = ir._ir_brut,
    entity = 'foy'))
build_simple_formula('nb_pac', FloatCol(function = ir._nb_pac,
    entity = 'foy'))
build_simple_formula('nb_adult', FloatCol(function = ir._nb_adult,
    entity = 'foy'))
build_simple_formula('ir_ss_qf', FloatCol(function = ir._ir_ss_qf,
    entity = 'foy'))
build_simple_formula('ir_plaf_qf', FloatCol(function = ir._ir_plaf_qf,
    entity = 'foy'))
build_simple_formula('avantage_qf', FloatCol(function = ir._avantage_qf,
    entity = 'foy'))
build_simple_formula('nat_imp', BoolCol(function = ir._nat_imp,
    entity = 'foy'))
build_simple_formula('decote', FloatCol(function = ir._decote,
    entity = 'foy'))

# réductions d'impots
#    build_simple_formula('donapd', FloatCol(function = ri._donapd,
#        entity = 'foy'))
build_dated_formula(
    'donapd',
    [dict(start = date(2002, 1, 1),
         end = date(2010, 12, 31),
         function = ri._donapd_2002_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2013, 12, 31),
         function = ri._donapd_2011_2013,
         ),
    ],
    FloatCol(entity = 'foy'))
#    build_simple_formula('dfppce', FloatCol(function = ri._dfppce,
#        entity = 'foy'))
build_dated_formula(
    'dfppce',
    [dict(start = date(2002, 1, 1),
         end = date(2003, 12, 31),
         function = ri._dfppce_2002_2003,
         ),
     dict(start = date(2004, 1, 1),
             end = date(2004, 12, 31),
             function = ri._dfppce_2004,
             ),
     dict(start = date(2005, 1, 1),
             end = date(2005, 12, 31),
             function = ri._dfppce_2005,
             ),
     dict(start = date(2006, 1, 1),
             end = date(2006, 12, 31),
             function = ri._dfppce_2006,
             ),
     dict(start = date(2007, 1, 1),
             end = date(2007, 12, 31),
             function = ri._dfppce_2007,
             ),
     dict(start = date(2008, 1, 1),
             end = date(2010, 12, 31),
             function = ri._dfppce_2008_2010,
             ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._dfppce_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._dfppce_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._dfppce_2013,
         ),
    ],
    FloatCol(entity = 'foy'))

build_simple_formula('cotsyn', FloatCol(function = ri._cotsyn,
    entity = 'foy'))
build_dated_formula('resimm', [
     dict(start = date(2009, 1, 1),
         end = date(2010, 12, 31),
         function = ri._resimm_2009_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._resimm_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._resimm_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._resimm_2013,
         ),
],
FloatCol(entity = 'foy'))
build_dated_formula('patnat', [
     dict(start = date(2010, 1, 1),
         end = date(2010, 12, 31),
         function = ri._patnat_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._patnat_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._patnat_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._patnat_2013,
         ),
],
FloatCol(entity = 'foy'))
build_simple_formula('sofipe', FloatCol(function = ri._sofipe,
    entity = 'foy',
    start = date(2009, 1, 1),
    end = date(2011, 1, 1)))
build_dated_formula('saldom',
    [
     dict(start = date(2002, 1, 1),
         end = date(2004, 12, 31),
         function = ri._saldom_2002_2004,
         ),
     dict(start = date(2005, 1, 1),
         end = date(2006, 12, 31),
         function = ri._saldom_2005_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2008, 12, 31),
         function = ri._saldom_2007_2008,
         ),
     dict(start = date(2009, 1, 1),
         end = date(2013, 12, 31),
         function = ri._saldom_2009_2013,
         ),
    ],
    FloatCol(entity= 'foy'))
build_simple_formula('intagr', FloatCol(function = ri._intagr,
    entity = 'foy',
    start = date(2005, 1, 1)))
build_simple_formula('duflot', FloatCol(function = ri._duflot,
    entity = 'foy',
    start = date(2013, 1, 1)))
build_simple_formula('prcomp', FloatCol(function = ri._prcomp,
    entity = 'foy'))
build_dated_formula('spfcpi',
    [
     dict(start = date(2002, 1, 1), #quid d'avant 2002 ?
         end = date(2002, 12, 31),
         function = ri._spfcpi_2002,
         ),
     dict(start = date(2003, 1, 1),
         end = date(2006, 12, 31),
         function = ri._spfcpi_2003_2006,
         ),
     dict(start = date(2007, 1, 1),
         end = date(2010, 12, 31),
         function = ri._spfcpi_2007_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2013, 12, 31),
         function = ri._spfcpi_2011_2013,
         ),
     dict(start = date(2014, 1, 1),
         end = date(2014, 12, 31),
         function = ri._spfcpi_2014,
         ),
    ],
    FloatCol(entity= 'foy'))
build_simple_formula('mohist', FloatCol(function = ri._mohist,
    entity = 'foy',
    start = date(2008, 1, 1)))
build_simple_formula('sofica', FloatCol(function = ri._sofica,
    entity = 'foy',
    start = date(2006, 1, 1)))
build_dated_formula('cappme',
    [
     dict(start = date(2002, 1, 1), #quid d'avant 2002 ?
         end = date(2002, 12, 31),
         function = ri._cappme_2002,
         ),
     dict(start = date(2003, 1, 1),
         end = date(2003, 12, 31),
         function = ri._cappme_2003,
         ),
     dict(start = date(2004, 1, 1),
         end = date(2004, 12, 31),
         function = ri._cappme_2004,
         ),
     dict(start = date(2005, 1, 1),
         end = date(2008, 12, 31),
         function = ri._cappme_2005_2008,
         ),
     dict(start = date(2009, 1, 1),
         end = date(2010, 12, 31),
         function = ri._cappme_2009_2010,
         ),
     dict(start = date(2011, 1, 1),
         end = date(2011, 12, 31),
         function = ri._cappme_2011,
         ),
     dict(start = date(2012, 1, 1),
         end = date(2012, 12, 31),
         function = ri._cappme_2012,
         ),
     dict(start = date(2013, 1, 1),
         end = date(2013, 12, 31),
         function = ri._cappme_2013,
         ),
    ],
    FloatCol(entity= 'foy'))
build_simple_formula('repsoc', FloatCol(function = ri._repsoc,
    entity = 'foy',
    start = date(2003, 1, 1)))
build_dated_formula('invfor',
[
 dict(start = date(2002, 1, 1),
      end = date(2005, 12, 31),
      function = ri._invfor_2002_2005,
      ),
 dict(start = date(2006, 1, 1),
      end = date(2008, 12, 31),
      function = ri._invfor_2006_2008,
      ),
 dict(start = date(2009, 1, 1),
      end = date(2009, 12, 31),
      function = ri._invfor_2009,
      ),
 dict(start = date(2010, 1, 1),
      end = date(2010, 12, 31),
      function = ri._invfor_2010,
      ),
 dict(start = date(2011, 1, 1),
      end = date(2011, 12, 31),
      function = ri._invfor_2011,
      ),
 dict(start = date(2012, 1, 1),
      end = date(2012, 12, 31),
      function = ri._invfor_2012,
      ),
 dict(start = date(2013, 1, 1),
      end = date(2013, 12, 31),
      function = ri._invfor_2013,
      ),
],
FloatCol(entity = 'foy'))
build_simple_formula('deffor', FloatCol(function = ri._deffor,
    entity = 'foy',
    start = date(2006, 1, 1)))
build_simple_formula('daepad', FloatCol(function = ri._daepad,
    entity = 'foy'))
build_simple_formula('rsceha', FloatCol(function = ri._rsceha,
    entity = 'foy'))
build_dated_formula('invlst',
    [
     dict(start = date(2004, 1, 1),
          end = date(2004, 12, 31),
          function = ri._invlst_2004,
          ),
     dict(start = date(2005, 1, 1),
          end = date(2010, 12, 31),
          function = ri._invlst_2005_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._invlst_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._invlst_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._invlst_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula('domlog',
    [
     dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = ri._domlog_2002,
          ),
     dict(start = date(2003, 1, 1),
          end = date(2004, 12, 31),
          function = ri._domlog_2003_2004,
          ),
     dict(start = date(2005, 1, 1),
          end = date(2007, 12, 31),
          function = ri._domlog_2005_2007,
          ),
     dict(start = date(2008, 1, 1),
          end = date(2008, 12, 31),
          function = ri._domlog_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._domlog_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._domlog_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._domlog_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._domlog_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._domlog_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_simple_formula('adhcga', FloatCol(function = ri._adhcga,
    entity = 'foy'))
build_dated_formula('creaen',
    [
     dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = ri._creaen_2006_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._creaen_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2011, 12, 31),
          function = ri._creaen_2010_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2014, 12, 31),
          function = ri._creaen_2012_2014,
          ),
    ],
    FloatCol(entity = 'foy'))
build_simple_formula('ecpess', FloatCol(function = ri._ecpess,
    entity = 'foy'))
build_dated_formula('scelli',
    [
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._scelli_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._scelli_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._scelli_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._scelli_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._scelli_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula('locmeu',
    [
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._locmeu_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._locmeu_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._locmeu_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._locmeu_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._locmeu_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula('doment',
    [
     dict(start = date(2005, 1, 1),
          end = date(2005, 12, 31),
          function = ri._doment_2005,
          ),
     dict(start = date(2006, 1, 1),
          end = date(2008, 12, 31),
          function = ri._doment_2006_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._doment_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._doment_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._doment_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._doment_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._doment_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_dated_formula('domsoc',
    [
     dict(start = date(2010, 1, 1),
          end = date(2012, 12, 31),
          function = ri._domsoc_2010_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 12, 31),
          function = ri._domsoc_2013,
          ),
    ],
    FloatCol(entity = 'foy'))
build_simple_formula('intemp', FloatCol(function = ri._intemp,
    entity = 'foy',
    start = date(2002, 1, 1),
    end = date(2003, 12, 31)))
build_dated_formula('garext',
    [
     dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = ri._garext_2002,
          ),
     dict(start = date(2003, 1, 1),
          end = date(2005, 12, 31),
          function = ri._garext_2003_2005,
          ),
    ],
    FloatCol(entity = 'foy'))
build_simple_formula('assvie', FloatCol(function = ri._assvie,
    entity = 'foy',
    start = date(2002, 1, 1),
    end = date(2004, 12, 31)))
build_simple_formula('invrev', FloatCol(function = ri._invrev,
    entity = 'foy',
    start = date(2002, 1, 1),
    end = date(2003, 12, 31)))
build_simple_formula('intcon', FloatCol(function = ri._intcon,
    entity = 'foy',
    start = date(2004, 1, 1),
    end = date(2005, 12, 31)))
build_simple_formula('ecodev', FloatCol(function = ri._ecodev,
    entity = 'foy',
    start = date(2009, 1, 1),
    end = date(2009, 12, 31)))

build_simple_formula('nb_pac2', FloatCol(function = ci._nb_pac2,
    entity = 'foy'))

build_simple_formula('creimp_exc_2008', FloatCol(function = ci._creimp_exc_2008,
    entity = 'foy'))

build_simple_formula('ip_net', FloatCol(function = ir._ip_net,
    entity = 'foy'))
#    build_simple_formula('reductions', FloatCol(function = ri._reductions,
#        entity = 'foy'))
build_dated_formula(
    'reductions',
    [dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = ri._reductions_2002,
          ),
     dict(start = date(2003, 1, 1),
          end = date(2004, 12, 31),
          function = ri._reductions_2003_2004,
          ),
     dict(start = date(2005, 1, 1),
          end = date(2005, 12, 31),
          function = ri._reductions_2005,
          ),
    dict(start = date(2006, 1, 1),
         end = date(2006, 12, 31),
         function = ri._reductions_2006,
         ),
     dict(start = date(2007, 1, 1),
          end = date(2007, 12, 31),
          function = ri._reductions_2007,
          ),
     dict(start = date(2008, 1, 1),
          end = date(2008, 12, 31),
          function = ri._reductions_2008,
          ),
     dict(start = date(2009, 1, 1),
          end = date(2009, 12, 31),
          function = ri._reductions_2009,
          ),
     dict(start = date(2010, 1, 1),
          end = date(2010, 12, 31),
          function = ri._reductions_2010,
          ),
     dict(start = date(2011, 1, 1),
          end = date(2011, 12, 31),
          function = ri._reductions_2011,
          ),
     dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = ri._reductions_2012,
          ),
     dict(start = date(2013, 1, 1),
          end = date(2013, 1, 1),
          function = ri._reductions_2013,
          ),
     ],
    FloatCol(entity = 'foy'))

build_simple_formula('iaidrdi', FloatCol(function = ir._iaidrdi,
    entity = 'foy'))
build_simple_formula('teicaa', FloatCol(function = ir._teicaa,
    entity = 'foy'))
build_simple_formula('cont_rev_loc', FloatCol(function = ir._cont_rev_loc,
    entity = 'foy',
    start = date(2001, 1, 1)))
build_simple_formula('iai', FloatCol(function = ir._iai,
    entity = 'foy',
    label = u"Impôt avant imputations",
    url = u"http://forum-juridique.net-iris.fr/finances-fiscalite-assurance/43963-declaration-impots.html",
    ))
build_simple_formula('cehr', FloatCol(function = ir._cehr,
    entity = 'foy',
    label = u"Contribution exceptionnelle sur les hauts revenus",
    url = u"http://www.legifrance.gouv.fr/affichCode.do?cidTexte=LEGITEXT000006069577&idSectionTA=LEGISCTA000025049019",
    ))
#    build_simple_formula('cesthra', FloatCol(function = ir._cesthra,
#        entity = 'foy',
#        start = date(2013, 1, 1),
#        )) # PLF 2013, amendement rejeté
build_dated_formula('imp_lib',# TODO: Check - de 2000euros
    [
        dict(start = date(2002, 1, 1),
          end = date(2007, 12, 31),
          function = ir._imp_lib__2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2012, 12, 31),
          function = ir._imp_lib_2008_,
         ),
    ],
    FloatCol(entity='foy',
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS"))
build_simple_formula('assiette_vente', FloatCol(function = ir._micro_social_vente,
    entity = 'foy',
    start = date(2009, 1, 1)))
build_simple_formula('assiette_service', FloatCol(function = ir._micro_social_service,
    entity = 'foy',
    start = date(2009, 1, 1)))
build_simple_formula('assiette_proflib', FloatCol(function = ir._micro_social_proflib,
    entity = 'foy',
    start = date(2009, 1, 1)))
build_simple_formula('microsocial', FloatCol(function = ir._micro_social_2009_,
    entity = 'foy',
    start = date(2009, 1, 1),
    url = u"http://fr.wikipedia.org/wiki/R%C3%A9gime_micro-social",
    ))
build_simple_formula('taux_effectif', FloatCol(function = ir._taux_effectif,
    entity = 'foy',
    start = date(2009, 1, 1)))
build_simple_formula('microentreprise', FloatCol(function = ir._micro_entreprise,
    entity = 'foy',
    start = date(2009, 1, 1)))

# Prime pour l'emploi
build_simple_formula('rev_act_nonsal', FloatCol(function = ir._rev_act_nonsal,
    entity = 'ind'))
build_simple_formula('rev_act_sal', FloatCol(function = ir._rev_act_sal,
    entity = 'ind'))
build_simple_formula('rev_act', FloatCol(function = ir._rev_act,
    entity = 'ind'))
build_simple_formula('ppe_coef', FloatCol(function = ir._ppe_coef,
    entity = 'foy'))
build_simple_formula('ppe_base', FloatCol(function = ir._ppe_base))
build_simple_formula('ppe_coef_tp', FloatCol(function = ir._ppe_coef_tp))
build_simple_formula('ppe_elig', BoolCol(function = ir._ppe_elig,
    entity = 'foy'))
build_simple_formula('ppe_elig_i', BoolCol(function = ir._ppe_elig_i))
build_simple_formula('ppe_rev', FloatCol(function = ir._ppe_rev))
build_simple_formula('ppe_brute', FloatCol(function = ir._ppe_brute,
    entity = 'foy',
    label = u"Prime pour l'emploi brute",
    ))
build_simple_formula('ppe', FloatCol(function = ir._ppe,
    entity = 'foy',
    label = u"Prime pour l'emploi",
    url = u"http://vosdroits.service-public.fr/particuliers/F2882.xhtml",
    ))

# Autres crédits d'impôts
#    build_simple_formula('creimp', FloatCol(function = ci._creimp,
#        entity = 'foy')) #TODO : adrien transform as credit_impot

build_dated_formula('creimp',  #TODO: Change name to credits_impot (before, take care of imputations)
    [
        dict(  #right way to ident dictionary
            start = date(2002, 1, 1),
            end = date(2002, 12, 31),
            function = ci._creimp_2002,
            ),
        dict(start = date(2003, 1, 1),
                 end = date(2003, 12, 31),
                 function = ci._creimp_2003,
                 ),
        dict(start = date(2004, 1, 1),
                 end = date(2004, 12, 31),
                 function = ci._creimp_2004,
                 ),
        dict(start = date(2005, 1, 1),
                 end = date(2005, 12, 31),
                 function = ci._creimp_2005,
                 ),

        dict(start = date(2006, 1, 1),
                 end = date(2006, 12, 31),
                 function = ci._creimp_2006,
                 ),
        dict(start = date(2007, 1, 1),
                 end = date(2007, 12, 31),
                 function = ci._creimp_2007,
                 ),
        dict(start = date(2008, 1, 1),
                 end = date(2008, 12, 31),
                 function = ci._creimp_2008,
                 ),
        dict(start = date(2009, 1, 1),
                 end = date(2009, 12, 31),
                 function = ci._creimp_2009,
                 ),
        dict(start = date(2010, 1, 1),
                 end = date(2011, 12, 31),
                 function = ci._creimp_2010_2011,
                 ),

        dict(start = date(2012, 1, 1),
                 end = date(2012, 12, 31),
                 function = ci._creimp_2012,
                 ),
        dict(start = date(2013, 1, 1),
                 end = date(2013, 12, 31),
                 function = ci._creimp_2013,
                 ),
        ],
    FloatCol(entity = 'foy'))
build_dated_formula('accult',
 [
  dict(start = date(2002, 1, 1),
       end = date(2012, 12, 31),
       function = ci._accult,
      ),
  dict(start = date(2012, 1, 1),
       end = date(2013, 12, 31),
       function = ri._accult,
      )
 ],
 FloatCol(entity = 'foy'))
build_simple_formula('percvm', FloatCol(function = ci._percvm,
    end = date(2010, 12, 31),
    entity = 'foy',
    start = date(2010, 1, 1),
    ))
build_simple_formula('direpa', FloatCol(function = ci._direpa,
    entity = 'foy'))
build_dated_formula('mecena',
 [
  dict(start = date(2003, 1, 1),
       end = date(2012, 12, 31),
       function = ci._mecena,
      ),
  dict(start = date(2012, 1, 1),
       end = date(2013, 12, 31),
       function = ri._mecena,
      )
 ],
 FloatCol(entity = 'foy'))
build_simple_formula('prlire', FloatCol(function = ci._prlire,
    entity = 'foy',
    label = u"Prélèvement libératoire à restituer (case 2DH)",
    end = date(2013, 12, 31)))
build_dated_formula('aidper',
[
     dict(start = date(2002, 1, 1),
      end = date(2003, 12, 31),
      function = ci._aidper_2002_2003,
     ),
     dict(start = date(2004, 1, 1),
      end = date(2005, 12, 31),
      function = ci._aidper_2004_2005,
     ),
     dict(start = date(2006, 1, 1),
      end = date(2009, 12, 31),
      function = ci._aidper_2006_2009,
     ),
     dict(start = date(2010, 1, 1),
      end = date(2011, 12, 31),
      function = ci._aidper_2010_2011,
     ),
     dict(start = date(2012, 1, 1),
      end = date(2012, 12, 31),
      function = ci._aidper_2012,
     ),
     dict(start = date(2013, 1, 1),
      end = date(2013, 12, 31),
      function = ci._aidper_2013,
     ),
],
FloatCol(entity='foy'))
build_dated_formula('quaenv',
[
     dict(start = date(2005, 1, 1),
      end = date(2005, 12, 31),
      function = ci._quaenv_2005,
     ),
     dict(start = date(2006, 1, 1),
      end = date(2008, 12, 31),
      function = ci._quaenv_2006_2008,
     ),
     dict(start = date(2009, 1, 1),
      end = date(2009, 12, 31),
      function = ci._quaenv_2009,
     ),
     dict(start = date(2010, 1, 1),
      end = date(2011, 12, 31),
      function = ci._quaenv_2010_2011,
     ),
     dict(start = date(2012, 1, 1),
      end = date(2012, 12, 31),
      function = ci._quaenv_2012,
     ),
  dict(start = date(2013, 1, 1),
      end = date(2013, 12, 31),
      function = ci._quaenv_2013,
     ),
],
FloatCol(entity='foy'))
build_simple_formula('quaenv_bouquet', BoolCol(function = ci._quaenv_bouquet,
    entity = 'foy',
    start = date(2013, 1, 1)))
build_simple_formula('drbail', FloatCol(function = ci._drbail,
    entity = 'foy'))
build_simple_formula('ci_garext', FloatCol(function = ci._ci_garext,
    entity = 'foy',
    start = date(2005, 1, 1)))
build_dated_formula('preetu',
    [
        dict(start = date(2005, 1, 1),
          end = date(2005, 12, 31),
          function = ci._preetu_2005,
         ),
        dict(start = date(2006, 1, 1),
          end = date(2007, 12, 31),
          function = ci._preetu_2006_2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2015, 12, 31),
          function = ci._preetu_2008_,
         ),
    ],
    FloatCol(entity='foy'))
build_dated_formula('saldom2',
    [
        dict(start = date(2007, 1, 1),
          end = date(2008, 12, 31),
          function = ci._saldom2_2007_2008,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2013, 12, 31),
          function = ci._saldom2_2009_,
         ),
    ],
    FloatCol(entity='foy'))
build_dated_formula('inthab',
[
     dict(start = date(2007, 1, 1),
      end = date(2007, 12, 31),
      function = ci._inthab_2007,
     ),
     dict(start = date(2008, 1, 1),
      end = date(2008, 12, 31),
      function = ci._inthab_2008,
     ),
     dict(start = date(2009, 1, 1),
      end = date(2009, 12, 31),
      function = ci._inthab_2009,
     ),
     dict(start = date(2010, 1, 1),
      end = date(2010, 12, 31),
      function = ci._inthab_2010,
     ),
     dict(start = date(2011, 1, 1),
      end = date(2011, 12, 31),
      function = ci._inthab_2011,
     ),
     dict(start = date(2012, 1, 1),
      end = date(2013, 12, 31),
      function = ci._inthab_2012_2013,
     ),
],
FloatCol(entity='foy'))
build_simple_formula('assloy', FloatCol(function = ci._assloy,
    entity = 'foy',
    start = date(2005, 1, 1)))
build_simple_formula('autent', FloatCol(function = ci._autent,
    entity = 'foy',
    start = date(2009, 1, 1)))
build_simple_formula('acqgpl', FloatCol(function = ci._acqgpl,
    entity = 'foy',
    start = date(2002, 1, 1),
    end = date(2007, 12, 31)))
build_simple_formula('divide', FloatCol(function = ci._divide,
    entity = 'foy',
    start = date(2005, 1, 1),
    end = date(2009, 12, 31)))
build_simple_formula('aidmob', FloatCol(function = ci._aidmob,
    entity = 'foy',
    start = date(2005, 1, 1),
    end = date(2008, 12, 31)))

build_simple_formula('jeunes', FloatCol(function = ci._jeunes_2005_2008,
    entity = 'foy',
    start = date(2005, 1, 1),
    end = date(2008, 12, 31)))
build_simple_formula('jeunes_ind', FloatCol(function = ci._jeunes_ind,
    entity = 'ind',
    start = date(2005, 1, 1),
    end = date(2008, 12, 31)))
build_dated_formula(
    'credits_impot',  # TODO: Change name to imputations
    [
        dict(start = date(2002, 1, 1),
             end = date(2002, 12, 31),
             function = ci._credits_impot_2002,
             ),
        dict(start = date(2003, 1, 1),
             end = date(2004, 12, 31),
             function = ci._credits_impot_2003_2004,
             ),
        dict(start = date(2005, 1, 1),
             end = date(2006, 12, 31),
             function = ci._credits_impot_2005_2006,
             ),
        dict(start = date(2007, 1, 1),
             end = date(2007, 12, 31),
             function = ci._credits_impot_2007,
             ),
        dict(start = date(2008, 1, 1),
             end = date(2008, 12, 31),
             function = ci._credits_impot_2008,
             ),
        dict(start = date(2009, 1, 1),
             end = date(2009, 12, 31),
             function = ci._credits_impot_2009,
             ),
        dict(start = date(2010, 1, 1),
             end = date(2010, 12, 31),
             function = ci._credits_impot_2010,
             ),
        dict(start = date(2011, 1, 1),
             end = date(2011, 12, 31),
             function = ci._credits_impot_2011,
             ),
        dict(start = date(2012, 1, 1),
             end = date(2012, 12, 31),
             function = ci._credits_impot_2012,
             ),
        dict(start = date(2013, 1, 1),
             end = date(2013, 12, 31),
             function = ci._credits_impot_2013,
             ),
        ],
    FloatCol(entity = 'foy'),
    )

build_simple_formula('irpp', FloatCol(function = ir._irpp,
    entity = 'foy',
    label = u"Impôt sur le revenu des personnes physiques",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_impot_revenu&espId=1&impot=IR&sfid=50",
    ))

build_simple_formula('rfr', FloatCol(function = ir._rfr,
    entity = 'foy',
    label = u"Revenu fiscal de référence",
    ))
build_simple_formula('rfr_rvcm', FloatCol(function = ir._rfr_rvcm,
    entity = 'foy'))

build_simple_formula('glo', FloatCol(function = ir._glo,
    label = u"Gain de levée d'options",
    url = u"http://www.officeo.fr/imposition-au-bareme-progressif-de-l-impot-sur-le-revenu-des-gains-de-levee-d-options-sur-actions-et-attributions-d-actions-gratuites",
    ))
build_simple_formula('rag', FloatCol(function = ir._rag,
    url = u"http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&impot=BA&pageId=prof_ba&sfid=50",
    ))
build_simple_formula('ric', FloatCol(function = ir._ric,
    url = u"http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?pageId=prof_bic&espId=2&impot=BIC&sfid=50",
    ))
build_simple_formula('rac', FloatCol(function = ir._rac,
    url = u"http://vosdroits.service-public.fr/particuliers/F1225.xhtml",
    ))
build_simple_formula('rnc', FloatCol(function = ir._rnc,
    url = u"http://www.impots.gouv.fr/portal/dgi/public/professionnels.impot?espId=2&pageId=prof_bnc&impot=BNC&sfid=50",
    ))
build_simple_formula('rpns', FloatCol(function = ir._rpns))
build_simple_formula('fon', FloatCol(function = ir._fon,
    entity = 'foy',
    url = u"http://impotsurlerevenu.org/definitions/220-revenu-foncier.php",
    ))

build_simple_formula('rpns_mvct', FloatCol(function = ir._rpns_mvct))
build_simple_formula('rpns_pvct', FloatCol(function = ir._rpns_pvct))
build_simple_formula('rpns_mvlt', FloatCol(function = ir._rpns_mvlt))
build_simple_formula('rpns_pvce', FloatCol(function = ir._rpns_pvce))
build_simple_formula('rpns_exon', FloatCol(function = ir._rpns_exon))
build_simple_formula('rpns_i', FloatCol(function = ir._rpns_i))

build_simple_formula('rev_cap_bar', FloatCol(function = ir._rev_cap_bar,
    entity = 'foy',
    url = u"http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital",
    ))
build_dated_formula('rev_cap_lib',
    [
        dict(start = date(2002, 1, 1),
          end = date(2007, 12, 31),
          function = ir._rev_cap_lib__2007,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2015, 12, 31),
          function = ir._rev_cap_lib_2008_,
         ),
    ],
    FloatCol(entity='foy',
    url = u"http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital"))
build_simple_formula('avf', FloatCol(function = ir._avf,
    entity = 'foy'))

###########################################################
# Impôt sur le revenu afférent à la plus-value immobilière
###########################################################

build_simple_formula('ir_pv_immo', FloatCol(function = immo._ir_pv_immo,
                          entity = 'foy',
                          label = u"Impôt sur le revenu afférent à la plus-value immobilière",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/popup?espId=1&typePage=cpr02&docOid=documentstandard_2157",
    ))

############################################################
# Impôt de solidarité sur la fortune
############################################################
build_simple_formula('isf_imm_bati', FloatCol(function = isf._isf_imm_bati,
    entity = 'foy'))
build_simple_formula('isf_imm_non_bati', FloatCol(function = isf._isf_imm_non_bati,
    entity = 'foy'))
build_simple_formula('isf_actions_sal', FloatCol(function = isf._isf_actions_sal,
    entity = 'foy',
    start = date(2006, 1, 1)))
build_simple_formula('isf_droits_sociaux', FloatCol(function = isf._isf_droits_sociaux,
    entity = 'foy'))
build_simple_formula('ass_isf', FloatCol(function = isf._ass_isf,
    entity = 'foy'))
build_dated_formula('isf_iai',
    [
        dict(start = date(2011, 1, 1),
          end = date(2015, 12, 31),
          function = isf._isf_iai_2011_,
         ),
        dict(start = date(2002, 1, 1),
          end = date(2010, 12, 31),
          function = isf._isf_iai__2010,
         ),
    ],
    FloatCol(entity='foy'))
build_simple_formula('tot_impot', FloatCol(function = isf._tot_impot,
    entity = 'foy'))
build_simple_formula('isf_avant_plaf', FloatCol(function = isf._isf_avant_plaf,
    entity = 'foy'))
build_simple_formula('isf_avant_reduction', FloatCol(function = isf._isf_avant_reduction,
    entity = 'foy'))
build_simple_formula('isf_reduc_pac', FloatCol(function = isf._isf_reduc_pac,
    entity = 'foy'))
build_simple_formula('isf_inv_pme', FloatCol(function = isf._isf_inv_pme,
    entity = 'foy',
    start = date(2008, 1, 1)))
build_simple_formula('isf_org_int_gen', FloatCol(function = isf._isf_org_int_gen,
    entity = 'foy'))
build_simple_formula('revetproduits', FloatCol(function = isf._revetproduits,
    entity = 'foy'))
build_dated_formula('isf_apres_plaf',
    [
        dict(start = date(2002, 1, 1),
          end = date(2011, 12, 31),
          function = isf._isf_apres_plaf__2011,
         ),
        dict(start = date(2012, 1, 1),
          end = date(2012, 12, 31),
          function = isf._isf_apres_plaf_2012,
         ),
        dict(start = date(2013, 1, 1),
          end = date(2015, 12, 31),
          function = isf._isf_apres_plaf_2013_,
         ),
    ],
    FloatCol(entity='foy'))
build_simple_formula('decote_isf', FloatCol(function = isf._decote_isf_2013_,
    entity = 'foy',
    start = date(2013, 1, 1)))
build_simple_formula('isf_tot', FloatCol(function = isf._isf_tot,
    entity = 'foy',
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_isf&espId=1&impot=ISF&sfid=50",
    ))

############################################################
#                            Bouclier Fiscal
############################################################

build_simple_formula('rvcm_plus_abat', FloatCol(function = isf._rvcm_plus_abat,
    entity = 'foy'))

# build_simple_formula('maj_cga_i', FloatCol(function = isf._maj_cga_i))
# build_simple_formula('maj_cga', FloatCol(function = isf._maj_cga, entity = 'foy'))

build_simple_formula('bouclier_rev', FloatCol(function = isf._bouclier_rev,
                            entity = 'foy',
                            start = date(2006, 1, 1),
                            end = date(2010, 12, 31)))
build_simple_formula('bouclier_imp_gen', FloatCol(function = isf._bouclier_imp_gen,
                                entity = 'foy',
                                start = date(2006, 1, 1),
                                end = date(2010, 12, 31)))
build_simple_formula('restitutions', FloatCol(function = isf._restitutions,
                            entity = 'foy',
                            start = date(2006, 1, 1),
                            end = date(2010, 12, 31)))
build_simple_formula('bouclier_sumimp', FloatCol(function = isf._bouclier_sumimp,
                               entity = 'foy',
                               start = date(2006, 1, 1),
                               end = date(2010, 12, 31)))
build_simple_formula('bouclier_fiscal', FloatCol(function = isf._bouclier_fiscal,
                               entity = 'foy',
                               start = date(2006, 1, 1),
                               end = date(2010, 12, 31),
                               url = u"http://fr.wikipedia.org/wiki/Bouclier_fiscal",
    ))

# TODO: inclure aussi les dates si nécessaire start = date(2007,1,1)

############################################################
# Prestations familiales
############################################################

build_simple_formula('etu', BoolCol(function = pf._etu,
    label = u"Indicatrice individuelle étudiant",
    ))
build_simple_formula('biact', BoolCol(function = pf._biact,
    entity = 'fam',
    label = u"Indicatrice de biactivité",
    ))
build_simple_formula('concub', BoolCol(function = pf._concub,
    entity = 'fam',
    label = u"Indicatrice de vie en couple",
    ))
build_simple_formula('maries', BoolCol(function = pf._maries,
    entity = 'fam'))
build_simple_formula('nb_par', PeriodSizeIndependentIntCol(function = pf._nb_par,
    entity = 'fam',
    label = u"Nombre de parents",
    ))
#build_simple_formula('smic55', BoolCol(function = pf._smic55,
#    label = u"Indicatrice individuelle d'un salaire supérieur à 55% du smic",
#    ))
build_simple_formula('isol', BoolCol(function = pf._isol,
    entity = 'fam'))

build_simple_formula('div', FloatCol(function = pf._div))
build_simple_formula('rev_coll', FloatCol(function = pf._rev_coll))
build_simple_formula('br_pf_i', FloatCol(function = pf._br_pf_i,
    label = 'Base ressource individuele des prestations familiales'))
build_simple_formula('br_pf', FloatCol(function = pf._br_pf,
    entity = 'fam',
    label = 'Base ressource des prestations familiales'))

#build_simple_formula('af_nbenf', FloatCol(function = af._af_nbenf,
#    entity = 'fam',
#    label = u"Nombre d'enfant au sens des AF",
#    )) TODO: REMOVEME
#build_simple_formula('af_base', FloatCol(function = af._af_base,
#    entity = 'fam',
#    label = 'Allocations familiales - Base'))
#build_simple_formula('af_majo', FloatCol(function = af._af_majo,
#    entity = 'fam',
#    label = 'Allocations familiales - Majoration pour age',
#    url = u"https://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/les-allocations-familiales-af-0",
#    ))
#build_simple_formula('af_forf', FloatCol(function = af._af_forf,
#    entity = 'fam',
#    label = 'Allocations familiales - Forfait 20 ans',
#    url = u"http://www.cleiss.fr/docs/regimes/regime_france4.html",
#    start = date(2003, 7, 1)))
#build_simple_formula('af', FloatCol(function = af._af,
#    entity = 'fam',
#    label = u"Allocations familiales",
#    url = u"https://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/les-allocations-familiales-af-0",
#    ))

build_simple_formula('cf_temp', FloatCol(function = cf._cf,
    entity = 'fam',
    label = u"Complément familial avant d'éventuels cumuls",
    url = u"http://vosdroits.service-public.fr/particuliers/F13214.xhtml",
    ))
build_simple_formula('asf_elig', BoolCol(function = asf._asf_elig,
    entity = 'fam'))
build_simple_formula('asf_nbenf', PeriodSizeIndependentIntCol(function = asf._asf_nbenf,
    entity = 'fam'))
build_simple_formula('asf', FloatCol(function = asf._asf,
    entity = 'fam',
    label = u"Allocation de soutien familial",
    url = u"http://vosdroits.service-public.fr/particuliers/F815.xhtml",
    ))

build_simple_formula('ars', FloatCol(function = ars._ars,
    entity = 'fam',
    label = u"Allocation de rentrée scolaire",
    url = u"http://vosdroits.service-public.fr/particuliers/F1878.xhtml",
    ))


build_simple_formula('paje_base_temp', FloatCol(function = paje._paje_base,
    entity = 'fam',
    label = u"Allocation de base de la PAJE sans tenir compte d'éventuels cumuls",
    start = date(2004, 1, 1)))
build_simple_formula('paje_base', FloatCol(function = paje._paje_cumul,
    entity = 'fam',
    label = u"Allocation de base de la PAJE",
    start = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F2552.xhtml",
    ))

build_simple_formula('paje_nais', FloatCol(function = paje._paje_nais,
    entity = 'fam',
    label = u"Allocation de naissance de la PAJE",
    start = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F2550.xhtml",
    ))
build_simple_formula('paje_clca', FloatCol(function = paje._paje_clca,
    entity = 'fam',
    label = u"PAJE - Complément de libre choix d'activité",
    start = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F313.xhtml",
    ))
build_simple_formula('paje_clca_taux_plein', BoolCol(function = paje._paje_clca_taux_plein,
    entity = 'fam',
    label = u"Indicatrice Clca taux plein",
    start = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F313.xhtml",
    ))
build_simple_formula('paje_clca_taux_partiel', BoolCol(function = paje._paje_clca_taux_partiel,
    entity = 'fam',
    label = u"Indicatrice Clca taux partiel",
    start = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F313.xhtml",
    ))
build_simple_formula('paje_colca', FloatCol(function = paje._paje_colca,
    entity = 'fam',
    label = u"PAJE - Complément optionnel de libre choix d'activité",
    start = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F15110.xhtml",
    ))
build_simple_formula('paje_clmg', FloatCol(function = paje._paje_clmg,
    entity = 'fam',
    label = u"PAJE - Complément de libre choix du mode de garde",
    start = date(2004, 1, 1),
    url = u"http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/le-complement-de-libre-choix-du-mode-de-garde",
    ))
build_simple_formula('paje', FloatCol(function = paje._paje,
    entity = 'fam',
    label = u"PAJE - Ensemble des prestations",
    start = date(2004, 1, 1),
    url = u"http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/petite-enfance/la-prestation-d-accueil-du-jeune-enfant-paje-0",
    ))


build_simple_formula('cf', FloatCol(function = cf._cf_cumul,
    entity = 'fam',
    label = u"Complément familial",
    url = u"http://vosdroits.service-public.fr/particuliers/F13214.xhtml",
    ))
build_dated_formula('aeeh',
    [
        dict(start = date(2002, 1, 1),
          end = date(2002, 12, 31),
          function = aeeh._aeeh__2002,
         ),
        dict(start = date(2003, 1, 1),
          end = date(2015, 12, 31),
          function = aeeh._aeeh_2003_,
         ),
    ],
    FloatCol(entity='fam',
    label = u"Allocation d'éducation de l'enfant handicapé",
    url = u"http://vosdroits.service-public.fr/particuliers/N14808.xhtml"))
build_simple_formula('ape_temp', FloatCol(function = paje._ape,
    entity = 'fam',
    label = u"Allocation parentale d'éducation",
    end = date(2004, 1, 1),
    url = u"http://fr.wikipedia.org/wiki/Allocation_parentale_d'%C3%A9ducation_en_France",
    ))
build_simple_formula('apje_temp', FloatCol(function = paje._apje,
    entity = 'fam',
    label = u"Allocation pour le jeune enfant",
    end = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F2552.xhtml",
    ))
build_simple_formula('ape', FloatCol(function = paje._ape_cumul,
    entity = 'fam',
    label = u"Allocation parentale d'éducation",
    end = date(2004, 1, 1),
    url = u"http://fr.wikipedia.org/wiki/Allocation_parentale_d'%C3%A9ducation_en_France",
    ))
build_simple_formula('apje', FloatCol(function = paje._apje_cumul,
    entity = 'fam',
    label = u"Allocation pour le jeune enfant",
    end = date(2004, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F2552.xhtml",
    ))

build_simple_formula('crds_pfam', FloatCol(function = pf._crds_pfam,
    entity = 'fam',
    label = u"CRDS (prestations familiales)",
    url = u"http://www.cleiss.fr/docs/regimes/regime_francea1.html",
    ))

# En fait en vigueur pour les enfants nés avant 2004 ...
# TODO Gestion du cumul apje ape


############################################################
# RSA/RMI
############################################################

build_simple_formula('div_ms', FloatCol(function = rsa._div_ms))
build_simple_formula('rfon_ms', FloatCol(function = rsa._rfon_ms))
build_simple_formula('enceinte_fam', BoolCol(function = rsa._enceinte_fam, entity = 'fam'))
build_simple_formula('rsa_forfait_asf', FloatCol(function = rsa._rsa_forfait_asf,
    entity = 'fam',
    label = u"Allocation de soutien familial forfaitisée pour le RSA",
    start = date(2014, 4, 1)))
build_dated_formula('br_rmi_pf',
    [
        dict(start = date(2002, 1, 1),
            end = date(2003, 12, 31),
            function = rsa._br_rmi_pf__2003,
         ),
        dict(start = date(2004, 1, 1),
            end = date(2014, 3, 31),
            function = rsa._br_rmi_pf_2004_2014,
         ),
        dict(start = date(2014, 4, 1),
            end = date(2015, 12, 31),
            function = rsa._br_rmi_pf_2014_,
         ),
    ],
    FloatCol(entity = 'fam'))
build_simple_formula('rmi_nbp', FloatCol(function = rsa._rmi_nbp,
    entity = 'fam',
    label = u"Nombre de personne à charge au sens du Rmi/Rsa",
    ))
build_simple_formula('rsa_forfait_logement', FloatCol(function = rsa._rsa_forfait_logement,
    entity = 'fam'))
build_simple_formula('rsa_socle', FloatCol(function = rsa._rsa_socle,
    entity = 'fam',
    label = u"RSA socle",
    ))
build_simple_formula('rmi', FloatCol(function = rsa._rmi,
    entity = 'fam',
    label = u"Revenu de solidarité active - socle",
    ))
build_simple_formula('rsa_socle_majore', FloatCol(function = rsa._rsa_socle_majore,
    entity = 'fam',
    label = u"Majoration pour parent isolé du Revenu de solidarité active socle",
    start = date(2009, 6, 1)))
build_simple_formula('rsa_act', FloatCol(function = rsa._rsa_act,
    entity = 'fam',
    label = u"Revenu de solidarité active - activité",
    start = date(2009, 6, 1)))
build_simple_formula('rsa_act_i', FloatCol(function = rsa._rsa_act_i))
build_simple_formula('psa', FloatCol(function = rsa._psa,
    entity = 'fam',
    label = u"Prime de solidarité active",
    start = date(2009, 1, 1),
    end = date(2009, 12, 31),
    url = u"http://www.service-public.fr/actualites/001077.html",
    ))
build_simple_formula('api', FloatCol(function = rsa._api,
    entity = 'fam',
    end = date(2009, 5, 31),
    label = u"Allocation de parent isolé",
    url = u"http://fr.wikipedia.org/wiki/Allocation_de_parent_isol%C3%A9",
    ))
build_simple_formula('crds_mini', FloatCol(function = rsa._crds_mini,
    entity = 'fam',
    start = date(2009, 6, 1)))
build_dated_formula('aefa',
    [
        dict(start = date(2002, 1, 1),
          end = date(2007, 12, 31),
          function = rsa._aefa__2008_,
         ),
        dict(start = date(2009, 1, 1),
          end = date(2015, 12, 31),#TODO: actualiser la date (si la loi n'a pas changé)
          function = rsa._aefa__2008_,
         ),
        dict(start = date(2008, 1, 1),
          end = date(2008, 12, 31),
          function = rsa._aefa_2008,
         ),
    ],
    FloatCol(entity='fam',
    label = u"Allocation exceptionnelle de fin d'année",
    url = u"http://www.pole-emploi.fr/candidat/aide-exceptionnelle-de-fin-d-annee-dite-prime-de-noel--@/suarticle.jspz?id=70996"))
############################################################
# ASPA/ASI, Minimum vieillesse
############################################################

build_simple_formula('asi_aspa_nb_alloc', FloatCol(function = asi_aspa._asi_aspa_nb_alloc,
    entity = 'fam'))
build_simple_formula('asi_elig', BoolCol(function = asi_aspa._asi_elig,
    label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité",
    ))
build_simple_formula('asi', FloatCol(function = asi_aspa._asi,
    entity = 'fam',
    label = u"Allocation supplémentaire d'invalidité",
    start = date(2007, 1, 1),
    url = u"http://vosdroits.service-public.fr/particuliers/F16940.xhtml",
    ))
    # En 2007, Transformation du MV et de L'ASI en ASPA et ASI. La prestation ASPA calcule bien l'ancien MV
    # mais TODO manque l'ancienne ASI

build_simple_formula('aspa_elig', BoolCol(function = asi_aspa._aspa_elig,
    label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées",
    ))
build_dated_formula('aspa_couple',
    [
        dict(start = date(2002, 1, 1),
          end = date(2006, 12, 31),
          function = asi_aspa._aspa_couple__2006,
         ),
        dict(start = date(2007, 1, 1),
          end = date(2015, 12, 31),
          function = asi_aspa._aspa_couple_2007_,
         ),
    ],
    BoolCol(entity='fam',
    label = u"Couple au sens de l'ASPA"))
build_simple_formula('aspa', FloatCol(function = asi_aspa._aspa,
    entity = 'fam',
    label = u"Allocation de solidarité aux personnes agées",
    url = u"http://vosdroits.service-public.fr/particuliers/F16871.xhtml",
    ))

############################################################
# Allocation adulte handicapé
############################################################

# build_simple_formula('br_aah', FloatCol(function = aah._br_aah,
#     entity = 'fam',
#     label = u"Base ressources de l'allocation adulte handicapé",
#     ))
# build_simple_formula('aah', FloatCol(function = aah._aah,
#     entity = 'fam',
#     label = u"Allocation adulte handicapé",
#     url = u"http://vosdroits.service-public.fr/particuliers/N12230.xhtml",
#     ))
# build_dated_formula('caah',
#     [
#         dict(start = date(2002, 1, 1),
#           end = date(2005, 12, 31),
#           function = aah._caah__2005,
#          ),
#         dict(start = date(2006, 1, 1),
#           end = date(2015, 12, 31), #TODO:actualiser la date (si la loi n'a pas changé)
#           function = aah._caah_2006_,
#          ),
#     ],
#     FloatCol(entity='fam',
#     label = u"Complément de l'allocation adulte handicapé",
#     url = u"http://vosdroits.service-public.fr/particuliers/N12230.xhtml"))
############################################################
# Taxe d'habitation
############################################################

build_simple_formula('exonere_taxe_habitation', BoolCol(function = th._exonere_taxe_habitation,
    default = True,
    entity = 'men',
    label = u"Exonération de la taxe d'habitation",
    url = u"http://vosdroits.service-public.fr/particuliers/F42.xhtml",
    ))
build_simple_formula('tax_hab', FloatCol(function = th._tax_hab,
    entity = 'men',
    label = u"Taxe d'habitation",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?espId=1&pageId=part_taxe_habitation&impot=TH&sfid=50",
    ))

############################################################
# Unité de consommation du ménage
############################################################
build_simple_formula('uc', FloatCol(function = cm._uc,
    entity = 'men',
    label = u"Unités de consommation",
    ))

############################################################
# Catégories
############################################################

build_simple_formula('typ_men', PeriodSizeIndependentIntCol(function = cm._typ_men,
    entity = 'men',
    label = u"Type de ménage",
    ))
build_simple_formula('nbinde', EnumCol(function = cl._nbinde,
                      label = u"Nombre d'individus dans le ménage",
    entity = 'men',
                      enum = Enum([u"Une personne",
                                   u"Deux personnes",
                                   u"Trois personnes",
                                   u"Quatre personnes",
                                   u"Cinq personnes",
                                   u"Six personnes et plus"],
    start = 1)))

build_simple_formula('cplx', BoolCol(function = cl._cplx,
    entity = 'men',
    label = u"Indicatrice de ménage complexe",
    ))

build_simple_formula('act_cpl', PeriodSizeIndependentIntCol(function = cl._act_cpl,
                       entity = 'men',
                       label = u"Nombre d'actifs parmi la personne de référence du méange et son conjoint",
    ))

build_simple_formula('cohab', BoolCol(function = cl._cohab,
                      entity = 'men',
                      label = u"Vie en couple",
    ))

build_simple_formula('act_enf', PeriodSizeIndependentIntCol(function = cl._act_enf,
    entity = 'men',
                       label = u"Nombre d'enfants actifs",
    ))

build_simple_formula(
    'typmen15',
    EnumCol(
        function = cl._typmen15,
        label = u"Type de ménage",
        entity = 'men',
        enum = Enum(
            [
                u"Personne seule active",
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
                u"Autres ménages, tous inactifs"
                ],
            start = 1,
            ),
        ),
    )
############################################################
# Totaux
############################################################

build_simple_formula('revdisp', FloatCol(function = cm._revdisp,
    entity = 'men',
    label = u"Revenu disponible du ménage",
    url = u"http://fr.wikipedia.org/wiki/Revenu_disponible",
    ))
build_simple_formula('nivvie', FloatCol(function = cm._nivvie,
    entity = 'men',
    label = u"Niveau de vie du ménage",
    ))
#
# build_simple_formula('revnet', FloatCol(function = cm._revnet,
#     entity = 'men',
#     label = u"Revenu net du ménage",
#     url = u"http://impotsurlerevenu.org/definitions/115-revenu-net-imposable.php",
#     ))
build_simple_formula('nivvie_net', FloatCol(function = cm._nivvie_net,
    entity = 'men',
    label = u"Niveau de vie net du ménage",
    ))

# build_simple_formula('revini', FloatCol(function = cm._revini,
#     entity = 'men',
#     label = u"Revenu initial du ménage",
#     ))
build_simple_formula('nivvie_ini', FloatCol(function = cm._nivvie_ini,
    entity = 'men',
    label = u"Niveau de vie initial du ménage",
    ))

build_simple_formula('rev_trav', FloatCol(function = cm._rev_trav,
    label = u"Revenus du travail (salariés et non salariés)",
    url = u"http://fr.wikipedia.org/wiki/Revenu_du_travail",
    ))
build_simple_formula('pen', FloatCol(function = cm._pen,
    label = u"Total des pensions et revenus de remplacement",
    url = u"http://fr.wikipedia.org/wiki/Rente",
    ))
build_simple_formula('cotsoc_bar_declarant1', FloatCol(function = cm._cotsoc_bar_declarant1,
    label = u"Cotisations sociales sur les revenus du capital imposés au barème",
    ))
build_simple_formula('cotsoc_lib_declarant1', FloatCol(function = cm._cotsoc_lib_declarant1,
    label = u"Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire",
    ))
build_simple_formula('rev_cap', FloatCol(function = cm._rev_cap,
    label = u"Revenus du patrimoine",
    url = u"http://fr.wikipedia.org/wiki/Revenu#Revenu_du_Capital",
    ))
build_simple_formula('psoc', FloatCol(function = cm._psoc,
    entity = 'fam',
    label = u"Total des prestations sociales",
    url = u"http://fr.wikipedia.org/wiki/Prestation_sociale",
    ))
build_simple_formula('prelsoc_cap', FloatCol(function = cm._prelsoc_cap,
    label = u"Prélèvements sociaux sur les revenus du capital",
    url = u"http://www.impots.gouv.fr/portal/dgi/public/particuliers.impot?pageId=part_ctrb_soc&paf_dm=popup&paf_gm=content&typePage=cpr02&sfid=501&espId=1&impot=CS",
    ))
build_simple_formula('pfam', FloatCol(function = cm._pfam,
    entity = 'fam',
    label = u"Total des prestations familiales",
    url = u"http://www.social-sante.gouv.fr/informations-pratiques,89/fiches-pratiques,91/prestations-familiales,1885/les-prestations-familiales,12626.html",
    ))
build_simple_formula('mini', FloatCol(function = cm._mini,
    entity = 'fam',
    label = u"Minima sociaux",
    url = u"http://fr.wikipedia.org/wiki/Minima_sociaux",
    ))
build_simple_formula('logt', FloatCol(function = cm._logt,
    entity = 'fam',
    label = u"Allocations logements",
    url = u"http://vosdroits.service-public.fr/particuliers/N20360.xhtml" ))
build_simple_formula('impo', FloatCol(function = cm._impo,
    entity = 'men',
    label = u"Impôts sur le revenu",
    url = u"http://fr.wikipedia.org/wiki/Imp%C3%B4t_direct",
    ))
build_simple_formula('crds', FloatCol(function = cm._crds,
    label = u"Total des contributions au remboursement de la dette sociale",
    ))
build_simple_formula('csg', FloatCol(function = cm._csg,
    label = u"Total des contributions sociale généralisée",
    ))
build_simple_formula('cotsoc_noncontrib', FloatCol(function = cm._cotsoc_noncontrib,
    label = u"Cotisations sociales non contributives",
    ))
build_simple_formula('check_csk', FloatCol(function = cm._check_csk,
    entity = 'men'))
build_simple_formula('check_csg', FloatCol(function = cm._check_csg,
    entity = 'men'))
build_simple_formula('check_crds', FloatCol(function = cm._check_crds,
    entity = 'men'))
############################################################
# Couverture Maladie Universelle
############################################################
build_dated_formula('acs_montant',
            [
        dict(
            start = date(2000, 1, 1),
            end = date(2009, 7, 31),
            function = cmu._acs_montant__2009,
        ),
        dict(
            start = date(2009, 8, 1),
            end = date(2014, 12, 31),
            function = cmu._acs_montant_2009_,
        ),
    ],
    FloatCol(label = u"Montant de l'ACS en cas d'éligibilité",
    entity = 'fam',
    ))
build_simple_formula('cmu_forfait_logement_base', FloatCol(function = cmu._cmu_forfait_logement_base,
    label = u"Forfait logement applicable en cas de propriété ou d'occupation à titre gratuit",
    entity = 'fam',
    ))
build_simple_formula('cmu_forfait_logement_al', FloatCol(function = cmu._cmu_forfait_logement_al,
    label = u"Forfait logement applicable en cas d'aide au logement",
    entity = 'fam',
    ))
build_simple_formula('cmu_nbp_foyer', PeriodSizeIndependentIntCol(function = cmu._cmu_nbp_foyer,
    label = u"Nombre de personnes dans le foyer CMU",
    entity = 'fam',
    ))
build_simple_formula('cmu_c_plafond', FloatCol(function = cmu._cmu_c_plafond,
    label = u"Plafond de ressources pour l'éligibilité à la CMU-C",
    entity = 'fam',
    ))
build_simple_formula('cmu_eligible_majoration_dom', BoolCol(function = cmu._cmu_eligible_majoration_dom,
    entity = 'fam'
    ))
build_simple_formula('acs_plafond', FloatCol(function = cmu._acs_plafond,
    label = u"Plafond de ressources pour l'éligibilité à l'ACS",
    entity = 'fam',
    ))
build_simple_formula('cmu_nb_pac', PeriodSizeIndependentIntCol(function = cmu._cmu_nb_pac,
    label = u"Nombre de personnes à charge au titre de la CMU",
    entity = 'fam',
    ))
############################################################
# Allocation Spécifique de Solidarité
############################################################
build_simple_formula('ass', FloatCol(function = ass._ass,
    label = u"Montant de l'Allocation Spécifique de Solidarité",
    entity = 'fam'
    ))
build_simple_formula('ass_elig_i', BoolCol(function = ass._ass_elig_i,
    label = u"Éligibilité individuelle à l'ASS",
    ))
build_simple_formula('chomeur', BoolCol(function = ass._chomeur,
    label = u"Montant de l'Allocation Spécifique de Solidarité",
    ))
