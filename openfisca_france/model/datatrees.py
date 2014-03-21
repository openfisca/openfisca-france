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


columns_name_tree_by_entity = collections.OrderedDict([
    ('ind', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'prenom',  # Prénom
                    'birth',  # Année de naissance
                    'statmarit',  # Statut marital
                    'sali',  # Revenus d'activité imposables
                    'choi',  # Autres revenus imposables (chômage, préretraite)
                    'rsti',  # Pensions, retraites, rentes connues imposables
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Traitements, salaires, primes pour l'emploi et rentes"""),
                ('children', [
                    'activite',  # Activité
                    'fra',  # Frais réels
                    'hsup',  # Heures supplémentaires : revenus exonérés connus
                    'ppe_tp_sa',  # Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière
                    'ppe_tp_ns',  # Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière
                    'ppe_du_sa',  # Prime pour l'emploi des salariés: nombre d'heures payées dans l'année
                    'ppe_du_ns',  # Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année
                    'cho_ld',  # Demandeur d'emploi inscrit depuis plus d'un an
                    'csg_rempl',  # Taux retenu sur la CSG des revenus de remplacment
                    'alr',  # Pensions alimentaires perçues
                    'alr_decl',  # Pension déclarée
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Auto-entrepreneur (ayant opté pour le versement libératoire)"""),
                ('children', [
                    'ebic_impv',  # Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur)
                    'ebic_imps',  # Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)
                    'ebnc_impo',  # Revenus non commerciaux imposables (régime auto-entrepreneur)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus agricoles"""),
                ('children', [
                    'frag_exon',  # Revenus agricoles exonérés (régime du forfait)
                    'frag_impo',  # Revenus agricoles imposables (régime du forfait)
                    'frag_pvct',  # Plus-values agricoles  à court terme (régime du forfait)
                    'frag_pvce',  # Plus-values agricoles de cession taxables à 16% (régime du forfait)
                    'arag_exon',  # Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse
                    'arag_impg',  # Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'arag_defi',  # Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'arag_pvce',  # Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'nrag_exon',  # Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse
                    'nrag_impg',  # Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)
                    'nrag_defi',  # Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)
                    'nrag_pvce',  # Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)
                    'nrag_ajag',  # Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus industriels et commerciaux professionnels"""),
                ('children', [
                    'mbic_exon',  # Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)
                    'mbic_impv',  # Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)
                    'mbic_imps',  # Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)
                    'mbic_pvct',  # Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)
                    'mbic_mvlt',  # Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)
                    'mbic_pvce',  # Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)
                    'abic_exon',  # Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_exon',  # Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)
                    'abic_impn',  # Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'abic_imps',  # Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_impn',  # Revenus industriels et commerciaux imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nbic_imps',  # Revenus industriels et commerciaux imposables: régime simplifié sans CGA (régime du bénéfice réel)
                    'abic_defn',  # Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'abic_defs',  # Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_defn',  # Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nbic_defs',  # Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)
                    'nbic_apch',  # Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)
                    'abic_pvce',  # Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_pvce',  # Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus industriels et commerciaux non professionnels"""),
                ('children', [
                    'macc_exon',  # Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)
                    'aacc_exon',  # Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)
                    'nacc_exon',  # Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)
                    'macc_impv',  # Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)
                    'macc_imps',  # Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)
                    'aacc_impn',  # Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'aacc_imps',  # Locations meublées non professionnelles (régime micro entreprise)
                    'aacc_defn',  # Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'aacc_defs',  # Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)
                    'nacc_impn',  # Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nacc_imps',  # Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)
                    'nacc_defn',  # Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nacc_defs',  # Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux avec CGA ou viseur (régime du bénéfice réel)
                    'macc_pvct',  # Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)
                    'macc_mvlt',  # Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)
                    'macc_pvce',  # Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)
                    'aacc_pvce',  # Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)
                    'nacc_pvce',  # Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus non commerciaux professionnels"""),
                ('children', [
                    'mbnc_exon',  # Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)
                    'abnc_exon',  # Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_exon',  # Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)
                    'mbnc_impo',  # Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)
                    'abnc_impo',  # Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'abnc_defi',  # Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_impo',  # Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)
                    'nbnc_defi',  # Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)
                    'mbnc_pvct',  # Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)
                    'mbnc_mvlt',  # Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)
                    'mbnc_pvce',  # Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)
                    'abnc_pvce',  # Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_pvce',  # Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus non commerciaux non professionnels"""),
                ('children', [
                    'mncn_impo',  # Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)
                    'cncn_bene',  # Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)
                    'cncn_defi',  # Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)
                    'mncn_pvct',  # Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)
                    'mncn_mvlt',  # Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)
                    'mncn_pvce',  # Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)
                    'cncn_pvce',  # Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""inv""",  # Invalide
                    u"""alt""",  # Enfant en garde alternée
                    u"""nbsala""",  # Nombre de salariés dans l'établissement de l'emploi actuel
                    u"""tva_ent""",  # L'entreprise employant le salarié paye de la TVA
                    u"""code_risque""",  # Code risque pour les accidents du travail
                    u"""exposition_accident""",  # Exposition au risque pour les accidents du travail
                    u"""boursier""",  # Elève ou étudiant boursier
                    u"""f1tv""",  # Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans
                    u"""f1tw""",  # Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans
                    u"""f1tx""",  # Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans
                    u"""f3vd""",  # Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %
                    u"""f3vf""",  # Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %
                    u"""f3vi""",  # Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %
                    u"""f3vj""",  # Gains imposables sur option dans la catégorie des salaires
                    u"""f3va""",  # Abattement pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values
                    u"""f5qm""",  # Agents généraux d’assurances: indemnités de cessation d’activité
                    u"""f6ps""",  # Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)
                    u"""f6rs""",  # Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S
                    u"""f6ss""",  # Rachat de cotisations PERP, PREFON, COREM et C.G.O.S
                    u"""f7ac""",  # Cotisations syndicales des salariées et pensionnés
                    u"""nbic_mvct""",  # Revenus industriels et commerciaux moins-values nettes à court terme
                    u"""categ_inv""",  # Catégorie de handicap (AEEH)
                    u"""etr""",
                    u"""coloc""",  # Vie en colocation
                    u"""aer""",  # Allocation équivalent retraite (AER)
                    u"""ass""",  # Allocation de solidarité spécifique (ASS)
                    u"""f5sq""",
                    u"""adoption""",  # Enfant adopté
                    ]),
                ]),
            ]),
        ])),
    ('fam', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""inactif""",  # Parent inactif (PAJE-CLCA)
                    u"""partiel1""",  # Parent actif à moins de 50% (PAJE-CLCA)
                    u"""partiel2""",  # Parent actif entre 50% et 80% (PAJE-CLCA)
                    u"""opt_colca""",  # Opte pour le COLCA
                    u"""empl_dir""",  # Emploi direct (CLCMG)
                    u"""ass_mat""",  # Assistante maternelle (CLCMG)
                    u"""gar_dom""",  # Garde à domicile (CLCMG)
                    ]),
                ]),
            ]),
        ])),
    ('foy', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'jour_xyz',  # Jours décomptés au titre de cette déclaration
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Situations particulières"""),
                ('children', [
                    'caseK',  # Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre
                    'caseL',  # Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul
                    'caseE',  # Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul
                    'caseN',  # Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus
                    'caseP',  # Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%
                    'caseF',  # Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)
                    'caseW',  # Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre
                    'caseS',  # Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre
                    'caseG',  # Titulaire d'une pension de veuve de guerre
                    'caseH',  # Année de naissance des enfants à charge en garde alternée
                    'nbN',  # Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille
                    'nbR',  # Nombre de titulaires de la carte invalidité d'au moins 80 %
                    'caseT',  # Vous êtes parent isolé au 1er janvier de l'année de perception des revenus
                    'rfr_n_2',  # Revenu fiscal de référence année n-2
                    'nbptr_n_2',  # Nombre de parts année n-2
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Traitements, salaires, primes pour l'emploi, pensions et rentes"""),
                ('children', [
                    'f1aw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans
                    'f1bw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans
                    'f1cw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans
                    'f1dw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus des valeurs et capitaux mobiliers"""),
                ('children', [
                    'f2da',  # Revenus des actions et parts soumis au prélèvement libératoire de 21 %
                    'f2dh',  # Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %
                    'f2ee',  # Autres produits de placement soumis aux prélèvements libératoires
                    'f2dc',  # Revenus des actions et parts donnant droit à abattement
                    'f2fu',  # Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement
                    'f2ch',  # Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement
                    'f2ts',  # Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)
                    'f2go',  # Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)
                    'f2tr',  # Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)
                    'f2cg',  # Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible
                    'f2bh',  # Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible
                    'f2ca',  # Frais et charges déductibles
                    'f2aa',  # Déficits des années antérieures non encore déduits
                    'f2ab',  # Crédits d'impôt sur valeurs étrangères
                    'f2al',  # Déficits des années antérieures non encore déduits
                    'f2am',  # Déficits des années antérieures non encore déduits
                    'f2an',  # Déficits des années antérieures non encore déduits
                    'f2aq',  # Déficits des années antérieures non encore déduits
                    'f2ar',  # Déficits des années antérieures non encore déduits
                    'f2as',  # Déficits des années antérieures non encore déduits: année 2012
                    'f2gr',  # Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Plus-values de cession de valeurs mobilières, droits sociaux et gains assimilés"""),
                ('children', [
                    'f3vc',  # Produits et plus-values exonérés provenant de structure de capital-risque
                    'f3ve',  # Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %
                    'f3vl',  # Distributions par des sociétés de capital-risque taxables à 19 %
                    'f3vm',  # Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %
                    'f3vg',  # Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés
                    'f3vh',  # Perte de l'année de perception des revenus
                    'f3vt',  # Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %
                    'f3vu',
                    'f3vv',  # Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé
                    'f3si',
                    'f3sa',
                    'f3sf',
                    'f3sd',
                    'f3vz',  # Plus-values imposables sur cessions d’immeubles ou de biens meubles
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus fonciers"""),
                ('children', [
                    'f4ba',  # Revenus fonciers imposables
                    'f4bb',  # Déficit imputable sur les revenus fonciers
                    'f4bc',  # Déficit imputable sur le revenu global
                    'f4bd',  # Déficits antérieurs non encore imputés
                    'f4be',  # Micro foncier: recettes brutes sans abattement
                    'f4bf',  # Primes d'assurance pour loyers impayés des locations conventionnées
                    'f4bl',
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Charges déductibles"""),
                ('children', [
                    'f6de',  # CSG déductible calculée sur les revenus du patrimoine
                    'f6gi',  # Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant
                    'f6gj',  # Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant
                    'f6el',  # Autres pensions alimentaires versées à des enfants majeurs: 1er enfant
                    'f6em',  # Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant
                    'f6gp',  # Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)
                    'f6gu',  # Autres pensions alimentaires versées (mineurs, ascendants)
                    'f6eu',  # Frais d'accueil de personnes de plus de 75 ans dans le besoin
                    'f6ev',  # Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit
                    'f6dd',  # Déductions diverses
                    'f6aa',  # Souscriptions en faveur du cinéma ou de l’audiovisuel
                    'f6cc',  # Souscriptions au capital des SOFIPÊCHE
                    'f6eh',
                    'f6da',  # Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté
                    'f6cb',  # Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)
                    'f6hj',  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    'f6gh',  # Sommes à ajouter au revenu imposable
                    'f6fa',  # Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6
                    'f6fb',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5
                    'f6fc',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4
                    'f6fd',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3
                    'f6fe',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2
                    'f6fl',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Charges déductibles (autres)"""),
                ('children', [
                    'f7ud',  # Dons à des organismes d'aide aux personnes en difficulté
                    'f7uf',  # Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général
                    'f7xs',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5
                    'f7xt',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4
                    'f7xu',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3
                    'f7xw',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2
                    'f7xy',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1
                    'f7db',  # Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés
                    'f7df',  # Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés
                    'f7dq',  # Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés
                    'f7dg',  # Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés
                    'f7dl',  # Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés
                    'f7vy',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité
                    'f7vz',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes
                    'f7vx',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011
                    'f7vw',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité
                    'f7cd',  # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne
                    'f7ce',  # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne
                    'f7ga',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge
                    'f7gb',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge
                    'f7gc',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge
                    'f7ge',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée
                    'f7gf',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée
                    'f7gg',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée
                    'f7ea',  # Nombre d'enfants à charge poursuivant leurs études au collège
                    'f7eb',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège
                    'f7ec',  # Nombre d'enfants à charge poursuivant leurs études au lycée
                    'f7ed',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée
                    'f7ef',  # Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur
                    'f7eg',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur
                    'f7td',  # Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés
                    'f7vo',  # Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés
                    'f7uk',  # Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés
                    'f7gz',  # Primes de rente survie, contrats d'épargne handicap
                    'f7wm',  # Prestations compensatoires: Capital fixé en substitution de rente
                    'f7wn',  # Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés
                    'f7wo',  # Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué
                    'f7wp',  # Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1
                    'f7we',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés
                    'f7wq',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées
                    'f7wh',  # Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus
                    'f7wk',  # Votre habitation principale est une maison individuelle
                    'f7wf',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1
                    'f7wi',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction
                    'f7wj',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées
                    'f7wl',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques
                    'f7ur',  # Investissements réalisés en n-1, total réduction d’impôt
                    'f7oz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6
                    'f7pz',  # Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures
                    'f7qz',  # Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures
                    'f7rz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3
                    'f7sz',  # Dépenses en faveur de la qualité environnementale des logements donnés en location
                    'f7fy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1
                    'f7gy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1
                    'f7jy',  # Report de 1/9 des investissements réalisés l'année de perception des revenus déclarés -3 ou -4
                    'f7hy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1
                    'f7ky',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1
                    'f7iy',  # Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés
                    'f7ly',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés
                    'f7my',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés
                    'f7ra',  # Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager
                    'f7rb',  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    'f7gw',  # Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt
                    'f7gx',  # Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt
                    'f7xc',  # Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1
                    'f7xd',  # Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans
                    'f7xe',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans
                    'f7xf',  # Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures
                    'f7xh',  # Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme
                    'f7xi',  # Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures
                    'f7xj',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures
                    'f7xk',  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    'f7xl',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans
                    'f7xm',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures
                    'f7xn',  # Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures
                    'f7xo',  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    'f7cf',  # Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion
                    'f7cl',  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4
                    'f7cm',  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3
                    'f7cn',  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2
                    'f7cu',  # Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures
                    'f7gs',  # Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon
                    'f7ua',
                    'f7ub',
                    'f7uc',  # Cotisations pour la défense des forêts contre l'incendie
                    'f7ui',
                    'f7uj',
                    'f7qb',
                    'f7qc',
                    'f7qd',
                    'f7ql',
                    'f7qt',
                    'f7qm',
                    'f7gq',  # Souscription de parts de fonds communs de placement dans l'innovation
                    'f7fq',  # Souscription de parts de fonds d'investissement de proximité
                    'f7fm',  # Souscription de parts de fonds d'investissement de proximité investis en Corse
                    'f7fl',  # Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer
                    'f7gn',  # Souscriptions au capital de SOFICA 36 %
                    'f7fn',  # Souscriptions au capital de SOFICA 30 %
                    'f7fh',  # Intérêts d'emprunt pour reprise de société
                    'f7ff',  # Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)
                    'f7fg',  # Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations
                    'f7nz',  # Travaux de conservation et de restauration d’objets classés monuments historiques
                    'f7ka',  # Dépenses de protection du patrimoine naturel
                    'f7wg',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1
                    'f7uh',  # Dons et cotisations versés aux partis politiques
                    'f7un',  # Investissements forestiers: acquisition
                    'f7um',  # Intérêts pour paiement différé accordé aux agriculteurs
                    'f7hj',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole
                    'f7hk',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM
                    'f7hn',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010
                    'f7ho',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010
                    'f7hl',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)
                    'f7hm',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds
                    'f7hr',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 (métropole et DOM ne respectant pas les plafonds): report de 1/9 de l'investissement
                    'f7hs',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM et respectant les plafonds: report de 1/9 de l'investissement
                    'f7la',  # Investissements locatifs neufs dispositif Scellier: report du solde de réduction d'impôt non encore imputé
                    'f7ij',  # Investissement destinés à la location meublée non professionnelle: engagement de réalisation de l'investissement en 2011
                    'f7il',  # Investissement destinés à la location meublée non professionnelle: promesse d'achat en 2010
                    'f7im',  # Investissement destinés à la location meublée non professionnelle: investissement réalisés en 2010 avec promesse d'achat en 2009
                    'f7ik',  # Reports de 1/9 de l'investissement réalisé et achevé en 2009
                    'f7is',  # Report du solde de réduction d'impôt non encore imputé: année  n-4
                    'f7gt',  # Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010
                    'f7xg',  # Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme
                    'f7gu',  # Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009
                    'f7gv',  # Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres imputations et divers"""),
                ('children', [
                    'f8ta',  # Retenue à la source en France ou impôt payé à l'étranger
                    'f8tb',  # Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)
                    'f8tf',  # Reprises de réductions ou de crédits d'impôt
                    'f8tg',  # Crédits d'impôt en faveur des entreprises: Investissement en Corse
                    'f8th',  # Retenue à la source élus locaux
                    'f8tc',  # Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))
                    'f8td',  # Contribution exceptionnelle sur les hauts revenus
                    'f8te',  # Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé
                    'f8to',  # Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures
                    'f8tp',  # Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt
                    'f8uz',  # Crédit d'impôt en faveur des entreprises: Famille
                    'f8tz',  # Crédit d'impôt en faveur des entreprises: Apprentissage
                    'f8wa',  # Crédit d'impôt en faveur des entreprises: Agriculture biologique
                    'f8wb',  # Crédit d'impôt en faveur des entreprises: Prospection commerciale
                    'f8wc',  # Crédit d'impôt en faveur des entreprises: Prêts sans intérêt
                    'f8wd',  # Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise
                    'f8we',  # Crédit d'impôt en faveur des entreprises: Intéressement
                    'f8wr',  # Crédit d'impôt en faveur des entreprises: Métiers d'art
                    'f8ws',  # Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes
                    'f8wt',  # Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs
                    'f8wu',  # Crédit d'impôt en faveur des entreprises: Maître restaurateur
                    'f8wv',  # Crédit d'impôt en faveur des entreprises: Débitants de tabac
                    'f8wx',  # Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise
                    'f8wy',
                    'f7uo',  # Acquisition de biens culturels
                    'f7us',  # Réduction d'impôt mécénat d'entreprise
                    'f7sb',  # Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %
                    'f7sd',  # Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation
                    'f7se',  # Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz
                    'f7sh',  # Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)
                    'f7sc',  # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
                    'f7up',  # Crédit d'impôt pour investissements forestiers: travaux
                    'f7uq',  # Crédit d'impôt pour investissements forestiers: contrat de gestion
                    'f1ar',  # Crédit d'impôt aide à la mobilité
                    'f1br',  # Crédit d'impôt aide à la mobilité
                    'f1cr',  # Crédit d'impôt aide à la mobilité
                    'f1dr',  # Crédit d'impôt aide à la mobilité
                    'f1er',  # Crédit d'impôt aide à la mobilité
                    'f2bg',  # Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables
                    'f4tq',  # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
                    'f7sf',  # Appareils de régulation du chauffage, matériaux de calorifugeage
                    'f7si',  # Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)
                    'f8uy',  # Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé
                    'mbic_mvct',  # Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)
                    'macc_mvct',  # Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)
                    'mncn_mvct',  # Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)
                    'mbnc_mvct',  # Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Impôt de solidarité sur la fortune"""),
                ('children', [
                    'b1ab',  # Valeur de la résidence principale avant abattement
                    'b1ac',  # Valeur des autres immeubles avant abattement
                    'b1bc',  # Immeubles non bâtis : bois, fôrets et parts de groupements forestiers
                    'b1be',  # Immeubles non bâtis : biens ruraux loués à long termes
                    'b1bh',  # Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers
                    'b1bk',  # Immeubles non bâtis : autres biens
                    'b1cl',  # Parts et actions détenues par les salariés et mandataires sociaux
                    'b1cb',  # Parts et actions de sociétés avec engagement de conservation de 6 ans minimum
                    'b1cd',  # Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité
                    'b1ce',  # Autres valeurs mobilières
                    'b1cf',  # Liquidités
                    'b1cg',  # Autres biens meubles
                    'b1co',  # Autres biens meubles : contrats d'assurance-vie
                    'b2gh',  # Total du passif et autres déductions
                    'b2mt',  # Réductions pour investissements directs dans une société
                    'b2ne',  # Réductions pour investissements directs dans une société
                    'b2mv',  # Réductions pour investissements par sociétés interposées, holdings
                    'b2nf',  # Réductions pour investissements par sociétés interposées, holdings
                    'b2mx',  # Réductions pour investissements par le biais de FIP
                    'b2na',  # Réductions pour investissements par le biais de FCPI ou FCPR
                    'b2nc',  # Réductions pour dons à certains organismes d'intérêt général
                    'b4rs',  # Montant de l'impôt acquitté hors de France
                    'rev_or',
                    'rev_exo',
                    'tax_fonc',  # Taxe foncière
                    'restit_imp',
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""f2ck""",  # Crédit d'impôt égal au prélèvement forfaitaire déjà versé
                    u"""f2dm""",  # Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %
                    u"""f6hk""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    u"""f6hl""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    u"""f6hm""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    u"""f7vv""",  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes
                    u"""f7vu""",  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité
                    u"""f7vt""",  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes
                    u"""f7wt""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement
                    u"""f7cc""",  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1
                    ]),
                ]),
            ]),
        ])),
    ('men', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'loyer',  # Loyer mensuel
                    'so',  # Statut d'occupation
                    'code_postal',  # Code postal du lieu de résidence
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""zthabm""",
                    ]),
                ]),
            ]),
        ])),
    ])
