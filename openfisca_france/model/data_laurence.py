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

from openfisca_core.columns import IntCol, EnumCol, BoolCol, AgesCol, FloatCol
from openfisca_core.enumerations import Enum

def build_column_couple(name, column):
    assert isinstance(name, basestring), name
    name = unicode(name)
    if column.label is None:
        column.label = name
    assert column.name is None
    column.name = name

    entity_column_by_name = entities.entity_class_by_symbol[column.entity].column_by_name
    assert name not in entity_column_by_name, name
    entity_column_by_name[name] = column

    return (name, column)



QUIFOY = Enum(['vous', 'conj', 'pac1', 'pac2', 'pac3', 'pac4', 'pac5', 'pac6', 'pac7', 'pac8', 'pac9'])
QUIFAM = Enum(['chef', 'part', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])
QUIMEN = Enum(['pref', 'cref', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])

# Socio-economic data
# Données d'entrée de la simulation à fournir à partir d'une enquête ou générées par le générateur de cas type
column_by_name = collections.OrderedDict((
    ('noi', IntCol(label = u"Numéro d'ordre individuel")),

    ('idmen', IntCol(label = u"Identifiant du ménage")),  # 600001, 600002,
    ('idfoy', IntCol(label = u"Identifiant du foyer")),  # idmen + noi du déclarant
    ('idfam', IntCol(label = u"Identifiant de la famille")),  # idmen + noi du chef de famille

    ('quimen', EnumCol(QUIMEN)),
    ('quifoy', EnumCol(QUIFOY)),
    ('quifam', EnumCol(QUIFAM)),

    ('sali', IntCol(label = u"Revenus d'activité imposables",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AJ",
                                   QUIFOY['conj']: u"1BJ",
                                   QUIFOY['pac1']: u"1CJ",
                                   QUIFOY['pac2']: u"1DJ",
                                   QUIFOY['pac3']: u"1EJ",
                                   })),  # (f1aj, f1bj, f1cj, f1dj, f1ej)

    ('choi', IntCol(label = u"Autres revenus imposables (chômage, préretraite)",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AP",
                                   QUIFOY['conj']: u"1BP",
                                   QUIFOY['pac1']: u"1CP",
                                   QUIFOY['pac2']: u"1DP",
                                   QUIFOY['pac3']: u"1EP",
                                   })),  # (f1ap, f1bp, f1cp, f1dp, f1ep)
    ('rsti', IntCol(label = u"Pensions, retraites, rentes connues imposables",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AS",
                                   QUIFOY['conj']: u"1BS",
                                   QUIFOY['pac1']: u"1CS",
                                   QUIFOY['pac2']: u"1DS",
                                   QUIFOY['pac3']: u"1ES",
                                   })),  # (f1as, f1bs, f1cs, f1ds, f1es)
    ('fra', IntCol(label = u"Frais réels",
                   val_type = "monetary",
                   cerfa_field = {QUIFOY['vous']: u"1AK",
                                  QUIFOY['conj']: u"1BK",
                                  QUIFOY['pac1']: u"1CK",
                                  QUIFOY['pac2']: u"1DK",
                                  QUIFOY['pac3']: u"1EK",
                                  })),  # (f1ak, f1bk, f1ck, f1dk, f1ek)

    ('alr', IntCol(label = u"Pensions alimentaires perçues",
                   val_type = "monetary",
                   cerfa_field = {QUIFOY['vous']: u"1AO",
                                  QUIFOY['conj']: u"1BO",
                                  QUIFOY['pac1']: u"1CO",
                                  QUIFOY['pac2']: u"1DO",
                                  QUIFOY['pac3']: u"1EO",
                                  })),  # (f1ao, f1bo, f1co, f1do, f1eo)
    ('alr_decl', BoolCol(label = u"Pension déclarée", default = True)),

    ('hsup', IntCol(label = u"Heures supplémentaires: revenus exonérés connus",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AU",
                                   QUIFOY['conj']: u"1BU",
                                   QUIFOY['pac1']: u"1CU",
                                   QUIFOY['pac2']: u"1DU",
                                   QUIFOY['pac3']: u"1EU",
                                   })),  # (f1au, f1bu, f1cu, f1du, f1eu)

"""pour inv, il faut que tu regardes si tu es d'accord et si c'est bien la bonne case,
   la case P exsite déjà plus bas ligne 339 sous le nom caseP  
"""
    ('inv', BoolCol(label = u'Invalide',
                    entity = 'foy',
                    cerfa_field = u'P')),  # case P

"""pour alt il faut que tu regardes si tu es d'accord et si c'est bien la bonne case, mais la case H existe déjà plus bas...
à la ligne 291 correspondrait donc à nbH
                                           
    ('alt', BoolCol(label = u'Enfant en garde alternée')),  # TODO: cerfa_field
"""
    ('alt', IntCol(label = u"Nombre d'enfants en garde alternée",
                   entity = 'foy',
                   cerfa_field = u'H')),

    ('cho_ld', BoolCol(label = u"Demandeur d'emploi inscrit depuis plus d'un an",
                       cerfa_field = {QUIFOY['vous']: u"1AI",
                                      QUIFOY['conj']: u"1BI",
                                      QUIFOY['pac1']: u"1CI",
                                      QUIFOY['pac2']: u"1DI",
                                      QUIFOY['pac3']: u"1EI",
                                   })),  # (f1ai, f1bi, f1ci, f1di, f1ei)

    ('ppe_tp_sa', BoolCol(label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière",
                          cerfa_field = {QUIFOY['vous']: u"1AX",
                                         QUIFOY['conj']: u"1BX",
                                         QUIFOY['pac1']: u"1CX",
                                         QUIFOY['pac2']: u"1DX",
                                         QUIFOY['pac3']: u"1QX",
                                         })),  # (f1ax, f1bx, f1cx, f1dx, f1qx)

    ('ppe_tp_ns', BoolCol(label = u"Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière",
                          cerfa_field = {QUIFOY['vous']: u"5NW",
                                         QUIFOY['conj']: u"5OW",
                                         QUIFOY['pac1']: u"5PW",
                                         })),  # (f5nw, f5ow, f5pw)

    ('ppe_du_sa', IntCol(label = u"Prime pour l'emploi des salariés: nombre d'heures payées dans l'année",
                         cerfa_field = {QUIFOY['vous']: u"1AV",
                                        QUIFOY['conj']: u"1BV",
                                        QUIFOY['pac1']: u"1CV",
                                        QUIFOY['pac2']: u"1DV",
                                        QUIFOY['pac3']: u"1QV",
                                        })),  # (f1av, f1bv, f1cv, f1dv, f1qv)

    ('ppe_du_ns', IntCol(label = u"Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année",
                         cerfa_field = {QUIFOY['vous']: u"5NV",
                                        QUIFOY['conj']: u"5OV",
                                        QUIFOY['pac1']: u"5PV",
                                   })),  # (f5nv, f5ov, f5pv)

    ('jour_xyz', IntCol(default = 360,
                        entity = "foy",
                        label = u"Jours décomptés au titre de cette déclaration")),

    ('age', AgesCol(label = u"Âge" , val_type = "age")),

    ('agem', AgesCol(label = u"Âge (en mois)", val_type = "months")),

    ('zone_apl', EnumCol(label = u"Zone apl",
                         entity = 'men',
                         enum = Enum([u"Non renseigné",
                                      u"Zone 1",
                                      u"Zone 2",
                                      u"Zone 3", ]), default = 2,)),

    ('loyer', IntCol(label = u"Loyer mensuel",
                     entity = 'men',
                     val_type = "monetary")),  # Loyer mensuel

    ('so', EnumCol(label = u"Statut d'occupation",
                   entity = 'men',
                   enum = Enum([u"Non renseigné",
                                u"Accédant à la propriété",
                                u"Propriétaire (non accédant) du logement",
                                u"Locataire d'un logement HLM",
                                u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
                                u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
                                u"Logé gratuitement par des parents, des amis ou l'employeur"]))),

    ('activite', EnumCol(label = u'Activité',
                         enum = Enum([u'Actif occupé',
                                    u'Chômeur',
                                    u'Étudiant, élève',
                                    u'Retraité',
                                    u'Autre inactif']), default = 4)),

    ('titc', EnumCol(label = u"Statut, pour les agents de l'Etat des collectivités locales, ou des hôpitaux",
                     enum = Enum([
                                  u"Sans objet ou non renseigné",
                                  u"Elève fonctionnaire ou stagiaire",
                                  u"Agent titulaire",
                                  u"Contractuel"]),
                     survey_only = True,
        )),

    ('statut', EnumCol(label = u"Statut détaillé mis en cohérence avec la profession",
                       enum = Enum([u"Sans objet",
                                    u"Indépendants",
                                    u"Employeurs",
                                    u"Aides familiaux",
                                    u"Intérimaires",
                                    u"Apprentis",
                                    u"CDD (hors Etat, coll.loc.), hors contrats aides",
                                    u"Stagiaires et contrats aides (hors Etat, coll.loc.)",
                                    u"Autres contrats (hors Etat, coll.loc.)",
                                    u"CDD (Etat, coll.loc.), hors contrats aides",
                                    u"Stagiaires et contrats aides (Etat, coll.loc.)",
                                    u"Autres contrats (Etat, coll.loc.)",
                                    ]),
                       survey_only = True,
                       )),

    ('txtppb', EnumCol(label = u"Taux du temps partiel",
                enum = Enum([u"Sans objet",
                            u"Moins d'un mi-temps (50%)",
                            u"Mi-temps (50%)",
                            u"Entre 50 et 80%",
                            u"80%",
                            u"Plus de 80%"]),
                       survey_only = True)),

    ('nbsala', EnumCol(label = u"Nombre de salariés dans l'établissement de l'emploi actuel",
                    enum = Enum([u"Sans objet",
                                u"Aucun salarié",
                                u"1 à 4 salariés",
                                u"5 à 9 salariés",
                                u"10 à 19 salariés",
                                u"20 à 49 salariés",
                                u"50 à 199 salariés",
                                u"200 à 499 salariés",
                                u"500 à 999 salariés",
                                u"1000 salariés ou plus",
                                u"Ne sait pas",
                                ]))),

    ('tva_ent', BoolCol(label = u"Entreprise employant le salarié paye de la TVA",
                        default = True)),

    ('chpub', EnumCol(label = u"Nature de l'employeur principal",
                      enum = Enum([u"Sans objet",
                                   u"Etat",
                                   u"Collectivités locales, HLM",
                                   u"Hôpitaux publics",
                                   u"Particulier",
                                   u"Entreprise publique (La Poste, EDF-GDF, etc.)",
                                   u"Entreprise privée, association",
                                   ]),
                      survey_only = True)),

    ('cadre', BoolCol(label = u"Cadre salarié du privé",
                      survey_only = True)),

    ('code_risque', EnumCol(label = u"Code risque pour les accidents du travail")),  # TODO: complete label and add relevant default

    ('exposition_accident', EnumCol(label = u"Exposition au risque pour les accidents du travail",
                            enum = Enum([u"Faible",
                                   u"Moyen",
                                   u"Elevé",
                                   u"Très elevé",
                                   ]))),

    ('boursier', BoolCol(label = u"Elève ou étudiant boursier")),

    ('code_postal', IntCol(label = u"Code postal du lieu de résidence",
                           entity = 'men')),

    ('statmarit', EnumCol(label = u"Statut marital",
                          default = 2,
                          enum = Enum([u"Marié",
                                    u"Célibataire",
                                    u"Divorcé",
                                    u"Veuf",
                                    u"Pacsé",
                                    u"Jeune veuf"], start = 1))),

    ('nbR', IntCol(label = u"Nombre de titulaires de la carte invalidité d'au moins 80 % (pac autre que vos enfants)",
                   entity = 'foy',
                   cerfa_field = u'R')),

    ('nbJ', IntCol(label = u"Nombre d'enfants majeurs célibataires sans enfant (pac)",
                   entity = 'foy',
                   cerfa_field = u'J')),

    ('nbI', IntCol(label = u"Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité",
                   entity = 'foy',
                   cerfa_field = u'I')),

# nbh est-il équivalent à alt ?
    ('nbH', IntCol(label = u"Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge",
                   entity = 'foy',
                   cerfa_field = u'H')),

    ('nbG', IntCol(label = u"Nombre d'enfants à charge titulaires de la carte d'invalidité",
                   entity = 'foy',
                   cerfa_field = u'G')),  # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case que l'on remplt et l'autre une case que l'on coche

    ('nbF', IntCol(label = u"Nombre d'enfants à charge  non mariés de moins de 18 ans au 1er janvier de l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge",
                   entity = 'foy',
                   cerfa_field = u'F')),

    ('nbN', IntCol(label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille",
                   entity = 'foy',
                   cerfa_field = u'N')),

    ('caseE', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul",
                      entity = 'foy',
                      cerfa_field = u'E', end = 2012)),  # à vérifier sur la nouvelle déclaration des revenus 2013

    ('caseF', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)",
                      entity = 'foy',
                      cerfa_field = u'F')),

    ('caseG', BoolCol(label = u"Titulaire d'une pension de veuve de guerre",
                      entity = 'foy',
                      cerfa_field = u'G')),  # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case que l'on remplt et l'autre une case que l'on coche

