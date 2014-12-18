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

import csv
import json
import pkg_resources

from numpy import ceil, fromiter, int16, logical_not as not_, maximum as max_, minimum as min_, round

import openfisca_france
from .base import *
from .pfam import nb_enf


zone_apl_by_depcom = None


@reference_formula
class al_pac(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Nombre de personne à charge au sens des allocations logement"

    def function(self, age_holder, smic55_holder, nbR_holder,
                 af = law.fam.af, cf = law.fam.cf, D_enfch = law.al.autres.D_enfch):
        '''
        site de la CAF en 2011:

        # Enfant à charge
        Vous assurez financièrement l'entretien et asez la responsabilité
        affective et éducative d'un enfant, que vous ayez ou non un lien de
        parenté avec lui. Il est reconnu à votre charge pour le versement
        des aides au logement jusqu'au mois précédent ses 21 ans.
        Attention, s'il travaille, il doit gagner moins de 836,55 € par mois.

        # Parents âgés ou infirmes
        Sont à votre charge s'ils vivent avec vous et si leurs revenus 2009
        ne dépassent pas 10 386,59 € :
        * vos parents ou grand-parents âgés de plus de 65 ans ou d'au moins
        60 ans, inaptes au travail, anciens déportés,
        * vos proches parents infirmes âgés de 22 ans ou plus (parents,
        grand-parents, enfants, petits enfants, frères, soeurs, oncles,
        tantes, neveux, nièces).
        '''
        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        # P_AL.D_enfch est une dummy qui vaut 1 si les enfants sont comptés à
        # charge (cas actuel) et zéro sinon.
        nbR = self.cast_from_entity_to_role(nbR_holder, role = VOUS)
        al_nbinv = self.sum_by_entity(nbR)

        age1 = af.age1
        age2 = cf.age2
        al_nbenf = nb_enf(age, smic55, age1, age2)
        al_pac = D_enfch * (al_nbenf + al_nbinv)  #  TODO: manque invalides
        # TODO: il faudrait probablement définir les aides au logement pour un ménage et non
        # pour une famille
        return al_pac

    def get_variable_period(self, output_period, variable_name):
        if variable_name == 'nbR_holder':
            return output_period.start.offset('first-of', 'year').period('year')
        else:
            return output_period

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class br_al(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Base ressource des allocations logement"

    def function(self, etu_holder, boursier_holder, br_pf_i_holder, rev_coll_holder, biact, Pr = law.al.ressources):
        # On ne considère que les revenus des 2 conjoints et les revenus non
        # individualisables
        #   0 - non étudiant
        #   1 - étudiant non boursier
        #   2 - éutidant boursier
        # revCatvous et self.conj : somme des revenus catégoriel après abatement
        # revColl : autres revenus du ménage non individualisable
        # ALabat : abatement prix en compte pour le calcul de la base ressources
        # des allocattions logement
        # plancher de ressources pour les etudiants
        boursier = self.split_by_roles(boursier_holder, roles = [CHEF, PART])
        br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])
        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        rev_coll = self.sum_by_entity(rev_coll_holder)
        etuC = (etu[CHEF]) & (not_(etu[PART]))
        etuP = not_(etu[CHEF]) & (etu[PART])
        etuCP = (etu[CHEF]) & (etu[PART])
        # Boursiers
        # TODO: distinguer boursier foyer/boursier locatif
        etuCB = etu[CHEF] & boursier[CHEF]
        etuPB = etu[PART] & boursier[PART]
        # self.etu = (self.etu[CHEF]>=1)|(self.etuP>=1)
        revCatVous = max_(br_pf_i[CHEF], etuC * (Pr.dar_4 - (etuCB) * Pr.dar_5))
        revCatConj = max_(br_pf_i[PART], etuP * (Pr.dar_4 - (etuPB) * Pr.dar_5))
        revCatVsCj = (
            not_(etuCP) * (revCatVous + revCatConj) +
            etuCP * max_(br_pf_i[CHEF] + br_pf_i[PART], Pr.dar_4 - (etuCB | etuPB) * Pr.dar_5 + Pr.dar_7)
            )

        # TODO: ajouter les paramètres pour les étudiants en foyer (boursier et non boursier),
        # les inclure dans le calcul somme des revenus catégoriels après abatement
        revCat = revCatVsCj + rev_coll

        # TODO: charges déductibles : pension alimentaires et abatements spéciaux
        revNet = revCat

        # On ne considère pas l'abattement sur les ressources de certaines
        # personnes (enfant, ascendants ou grands infirmes).

        # abattement forfaitaire double activité
        abatDoubleAct = biact * Pr.dar_1

        # TODO: neutralisation des ressources
        # ...

        # TODO: abbattement sur les ressources
        # ...

        # TODO: évaluation forfaitaire des ressources (première demande)

        # TODO :double résidence pour raisons professionnelles

        # Base ressource des aides au logement (arrondies aux 100 euros supérieurs)

        br_al = ceil(max_(revNet - abatDoubleAct, 0) / 100) * 100

        return br_al

    def get_variable_period(self, output_period, variable_name):
        if variable_name in ['br_pf_i_holder', 'rev_coll_holder']:
            return output_period.start.offset('first-of', 'year').period('year').offset(-2)
        else:
            return output_period

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class aide_logement_montant(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Formule des aides aux logements en secteur locatif"

    def function(self, concub, br_al, so_holder, loyer_holder, coloc_holder, isol, al_pac, zone_apl_famille,
                 nat_imp_holder,
                 al = law.al,
                 fam = law.fam):
        # variable ménage à redistribuer
        so = self.cast_from_entity_to_roles(so_holder)
        so = self.filter_role(so, role = CHEF)
        loyer = self.cast_from_entity_to_roles(loyer_holder)
        loyer = self.filter_role(loyer, role = CHEF)

        zone_apl = zone_apl_famille
        # Variables individuelles
        coloc = self.any_by_roles(coloc_holder)
        # Variables du foyer fiscal
        nat_imp = self.cast_from_entity_to_roles(nat_imp_holder)
        nat_imp = self.any_by_roles(nat_imp)

        # ne prend pas en compte les chambres ni les logements-foyers.
        # variables nécéssaires dans FA
        # isol : ménage isolé
        # concub: ménage en couple (rq : concub = ~isol.
        # al_pac : nb de personne à charge du ménage prise en compte pour les AL
        # zone_apl
        # loyer
        # br_al : base ressource des al après abattement.
        # coloc (1 si colocation, 0 sinon)
        # so : statut d'occupation du logement
        #   SO==1 : Accédant à la propriété
        #   SO==2 : Propriétaire (non accédant) du logement.
        #   SO==3 : Locataire d'un logement HLM
        #   SO==4 : Locataire ou sous-locataire d'un logement loué vie non-HLM
        #   SO==5 : Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel.
        #   sO==6 : Logé gratuitement par des parents, des amis ou l'employeur

        loca = (3 <= so) & (5 >= so)
        acce = so == 1
        rmi = al.rmi
        bmaf = fam.af.bmaf_n_2

        # # aides au logement pour les locataires
        # loyer mensuel;
        L1 = loyer
        # loyer plafond;
        lp_taux = (not_(coloc)) * 1 + coloc * al.loyers_plafond.colocation

        z1 = al.loyers_plafond.zone1
        z2 = al.loyers_plafond.zone2
        z3 = al.loyers_plafond.zone3

        Lz1 = (
            isol * (al_pac == 0) * z1.L1 +
            concub * (al_pac == 0) * z1.L2 +
            (al_pac > 0) * z1.L3 +
            (al_pac > 1) * (al_pac - 1) * z1.L4
            ) * lp_taux
        Lz2 = (
            isol * (al_pac == 0) * z2.L1 +
            concub * (al_pac == 0) * z2.L2 +
            (al_pac > 0) * z2.L3 +
            (al_pac > 1) * (al_pac - 1) * z2.L4
            ) * lp_taux
        Lz3 = (
            isol * (al_pac == 0) * z3.L1 +
            concub * (al_pac == 0) * z3.L2 +
            (al_pac > 0) * z3.L3 +
            (al_pac > 1) * (al_pac - 1) * z3.L4
            ) * lp_taux

        L2 = Lz1 * (zone_apl == 1) + Lz2 * (zone_apl == 2) + Lz3 * (zone_apl == 3)
        # loyer retenu
        L = min_(L1, L2)

        # forfait de charges
        P_fc = al.forfait_charges
        C = (
            not_(coloc) * (P_fc.fc1 + al_pac * P_fc.fc2) +
            coloc * ((isol * 0.5 + concub) * P_fc.fc1 + al_pac * P_fc.fc2)
            )

        # dépense éligible
        E = L + C

        # ressources prises en compte
        R = br_al

        # Plafond RO
        R1 = (
            al.R1.taux1 * rmi * (isol) * (al_pac == 0) +
            al.R1.taux2 * rmi * (concub) * (al_pac == 0) +
            al.R1.taux3 * rmi * (al_pac == 1) +
            al.R1.taux4 * rmi * (al_pac >= 2) +
            al.R1.taux5 * rmi * (al_pac > 2) * (al_pac - 2)
            )

        R2 = (
            al.R2.taux4 * bmaf * (al_pac >= 2) +
            al.R2.taux5 * bmaf * (al_pac > 2) * (al_pac - 2)
            )

        Ro = round(12 * (R1 - R2) * (1 - al.autres.abat_sal))

        Rp = max_(0, R - Ro)

        # Participation personnelle
        Po = max_(al.pp.taux * E, al.pp.min)

        # Taux de famille
        TF = (
            al.TF.taux1 * (isol) * (al_pac == 0) +
            al.TF.taux2 * (concub) * (al_pac == 0) +
            al.TF.taux3 * (al_pac == 1) +
            al.TF.taux4 * (al_pac == 2) +
            al.TF.taux5 * (al_pac == 3) +
            al.TF.taux6 * (al_pac >= 4) +
            al.TF.taux7 * (al_pac > 4) * (al_pac - 4)
            )
        # Loyer de référence
        L_Ref = (
            z2.L1 * (isol) * (al_pac == 0) +
            z2.L2 * (concub) * (al_pac == 0) +
            z2.L3 * (al_pac >= 1) +
            z2.L4 * (al_pac > 1) * (al_pac - 1)
            )

        RL = L / L_Ref

        # TODO: paramètres en dur ??
        TL = max_(max_(0, al.TL.taux2 * (RL - 0.45)), al.TL.taux3 * (RL - 0.75) + al.TL.taux2 * (0.75 - 0.45))

        Tp = TF + TL

        PP = Po + Tp * Rp
        al_loc = max_(0, E - PP) * loca
        al_loc = al_loc * (al_loc >= al.autres.nv_seuil)

        # # TODO: APL pour les accédants à la propriété
        al_acc = 0 * acce
        # # APL (tous)
        return al_loc + al_acc

    def get_variable_period(self, output_period, variable_name):
        if variable_name in ['nat_imp_holder']:
            return output_period.start.period(u'year').offset('first-of')
        else:
            return output_period

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class alf(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement familiale"
    url = u"http://vosdroits.service-public.fr/particuliers/F13132.xhtml"

    def function(self, aide_logement_montant, al_pac, so_famille, proprietaire_proche_famille):
        # TODO: également pour les jeunes ménages et femmes enceintes
        # variable ménage à redistribuer
        so = so_famille
        return (al_pac >= 1) * (so != 3) * not_(proprietaire_proche_famille) * aide_logement_montant

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class als_nonet(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement sociale (non étudiante)"

    def function(self, aide_logement_montant, al_pac, etu_holder, so_famille, proprietaire_proche_famille):
        # variable ménage à redistribuer
        so = so_famille

        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        return (al_pac == 0) * (so != 3) * not_(proprietaire_proche_famille) * not_(etu[CHEF] | etu[PART]) * aide_logement_montant

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class alset(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement sociale (non étudiante)"
    url = u"https://www.caf.fr/actualites/2012/etudiants-tout-savoir-sur-les-aides-au-logement"

    def function(self, aide_logement_montant, al_pac, etu_holder, so_holder, proprietaire_proche_famille):
        # variable ménage à redistribuer
        so = self.cast_from_entity_to_roles(so_holder)
        so = self.filter_role(so, role = CHEF)

        etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
        return (al_pac == 0) * (so != 3) * not_(proprietaire_proche_famille) * (etu[CHEF] | etu[PART]) * aide_logement_montant

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class als(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocation logement sociale"
    url = u"http://vosdroits.service-public.fr/particuliers/F1280.xhtml"

    def function(self, als_nonet, alset):
        return als_nonet + alset

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class apl(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u" Aide personnalisée au logement"
    # (réservée aux logements conventionné, surtout des HLM, et financé par le fonds national de l'habitation)"
    url = u"http://vosdroits.service-public.fr/particuliers/F12006.xhtml",

    def function(self, aide_logement_montant, so_holder):
        # TODO:
        # variable ménage à redistribuer
        so = self.cast_from_entity_to_roles(so_holder)
        so = self.filter_role(so, role = CHEF)
        return aide_logement_montant * (so == 3)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class aide_logement(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Aide au logement (tout type)"

    def function(self, apl, als, alf):
        return max_(max_(apl, als), alf)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class crds_lgtm(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"CRDS des allocations logement"
    url = u"http://vosdroits.service-public.fr/particuliers/F17585.xhtml"

    def function(self, aide_logement, crds = law.fam.af.crds):
        return -aide_logement * crds

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class so_individu(EntityToPersonColumn):
    entity_class = Individus
    label = u"Statut d'occupation de l'individu"
    variable = Menages.column_by_name["so"]


@reference_formula
class so_famille(PersonToEntityColumn):
    entity_class = Familles
    label = u"Statut d'occupation de la famille"
    role = CHEF
    variable = Individus.column_by_name["so_individu"]


@reference_formula
class zone_apl(SimpleFormulaColumn):
    column = EnumCol(
        enum = Enum([
            u"Non renseigné",
            u"Zone 1",
            u"Zone 2",
            u"Zone 3",
            ]),
        default = 2
        )
    entity_class = Menages
    label = u"Zone APL"

    def function(self, depcom):
        '''
        Retrouve la zone APL (aide personnalisée au logement) de la commune
        en fonction du depcom (code INSEE)
        '''
        preload_zone_apl()
        default_value = 2
        return fromiter(
            (
                zone_apl_by_depcom.get(depcom_cell, default_value)
                for depcom_cell in depcom
                ),
            dtype = int16,
            )

    def get_output_period(self, period):
        return period


def preload_zone_apl():
    global zone_apl_by_depcom
    if zone_apl_by_depcom is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/20110914_zonage.csv',
                ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            zone_apl_by_depcom = {
                # Keep only first char of Zonage column because of 1bis value considered equivalent to 1.
                row['CODGEO']: int(row['Zonage'][0])
                for row in csv_reader
                }
        # Add subcommunes (arrondissements and communes associées), use the same value as their parent commune.
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/apl/commune_depcom_by_subcommune_depcom.json',
                ) as json_file:
            commune_depcom_by_subcommune_depcom = json.load(json_file)
            for subcommune_depcom, commune_depcom in commune_depcom_by_subcommune_depcom.iteritems():
                zone_apl_by_depcom[subcommune_depcom] = zone_apl_by_depcom[commune_depcom]


@reference_formula
class zone_apl_individu(EntityToPersonColumn):
    entity_class = Individus
    label = u"Zone apl de la personne"
    variable = zone_apl


@reference_formula
class zone_apl_famille(PersonToEntityColumn):
    entity_class = Familles
    label = u"Zone apl de la famille"
    role = CHEF
    variable = zone_apl_individu
