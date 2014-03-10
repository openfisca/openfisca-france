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

from .. import entities


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
    build_column_couple('noi', IntCol(label = u"Numéro d'ordre individuel")),

    build_column_couple('idmen', IntCol(label = u"Identifiant du ménage")),  # 600001, 600002,
    build_column_couple('idfoy', IntCol(label = u"Identifiant du foyer")),  # idmen + noi du déclarant
    build_column_couple('idfam', IntCol(label = u"Identifiant de la famille")),  # idmen + noi du chef de famille

    build_column_couple('quimen', EnumCol(QUIMEN)),
    build_column_couple('quifoy', EnumCol(QUIFOY)),
    build_column_couple('quifam', EnumCol(QUIFAM)),

    build_column_couple('sali', IntCol(label = u"Revenus d'activité imposables",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AJ",
                                   QUIFOY['conj']: u"1BJ",
                                   QUIFOY['pac1']: u"1CJ",
                                   QUIFOY['pac2']: u"1DJ",
                                   QUIFOY['pac3']: u"1EJ",
                                   })),  # (f1aj, f1bj, f1cj, f1dj, f1ej)
    build_column_couple('choi', IntCol(label = u"Autres revenus imposables (chômage, préretraite)",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AP",
                                   QUIFOY['conj']: u"1BP",
                                   QUIFOY['pac1']: u"1CP",
                                   QUIFOY['pac2']: u"1DP",
                                   QUIFOY['pac3']: u"1EP",
                                   })),  # (f1ap, f1bp, f1cp, f1dp, f1ep)
    build_column_couple('rsti', IntCol(label = u"Pensions, retraites, rentes connues imposables!p",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AS",
                                   QUIFOY['conj']: u"1BS",
                                   QUIFOY['pac1']: u"1CS",
                                   QUIFOY['pac2']: u"1DS",
                                   QUIFOY['pac3']: u"1ES",
                                   })),  # (f1as, f1bs, f1cs, f1ds, f1es)
    build_column_couple('fra', IntCol(label = u"Frais réels",
                   val_type = "monetary",
                   cerfa_field = {QUIFOY['vous']: u"1AK",
                                  QUIFOY['conj']: u"1BK",
                                  QUIFOY['pac1']: u"1CK",
                                  QUIFOY['pac2']: u"1DK",
                                  QUIFOY['pac3']: u"1EK",
                                  })),  # (f1ak, f1bk, f1ck, f1dk, f1ek)

    build_column_couple('alr', IntCol(label = u"Pensions alimentaires perçues",
                   val_type = "monetary",
                   cerfa_field = {QUIFOY['vous']: u"1AO",
                                  QUIFOY['conj']: u"1BO",
                                  QUIFOY['pac1']: u"1CO",
                                  QUIFOY['pac2']: u"1DO",
                                  QUIFOY['pac3']: u"1EO",
                                  })),  # (f1ao, f1bo, f1co, f1do, f1eo)
    build_column_couple('alr_decl', BoolCol(label = u"Pension déclarée", default = True)),

    build_column_couple('hsup', IntCol(label = u"Heures supplémentaires: revenus exonérés connus",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AU",
                                   QUIFOY['conj']: u"1BU",
                                   QUIFOY['pac1']: u"1CU",
                                   QUIFOY['pac2']: u"1DU",
                                   QUIFOY['pac3']: u"1EU",
                                   })),  # (f1au, f1bu, f1cu, f1du, f1eu)