"""il ne s'agit pas à proprement parlé de la case H, les cases permettant d'indiquer l'année de naissance
   se rapportent bien à nbH mais ne sont pas nommées, choisissons nous de laisser cerfa_field = u'H' pour caseH ?
   De plus les caseH peuvent être multiples puisqu'il peut y avoir plusieurs enfants? donc faut-il les nommer caseH1, caseH2...caseH6 (les 6 présentes dans la déclaration) ?
   il faut aussi créer les cases F, G, R et I qui donnent également les années de naissances des PAC
"""
    ('caseH', IntCol(label = u"Année de naissance des enfants à charge en garde alternée",
                     entity = 'foy',
                     cerfa_field = u'H')),

    ('caseK', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre",
                      entity = 'foy',
                      cerfa_field = u'K', end = 2011)),

    ('caseL', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul",
                      entity = 'foy',
                      cerfa_field = u'L')),

    ('caseN', BoolCol(label = u"Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus",
                      entity = 'foy',
                      cerfa_field = u'N')),

    ('caseP', BoolCol(label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%",
                      entity = 'foy',
                      cerfa_field = u'P')),

    ('caseS', BoolCol(label = u"Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                      entity = 'foy',
                      cerfa_field = u'S')),

    ('caseT', BoolCol(label = u"Vous êtes parent isolé au 1er janvier de l'année de perception des revenus",
                      entity = 'foy',
                      cerfa_field = u'T')),

    ('caseW', BoolCol(label = u"Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                      entity = 'foy',
                      cerfa_field = u'W')),

    ('rfr_n_2', IntCol(entity = 'foy', label = u"Revenu fiscal de référence année n-2", val_type = "monetary")),  # TODO: provide in data
    ('nbptr_n_2', IntCol(entity = 'foy', label = u"Nombre de parts année n-2", val_type = "monetary")),  # TODO: provide in data

    # Rentes viagères
    ('f1aw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1AW')),

    ('f1bw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1BW')),

    ('f1cw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1CW')),

    ('f1dw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1DW')),

    # Gain de levée d'options
    # j'ai changé là mais pas dans le code, il faut chercher les f1uv
    # et les mettre en f1tvm comme pour sali
    # Il faut aussi le faire en amont dans les tables
""" là je ne comprends pas pourquoi il faut changer les f1uv en f1tvm....
    du coups je n'ai pas changé et j'ai fait un dico comme pour sali
"""
    ('f1tv', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans",
                            entity = 'ind',
                            val_type = "monetary",
                            cerfa_field = {QUIFOY['vous']: u"1TV",
                                           QUIFOY['conj']: u"1UV",
                                           })),  # (f1tv,f1uv)),

    ('f1tw', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans",
                            entity = 'ind',
                            val_type = "monetary",
                            cerfa_field = {QUIFOY['vous']: u"1TW",
                                           QUIFOY['conj']: u"1UW",
                                           })),  # (f1tw,f1uw)),

    ('f1tx', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans",
                            entity = 'ind',
                            val_type = "monetary",
                            cerfa_field = {QUIFOY['vous']: u"1TX",
                                           QUIFOY['conj']: u"1UX",
                            })),  # (f1tx,f1ux)),

    # RVCM
    # revenus au prélèvement libératoire
    ('f2da', IntCol(label = u"Revenus des actions et parts soumis au prélèvement libératoire de 21 %",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2DA', end = 2012)),

    ('f2dh', IntCol(label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2DH')),

    ('f2ee', IntCol(label = u"Autres produits de placement soumis aux prélèvements libératoires",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2EE')),

    # revenus des valeurs et capitaux mobiliers ouvrant droit à abattement
    ('f2dc', IntCol(entity = 'foy',
                    label = u"Revenus des actions et parts donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2DC')),

    ('f2fu', IntCol(entity = 'foy',
                    label = u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2FU')),

    ('f2ch', IntCol(entity = 'foy',
                    label = u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2CH')),

    # Revenus des valeurs et capitaux mobiliers n'ouvrant pas droit à abattement
    ('f2ts', IntCol(entity = 'foy',
                    label = u"Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans  et distributions (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2TS')),

    ('f2go', IntCol(entity = 'foy',
                    label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2GO')),

    ('f2tr', IntCol(entity = 'foy', label = u"Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2TR')),

    ('f2fa', IntCol(entity = 'foy', label = u"Produits de placements à revenu fixe inférieur à 2000 € taxable sur option à 24 % (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2FA',
                    start = 2013)),  # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013

    # Autres revenus des valeurs et capitaux mobiliers
    ('f2cg', IntCol(entity = 'foy',
                    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible",
                    val_type = "monetary",
                    cerfa_field = u'2CG')),

    ('f2bh', IntCol(entity = 'foy',
                    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible",
                    val_type = "monetary",
                    cerfa_field = u'2BH')),

    ('f2ca', IntCol(entity = 'foy',
                    label = u"Frais et charges déductibles",
                    val_type = "monetary",
                    cerfa_field = u'2CA')),

    ('f2ck', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt égal au prélèvement forfaitaire déjà versé",
                    val_type = "monetary",
                    cerfa_field = u'2CK',
                    start = 2013)),  # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013

    ('f2ab', IntCol(entity = 'foy',
                    label = u"Crédits d'impôt sur valeurs étrangères",
                    val_type = "monetary",
                    cerfa_field = u'2AB')),

    ('f2bg', IntCol(entity = 'foy',
                    label = u"Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables",
                    val_type = "monetary",
                    cerfa_field = u'2BG',
                    start = 2012)),   # TODO: vérifier existence avant 2012

    ('f2aa', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AA')),

    ('f2al', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AL')),

    ('f2am', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AM')),

    ('f2an', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AN',
                    start = 2010)),

    ('f2aq', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AQ',
                    start = 2011)),

    ('f2ar', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AR',
                    start = 2012)),
"""
je ne sais pas d'ou sort f2as...! probablement une ancienne année à laquelle je ne suis pas encore arrivé
 
"""
    ('f2as', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2012", val_type = "monetary", end = 2011)),  # TODO: vérifier existence <=2011

    ('f2dm', IntCol(entity = 'foy',
                    label = u"Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %",
                    val_type = "monetary",
                    cerfa_field = u'2DM',
                    start = 2012)),  # TODO: nouvelle case à créer où c'est nécessaire
                                    # TODO: vérifier existence avant 2012

    ('f2gr', IntCol(entity = 'foy',
                    label = u"Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)",
                    val_type = "monetary",
                    cerfa_field = u'2GR',
                    start = 2009,
                    end = 2009)),  # TODO: vérifier existence à partir de 2011

    ('f3vc', IntCol(entity = 'foy',
                    label = u"Produits et plus-values exonérés provenant de structure de capital-risque",
                    val_type = "monetary",
                    cerfa_field = u'3VC')),

    ('f3vd', IntCol(entity = 'ind',
                    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VD",
                                   QUIFOY['conj']: u"3SD",
                                   })),  # (f3vd, f3sd)

    ('f3ve', IntCol(entity = 'foy',
                    label = u"Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %",
                    val_type = "monetary",
                    cerfa_field = u'3VE')),

    ('f3vf', IntCol(entity = 'ind',
                    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VF",
                                   QUIFOY['conj']: u"3SF",
                                   })),  # (f3vf, f3sf)
"""
comment gérer les cases qui ont le même nom mais qui ne correspondent pas tout à fait à la même chose ? 
peut-ont garder le même nom et l'encadrer par des start-end ? ou avec un truc genre if sur l'année ?(pour ne pas avoir à changer le nom de la variable)
si on garde le même nom avec des start-end, et si on intégre la variable partout où elle doit être (dans les différents calculs), est-on sûr que lors des calculs les start-end seront bien pris en compte ?
ça rendra le modéle un peu moins clair parce qu'il y aura le même nom de variable pour des choses différentes et dans des calculs ne se rapportant pas aux mêmes choses, 
mais si les start-end fonctionne ça ne devrait pas avoir d'impact sur les calculs ? qu'en penses-tu ? 

    ('f3vl', IntCol(entity = 'foy', 
                    label = u"Distributions par des sociétés de capital-risque taxables à 24 %", 
                    val_type = "monetary",
                    cerfa_field = u'3VL'
                    start = 2009,
                    end = 2009)),#vérifier avant 2009
                                          
    ('f3vl', IntCol(entity = 'foy', 
                    label = u"Distributions par des sociétés de capital-risque taxables à 19 %", 
                    val_type = "monetary",
                    cerfa_field = u'3VL'
                    start = 2012,
                    end = 2013)),# vérifier pour 2011 et 2010
"""

    ('f3vi', IntCol(entity = 'ind',
                    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VI",
                                   QUIFOY['conj']: u"3SI",
                                   })),  # (f3vi, f3si )

    ('f3vm', IntCol(entity = 'foy',
                    label = u"Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %",
                    val_type = "monetary",
                    cerfa_field = u'3VM')),

    ('f3vt', IntCol(entity = 'foy',
                    label = u"Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %",
                    val_type = "monetary",
                    cerfa_field = u'3VT')),

    ('f3vj', IntCol(entity = 'ind',
                    label = u"Gains imposables sur option dans la catégorie des salaires",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VJ",
                                   QUIFOY['conj']: u"3VK",
                                   })),  # (f3vj, f3vk )

    ('f3va', IntCol(entity = 'ind',
                    label = u"Abattement pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VA",
                                   QUIFOY['conj']: u"3VB",
                                   })),  # (f3va, f3vb ))),

    # Plus values et gains taxables à des taux forfaitaires
    ('f3vg', IntCol(entity = 'foy',
                    label = u"Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés",
                    val_type = "monetary",
                    cerfa_field = u'3VG')),

    ('f3vh', IntCol(entity = 'foy',
                    label = u"Perte de l'année de perception des revenus",
                    val_type = "monetary",
                    cerfa_field = u'3VH')),

    ('f3vu', IntCol(entity = 'foy',
                    end = 2009)),  # vérifier pour 2010 et 2011

    ('f3vv', IntCol(entity = 'foy',
                    label = u"Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé ",
                    val_type = "monetary",
                    cerfa_field = u'3VV')),  # TODO: à revoir :ok pour 2013, pas de 3vv pour 2012, et correspond à autre chose en 2009, vérifier 2010 et 2011

    ('f3si', IntCol(entity = 'foy')),  # TODO: parmi ces cas créer des valeurs individuelles
                                       # correspond à autre chose en 2009, vérifier 2011,2010

    ('f3sa', IntCol(entity = 'foy', end = 2009)),  # TODO: n'existe pas en 2013 et 2012 vérifier 2011 et 2010

    ('f3sf', IntCol(entity = 'foy')),  # déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

    ('f3sd', IntCol(entity = 'foy')),  # déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

    ('f3vz', IntCol(entity = 'foy',
                    label = u"Plus-values imposables sur cessions d’immeubles ou de biens meubles",
                    val_type = "monetary",
                    cerfa_field = u'3VV',
                    start = 2011)),  # TODO: vérifier avant 2012

    # Revenus fonciers
    ('f4ba', IntCol(entity = 'foy',
                    label = u"Revenus fonciers imposables",
                    val_type = "monetary",
                    cerfa_field = u'4BA')),

    ('f4bb', IntCol(entity = 'foy',
                    label = u"Déficit imputable sur les revenus fonciers",
                    val_type = "monetary",
                    cerfa_field = u'4BB')),

    ('f4bc', IntCol(entity = 'foy',
                    label = u"Déficit imputable sur le revenu global",
                    val_type = "monetary",
                    cerfa_field = u'7BC')),

    ('f4bd', IntCol(entity = 'foy',
                    label = u"Déficits antérieurs non encore imputés",
                    val_type = "monetary",
                    cerfa_field = u'4BD')),

    ('f4be', IntCol(entity = 'foy',
                    label = u"Micro foncier: recettes brutes sans abattement",
                    val_type = "monetary",
                    cerfa_field = u'4BE')),

    # Prime d'assurance loyers impayés
    ('f4bf', IntCol(entity = 'foy',
                    label = u"Primes d'assurance pour loyers impayés des locations conventionnées",
                    val_type = "monetary",
                    cerfa_field = u'4BF')),

    ('f4bl', IntCol(entity = 'foy', label = u"", end = 2009)),  # TODO: cf 2010 2011

    ('f5qm', IntCol(entity = 'ind',
                    label = u"Agents généraux d’assurances: indemnités de cessation d’activité",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"5QM",
                                   QUIFOY['conj']: u"5RM",
                                   })),  # (f5qm, f5rm )

    # Charges et imputations diverses
    # Csg déductible
    ('f6de', IntCol(entity = 'foy',
                    label = u"CSG déductible calculée sur les revenus du patrimoine",
                    val_type = "monetary",
                    cerfa_field = u'6DE')),

    # Pensions alimentaires
    ('f6gi', IntCol(entity = 'foy',
                    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant",
                    val_type = "monetary",
                    cerfa_field = u'6GI')),

    ('f6gj', IntCol(entity = 'foy',
                    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant",
                    val_type = "monetary",
                    cerfa_field = u'6GJ')),

    ('f6el', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant",
                    val_type = "monetary",
                    cerfa_field = u'6EL')),

    ('f6em', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant",
                    val_type = "monetary",
                    cerfa_field = u'6EM')),

    ('f6gp', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)",
                    val_type = "monetary",
                    cerfa_field = u'6GP')),

    ('f6gu', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées (mineurs, ascendants)",
                    val_type = "monetary",
                    cerfa_field = u'6GU')),

    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    ('f6eu', IntCol(entity = 'foy',
                    label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin",
                    val_type = "monetary",
                    cerfa_field = u'6EU')),

    ('f6ev', IntCol(entity = 'foy',
                    label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit",
                    cerfa_field = u'6EV')),

    # Déductions diverses
    ('f6dd', IntCol(entity = 'foy',
                    label = u"Déductions diverses",
                    val_type = "monetary",
                    cerfa_field = u'6DD')),

    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    ('f6ps', IntCol(entity = 'ind',
                    label = u"Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6PS",
                                   QUIFOY['conj']: u"6PT",
                                   QUIFOY['pac1']: u"6PU",
                                   })),  # (f6ps, f6pt, f6pu)

    ('f6rs', IntCol(entity = 'ind',
                    label = u"Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6RS",
                                   QUIFOY['conj']: u"6RT",
                                   QUIFOY['pac1']: u"6RU",
                                   })),  # (f6rs, f6rt, f6ru))),

    ('f6ss', IntCol(entity = 'ind',
                    label = u"Rachat de cotisations PERP, PREFON, COREM et C.G.O.S",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6SS",
                                   QUIFOY['conj']: u"6ST",
                                   QUIFOY['pac1']: u"6SU",
                                   })),  # (f6ss, f6st, f6su))),
"""
attention pour les 4 cases suivantes, le format cerfa_field n'est pas sur 3 positions
il s'agit de la déclaration 2005 et même si effectivemnt c'est dans l'encart 6, les cases ne portent que 2 lettres, 
mettons nous 6AA ou seulement AA ? 
"""
     # Souscriptions en faveur du cinéma ou de l’audiovisuel (SOFICA)
    ('f6aa', IntCol(entity = 'foy',
                    label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel",
                    val_type = "monetary",
                    start = 2005,
                    end = 2005,
                    cerfa_field = u'AA')),  # TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)

    # Souscriptions au capital des SOFIPÊCHE
    ('f6cc', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des SOFIPÊCHE",
                    val_type = "monetary",
                    cerfa_field = u'CC',
                    start = 2005,
                    end = 2005)),  # ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)

    # Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
    # ou Versements sur un compte épargne codéveloppement
    ('f6eh', IntCol(entity = 'foy',
                    label = u"",
                    val_type = "monetary",
                    start = 2005,
                    end = 2005,
                    cerfa_field = u'EH')),  # TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)

    # Pertes en capital consécutives à la souscription au capital de sociétés
    # nouvelles ou de sociétés en difficulté
    ('f6da', IntCol(entity = 'foy',
                    label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté",
                    val_type = "monetary",
                    start = 2005,
                    end = 2005,
                    cerfa_field = u'DA')),


    # Dépenses de grosses réparations effectuées par les nus propriétaires
    ('f6cb', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)",
                    val_type = "monetary",
                    start = 2006,
                    cerfa_field = u'6CB')),  # TODO: vérifier 2011, 10, 9 ,8, 7,6, ok pou 12 et 13
                                           # TODO: before 2006 wasPertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

    ('f6hj', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'6HJ')),

    ('f6hk', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'6HK')),

    ('f6hl', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'6HL')),

    ('f6hm', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    start = 2013,
                    cerfa_field = u'6HM')),

    # Sommes à rajouter au revenu imposable
    ('f6gh', IntCol(entity = 'foy',
                    label = u"Sommes à ajouter au revenu imposable",
                    val_type = "monetary",
                    cerfa_field = u'6GH')),

    # Deficits antérieurs
    ('f6fa', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6",
                    val_type = "monetary",
                    cerfa_field = u'6FA')),

    ('f6fb', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5",
                    val_type = "monetary",
                    cerfa_field = u'6FB')),

    ('f6fc', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'6FC')),

    ('f6fd', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'6FD')),

    ('f6fe', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'6FE')),

    ('f6fl', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'6FL')),

    # Dons à des organismes établis en France
    ('f7ud', IntCol(entity = 'foy',
                    label = u"Dons à des organismes d'aide aux personnes en difficulté",
                    val_type = "monetary",
                    cerfa_field = u'7UD')),

    ('f7uf', IntCol(entity = 'foy',
                    label = u"Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général",
                    val_type = "monetary",
                    cerfa_field = u'7UF')),

    ('f7xs', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5",
                    val_type = "monetary",
                    cerfa_field = u'7XS')),

    ('f7xt', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'7XT')),

    ('f7xu', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'7XU')),

    ('f7xw', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'7XW')),

    ('f7xy', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7XY')),

    # Cotisations syndicales des salariées et pensionnés
    ('f7ac', IntCol(entity = 'ind',
                    label = u"Cotisations syndicales des salariées et pensionnés",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"7AC",
                                   QUIFOY['conj']: u"7AE",
                                   QUIFOY['pac1']: u"7AG",
                                   })),  # f7ac, f7ae, f7ag

    # Salarié à domicile
    ('f7db', IntCol(entity = 'foy',
                    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7DB')),

    ('f7df', IntCol(entity = 'foy',
                    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7DF')),

    ('f7dq', BoolCol(entity = 'foy',
                     label = u"Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés",
                     cerfa_field = u'7DQ')),

    ('f7dg', BoolCol(entity = 'foy',
                     label = u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés",
                     cerfa_field = u'7DG')),

    ('f7dl', IntCol(entity = 'foy',
                    label = u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés",
                    cerfa_field = u'7DL')),

    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    ('f7vy', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VY')),

    ('f7vz', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VZ')),

    ('f7vx', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011",
                    val_type = "monetary",
                    cerfa_field = u'7VX')),

    ('f7vw', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VW')),

    ('f7vv', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VV')),  # variable non présente dans OF, à intégrer partout où c'est nécessaire

    ('f7vu', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VU')),  # variable non présente dans OF, à intégrer partout où c'est nécessaire

    ('f7vt', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VT')),  # variable non présente dans OF, à intégrer partout où c'est nécessaire


    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    ('f7cd', IntCol(entity = 'foy',
                    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne",
                    val_type = "monetary",
                    cerfa_field = u'7CD')),

    ('f7ce', IntCol(entity = 'foy',
                    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne",
                    val_type = "monetary",
                    cerfa_field = u'7CE')),

    # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus
    ('f7ga', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GA')),

    ('f7gb', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GB')),

    ('f7gc', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GC')),

    ('f7ge', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GE')),

    ('f7gf', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GF')),

    ('f7gg', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GG')),

    # Nombre d'enfants à charge poursuivant leurs études
    ('f7ea', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études au collège",
                    cerfa_field = u'7EA')),

    ('f7eb', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège",
                    cerfa_field = u'7EB')),

    ('f7ec', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études au lycée",
                    cerfa_field = u'7EC')),

    ('f7ed', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée",
                    cerfa_field = u'7ED')),

    ('f7ef', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur",
                    cerfa_field = u'7EF')),

    ('f7eg', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur",
                    cerfa_field = u'7EG')),

    # Intérêts des prêts étudiants
    ('f7td', IntCol(entity = 'foy',
                    label = u"Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7TD')),

    ('f7vo', IntCol(entity = 'foy',
                    label = u"Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés",
                    cerfa_field = u'7VO')),

    ('f7uk', IntCol(entity = 'foy',
                    label = u"Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7UK')),

    # Primes de rente survie, contrats d'épargne handicap
    ('f7gz', IntCol(entity = 'foy',
                    label = u"Primes de rente survie, contrats d'épargne handicap",
                    val_type = "monetary",
                    cerfa_field = u'7GZ')),

    # Prestations compensatoires
    ('f7wm', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Capital fixé en substitution de rente",
                    val_type = "monetary",
                    cerfa_field = u'7WM')),

    ('f7wn', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7WN')),

    ('f7wo', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué",
                    val_type = "monetary",
                    cerfa_field = u'7WO')),

    ('f7wp', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7WP')),

    # Dépenses en faveur de la qualité environnementale de l'habitation principale
    ('f7we', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés",
                    cerfa_field = u'7WE')),

    ('f7wg', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1",
                    val_type = "monetary",
                    cerfa_field = u'7',
                    start = 2012)),  # TODO, nouvelle variable à intégrer dans OF (cf ancien nom déjà utilisé)
                                    # TODO vérifier pour les années précédentes
"""                                         
    # Intérêts d'emprunts
    ('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary", cerfa_field = u'7')), # cf pour quelle année

    ('f7wq', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées", cerfa_field = u'7')),
"""

    ('f7wt', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement ",
                    start = 2013,
                    cerfa_field = u'7WT')),  # TODO vérifier année de début

    ('f7wh', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus",
                    start = 2013,
                    cerfa_field = u'7WH')),  # TODO vérifier année de début

    ('f7wk', BoolCol(entity = 'foy',
                     label = u"Votre habitation principale est une maison individuelle",
                     cerfa_field = u'7WK')),

    ('f7wf', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1",
                    end = 2012,
                    cerfa_field = u'7WF')),  # TODO vérifier les années précédentes

    # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
    ('f7wi', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction",
                    val_type = "monetary",
                    cerfa_field = u'7WI',
                    end = 2012)),

    ('f7wj', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées",
                    val_type = "monetary",
                    cerfa_field = u'7WJ')),

    ('f7wl', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques",
                    val_type = "monetary",
                    cerfa_field = u'7WL')),

    # Investissements dans les DOM-TOM dans le cadre d'une entrepise
    ('f7ur', IntCol(entity = 'foy',
                    label = u"Investissements réalisés en n-1, total réduction d’impôt",
                    val_type = "monetary",
                    cerfa_field = u'7UR',
                    end = 2011)),  # TODO vérifier les années antérieures

    ('f7oz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6",
                    val_type = "monetary",
                    cerfa_field = u'7OZ',
                    end = 2011)),  # TODO vérifier les années antérieures

    ('f7pz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7PZ',
                    end = 2012)),  # TODO vérifier les années antérieures

    ('f7qz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7QZ',
                    end = 2012)),  # TODO vérifier les années antérieures

    ('f7rz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3",
                    val_type = "monetary",
                    cerfa_field = u'7RZ',
                    end = 2011)),  # TODO vérifier années antérieures.

"""
7sz se rapporte à des choses différentes en 2012 et 2013 par rapport aux années précédentes, cf pour les années antérieures
"""
    ('f7sz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-2",
                    val_type = "monetary",
                    cerfa_field = u'7SZ',
                    end = 2011)),  # TODO vérifier années <=2011.

    ('f7sz', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location",
                    val_type = "monetary",
                    cerfa_field = u'7SZ',
                    start = 2012)),  # TODO vérifier années <=2011

    # Aide aux créateurs et repreneurs d'entreprises
    ('f7fy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                    cerfa_field = u'7FY',
                    end = 2011)),  # TODO vérifier date <=2011

    ('f7gy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                    cerfa_field = u'7GY',
                    end = 2011)),  # TODO vérifier date <=2011

