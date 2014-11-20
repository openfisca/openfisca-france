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

from numpy import logical_not as not_, zeros
from openfisca_core.columns import FloatCol
from openfisca_core.formulas import SimpleFormulaColumn

from ..base import CAT, Individus, QUIFAM, QUIFOY, QUIMEN, reference_formula


CHEF = QUIFAM['chef']
DEBUG_SAL_TYPE = 'public_titulaire_hospitaliere'
log = logging.getLogger(__name__)
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


taux_versement_transport_by_localisation_entreprise = None


@reference_formula
class cotpat_contrib2(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales contributives"

    def function(self, agff_tranche_a_employeur, ags, arrco_tranche_a_employeur, assedic_employeur,
                 pension_civile_employeur, rafp_employeur, vieillesse_deplafonnee_employeur,
                 vieillesse_plafonnee_employeur):
        cotpat = (
            agff_tranche_a_employeur +
            ags +
            arrco_tranche_a_employeur +
            assedic_employeur +
            vieillesse_plafonnee_employeur +
            vieillesse_deplafonnee_employeur +
            rafp_employeur + pension_civile_employeur
            )


        return cotpat

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat_main_d_oeuvre2(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales main d'oeuvre"

    # TODO: A discriminer selon la taille de l'entreprise
    # Il s'agit de prélèvements sur les salaires que la CN ne classe pas dans les cotisations sociales
    #  En particulier, la CN classe:
    #     - D291: taxe sur les salaire, versement transport, FNAL, CSA, taxe d'apprentissage, formation continue
    #     - D993: participation à l'effort de construction

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cotpat_transport, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotpat = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])  # category[1] is the numerical index
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_mo = (bar.option == "main-d-oeuvre")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                                 indemnite_residence + primes_fonction_publique))
                             * is_mo)
                    cotpat += temp
        return cotpat + cotpat_transport

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat_noncontrib2(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation sociales patronales non contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cotpat_accident, _P):
        pat = _P.cotsoc.cotisations_employeur.__dict__
        cotpat = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in pat.keys():
                for bar in pat[category[0]].itervalues():
                    is_noncontrib = (bar.option == "noncontrib")
                    temp = -(iscat
                             * bar.calc(salbrut + (category[0] == 'public_non_titulaire') * (
                                 indemnite_residence + primes_fonction_publique))
                             * is_noncontrib)
                    cotpat += temp
        return cotpat + cotpat_accident

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotpat2(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"

    def function(self, cotpat_contrib, cotpat_noncontrib, cotpat_main_d_oeuvre):
        return cotpat_contrib + cotpat_noncontrib + cotpat_main_d_oeuvre

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


def seuil_fds(_P):
    from math import floor
    ind_maj_ref = _P.cotsoc.sal.fonc.commun.ind_maj_ref
    pt_ind = _P.cotsoc.sal.fonc.commun.pt_ind
    seuil_mensuel = floor((pt_ind * ind_maj_ref) / 12)
    return seuil_mensuel


@reference_formula
class cotsal_contrib2(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cot_sal_rafp,
                 pension_civile_employe, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        cotsal = zeros(len(salbrut))
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_contrib = (bar.option == "contrib") & (
                        bar.name not in ["rafp", "pension", "cnracl1", "cnracl2"])  # dealed by pension civile and rafp
                    temp = -(iscat * bar.calc(
                        salbrut - hsup + (category[0] == 'public_non_titulaire') * (
                            indemnite_residence + primes_fonction_publique
                            )
                        )
                    ) * is_contrib
                    cotsal += temp
        public_titulaire = (
            (type_sal == CAT['public_titulaire_etat'])
            + (type_sal == CAT['public_titulaire_territoriale'])
            + (type_sal == CAT['public_titulaire_hospitaliere']))

        return cotsal + (pension_civile_employe + cot_sal_rafp) * public_titulaire

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotsal_noncontrib2(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales non-contributives"

    def function(self, salbrut, hsup, type_sal, primes_fonction_publique, indemnite_residence, cot_sal_rafp,
                 pension_civile_employe, cotsal_contrib, _P):
        sal = _P.cotsoc.cotisations_salarie.__dict__
        cotsal = zeros(len(salbrut))
        seuil_assuj_fds = seuil_fds(_P)
    #    log.info("seuil assujetissement FDS %i", seuil_assuj_fds)
        for category in CAT:
            iscat = (type_sal == category[1])
            if category[0] in sal:
                for bar in sal[category[0]].itervalues():
                    is_exempt_fds = (category[0] in ['public_titulaire_etat', 'public_titulaire_territoriale', 'public_titulaire_hospitaliere']) * (bar.name == 'solidarite') * ((salbrut - hsup) / 12 <= seuil_assuj_fds)  # TODO: check assiette voir IPP
                    is_noncontrib = (bar.option == "noncontrib")  # and (bar.name in ["famille", "maladie"])
                    temp = -(iscat * bar.calc(
                        salbrut + primes_fonction_publique + indemnite_residence -
                        hsup + cot_sal_rafp + pension_civile_employe +
                        cotsal_contrib * (
                            category[0] == 'public_non_titulaire'
                            ) * (bar.name == "excep_solidarite")
                        )  # * (category[0] == 'public_non_titulaire')
                        * is_noncontrib * not_(is_exempt_fds)
                        )
                    cotsal += temp
        return cotsal

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class cotsal2(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales"

    def function(self, cotsal_contrib, cotsal_noncontrib):
        return cotsal_contrib + cotsal_noncontrib

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')