# pour inv, il faut que tu regardes si tu es d'accord et si c'est bien la bonne case,
# la case P exsite déjà plus bas ligne 339 sous le nom caseP

    build_column_couple('inv', BoolCol(label = u'Invalide')),  # TODO: cerfa_field

    build_column_couple('alt', BoolCol(label = u'Enfant en garde alternée')),  # TODO: cerfa_field

    build_column_couple('cho_ld', BoolCol(label = u"Demandeur d'emploi inscrit depuis plus d'un an",
                       cerfa_field = {QUIFOY['vous']: u"1AI",
                                      QUIFOY['conj']: u"1BI",
                                      QUIFOY['pac1']: u"1CI",
                                      QUIFOY['pac2']: u"1DI",
                                      QUIFOY['pac3']: u"1EI",
                                   })),  # (f1ai, f1bi, f1ci, f1di, f1ei)
    build_column_couple('ppe_tp_sa', BoolCol(label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière",
                          cerfa_field = {QUIFOY['vous']: u"1AX",
                                         QUIFOY['conj']: u"1BX",
                                         QUIFOY['pac1']: u"1CX",
                                         QUIFOY['pac2']: u"1DX",
                                         QUIFOY['pac3']: u"1QX",
                                         })),  # (f1ax, f1bx, f1cx, f1dx, f1qx)
    build_column_couple('ppe_tp_ns', BoolCol(label = u"Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière",
                          cerfa_field = {QUIFOY['vous']: u"5NW",
                                         QUIFOY['conj']: u"5OW",
                                         QUIFOY['pac1']: u"5PW",
                                         })),  # (f5nw, f5ow, f5pw)
    build_column_couple('ppe_du_sa', IntCol(label = u"Prime pour l'emploi des salariés: nombre d'heures payées dans l'année",
                         cerfa_field = {QUIFOY['vous']: u"1AV",
                                        QUIFOY['conj']: u"1BV",
                                        QUIFOY['pac1']: u"1CV",
                                        QUIFOY['pac2']: u"1DV",
                                        QUIFOY['pac3']: u"1QV",
                                        })),  # (f1av, f1bv, f1cv, f1dv, f1qv)
    build_column_couple('ppe_du_ns', IntCol(label = u"Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année",
                         cerfa_field = {QUIFOY['vous']: u"5NV",
                                        QUIFOY['conj']: u"5OV",
                                        QUIFOY['pac1']: u"5PV",
                                   })),  # (f5nv, f5ov, f5pv)
    build_column_couple('jour_xyz', IntCol(default = 360,
                        entity = "foy",
                        label = u"Jours décomptés au titre de cette déclaration")),
    build_column_couple('age', AgesCol(label = u"Âge" , val_type = "age")),
    build_column_couple('agem', AgesCol(label = u"Âge (en mois)", val_type = "months")),

    build_column_couple('zone_apl', EnumCol(label = u"Zone apl",
                         entity = 'men',
                         enum = Enum([u"Non renseigné",
                                      u"Zone 1",
                                      u"Zone 2",
                                      u"Zone 3", ]), default = 2,)),
    build_column_couple('loyer', IntCol(label = u"Loyer mensuel",
                     entity = 'men',
                     val_type = "monetary")),  # Loyer mensuel
    build_column_couple('so', EnumCol(label = u"Statut d'occupation",
                   entity = 'men',
                   enum = Enum([u"Non renseigné",
                                u"Accédant à la propriété",
                                u"Propriétaire (non accédant) du logement",
                                u"Locataire d'un logement HLM",
                                u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
                                u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
                                u"Logé gratuitement par des parents, des amis ou l'employeur"]))),

    build_column_couple('activite', EnumCol(label = u'Activité',
                         enum = Enum([u'Actif occupé',
                                    u'Chômeur',
                                    u'Étudiant, élève',
                                    u'Retraité',
                                    u'Autre inactif']), default = 4)),

    build_column_couple('titc', EnumCol(label = u"Statut, pour les agents de l'Etat des collectivités locales, ou des hôpitaux",
                     enum = Enum([
                                  u"Sans objet ou non renseigné",
                                  u"Elève fonctionnaire ou stagiaire",
                                  u"Agent titulaire",
                                  u"Contractuel"]),
                     survey_only = True,
        )),

    build_column_couple('statut', EnumCol(label = u"Statut détaillé mis en cohérence avec la profession",
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

    build_column_couple('txtppb', EnumCol(label = u"Taux du temps partiel",
                enum = Enum([u"Sans objet",
                            u"Moins d'un mi-temps (50%)",
                            u"Mi-temps (50%)",
                            u"Entre 50 et 80%",
                            u"80%",
                            u"Plus de 80%"]),
                       survey_only = True)),

    build_column_couple('nbsala', EnumCol(label = u"Nombre de salariés dans l'établissement de l'emploi actuel",
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

    build_column_couple('tva_ent', BoolCol(label = u"Entreprise employant le salarié paye de la TVA",
                        default = True)),

    build_column_couple('chpub', EnumCol(label = u"Nature de l'employeur principal",
                      enum = Enum([u"Sans objet",
                                   u"Etat",
                                   u"Collectivités locales, HLM",
                                   u"Hôpitaux publics",
                                   u"Particulier",
                                   u"Entreprise publique (La Poste, EDF-GDF, etc.)",
                                   u"Entreprise privée, association",
                                   ]),
                      survey_only = True)),

    build_column_couple('cadre', BoolCol(label = u"Cadre salarié du privé",
                      survey_only = True)),

    build_column_couple('code_risque', EnumCol(label = u"Code risque pour les accidents du travail")),  # TODO: complete label and add relevant default
    build_column_couple('exposition_accident', EnumCol(label = u"Exposition au risque pour les accidents du travail",
                            enum = Enum([u"Faible",
                                   u"Moyen",
                                   u"Elevé",
                                   u"Très elevé",
                                   ]))),

    build_column_couple('boursier', BoolCol(label = u"Elève ou étudiant boursier")),
    build_column_couple('code_postal', IntCol(label = u"Code postal du lieu de résidence",
                           entity = 'men')),

    build_column_couple('statmarit', EnumCol(label = u"Statut marital",
                          default = 2,
                          enum = Enum([u"Marié",
                                    u"Célibataire",
                                    u"Divorcé",
                                    u"Veuf",
                                    u"Pacsé",
                                    u"Jeune veuf"], start = 1))),

    build_column_couple('nbR', IntCol(label = u"Nombre de titulaires de la carte invalidité d'au moins 80 %",
                   entity = 'foy',
                   cerfa_field = u'R')),
    build_column_couple('nbJ', IntCol(label = u"Nombre d'enfants majeurs célibataires sans enfant",
                   entity = 'foy',
                   cerfa_field = u'J')),
    build_column_couple('nbI', IntCol(label = u"Nombre d'enfants à charge en résidence alternée titulaires de la carte d'invalidité",
                   entity = 'foy',
                   cerfa_field = u'I')),
    build_column_couple('nbH', IntCol(label = u"Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de l'année de perception des revenus, ou nés durant la même année ou handicapés quel que soit leur âge",
                   entity = 'foy',
                   cerfa_field = u'H')),
# TODO: vérifier si c'est bien ça pour la nbH et la caseH qui suit
    build_column_couple('nbG', IntCol(label = u"Nombre d'enfants à charge titulaires de la carte d'invalidité",
                   entity = 'foy',
                   cerfa_field = u'G')),
    build_column_couple('nbF', IntCol(label = u"Nombre d'enfants à charge  non mariés de moins de 18 ans au 1er janvier de l'année de perception des revenus, ou nés en durant la même année ou handicapés quel que soit leur âge",
                   entity = 'foy',
                   cerfa_field = u'F')),
    build_column_couple('nbN', IntCol(label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille",
                   entity = 'foy',
                   cerfa_field = u'N')),

    build_column_couple('caseE', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul",
                      entity = 'foy',
                      cerfa_field = u'E', end = 2012)),
    build_column_couple('caseF', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)",
                      entity = 'foy',
                      cerfa_field = u'F')),
    build_column_couple('caseG', BoolCol(label = u"Titulaire d'une pension de veuve de guerre",
                      entity = 'foy',
                      cerfa_field = u'G')),  # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case que l'on remplt et l'autre une case que l'on coche
    build_column_couple('caseH', IntCol(label = u"Année de naissance des enfants à charge en garde alternée", entity = 'foy',
                     cerfa_field = u'H')),
# il ne s'agit pas à proprement parlé de la case H, les cases permettant d'indiquer l'année de naissance
#    se rapportent bien à nbH mais ne sont pas nommées, choisissons nous de laisser cerfa_field = u'H' pour caseH ?
#    De plus les caseH peuvent être multiples puisqu'il peut y avoir plusieurs enfants? donc faut-il les nommer caseH1, caseH2...caseH6 (les 6 présentes dans la déclaration) ?
#    il faut aussi créer les cases F, G, R et I qui donnent également les années de naissances des PAC


    build_column_couple('caseK', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre",
                      entity = 'foy',
                      cerfa_field = u'K', end = 2011)),

    build_column_couple('caseL', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul",
                      entity = 'foy',
                      cerfa_field = u'L')),

    build_column_couple('caseN', BoolCol(label = u"Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus",
                      entity = 'foy',
                      cerfa_field = u'N')),
    build_column_couple('caseP', BoolCol(label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%",
                      entity = 'foy',
                      cerfa_field = u'P')),
    build_column_couple('caseS', BoolCol(label = u"Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                      entity = 'foy',
                      cerfa_field = u'S')),

    build_column_couple('caseT', BoolCol(label = u"Vous êtes parent isolé au 1er janvier de l'année de perception des revenus",
                      entity = 'foy',
                      cerfa_field = u'T')),

    build_column_couple('caseW', BoolCol(label = u"Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                      entity = 'foy',
                      cerfa_field = u'W')),

    build_column_couple('rfr_n_2', IntCol(entity = 'foy', label = u"Revenu fiscal de référence année n-2", val_type = "monetary")),  # TODO: provide in data
    build_column_couple('nbptr_n_2', IntCol(entity = 'foy', label = u"Nombre de parts année n-2", val_type = "monetary")),  # TODO: provide in data

    # Rentes viagères
    build_column_couple('f1aw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1AW')),
    build_column_couple('f1bw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1BW')),
    build_column_couple('f1cw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1CW')),
    build_column_couple('f1dw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1DW')),

    # Gain de levée d'options
    # Bouvard: j'ai changé là mais pas dans le code, il faut chercher les f1uv
    # et les mettre en f1tvm comme pour sali
    # Il faut aussi le faire en amont dans les tables

    # là je ne comprends pas pourquoi il faut changer les f1uv en f1tvm....
    # du coups je n'ai pas changé et j'ai fait un dico comme pour sali

    build_column_couple('f1tv', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans",
                            entity = 'ind',
                            val_type = "monetary",
                            cerfa_field = {QUIFOY['vous']: u"1TV",
                                           QUIFOY['conj']: u"1UV",
                                           })),  # (f1tv,f1uv)),

    build_column_couple('f1tw', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans",
                            entity = 'ind',
                            val_type = "monetary",
                            cerfa_field = {QUIFOY['vous']: u"1TW",
                                           QUIFOY['conj']: u"1UW",
                                           })),  # (f1tw,f1uw)),

    build_column_couple('f1tx', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans",
                            entity = 'ind',
                            val_type = "monetary",
                            cerfa_field = {QUIFOY['vous']: u"1TX",
                                           QUIFOY['conj']: u"1UX",
                            })),  # (f1tx,f1ux)),

    # RVCM
    # revenus au prélèvement libératoire
    build_column_couple('f2da', IntCol(label = u"Revenus des actions et parts soumis au prélèvement libératoire de 21 %",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2DA', end = 2012)),  # à vérifier sur la nouvelle déclaration des revenus 2013

    build_column_couple('f2dh', IntCol(label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2DH')),

    build_column_couple('f2ee', IntCol(label = u"Autres produits de placement soumis aux prélèvements libératoires",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'2EE')),

    # revenus des valeurs et capitaux mobiliers ouvrant droit à abattement
    build_column_couple('f2dc', IntCol(entity = 'foy',
                    label = u"Revenus des actions et parts donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2DC')),

    build_column_couple('f2fu', IntCol(entity = 'foy',
                    label = u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2FU')),
    build_column_couple('f2ch', IntCol(entity = 'foy',
                    label = u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement",
                    val_type = "monetary",
                    cerfa_field = u'2CH')),

    #  Revenus des valeurs et capitaux mobiliers n'ouvrant pas droit à abattement
    build_column_couple('f2ts', IntCol(entity = 'foy', label = u"Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2TS')),
    build_column_couple('f2go', IntCol(entity = 'foy',
                    label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2GO')),
    build_column_couple('f2tr', IntCol(entity = 'foy', label = u"Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)",
                    val_type = "monetary",
                    cerfa_field = u'2TR')),


    # Autres revenus des valeurs et capitaux mobiliers
    build_column_couple('f2cg', IntCol(entity = 'foy',
                    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible",
                    val_type = "monetary",
                    cerfa_field = u'2CG')),

    build_column_couple('f2bh', IntCol(entity = 'foy',
                    label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible",
                    val_type = "monetary",
                    cerfa_field = u'2BH')),

    build_column_couple('f2ca', IntCol(entity = 'foy',
                    label = u"Frais et charges déductibles",
                    val_type = "monetary",
                    cerfa_field = u'2CA')),

    build_column_couple('f2ck', IntCol(entity = 'foy',
                    label = u"Crédit d'impôt égal au prélèvement forfaitaire déjà versé",
                    val_type = "monetary",
                    cerfa_field = u'2CK',
                    start = 2013)),  # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013

    build_column_couple('f2ab', IntCol(entity = 'foy',
                    label = u"Crédits d'impôt sur valeurs étrangères",
                    val_type = "monetary",
                    cerfa_field = u'2AB')),

    build_column_couple('f2bg', IntCol(entity = 'foy',
                    label = u"Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables",
                    val_type = "monetary",
                    cerfa_field = u'2BG',
                    start = 2012)),  # TODO: nouvelle case à créer où c'est nécessaire
                                     # TODO: vérifier existence avant 2012

    build_column_couple('f2aa', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AA')),

    build_column_couple('f2al', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AL')),

    build_column_couple('f2am', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AM')),

    build_column_couple('f2an', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AN',
                    start = 2010)),

    build_column_couple('f2aq', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AQ',
                    start = 2011)),

    build_column_couple('f2ar', IntCol(entity = 'foy',
                    label = u"Déficits des années antérieures non encore déduits",
                    val_type = "monetary",
                    cerfa_field = u'2AR',
                    start = 2012)),

# je ne sais pas d'ou sort f2as...! probablement une ancienne année à laquelle je ne suis pas encore arrivé
#
#   ('f2as', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2012", val_type = "monetary", end = 2011)),  # TODO: vérifier existence <=2011

    build_column_couple('f2dm', IntCol(entity = 'foy',
                    label = u"Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %",
                    val_type = "monetary",
                    cerfa_field = u'2DM',
                    start = 2012)),  # TODO: nouvelle case à utiliser où c'est nécessaire
                                     # TODO: vérifier existence avant 2012

    build_column_couple('f2gr', IntCol(entity = 'foy',
                    label = u"Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)",
                    val_type = "monetary",
                    cerfa_field = u'2GR',
                    start = 2009,
                    end = 2009)),  # TODO: vérifier existence à partir de 2011

    build_column_couple('f3vc', IntCol(entity = 'foy',
                    label = u"Produits et plus-values exonérés provenant de structure de capital-risque",
                    val_type = "monetary",
                    cerfa_field = u'3VC')),

    build_column_couple('f3vd', IntCol(entity = 'ind',
                    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VD",
                                   QUIFOY['conj']: u"3SD",
                                   })),  # (f3vd, f3sd)

    build_column_couple('f3ve', IntCol(entity = 'foy',
                    label = u"Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %",
                    val_type = "monetary",
                    cerfa_field = u'3VE')),

    build_column_couple('f3vf', IntCol(entity = 'ind',
                    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VF",
                                   QUIFOY['conj']: u"3SF",
                                   })),  # (f3vf, f3sf)

# comment gérer les cases qui ont le même nom mais qui ne correspondent pas tout à fait à la même chose ?
# peut-ont garder le même nom et l'encadrer par des start-end ? ou avec un truc genre if sur l'année ?(pour ne pas avoir à changer le nom de la variable)
# si on garde le même nom avec des start-end, et si on intégre la variable partout où elle doit être (dans les différents calculs), est-on sûr que lors des calculs les start-end seront bien pris en compte ?
# ça rendra le modéle un peu moins clair parce qu'il y aura le même nom de variable pour des choses différentes et dans des calculs ne se rapportant pas aux mêmes choses,
# mais si les start-end fonctionne ça ne devrait pas avoir d'impact sur les calculs ? qu'en penses-tu ?

    # ## build_column_couple('f3vl', IntCol(entity = 'foy',
    # ##                 label = u"Distributions par des sociétés de capital-risque taxables à 24 %",
    # ##                 val_type = "monetary",
    # ##                 cerfa_field = u'3VL'
    # ##                 start = 2009,
    # ##                 end = 2009)),#vérifier avant 2009

    build_column_couple('f3vl', IntCol(entity = 'foy',
                    label = u"Distributions par des sociétés de capital-risque taxables à 19 %",
                    val_type = "monetary",
                    cerfa_field = u'3VL',
                    start = 2012,
                    end = 2013)),  # vérifier pour 2011 et 2010

    build_column_couple('f3vi', IntCol(entity = 'ind',
                    label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VI",
                                   QUIFOY['conj']: u"3SI",
                                   })),  # (f3vi, f3si )

    build_column_couple('f3vm', IntCol(entity = 'foy',
                    label = u"Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %",
                    val_type = "monetary",
                    cerfa_field = u'3VM')),

    build_column_couple('f3vt', IntCol(entity = 'foy',
                    label = u"Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %",
                    val_type = "monetary",
                    cerfa_field = u'3VT')),

    build_column_couple('f3vj', IntCol(entity = 'ind',
                    label = u"Gains imposables sur option dans la catégorie des salaires",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VJ",
                                   QUIFOY['conj']: u"3VK",
                                   })),  # (f3vj, f3vk )

    build_column_couple('f3va', IntCol(entity = 'ind',
                    label = u"Abattement pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"3VA",
                                   QUIFOY['conj']: u"3VB",
                                   })),  # (f3va, f3vb ))),

    # Plus values et gains taxables à des taux forfaitaires

    build_column_couple('f3vg', IntCol(entity = 'foy',
                    label = u"Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés",
                    val_type = "monetary",
                    cerfa_field = u'3VG')),

    build_column_couple('f3vh', IntCol(entity = 'foy',
                    label = u"Perte de l'année de perception des revenus",
                    val_type = "monetary",
                    cerfa_field = u'3VH')),

    build_column_couple('f3vu', IntCol(entity = 'foy',
                    end = 2009)),  # TODO: vérifier pour 2010 et 2011

    # build_column_couple('f3vv', IntCol(entity = 'foy',
    #                 label = u"Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé ",
    #                 val_type = "monetary",
    #                 cerfa_field = u'3VV')),  # TODO: à revoir :ok pour 2013, pas de 3vv pour 2012, et correspond à autre chose en 2009, vérifier 2010 et 2011

    # build_column_couple('f3si', IntCol(entity = 'foy')),  # TODO: parmi ces cas créer des valeurs individuelles
    #                                    # correspond à autre chose en 2009, vérifier 2011,2010

    # build_column_couple('f3sa', IntCol(entity = 'foy', end = 2009)),  # TODO: n'existe pas en 2013 et 2012 vérifier 2011 et 2010

    # build_column_couple('f3sf', IntCol(entity = 'foy')),  # déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

    # build_column_couple('f3sd', IntCol(entity = 'foy')),  # déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

    # build_column_couple('f3vz', IntCol(entity = 'foy',
    #                 label = u"Plus-values imposables sur cessions d’immeubles ou de biens meubles",
    #                 val_type = "monetary",
    #                 cerfa_field = u'3VV',
    #                 start = 2011)),  # TODO: vérifier avant 2012

    # Revenus fonciers
    build_column_couple('f4ba', IntCol(entity = 'foy',
                    label = u"Revenus fonciers imposables",
                    val_type = "monetary",
                    cerfa_field = u'4BA')),

    build_column_couple('f4bb', IntCol(entity = 'foy',
                    label = u"Déficit imputable sur les revenus fonciers",
                    val_type = "monetary",
                    cerfa_field = u'4BB')),

    build_column_couple('f4bc', IntCol(entity = 'foy',
                    label = u"Déficit imputable sur le revenu global",
                    val_type = "monetary",
                    cerfa_field = u'7BC')),

    build_column_couple('f4bd', IntCol(entity = 'foy',
                    label = u"Déficits antérieurs non encore imputés",
                    val_type = "monetary",
                    cerfa_field = u'4BD')),

    build_column_couple('f4be', IntCol(entity = 'foy',
                    label = u"Micro foncier: recettes brutes sans abattement",
                    val_type = "monetary",
                    cerfa_field = u'4BE')),

    # Prime d'assurance loyers impayés
    build_column_couple('f4bf', IntCol(entity = 'foy',
                    label = u"Primes d'assurance pour loyers impayés des locations conventionnées",
                    val_type = "monetary",
                    cerfa_field = u'4BF')),

    build_column_couple('f4bl', IntCol(entity = 'foy', label = u"", end = 2009)),  # TODO: cf 2010 2011

    build_column_couple('f5qm', IntCol(entity = 'ind',
                    label = u"Agents généraux d’assurances: indemnités de cessation d’activité",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"5QM",
                                   QUIFOY['conj']: u"5RM",
                                   })),  # (f5qm, f5rm )

    # Csg déductible
    build_column_couple('f6de', IntCol(entity = 'foy',
                    label = u"CSG déductible calculée sur les revenus du patrimoine",
                    val_type = "monetary",
                    cerfa_field = u'6DE')),

    # Pensions alimentaires
    build_column_couple('f6gi', IntCol(entity = 'foy',
                    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant",
                    val_type = "monetary",
                    cerfa_field = u'6GI')),

    build_column_couple('f6gj', IntCol(entity = 'foy',
                    label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant",
                    val_type = "monetary",
                    cerfa_field = u'6GJ')),

    build_column_couple('f6el', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant",
                    val_type = "monetary",
                    cerfa_field = u'6EL')),

    build_column_couple('f6em', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant",
                    val_type = "monetary",
                    cerfa_field = u'6EM')),

    build_column_couple('f6gp', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)",
                    val_type = "monetary",
                    cerfa_field = u'6GP')),

    build_column_couple('f6gu', IntCol(entity = 'foy',
                    label = u"Autres pensions alimentaires versées (mineurs, ascendants)",
                    val_type = "monetary",
                    cerfa_field = u'6GU')),


    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    build_column_couple('f6eu', IntCol(entity = 'foy',
                    label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin",
                    val_type = "monetary",
                    cerfa_field = u'6EU')),

    build_column_couple('f6ev', IntCol(entity = 'foy',
                    label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit",
                    cerfa_field = u'6EV')),

    # Déductions diverses
    build_column_couple('f6dd', IntCol(entity = 'foy',
                    label = u"Déductions diverses",
                    val_type = "monetary",
                    cerfa_field = u'6DD')),

    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    build_column_couple('f6ps', IntCol(entity = 'ind',
                    label = u"Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6PS",
                                   QUIFOY['conj']: u"6PT",
                                   QUIFOY['pac1']: u"6PU",
                                   })),  # (f6ps, f6pt, f6pu)

    build_column_couple('f6rs', IntCol(entity = 'ind',
                    label = u"Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6RS",
                                   QUIFOY['conj']: u"6RT",
                                   QUIFOY['pac1']: u"6RU",
                                   })),  # (f6rs, f6rt, f6ru))),

    build_column_couple('f6ss', IntCol(entity = 'ind',
                    label = u"Rachat de cotisations PERP, PREFON, COREM et C.G.O.S",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"6SS",
                                   QUIFOY['conj']: u"6ST",
                                   QUIFOY['pac1']: u"6SU",
                                   })),  # (f6ss, f6st, f6su))),


    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    build_column_couple('f6aa', IntCol(entity = 'foy',
                    label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel",
                    val_type = "monetary",
                    start = 2005,
                    end = 2005,
                    cerfa_field = u'6AA')),  # TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)

    # Souscriptions au capital des SOFIPÊCHE
    build_column_couple('f6cc', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des SOFIPÊCHE",
                    val_type = "monetary",
                    cerfa_field = u'CC',
                    start = 2005,
                    end = 2005)),  # ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)


    # Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
    # ou Versements sur un compte épargne codéveloppement
    build_column_couple('f6eh', IntCol(entity = 'foy',
                    label = u"",
                    val_type = "monetary",
                    start = 2005,
                    end = 2005,
                    cerfa_field = u'EH')),  # TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)

    # Pertes en capital consécutives à la souscription au capital de sociétés
    # nouvelles ou de sociétés en difficulté
    build_column_couple('f6da', IntCol(entity = 'foy',
                    label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté",
                    val_type = "monetary",
                    start = 2005,
                    end = 2005,
                    cerfa_field = u'DA')),


    # Dépenses de grosses réparations effectuées par les nus propriétaires
    build_column_couple('f6cb', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)",
                    val_type = "monetary",
                    start = 2006,
                    cerfa_field = u'6CB')),  # TODO: vérifier 2011, 10, 9 ,8, 7,6, ok pou 12 et 13
                                           # TODO: before 2006 wasPertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

    build_column_couple('f6hj', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'6HJ')),

    build_column_couple('f6hk', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'6HK')),

    build_column_couple('f6hl', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'6HL')),

    build_column_couple('f6hm', IntCol(entity = 'foy',
                    label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                    val_type = "monetary",
                    start = 2013,
                    cerfa_field = u'6HM')),

    # Sommes à rajouter au revenu imposable
    build_column_couple('f6gh', IntCol(entity = 'foy',
                    label = u"Sommes à ajouter au revenu imposable",
                    val_type = "monetary",
                    cerfa_field = u'6GH')),

    # Deficits antérieurs
    build_column_couple('f6fa', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6",
                    val_type = "monetary",
                    cerfa_field = u'6FA')),

    build_column_couple('f6fb', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5",
                    val_type = "monetary",
                    cerfa_field = u'6FB')),

    build_column_couple('f6fc', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'6FC')),

    build_column_couple('f6fd', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'6FD')),

    build_column_couple('f6fe', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'6FE')),

    build_column_couple('f6fl', IntCol(entity = 'foy',
                    label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'6FL')),

    # Dons à des organismes établis en France
    build_column_couple('f7ud', IntCol(entity = 'foy',
                    label = u"Dons à des organismes d'aide aux personnes en difficulté",
                    val_type = "monetary",
                    cerfa_field = u'7UD')),

    build_column_couple('f7uf', IntCol(entity = 'foy',
                    label = u"Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général",
                    val_type = "monetary",
                    cerfa_field = u'7UF')),

    build_column_couple('f7xs', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5",
                    val_type = "monetary",
                    cerfa_field = u'7XS')),

    build_column_couple('f7xt', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'7XT')),

    build_column_couple('f7xu', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'7XU')),

    build_column_couple('f7xw', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'7XW')),

    build_column_couple('f7xy', IntCol(entity = 'foy',
                    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7XY')),

    # Cotisations syndicales des salariées et pensionnés
    build_column_couple('f7ac', IntCol(entity = 'ind',
                    label = u"Cotisations syndicales des salariées et pensionnés",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"7AC",
                                   QUIFOY['conj']: u"7AE",
                                   QUIFOY['pac1']: u"7AG",
                                   })),  # f7ac, f7ae, f7ag

    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    build_column_couple('f7vy', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VY')),

    build_column_couple('f7vz', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VZ')),

    build_column_couple('f7vx', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011",
                    val_type = "monetary",
                    cerfa_field = u'7VX')),

    build_column_couple('f7vw', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VW')),

    build_column_couple('f7vv', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VV')),  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

    build_column_couple('f7vu', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité",
                    val_type = "monetary",
                    cerfa_field = u'7VU')),  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

    build_column_couple('f7vt', IntCol(entity = 'foy',
                    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes",
                    val_type = "monetary",
                    cerfa_field = u'7VT')),  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    build_column_couple('f7cd', IntCol(entity = 'foy',
                    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne",
                    val_type = "monetary",
                    cerfa_field = u'7CD')),

    build_column_couple('f7ce', IntCol(entity = 'foy',
                    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne",
                    val_type = "monetary",
                    cerfa_field = u'7CE')),

    # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus
    build_column_couple('f7ga', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GA')),

    build_column_couple('f7gb', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GB')),

    build_column_couple('f7gc', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge",
                    val_type = "monetary",
                    cerfa_field = u'7GC')),

    build_column_couple('f7ge', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GE')),

    build_column_couple('f7gf', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GF')),

    build_column_couple('f7gg', IntCol(entity = 'foy',
                    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée",
                    val_type = "monetary",
                    cerfa_field = u'7GG')),

    # Nombre d'enfants à charge poursuivant leurs études
    build_column_couple('f7ea', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études au collège",
                    cerfa_field = u'7EA')),

    build_column_couple('f7eb', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège",
                    cerfa_field = u'7EB')),

    build_column_couple('f7ec', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études au lycée",
                    cerfa_field = u'7EC')),

    build_column_couple('f7ed', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée",
                    cerfa_field = u'7ED')),

    build_column_couple('f7ef', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur",
                    cerfa_field = u'7EF')),

    build_column_couple('f7eg', IntCol(entity = 'foy',
                    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur",
                    cerfa_field = u'7EG')),

    # Intérêts des prêts étudiants
    build_column_couple('f7td', IntCol(entity = 'foy',
                    label = u"Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7TD')),

    build_column_couple('f7vo', IntCol(entity = 'foy',
                    label = u"Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés",
                    cerfa_field = u'7VO')),

    build_column_couple('f7uk', IntCol(entity = 'foy',
                    label = u"Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7UK')),

    # Primes de rente survie, contrats d'épargne handicap
    build_column_couple('f7gz', IntCol(entity = 'foy',
                    label = u"Primes de rente survie, contrats d'épargne handicap",
                    val_type = "monetary",
                    cerfa_field = u'7GZ')),

    # Prestations compensatoires
    build_column_couple('f7wm', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Capital fixé en substitution de rente",
                    val_type = "monetary",
                    cerfa_field = u'7WM')),

    build_column_couple('f7wn', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés",
                    val_type = "monetary",
                    cerfa_field = u'7WN')),

    build_column_couple('f7wo', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué",
                    val_type = "monetary",
                    cerfa_field = u'7WO')),

    build_column_couple('f7wp', IntCol(entity = 'foy',
                    label = u"Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7WP')),

    # Dépenses en faveur de la qualité environnementale de l'habitation principale
    build_column_couple('f7we', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés",
                    cerfa_field = u'7WE')),

    build_column_couple('f7wg', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1",
                    val_type = "monetary",
                    cerfa_field = u'7',
                    start = 2012)),  # TODO, nouvelle variable à intégrer dans OF (cf ancien nom déjà utilisé)
                                    # TODO vérifier pour les années précédentes
# TODO: CHECK
    # Intérêts d'emprunts
#     build_column_couple('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary", cerfa_field = u'7')), # cf pour quelle année
#
#     build_column_couple('f7wq', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées", cerfa_field = u'7')),

    build_column_couple('f7wt', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement ",
                    start = 2013,
                    cerfa_field = u'7WT')),  # TODO vérifier année de début

    build_column_couple('f7wh', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus",
                    start = 2013,
                    cerfa_field = u'7WH')),  # TODO vérifier année de début

    build_column_couple('f7wk', BoolCol(entity = 'foy',
                     label = u"Votre habitation principale est une maison individuelle",
                     cerfa_field = u'7WK')),

    build_column_couple('f7wf', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1",
                    end = 2012,
                    cerfa_field = u'7WF')),  # TODO vérifier les années précédentes

    # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
    build_column_couple('f7wi', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction",
                    val_type = "monetary",
                    cerfa_field = u'7WI',
                    end = 2012)),

    build_column_couple('f7wj', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées",
                    val_type = "monetary",
                    cerfa_field = u'7WJ')),

    build_column_couple('f7wl', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques",
                    val_type = "monetary",
                    cerfa_field = u'7WL')),

    # Investissements dans les DOM-TOM dans le cadre d'une entrepise
    build_column_couple('f7ur', IntCol(entity = 'foy',
                    label = u"Investissements réalisés en n-1, total réduction d’impôt",
                    val_type = "monetary",
                    cerfa_field = u'7UR',
                    end = 2011)),  # TODO: vérifier les années antérieures

    build_column_couple('f7oz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6",
                    val_type = "monetary",
                    cerfa_field = u'7OZ',
                    end = 2011)),  # TODO: vérifier les années antérieures

    build_column_couple('f7pz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7PZ',
                    end = 2012)),  # TODO: vérifier les années antérieures

    build_column_couple('f7qz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7QZ',
                    end = 2012)),  # TODO: vérifier les années antérieures

    build_column_couple('f7rz', IntCol(entity = 'foy',
                    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3",
                    val_type = "monetary",
                    cerfa_field = u'7RZ',
                    end = 2011)),  # TODO: vérifier années antérieures.