"""
7jy réutilisée en 2013 
"""
    ('f7jy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et ayant pris fin en n-1",
                    cerfa_field = u'7JY',
                    end = 2011)),

     ('f7jy', IntCol(entity = 'foy',
                    label = u"Report de 1/9 des investissements réalisés l'année de perception des revenus déclarés -3 ou -4",
                    cerfa_field = u'7JY',
                    start = 2013)),

    ('f7hy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
                    cerfa_field = u'7HY',
                    end = 2011)),  # TODO vérifier date <=2011

    ('f7ky', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1",
                    cerfa_field = u'7KY',
                    end = 2011)),  # TODO vérifier date <=2011

"""
7iy réutilisée en 2013 
"""
    ('f7iy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
                    cerfa_field = u'7IY',
                    end = 2011)),  # TODO vérifier date <=2011

    ('f7iy', IntCol(entity = 'foy',
                    label = u"Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés",
                    cerfa_field = u'7IY',
                    start = 2013)),

    ('f7ly', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                    cerfa_field = u'7LY')),  # 2012 et 2013 ok

    ('f7my', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                    cerfa_field = u'7MY')),  # 2012 et 2013 ok

    # Travaux de restauration immobilière
    ('f7ra', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager",
                    val_type = "monetary",
                    cerfa_field = u'7RA')),  # 2012 et 2013 ok

    ('f7rb', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7RB')),  # 2012 et 2013 ok

"""
f7gw et f7gx ne se rapporte pas a de l'assurance vie en 2013
"""

    # Assurance-vie
    ('f7gw', IntCol(entity = 'foy', label = u"", cerfa_field = u'7GW', end = 2011)),  # cf pour <=2011
    ('f7gx', IntCol(entity = 'foy', label = u"", cerfa_field = u'7GX', end = 2011)),  # cf pour <=2011
    # ('f7gy', IntCol()), existe ailleurs (n'existe pas en 2013 et 2012)

    ('f7gw', IntCol(entity = 'foy',
                    label = u"Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                    cerfa_field = u'7GW',
                    start = 2013)),

    ('f7gx', IntCol(entity = 'foy',
                    label = u"Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                    cerfa_field = u'7GX',
                    start = 2013)),

    # Investissements locatifs dans le secteur de touristique
    ('f7xc', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1",
                    val_type = "monetary",
                    cerfa_field = u'7XC',
                    end = 2012)),

    ('f7xd', BoolCol(entity = 'foy',
                     label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                     cerfa_field = u'7XD',
                     end = 2012)),

    ('f7xe', BoolCol(entity = 'foy',
                     label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                     cerfa_field = u'7XE',
                     end = 2012)),

    ('f7xf', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XF')),

    ('f7xh', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XH',
                    end = 2012)),

    ('f7xi', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XI')),

    ('f7xj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XJ')),

    ('f7xk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XK')),

    ('f7xl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans",
                    val_type = "monetary",
                    cerfa_field = u'7XL',
                    end = 2012)),

    ('f7xm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XM')),
