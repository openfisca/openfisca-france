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


from __future__ import division

import logging

from numpy import minimum as min_
from openfisca_core.accessors import law
from openfisca_core.enumerations import Enum
from openfisca_core.taxscales import TaxScalesTree, scale_tax_scales

from ..base import FloatCol, Individus, QUIFAM, QUIFOY, QUIMEN, reference_formula, SimpleFormulaColumn


TAUX_DE_PRIME = 1 / 4  # primes_fonction_publique (hors supplément familial et indemnité de résidence) / rémunération brute


CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])
CHEF = QUIFAM['chef']
DEBUG_SAL_TYPE = 'public_titulaire_hospitaliere'
log = logging.getLogger(__name__)
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


@reference_formula
class cot_pat_pension_civile(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation patronale pension civile"
    url = u"http://www.ac-besancon.fr/spip.php?article2662"

    def function(self, salbrut, type_sal, _P):
        """
        Pension civile part patronale
        Note : salbrut est égal au traitement indiciaire brut
        """
        pat = _P.cotsoc.cotisations_employeur.__dict__
        terr_or_hosp = (
            (type_sal == CAT['public_titulaire_territoriale']) |
            (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        cot_pat_pension_civile = (
            (type_sal == CAT['public_titulaire_etat']) * pat['public_titulaire_etat']['pension'].calc(salbrut)
            + terr_or_hosp * pat['public_titulaire_territoriale']['cnracl'].calc(salbrut)
            )
        return -cot_pat_pension_civile

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cot_pat_rafp(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part patronale de la retraite additionelle de la fonction publique"
    url = u"http://www.rafp.fr/Cotisations-et-autres-types-dabondement-CET-fr-ru99/Les-cotisations-ar223",

#    TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
#    Note: salbrut est le traitement indiciaire brut pour les fonctionnaires

    def function(self, salbrut, type_sal, primes_fonction_publique, supp_familial_traitement, indemnite_residence, _P):
        eligibles = ((type_sal == CAT['public_titulaire_etat'])
                     + (type_sal == CAT['public_titulaire_territoriale'])
                     + (type_sal == CAT['public_titulaire_hospitaliere']))
        tib = salbrut * eligibles / 12
        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        plaf_ss = _P.cotsoc.gen.plaf_ss  # TODO: build somewhere else
        pat = scale_tax_scales(TaxScalesTree('pat', _P.cotsoc.pat), plaf_ss)
        assiette = min_(base_imposable / 12, plaf_ass * tib)

        bareme_rafp = _P.cotsoc.cotisations_employeur.public_titulaire_etat['rafp']
        cot_pat_rafp = eligibles * bareme_rafp.calc(assiette)
        return -12 * cot_pat_rafp

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cot_sal_pension_civile(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part patronale de la retraite additionelle de la fonction publique"
    url = u"http://www.ac-besancon.fr/spip.php?article2662",

    def function(self, salbrut, type_sal, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        terr_or_hosp = (
            (type_sal == CAT['public_titulaire_territoriale']) |
            (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        cot_sal_pension_civile = (
            (type_sal == CAT['public_titulaire_etat']) * sal['public_titulaire_etat']['pension'].calc(salbrut) +
            terr_or_hosp * sal['public_titulaire_territoriale']['cnracl1'].calc(salbrut)
            )
    #    if array(type_sal == DEBUG_SAL_TYPE).all():
    #        log.info('cot_sal_pension_civile %s', cot_sal_pension_civile / 12)

        return -cot_sal_pension_civile

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')