# TODO: 7sz se rapporte à des choses différentes en 2012 et 2013 par rapport aux années précédentes, cf pour les années antérieures
#     build_column_couple('f7sz', IntCol(entity = 'foy',
#                     label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-2",
#                     val_type = "monetary",
#                     cerfa_field = u'7SZ',
#                     end = 2011)),  # TODO: vérifier années <=2011.

    build_column_couple('f7sz', IntCol(entity = 'foy',
                    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location",
                    val_type = "monetary",
                    cerfa_field = u'7SZ',
                    start = 2012)),  # TODO: vérifier années <=2011

    # Aide aux créateurs et repreneurs d'entreprises
    build_column_couple('f7fy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                    cerfa_field = u'7FY',
                    end = 2011)),  # TODO: vérifier date <=2011

    build_column_couple('f7gy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                    cerfa_field = u'7GY',
                    end = 2011)),  # TODO: vérifier date <=2011


# TODO: 7jy réutilisée en 2013
#
#     build_column_couple('f7jy', IntCol(entity = 'foy',
#                     label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et ayant pris fin en n-1",
#                     cerfa_field = u'7JY',
#                     end = 2011)),

     build_column_couple('f7jy', IntCol(entity = 'foy',
                    label = u"Report de 1/9 des investissements réalisés l'année de perception des revenus déclarés -3 ou -4",
                    cerfa_field = u'7JY',
                    start = 2013)),

    build_column_couple('f7hy', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
                    cerfa_field = u'7HY',
                    end = 2011)),  # TODO: vérifier date <=2011

    build_column_couple('f7ky', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1",
                    cerfa_field = u'7KY',
                    end = 2011)),  # TODO: vérifier date <=2011