"""
f7xn cf années <= à 2011 (possible erreur dans le label pour ces dates, à vérifier)
"""

     ('f7xn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: investissement réalisé en n-1",
                    val_type = "monetary",
                    cerfa_field = u'7XN',
                    end = 2011)),

    ('f7xn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XN',
                    start = 2012)),

    ('f7xo', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XO')),

    # Souscriptions au capital des PME
    ('f7cf', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion",
                    val_type = "monetary",
                    cerfa_field = u'7CF')),

    ('f7cl', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'7CL')),

    ('f7cm', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'7CM')),

    ('f7cn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'7CN')),

    ('f7cc', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7CC')),  # TODO: nouvelle variable à intégrer dans OF

    ('f7cu', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7CU')),


"""
en 2013 et 2012 plus de sofipêche (pourtant présent dans param à ces dates...), case 7gs réutilisée
"""
    # Souscription au capital d’une SOFIPECHE
    ('f7gs', IntCol(entity = 'foy',
                    label = u"Souscription au capital d’une SOFIPECHE",
                    val_type = "monetary",
                    cerfa_field = u'7GS',
                    end = 2011)),

    ('f7gs', IntCol(entity = 'foy',
                    label = u"Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7GS',
                    start = 2013)),

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
    ('f7ua', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UA', end = 2011)),  # vérifier <=2011
    ('f7ub', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UB', end = 2011)),  # vérifier <=2011
"""
en 2013 et 2012, 7uc se rapporte à autre chose, réutilisation de la case
"""
    ('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UC', end = 2011)),  # vérifier <=2011

    ('f7uc', IntCol(entity = 'foy',
                    label = u"Cotisations pour la défense des forêts contre l'incendie ",
                    val_type = "monetary",
                    cerfa_field = u'7UC',
                    start = 2012)),

    ('f7ui', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UI', end = 2011)),  # vérifier <=2011
    ('f7uj', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UJ', end = 2011)),  # vérifier <=2011
    ('f7qb', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QB', end = 2011)),  # vérifier <=2011
    ('f7qc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QC', end = 2011)),  # vérifier <=2011
    ('f7qd', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QD', end = 2011)),  # vérifier <=2011
    ('f7ql', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QL', end = 2011)),  # vérifier <=2011
    ('f7qt', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QT', end = 2011)),  # vérifier <=2011
    ('f7qm', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QM', end = 2011)),  # vérifier <=2011

    # Souscription de parts de fonds communs de placement dans l'innovation,
    # de fonds d'investissement de proximité
    ('f7gq', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds communs de placement dans l'innovation",
                    val_type = "monetary",
                    cerfa_field = u'7GQ')),

    ('f7fq', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité",
                    val_type = "monetary",
                    cerfa_field = u'7FQ')),

    ('f7fm', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse",
                    val_type = "monetary",
                    cerfa_field = u'7FM')),

    ('f7fl', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer",
                    val_type = "monetary",
                    cerfa_field = u'7FL')),
"""
Différence de % selon l'année pour le sofica, mais il se peut que cela n'ait aucun impact (si les param sont bons) puisque les cases ne changent pas
"""
    # Souscriptions au capital de SOFICA
    ('f7gn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 48 %",
                    val_type = "monetary",
                    cerfa_field = u'7GN',
                    end = 2011)),  # vérifier <=2011
    ('f7fn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 40 %",
                    val_type = "monetary",
                    cerfa_field = u'7FN',
                    end = 2011)),  # vérifier <=2011

    ('f7gn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 36 %",
                    val_type = "monetary",
                    cerfa_field = u'7GN',
                    start = 2012)),
    ('f7fn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 30 %",
                    val_type = "monetary",
                    cerfa_field = u'7FN',
                    start = 2012)),



# """
# DEBUT de ce qui reste à vérifier
# """
    # Intérêts d'emprunt pour reprise de société
    build_column_couple('f7fh', IntCol(entity = 'foy',
                    label = u"Intérêts d'emprunt pour reprise de société",
                    val_type = "monetary", cerfa_field = u'7FH')),

    # Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)),
    build_column_couple('f7ff', IntCol(entity = 'foy',
                    label = u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)",
                    val_type = "monetary",
                    cerfa_field = u'7FF')),

    build_column_couple('f7fg', IntCol(entity = 'foy',
                    label = u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations",
                    cerfa_field = u'7FG')),

    # Travaux de conservation et de restauration d’objets classés monuments historiques
    build_column_couple('f7nz', IntCol(entity = 'foy',
                    label = u"Travaux de conservation et de restauration d’objets classés monuments historiques",
                    val_type = "monetary" ,
                    cerfa_field = u'7NZ')),

    # Dépenses de protection du patrimoine naturel
    build_column_couple('f7ka', IntCol(entity = 'foy',
                    label = u"Dépenses de protection du patrimoine naturel",
                    val_type = "monetary",
                    cerfa_field = u'7KA')),

# """
# réutilisation case f7uh
# """
    # Intérêts des prêts à la consommation (case UH)),
    build_column_couple('f7uh', IntCol(entity = 'foy',
                    label = u"Intérêts des prêts à la consommation",
                    val_type = "monetary",
                    cerfa_field = u'7UH',
                    end = datetime.date(2012, 12, 1))),  # verif <=2012

    build_column_couple('f7uh', IntCol(entity = 'foy',
                    label = u"Dons et cotisations versés aux partis politiques",
                    val_type = "monetary",
                    cerfa_field = u'7UH',
                    start = datetime.date(2013, 1, 1))),

    # Investissements forestiers
    build_column_couple('f7un', IntCol(entity = 'foy',
                    label = u"Investissements forestiers: acquisition",
                    val_type = "monetary",
                    cerfa_field = u'7UN')),

    # Intérêts pour paiement différé accordé aux agriculteurs
    build_column_couple('f7um', IntCol(entity = 'foy',
                    label = u"Intérêts pour paiement différé accordé aux agriculteurs",
                    val_type = "monetary",
                    cerfa_field = u'7UM')),

    # Investissements locatifs neufs : Dispositif Scellier:
    build_column_couple('f7hj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole",
                    val_type = "monetary",
                    cerfa_field = u'7HJ')),

    build_column_couple('f7hk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM",
                    val_type = "monetary",
                    cerfa_field = u'7HK')),

    build_column_couple('f7hn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010",
                    val_type = "monetary",
                    cerfa_field = u'7HN')),

    build_column_couple('f7ho', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010",
                    val_type = "monetary",
                    cerfa_field = u'7HO')),

    build_column_couple('f7hl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)",
                    val_type = "monetary",
                    cerfa_field = u'7HL')),

    build_column_couple('f7hm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds",
                    val_type = "monetary",
                    cerfa_field = u'7HM')),

    build_column_couple('f7hr', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 (métropole et DOM ne respectant pas les plafonds): report de 1/9 de l'investissement",
                    val_type = "monetary",
                    cerfa_field = u'7HR')),

    build_column_couple('f7hs', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM et respectant les plafonds: report de 1/9 de l'investissement",
                    val_type = "monetary",
                    cerfa_field = u'7HS')),

    build_column_couple('f7la', IntCol(entity = 'foy',
                    label = u"Investissements locatifs neufs dispositif Scellier: report du solde de réduction d'impôt non encore imputé",
                    val_type = "monetary",
                    cerfa_field = u'7LA')),

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    build_column_couple('f7ij', IntCol(entity = 'foy',
                    label = u"Investissement destinés à la location meublée non professionnelle: engagement de réalisation de l'investissement en 2011",
                    val_type = "monetary",
                    cerfa_field = u'7IJ')),

    build_column_couple('f7il', IntCol(entity = 'foy',
                    label = u"Investissement destinés à la location meublée non professionnelle: promesse d'achat en 2010",
                    val_type = "monetary",
                    cerfa_field = u'7IL')),

    build_column_couple('f7im', IntCol(entity = 'foy',
                    label = u"Investissement destinés à la location meublée non professionnelle: investissement réalisés en 2010 avec promesse d'achat en 2009",
                    val_type = "monetary",
                    cerfa_field = u'7IM')),

    build_column_couple('f7ik', IntCol(entity = 'foy',
                    label = u"Reports de 1/9 de l'investissement réalisé et achevé en 2009",
                    val_type = "monetary",
                    cerfa_field = u'7IK')),

    build_column_couple('f7is', IntCol(entity = 'foy',
                    label = u"Report du solde de réduction d'impôt non encore imputé: année  n-4",
                    val_type = "monetary",
                    cerfa_field = u'7IS')),

    # Investissements locatifs dans les résidences de tourisme situées dans une zone de
    # revitalisation rurale

# """
# réutilisation de cases en 2013
# """
    build_column_couple('f7gt', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans les résidences de tourisme situées dans une zone de revitalisation rurale",
                    val_type = "monetary",
                    cerfa_field = u'7GT',
                    end = datetime.date(2012, 12, 1))),  # vérif <=2012

    build_column_couple('f7gt', IntCol(entity = 'foy',
                    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010",
                    val_type = "monetary",
                    cerfa_field = u'7GT',
                    start = datetime.date(2013, 1, 1))),  # vérif <=2012

    build_column_couple('f7gu', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans les résidences de tourisme situées dans une zone de revitalisation rurale",
                    val_type = "monetary",
                    cerfa_field = u'7GU',
                    end = datetime.date(2012, 12, 1))),  # vérif <=2012

    build_column_couple('f7gu', IntCol(entity = 'foy',
                    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009",
                    val_type = "monetary",
                    cerfa_field = u'7GU',
                    start = datetime.date(2013, 1, 1))),  # vérif <=2012

    build_column_couple('f7gv', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans les résidences de tourisme situées dans une zone de revitalisation rurale",
                    val_type = "monetary",
                    cerfa_field = u'7GV',
                    end = datetime.date(2012, 12, 1))),  # vérif <=2012

    build_column_couple('f7gv', IntCol(entity = 'foy',
                    label = u"Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna ",
                    val_type = "monetary",
                    cerfa_field = u'7GV',
                    start = datetime.date(2013, 1, 1))),  # vérif <=2012

    build_column_couple('f7xg', IntCol(entity = 'foy', label = u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XG',
                    end = datetime.date(2012, 12, 1))),  # vérif <=2012

    # Avoir fiscaux et crédits d'impôt
    # f2ab déjà disponible
    build_column_couple('f8ta', IntCol(entity = 'foy',
                    label = u"Retenue à la source en France ou impôt payé à l'étranger",
                    val_type = "monetary",
                    cerfa_field = u'8TA')),

    build_column_couple('f8tb', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)",  # TODO: différence de label entre les années à voir
                    val_type = "monetary",
                    cerfa_field = u'8TB')),

    build_column_couple('f8tf', IntCol(entity = 'foy',
                    label = u"Reprises de réductions ou de crédits d'impôt",
                    val_type = "monetary",
                    cerfa_field = u'8TF')),

    build_column_couple('f8tg', IntCol(entity = 'foy',
                    label = u"Crédits d'impôt en faveur des entreprises: Investissement en Corse",
                    val_type = "monetary",
                    cerfa_field = u'8TG')),

    build_column_couple('f8th', IntCol(entity = 'foy',
                    label = u"Retenue à la source élus locaux",
                    val_type = "monetary",
                    cerfa_field = u'8TH')),

    build_column_couple('f8tc', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))",  # différence de label entre les années à voir
                    val_type = "monetary",
                    cerfa_field = u'8TC')),

    build_column_couple('f8td', IntCol(entity = 'foy',
                    label = u"Contribution exceptionnelle sur les hauts revenus",
                    cerfa_field = u'8TD')),

    build_column_couple('f8te', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé",
                    val_type = "monetary",
                    cerfa_field = u'8TE')),

    build_column_couple('f8to', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'8TO')),

    build_column_couple('f8tp', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt",
                    val_type = "monetary",
                    cerfa_field = u'8TP')),

    build_column_couple('f8uz', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Famille",
                    val_type = "monetary",
                    cerfa_field = u'8UZ')),

    build_column_couple('f8tz', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Apprentissage",
                    val_type = "monetary",
                    cerfa_field = u'8TZ')),

    build_column_couple('f8wa', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Agriculture biologique",
                    val_type = "monetary",
                    cerfa_field = u'8WA')),

    build_column_couple('f8wb', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Prospection commerciale",
                    val_type = "monetary",
                    cerfa_field = u'8WB')),
# """
# réutilisation f8wc
# """
    build_column_couple('f8wc', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Nouvelles technologies",
                    val_type = "monetary",
                    cerfa_field = u'8WC',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f8wc', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Prêts sans intérêt",
                    val_type = "monetary",
                    cerfa_field = u'8WC',
                    start = datetime.date(2013, 1, 1))),

    build_column_couple('f8wd', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise",
                    val_type = "monetary",
                    cerfa_field = u'8WD')),

    build_column_couple('f8we', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Intéressement",
                    val_type = "monetary",
                    cerfa_field = u'8WE')),

    build_column_couple('f8wr', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Métiers d'art",
                    val_type = "monetary",
                    cerfa_field = u'8WR')),

    build_column_couple('f8ws', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes",
                    val_type = "monetary",
                    cerfa_field = u'8WS',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f8wt', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs",
                    val_type = "monetary",
                    cerfa_field = u'8WT')),

    build_column_couple('f8wu', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Maître restaurateur",
                    val_type = "monetary",
                    cerfa_field = u'8WU')),

    build_column_couple('f8wv', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Débitants de tabac",
                    val_type = "monetary",
                    cerfa_field = u'8WV',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f8wx', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise",
                    val_type = "monetary",
                    cerfa_field = u'8WX',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f8wy', IntCol(entity = 'foy',
                    label = u"",
                    val_type = "monetary",
                    cerfa_field = u'8WY',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    # Acquisition de biens culturels
    build_column_couple('f7uo', IntCol(entity = 'foy',
                    label = u"Acquisition de biens culturels",
                    val_type = "monetary",
                    cerfa_field = u'7UO')),

    # Mécénat d'entreprise
    build_column_couple('f7us', IntCol(entity = 'foy',
                    label = u"Réduction d'impôt mécénat d'entreprise",
                    val_type = "monetary",
                    cerfa_field = u'7US')),

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    # ('f7wf', IntCol() déjà disponible
    # ('f7wh', IntCol() déjà disponible
    # ('f7wk', IntCol() déjà disponible
    # ('f7wq', IntCol() déjà disponible

    build_column_couple('f7sb', IntCol(entity = 'foy',
                   label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %",
                   val_type = "monetary",
                   cerfa_field = u'7SB',
                   end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f7sc', IntCol(entity = 'foy',
                   label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale",
                   val_type = "monetary",
                   cerfa_field = u'7SC',
                   end = datetime.date(2012, 12, 1))),  # verif<=2012

# """
# réutilisation de case pour 2013
# """

    build_column_couple('f7sd', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 40 %",
                    val_type = "monetary",
                    cerfa_field = u'7SD',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f7sd', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation",
                    val_type = "monetary",
                    cerfa_field = u'7SD',
                    start = datetime.date(2013, 1, 1))),  # verif<=2012 et vérifier autres prog comportant f7sd

    build_column_couple('f7se', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 50 %",
                    val_type = "monetary",
                    cerfa_field = u'7SE',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f7se', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz",
                    val_type = "monetary",
                    cerfa_field = u'7SE',
                    start = datetime.date(2013, 1, 1))),  # verif<=2012

    build_column_couple('f7sh', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 15 %",
                    val_type = "monetary",
                    cerfa_field = u'7SH',
                    end = datetime.date(2012, 12, 1))),  # verif<=2012

    build_column_couple('f7sh', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)",
                    val_type = "monetary",
                    cerfa_field = u'7SH',
                    start = datetime.date(2013, 1, 1))),  # verif<=2012

    # ('f7wg', IntCol() déjà disponible

