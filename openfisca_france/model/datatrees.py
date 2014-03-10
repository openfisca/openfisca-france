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
                    'statmarit',  # Statut marital
                    'sali',  # Salaire imposable
                    'choi',  # Chômage imposable
                    'rsti',  # Retraite imposable
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Traitements, salaires, primes pour l'emploi et rentes"""),
                ('children', [
                    'activite',  # Activité
                    'fra',  # Frais réels
                    'hsup',  # Heures supplémentaires
                    'ppe_tp_sa',  # Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière
                    'ppe_tp_ns',  # Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière
                    'ppe_du_sa',  # Prime pour l'emploi des salariés: nombre d'heures payées dans l'année
                    'ppe_du_ns',  # Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année
                    'cho_ld',  # Chômeur de longue durée
                    'csg_rempl',  # Taux retenu sur la CSG des revenus de remplacment
                    'alr',  # Pension alimentaire reçue
                    'alr_decl',  # Pension déclarée
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Auto-entrepreneur (ayant opté pour le versement libératoire)"""),
                ('children', [
                    'ebic_impv',  # Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime auto-entrepreneur)
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
                    'arag_exon',  # Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'arag_impg',  # Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'arag_defi',  # Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'arag_pvce',  # Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'nrag_exon',  # Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)
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
                    'abnc_exon',  # Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_exon',  # Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)
                    'mbnc_impo',  # Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)
                    'abnc_impo',  # Revenus non commerciaux professionnels imposables (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)
                    'abnc_defi',  # Déficits non commerciaux professionnels (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_impo',  # Revenus non commerciaux professionnels imposables (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)
                    'nbnc_defi',  # Déficits non commerciaux professionnels (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)
                    'mbnc_pvct',  # Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)
                    'mbnc_mvlt',  # Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)
                    'mbnc_pvce',  # Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)
                    'abnc_pvce',  # Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)
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
                    u"""tva_ent""",  # Entreprise employant le salarié paye de la TVA
                    u"""code_risque""",  # Code risque pour les accidents du travail
                    u"""exposition_accident""",  # Exposition au risque pour les accidents du travail
                    u"""boursier""",  # Elève ou étudiant boursier
                    u"""f1tv""",
                    u"""f1tw""",
                    u"""f1tx""",
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
                    u"""inactif""",  # Parent incatif (PAJE-CLCA)
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
                    'jour_xyz',  # Jours décomptés au tire de cette déclaration
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Situations particulières"""),
                ('children', [
                    'caseK',  # Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre
                    'caseL',  # Situation pouvant donner droit à une demi-part supplémentaire: enfant élevé seul pendant plus de 5 ans
                    'caseE',  # Situation pouvant donner droit à une demi-part supplémentaire: enfant élevé seul pendant moins de 5 ans
                    'caseN',  # Vous ne vivez pas seul au 1er janvier de l'année n-1
                    'caseP',  # Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%
                    'caseF',  # Situation pouvant donner droit à une demi-part supplémentaire: conjoint titulaire d'une pension ou d'une carte d'invalidité(vivant ou décédé l'année précédente
                    'caseW',  # Votre conjoint âgé de plus de 75 ans, décédé en n-1 était titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre
                    'caseS',  # Vous ou votre conjoint êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre
                    'caseG',  # Titulaire d'une pension de veuve de guerre
                    'nbF',  # Nombre d'enfants à charge  non mariés de moins de 18 ans au 1er janvier de l'année n-1, ou nés en n-1 ou handicapés quel que soit l'âge
                    'nbJ',  # Nombre d'enfants majeurs célibataires sans enfant
                    'nbI',  # Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité
                    'nbH',  # Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de l'année n-1, ou nés en n-1 ou handicapés quel que soit l'âge
                    'caseH',  # Année de naissance des enfants à charge en garde alternée
                    'nbG',  # Nombre d'enfants à charge titulaires de la carte d'invalidité
                    'nbN',  # Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille
                    'nbR',  # Nombre de titulaires de la carte invalidité d'au moins 80 %
                    'caseT',  # Vous êtes parent isolé au 1er janvier de l'année n-1
                    'rfr_n_2',  # Revenu fiscal de référence année n-2
                    'nbptr_n_2',  # Nombre de parts année n-2
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Traitements, salaires, primes pour l'emploi, pensions et rentes"""),
                ('children', [
                    'f1aw',  # Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : Moins de 50 ans
                    'f1bw',  # Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : De 50 à 59 ans
                    'f1cw',  # Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : De 60 à 69 ans
                    'f1dw',  # Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : A partir de 70 ans
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus des valeurs et capitaux mobiliers"""),
                ('children', [
                    'f2da',  # Revenus des actions et parts soumis au prélèvement libératoire
                    'f2dh',  # Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire
                    'f2ee',  # Revenus au prélèvement libératoire hors actions et assurance-vie
                    'f2dc',  # Revenus des actions et parts donnant droit à abattement
                    'f2fu',  # Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement
                    'f2ch',  # Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement
                    'f2ts',  # Revenus de valeurs mobilières et distributions
                    'f2go',  # Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié
                    'f2tr',  # Intérêts et autres revenus assimilés
                    'f2cg',  # Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible
                    'f2bh',  # Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible
                    'f2ca',  # Frais venant en déduction
                    'f2aa',  # Déficits des années antérieures non encore déduits: année 2006
                    'f2ab',  # Crédits d'impôt sur valeurs étrangères
                    'f2al',  # Déficits des années antérieures non encore déduits: année 2007
                    'f2am',  # Déficits des années antérieures non encore déduits: année 2008
                    'f2an',  # Déficits des années antérieures non encore déduits: année 2009
                    'f2aq',  # Déficits des années antérieures non encore déduits: année 2010
                    'f2ar',  # Déficits des années antérieures non encore déduits: année 2011
                    'f2as',  # Déficits des années antérieures non encore déduits: année 2012
                    'f2gr',
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Plus-values de cession de valeurs mobilières, droits sociaux et gains assimilés"""),
                ('children', [
                    'f3vc',  # Produits et plus-values exonérés provenant de structure de capital-risque
                    'f3vd',  # Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 18 %
                    'f3ve',
                    'f3vf',  # Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 41 %
                    'f3vl',  # Distributions par des sociétés de capital-risque taxables à 24 %
                    'f3vi',  # Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 30 %
                    'f3vm',  # Clôture du PEA : avant l'expiration de la 2e année
                    'f3vj',  # Gains imposables sur option dans la catégorie des salaires: déclarant 1
                    'f3vk',  # Gains imposables sur option dans la catégorie des salaires: déclarant 2
                    'f3va',  # Abattement net pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values
                    'f3vg',  # Plus-values de cession de valeurs mobilières, droits sociaux et gains assimilés
                    'f3vh',  # Perte de l'année n-1
                    'f3vt',  # Clôture du PEA : entre la 2e et la 5e année
                    'f3vu',
                    'f3vv',
                    'f3si',
                    'f3sa',
                    'f3sf',
                    'f3sd',
                    'f3vz',  # Plus-values imposables de cession d’immeubles ou de biens meubles
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
                ('label', u"""Section 5"""),
                ('children', [
                    'f5qm',  # Agents généraux d’assurances: indemnités de cessation d’activité, déclarant 1
                    'f5rm',  # Agents généraux d’assurances: indemnités de cessation d’activité, déclarant 2
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Charges déductibles"""),
                ('children', [
                    'f6de',  # CSG déductible calculée sur les revenus du patrimoine
                    'f6gi',  # Pensions alimentaires versées à des enfants majeurs: 1er enfant
                    'f6gj',  # Pensions alimentaires versées à des enfants majeurs: 2eme enfant
                    'f6el',  # Autres pensions alimentaires versées à des enfants majeurs: 1er enfant
                    'f6em',  # Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant
                    'f6gp',  # Autres pensions alimentaires versées (mineurs, ascendants)
                    'f6gu',  # Autres pensions alimentaires versées (mineurs, ascendants)
                    'f6eu',  # Frais d'accueil de personnes de plus de 75 ans dans le besoin
                    'f6ev',  # Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit
                    'f6dd',  # Déductions diverses
                    'f6ps',  # Plafond de déduction: déclarant 1
                    'f6rs',  # Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: déclarant 1
                    'f6ss',  # Rachat de cotisations PREFON, COREM et C.G.O.S: déclarant 1
                    'f6pt',  # Plafond de déduction: déclarant 2
                    'f6rt',  # Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: déclarant 2
                    'f6st',  # Rachat de cotisations PREFON, COREM et C.G.O.S: déclarant 2
                    'f6pu',  # Plafond de déduction: personne à charge
                    'f6ru',  # Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: personne à charge
                    'f6su',  # Rachat de cotisations PREFON, COREM et C.G.O.S: personne à charge
                    'f6aa',  # Souscriptions en faveur du cinéma ou de l’audiovisuel
                    'f6cc',  # Souscriptions au capital des SOFIPÊCHE
                    'f6eh',
                    'f6da',  # Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté
                    'f6cb',  # Dépenses de grosses réparations effectuées par les nus-propriétaires
                    'f6hj',  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    'f6gh',  # Sommes à ajouter au revenu imposable
                    'f6fa',  # Deficits globaux des années antérieures non encore déduits: année n-7
                    'f6fb',  # Deficits globaux des années antérieures non encore déduits: année n-6
                    'f6fc',  # Deficits globaux des années antérieures non encore déduits: année n-5
                    'f6fd',  # Deficits globaux des années antérieures non encore déduits: année n-4
                    'f6fe',  # Deficits globaux des années antérieures non encore déduits: année n-3
                    'f6fl',  # Deficits globaux des années antérieures non encore déduits: année n-2
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Charges déductibles (autres)"""),
                ('children', [
                    'f7ud',  # Dons à des organismes d'aide aux personnes en difficulté
                    'f7uf',  # Autres dons
                    'f7xs',  # Report des années antérieures des réductions et crédits d'impôt: année n-6
                    'f7xt',  # Report des années antérieures des réductions et crédits d'impôt: année n-5
                    'f7xu',  # Report des années antérieures des réductions et crédits d'impôt: année n-4
                    'f7xw',  # Report des années antérieures des réductions et crédits d'impôt: année n-3
                    'f7xy',  # Report des années antérieures des réductions et crédits d'impôt: année n-2
                    'f7ac',  # Cotisations syndicales des salariées et pensionnés: déclarant 1
                    'f7ae',  # Cotisations syndicales des salariées et pensionnés: déclarant 2
                    'f7ag',  # Cotisations syndicales des salariées et pensionnés: personne à charge
                    'f7db',  # Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi en n-1
                    'f7df',  # Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives en n-1
                    'f7dq',  # Emploi direct pour la première fois d'un salarié à domicile en n-1
                    'f7dg',  # Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'aumoins 80 % en n-1
                    'f7dl',  # Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées en n-1
                    'f7vy',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité
                    'f7vz',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première suivante
                    'f7vx',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011
                    'f7vw',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010
                    'f7cd',  # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne
                    'f7ce',  # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne
                    'f7ga',  # Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 1er enfant à charge
                    'f7gb',  # Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 2ème enfant à charge
                    'f7gc',  # Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 3ème enfant à charge
                    'f7ge',  # Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 1er enfant à charge en résidence alternée
                    'f7gf',  # Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 2ème enfant à charge en résidence alternée
                    'f7gg',  # Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 3ème enfant à charge en résidence alternée
                    'f7ea',  # Nombre d'enfants à charge poursuivant leurs études au collège
                    'f7eb',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège
                    'f7ec',  # Nombre d'enfants à charge poursuivant leurs études au lycée
                    'f7ed',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée
                    'f7ef',  # Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur
                    'f7eg',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur
                    'f7td',  # Intérêts des prêts étudiants versés avant l'année n-1
                    'f7vo',  # Nombre d'années de remboursement du prêt étudiant avant l'année n-1
                    'f7uk',  # Intérêts des prêts étudiants versés en n-1
                    'f7gz',  # Primes de rente survie, contrats d'épargne handicap
                    'f7wm',  # Prestations compensatoires: Capital fixé en substitution de rente
                    'f7wn',  # Prestations compensatoires: Sommes versées en n-1
                    'f7wo',  # Prestations compensatoires: Sommes totales décidées par jugement en n-1 ou capital reconstitué
                    'f7wp',  # Prestations compensatoires: Report des sommes décidées en n-2
                    'f7we',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise en n-1
                    'f7wq',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées
                    'f7wh',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: bouquet de travaux
                    'f7wk',  # Votre habitation principale est une maison individuelle
                    'f7wf',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1
                    'f7wi',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction
                    'f7wj',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées
                    'f7wl',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques
                    'f7ur',  # Investissements réalisés en n-1, total réduction d’impôt
                    'f7oz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6
                    'f7pz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-5
                    'f7qz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-4
                    'f7rz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3
                    'f7sz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-2
                    'f7fy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1
                    'f7gy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1
                    'f7jy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et ayant pris fin en n-1
                    'f7hy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1
                    'f7ky',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1
                    'f7iy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et n'ayant pas pris fin en n-1
                    'f7ly',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-2 et ayant pas pris fin en n-1
                    'f7my',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-2 et ayant pas pris fin en n-1
                    'f7ra',  # Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbail et paysager
                    'f7rb',  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    'f7gw',
                    'f7gx',
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
                    'f7xn',  # Investissements locatifs dans une résidence hôtelière à vocation sociale: investissement réalisé en n-1
                    'f7xo',  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    'f7cf',  # Souscriptions au capital des PME non cotées, montant versé en n-1
                    'f7cl',  # Souscriptions au capital des PME non cotées, report de versement de l'année n-4
                    'f7cm',  # Souscriptions au capital des PME non cotées, report de versement de l'année n-3
                    'f7cn',  # Souscriptions au capital des PME non cotées, report de versement de l'année n-2
                    'f7cu',  # Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures
                    'f7gs',  # Souscription au capital d’une SOFIPECHE
                    'f7ua',
                    'f7ub',
                    'f7uc',
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
                    'f7fl',
                    'f7gn',  # Souscriptions au capital de SOFICA 48 %
                    'f7fn',  # Souscriptions au capital de SOFICA 40 %
                    'f7fh',  # Intérêts d'emprunt pour reprise de société
                    'f7ff',  # Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)
                    'f7fg',  # Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations
                    'f7nz',  # Travaux de conservation et de restauration d’objets classés monuments historiques
                    'f7ka',  # Dépenses de protection du patrimoine naturel
                    'f7wg',  # Intérêts d'emprunts
                    'f7uh',
                    'f7un',  # Investissements forestiers: acquisition
                    'f7um',  # Intérêts pour paiement différé accordé aux agriculteurs
                    'f7hj',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole
                    'f7hk',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM
                    'f7hn',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier
                    'f7ho',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier
                    'f7hl',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)
                    'f7hm',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds
                    'f7hr',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 (métropole et DOM ne respectant pas les plafonds)
                    'f7hs',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM et respectant les plafonds
                    'f7la',  # Investissements locatifs neufs dispositif Scellier: report du solde de réduction d'impôt non encore imputé
                    'f7ij',  # Investissement destinés à la location meublée non professionnelle: engagement de réalisation de l'investissement en n-1
                    'f7il',  # Investissement destinés à la location meublée non professionnelle: promesse d'achat en n-2
                    'f7im',  # Investissement destinés à la location meublée non professionnelle: promesse d'achat en n-3
                    'f7ik',  # Reports de 1/9 de l'investissement réalisé et achevé au cours de l'année n-4
                    'f7is',  # Report du solde de réduction d'impôt non encor imputé: année  n-4
                    'f7gt',
                    'f7xg',  # Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme
                    'f7gu',
                    'f7gv',
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres imputations et divers"""),
                ('children', [
                    'f8ta',  # Retenue à la source en France ou impôt payé à l'étranger
                    'f8tb',  # Crédit d'impôt recherche non encore remboursé
                    'f8tf',  # Reprises de réductions ou de crédits d'impôt
                    'f8tg',  # Crédits d'impôt en faveur des entreprises: Investissement en Corse
                    'f8th',  # Retenue à la source élus locaux
                    'f8tc',  # Crédit d'impôt recherche non encore remboursé (années antérieures)
                    'f8td',  # Contribution exceptionnelle sur les hauts revenus
                    'f8te',  # Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé
                    'f8to',  # Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures
                    'f8tp',  # Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt
                    'f8uz',  # Crédit d'impôt en faveur des entreprises: Famille
                    'f8tz',  # Crédit d'impôt en faveur des entreprises: Apprentissage
                    'f8wa',  # Crédit d'impôt en faveur des entreprises: Agriculture biologique
                    'f8wb',  # Crédit d'impôt en faveur des entreprises: Prospection commerciale
                    'f8wc',  # Crédit d'impôt en faveur des entreprises: Nouvelles technologies
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
                    'f7sd',  # Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 40 %
                    'f7se',  # Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 50 %
                    'f7sh',  # Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 15 %
                    'f7sc',
                    'f7up',  # Crédit d'impôt
                    'f7uq',  # Crédit d'impôt
                    'f1ar',  # Crédit d'impôt aide à la mobilité
                    'f1br',  # Crédit d'impôt aide à la mobilité
                    'f1cr',  # Crédit d'impôt aide à la mobilité
                    'f1dr',  # Crédit d'impôt aide à la mobilité
                    'f1er',  # Crédit d'impôt aide à la mobilité
                    'f2bg',  # Crédit d’impôt directive « épargne »
                    'f4tq',  # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
                    'f7sf',  # Appareils de régulation du chauffage, matériaux de calorifugeage
                    'f7si',  # Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)
                    'f8uy',  # Auto-entrepreneur : versements libératoires d’impôt sur le revenu
                    'mbic_mvct',  # Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)
                    'macc_mvct',  # Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)
                    'mncn_mvct',  # Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)
                    'mbnc_mvct',  # Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Impôt de solidarité sur la fortune"""),
                ('children', [
                    'b1ab',  # valeur résidence principale avant abattement 
                    'b1ac',  # valeur autres immeubles avant abattement
                    'b1bc',  # Immeubles non bâtis: bois, fôrets et parts de groupements forestiers
                    'b1be',  # Immeubles non bâtis: biens ruraux loués à long termes
                    'b1bh',  # Immeubles non bâtis: parts de groupements fonciers agricoles et de groupements agricoles fonciers
                    'b1bk',  # Immeubles non bâtis: autres biens
                    'b1cl',  # Parts et actions détenues par les salariés et mandataires sociaux
                    'b1cb',  # Parts et actions de sociétés avec engagement de conservation de 6 ans minimum
                    'b1cd',  # Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité
                    'b1ce',  # Autres valeurs mobilières
                    'b1cf',  # Liquidités
                    'b1cg',  # Autres biens meubles
                    'b1co',  # Autres biens meubles: contrats d'assurance-vie
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
                    u"""f6hl""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    u"""f6hk""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    ]),
                ]),
            ]),
        ])),
    ('men', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'zone_apl',  # Zone apl
                    'loyer',  # Loyer mensuel
                    'so',  # Statut d'occupation
                    'code_postal',  # Code postal du lieu de résidence
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""m_afeamam""",
                    u"""m_agedm""",
                    u"""m_clcam""",
                    u"""m_colcam""",
                    u"""m_mgamm""",
                    u"""m_mgdomm""",
                    u"""zthabm""",
                    ]),
                ]),
            ]),
        ])),
    ])
