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


from __future__ import division

import math

from numpy import minimum as min_

from ....base import *  # noqa analysis:ignore
from .base import apply_bareme_for_relevant_type_sal


@reference_formula
class allocations_temporaires_invalidite(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations temporaires d'invalidité (ATI, fonction publique et collectivités locales)"
    # patronale, non-contributive

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        assiette_cotisations_sociales_public = simulation.calculate('assiette_cotisations_sociales_public', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        base = assiette_cotisations_sociales_public
        cotisation_etat = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "ati",
            base = base,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        cotisation_collectivites_locales = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "atiacl",
            base = base,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation_etat + cotisation_collectivites_locales


@reference_formula
class assiette_cotisations_sociales_public(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des agents titulaires de la fonction publique"
    # TODO: gestion des heures supplémentaires

    def function(self, simulation, period):
        remuneration_principale = simulation.calculate('remuneration_principale', period)
        # primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        # indemnite_residence = simulation.calculate('indemnite_residence', period)
        type_sal = simulation.calculate('type_sal', period)
        public = (type_sal >= 2)
        # titulaire = (type_sal >= 2) * (type_sal <= 5)
        assiette = public * (
            remuneration_principale
            # + not_(titulaire) * (indemnite_residence + primes_fonction_publique)
            )
        return period, assiette


# sft dans assiette csg et RAFP et Cotisation exceptionnelle de solidarité et taxe sur les salaires
# primes dont indemnites de residences idem sft
# avantages en nature contrib exceptionnelle de solidarite, RAFP, CSG, CRDS.


@reference_formula
class contribution_exceptionnelle_solidarite(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation exceptionnelle au fonds de solidarité (salarié)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        hsup = simulation.calculate('hsup', period)
        type_sal = simulation.calculate('type_sal', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        rafp_salarie = simulation.calculate('rafp_salarie', period)
        pension_civile_salarie = simulation.calculate('pension_civile_salarie', period)
        cotisations_salariales_contributives = simulation.calculate('cotisations_salariales_contributives', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)

        _P = simulation.legislation_at(period.start)

        seuil_assuj_fds = seuil_fds(_P)

        assujettis = (
            (type_sal == CAT['public_titulaire_etat']) +
            (type_sal == CAT['public_titulaire_territoriale']) +
            (type_sal == CAT['public_titulaire_hospitaliere']) +
            (type_sal == CAT['public_non_titulaire'])
            ) * (
            (traitement_indiciaire_brut + salaire_de_base - hsup) > seuil_assuj_fds
            )

        # TODO: check assiette voir IPP
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie,
            bareme_name = "excep_solidarite",
            base = assujettis * min_(
                (
                    traitement_indiciaire_brut + salaire_de_base - hsup + indemnite_residence + rafp_salarie +
                    pension_civile_salarie +
                    primes_fonction_publique +
                    (type_sal == CAT['public_non_titulaire']) * cotisations_salariales_contributives
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

        assiette_cotisations_sociales_public = simulation.calculate('assiette_cotisations_sociales_public', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)
        cotisation = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "feh",
            base = assiette_cotisations_sociales_public,  # TODO: check base
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation


@reference_formula
class ircantec_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Ircantec salarié"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_salarie,
            bareme_name = "ircantec",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, ircantec


@reference_formula
class ircantec_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Ircantec employeur"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        ircantec = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = _P.cotsoc.cotisations_employeur,
            bareme_name = "ircantec",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, ircantec


@reference_formula
class pension_civile_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Pension civile salarié"
    url = u"http://www.ac-besancon.fr/spip.php?article2662",

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)  # TODO: check nbi
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        sal =  _P.cotsoc.cotisations_salarie
        terr_or_hosp = (
            type_sal == CAT['public_titulaire_territoriale']) | (type_sal == CAT['public_titulaire_hospitaliere'])
        pension_civile_salarie = (
            (type_sal == CAT['public_titulaire_etat']) *
            sal['public_titulaire_etat']['pension'].calc(traitement_indiciaire_brut) +
            terr_or_hosp * sal['public_titulaire_territoriale']['cnracl1'].calc(traitement_indiciaire_brut)
            )
        return period, -pension_civile_salarie


@reference_formula
class pension_civile_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation patronale pension civile"
    url = u"http://www.ac-besancon.fr/spip.php?article2662"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        assiette_cotisations_sociales_public = simulation.calculate('assiette_cotisations_sociales_public', period)
        # plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        type_sal = simulation.calculate('type_sal', period)
        _P = simulation.legislation_at(period.start)

        pat = _P.cotsoc.cotisations_employeur
        terr_or_hosp = (
            (type_sal == CAT['public_titulaire_territoriale']) | (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        cot_pat_pension_civile = (
            (type_sal == CAT['public_titulaire_etat']) * pat['public_titulaire_etat']['pension'].calc(
                assiette_cotisations_sociales_public) +
            terr_or_hosp * pat['public_titulaire_territoriale']['cnracl'].calc(assiette_cotisations_sociales_public)
            )
        return period, -cot_pat_pension_civile


@reference_formula
class rafp_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part salariale de la retraite additionelle de la fonction publique"
    # Part salariale de la retraite additionelle de la fonction publique
    # TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        _P = simulation.legislation_at(period.start)

        eligible = ((type_sal == CAT['public_titulaire_etat'])
                     + (type_sal == CAT['public_titulaire_territoriale'])
                     + (type_sal == CAT['public_titulaire_hospitaliere']))

        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * traitement_indiciaire_brut * eligible)
        # Même régime pour les fonctions publiques d'Etat et des collectivité locales
        rafp_salarie = eligible * _P.cotsoc.cotisations_salarie.public_titulaire_etat['rafp'].calc(assiette)
        return period, -rafp_salarie


@reference_formula
class rafp_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Part patronale de la retraite additionnelle de la fonction publique"

    # TODO: ajouter la gipa qui n'est pas affectée par le plafond d'assiette
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        traitement_indiciaire_brut = simulation.calculate('traitement_indiciaire_brut', period)
        type_sal = simulation.calculate('type_sal', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        supp_familial_traitement = simulation.calculate('supp_familial_traitement', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        _P = simulation.legislation_at(period.start)

        eligible = (
            (type_sal == CAT['public_titulaire_etat']) +
            (type_sal == CAT['public_titulaire_territoriale']) +
            (type_sal == CAT['public_titulaire_hospitaliere'])
            )
        plaf_ass = _P.cotsoc.sal.fonc.etat.rafp_plaf_assiette
        base_imposable = primes_fonction_publique + supp_familial_traitement + indemnite_residence
        assiette = min_(base_imposable, plaf_ass * traitement_indiciaire_brut * eligible)
        bareme_rafp = _P.cotsoc.cotisations_employeur.public_titulaire_etat['rafp']
        rafp_employeur = eligible * bareme_rafp.calc(assiette)
        return period, - rafp_employeur


def seuil_fds(law):
    '''
    Calcul du seuil mensuel d'assujetissement à la contribution au fond de solidarité
    '''
    ind_maj_ref = law.cotsoc.sal.fonc.commun.ind_maj_ref
    pt_ind_mensuel = law.cotsoc.sal.fonc.commun.pt_ind / 12
    seuil_mensuel = math.floor((pt_ind_mensuel * ind_maj_ref))
    return seuil_mensuel