# """
# réutilisation en 2013 de f7up et f7uq
# """
    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???
    # build_column_couple('f7up', IntCol(entity = 'foy',
    #                 label = u"Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ",
    #                 val_type = "monetary",
    #                 cerfa_field = u'7UP',
    #                 end = datetime.date(2007, 12, 1))),  # TODO: vérif date de fin

    build_column_couple('f7up', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt pour investissements forestiers: travaux",
                    val_type = "monetary",
                    cerfa_field = u'7UP',
                    start = datetime.date(2008, 1, 1))),  # TODO: vérif date début, ok pour 13

    build_column_couple('f7uq', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL",
                    val_type = "monetary",
                    cerfa_field = u'7UQ',
                    end = datetime.date(2007, 12, 1))),  # TODO: vérif date de fin

    build_column_couple('f7uq', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt pour investissements forestiers: contrat de gestion",
                    val_type = "monetary",
                    cerfa_field = u'7UQ',
                    start = datetime.date(2008, 1, 1))),  # TODO: vérif date début, ok pour 13

    # Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
    build_column_couple('f1ar', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1AR',
                    end = datetime.date(2012, 12, 1))),  # TODO: vérifier <=2012

    build_column_couple('f1br', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1BR',
                    end = datetime.date(2012, 12, 1))),  # TODO: vérifier <=2012

    build_column_couple('f1cr', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1CR',
                    end = datetime.date(2012, 12, 1))),  # TODO: vérifier <=2012

    build_column_couple('f1dr', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1DR',
                    end = datetime.date(2012, 12, 1))),  # TODO: vérifier <=2012

    build_column_couple('f1er', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt aide à la mobilité",
                    cerfa_field = u'1ER',p
                    end = datetime.date(2012, 12, 1))),  # TODO: vérifier <=2012

    # Crédit d’impôt directive « épargne » (case 2BG)),
    build_column_couple('f2bg', IntCol(entity = 'foy',
                    label = u"Crédit d’impôt directive « épargne »",
                    val_type = "monetary",
                    cerfa_field = u'2BG')),!

    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    build_column_couple('f4tq', IntCol(entity = 'foy',
                    label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail",
                    val_type = "monetary",
                    cerfa_field = u'4TQ')),  # vérif libéllé, en 2013=Montant des loyers courus du 01/01/1998 au 30/09/1998 provenant des immeubles
                                           # pour lesquels la cessation ou l'interruption de la location est intervenue en 2013 et qui ont été
                                           # soumis à la taxe additionnelle au droit de bail

    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    # f7wf
    # f7wi
    # f7wj
    # f7wl
    build_column_couple('f7sf', IntCol(entity = 'foy',
                    label = u"Appareils de régulation du chauffage, matériaux de calorifugeage",
                    val_type = "monetary",
                    cerfa_field = u'7SF')),

    build_column_couple('f7si', IntCol(entity = 'foy',
                    label = u"Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)",
                    val_type = "monetary",
                    cerfa_field = u'7SI')),

    # Auto-entrepreneur : versements libératoires d’impôt sur le revenu
    build_column_couple('f8uy', IntCol(entity = 'foy',
                    label = u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé",
                    val_type = "monetary",
                    cerfa_field = u'8uy')),

    # Revenus des professions non salariées

    build_column_couple('frag_exon', IntCol(entity = 'ind', label = u"Revenus agricoles exonérés (régime du forfait)", val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HN",
                                        QUIFOY['conj']: u"5IN",
                                        QUIFOY['pac1']: u"5JN", })),  # (f5hn, f5in, f5jn)),

    build_column_couple('frag_impo', IntCol(entity = 'ind',
                         label = u"Revenus agricoles imposables (régime du forfait)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HO",
                                        QUIFOY['conj']: u"5IO",
                                        QUIFOY['pac1']: u"5JO", })),  # (f5ho, f5io, f5jo)),

    build_column_couple('arag_exon', IntCol(entity = 'ind',
                         label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HB",
                                        QUIFOY['conj']: u"5IB",
                                        QUIFOY['pac1']: u"5JB", })),  # (f5hb, f5ib, f5jb)),

    build_column_couple('arag_impg', IntCol(entity = 'ind',
                         label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HC",
                                        QUIFOY['conj']: u"5IC",
                                        QUIFOY['pac1']: u"5JC", })),  # (f5hc, f5ic, f5jc)),

    build_column_couple('arag_defi', IntCol(entity = 'ind',
                         label = u"Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HF",
                                        QUIFOY['conj']: u"5IF",
                                        QUIFOY['pac1']: u"5JF", })),  # (f5hf, f5if, f5jf)),

    build_column_couple('nrag_exon', IntCol(entity = 'ind',
                         label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HH",
                                        QUIFOY['conj']: u"5IH",
                                        QUIFOY['pac1']: u"5JH", })),  # (f5hh, f5ih, f5jh)),

    build_column_couple('nrag_impg', IntCol(entity = 'ind',
                         label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HI",
                                        QUIFOY['conj']: u"5II",
                                        QUIFOY['pac1']: u"5JI", })),  # (f5hi, f5ii, f5ji)),

    build_column_couple('nrag_defi', IntCol(entity = 'ind',
                         label = u"Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HL",
                                        QUIFOY['conj']: u"5IL",
                                        QUIFOY['pac1']: u"5JL", })),  # (f5hl, f5il, f5jl)),

    build_column_couple('nrag_ajag', IntCol(entity = 'ind',
                         label = u"Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HM",
                                        QUIFOY['conj']: u"5IM",
                                        QUIFOY['pac1']: u"5JM", })),  # (f5hm, f5im, f5jm)),

    # Autoentrepreneur
    build_column_couple('ebic_impv', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5TA",
                                        QUIFOY['conj']: u"5UA",
                                        QUIFOY['pac1']: u"5VA", })),  # (f5ta, f5ua, f5va)),

    build_column_couple('ebic_imps', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5TB",
                                        QUIFOY['conj']: u"5UB",
                                        QUIFOY['pac1']: u"5VB", })),  # (f5tb, f5ub, f5vb)),

    build_column_couple('ebnc_impo', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux imposables (régime auto-entrepreneur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5TE",
                                        QUIFOY['conj']: u"5UE",
                                        QUIFOY['pac1']: u"5VE", })),  # (f5te, f5ue, f5ve)),

    build_column_couple('mbic_exon', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KN",
                                        QUIFOY['conj']: u"5LN",
                                        QUIFOY['pac1']: u"5MN", })),  # (f5kn, f5ln, f5mn)),

    build_column_couple('abic_exon', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KB",
                                        QUIFOY['conj']: u"5LB",
                                        QUIFOY['pac1']: u"5MB", })),  # (f5kb, f5lb, f5mb)),

    build_column_couple('nbic_exon', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KH",
                                        QUIFOY['conj']: u"5LH",
                                        QUIFOY['pac1']: u"5MH", })),  # (f5kh, f5lh, f5mh)),

    build_column_couple('mbic_impv', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KO",
                                        QUIFOY['conj']: u"5LO",
                                        QUIFOY['pac1']: u"5MO", })),  # (f5ko, f5lo, f5mo)),

    build_column_couple('mbic_imps', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KP",
                                        QUIFOY['conj']: u"5LP",
                                        QUIFOY['pac1']: u"5MP", })),  # (f5kp, f5lp, f5mp)),

    build_column_couple('abic_impn', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                          val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KC",
                                        QUIFOY['conj']: u"5LC",
                                        QUIFOY['pac1']: u"5MC", })),  # (f5kc, f5lc, f5mc)),

    build_column_couple('abic_imps', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KD",
                                        QUIFOY['conj']: u"5LD",
                                        QUIFOY['pac1']: u"5MD", },
                         end = datetime.date(2012, 12, 1))),  # (f5kd, f5ld, f5md)),
                                                              # TODO: vérifier date fin

    build_column_couple('nbic_impn', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KI",
                                        QUIFOY['conj']: u"5LI",
                                        QUIFOY['pac1']: u"5MI", }
                         )),  # (f5ki, f5li, f5mi)),

