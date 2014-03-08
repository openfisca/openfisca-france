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

    build_column_couple('sali', IntCol(label = u"Salaire imposable",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AJ",
                                   QUIFOY['conj']: u"1BJ",
                                   QUIFOY['pac1']: u"1CJ",
                                   QUIFOY['pac2']: u"1DJ",
                                   QUIFOY['pac3']: u"1EJ",
                                   })),  # (f1aj, f1bj, f1cj, f1dj, f1ej)
    build_column_couple('choi', IntCol(label = u"Chômage imposable",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AP",
                                   QUIFOY['conj']: u"1BP",
                                   QUIFOY['pac1']: u"1CP",
                                   QUIFOY['pac2']: u"1DP",
                                   QUIFOY['pac3']: u"1EP",
                                   })),  # (f1ap, f1bp, f1cp, f1dp, f1ep)
    build_column_couple('rsti', IntCol(label = u"Retraite imposable",
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

    build_column_couple('alr', IntCol(label = u"Pension alimentaire reçue",
                   val_type = "monetary",
                   cerfa_field = {QUIFOY['vous']: u"1AO",
                                  QUIFOY['conj']: u"1BO",
                                  QUIFOY['pac1']: u"1CO",
                                  QUIFOY['pac2']: u"1DO",
                                  QUIFOY['pac3']: u"1EO",
                                  })),  # (f1ao, f1bo, f1co, f1do, f1eo)
    build_column_couple('alr_decl', BoolCol(label = u"Pension déclarée", default = True)),

    build_column_couple('hsup', IntCol(label = u"Heures supplémentaires",
                    val_type = "monetary",
                    cerfa_field = {QUIFOY['vous']: u"1AU",
                                   QUIFOY['conj']: u"1BU",
                                   QUIFOY['pac1']: u"1CU",
                                   QUIFOY['pac2']: u"1DU",
                                   QUIFOY['pac3']: u"1EU",
                                   })),  # (f1au, f1bu, f1cu, f1du, f1eu)

    build_column_couple('inv', BoolCol(label = u'Invalide')),  # TODO: cerfa_field

    build_column_couple('alt', BoolCol(label = u'Enfant en garde alternée')),  # TODO: cerfa_field

    build_column_couple('cho_ld', BoolCol(label = u"Chômeur de longue durée",
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
                        label = u"Jours décomptés au tire de cette déclaration")),
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
    build_column_couple('nbH', IntCol(label = u"Nombre d'enfants à charge en résidence alternée, non mariés de moins de 18 ans au 1er janvier de l'année n-1, ou nés en n-1 ou handicapés quel que soit l'âge",
                   entity = 'foy',
                   cerfa_field = u'H')),
# TODO: vérifier si c'est bien ça pour la nbH et la caseH qui suit
    build_column_couple('nbG', IntCol(label = u"Nombre d'enfants à charge titulaires de la carte d'invalidité",
                   entity = 'foy',
                   cerfa_field = u'G')),
    build_column_couple('nbF', IntCol(label = u"Nombre d'enfants à charge  non mariés de moins de 18 ans au 1er janvier de l'année n-1, ou nés en n-1 ou handicapés quel que soit l'âge",
                   entity = 'foy',
                   cerfa_field = u'F')),
    build_column_couple('nbN', IntCol(label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille",
                   entity = 'foy',
                   cerfa_field = u'N')),

    build_column_couple('caseE', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: enfant élevé seul pendant moins de 5 ans",
                      entity = 'foy',
                      cerfa_field = u'E')),
    build_column_couple('caseF', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: conjoint titulaire d'une pension ou d'une carte d'invalidité(vivant ou décédé l'année précédente",
                      entity = 'foy',
                      cerfa_field = u'F')),
    build_column_couple('caseG', BoolCol(label = u"Titulaire d'une pension de veuve de guerre",
                      entity = 'foy',
                      cerfa_field = u'G')),
    build_column_couple('caseH', IntCol(label = u"Année de naissance des enfants à charge en garde alternée", entity = 'foy',
                     cerfa_field = u'H')),
    build_column_couple('caseK', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre",
                      entity = 'foy',
                      cerfa_field = u'K')),
    build_column_couple('caseL', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: enfant élevé seul pendant plus de 5 ans",
                      entity = 'foy',
                      cerfa_field = u'L')),
    build_column_couple('caseN', BoolCol(label = u"Vous ne vivez pas seul au 1er janvier de l'année n-1",
                      entity = 'foy',
                      cerfa_field = u'N')),
    build_column_couple('caseP', BoolCol(label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%",
                      entity = 'foy',
                      cerfa_field = u'P')),
    build_column_couple('caseS', BoolCol(label = u"Vous ou votre conjoint êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                      entity = 'foy',
                      cerfa_field = u'S')),
    build_column_couple('caseT', BoolCol(label = u"Vous êtes parent isolé au 1er janvier de l'année n-1",
                      entity = 'foy',
                      cerfa_field = u'T')),
    build_column_couple('caseW', BoolCol(label = u"Votre conjoint âgé de plus de 75 ans, décédé en n-1 était titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                      entity = 'foy',
                      cerfa_field = u'W')),

    build_column_couple('rfr_n_2', IntCol(entity = 'foy', label = u"Revenu fiscal de référence année n-2", val_type = "monetary")),  # TODO: provide in data
    build_column_couple('nbptr_n_2', IntCol(entity = 'foy', label = u"Nombre de parts année n-2", val_type = "monetary")),  # TODO: provide in data

    # Rentes viagères
    build_column_couple('f1aw', IntCol(label = u"Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : Moins de 50 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1AW')),
    build_column_couple('f1bw', IntCol(label = u"Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : De 50 à 59 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1BW')),
    build_column_couple('f1cw', IntCol(label = u"Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : De 60 à 69 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1CW')),
    build_column_couple('f1dw', IntCol(label = u"Rentes viagères à titre onéreux perçu par le foyer par âge d'entrée en jouissance : A partir de 70 ans",
                    entity = 'foy',
                    val_type = "monetary",
                    cerfa_field = u'1DW')),

    # Gain de levée d'option
    # TODO: Labels des gains de levée d'option
    # j'ai changé là mais pas dans le code, il faut chercher les f1uv
    # et les mettre en f1tvm comme pour sali
    # Il faut aussi le faire en amont dans les tables
    build_column_couple('f1tv', IntCol(label = u"", entity = 'ind')),  # (f1tv,f1uv)),
    build_column_couple('f1tw', IntCol(label = u"", entity = 'ind')),  # (f1tw,f1uw)),
    build_column_couple('f1tx', IntCol(label = u"", entity = 'ind')),  # (f1tx,f1ux)),


    # RVCM
    # revenus au prélèvement libératoire
    build_column_couple('f2da', IntCol(entity = 'foy', label = u"Revenus des actions et parts soumis au prélèvement libératoire",
                    val_type = "monetary",
                    cerfa_field = u'2DA')),
    build_column_couple('f2dh', IntCol(entity = 'foy',
                    label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire",
                    val_type = "monetary",
                    cerfa_field = u'2DH')),
    build_column_couple('f2ee', IntCol(entity = 'foy',
                    label = u"Revenus au prélèvement libératoire hors actions et assurance-vie",
                    val_type = "monetary",
                    cerfa_field = u'2EE')),

    # revenus ouvrant droit à abattement
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

    # Revenus n'ouvrant pas droit à abattement
    build_column_couple('f2ts', IntCol(entity = 'foy', label = u"Revenus de valeurs mobilières et distributions",
                    val_type = "monetary",
                    cerfa_field = u'2TS')),
    build_column_couple('f2go', IntCol(entity = 'foy',
                    label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié",
                    val_type = "monetary",
                    cerfa_field = u'2GO')),
    build_column_couple('f2tr', IntCol(entity = 'foy', label = u"Intérêts et autres revenus assimilés",
                    val_type = "monetary",
                    cerfa_field = u'2TR')),

    # Autres
    build_column_couple('f2cg', IntCol(entity = 'foy', label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible", val_type = "monetary")),
    build_column_couple('f2bh', IntCol(entity = 'foy', label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible", val_type = "monetary")),
    build_column_couple('f2ca', IntCol(entity = 'foy', label = u"Frais venant en déduction", val_type = "monetary")),
    build_column_couple('f2aa', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2006", val_type = "monetary")),
    build_column_couple('f2ab', IntCol(entity = 'foy', label = u"Crédits d'impôt sur valeurs étrangères", val_type = "monetary")),
    build_column_couple('f2al', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2007", val_type = "monetary")),
    build_column_couple('f2am', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2008", val_type = "monetary")),
    build_column_couple('f2an', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2009", val_type = "monetary")),
    build_column_couple('f2aq', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2010", val_type = "monetary")),
    build_column_couple('f2ar', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2011", val_type = "monetary")),
    build_column_couple('f2as', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2012", val_type = "monetary")),

    # non accessible (from previous years)
    build_column_couple('f2gr', IntCol(entity = 'foy')),

    build_column_couple('f3vc', IntCol(entity = 'foy', label = u"Produits et plus-values exonérés provenant de structure de capital-risque", val_type = "monetary")),
    build_column_couple('f3vd', IntCol(entity = 'foy', label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 18 %", val_type = "monetary")),
    build_column_couple('f3ve', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f3vf', IntCol(entity = 'foy', label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 41 %", val_type = "monetary")),

    build_column_couple('f3vl', IntCol(entity = 'foy', label = u"Distributions par des sociétés de capital-risque taxables à 24 %", val_type = "monetary")),
    build_column_couple('f3vi', IntCol(entity = 'foy', label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions gratuites taxables à 30 %", val_type = "monetary")),
    build_column_couple('f3vm', IntCol(entity = 'foy', label = u"Clôture du PEA : avant l'expiration de la 2e année", val_type = "monetary")),

    build_column_couple('f3vj', IntCol(entity = 'foy', label = u"Gains imposables sur option dans la catégorie des salaires: déclarant 1", val_type = "monetary")),
    build_column_couple('f3vk', IntCol(entity = 'foy', label = u"Gains imposables sur option dans la catégorie des salaires: déclarant 2", val_type = "monetary")),
    build_column_couple('f3va', IntCol(entity = 'foy', label = u"Abattement net pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values", val_type = "monetary")),

    # Plus values et gains taxables à des taux forfaitaires
    build_column_couple('f3vg', IntCol(entity = 'foy', label = u"Plus-values de cession de valeurs mobilières, droits sociaux et gains assimilés", val_type = "monetary")),
    build_column_couple('f3vh', IntCol(entity = 'foy', label = u"Perte de l'année n-1", val_type = "monetary")),
    build_column_couple('f3vt', IntCol(entity = 'foy', label = u"Clôture du PEA : entre la 2e et la 5e année", val_type = "monetary")),
    build_column_couple('f3vu', IntCol(entity = 'foy')),
    build_column_couple('f3vv', IntCol(entity = 'foy')),

    build_column_couple('f3si', IntCol(entity = 'foy')),  # TODO: parmi ces cas créer des valeurs individuelles
    build_column_couple('f3sa', IntCol(entity = 'foy')),
    build_column_couple('f3sf', IntCol(entity = 'foy')),
    build_column_couple('f3sd', IntCol(entity = 'foy')),

    build_column_couple('f3vz', IntCol(entity = 'foy', label = u"Plus-values imposables de cession d’immeubles ou de biens meubles", val_type = "monetary")),  # Revenus 2011

    # Revenu foncier
    build_column_couple('f4ba', IntCol(entity = 'foy', label = u"Revenus fonciers imposables", val_type = "monetary")),
    build_column_couple('f4bb', IntCol(entity = 'foy', label = u"Déficit imputable sur les revenus fonciers", val_type = "monetary")),
    build_column_couple('f4bc', IntCol(entity = 'foy', label = u"Déficit imputable sur le revenu global", val_type = "monetary")),
    build_column_couple('f4bd', IntCol(entity = 'foy', label = u"Déficits antérieurs non encore imputés", val_type = "monetary")),
    build_column_couple('f4be', IntCol(entity = 'foy', label = u"Micro foncier: recettes brutes sans abattement", val_type = "monetary")),

    # Prime d'assurance loyers impayés
    build_column_couple('f4bf', IntCol(entity = 'foy', label = u"Primes d'assurance pour loyers impayés des locations conventionnées", val_type = "monetary")),

    build_column_couple('f4bl', IntCol(entity = 'foy', label = u"")),

    build_column_couple('f5qm', IntCol(entity = 'foy', label = u"Agents généraux d’assurances: indemnités de cessation d’activité, déclarant 1", val_type = "monetary")),
    build_column_couple('f5rm', IntCol(entity = 'foy', label = u"Agents généraux d’assurances: indemnités de cessation d’activité, déclarant 2", val_type = "monetary")),

    # Csg déductible
    build_column_couple('f6de', IntCol(entity = 'foy', label = u"CSG déductible calculée sur les revenus du patrimoine", val_type = "monetary")),

    # Pensions alimentaires
    build_column_couple('f6gi', IntCol(entity = 'foy', label = u"Pensions alimentaires versées à des enfants majeurs: 1er enfant", val_type = "monetary")),
    build_column_couple('f6gj', IntCol(entity = 'foy', label = u"Pensions alimentaires versées à des enfants majeurs: 2eme enfant", val_type = "monetary")),
    build_column_couple('f6el', IntCol(entity = 'foy', label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant", val_type = "monetary")),
    build_column_couple('f6em', IntCol(entity = 'foy', label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant", val_type = "monetary")),
    build_column_couple('f6gp', IntCol(entity = 'foy', label = u"Autres pensions alimentaires versées (mineurs, ascendants)", val_type = "monetary")),
    build_column_couple('f6gu', IntCol(entity = 'foy', label = u"Autres pensions alimentaires versées (mineurs, ascendants)", val_type = "monetary")),

    # Frais d'accueil d'une personne de plus de 75 ans dans le besoin
    build_column_couple('f6eu', IntCol(entity = 'foy', label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin", val_type = "monetary")),
    build_column_couple('f6ev', IntCol(entity = 'foy', label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit")),

    # Déductions diverses
    build_column_couple('f6dd', IntCol(entity = 'foy', label = u"Déductions diverses", val_type = "monetary")),

    # Épargne retraite - PERP, PRÉFON, COREM et CGOS
    build_column_couple('f6ps', IntCol(entity = 'foy', label = u"Plafond de déduction: déclarant 1", val_type = "monetary")),
    build_column_couple('f6rs', IntCol(entity = 'foy', label = u"Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: déclarant 1", val_type = "monetary")),
    build_column_couple('f6ss', IntCol(entity = 'foy', label = u"Rachat de cotisations PREFON, COREM et C.G.O.S: déclarant 1", val_type = "monetary")),
    build_column_couple('f6pt', IntCol(entity = 'foy', label = u"Plafond de déduction: déclarant 2", val_type = "monetary")),
    build_column_couple('f6rt', IntCol(entity = 'foy', label = u"Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: déclarant 2", val_type = "monetary")),
    build_column_couple('f6st', IntCol(entity = 'foy', label = u"Rachat de cotisations PREFON, COREM et C.G.O.S: déclarant 2", val_type = "monetary")),
    build_column_couple('f6pu', IntCol(entity = 'foy', label = u"Plafond de déduction: personne à charge", val_type = "monetary")),
    build_column_couple('f6ru', IntCol(entity = 'foy', label = u"Cotisations versées au titre d'un PERP, PREFON, COREM et C.G.O.S: personne à charge", val_type = "monetary")),
    build_column_couple('f6su', IntCol(entity = 'foy', label = u"Rachat de cotisations PREFON, COREM et C.G.O.S: personne à charge", val_type = "monetary")),

    # Souscriptions en faveur du cinéma ou de l’audiovisuel
    build_column_couple('f6aa', IntCol(entity = 'foy', label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel", val_type = "monetary")),

    # Souscriptions au capital des SOFIPÊCHE
    build_column_couple('f6cc', IntCol(entity = 'foy', label = u"Souscriptions au capital des SOFIPÊCHE", val_type = "monetary")),

    # Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
    # ou Versements sur un compte épargne codéveloppement
    build_column_couple('f6eh', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # Pertes en capital consécutives à la souscription au capital de sociétés
    # nouvelles ou de sociétés en difficulté
    build_column_couple('f6da', IntCol(entity = 'foy', label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté", val_type = "monetary")),


    # Dépenses de grosses réparations effectuées par les nus propriétaires
    build_column_couple('f6cb', IntCol(entity = 'foy', label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires", val_type = "monetary")),  # TODO: before 2006 wasPertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)
    build_column_couple('f6hj', IntCol(entity = 'foy', label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures", val_type = "monetary")),
    build_column_couple('f6hl', IntCol(entity = 'foy', label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures", val_type = "monetary")),
    build_column_couple('f6hk', IntCol(entity = 'foy', label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures", val_type = "monetary")),

    # Sommes à rajouter au revenu imposable
    build_column_couple('f6gh', IntCol(entity = 'foy', label = u"Sommes à ajouter au revenu imposable", val_type = "monetary")),

    # Deficits antérieurs
    build_column_couple('f6fa', IntCol(entity = 'foy', label = u"Deficits globaux des années antérieures non encore déduits: année n-7", val_type = "monetary")),
    build_column_couple('f6fb', IntCol(entity = 'foy', label = u"Deficits globaux des années antérieures non encore déduits: année n-6", val_type = "monetary")),
    build_column_couple('f6fc', IntCol(entity = 'foy', label = u"Deficits globaux des années antérieures non encore déduits: année n-5", val_type = "monetary")),
    build_column_couple('f6fd', IntCol(entity = 'foy', label = u"Deficits globaux des années antérieures non encore déduits: année n-4", val_type = "monetary")),
    build_column_couple('f6fe', IntCol(entity = 'foy', label = u"Deficits globaux des années antérieures non encore déduits: année n-3", val_type = "monetary")),
    build_column_couple('f6fl', IntCol(entity = 'foy', label = u"Deficits globaux des années antérieures non encore déduits: année n-2", val_type = "monetary")),

    # Dons
    build_column_couple('f7ud', IntCol(entity = 'foy', label = u"Dons à des organismes d'aide aux personnes en difficulté", val_type = "monetary")),
    build_column_couple('f7uf', IntCol(entity = 'foy', label = u"Autres dons", val_type = "monetary")),
    build_column_couple('f7xs', IntCol(entity = 'foy', label = u"Report des années antérieures des réductions et crédits d'impôt: année n-6", val_type = "monetary")),
    build_column_couple('f7xt', IntCol(entity = 'foy', label = u"Report des années antérieures des réductions et crédits d'impôt: année n-5", val_type = "monetary")),
    build_column_couple('f7xu', IntCol(entity = 'foy', label = u"Report des années antérieures des réductions et crédits d'impôt: année n-4", val_type = "monetary")),
    build_column_couple('f7xw', IntCol(entity = 'foy', label = u"Report des années antérieures des réductions et crédits d'impôt: année n-3", val_type = "monetary")),
    build_column_couple('f7xy', IntCol(entity = 'foy', label = u"Report des années antérieures des réductions et crédits d'impôt: année n-2", val_type = "monetary")),

    # Cotisations syndicales des salariées et pensionnés
    build_column_couple('f7ac', IntCol(entity = 'foy', label = u"Cotisations syndicales des salariées et pensionnés: déclarant 1", val_type = "monetary")),
    build_column_couple('f7ae', IntCol(entity = 'foy', label = u"Cotisations syndicales des salariées et pensionnés: déclarant 2", val_type = "monetary")),
    build_column_couple('f7ag', IntCol(entity = 'foy', label = u"Cotisations syndicales des salariées et pensionnés: personne à charge", val_type = "monetary")),

    # Salarié à domicile
    build_column_couple('f7db', IntCol(entity = 'foy', label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi en n-1", val_type = "monetary")),
    build_column_couple('f7df', IntCol(entity = 'foy', label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives en n-1", val_type = "monetary")),
    build_column_couple('f7dq', BoolCol(entity = 'foy', label = u"Emploi direct pour la première fois d'un salarié à domicile en n-1")),
    build_column_couple('f7dg', BoolCol(entity = 'foy', label = u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'aumoins 80 % en n-1")),
    build_column_couple('f7dl', IntCol(entity = 'foy', label = u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées en n-1")),

    # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
    build_column_couple('f7vy', IntCol(entity = 'foy', label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité", val_type = "monetary")),
    build_column_couple('f7vz', IntCol(entity = 'foy', label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première suivante", val_type = "monetary")),
    build_column_couple('f7vx', IntCol(entity = 'foy', label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011", val_type = "monetary")),
    build_column_couple('f7vw', IntCol(entity = 'foy', label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010", val_type = "monetary")),

    # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    build_column_couple('f7cd', IntCol(entity = 'foy', label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne", val_type = "monetary")),
    build_column_couple('f7ce', IntCol(entity = 'foy', label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne", val_type = "monetary")),

    # Frais de garde des enfants de moins de 6 ans au 01/01/n-1
    build_column_couple('f7ga', IntCol(entity = 'foy', label = u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 1er enfant à charge", val_type = "monetary")),
    build_column_couple('f7gb', IntCol(entity = 'foy', label = u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 2ème enfant à charge", val_type = "monetary")),
    build_column_couple('f7gc', IntCol(entity = 'foy', label = u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 3ème enfant à charge", val_type = "monetary")),
    build_column_couple('f7ge', IntCol(entity = 'foy', label = u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 1er enfant à charge en résidence alternée", val_type = "monetary")),
    build_column_couple('f7gf', IntCol(entity = 'foy', label = u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 2ème enfant à charge en résidence alternée", val_type = "monetary")),
    build_column_couple('f7gg', IntCol(entity = 'foy', label = u"Frais de garde des enfants de moins de 6 ans au 01/01/n-1: 3ème enfant à charge en résidence alternée", val_type = "monetary")),

    # Nombre d'enfants à charge poursuivant leurs études
    build_column_couple('f7ea', IntCol(entity = 'foy', label = u"Nombre d'enfants à charge poursuivant leurs études au collège")),
    build_column_couple('f7eb', IntCol(entity = 'foy', label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège")),
    build_column_couple('f7ec', IntCol(entity = 'foy', label = u"Nombre d'enfants à charge poursuivant leurs études au lycée")),
    build_column_couple('f7ed', IntCol(entity = 'foy', label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée")),
    build_column_couple('f7ef', IntCol(entity = 'foy', label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur")),
    build_column_couple('f7eg', IntCol(entity = 'foy', label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur")),

    # Intérêts des prêts étudiants
    build_column_couple('f7td', IntCol(entity = 'foy', label = u"Intérêts des prêts étudiants versés avant l'année n-1", val_type = "monetary")),
    build_column_couple('f7vo', IntCol(entity = 'foy', label = u"Nombre d'années de remboursement du prêt étudiant avant l'année n-1")),
    build_column_couple('f7uk', IntCol(entity = 'foy', label = u"Intérêts des prêts étudiants versés en n-1", val_type = "monetary")),

    # Primes de rente survie, contrats d'épargne handicap
    build_column_couple('f7gz', IntCol(entity = 'foy', label = u"Primes de rente survie, contrats d'épargne handicap", val_type = "monetary")),

    # Prestations compensatoires
    build_column_couple('f7wm', IntCol(entity = 'foy', label = u"Prestations compensatoires: Capital fixé en substitution de rente", val_type = "monetary")),
    build_column_couple('f7wn', IntCol(entity = 'foy', label = u"Prestations compensatoires: Sommes versées en n-1", val_type = "monetary")),
    build_column_couple('f7wo', IntCol(entity = 'foy', label = u"Prestations compensatoires: Sommes totales décidées par jugement en n-1 ou capital reconstitué", val_type = "monetary")),
    build_column_couple('f7wp', IntCol(entity = 'foy', label = u"Prestations compensatoires: Report des sommes décidées en n-2", val_type = "monetary")),

    # Dépenses en faveur de la qualité environnementale de l'habitation principale
    build_column_couple('f7we', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise en n-1")),
    build_column_couple('f7wq', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées")),
    build_column_couple('f7wh', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: bouquet de travaux")),
    build_column_couple('f7wk', BoolCol(entity = 'foy', label = u"Votre habitation principale est une maison individuelle")),
    build_column_couple('f7wf', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1")),

    # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
    build_column_couple('f7wi', IntCol(entity = 'foy', label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction", val_type = "monetary")),
    build_column_couple('f7wj', IntCol(entity = 'foy', label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées", val_type = "monetary")),
    build_column_couple('f7wl', IntCol(entity = 'foy', label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques", val_type = "monetary")),

    # Investissements dans les DOM-TOM dans le cadre d'une entrepise
    build_column_couple('f7ur', IntCol(entity = 'foy', label = u"Investissements réalisés en n-1, total réduction d’impôt", val_type = "monetary")),
    build_column_couple('f7oz', IntCol(entity = 'foy', label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6", val_type = "monetary")),
    build_column_couple('f7pz', IntCol(entity = 'foy', label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-5", val_type = "monetary")),
    build_column_couple('f7qz', IntCol(entity = 'foy', label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-4", val_type = "monetary")),
    build_column_couple('f7rz', IntCol(entity = 'foy', label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3", val_type = "monetary")),
    build_column_couple('f7sz', IntCol(entity = 'foy', label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-2", val_type = "monetary")),

    # Aide aux créateurs et repreneurs d'entreprises
    build_column_couple('f7fy', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1")),
    build_column_couple('f7gy', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1")),
    build_column_couple('f7jy', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et ayant pris fin en n-1")),
    build_column_couple('f7hy', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1")),
    build_column_couple('f7ky', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1")),
    build_column_couple('f7iy', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et n'ayant pas pris fin en n-1")),
    build_column_couple('f7ly', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-2 et ayant pas pris fin en n-1")),
    build_column_couple('f7my', IntCol(entity = 'foy', label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-2 et ayant pas pris fin en n-1 ")),

    # Travaux de restauration immobilière
    build_column_couple('f7ra', IntCol(entity = 'foy', label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbail et paysager", val_type = "monetary")),
    build_column_couple('f7rb', IntCol(entity = 'foy', label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé", val_type = "monetary")),

    # Assurance-vie
    build_column_couple('f7gw', IntCol(entity = 'foy', label = u"")),
    build_column_couple('f7gx', IntCol(entity = 'foy', label = u"")),
    # ('f7gy', IntCol()), existe ailleurs

    # Investissements locatifs dans le secteur de touristique
    build_column_couple('f7xc', IntCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1", val_type = "monetary")),
    build_column_couple('f7xd', BoolCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans")),
    build_column_couple('f7xe', BoolCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans")),
    build_column_couple('f7xf', IntCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures", val_type = "monetary")),
    build_column_couple('f7xh', IntCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme", val_type = "monetary")),
    build_column_couple('f7xi', IntCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures", val_type = "monetary")),
    build_column_couple('f7xj', IntCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures", val_type = "monetary")),
    build_column_couple('f7xk', IntCol(entity = 'foy', label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures", val_type = "monetary")),
    build_column_couple('f7xl', IntCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans", val_type = "monetary")),
    build_column_couple('f7xm', IntCol(entity = 'foy', label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures", val_type = "monetary")),
    build_column_couple('f7xn', IntCol(entity = 'foy', label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: investissement réalisé en n-1", val_type = "monetary")),
    build_column_couple('f7xo', IntCol(entity = 'foy', label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures", val_type = "monetary")),

    # Souscriptions au capital des PME
    build_column_couple('f7cf', IntCol(entity = 'foy', label = u"Souscriptions au capital des PME non cotées, montant versé en n-1", val_type = "monetary")),
    build_column_couple('f7cl', IntCol(entity = 'foy', label = u"Souscriptions au capital des PME non cotées, report de versement de l'année n-4", val_type = "monetary")),
    build_column_couple('f7cm', IntCol(entity = 'foy', label = u"Souscriptions au capital des PME non cotées, report de versement de l'année n-3", val_type = "monetary")),
    build_column_couple('f7cn', IntCol(entity = 'foy', label = u"Souscriptions au capital des PME non cotées, report de versement de l'année n-2", val_type = "monetary")),
    build_column_couple('f7cu', IntCol(entity = 'foy', label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures", val_type = "monetary")),

    # Souscription au capital d’une SOFIPECHE
    build_column_couple('f7gs', IntCol(entity = 'foy', label = u"Souscription au capital d’une SOFIPECHE", val_type = "monetary")),

    # Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
    build_column_couple('f7ua', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7ub', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7ui', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7uj', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7qb', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7qc', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7qd', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7ql', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7qt', IntCol(entity = 'foy', label = u"", val_type = "monetary")),
    build_column_couple('f7qm', IntCol(entity = 'foy', label = u"", val_type = "monetary")),

    # Souscription de parts de fonds communs de placement dans l'innovation,
    # de fonds d'investissement de proximité
    build_column_couple('f7gq', IntCol(entity = 'foy', label = u"Souscription de parts de fonds communs de placement dans l'innovation", val_type = "monetary")),
    build_column_couple('f7fq', IntCol(entity = 'foy', label = u"Souscription de parts de fonds d'investissement de proximité", val_type = "monetary")),
    build_column_couple('f7fm', IntCol(entity = 'foy', label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse", val_type = "monetary")),
    build_column_couple('f7fl', IntCol(entity = 'foy', label = u"")),

    # Souscriptions au capital de SOFICA
    build_column_couple('f7gn', IntCol(entity = 'foy', label = u"Souscriptions au capital de SOFICA 48 %", val_type = "monetary")),
    build_column_couple('f7fn', IntCol(entity = 'foy', label = u"Souscriptions au capital de SOFICA 40 %", val_type = "monetary")),

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
    build_column_couple('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary")),

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
    build_column_couple('f2bg', IntCol(entity = 'foy', label = u"Crédit d’impôt directive « épargne »", val_type = "monetary")),

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

    build_column_couple('wprm_init', FloatCol(label = u"Effectifs",
                           survey_only = True)),

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

    build_column_couple('aer', IntCol(label = u"Allocation équivalent retraite (AER)")),
    build_column_couple('ass', IntCol(label = u"Allocation de solidarité spécifique (ASS)")),
    build_column_couple('f5sq', IntCol()),

    build_column_couple('m_afeamam', IntCol(entity = 'men')),
    build_column_couple('m_agedm', IntCol(entity = 'men')),
    build_column_couple('m_clcam', IntCol(entity = 'men')),
    build_column_couple('m_colcam', IntCol(entity = 'men')),
    build_column_couple('m_mgamm', IntCol(entity = 'men')),
    build_column_couple('m_mgdomm', IntCol(entity = 'men')),
    build_column_couple('zthabm', IntCol(entity = 'men')),  # Devrait être renommée tax

    build_column_couple('adoption', BoolCol(entity = "ind", label = u"Enfant adopté")),

    # ('tax_hab', IntCol()),
    ))