# 7iy réutilisée en 2013
#
#     build_column_couple('f7iy', IntCol(entity = 'foy',
#                     label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
#                     cerfa_field = u'7IY',
#                     end = 2011)),  # TODO: vérifier date <=2011

    build_column_couple('f7iy', IntCol(entity = 'foy',
                    label = u"Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés",
                    cerfa_field = u'7IY',
                    start = 2013)),

    build_column_couple('f7ly', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                    cerfa_field = u'7LY')),  # 2012 et 2013 ok

    build_column_couple('f7my', IntCol(entity = 'foy',
                    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                    cerfa_field = u'7MY')),  # 2012 et 2013 ok

    # Travaux de restauration immobilière
    build_column_couple('f7ra', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager",
                    val_type = "monetary",
                    cerfa_field = u'7RA')),  # 2012 et 2013 ok

    build_column_couple('f7rb', IntCol(entity = 'foy',
                    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                    val_type = "monetary",
                    cerfa_field = u'7RB')),  # 2012 et 2013 ok


# TOOD: f7gw et f7gx ne se rapporte pas a de l'assurance vie en 2013
    # Assurance-vie
#     build_column_couple('f7gw', IntCol(entity = 'foy', label = u"", cerfa_field = u'7GW', end = 2011)),  # TODO: cf pour <=2011
#     build_column_couple('f7gx', IntCol(entity = 'foy', label = u"", cerfa_field = u'7GX', end = 2011)),  # TODO: cf pour <=2011
    # build_column_couple('f7gy', IntCol()), existe ailleurs (n'existe pas en 2013 et 2012)

    build_column_couple('f7gw', IntCol(entity = 'foy',
                    label = u"Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                    cerfa_field = u'7GW',
                    start = 2013)),

    build_column_couple('f7gx', IntCol(entity = 'foy',
                    label = u"Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                    cerfa_field = u'7GX',
                    start = 2013)),

    # Investissements locatifs dans le secteur de touristique
    build_column_couple('f7xc', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1",
                    val_type = "monetary",
                    cerfa_field = u'7XC',
                    end = 2012)),

    build_column_couple('f7xd', BoolCol(entity = 'foy',
                     label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                     cerfa_field = u'7XD',
                     end = 2012)),

    build_column_couple('f7xe', BoolCol(entity = 'foy',
                     label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                     cerfa_field = u'7XE',
                     end = 2012)),

    build_column_couple('f7xf', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XF')),

    build_column_couple('f7xh', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme",
                    val_type = "monetary",
                    cerfa_field = u'7XH',
                    end = 2012)),

    build_column_couple('f7xi', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XI')),

    build_column_couple('f7xj', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XJ')),

    build_column_couple('f7xk', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XK')),

    build_column_couple('f7xl', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans",
                    val_type = "monetary",
                    cerfa_field = u'7XL',
                    end = 2012)),

    build_column_couple('f7xm', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XM')),

# TODO: f7xn cf années <= à 2011 (possible erreur dans le label pour ces dates, à vérifier)
#      build_column_couple('f7xn', IntCol(entity = 'foy',
#                     label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: investissement réalisé en n-1",
#                     val_type = "monetary",
#                     cerfa_field = u'7XN',
#                     end = 2011)),

    build_column_couple('f7xn', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XN',
                    start = 2012)),

    build_column_couple('f7xo', IntCol(entity = 'foy',
                    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7XO')),

    # Souscriptions au capital des PME
    build_column_couple('f7cf', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion",
                    val_type = "monetary",
                    cerfa_field = u'7CF')),

    build_column_couple('f7cl', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4",
                    val_type = "monetary",
                    cerfa_field = u'7CL')),

    build_column_couple('f7cm', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3",
                    val_type = "monetary",
                    cerfa_field = u'7CM')),

    build_column_couple('f7cn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2",
                    val_type = "monetary",
                    cerfa_field = u'7CN')),

    build_column_couple('f7cc', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1",
                    val_type = "monetary",
                    cerfa_field = u'7CC')),  # TODO: nouvelle variable à intégrer dans OF

    build_column_couple('f7cu', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures",
                    val_type = "monetary",
                    cerfa_field = u'7CU')),