# """
# réutilisation cases 2013
# """
    build_column_couple('nbic_imps', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux imposables: régime simplifié sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KJ",
                                        QUIFOY['conj']: u"5LJ",
                                        QUIFOY['pac1']: u"5MJ", },
                         end = datetime.date(2012, 12, 1))),  # (f5kj, f5lj, f5mj)),
                                                              # TODO: vérifier date fin
    build_column_couple('nbic_mvct', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux moins-values nettes à court terme",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KJ",
                                        QUIFOY['conj']: u"5LJ",
                                        QUIFOY['pac1']: u"5MJ", },
                         start = datetime.date(2013, 1, 1))),  # (f5kj, f5lj, f5mj)),
                                                              # vérifier date début #####à intégrer dans OF#######

    build_column_couple('abic_defn', IntCol(entity = 'ind',
                         label = u"Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KF",
                                        QUIFOY['conj']: u"5LF",
                                        QUIFOY['pac1']: u"5MF", })),  # (f5kf, f5lf, f5mf)),

    build_column_couple('abic_defs', IntCol(entity = 'ind',
                         label = u"Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KG",
                                        QUIFOY['conj']: u"5LG",
                                        QUIFOY['pac1']: u"5MG", },
                         end = datetime.date(2012, 12, 1))),  # (f5kg, f5lg, f5mg)),
                                                              # vérif <=2012

    build_column_couple('nbic_defn', IntCol(entity = 'ind',
                         label = u"Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KL",
                                        QUIFOY['conj']: u"5LL",
                                        QUIFOY['pac1']: u"5ML", })),  # (f5kl, f5ll, f5ml)),

    build_column_couple('nbic_defs', IntCol(entity = 'ind',
                         label = u"Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KL",
                                        QUIFOY['conj']: u"5LM",
                                        QUIFOY['pac1']: u"5MM", })),  # (f5km, f5lm, f5mm)),

    build_column_couple('nbic_apch', IntCol(entity = 'ind',
                         label = u"Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KS",
                                        QUIFOY['conj']: u"5LS",
                                        QUIFOY['pac1']: u"5MS", })),  # (f5ks, f5ls, f5ms)),

    build_column_couple('macc_exon', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NN",
                                        QUIFOY['conj']: u"5ON",
                                        QUIFOY['pac1']: u"5PN", })),  # (f5nn, f5on, f5pn)),

    build_column_couple('aacc_exon', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NB",
                                        QUIFOY['conj']: u"5OB",
                                        QUIFOY['pac1']: u"5PB", })),  # (f5nb, f5ob, f5pb)),

    build_column_couple('nacc_exon', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NH",
                                        QUIFOY['conj']: u"5OH",
                                        QUIFOY['pac1']: u"5PH", })),  # (f5nh, f5oh, f5ph)),

    build_column_couple('macc_impv', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NO",
                                        QUIFOY['conj']: u"5OO",
                                        QUIFOY['pac1']: u"5PO", })),  # (f5no, f5oo, f5po)),

    build_column_couple('macc_imps', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NP",
                                        QUIFOY['conj']: u"5OP",
                                        QUIFOY['pac1']: u"5PP", })),  # (f5np, f5op, f5pp)),

    build_column_couple('aacc_impn', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NC",
                                        QUIFOY['conj']: u"5OC",
                                        QUIFOY['pac1']: u"5PC", })),  # (f5nc, f5oc, f5pc)),

    build_column_couple('aacc_imps', IntCol(entity = 'ind',
                         label = u"Locations meublées non professionnelles (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5ND",
                                        QUIFOY['conj']: u"5OD",
                                        QUIFOY['pac1']: u"5PD", })),  # (f5nd, f5od, f5pd)),

    build_column_couple('aacc_defn', IntCol(entity = 'ind',
                         label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NF",
                                        QUIFOY['conj']: u"5OF",
                                        QUIFOY['pac1']: u"5PF", })),  # (f5nf, f5of, f5pf)),

    build_column_couple('aacc_defs', IntCol(entity = 'ind',
                         label = u"Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NG",
                                        QUIFOY['conj']: u"5OG",
                                        QUIFOY['pac1']: u"5PG", })),  # (f5ng, f5og, f5pg)),

    build_column_couple('nacc_impn', IntCol(entity = 'ind',
                         label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NI",
                                        QUIFOY['conj']: u"5OI",
                                        QUIFOY['pac1']: u"5PI", })),  # (f5ni, f5oi, f5pi)),

    build_column_couple('nacc_imps', IntCol(entity = 'ind',
                         label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NJ",
                                        QUIFOY['conj']: u"5OJ",
                                        QUIFOY['pac1']: u"5PJ", })),  # (f5nj, f5oj, f5pj)),

    build_column_couple('nacc_defn', IntCol(entity = 'ind',
                         label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NL",
                                        QUIFOY['conj']: u"5OL",
                                        QUIFOY['pac1']: u"5PL", })),  # (f5nl, f5ol, f5pl)),

    build_column_couple('nacc_defs', IntCol(entity = 'ind',
                         label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NM",
                                        QUIFOY['conj']: u"5OM",
                                        QUIFOY['pac1']: u"5PM", })),  # (f5nm, f5om, f5pm)),

    build_column_couple('mncn_impo', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KU",
                                        QUIFOY['conj']: u"5LU",
                                        QUIFOY['pac1']: u"5MU", })),  # (f5ku, f5lu, f5mu)),

    build_column_couple('cncn_bene', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5SN",
                                        QUIFOY['conj']: u"5NS",
                                        QUIFOY['pac1']: u"5OS", })),  # (f5sn, f5ns, f5os)),

    build_column_couple('cncn_defi', IntCol(entity = 'ind',
                         label = u"Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5SP",
                                        QUIFOY['conj']: u"5NU",
                                        QUIFOY['pac1']: u"5OU", })),  # (f5sp, f5nu, f5ou, f5sr)),
                                                                      # pas de f5sr en 2013

    build_column_couple('mbnc_exon', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HP",
                                        QUIFOY['conj']: u"5IP",
                                        QUIFOY['pac1']: u"5JP", })),  # (f5hp, f5ip, f5jp)),

    build_column_couple('abnc_exon', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QB",
                                        QUIFOY['conj']: u"5RB",
                                        QUIFOY['pac1']: u"5SB", })),  # (f5qb, f5rb, f5sb)),

    build_column_couple('nbnc_exon', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QH",
                                        QUIFOY['conj']: u"5RH",
                                        QUIFOY['pac1']: u"5SH", })),  # (f5qh, f5rh, f5sh)),

    build_column_couple('mbnc_impo', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HQ",
                                        QUIFOY['conj']: u"5IQ",
                                        QUIFOY['pac1']: u"5JQ", })),  # (f5hq, f5iq, f5jq)),

    build_column_couple('abnc_impo', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QC",
                                        QUIFOY['conj']: u"5RC",
                                        QUIFOY['pac1']: u"5SC", })),  # (f5qc, f5rc, f5sc)),

    build_column_couple('abnc_defi', IntCol(entity = 'ind',
                         label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QE",
                                        QUIFOY['conj']: u"5RE",
                                        QUIFOY['pac1']: u"5SE", })),  # (f5qe, f5re, f5se)),

    build_column_couple('nbnc_impo', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QI",
                                        QUIFOY['conj']: u"5RI",
                                        QUIFOY['pac1']: u"5SI", })),  # (f5qi, f5ri, f5si)),

    build_column_couple('nbnc_defi', IntCol(entity = 'ind',
                         label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QK",
                                        QUIFOY['conj']: u"5RK",
                                        QUIFOY['pac1']: u"5SK", })),  # (f5qk, f5rk, f5sk)),

    build_column_couple('mbic_mvct', IntCol(entity = 'foy',
                         label = u"Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = u'5HU',
                         end = datetime.date(2012, 12, 1))),  # (f5hu)),
                                                              # vérif <=2012

    build_column_couple('macc_mvct', IntCol(entity = 'foy', label = u"Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = u'5IU')),  # (f5iu)),

    build_column_couple('mncn_mvct', IntCol(entity = 'foy',
                         label = u"Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = u'JU')),  # (f5ju)),

    build_column_couple('mbnc_mvct', IntCol(entity = 'foy', label = u"Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KZ",
                                        QUIFOY['conj']: u"5LZ",
                                        QUIFOY['pac1']: u"5MZ", })),  # (f5kz, f5lz , f5mz), f5lz , f5mz sont présentent en 2013
                                                                      # TODO: intégrer f5lz , f5mz à OF

    build_column_couple('frag_pvct', IntCol(entity = 'ind',
                         label = u"Plus-values agricoles  à court terme (régime du forfait)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HW",
                                        QUIFOY['conj']: u"5IW",
                                        QUIFOY['pac1']: u"5JW", })),  # (f5hw, f5iw, f5jw)),

    build_column_couple('mbic_pvct', IntCol(entity = 'ind',
                         label = u"Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KX",
                                        QUIFOY['conj']: u"5LX",
                                        QUIFOY['pac1']: u"5MX", })),  # (f5kx, f5lx, f5mx)),

    build_column_couple('macc_pvct', IntCol(entity = 'ind',
                         label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NX",
                                        QUIFOY['conj']: u"5OX",
                                        QUIFOY['pac1']: u"5PX", })),  # (f5nx, f5ox, f5px)),

    build_column_couple('mbnc_pvct', IntCol(entity = 'ind',
                         label = u"Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)",
                          val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HV",
                                        QUIFOY['conj']: u"5IV",
                                        QUIFOY['pac1']: u"5JV", })),  # (f5hv, f5iv, f5jv)),

    build_column_couple('mncn_pvct', IntCol(entity = 'ind',
                         label = u"Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KY",
                                        QUIFOY['conj']: u"5LY",
                                        QUIFOY['pac1']: u"5MY", })),  # (f5ky, f5ly, f5my)),

    build_column_couple('mbic_mvlt', IntCol(entity = 'ind',
                         label = u"Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KR",
                                        QUIFOY['conj']: u"5LR",
                                        QUIFOY['pac1']: u"5MR", })),  # (f5kr, f5lr, f5mr)),

    build_column_couple('macc_mvlt', IntCol(entity = 'ind',
                         label = u"Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NR",
                                        QUIFOY['conj']: u"5OR",
                                        QUIFOY['pac1']: u"5PR", })),  # (f5nr, f5or, f5pr)),

    build_column_couple('mncn_mvlt', IntCol(entity = 'ind',
                         label = u"Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KW",
                                        QUIFOY['conj']: u"5LW",
                                        QUIFOY['pac1']: u"5MW", })),  # (f5kw, f5lw, f5mw)),

    build_column_couple('mbnc_mvlt', IntCol(entity = 'ind',
                         label = u"Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HS",
                                        QUIFOY['conj']: u"5IS",
                                        QUIFOY['pac1']: u"5JS", })),  # (f5hs, f5is, f5js)),

    build_column_couple('frag_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values agricoles de cession taxables à 16% (régime du forfait)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HX",
                                        QUIFOY['conj']: u"5IX",
                                        QUIFOY['pac1']: u"5JX", })),  # (f5hx, f5ix, f5jx)),

    build_column_couple('arag_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HE",
                                        QUIFOY['conj']: u"5IE",
                                        QUIFOY['pac1']: u"5JE", })),  # (f5he, f5ie, f5je)),

    build_column_couple('nrag_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HK",
                                        QUIFOY['conj']: u"5LK",
                                        QUIFOY['pac1']: u"5JK", },
                         end = datetime.date(2012, 12, 1))),  # TODO: vérif <=2012)),  # (f5hk, f5lk, f5jk)),

    build_column_couple('mbic_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KQ",
                                        QUIFOY['conj']: u"5LQ",
                                        QUIFOY['pac1']: u"5MQ", })),  # (f5kq, f5lq, f5mq)),

    build_column_couple('abic_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KE",
                                        QUIFOY['conj']: u"5LE",
                                        QUIFOY['pac1']: u"5ME", })),  # (f5ke, f5le, f5me)),

    build_column_couple('nbic_pvce', IntCol(entity = 'ind',
                         label = u"Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5IK",
                                        QUIFOY['conj']: u"5KK",
                                        QUIFOY['pac1']: u"5MK", })),  # (f5kk, f5ik, f5mk)),

    build_column_couple('macc_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NQ",
                                        QUIFOY['conj']: u"5OQ",
                                        QUIFOY['pac1']: u"5PQ", })),  # (f5nq, f5oq, f5pq)),

    build_column_couple('aacc_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NE",
                                        QUIFOY['conj']: u"5OE",
                                        QUIFOY['pac1']: u"5PE", })),  # (f5ne, f5oe, f5pe)),

    build_column_couple('nacc_pvce', IntCol(entity = 'ind',
                         label = u"Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5NK",
                                        QUIFOY['conj']: u"5OK",
                                        QUIFOY['pac1']: u"5PK", })),  # (f5nk, f5ok, f5pk)),

    build_column_couple('mncn_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5KV",
                                        QUIFOY['conj']: u"5LV",
                                        QUIFOY['pac1']: u"5MV", })),  # (f5kv, f5lv, f5mv)),

    build_column_couple('cncn_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5SO",
                                        QUIFOY['conj']: u"5NT",
                                        QUIFOY['pac1']: u"5OT", })),  # (f5so, f5nt, f5ot)),

    build_column_couple('mbnc_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5HR",
                                        QUIFOY['conj']: u"5IR",
                                        QUIFOY['pac1']: u"5JR", })),  # (f5hr, f5ir, f5jr)),

    build_column_couple('abnc_pvce', IntCol(entity = 'ind',
                         label = u"Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QD",
                                        QUIFOY['conj']: u"5RD",
                                        QUIFOY['pac1']: u"5SD", })),  # (f5qd, f5rd, f5sd)),

    build_column_couple('nbnc_pvce', IntCol(entity = 'ind',
                         label = u"Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)",
                         val_type = "monetary",
                         cerfa_field = {QUIFOY['vous']: u"5QJ",
                                        QUIFOY['conj']: u"5RJ",
                                        QUIFOY['pac1']: u"5SJ", })),  # (f5qj, f5rj, f5sj)),

"""
CASES MANQUANTES PRESENTENT DANS LA DECLARATION DES REVENUS 2013
"""
# A CREER ET A INTEGRER DANS OF

