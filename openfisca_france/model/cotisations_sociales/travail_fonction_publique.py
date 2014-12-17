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


import math
from numpy import maximum as max_, minimum as min_, zeros


from ..base import *  # noqa
from . import apply_bareme_for_relevant_type_sal


@reference_formula
class allocations_temporaires_invalidite(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations temporaires d'invalidité (ATI, fonction publique et collectivités locales)"
    # patronale, non-contributive

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        eligibles = (
            (type_sal == CAT['public_titulaire_etat']) +
            (type_sal == CAT['public_titulaire_hospitaliere']) +
            (type_sal == CAT['public_non_titulaire'])
            ) > 0  # TODO check
        base = salbrut + (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
        base = eligibles * base
        cotisation_etat = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "ati",
            base = salbrut,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        cotisation_collectivites_locales = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "atiacl",
            base = salbrut,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation_etat + cotisation_collectivites_locales
        return output_period.start.offset('first-of', 'month').period('month')


@reference_formula
class contribution_exceptionnelle_solidarite_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation exceptionnelle de solidarité (employe)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        rafp_employe = simulation.calculate('rafp_employe', period)
        pension_civile_employe = simulation.calculate('pension_civile_employe', period)
        cotisations_salariales_contributives = simulation.calculate('cotisations_salariales_contributives', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        seuil_assuj_fds = seuil_fds(_P)

        assujettis = (
            (type_sal == CAT['public_titulaire_etat']) +
            (type_sal == CAT['public_titulaire_territoriale']) +
            (type_sal == CAT['public_titulaire_hospitaliere']) +
            (type_sal == CAT['public_non_titulaire'])
            ) * (
            (salbrut - hsup) > seuil_assuj_fds
            )

        # TODO: check assiette voir IPP
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "excep_solidarite",
            base = assujettis * min_(
                (
                    salbrut - hsup + indemnite_residence + rafp_employe + pension_civile_employe
                    + primes_fonction_publique
                    + (type_sal == CAT['public_non_titulaire']) * cotisations_salariales_contributives
                    ),
                _P.cotsoc.sal.fonc.commun.plafond_base_solidarite,
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class fonds_emploi_hospitalier(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Fonds pour l'emploi hospitalier (employeur)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "feh",
            base = (
                salbrut + indemnite_residence # TODO check base
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class ircantec_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Ircantec employé"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        hsup = simulation.calculate('hsup', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        _P = simulation.legislation_at(period.start)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie.__dict__,
            bareme_name = "ircantec",
            base = (
                salbrut - hsup + indemnite_residence + primes_fonction_publique
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, ircantec


@reference_formula
class gipa(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de garantie individuelle du pouvoir d'achat"

    def function(self, simulation, period):
        period = period.start.period(u'year').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        return period, zeros(len(type_sal))


@reference_formula
class ircantec_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Ircantec employeur"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        hsup = simulation.calculate('hsup', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        _P = simulation.legislation_at(period.start)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur.__dict__,
            bareme_name = "ircantec",
            base = (
                salbrut - hsup + indemnite_residence + primes_fonction_publique
                ),
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, ircantec


@reference_formula
class indemnite_residence(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indemnité de résidence des fonctionnaires"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        zone_apl_individu = simulation.calculate('zone_apl_individu', period)
        _P = simulation.legislation_at(period.start)

        zone_apl = zone_apl_individu
        P = _P.fonc.indem_resid
        min_zone_1, min_zone_2, min_zone_3 = P.min * P.taux.zone1, P.min * P.taux.zone2, P.min * P.taux.zone3
        taux = P.taux.zone1 * (zone_apl == 1) + P.taux.zone2 * (zone_apl == 2) + P.taux.zone3 * (zone_apl == 3)
        plancher = min_zone_1 * (zone_apl == 1) + min_zone_2 * (zone_apl == 2) + min_zone_3 * (zone_apl == 3)
        return period, max_(plancher, taux * salbrut) * (type_sal >= 2)


@reference_formula
class indice_majore(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Indice majoré"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        salbrut = simulation.calculate('salbrut', period)
        _P = simulation.legislation_at(period.start)

        traitement_annuel_brut = _P.fonc.IM_100
        return period, (salbrut * 100 * 12 / traitement_annuel_brut) * (type_sal >= 2)


@reference_formula
class pension_civile_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pension civile employé"
    url = u"http://www.ac-besancon.fr/spip.php?article2662",

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        sal = _P.cotsoc.cotisations_salarie.__dict__
        terr_or_hosp = (
            type_sal == CAT['public_titulaire_territoriale']) | (type_sal == CAT['public_titulaire_hospitaliere'])
        pension_civile_employe = (
            (type_sal == CAT['public_titulaire_etat']) * sal['public_titulaire_etat']['pension'].calc(salbrut)
            + terr_or_hosp * sal['public_titulaire_territoriale']['cnracl1'].calc(salbrut)
            )
        return period, -pension_civile_employe


@reference_formula
class pension_civile_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation patronale pension civile"
    url = u"http://www.ac-besancon.fr/spip.php?article2662"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        _P = simulation.legislation_at(period.start)

        pat = _P.cotsoc.cotisations_employeur.__dict__
        terr_or_hosp = (
            (type_sal == CAT['public_titulaire_territoriale']) |
            (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        cot_pat_pension_civile = (
            (type_sal == CAT['public_titulaire_etat']) * pat['public_titulaire_etat']['pension'].calc(salbrut)
            + terr_or_hosp * pat['public_titulaire_territoriale']['cnracl'].calc(salbrut)
            )
        return period, -cot_pat_pension_civile


@reference_formula
class primes_fonction_publique(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Calcul des primes pour les fonctionnaries"
    url = u"http://vosdroits.service-public.fr/particuliers/F465.xhtml"

#   Note: sal_brut est égal au traitement indiciaire brut

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        salbrut = simulation.calculate('salbrut', period)

        public = (
            (type_sal == CAT['public_titulaire_etat'])
            + (type_sal == CAT['public_titulaire_territoriale'])
            + (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        tib = salbrut * public
        return period, TAUX_DE_PRIME * tib


@reference_formula
class rafp_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part salariale de la retraite additionelle de la fonction publique"
#    Part salariale de la retraite additionelle de la fonction publique
#    TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
#    Note: sal_brut est le traitement indiciaire brut pour les fonctionnaires

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        _P = simulation.legislation_at(period.start)

        eligibles = ((type_sal == CAT['public_titulaire_etat'])
                     + (type_sal == CAT['public_titulaire_territoriale'])
                     + (type_sal == CAT['public_titulaire_hospitaliere']))
        tib = salbrut * eligibles

        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * tib)
        # Même régime pour etat et colloc
        rafp_employe = eligibles * _P.cotsoc.cotisations_salarie.public_titulaire_etat['rafp'].calc(assiette)
        return period, -rafp_employe


@reference_formula
class rafp_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part patronale de la retraite additionnelle de la fonction publique"

    # TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
    # Note: salbrut est le traitement indiciaire brut pour les fonctionnaires
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        salbrut = simulation.calculate('salbrut', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        _P = simulation.legislation_at(period.start)

        eligibles = ((type_sal == CAT['public_titulaire_etat'])
                     + (type_sal == CAT['public_titulaire_territoriale'])
                     + (type_sal == CAT['public_titulaire_hospitaliere']))
        tib = salbrut * eligibles
        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * tib)
        bareme_rafp = _P.cotsoc.cotisations_employeur.public_titulaire_etat['rafp']
        rafp_employeur = eligibles * bareme_rafp.calc(assiette)
        return period, - rafp_employeur
        return output_period.start.offset('first-of', 'month').period('month')


@reference_formula
class supp_familial_traitement(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Supplément familial de traitement"
    # Attention : par hypothèse ne peut êre attribué qu'à la tête du ménage
    # TODO: gérer le cas encore problématique du conjoint fonctionnaire

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        salbrut = simulation.calculate('salbrut', period)
        af_nbenf_holder = simulation.compute('af_nbenf', period)
        _P = simulation.legislation_at(period.start)

        fonc_nbenf = self.cast_from_entity_to_role(af_nbenf_holder, role = CHEF)
        P = _P.fonc.supp_fam
        part_fixe_1 = P.fixe.enf1
        part_fixe_2 = P.fixe.enf2
        part_fixe_supp = P.fixe.enfsupp
        part_fixe = (
            part_fixe_1 * (fonc_nbenf == 1) + part_fixe_2 * (fonc_nbenf == 2)
            + part_fixe_supp * max_(0, fonc_nbenf - 2)
            )
        # pct_variable_1 = 0
        pct_variable_2 = P.prop.enf2
        pct_variable_3 = P.prop.enf3
        pct_variable_supp = P.prop.enfsupp
        pct_variable = (
            pct_variable_2 * (fonc_nbenf == 2) + (pct_variable_3) * (fonc_nbenf == 3)
            + pct_variable_supp * max_(0, fonc_nbenf - 3))

        indice_maj_min = P.IM_min
        indice_maj_max = P.IM_max

        traitement_brut_mensuel_min = _traitement_brut_mensuel(indice_maj_min, _P)
        plancher_mensuel_1 = part_fixe
        plancher_mensuel_2 = part_fixe + traitement_brut_mensuel_min * pct_variable_2
        plancher_mensuel_3 = part_fixe + traitement_brut_mensuel_min * pct_variable_3
        plancher_mensuel_supp = traitement_brut_mensuel_min * pct_variable_supp

        plancher = (plancher_mensuel_1 * (fonc_nbenf == 1) +
                    plancher_mensuel_2 * (fonc_nbenf == 2) +
                    plancher_mensuel_3 * (fonc_nbenf >= 3) +
                    plancher_mensuel_supp * max_(0, fonc_nbenf - 3))

        traitement_brut_mensuel_max = _traitement_brut_mensuel(indice_maj_max, _P)
        plafond_mensuel_1 = part_fixe
        plafond_mensuel_2 = part_fixe + traitement_brut_mensuel_max * pct_variable_2
        plafond_mensuel_3 = part_fixe + traitement_brut_mensuel_max * pct_variable_3
        plafond_mensuel_supp = traitement_brut_mensuel_max * pct_variable_supp

        plafond = (plafond_mensuel_1 * (fonc_nbenf == 1) + plafond_mensuel_2 * (fonc_nbenf == 2) +
                   plafond_mensuel_3 * (fonc_nbenf == 3) +
                   plafond_mensuel_supp * max_(0, fonc_nbenf - 3))

        sft = min_(max_(part_fixe + pct_variable * salbrut, plancher), plafond) * (type_sal >= 2)
        # Nota Bene:
        # type_sal is an EnumCol which enum is:
        # CAT = Enum(['prive_non_cadre',
        #             'prive_cadre',
        #             'public_titulaire_etat',
        #             'public_titulaire_militaire',
        #             'public_titulaire_territoriale',
        #             'public_titulaire_hospitaliere',
        #             'public_non_titulaire'])
        return period, sft


def seuil_fds(_P):
    '''
    Calcul du seuil mensuel d'assujetissement à la contribution au fond de solidarité
    '''
    ind_maj_ref = _P.cotsoc.sal.fonc.commun.ind_maj_ref
    pt_ind_mensuel = _P.cotsoc.sal.fonc.commun.pt_ind / 12
    seuil_mensuel = math.floor((pt_ind_mensuel * ind_maj_ref))
    return seuil_mensuel


def _traitement_brut_mensuel(indice_maj, _P):
        Indice_majore_100_annuel = _P.fonc.IM_100
        traitement_brut = Indice_majore_100_annuel * indice_maj / 100 / 12
        return traitement_brut