# TODO: en 2013 et 2012 plus de sofipêche (pourtant présent dans param à ces dates...), case 7gs réutilisée
    # Souscription au capital d’une SOFIPECHE
#     build_column_couple('f7gs', IntCol(entity = 'foy',
#                     label = u"Souscription au capital d’une SOFIPECHE",
#                     val_type = "monetary",
#                     cerfa_field = u'7GS',
#                     end = 2011)),

    build_column_couple('f7gs', IntCol(entity = 'foy',
                    label = u"Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                    val_type = "monetary",
                    cerfa_field = u'7GS',
                    start = 2013)),

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
    build_column_couple('f7ua', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UA', end = 2011)),  # vérifier <=2011
    build_column_couple('f7ub', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UB', end = 2011)),  # vérifier <=2011

# en 2013 et 2012, 7uc se rapporte à autre chose, réutilisation de la case
#    build_column_couple('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UC', end = 2011)),  # vérifier <=2011

    build_column_couple('f7uc', IntCol(entity = 'foy',
                    label = u"Cotisations pour la défense des forêts contre l'incendie ",
                    val_type = "monetary",
                    cerfa_field = u'7UC',
                    start = 2012)),

    build_column_couple('f7ui', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UI', end = 2011)),  # vérifier <=2011
    build_column_couple('f7uj', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UJ', end = 2011)),  # vérifier <=2011
    build_column_couple('f7qb', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QB', end = 2011)),  # vérifier <=2011
    build_column_couple('f7qc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QC', end = 2011)),  # vérifier <=2011
    build_column_couple('f7qd', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QD', end = 2011)),  # vérifier <=2011
    build_column_couple('f7ql', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QL', end = 2011)),  # vérifier <=2011
    build_column_couple('f7qt', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QT', end = 2011)),  # vérifier <=2011
    build_column_couple('f7qm', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QM', end = 2011)),  # vérifier <=2011

    # Souscription de parts de fonds communs de placement dans l'innovation,
    # de fonds d'investissement de proximité
    build_column_couple('f7gq', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds communs de placement dans l'innovation",
                    val_type = "monetary",
                    cerfa_field = u'7GQ')),

    build_column_couple('f7fq', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité",
                    val_type = "monetary",
                    cerfa_field = u'7FQ')),

    build_column_couple('f7fm', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse",
                    val_type = "monetary",
                    cerfa_field = u'7FM')),

    build_column_couple('f7fl', IntCol(entity = 'foy',
                    label = u"Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer",
                    val_type = "monetary",
                    cerfa_field = u'7FL')),

    # Souscriptions au capital de SOFICA
    # Différence de % selon l'année pour le sofica, mais il se peut que cela n'ait aucun impact (si les param sont bons) puisque les cases ne changent pas
#     build_column_couple('f7gn', IntCol(entity = 'foy',
#                     label = u"Souscriptions au capital de SOFICA 48 %",
#                     val_type = "monetary",
#                     cerfa_field = u'7GN',
#                     end = 2011)),  # TODO: vérifier <=2011
#     build_column_couple('f7fn', IntCol(entity = 'foy',
#                     label = u"Souscriptions au capital de SOFICA 40 %",
#                     val_type = "monetary",
#                     cerfa_field = u'7FN',
#                     end = 2011)),  # TODO: vérifier <=2011

    build_column_couple('f7gn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 36 %",
                    val_type = "monetary",
                    cerfa_field = u'7GN',
                    start = 2012)),

    build_column_couple('f7fn', IntCol(entity = 'foy',
                    label = u"Souscriptions au capital de SOFICA 30 %",
                    val_type = "monetary",
                    cerfa_field = u'7FN',
                    start = 2012)),

    # Intérêts d'emprunt pour reprise de société
    build_column_couple('f7fh', IntCol(entity = 'foy', label = u"Intérêts d'emprunt pour reprise de société", val_type = "monetary")),

    # Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)),
    build_column_couple('f7ff', IntCol(entity = 'foy', label = u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)", val_type = "monetary")),
    build_column_couple('f7fg', IntCol(entity = 'foy', label = u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations")),

    # Travaux de conservation et de restauration d’objets classés monuments historiques
    build_column_couple('f7nz', IntCol(entity = 'foy', label = u"Travaux de conservation et de restauration d’objets classés monuments historiques", val_type = "monetary")),

    # Dépenses de protection du patrimoine naturel
    build_column_couple('f7ka', IntCol(entity = 'foy', label = u"Dépenses de protection du patrimoine naturel", val_type = "monetary")),

    # Intérêts d'emprunts
#    build_column_couple('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary")),

    # Intérêts des prêts à la consommation (case UH)),
    build_column_couple('f7uh', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # Investissements forestiers
    build_column_couple('f7un', IntCol(entity = 'foy', label = u"Investissements forestiers: acquisition", val_type = "monetary")),

    # Intérêts pour paiement différé accordé aux agriculteurs
    build_column_couple('f7um', IntCol(entity = 'foy', label = u"Intérêts pour paiement différé accordé aux agriculteurs", val_type = "monetary")),

    # Investissements locatifs neufs : Dispositif Scellier:
    build_column_couple('f7hj', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole", val_type = "monetary")),
    build_column_couple('f7hk', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM", val_type = "monetary")),
    build_column_couple('f7hn', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier", val_type = "monetary")),
    build_column_couple('f7ho', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier", val_type = "monetary")),
    build_column_couple('f7hl', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)", val_type = "monetary")),
    build_column_couple('f7hm', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds", val_type = "monetary")),
    build_column_couple('f7hr', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 (métropole et DOM ne respectant pas les plafonds)", val_type = "monetary")),
    build_column_couple('f7hs', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM et respectant les plafonds", val_type = "monetary")),
    build_column_couple('f7la', IntCol(entity = 'foy', label = u"Investissements locatifs neufs dispositif Scellier: report du solde de réduction d'impôt non encore imputé", val_type = "monetary")),

    # Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
    build_column_couple('f7ij', IntCol(entity = 'foy', label = u"Investissement destinés à la location meublée non professionnelle: engagement de réalisation de l'investissement en n-1", val_type = "monetary")),
    build_column_couple('f7il', IntCol(entity = 'foy', label = u"Investissement destinés à la location meublée non professionnelle: promesse d'achat en n-2", val_type = "monetary")),
    build_column_couple('f7im', IntCol(entity = 'foy', label = u"Investissement destinés à la location meublée non professionnelle: promesse d'achat en n-3", val_type = "monetary")),
    build_column_couple('f7ik', IntCol(entity = 'foy', label = u"Reports de 1/9 de l'investissement réalisé et achevé au cours de l'année n-4", val_type = "monetary")),
    build_column_couple('f7is', IntCol(entity = 'foy', label = u"Report du solde de réduction d'impôt non encor imputé: année  n-4", val_type = "monetary")),

    # Investissements locatifs dans les résidences de tourisme situées dans une zone de
    # revitalisation rurale
    build_column_couple('f7gt', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7xg', IntCol(entity = 'foy', label = u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme", val_type = "monetary")),
    build_column_couple('f7gu', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7gv', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # Avoir fiscaux et crédits d'impôt
    # f2ab déjà disponible
    build_column_couple('f8ta', IntCol(entity = 'foy', label = u"Retenue à la source en France ou impôt payé à l'étranger", val_type = "monetary")),
    build_column_couple('f8tb', IntCol(entity = 'foy', label = u"Crédit d'impôt recherche non encore remboursé", val_type = "monetary")),
    build_column_couple('f8tf', IntCol(entity = 'foy', label = u"Reprises de réductions ou de crédits d'impôt", val_type = "monetary")),
    build_column_couple('f8tg', IntCol(entity = 'foy', label = u"Crédits d'impôt en faveur des entreprises: Investissement en Corse", val_type = "monetary")),
    build_column_couple('f8th', IntCol(entity = 'foy', label = u"Retenue à la source élus locaux", val_type = "monetary")),
    build_column_couple('f8tc', IntCol(entity = 'foy', label = u"Crédit d'impôt recherche non encore remboursé (années antérieures)", val_type = "monetary")),
    build_column_couple('f8td', IntCol(entity = 'foy', label = u"Contribution exceptionnelle sur les hauts revenus")),
    build_column_couple('f8te', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé", val_type = "monetary")),
    build_column_couple('f8to', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures", val_type = "monetary")),
    build_column_couple('f8tp', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt", val_type = "monetary")),
    build_column_couple('f8uz', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Famille", val_type = "monetary")),
    build_column_couple('f8tz', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Apprentissage", val_type = "monetary")),
    build_column_couple('f8wa', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Agriculture biologique", val_type = "monetary")),
    build_column_couple('f8wb', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Prospection commerciale", val_type = "monetary")),
    build_column_couple('f8wc', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Nouvelles technologies", val_type = "monetary")),
    build_column_couple('f8wd', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise", val_type = "monetary")),
    build_column_couple('f8we', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Intéressement", val_type = "monetary")),
    build_column_couple('f8wr', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Métiers d'art", val_type = "monetary")),
    build_column_couple('f8ws', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes", val_type = "monetary")),
    build_column_couple('f8wt', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs", val_type = "monetary")),
    build_column_couple('f8wu', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Maître restaurateur", val_type = "monetary")),
    build_column_couple('f8wv', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Débitants de tabac", val_type = "monetary")),
    build_column_couple('f8wx', IntCol(entity = 'foy', label = u"Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise", val_type = "monetary")),
    build_column_couple('f8wy', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # Acquisition de biens culturels
    build_column_couple('f7uo', IntCol(entity = 'foy', label = u"Acquisition de biens culturels", val_type = "monetary")),


    # Mécénat d'entreprise
    build_column_couple('f7us', IntCol(entity = 'foy', label = u"Réduction d'impôt mécénat d'entreprise", val_type = "monetary")),

    # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
    # ('f7wf', IntCol() déjà disponible
    # ('f7wh', IntCol() déjà disponible
    # ('f7wk', IntCol() déjà disponible
    # ('f7wq', IntCol() déjà disponible
    build_column_couple('f7sb', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %", val_type = "monetary")),
    build_column_couple('f7sd', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 40 %", val_type = "monetary")),
    build_column_couple('f7se', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 50 %", val_type = "monetary")),
    build_column_couple('f7sh', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 15 %", val_type = "monetary")),
    # ('f7wg', IntCol() déjà disponible
    build_column_couple('f7sc', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???
    build_column_couple('f7up', IntCol(entity = 'foy', label = u"Crédit d'impôt", val_type = "monetary")),
    build_column_couple('f7uq', IntCol(entity = 'foy', label = u"Crédit d'impôt", val_type = "monetary")),

    # Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
    build_column_couple('f1ar', IntCol(entity = 'foy', label = u"Crédit d'impôt aide à la mobilité")),
    build_column_couple('f1br', IntCol(entity = 'foy', label = u"Crédit d'impôt aide à la mobilité")),
    build_column_couple('f1cr', IntCol(entity = 'foy', label = u"Crédit d'impôt aide à la mobilité")),
    build_column_couple('f1dr', IntCol(entity = 'foy', label = u"Crédit d'impôt aide à la mobilité")),
    build_column_couple('f1er', IntCol(entity = 'foy', label = u"Crédit d'impôt aide à la mobilité")),

    # Crédit d’impôt directive « épargne » (case 2BG)),
# TODO: double check or remove    build_column_couple('f2bg', IntCol(entity = 'foy', label = u"Crédit d’impôt directive « épargne »", val_type = "monetary")),

    # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
    build_column_couple('f4tq', IntCol(entity = 'foy', label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail", val_type = "monetary")),


    # Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
    # f7wf
    # f7wi
    # f7wj
    # f7wl
    build_column_couple('f7sf', IntCol(entity = 'foy', label = u"Appareils de régulation du chauffage, matériaux de calorifugeage", val_type = "monetary")),
    build_column_couple('f7si', IntCol(entity = 'foy', label = u"Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)", val_type = "monetary")),



    # Auto-entrepreneur : versements libératoires d’impôt sur le revenu
    build_column_couple('f8uy', IntCol(entity = 'foy', label = u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu", val_type = "monetary")),


    # Revenus des professions non salariées

    build_column_couple('frag_exon', IntCol(entity = 'ind', label = u"Revenus agricoles exonérés (régime du forfait)", val_type = "monetary")),  # (f5hn, f5in, f5jn)),
    build_column_couple('frag_impo', IntCol(entity = 'ind', label = u"Revenus agricoles imposables (régime du forfait)", val_type = "monetary")),  # (f5ho, f5io, f5jo)),
    build_column_couple('arag_exon', IntCol(entity = 'ind', label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hb, f5ib, f5jb)),
    build_column_couple('arag_impg', IntCol(entity = 'ind', label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hc, f5ic, f5jc)),
    build_column_couple('arag_defi', IntCol(entity = 'ind', label = u"Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hf, f5if, f5jf)),
    build_column_couple('nrag_exon', IntCol(entity = 'ind', label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hh, f5ih, f5jh)),
    build_column_couple('nrag_impg', IntCol(entity = 'ind', label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hi, f5ii, f5ji)),
    build_column_couple('nrag_defi', IntCol(entity = 'ind', label = u"Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hl, f5il, f5jl)),
    build_column_couple('nrag_ajag', IntCol(entity = 'ind', label = u"Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hm, f5im, f5jm)),

    # Autoentrepreneur
    build_column_couple('ebic_impv', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime auto-entrepreneur)", val_type = "monetary")),  # (f5ta, f5ua, f5va)),
    build_column_couple('ebic_imps', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)", val_type = "monetary")),  # (f5tb, f5ub, f5vb)),
    build_column_couple('ebnc_impo', IntCol(entity = 'ind', label = u"Revenus non commerciaux imposables (régime auto-entrepreneur)", val_type = "monetary")),  # (f5te, f5ue, f5ve)),

    build_column_couple('mbic_exon', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)", val_type = "monetary")),  # (f5kn, f5ln, f5mn)),
    build_column_couple('abic_exon', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5kb, f5lb, f5mb)),
    build_column_couple('nbic_exon', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5kh, f5lh, f5mh)),
    build_column_couple('mbic_impv', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)", val_type = "monetary")),  # (f5ko, f5lo, f5mo)),
    build_column_couple('mbic_imps', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)", val_type = "monetary")),  # (f5kp, f5lp, f5mp)),
    build_column_couple('abic_impn', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5kc, f5lc, f5mc)),
    build_column_couple('abic_imps', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5kd, f5ld, f5md)),
    build_column_couple('nbic_impn', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5ki, f5li, f5mi)),
    build_column_couple('nbic_imps', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux imposables: régime simplifié sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5kj, f5lj, f5mj)),
    build_column_couple('abic_defn', IntCol(entity = 'ind', label = u"Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5kf, f5lf, f5mf)),
    build_column_couple('abic_defs', IntCol(entity = 'ind', label = u"Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5kg, f5lg, f5mg)),
    build_column_couple('nbic_defn', IntCol(entity = 'ind', label = u"Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5kl, f5ll, f5ml)),
    build_column_couple('nbic_defs', IntCol(entity = 'ind', label = u"Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5km, f5lm, f5mm)),
    build_column_couple('nbic_apch', IntCol(entity = 'ind', label = u"Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5ks, f5ls, f5ms)),

    build_column_couple('macc_exon', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)", val_type = "monetary")),  # (f5nn, f5on, f5pn)),
    build_column_couple('aacc_exon', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5nb, f5ob, f5pb)),
    build_column_couple('nacc_exon', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5nh, f5oh, f5ph)),
    build_column_couple('macc_impv', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)", val_type = "monetary")),  # (f5no, f5oo, f5po)),
    build_column_couple('macc_imps', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)", val_type = "monetary")),  # (f5np, f5op, f5pp)),
    build_column_couple('aacc_impn', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5nc, f5oc, f5pc)),
    build_column_couple('aacc_imps', IntCol(entity = 'ind', label = u"Locations meublées non professionnelles (régime micro entreprise)", val_type = "monetary")),  # (f5nd, f5od, f5pd)),
    build_column_couple('aacc_defn', IntCol(entity = 'ind', label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5nf, f5of, f5pf)),
    build_column_couple('aacc_defs', IntCol(entity = 'ind', label = u"Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)", val_type = "monetary")),  # (f5ng, f5og, f5pg)),
    build_column_couple('nacc_impn', IntCol(entity = 'ind', label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5ni, f5oi, f5pi)),
    build_column_couple('nacc_imps', IntCol(entity = 'ind', label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)", val_type = "monetary")),  # (f5nj, f5oj, f5pj)),
    build_column_couple('nacc_defn', IntCol(entity = 'ind', label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5nl, f5ol, f5pl)),
    build_column_couple('nacc_defs', IntCol(entity = 'ind', label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5nm, f5om, f5pm)),
    build_column_couple('mncn_impo', IntCol(entity = 'ind', label = u"Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5ku, f5lu, f5mu)),
    build_column_couple('cncn_bene', IntCol(entity = 'ind', label = u"Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)", val_type = "monetary")),  # (f5sn, f5ns, f5os)),
    build_column_couple('cncn_defi', IntCol(entity = 'ind', label = u"Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)", val_type = "monetary")),  # (f5sp, f5nu, f5ou, f5sr)),

    build_column_couple('mbnc_exon', IntCol(entity = 'ind', label = u"Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5hp, f5ip, f5jp)),
    build_column_couple('abnc_exon', IntCol(entity = 'ind', label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type = "monetary")),  # (f5qb, f5rb, f5sb)),
    build_column_couple('nbnc_exon', IntCol(entity = 'ind', label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)", val_type = "monetary")),  # (f5qh, f5rh, f5sh)),
    build_column_couple('mbnc_impo', IntCol(entity = 'ind', label = u"Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5hq, f5iq, f5jq)),
    build_column_couple('abnc_impo', IntCol(entity = 'ind', label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type = "monetary")),  # (f5qc, f5rc, f5sc)),
    build_column_couple('abnc_defi', IntCol(entity = 'ind', label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type = "monetary")),  # (f5qe, f5re, f5se)),
    build_column_couple('nbnc_impo', IntCol(entity = 'ind', label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)", val_type = "monetary")),  # (f5qi, f5ri, f5si)),
    build_column_couple('nbnc_defi', IntCol(entity = 'ind', label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée. Revenus ne bénéficiant pas de l'abattement association agrée)", val_type = "monetary")),  # (f5qk, f5rk, f5sk)),

    build_column_couple('mbic_mvct', IntCol(entity = 'foy', label = u"Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)", val_type = "monetary")),  # (f5hu)),
    build_column_couple('macc_mvct', IntCol(entity = 'foy', label = u"Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)", val_type = "monetary")),  # (f5iu)),
    build_column_couple('mncn_mvct', IntCol(entity = 'foy', label = u"Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5ju)),
    build_column_couple('mbnc_mvct', IntCol(entity = 'foy', label = u"Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5kz

    build_column_couple('frag_pvct', IntCol(entity = 'ind', label = u"Plus-values agricoles  à court terme (régime du forfait)", val_type = "monetary")),  # (f5hw, f5iw, f5jw)),
    build_column_couple('mbic_pvct', IntCol(entity = 'ind', label = u"Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)", val_type = "monetary")),  # (f5kx, f5lx, f5mx)),
    build_column_couple('macc_pvct', IntCol(entity = 'ind', label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)", val_type = "monetary")),  # (f5nx, f5ox, f5px)),
    build_column_couple('mbnc_pvct', IntCol(entity = 'ind', label = u"Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5hv, f5iv, f5jv)),
    build_column_couple('mncn_pvct', IntCol(entity = 'ind', label = u"Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5ky, f5ly, f5my)),

    build_column_couple('mbic_mvlt', IntCol(entity = 'ind', label = u"Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)", val_type = "monetary")),  # (f5kr, f5lr, f5mr)),
    build_column_couple('macc_mvlt', IntCol(entity = 'ind', label = u"Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)", val_type = "monetary")),  # (f5nr, f5or, f5pr)),
    build_column_couple('mncn_mvlt', IntCol(entity = 'ind', label = u"Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5kw, f5lw, f5mw)),
    build_column_couple('mbnc_mvlt', IntCol(entity = 'ind', label = u"Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5hs, f5is, f5js)),

    build_column_couple('frag_pvce', IntCol(entity = 'ind', label = u"Plus-values agricoles de cession taxables à 16% (régime du forfait)", val_type = "monetary")),  # (f5hx, f5ix, f5jx)),
    build_column_couple('arag_pvce', IntCol(entity = 'ind', label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5he, f5ie, f5je)),
    build_column_couple('nrag_pvce', IntCol(entity = 'ind', label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)", val_type = "monetary")),  # (f5hk, f5lk, f5jk)),
    build_column_couple('mbic_pvce', IntCol(entity = 'ind', label = u"Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)", val_type = "monetary")),  # (f5kq, f5lq, f5mq)),
    build_column_couple('abic_pvce', IntCol(entity = 'ind', label = u"Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5ke, f5le, f5me)),
    build_column_couple('nbic_pvce', IntCol(entity = 'ind', label = u"Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)", val_type = "monetary")),  # (f5kk, f5ik, f5mk)),
    build_column_couple('macc_pvce', IntCol(entity = 'ind', label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)", val_type = "monetary")),  # (f5nq, f5oq, f5pq)),
    build_column_couple('aacc_pvce', IntCol(entity = 'ind', label = u"Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)", val_type = "monetary")),  # (f5ne, f5oe, f5pe)),
    build_column_couple('nacc_pvce', IntCol(entity = 'ind', label = u"Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5nk, f5ok, f5pk)),
    build_column_couple('mncn_pvce', IntCol(entity = 'ind', label = u"Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5kv, f5lv, f5mv)),
    build_column_couple('cncn_pvce', IntCol(entity = 'ind', label = u"Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)", val_type = "monetary")),  # (f5so, f5nt, f5ot)),
    build_column_couple('mbnc_pvce', IntCol(entity = 'ind', label = u"Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)", val_type = "monetary")),  # (f5hr, f5ir, f5jr)),
    build_column_couple('abnc_pvce', IntCol(entity = 'ind', label = u"Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée. Revenus bénéficiant de l'abattement association agrée ou viseur)", val_type = "monetary")),  # (f5qd, f5rd, f5sd)),
    build_column_couple('nbnc_pvce', IntCol(entity = 'ind', label = u"Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)", val_type = "monetary")),  # (f5qj, f5rj, f5sj)),

# pfam only
    build_column_couple('inactif', BoolCol(entity = 'fam',
                        label = u"Parent incatif (PAJE-CLCA)")),

    build_column_couple('partiel1', BoolCol(entity = 'fam',
                         label = u"Parent actif à moins de 50% (PAJE-CLCA)")),

    build_column_couple('partiel2', BoolCol(entity = 'fam',
                         label = u"Parent actif entre 50% et 80% (PAJE-CLCA)")),

    build_column_couple('categ_inv', IntCol(label = u"Catégorie de handicap (AEEH)")),

    build_column_couple('opt_colca', BoolCol(entity = 'fam',
                          label = u"Opte pour le COLCA")),

    build_column_couple('empl_dir', BoolCol(entity = 'fam',
                         label = u"Emploi direct (CLCMG)")),

    build_column_couple('ass_mat', BoolCol(entity = 'fam',
                        label = u"Assistante maternelle (CLCMG)")),

    build_column_couple('gar_dom', BoolCol(entity = 'fam',
                        label = u"Garde à domicile (CLCMG)")),

# zones apl and calibration
    build_column_couple('tu99', EnumCol(label = u"Tranche d'unité urbaine",
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

    build_column_couple('tau99', EnumCol(label = u"tranche d'aire urbaine",
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

    build_column_couple('reg', EnumCol(label = u"Région",
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

    build_column_couple('pol99', EnumCol(label = u"Catégorie de la commune au sein du découpage en aires et espaces urbains",
                      entity = 'men',
                      enum = Enum([u"Commune appartenant à un pôle urbain",
                                   u"Commune monopolarisée (appartenant à une couronne périurbaine",
                                   u"Commune monopolarisée",
                                   u"Espace à dominante rurale"]),
                      survey_only = True)),

    build_column_couple('cstotpragr', EnumCol(label = u"catégorie socio_professionelle agrégée de la personne de référence",
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

    build_column_couple('naf16pr', EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence",
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

    build_column_couple('nafg17npr', EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence ",
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


#    build_column_couple('typmen15', EnumCol(label = u"Type de ménage",
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

    build_column_couple('ageq', EnumCol(label = u"âge quinquennal de la personne de référence",
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


#    build_column_couple('nbinde', EnumCol(label = u"taille du ménage",
#                     entity = 'men',
#                     enum = Enum([u"Une personne",
#                                  u"Deux personnes",
#                                  u"Trois personnes",
#                                  u"Quatre personnes",
#                                  u"Cinq personnes",
#                                  u"Six personnes et plus"], start = 1))),

    build_column_couple('ddipl', EnumCol(label = u"diplôme de la personne de référence",
                    entity = 'men',
                    enum = Enum([u"Non renseigné"
                                 u"Diplôme supérieur",
                                 u"Baccalauréat + 2 ans",
                                 u"Baccalauréat ou brevet professionnel ou autre diplôme de ce niveau",
                                 u"CAP, BEP ou autre diplôme de ce niveau",
                                 u"Brevet des collèges",
                                 u"Aucun diplôme ou CEP"], start = 1),
                    survey_only = True)),

    build_column_couple('act5', EnumCol(label = u"activité",
                     enum = Enum([u"Salarié",
                                  u"Indépendant",
                                  u"Chômeur",
                                  u"Retraité",
                                  u"Inactif"], start = 1),
                    survey_only = True)),  # 5 postes normalement TODO: check = 0

    build_column_couple('wprm_init', FloatCol(label = u"Effectifs", survey_only = True)),

# # ISF ##

# # Immeubles bâtis ##
    build_column_couple('b1ab', IntCol(entity = 'foy', label = u"valeur résidence principale avant abattement", val_type = "monetary")),  # #  valeur résidence principale avant abattement ##
    build_column_couple('b1ac', IntCol(entity = 'foy', label = u"valeur autres immeubles avant abattement", val_type = "monetary")),
# # non bâtis ##
    build_column_couple('b1bc', IntCol(entity = 'foy', label = u"Immeubles non bâtis: bois, fôrets et parts de groupements forestiers", val_type = "monetary")),
    build_column_couple('b1be', IntCol(entity = 'foy', label = u"Immeubles non bâtis: biens ruraux loués à long termes", val_type = "monetary")),
    build_column_couple('b1bh', IntCol(entity = 'foy', label = u"Immeubles non bâtis: parts de groupements fonciers agricoles et de groupements agricoles fonciers", val_type = "monetary")),
    build_column_couple('b1bk', IntCol(entity = 'foy', label = u"Immeubles non bâtis: autres biens", val_type = "monetary")),

# # droits sociaux- valeurs mobilières-liquidités- autres meubles ##
    build_column_couple('b1cl', IntCol(entity = 'foy', label = u"Parts et actions détenues par les salariés et mandataires sociaux", val_type = "monetary")),
    build_column_couple('b1cb', IntCol(entity = 'foy', label = u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum", val_type = "monetary")),
    build_column_couple('b1cd', IntCol(entity = 'foy', label = u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité", val_type = "monetary")),
    build_column_couple('b1ce', IntCol(entity = 'foy', label = u"Autres valeurs mobilières", val_type = "monetary")),
    build_column_couple('b1cf', IntCol(entity = 'foy', label = u"Liquidités", val_type = "monetary")),
    build_column_couple('b1cg', IntCol(entity = 'foy', label = u"Autres biens meubles", val_type = "monetary")),

    build_column_couple('b1co', IntCol(entity = 'foy', label = u"Autres biens meubles: contrats d'assurance-vie", val_type = "monetary")),

#    b1ch
#    b1ci
#    b1cj
#    b1ck


# # passifs et autres réduc ##
    build_column_couple('b2gh', IntCol(entity = 'foy', label = u"Total du passif et autres déductions", val_type = "monetary")),

# # réductions ##
    build_column_couple('b2mt', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary")),
    build_column_couple('b2ne', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary")),
    build_column_couple('b2mv', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings" , val_type = "monetary")),
    build_column_couple('b2nf', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings", val_type = "monetary")),
    build_column_couple('b2mx', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FIP", val_type = "monetary")),
    build_column_couple('b2na', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FCPI ou FCPR", val_type = "monetary")),
    build_column_couple('b2nc', IntCol(entity = 'foy', label = u"Réductions pour dons à certains organismes d'intérêt général", val_type = "monetary")),

# #  montant impôt acquitté hors de France ##
    build_column_couple('b4rs', IntCol(entity = 'foy', label = u"Montant de l'impôt acquitté hors de France", val_type = "monetary")),

# # BOUCLIER FISCAL ##

    build_column_couple('rev_or', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('rev_exo', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    build_column_couple('tax_fonc', IntCol(entity = 'foy', label = u"Taxe foncière", val_type = "monetary")),
    build_column_couple('restit_imp', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # to remove
    build_column_couple('champm', BoolCol(entity = 'men',
                       default = True,
                       survey_only = True,
                       )),

    build_column_couple('wprm', FloatCol(entity = 'men',
                      default = 1,
                      label = u"Effectifs",
                      survey_only = True,
                      )),

    build_column_couple('etr', IntCol()),
    build_column_couple('coloc', BoolCol(label = u"Vie en colocation")),
    build_column_couple('csg_rempl', EnumCol(label = u"Taux retenu sur la CSG des revenus de remplacment",
                 entity = 'ind',
                 enum = Enum([u"Non renseigné/non pertinent",
                              u"Exonéré",
                              u"Taux réduit",
                              u"Taux plein"]),
                default = 3)),

    build_column_couple('aer', IntCol(label = u"Allocation équivalent retraite (AER)")),  # L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
    build_column_couple('ass', IntCol(label = u"Allocation de solidarité spécifique (ASS)")),
    build_column_couple('f5sq', IntCol()),

    build_column_couple('m_afeamam', IntCol(entity = 'men', survey_only = True)),
    build_column_couple('m_agedm', IntCol(entity = 'men', survey_only = True)),
    build_column_couple('m_clcam', IntCol(entity = 'men', survey_only = True)),
    build_column_couple('m_colcam', IntCol(entity = 'men', survey_only = True)),
    build_column_couple('m_mgamm', IntCol(entity = 'men', survey_only = True)),
    build_column_couple('m_mgdomm', IntCol(entity = 'men', survey_only = True)),
    build_column_couple('zthabm', IntCol(entity = 'men')),  # TODO: Devrait être renommée tax_hab

    build_column_couple('adoption', BoolCol(entity = "ind", label = u"Enfant adopté")),

    # ('tax_hab', IntCol()),
    ))