"""
### VOS REVENUS

#revenu de solidarité active
pour le foyer:1BL
1ere PAC: 1CB
2ème PAC: 1DQ

#pensions, retraites, rentes, rentes viagères à titre onéreux
Pensions de retraite en capital taxables à 7.5%
vous:1AT
conj:1BT

#gains de levée d'options, revenus éxonérés ou non imposables en France, revenus exceptionnels ou différés
    #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 28/9/2012
    imposables en salaires:
    vous:1TT
    conj:1UT

    #gains et distributions provenant de parts ou actions de carried-interest, déclarés cases 1AJ ou 1BJ, soumis à la contribution salariale de 30 %
    vous:1NY
    conj:1OY
    
    #agents d'assurance: salaires éxonérés
    vous:1AQ
    conj:1BQ
    
    #salariés impatriés: salaires et primes éxonérés
    vous:1DY
    conj:1EY
    
    #salaires imposables à l'étranger, non déclarés cases 1Aj ou 1BJ, retenus pour le calcul de la prime pour l'emploi
    vous:1LZ
    conj:1MZ
    
    #sommes éxonérées transférées du CET au PERCO ou à un régime supplémentaire d'entreprise
    vous: 1SM
    conj:1DN
    
#salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif
(n'indiquez pas ces revenus ligne 8TI (2042) ni ligne 1LZ et 1MZ).
    
    #total de vos salaires
    vous:1AC
    conj:1BC
    pac1:1CC 
    pac2:1DC
    
    #montant de l'impôt acquitté à l'étranger
    vous:1AD
    conj:1BD
    pac1:1CD 
    pac2:1DD

    #frais rééls
    vous:1AE
    conj:1BE
    pac1:1CE
    pac2:1DE

    #pour recevoir la PPE: activité à temps plein exercée à l'étranger toute l'année
    vous:1AX
    conj:1BX
    pac1:1CX 
    pac2:1DX

    #pour recevoir la PPE: sinon, nombre d'heures payées dans l'année
    vous:1AG
    conj:1BG
    pac1:1CG 
    pac2:1DG

    #pensions exonérées de source étrangère: total des pensions nettes encaissées    
    vous:1AH
    conj:1BH
    pac1:1CH 
    pac2:1DH
    
#revenus exceptionnels ou différés à imposer selon le système du quotient
montant total des revenus à imposer selon le système du quotient: 0XX


#plus-values et gains divers
    #gains de cession de bons de souscription de parts de créateurs d'entreprise taxable à 19 %:3SJ
    #gains de cession de bons de souscription de parts de créateurs d'entreprise taxable à 30 %:3SK
    #gains de cession de valeurs mobilières, de droits sociaux et assimilés: 
        #plus-value imposable:3VG
        #perte 2013:3VH
        #abattement net pour durée de détention appliquée:
            #sur des plus-values:3SG
            #sur des moins-values:3SH
        #abattement net pour durée de détention renforcée appliquée:
            #sur des plus-values:3SL
            #sur des moins-values:3SM
    #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 16/10/2007, soumis à la contributin salariale de 10%:
    vous:3VN
    conj:3SN
    #impatriés: cessions de titres détenus à l'étranger (report de la déclaration 2047 IMP)
        #plus-values exonérées (50 %):3VQ
        #moins-values non imputables (50 %):3VR
    #plus-values en report d'imposition (art 150-0 D ter du CGI):3WE
        #plus-values taxables à 24 %:3SB
    #plus-values en report d'imposition (art 150-0 B ter du CGI):3WH
    #transfert du domicile hors de France, report de la déclaration 2074 ET:
        #plus-values et créances dont l'imposition est en sursis de paiement:
            #plus-values imposables:3WA
            #plus-values taxables à 19 %:3WF
        #plus-values et créances dont l'imposition ne bénéficie pas du sursis de paiement:
            #plus-values imposables:3WB
            #plus-values taxables à 19 %:3WG
            #abattement pour durée de détention:3WD
            #plus-values imposables (art 150-0 D ter bis du CGI):3WI
            #plus-values taxables à 19 % (art 150-0 D ter bis du CGI):3WJ
    #plus-values de cession de titres de jeunes entreprises innovantes exonérées:3VP
    #plus-values exonérées de cession de participations supérieures à 25 % au sein du groupe familial:3VY
    #plus-values de cession d'une résidence secondaire exonérée sous condition de remploi:3VW
    #plus-values réalisées par les non-résidents:
        #plus-values de cession de droits sociaux art 244 bis B du CGI et distributions de sociétés de capital-risque:3SE
    
#revenus fonciers
    #amortissement "Robien" et "Borloo neuf" déduit des revenus fonciers 2013 (investissements réalisés en 2009):4BY
    #taxe sur les loyers élevés (report de la déclaration 2042 LE):4BH
    
#revenus agricoles
    #revenus des exploitants forestiers (régime du forfait)
    vous:5HD
    conj:5ID
    pac1:5JD
    #régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur:
        #jeunes agriculteurs, abattement de 50% ou 100% (à vérifier sur la déclaration papier):
        vous:5HZ
        conj:5IZ
        pac1:5JZ
    #déficits agricoles des années antérieures du foyer non encore déduits:
    2007:5QF
    2008:5QG
    2009:5QN
    2010:5QO
    2011:5QP
    2012:5QQ
    
#revenus non commerciaux professionnels:
    #régime de la déclaratin contrôlée, revenus bénéficiant de l'abattement association agrée ou viseur
        #jeunes créateurs abattement 50 %:
        vous:5QL
        conj:5RL
        pac1:5SL
        #honoraires de prospection commerciale exonérs:
        vous:5TF
        conj:5UF
        pac1:5VF    
    #régime de la déclaratin contrôlée, revenus ne bénéficiant pas de l'abattement association agrée
        #honoraires de prospection commerciale exonérs:
        vous:5TI
        conj:5UI
        pac1:5VI
        
#revenus non commerciaux non professionnels
    #régime déclaratif spécial ou micro BNC (recettes brutes sans déduction d'abattement)
        #revenus nets exonérés
        vous:5TH
        conj:5UH
        pac1:5VH
    #régime de la déclaration contrôlée
        #revenus exonérés avec AA ou viseur
        vous:5HK
        conj:5JK
        pac1:5LK
        #revenus imposables avec AA ou viseur
        vous:5JG
        conj:5RF
        pac1:5SF
        #déficits avec AA ou viseur
        vous:5JJ
        conj:5RG
        pac1:5SG
        #inventeurs et auteurs de logiciels: produits taxables à 16 % avec AA ou viseur
        vous:5TC
        conj:5UC
        pac1:5VC
        #jeunes créateurs abattement de 50 %, avec AA ou viseur
        vous:5SV
        conj:5SW
        pac1:5SX
    #déficits des années antérieures non encore déduite=s:
    2007:5HT
    2008:5IT
    2009:5JT
    2010:5KT
    2011:5LT
    2012:5MT

#revenus à imposer aux prélèvements sociaux
    #revenus nets:
    vous:5HY
    conj:5IY
    pac1:5JY
    #plus-values à long terme exonérées en cas de départ à la retraite
    vous:5HG
    conj:5IG
    
#revenus industriels et commerciaux professionnels
    #régime du bénéfice réel:
        #locations meublées avec CGA ou viseur:
        vous:5HA
        conj:5IA
        pac1:5JA
        #locations meublées sans CGA:
        vous:5KA
        conj:5LA
        pac1:5MA 
        #déficit locations meublées avec CGA ou viseur:
        vous:5QA
        conj:5RA
        pac1:5SA
    
#revenus industriels et commerciaux non professionnels
    #déficits industriels et commerciaux non professionnels des années antérieures non encore déduits
    2007:5RN
    2008:5RO
    2009:5RP
    2010:5RQ
    2011:5RR
    2012:5RW
    
#locations meublées non professionnelles
    #régime du bénéfice réel
        #revenus imposables avec CGA ou viseur:
        vous:5NA
        conj:5OA
        pac1:5PA
        #déficits avec CGA ou viseur:
        vous:5NY
        conj:5OY
        pac1:5PY
        #déficits sans CGA:
        vous:5NZ
        conj:5OZ
        pac1:5PZ
        #déficits des années antérieures non encore déduits:
        2003:5GA
        2004:5GB
        2005:5GC
        2006:5GD
        2007:5GE
        2008:5GF
        2009:5GG
        2010:5GH
        2011:5GI
        2012:5GJ
        
### CHARGES ET IMPUTATIONS DIVERSES    

    #epargne retraite PERP et produits assimilés (PREFON, COREM et C.G.O.S)
        #plafond de déduction non utilisé sur les revenus de 2010
        vous:6PS
        conj:6PT
        pac1:6PU
        #plafond de déduction non utilisé sur les revenus de 2011
        vous:6PS
        conj:6PT
        pac1:6PU
        #plafond de déduction non utilisé sur les revenus de 2012
        vous:6PS
        conj:6PT
        pac1:6PU
        #vous souhaitez bénéficier du plafond de votre conjoint, cochez la case:6QR
        #si vous êtes nouvellement domicilié en France en 2013 après avoir résidé à l'étranger au cours des 3 années précédentes:6QW
        #Détermination du plafond de déduction pour les revenus 2013 au titre de l'Epargne Retraite (PERP, Préfon et assimilés):   
          Cotisations versées en 2013 aux régimes obligatoires d'entreprise de retraite  supplémentaire "article 83", PERCO et, pour leur montant total ou partiel,
          celles versées aux régimes ou contrats facultatifs de retraite "Madelin" et "Madelin agricole":  
          vous:6QS   
          conj:6QT   
          pac1:6QU   

### CHARGES OUVRANT DROIT A REDUCTION OU CREDIT D'IMPOT
    #dons à des organismes d'intérêt général établis dans l'Etat européen:
        #dons à des organismes d'aides aux personnes:7VA
        #dons à des autres organismes:7VC
    #dépenses en faveur de la qualité environnementale de l'habitation principale
        #vous avez réalisé des dépenses d'isolation thermique des murs donnant sur l'extérieur, travaux effectués sur au moins la moitié de la surface totale des murs: 7WC
        #vous avez réalisé des dépenses d'isolation thermique des toitures, travaux effectués sur la totalité de la toiture:7VG
        #isolation thermique:
            #matériaux d'isolation des murs (montant acquisition et pose):7SG
            #matériaux d'isolation thermique des parois vitrées (montant):7SJ
            #volets isolants (montant):7SK
            #porte d'entrée donnant sur l'extérieur (montant):7SL
        #equipement de production d'énergie utilisant une source d'énergie renouvelable
            #Équipements de production d'électricité utilisant l'énergie radiative du soleil (panneaux photovoltaïques):7SM    
            #Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent:7SN    
            #Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent:7SO    
            #Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur:7SP   
            #Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur (y compris le coût de la pose de l'échangeur de chaleur souterrain):7SQ  
            #Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques):7SR  
            #Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires (chauffe-eaux solaires...):7SS   
            #Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (énergie éolienne, hydraulique…):7ST   
        #Autres dépenses
            # Équipements de récupération et de traitement des eaux pluviales:7SU   
            #Diagnostic de performance énergétique:7SV    
            #Équipements de raccordement à un réseau de chaleur:7SW   
    #dépenses en faveur de la qualité environnementale des habitations données en location
        #montant du crédit d'impôt calculé:7SZ
    #travaux de prévention des risques technologiques dans les logements données en location (report 2041 gr)
        #dépenses réalisées en 2013:7WR
    #travaux de restauration immobilière: loi Malraux
        #opérations engagées avant le 1/1/2011:
            #dans un secteur sauvegardé ou assimilé:7RD
            #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7RC
        #opérations engagées en 2012:
            #dans un secteur sauvegardé ou assimilé:7RF
            #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7RE
        #opérations engagées en 2013:
            #dans un secteur sauvegardé ou assimilé:7SY
            #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7SX
    #dépenses de protection du patrimoine naturel
        #report de réduction d'impôt non encore imputée de l'année 2010:7KB
        #report de réduction d'impôt non encore imputée de l'année 2011:7KC            
        #report de réduction d'impôt non encore imputée de l'année 2012:7KD
    #investissement locatifs: loi Duflot
        #investissement réalisés et achevés en 2013:
            #en métropole:7GH
            #outre-mer:7GI
    #investissement locatifs neufs: loi Scellier
        #investissement achevés ou acquis en 2013:
            #investissements réalisés de 1/1/2013 au 31/03/2013 avec engagement de réalisation en 2012:
                #Métropole, logement BBC:7FA
                #Métropole, logement non-BBC:7FB
                #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7FC
                #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7FD
            #investissements réalisés en 2012 avec engagement de réalisation de l'investissement à compter du 1/1/2012:
                #Métropole, logement BBC:7JA
                #Métropole, logement non-BBC:7JF
                #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JK
                #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JO
            #investissements réalisés en 2012 avec engagement de réalisation de l'investissement en 2011:
                #Métropole, logement BBC:7JB
                #Métropole, logement non-BBC:7JG
                #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JL
                #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JP
            #investissements réalisés en 2012, logement acquis en l'état de futur achévement avec contrat de réservation enregistré au plus tard le 31/12/2011:
                #investissements réalisés du 1/1/2012 au 31/3/2012:
                    #Métropole, logement BBC:7JD
                    #Métropole, logement non-BBC:7JH
                    #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JM
                    #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JQ
                #investissements réalisés du 1/4/2012 au 31/12/2012:
                    #Métropole, logement BBC:7JE
                    #Métropole, logement non-BBC:7JJ
                    #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JN
                    #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JR                                
            #investissements réalisés en 2011 avec engagement de réalisation de l'investissement à compter du 1/1/2011:
                #Métropole, logement BBC:7NA
                #Métropole, logement non-BBC:7NF
                #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NK
                #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NP
            #investissements réalisés en 2011 avec engagement de réalisation de l'investissement en 2010:
                #Métropole, logement BBC:7NB
                #Métropole, logement non-BBC:7NG
                #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NL
                #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NQ
            #investissements réalisés en 2011, logement acquis en l'état de futur achévement avec contrat de réservation enregistré au plus tard le 31/12/2010:
                #investissements réalisés du 1/1/2011 au 31/1/2011:
                    #Métropole, logement BBC:7NC
                    #Métropole, logement non-BBC:7NH
                    #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NM
                    #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NR
                #investissements réalisés du 1/2/2011 au 31/3/2011:
                    #Métropole, logement BBC:7ND
                    #Métropole, logement non-BBC:7NI
                    #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NN
                    #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NS                                               
                #investissements réalisés du 1/4/2011 au 31/12/2011:
                    #Métropole, logement BBC:7NE
                    #Métropole, logement non-BBC:7NJ
                    #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NO
                    #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NT
            #report concernant les investissements achevés ou acquis au cours des années antérieures:
                #investissements achevés en 2012: report de 1/9 de la réduction d'impôt:
                    #investissements réalisés en 2012:
                        #investissements réalisés en 2012, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GS
                        #investissements réalisés en 2012 avec promesse d'achat en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GK
                    #investissements réalisés en 2011:
                        #investissements réalisés en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GL
                        #investissements réalisés en 2011 avec promesse d'achat en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GP
                    #investissements réalisés en 2010:
                        #investissements réalisés en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GS
                #investissements achevés en 2011: report de 1/9 de la réduction d'impôt:
                    #investissements réalisés en 2011:
                        #investissements réalisés en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7HA
                        #investissements réalisés en 2011 avec promesse d'achat en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7HB
                    #investissements réalisés en 2010:
                        #investissements réalisés en 2010, en Métropole et dans les DOM-COM:7HD
                        #investissements réalisés en 2010 avec promesse d'achat avant le 1/1/2010, en Métropole et dans les DOM-COM:7HE
                    #investissements réalisés en 2009, en Métropole et dans les DOM-COM:7HF
                #investissements réalisés et achevés en 2011: report de 1/5 de la réduction d'impôt:
                    #investissement en Polynésie, Nouvelle Calédonie, dans les îles Wallis et Futuna:7HG                    
                    #investissement en Polynésie, Nouvelle Calédonie, dans les îles Wallis et Futuna avec promesse d'achat en 2010:7HH
            #investissements achevés en 2010:report de 1/9 de l'investissement:
                #investissement réalisés et achevés en 2010, en Métropole:7HV
                #investissement réalisés et achevés en 2010, dans les DOM-COM:7HW
                #investissement réalisés et achevés en 2010, en Métropole avec promesse d'achat avant le 1/1/2010:7HX                
                #investissement réalisés et achevés en 2010, dans les DOM-COM avec promesse d'achat avant le 1/1/2010:7HZ                     
            #investissements réalisés en 2009 et achevés en 2010:
                #investissement réalisés en 2009 et achevés en 2010, en Métropole en 2009, dans les DOM du 1/1/2009 au 26/5/2009, dans les DOM du 27/5/2009 au 30/12/2009 lorsqu'ils ne respectent pas les plafonds spécifiques:7HT
                #investissement réalisés et achevés en 2010, dans les DOM-COM du 27/5/2009 au 31/12/2009 respectant les plafonds spécifiques:7HU
            #report du solde des réductions d'impôts non encore imputé
                #investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1/1/2010:
                    #report de l'année 2010:7LB
                    #report de l'année 2011:7LE
                    #report de l'année 2012:7LM
                #investissements réalisés et achevés en 2010, ou réalisés en 2010 et achevés en 2011, ou rélisés et achevés en 2011 avec engagement en 2010:
                    #report de l'année 2010:7LC
                    #report de l'année 2011:7LD
                    #report de l'année 2012:7LS
                #investissements réalisés et achevés en 2011: report du solde de réduction d'impôt de l'année 2011:7LF
                #investissements réalisés et achevés en 2011: report du solde de réduction d'impôt de l'année 2012:7LZ                    
                #investissements réalisés et achevés en 2012: report du solde de réduction d'impôt de l'année 2012:7MG
    #investissement destinés à la location meublée non professionnelle: loi Censi-Bouvard
            #investissement réalisés en 2013:
                #





"""




# pfam only
    ('inactif', BoolCol(entity = 'fam',
                        label = u"Parent inactif (PAJE-CLCA)")),

    ('partiel1', BoolCol(entity = 'fam',
                         label = u"Parent actif à moins de 50% (PAJE-CLCA)")),

    ('partiel2', BoolCol(entity = 'fam',
                         label = u"Parent actif entre 50% et 80% (PAJE-CLCA)")),

    ('categ_inv', IntCol(label = u"Catégorie de handicap (AEEH)")),

    ('opt_colca', BoolCol(entity = 'fam',
                          label = u"Opte pour le COLCA")),

    ('empl_dir', BoolCol(entity = 'fam',
                         label = u"Emploi direct (CLCMG)")),

    ('ass_mat', BoolCol(entity = 'fam',
                        label = u"Assistante maternelle (CLCMG)")),

    ('gar_dom', BoolCol(entity = 'fam',
                        label = u"Garde à domicile (CLCMG)")),

# zones apl and calibration
    ('tu99', EnumCol(label = u"Tranche d'unité urbaine",
                     entity = 'men',
                     enum = Enum([u'Communes rurales',
                                  u'moins de 5 000 habitants',
                                  u'5 000 à 9 999 habitants',
                                  u'10 000 à 19 999 habitants',
                                  u'20 000 à 49 999 habitants',
                                  u'50 000 à 99 999 habitants',
                                  u'100 000 à 199 999 habitants',
                                  u'200 000 habitants ou plus (sauf agglomération parisienne)',
                                  u'agglomération parisienne']),
                     survey_only = True)),

    ('tau99', EnumCol(label = u"tranche d'aire urbaine",
                      entity = 'men',
                      enum = Enum([u'Communes hors aire urbaine',
                                   u'Aire urbaine de moins de 15 000 habitants',
                                   u'Aire urbaine de 15 000 à 19 999 habitants',
                                   u'Aire urbaine de 20 000 à 24 999 habitants',
                                   u'Aire urbaine de 25 000 à 34 999 habitants',
                                   u'Aire urbaine de 35 000 à 49 999 habitants',
                                   u'Aire urbaine de 50 000 à 99 999 habitants',
                                   u'Aire urbaine de 100 000 à 199 999 habitants',
                                   u'Aire urbaine de 200 000 à 499 999 habitants',
                                   u'Aire urbaine de 500 000 à 9 999 999 habitants',
                                   u'Aire urbaine de Paris']),
                      survey_only = True)),

    ('reg', EnumCol(label = u"Région",
                    entity = 'men',
                    enum = Enum([u'Ile-de-France',
                                 u'Champagne-Ardenne',
                                 u'Picardie',
                                 u'Haute-Normandie',
                                 u'Centre',
                                 u'Basse-Normandie',
                                 u'Bourgogne',
                                 u'Nord-Pas de Calais',
                                 u'Lorraine',
                                 u'Alsace',
                                 u'Franche-Comté',
                                 u'Pays de la Loire',
                                 u'Bretagne',
                                 u'Poitou-Charentes',
                                 u'Aquitaine',
                                 u'Midi-Pyrénées',
                                 u'Limousin',
                                 u'Rhône-Alpes',
                                 u'Auvergne',
                                 u'Languedoc-Roussillon',
                                 u"Provence-Alpes-Côte-d'Azur",
                                 u'Corse' ]),
                    survey_only = True)),

    ('pol99', EnumCol(label = u"Catégorie de la commune au sein du découpage en aires et espaces urbains",
                      entity = 'men',
                      enum = Enum([u"Commune appartenant à un pôle urbain",
                                   u"Commune monopolarisée (appartenant à une couronne périurbaine",
                                   u"Commune monopolarisée",
                                   u"Espace à dominante rurale"]),
                      survey_only = True)),

    ('cstotpragr', EnumCol(label = u"catégorie socio_professionelle agrégée de la personne de référence",
                           entity = 'men',
                           enum = Enum([u"Non renseignée",
                                        u"Agriculteurs exploitants",
                                        u"Artisans, commerçants, chefs d'entreprise",
                                        u"Cadres supérieurs",
                                        u"Professions intermédiaires",
                                        u"Employés",
                                        u"Ouvriers",
                                        u"Retraités",
                                        u"Autres inactifs"]),
                           survey_only = True)),

    ('naf16pr', EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence",
                        entity = 'men',
                        enum = Enum([u"Sans objet",
                                     u"Non renseigné",
                                     u"Agriculture, sylviculture et pêche",
                                     u"Industries agricoles",
                                     u"Industries des biens de consommation",
                                     u"Industrie automobile",
                                     u"Industries des biens d'équipement",
                                     u"Industries des biens intermédiaires",
                                     u"Energie",
                                     u"Construction",
                                     u"Commerce et réparations",
                                     u"Transports",
                                     u"Activités financières",
                                     u"Activités immobilières",
                                     u"Services aux entreprises",
                                     u"Services aux particuliers",
                                     u"Education, santé, action sociale",
                                     u"Administrations"], start = -1),
                        survey_only = True)),  # 17 postes + 1 (-1: sans objet, 0: nonrenseigné)

    ('nafg17npr', EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence ",
                      entity = 'men',
                      enum = Enum([u"Sans objet",
                                   u"Non renseigné",
                                   u"Agriculture, sylviculture et pêche",
                                   u"Industries extractives, énergie, eau, gestion des déchets et dépollution",
                                   u"Fabrication de denrées alimentaires, de boissons et de produits à base de tabac",
                                   u"Cokéfaction et raffinage",
                                   u"Fabrication d'équipements électriques, électroniques, informatiques ; fabrication de machines",
                                   u"Fabrication de matériels de transport",
                                   u"Fabrication d'autres produits industriels",
                                   u"Construction",
                                   u"Commerce ; réparation d'automobiles et de motocycles",
                                   u"Transports et entreposage",
                                   u"Hébergement et restauration",
                                   u"Information et communication",
                                   u"Activités financières et d'assurance",
                                   u"Activités immobilières",
                                   u"Activités scientifiques et techniques ; services administratifs et de soutien",
                                   u"Administration publique, enseignement, santé humaine et action sociale",
                                   u"Autres activités de services"], start = -1),  # 17 postes + 1 (-1: sans objet, 0: nonrenseigné)
                    survey_only = True)),


#    ('typmen15', EnumCol(label = u"Type de ménage",
#                       entity = 'men',
#                       enum = Enum([u"Personne seule active",
#                                    u"Personne seule inactive",
#                                    u"Familles monoparentales, parent actif",
#                                    u"Familles monoparentales, parent inactif et au moins un enfant actif",
#                                    u"Familles monoparentales, tous inactifs",
#                                    u"Couples sans enfant, 1 actif",
#                                    u"Couples sans enfant, 2 actifs",
#                                    u"Couples sans enfant, tous inactifs",
#                                    u"Couples avec enfant, 1 membre du couple actif",
#                                    u"Couples avec enfant, 2 membres du couple actif",
#                                    u"Couples avec enfant, couple inactif et au moins un enfant actif",
#                                    u"Couples avec enfant, tous inactifs",
#                                    u"Autres ménages, 1 actif",
#                                    u"Autres ménages, 2 actifs ou plus",
#                                    u"Autres ménages, tous inactifs"],start = 1))),

    ('ageq', EnumCol(label = u"âge quinquennal de la personne de référence",
                    entity = 'men',
                    enum = Enum([u"moins de 25 ans",
                                 u"25 à 29 ans",
                                 u"30 à 34 ans",
                                 u"35 à 39 ans",
                                 u"40 à 44 ans",
                                 u"45 à 49 ans",
                                 u"50 à 54 ans",
                                 u"55 à 59 ans",
                                 u"60 à 64 ans",
                                 u"65 à 69 ans",
                                 u"70 à 74 ans",
                                 u"75 à 79 ans",
                                 u"80 ans et plus"]),
                    survey_only = True)),


#    ('nbinde', EnumCol(label = u"taille du ménage",
#                     entity = 'men',
#                     enum = Enum([u"Une personne",
#                                  u"Deux personnes",
#                                  u"Trois personnes",
#                                  u"Quatre personnes",
#                                  u"Cinq personnes",
#                                  u"Six personnes et plus"], start = 1))),

    ('ddipl', EnumCol(label = u"diplôme de la personne de référence",
                    entity = 'men',
                    enum = Enum([u"Non renseigné"
                                 u"Diplôme supérieur",
                                 u"Baccalauréat + 2 ans",
                                 u"Baccalauréat ou brevet professionnel ou autre diplôme de ce niveau",
                                 u"CAP, BEP ou autre diplôme de ce niveau",
                                 u"Brevet des collèges",
                                 u"Aucun diplôme ou CEP"], start = 1),
                    survey_only = True)),

    ('act5', EnumCol(label = u"activité",
                     enum = Enum([u"Salarié",
                                  u"Indépendant",
                                  u"Chômeur",
                                  u"Retraité",
                                  u"Inactif"], start = 1),
                    survey_only = True)),  # 5 postes normalement TODO: check = 0

    ('wprm_init', FloatCol(label = u"Effectifs",
                           survey_only = True)),

# # ISF ##

# # Immeubles bâtis ##
    ('b1ab', IntCol(entity = 'ind', label = u"valeur résidence principale avant abattement", val_type = "monetary")),  # #  valeur résidence principale avant abattement ##
    ('b1ac', IntCol(entity = 'foy', label = u"valeur autres immeubles avant abattement", val_type = "monetary")),
# # non bâtis ##
    ('b1bc', IntCol(entity = 'foy', label = u"Immeubles non bâtis: bois, fôrets et parts de groupements forestiers", val_type = "monetary")),
    ('b1be', IntCol(entity = 'foy', label = u"Immeubles non bâtis: biens ruraux loués à long termes", val_type = "monetary")),
    ('b1bh', IntCol(entity = 'foy', label = u"Immeubles non bâtis: parts de groupements fonciers agricoles et de groupements agricoles fonciers", val_type = "monetary")),
    ('b1bk', IntCol(entity = 'foy', label = u"Immeubles non bâtis: autres biens", val_type = "monetary")),

# # droits sociaux- valeurs mobilières-liquidités- autres meubles ##
    ('b1cl', IntCol(entity = 'foy', label = u"Parts et actions détenues par les salariés et mandataires sociaux", val_type = "monetary")),
    ('b1cb', IntCol(entity = 'foy', label = u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum", val_type = "monetary")),
    ('b1cd', IntCol(entity = 'foy', label = u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité", val_type = "monetary")),
    ('b1ce', IntCol(entity = 'foy', label = u"Autres valeurs mobilières", val_type = "monetary")),
    ('b1cf', IntCol(entity = 'foy', label = u"Liquidités", val_type = "monetary")),
    ('b1cg', IntCol(entity = 'foy', label = u"Autres biens meubles", val_type = "monetary")),

    ('b1co', IntCol(entity = 'foy', label = u"Autres biens meubles: contrats d'assurance-vie", val_type = "monetary")),

#    b1ch
#    b1ci
#    b1cj
#    b1ck


# # passifs et autres réduc ##
    ('b2gh', IntCol(entity = 'foy', label = u"Total du passif et autres déductions", val_type = "monetary")),

# # réductions ##
    ('b2mt', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary")),
    ('b2ne', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary")),
    ('b2mv', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings" , val_type = "monetary")),
    ('b2nf', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings", val_type = "monetary")),
    ('b2mx', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FIP", val_type = "monetary")),
    ('b2na', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FCPI ou FCPR", val_type = "monetary")),
    ('b2nc', IntCol(entity = 'foy', label = u"Réductions pour dons à certains organismes d'intérêt général", val_type = "monetary")),

# #  montant impôt acquitté hors de France ##
    ('b4rs', IntCol(entity = 'foy', label = u"Montant de l'impôt acquitté hors de France", val_type = "monetary")),

# # BOUCLIER FISCAL ##

    ('rev_or', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    ('rev_exo', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    ('tax_fonc', IntCol(entity = 'foy', label = u"Taxe foncière", val_type = "monetary")),
    ('restit_imp', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # to remove
    ('champm', BoolCol(entity = 'men',
                       default = True,
                       survey_only = True,
                       )),

    ('wprm', FloatCol(entity = 'men',
                      default = 1,
                      label = u"Effectifs",
                      survey_only = True,
                      )),

    ('etr', IntCol()),
    ('coloc', BoolCol(label = u"Vie en colocation")),
    ('csg_rempl', EnumCol(label = u"Taux retenu sur la CSG des revenus de remplacment",
                 entity = 'ind',
                 enum = Enum([u"Non renseigné/non pertinent",
                              u"Exonéré",
                              u"Taux réduit",
                              u"Taux plein"]),
                default = 3)),

    ('aer', IntCol()),
    ('ass', IntCol()),
    ('f5sq', IntCol()),

    ('m_afeamam', IntCol(entity = 'men')),
    ('m_agedm', IntCol(entity = 'men')),
    ('m_clcam', IntCol(entity = 'men')),
    ('m_colcam', IntCol(entity = 'men')),
    ('m_mgamm', IntCol(entity = 'men')),
    ('m_mgdomm', IntCol(entity = 'men')),
    ('zthabm', IntCol(entity = 'men')),  # Devrait être renommée tax

    ('adoption', BoolCol(entity = "ind", label = u"Enfant adopté")),

    # ('tax_hab', IntCol()),
    ))

for name, column in column_by_name.iteritems():
    if column.label is None:
        column.label = name
    assert column.name is None
    column.name = name
