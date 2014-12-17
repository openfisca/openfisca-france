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


from ..base import *  # noqa


# Socio-economic data
# Données d'entrée de la simulation à fournir à partir d'une enquête ou générées par le générateur de cas type
build_column('idmen', IntCol(label = u"Identifiant du ménage"))  # 600001, 600002,
build_column('idfoy', IntCol(label = u"Identifiant du foyer"))  # idmen + noi du déclarant
build_column('idfam', IntCol(label = u"Identifiant de la famille"))  # idmen + noi du chef de famille

build_column('quimen', EnumCol(QUIMEN))
build_column('quifoy', EnumCol(QUIFOY))
build_column('quifam', EnumCol(QUIFAM))

build_column('sali', IntCol(label = u"Revenus d'activité imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AJ",
                               QUIFOY['conj']: u"1BJ",
                               QUIFOY['pac1']: u"1CJ",
                               QUIFOY['pac2']: u"1DJ",
                               QUIFOY['pac3']: u"1EJ",
                               }))  # (f1aj, f1bj, f1cj, f1dj, f1ej)
build_column('choi', IntCol(label = u"Autres revenus imposables (chômage, préretraite)",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AP",
                               QUIFOY['conj']: u"1BP",
                               QUIFOY['pac1']: u"1CP",
                               QUIFOY['pac2']: u"1DP",
                               QUIFOY['pac3']: u"1EP",
                               }))  # (f1ap, f1bp, f1cp, f1dp, f1ep)
build_column('rsti', IntCol(label = u"Pensions, retraites, rentes connues imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AS",
                               QUIFOY['conj']: u"1BS",
                               QUIFOY['pac1']: u"1CS",
                               QUIFOY['pac2']: u"1DS",
                               QUIFOY['pac3']: u"1ES",
                               }))  # (f1as, f1bs, f1cs, f1ds, f1es)
build_column('fra', IntCol(label = u"Frais réels",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AK",
                              QUIFOY['conj']: u"1BK",
                              QUIFOY['pac1']: u"1CK",
                              QUIFOY['pac2']: u"1DK",
                              QUIFOY['pac3']: u"1EK",
                              }))  # (f1ak, f1bk, f1ck, f1dk, f1ek)

build_column('alr', IntCol(label = u"Pensions alimentaires perçues",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AO",
                              QUIFOY['conj']: u"1BO",
                              QUIFOY['pac1']: u"1CO",
                              QUIFOY['pac2']: u"1DO",
                              QUIFOY['pac3']: u"1EO",
                              }))  # (f1ao, f1bo, f1co, f1do, f1eo)
build_column('alr_decl', BoolCol(label = u"Pension déclarée", default = True))

build_column('hsup', IntCol(label = u"Heures supplémentaires : revenus exonérés connus",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AU",
                               QUIFOY['conj']: u"1BU",
                               QUIFOY['pac1']: u"1CU",
                               QUIFOY['pac2']: u"1DU",
                               QUIFOY['pac3']: u"1EU",
                               }))  # (f1au, f1bu, f1cu, f1du, f1eu)

# pour inv, il faut que tu regardes si tu es d'accord et si c'est bien la bonne case,
# la case P exsite déjà plus bas ligne 339 sous le nom caseP

build_column('inv', BoolCol(label = u'Invalide'))  # TODO: cerfa_field

build_column('alt', BoolCol(label = u'Enfant en garde alternée'))  # TODO: cerfa_field

build_column('cho_ld', BoolCol(label = u"Demandeur d'emploi inscrit depuis plus d'un an",
                   cerfa_field = {QUIFOY['vous']: u"1AI",
                                  QUIFOY['conj']: u"1BI",
                                  QUIFOY['pac1']: u"1CI",
                                  QUIFOY['pac2']: u"1DI",
                                  QUIFOY['pac3']: u"1EI",
                               }))  # (f1ai, f1bi, f1ci, f1di, f1ei)
build_column('ppe_tp_sa', BoolCol(label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière",
                      cerfa_field = {QUIFOY['vous']: u"1AX",
                                     QUIFOY['conj']: u"1BX",
                                     QUIFOY['pac1']: u"1CX",
                                     QUIFOY['pac2']: u"1DX",
                                     QUIFOY['pac3']: u"1QX",
                                     }))  # (f1ax, f1bx, f1cx, f1dx, f1qx)
build_column('ppe_tp_ns', BoolCol(label = u"Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière",
                      cerfa_field = {QUIFOY['vous']: u"5NW",
                                     QUIFOY['conj']: u"5OW",
                                     QUIFOY['pac1']: u"5PW",
                                     }))  # (f5nw, f5ow, f5pw)
build_column('ppe_du_sa', IntCol(label = u"Prime pour l'emploi des salariés: nombre d'heures payées dans l'année",
                     cerfa_field = {QUIFOY['vous']: u"1AV",
                                    QUIFOY['conj']: u"1BV",
                                    QUIFOY['pac1']: u"1CV",
                                    QUIFOY['pac2']: u"1DV",
                                    QUIFOY['pac3']: u"1QV",
                                    }))  # (f1av, f1bv, f1cv, f1dv, f1qv)
build_column('ppe_du_ns', IntCol(label = u"Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année",
                     cerfa_field = {QUIFOY['vous']: u"5NV",
                                    QUIFOY['conj']: u"5OV",
                                    QUIFOY['pac1']: u"5PV",
                               }))  # (f5nv, f5ov, f5pv)
build_column('jour_xyz', IntCol(default = 360,
                    entity = "foy",
                    label = u"Jours décomptés au titre de cette déclaration"))
build_column('birth', DateCol(label = u"Année de naissance"))
build_column('prenom', StrCol(label = u"Prénom"))

build_column('loyer', IntCol(label = u"Loyer mensuel",
                 entity = 'men',
                 val_type = "monetary"))  # Loyer mensuel
build_column('so', EnumCol(label = u"Statut d'occupation",
               entity = 'men',
               enum = Enum([u"Non renseigné",
                            u"Accédant à la propriété",
                            u"Propriétaire (non accédant) du logement",
                            u"Locataire d'un logement HLM",
                            u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
                            u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
                            u"Logé gratuitement par des parents, des amis ou l'employeur"])))

build_column('activite', EnumCol(label = u'Activité',
                     enum = Enum([u'Actif occupé',
                                u'Chômeur',
                                u'Étudiant, élève',
                                u'Retraité',
                                u'Autre inactif']), default = 4))

build_column('titc', EnumCol(label = u"Statut, pour les agents de l'Etat des collectivités locales, ou des hôpitaux",
                 enum = Enum([
                              u"Sans objet ou non renseigné",
                              u"Elève fonctionnaire ou stagiaire",
                              u"Agent titulaire",
                              u"Contractuel"]),
                 survey_only = True,
    ))

build_column('statut', EnumCol(label = u"Statut détaillé mis en cohérence avec la profession",
                   enum = Enum([u"Sans objet",
                                u"Indépendants",
                                u"Employeurs",
                                u"Aides familiaux",
                                u"Intérimaires",
                                u"Apprentis",
                                u"CDD (hors Etat, coll.loc.), hors contrats aidés",
                                u"Stagiaires et contrats aides (hors Etat, coll.loc.)",
                                u"Autres contrats (hors Etat, coll.loc.)",
                                u"CDD (Etat, coll.loc.), hors contrats aidés",
                                u"Stagiaires et contrats aidés (Etat, coll.loc.)",
                                u"Autres contrats (Etat, coll.loc.)",
                                ]),
                   survey_only = True,
                   ))

build_column('txtppb', EnumCol(label = u"Taux du temps partiel",
            enum = Enum([u"Sans objet",
                        u"Moins d'un mi-temps (50%)",
                        u"Mi-temps (50%)",
                        u"Entre 50 et 80%",
                        u"80%",
                        u"Plus de 80%"]),
                   survey_only = True))

build_column('nbsala', EnumCol(label = u"Nombre de salariés dans l'établissement de l'emploi actuel",
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
                            ])))

build_column('tva_ent', BoolCol(label = u"L'entreprise employant le salarié paye de la TVA",
                    default = True))

build_column('chpub', EnumCol(label = u"Nature de l'employeur principal",
                  enum = Enum([u"Sans objet",
                               u"Etat",
                               u"Collectivités locales, HLM",
                               u"Hôpitaux publics",
                               u"Particulier",
                               u"Entreprise publique (La Poste, EDF-GDF, etc.)",
                               u"Entreprise privée, association",
                               ]),
                  survey_only = True))

build_column('cadre', BoolCol(label = u"Cadre salarié du privé",
                  survey_only = True))

build_column('code_risque', EnumCol(label = u"Code risque pour les accidents du travail"))  # TODO: complete label and add relevant default
build_column('exposition_accident', EnumCol(label = u"Exposition au risque pour les accidents du travail",
                        enum = Enum([u"Faible",
                               u"Moyen",
                               u"Elevé",
                               u"Très elevé",
                               ])))

build_column('boursier', BoolCol(label = u"Elève ou étudiant boursier"))
build_column('code_postal', IntCol(label = u"Code postal du lieu de résidence",
                       entity = 'men'))

build_column('statmarit', EnumCol(label = u"Statut marital",
                      default = 2,
                      enum = Enum([u"Marié",
                                u"Célibataire",
                                u"Divorcé",
                                u"Veuf",
                                u"Pacsé",
                                u"Jeune veuf"], start = 1)))

build_column('nbN', IntCol(cerfa_field = u'N', entity = 'foy',
    label = u"Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille"))
build_column('nbR', IntCol(cerfa_field = u'R', entity = 'foy',
    label = u"Nombre de titulaires (autres que les enfants) de la carte invalidité d'au moins 80 %"))

build_column('caseE', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul",
                  entity = 'foy',
                  cerfa_field = u'E', end = date(2012, 12, 31)))
build_column('caseF', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)",
                  entity = 'foy',
                  cerfa_field = u'F'))
build_column('caseG', BoolCol(label = u"Titulaire d'une pension de veuve de guerre",
                  entity = 'foy',
                  cerfa_field = u'G'))  # attention, ne pas confondre caseG et nbG qui se rapportent toutes les 2 à une "case" G, l'une étant une vraie case que l'on remplt et l'autre une case que l'on coche
build_column('caseH', IntCol(label = u"Année de naissance des enfants à charge en garde alternée", entity = 'foy',
                 cerfa_field = u'H'))
# il ne s'agit pas à proprement parlé de la case H, les cases permettant d'indiquer l'année de naissance
#    se rapportent bien à nbH mais ne sont pas nommées, choisissons nous de laisser cerfa_field = u'H' pour caseH ?
#    De plus les caseH peuvent être multiples puisqu'il peut y avoir plusieurs enfants? donc faut-il les nommer caseH1, caseH2...caseH6 (les 6 présentes dans la déclaration) ?
#    il faut aussi créer les cases F, G, R et I qui donnent également les années de naissances des PAC


build_column('caseK', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre",
                  entity = 'foy',
                  cerfa_field = u'K', end = date(2011, 12, 31)))

build_column('caseL', BoolCol(label = u"Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul",
                  entity = 'foy',
                  cerfa_field = u'L'))

build_column('caseN', BoolCol(label = u"Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus",
                  entity = 'foy',
                  cerfa_field = u'N'))
build_column('caseP', BoolCol(label = u"Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%",
                  entity = 'foy',
                  cerfa_field = u'P'))
build_column('caseS', BoolCol(label = u"Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                  entity = 'foy',
                  cerfa_field = u'S'))

build_column('caseT', BoolCol(label = u"Vous êtes parent isolé au 1er janvier de l'année de perception des revenus",
                  entity = 'foy',
                  cerfa_field = u'T'))

build_column('caseW', BoolCol(label = u"Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre",
                  entity = 'foy',
                  cerfa_field = u'W'))

build_column('rfr_n_1', IntCol(entity = 'foy', label = u"Revenu fiscal de référence année n - 1",
    val_type = "monetary"))
build_column('rfr_n_2', IntCol(entity = 'foy', label = u"Revenu fiscal de référence année n - 2",
    val_type = "monetary"))
build_column('nbptr_n_2', IntCol(entity = 'foy', label = u"Nombre de parts année n - 2",
    val_type = "monetary"))

# Rentes viagères
build_column('f1aw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1AW'))
build_column('f1bw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1BW'))
build_column('f1cw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1CW'))
build_column('f1dw', IntCol(label = u"Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'1DW'))

# Gain de levée d'options
# Bouvard: j'ai changé là mais pas dans le code, il faut chercher les f1uv
# et les mettre en f1tvm comme pour sali
# Il faut aussi le faire en amont dans les tables

# là je ne comprends pas pourquoi il faut changer les f1uv en f1tvm....
# du coups je n'ai pas changé et j'ai fait un dico comme pour sali

build_column('f1tv', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TV",
                                       QUIFOY['conj']: u"1UV",
                                       }))  # (f1tv,f1uv))

build_column('f1tw', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TW",
                                       QUIFOY['conj']: u"1UW",
                                       }))  # (f1tw,f1uw))

build_column('f1tx', IntCol(label = u"Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans",
                        entity = 'ind',
                        val_type = "monetary",
                        cerfa_field = {QUIFOY['vous']: u"1TX",
                                       QUIFOY['conj']: u"1UX",
                        }))  # (f1tx,f1ux))

# RVCM
# revenus au prélèvement libératoire
build_column('f2da', IntCol(label = u"Revenus des actions et parts soumis au prélèvement libératoire de 21 %",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'2DA', end = date(2012, 12, 31)))  # à vérifier sur la nouvelle déclaration des revenus 2013

build_column('f2dh', IntCol(label = u"Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'2DH'))

build_column('f2ee', IntCol(label = u"Autres produits de placement soumis aux prélèvements libératoires",
                entity = 'foy',
                val_type = "monetary",
                cerfa_field = u'2EE'))

# revenus des valeurs et capitaux mobiliers ouvrant droit à abattement
build_column('f2dc', IntCol(entity = 'foy',
                label = u"Revenus des actions et parts donnant droit à abattement",
                val_type = "monetary",
                cerfa_field = u'2DC'))

build_column('f2fu', IntCol(entity = 'foy',
                label = u"Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement",
                val_type = "monetary",
                cerfa_field = u'2FU'))
build_column('f2ch', IntCol(entity = 'foy',
                label = u"Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement",
                val_type = "monetary",
                cerfa_field = u'2CH'))

#  Revenus des valeurs et capitaux mobiliers n'ouvrant pas droit à abattement
build_column('f2ts', IntCol(entity = 'foy', label = u"Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)",
                val_type = "monetary",
                cerfa_field = u'2TS'))
build_column('f2go', IntCol(entity = 'foy',
                label = u"Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)",
                val_type = "monetary",
                cerfa_field = u'2GO'))
build_column('f2tr', IntCol(entity = 'foy', label = u"Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)",
                val_type = "monetary",
                cerfa_field = u'2TR'))


# Autres revenus des valeurs et capitaux mobiliers
build_column('f2cg', IntCol(entity = 'foy',
                label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible",
                val_type = "monetary",
                cerfa_field = u'2CG'))

build_column('f2bh', IntCol(entity = 'foy',
                label = u"Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible",
                val_type = "monetary",
                cerfa_field = u'2BH'))

build_column('f2ca', IntCol(entity = 'foy',
                label = u"Frais et charges déductibles",
                val_type = "monetary",
                cerfa_field = u'2CA'))

build_column('f2ck', IntCol(entity = 'foy',
                label = u"Crédit d'impôt égal au prélèvement forfaitaire déjà versé",
                val_type = "monetary",
                cerfa_field = u'2CK',
                start = date(2013, 1, 1)))  # TODO: nouvelle case à créer où c'est nécessaire, vérifier sur la déclaration des revenus 2013

build_column('f2ab', IntCol(entity = 'foy',
                label = u"Crédits d'impôt sur valeurs étrangères",
                val_type = "monetary",
                cerfa_field = u'2AB'))

build_column('f2bg', IntCol(entity = 'foy',
                label = u"Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables",
                val_type = "monetary",
                cerfa_field = u'2BG',
                start = date(2012, 1, 1)))  # TODO: nouvelle case à créer où c'est nécessaire
                                 # TODO: vérifier existence avant 2012

build_column('f2aa', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AA'))

build_column('f2al', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AL'))

build_column('f2am', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AM'))

build_column('f2an', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AN',
                start = date(2010, 1, 1)))

build_column('f2aq', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AQ',
                start = date(2011, 1, 1)))

build_column('f2ar', IntCol(entity = 'foy',
                label = u"Déficits des années antérieures non encore déduits",
                val_type = "monetary",
                cerfa_field = u'2AR',
                start = date(2012, 1, 1)))

# je ne sais pas d'ou sort f2as...! probablement une ancienne année à laquelle je ne suis pas encore arrivé
#
build_column('f2as', IntCol(entity = 'foy', label = u"Déficits des années antérieures non encore déduits: année 2012", val_type = "monetary", end = date(2011, 12, 31)))  # TODO: vérifier existence <=2011

build_column('f2dm', IntCol(entity = 'foy',
                label = u"Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %",
                val_type = "monetary",
                cerfa_field = u'2DM',
                start = date(2012, 1, 1)))  # TODO: nouvelle case à utiliser où c'est nécessaire
                                 # TODO: vérifier existence avant 2012

build_column('f2gr', IntCol(entity = 'foy',
                label = u"Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)",
                val_type = "monetary",
                cerfa_field = u'2GR',
                start = date(2009, 1, 1),
                end = date(2009, 12, 31)))  # TODO: vérifier existence à partir de 2011

build_column('f3vc', IntCol(entity = 'foy',
                label = u"Produits et plus-values exonérés provenant de structure de capital-risque",
                val_type = "monetary",
                cerfa_field = u'3VC'))

build_column('f3vd', IntCol(entity = 'ind',
                label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VD",
                               QUIFOY['conj']: u"3SD",
                               }))  # (f3vd, f3sd)

build_column('f3ve', IntCol(entity = 'foy',
                label = u"Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %",
                val_type = "monetary",
                cerfa_field = u'3VE',
                start = date(2013, 1, 1)))
# """
# réutilisation case 3VE en 2013


#    build_column('f3ve', IntCol(entity = 'foy',
#                    label = u"Plus-values de cession de droits sociaux réalisées par des personnes domiciliées dans les DOM",
#                    val_type = "monetary",
#                    cerfa_field = u'3VE',
#                    end = date(2012, 12, 31)))
# """


build_column('f3vf', IntCol(entity = 'ind',
                label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VF",
                               QUIFOY['conj']: u"3SF",
                               }))  # (f3vf, f3sf)

# comment gérer les cases qui ont le même nom mais qui ne correspondent pas tout à fait à la même chose ?
# peut-ont garder le même nom et l'encadrer par des start-end ? ou avec un truc genre if sur l'année ?(pour ne pas avoir à changer le nom de la variable)
# si on garde le même nom avec des start-end, et si on intégre la variable partout où elle doit être (dans les différents calculs), est-on sûr que lors des calculs les start-end seront bien pris en compte ?
# ça rendra le modéle un peu moins clair parce qu'il y aura le même nom de variable pour des choses différentes et dans des calculs ne se rapportant pas aux mêmes choses,
# mais si les start-end fonctionne ça ne devrait pas avoir d'impact sur les calculs ? qu'en penses-tu ?

# ## build_column('f3vl', IntCol(entity = 'foy',
# ##                 label = u"Distributions par des sociétés de capital-risque taxables à 24 %",
# ##                 val_type = "monetary",
# ##                 cerfa_field = u'3VL'
# ##                 start = date(2009, 1, 1),
# ##                 end = date(2009, 12, 31)))#vérifier avant 2009

build_column('f3vl', IntCol(entity = 'foy',
                label = u"Distributions par des sociétés de capital-risque taxables à 19 %",
                val_type = "monetary",
                cerfa_field = u'3VL',
                start = date(2012, 1, 1),
                end = date(2013, 12, 31)))  # vérifier pour 2011 et 2010

build_column('f3vi', IntCol(entity = 'ind',
                label = u"Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VI",
                               QUIFOY['conj']: u"3SI",
                               }))  # (f3vi, f3si )

build_column('f3vm', IntCol(entity = 'foy',
                label = u"Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %",
                val_type = "monetary",
                cerfa_field = u'3VM'))

build_column('f3vt', IntCol(entity = 'foy',
                label = u"Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %",
                val_type = "monetary",
                cerfa_field = u'3VT'))

build_column('f3vj', IntCol(entity = 'ind',
                label = u"Gains imposables sur option dans la catégorie des salaires",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VJ",
                               QUIFOY['conj']: u"3VK",
                               }))  # (f3vj, f3vk )

build_column('f3va', IntCol(entity = 'ind',
                label = u"Abattement pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"3VA",
                               QUIFOY['conj']: u"3VB",
                               }))  # (f3va, f3vb )))

# Plus values et gains taxables à des taux forfaitaires

build_column('f3vg', IntCol(entity = 'foy',
                label = u"Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés",
                val_type = "monetary",
                cerfa_field = u'3VG'))

build_column('f3vh', IntCol(entity = 'foy',
                label = u"Perte de l'année de perception des revenus",
                val_type = "monetary",
                cerfa_field = u'3VH'))

build_column('f3vu', IntCol(entity = 'foy',
                end = date(2009, 12, 31)))  # TODO: vérifier pour 2010 et 2011

build_column('f3vv', IntCol(entity = 'foy',
                 label = u"Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé ",
                 val_type = "monetary",
                 cerfa_field = u'3VV'))  # TODO: à revoir :ok pour 2013, pas de 3vv pour 2012, et correspond à autre chose en 2009, vérifier 2010 et 2011

build_column('f3si', IntCol(entity = 'foy'))  # TODO: parmi ces cas créer des valeurs individuelles
#                                    # correspond à autre chose en 2009, vérifier 2011,2010

build_column('f3sa', IntCol(entity = 'foy', end = date(2009, 12, 31)))  # TODO: n'existe pas en 2013 et 2012 vérifier 2011 et 2010

build_column('f3sf', IntCol(entity = 'foy'))  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

build_column('f3sd', IntCol(entity = 'foy'))  # TODO: déjà définit plus haut, vérifier si 2009, 2010, 2011 correspondent à la même chose que 12 et 13

build_column('f3vz', IntCol(entity = 'foy',
                 label = u"Plus-values imposables sur cessions d’immeubles ou de biens meubles",
                 val_type = "monetary",
                 cerfa_field = u'3VZ',
                 start = date(2011, 1, 1)))  # TODO: vérifier avant 2012

# Revenus fonciers
build_column('f4ba', IntCol(entity = 'foy',
                label = u"Revenus fonciers imposables",
                val_type = "monetary",
                cerfa_field = u'4BA'))

build_column('f4bb', IntCol(entity = 'foy',
                label = u"Déficit imputable sur les revenus fonciers",
                val_type = "monetary",
                cerfa_field = u'4BB'))

build_column('f4bc', IntCol(entity = 'foy',
                label = u"Déficit imputable sur le revenu global",
                val_type = "monetary",
                cerfa_field = u'4BC'))

build_column('f4bd', IntCol(entity = 'foy',
                label = u"Déficits antérieurs non encore imputés",
                val_type = "monetary",
                cerfa_field = u'4BD'))

build_column('f4be', IntCol(entity = 'foy',
                label = u"Micro foncier: recettes brutes sans abattement",
                val_type = "monetary",
                cerfa_field = u'4BE'))

# Prime d'assurance loyers impayés
build_column('f4bf', IntCol(entity = 'foy',
                label = u"Primes d'assurance pour loyers impayés des locations conventionnées",
                val_type = "monetary",
                cerfa_field = u'4BF'))

build_column('f4bl', IntCol(entity = 'foy', label = u"", end = date(2009, 12, 31)))  # TODO: cf 2010 2011

build_column('f5qm', IntCol(entity = 'ind',
                label = u"Agents généraux d’assurances: indemnités de cessation d’activité",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"5QM",
                               QUIFOY['conj']: u"5RM",
                               }))  # (f5qm, f5rm )

# Csg déductible
build_column('f6de', IntCol(entity = 'foy',
                label = u"CSG déductible calculée sur les revenus du patrimoine",
                val_type = "monetary",
                cerfa_field = u'6DE'))

# Pensions alimentaires
build_column('f6gi', IntCol(entity = 'foy',
                label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant",
                val_type = "monetary",
                cerfa_field = u'6GI'))

build_column('f6gj', IntCol(entity = 'foy',
                label = u"Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant",
                val_type = "monetary",
                cerfa_field = u'6GJ'))

build_column('f6el', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées à des enfants majeurs: 1er enfant",
                val_type = "monetary",
                cerfa_field = u'6EL'))

build_column('f6em', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant",
                val_type = "monetary",
                cerfa_field = u'6EM'))

build_column('f6gp', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)",
                val_type = "monetary",
                cerfa_field = u'6GP'))

build_column('f6gu', IntCol(entity = 'foy',
                label = u"Autres pensions alimentaires versées (mineurs, ascendants)",
                val_type = "monetary",
                cerfa_field = u'6GU'))


# Frais d'accueil d'une personne de plus de 75 ans dans le besoin
build_column('f6eu', IntCol(entity = 'foy',
                label = u"Frais d'accueil de personnes de plus de 75 ans dans le besoin",
                val_type = "monetary",
                cerfa_field = u'6EU'))

build_column('f6ev', IntCol(entity = 'foy',
                label = u"Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit",
                cerfa_field = u'6EV'))

# Déductions diverses
build_column('f6dd', IntCol(entity = 'foy',
                label = u"Déductions diverses",
                val_type = "monetary",
                cerfa_field = u'6DD'))

# Épargne retraite - PERP, PRÉFON, COREM et CGOS
build_column('f6ps', IntCol(entity = 'ind',
                label = u"Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"6PS",
                               QUIFOY['conj']: u"6PT",
                               QUIFOY['pac1']: u"6PU",
                               }))  # (f6ps, f6pt, f6pu)

build_column('f6rs', IntCol(entity = 'ind',
                label = u"Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"6RS",
                               QUIFOY['conj']: u"6RT",
                               QUIFOY['pac1']: u"6RU",
                               }))  # (f6rs, f6rt, f6ru)))

build_column('f6ss', IntCol(entity = 'ind',
                label = u"Rachat de cotisations PERP, PREFON, COREM et C.G.O.S",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"6SS",
                               QUIFOY['conj']: u"6ST",
                               QUIFOY['pac1']: u"6SU",
                               }))  # (f6ss, f6st, f6su)))


# Souscriptions en faveur du cinéma ou de l’audiovisuel
build_column('f6aa', IntCol(entity = 'foy',
                label = u"Souscriptions en faveur du cinéma ou de l’audiovisuel",
                val_type = "monetary",
                start = date(2005, 1, 1),
                end = date(2005, 12, 31),
                cerfa_field = u'6AA'))  # TODO: ancien numéro de case, antérieur à 2008 ....au moins! vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en 12 et 13)

# Souscriptions au capital des SOFIPÊCHE
build_column('f6cc', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des SOFIPÊCHE",
                val_type = "monetary",
                cerfa_field = u'CC',
                start = date(2005, 1, 1),
                end = date(2005, 12, 31)))  # ancien numéro de case, antérieur à 2008 ....au moins vérifier pour 07-06-05 ect...probablement avant 2005 (autre nom en  12 et13)


# Investissements DOM-TOM dans le cadre d’une entreprise < = 2005
# ou Versements sur un compte épargne codéveloppement
build_column('f6eh', IntCol(entity = 'foy',
                label = u"",
                val_type = "monetary",
                start = date(2005, 1, 1),
                end = date(2005, 12, 31),
                cerfa_field = u'EH'))  # TODO: vérifier date de début et de fin de cette case (rien en 12 et 13)

# Pertes en capital consécutives à la souscription au capital de sociétés
# nouvelles ou de sociétés en difficulté
build_column('f6da', IntCol(entity = 'foy',
                label = u"Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté",
                val_type = "monetary",
                start = date(2005, 1, 1),
                end = date(2005, 12, 31),
                cerfa_field = u'DA'))


# Dépenses de grosses réparations effectuées par les nus propriétaires
build_column('f6cb', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)",
                val_type = "monetary",
                start = date(2006, 1, 1),
                cerfa_field = u'6CB'))  # TODO: vérifier 2011, 10, 9 ,8, 7,6, ok pou 12 et 13
                                       # TODO: before 2006 wasPertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration complémentaire)

build_column('f6hj', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                cerfa_field = u'6HJ'))

build_column('f6hk', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                cerfa_field = u'6HK'))

build_column('f6hl', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                cerfa_field = u'6HL'))

build_column('f6hm', IntCol(entity = 'foy',
                label = u"Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures",
                val_type = "monetary",
                start = date(2013, 1, 1),
                cerfa_field = u'6HM'))

# Sommes à rajouter au revenu imposable
build_column('f6gh', IntCol(entity = 'foy',
                label = u"Sommes à ajouter au revenu imposable",
                val_type = "monetary",
                cerfa_field = u'6GH'))

# Deficits antérieurs
build_column('f6fa', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6",
                val_type = "monetary",
                cerfa_field = u'6FA'))

build_column('f6fb', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5",
                val_type = "monetary",
                cerfa_field = u'6FB'))

build_column('f6fc', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4",
                val_type = "monetary",
                cerfa_field = u'6FC'))

build_column('f6fd', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3",
                val_type = "monetary",
                cerfa_field = u'6FD'))

build_column('f6fe', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2",
                val_type = "monetary",
                cerfa_field = u'6FE'))

build_column('f6fl', IntCol(entity = 'foy',
                label = u"Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1",
                val_type = "monetary",
                cerfa_field = u'6FL'))

# Dons à des organismes établis en France
build_column('f7ud', IntCol(entity = 'foy',
                label = u"Dons à des organismes d'aide aux personnes en difficulté",
                val_type = "monetary",
                cerfa_field = u'7UD'))

build_column('f7uf', IntCol(entity = 'foy',
                label = u"Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général",
                val_type = "monetary",
                cerfa_field = u'7UF'))

build_column('f7xs', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5",
                val_type = "monetary",
                cerfa_field = u'7XS'))

build_column('f7xt', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4",
                val_type = "monetary",
                cerfa_field = u'7XT'))

build_column('f7xu', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3",
                val_type = "monetary",
                cerfa_field = u'7XU'))

build_column('f7xw', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2",
                val_type = "monetary",
                cerfa_field = u'7XW'))

build_column('f7xy', IntCol(entity = 'foy',
                label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1",
                val_type = "monetary",
                cerfa_field = u'7XY'))

# Cotisations syndicales des salariées et pensionnés
build_column('f7ac', IntCol(entity = 'ind',
                label = u"Cotisations syndicales des salariées et pensionnés",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"7AC",
                               QUIFOY['conj']: u"7AE",
                               QUIFOY['pac1']: u"7AG",
                               }))  # f7ac, f7ae, f7ag

# Salarié à domicile
build_column('f7db', IntCol(entity = 'foy',
                label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7DB'))

build_column('f7df', IntCol(entity = 'foy',
                label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7DF'))

build_column('f7dq', BoolCol(entity = 'foy',
                 label = u"Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés",
                 cerfa_field = u'7DQ'))

build_column('f7dg', BoolCol(entity = 'foy',
                 label = u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés",
                 cerfa_field = u'7DG'))

build_column('f7dl', IntCol(entity = 'foy',
                label = u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés",
                cerfa_field = u'7DL'))

# Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
build_column('f7vy', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité",
                val_type = "monetary",
                cerfa_field = u'7VY'))

build_column('f7vz', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes",
                val_type = "monetary",
                cerfa_field = u'7VZ'))

build_column('f7vx', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011",
                val_type = "monetary",
                cerfa_field = u'7VX'))

build_column('f7vw', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité",
                val_type = "monetary",
                cerfa_field = u'7VW'))

build_column('f7vv', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes",
                val_type = "monetary",
                cerfa_field = u'7VV'))  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

build_column('f7vu', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité",
                val_type = "monetary",
                cerfa_field = u'7VU'))  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

build_column('f7vt', IntCol(entity = 'foy',
                label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes",
                val_type = "monetary",
                cerfa_field = u'7VT'))  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

# Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
build_column('f7cd', IntCol(entity = 'foy',
                label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne",
                val_type = "monetary",
                cerfa_field = u'7CD'))

build_column('f7ce', IntCol(entity = 'foy',
                label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne",
                val_type = "monetary",
                cerfa_field = u'7CE'))

# Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus
build_column('f7ga', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge",
                val_type = "monetary",
                cerfa_field = u'7GA'))

build_column('f7gb', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge",
                val_type = "monetary",
                cerfa_field = u'7GB'))

build_column('f7gc', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge",
                val_type = "monetary",
                cerfa_field = u'7GC'))

build_column('f7ge', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée",
                val_type = "monetary",
                cerfa_field = u'7GE'))

build_column('f7gf', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée",
                val_type = "monetary",
                cerfa_field = u'7GF'))

build_column('f7gg', IntCol(entity = 'foy',
                label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée",
                val_type = "monetary",
                cerfa_field = u'7GG'))

# Nombre d'enfants à charge poursuivant leurs études
build_column('f7ea', IntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge poursuivant leurs études au collège",
                cerfa_field = u'7EA'))

build_column('f7eb', IntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège",
                cerfa_field = u'7EB'))

build_column('f7ec', IntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge poursuivant leurs études au lycée",
                cerfa_field = u'7EC'))

build_column('f7ed', IntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée",
                cerfa_field = u'7ED'))

build_column('f7ef', IntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur",
                cerfa_field = u'7EF'))

build_column('f7eg', IntCol(entity = 'foy',
                label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur",
                cerfa_field = u'7EG'))

# Intérêts des prêts étudiants
build_column('f7td', IntCol(entity = 'foy',
                label = u"Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7TD'))

build_column('f7vo', IntCol(entity = 'foy',
                label = u"Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés",
                cerfa_field = u'7VO'))

build_column('f7uk', IntCol(entity = 'foy',
                label = u"Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7UK'))

# Primes de rente survie, contrats d'épargne handicap
build_column('f7gz', IntCol(entity = 'foy',
                label = u"Primes de rente survie, contrats d'épargne handicap",
                val_type = "monetary",
                cerfa_field = u'7GZ'))

# Prestations compensatoires
build_column('f7wm', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Capital fixé en substitution de rente",
                val_type = "monetary",
                cerfa_field = u'7WM'))

build_column('f7wn', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés",
                val_type = "monetary",
                cerfa_field = u'7WN'))

build_column('f7wo', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué",
                val_type = "monetary",
                cerfa_field = u'7WO'))

build_column('f7wp', IntCol(entity = 'foy',
                label = u"Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1",
                val_type = "monetary",
                cerfa_field = u'7WP'))

# Dépenses en faveur de la qualité environnementale de l'habitation principale
build_column('f7we', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés",
                cerfa_field = u'7WE'))

build_column('f7wg', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1",
                val_type = "monetary",
                cerfa_field = u'7WG',
                start = date(2012, 1, 1)))  # TODO, nouvelle variable à intégrer dans OF (cf ancien nom déjà utilisé)
                                # TODO vérifier pour les années précédentes
# TODO: CHECK
# Intérêts d'emprunts
#     build_column('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary", cerfa_field = u'7')) # cf pour quelle année
#
build_column('f7wq', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées", cerfa_field = u'7WQ'))

build_column('f7wt', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement ",
                start = date(2013, 1, 1),
                cerfa_field = u'7WT'))  # TODO vérifier année de début

build_column('f7wh', IntCol(entity = 'foy', label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus",
                start = date(2013, 1, 1),
                cerfa_field = u'7WH'))  # TODO vérifier année de début

build_column('f7wk', BoolCol(entity = 'foy',
                 label = u"Votre habitation principale est une maison individuelle",
                 cerfa_field = u'7WK'))

build_column('f7wf', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1",
                end = date(2012, 12, 31),
                cerfa_field = u'7WF'))  # TODO vérifier les années précédentes

# Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
build_column('f7wi', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction",
                val_type = "monetary",
                cerfa_field = u'7WI',
                end = date(2012, 12, 31)))

build_column('f7wj', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées",
                val_type = "monetary",
                cerfa_field = u'7WJ'))

build_column('f7wl', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques",
                val_type = "monetary",
                cerfa_field = u'7WL'))

# Investissements dans les DOM-TOM dans le cadre d'une entrepise
build_column('f7ur', IntCol(entity = 'foy',
                label = u"Investissements réalisés en n-1, total réduction d’impôt",
                val_type = "monetary",
                cerfa_field = u'7UR',
                end = date(2011, 12, 31)))  # TODO: vérifier les années antérieures

build_column('f7oz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6",
                val_type = "monetary",
                cerfa_field = u'7OZ',
                end = date(2011, 12, 31)))  # TODO: vérifier les années antérieures

build_column('f7pz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                val_type = "monetary",
                cerfa_field = u'7PZ',
                end = date(2012, 12, 31)))  # TODO: vérifier les années antérieures

build_column('f7qz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures",
                val_type = "monetary",
                cerfa_field = u'7QZ',
                end = date(2012, 12, 31)))  # TODO: vérifier les années antérieures

build_column('f7rz', IntCol(entity = 'foy',
                label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3",
                val_type = "monetary",
                cerfa_field = u'7RZ',
                end = date(2011, 12, 31)))  # TODO: vérifier années antérieures.

# TODO: 7sz se rapporte à des choses différentes en 2012 et 2013 par rapport aux années précédentes, cf pour les années antérieures
#     build_column('f7sz', IntCol(entity = 'foy',
#                     label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-2",
#                     val_type = "monetary",
#                     cerfa_field = u'7SZ',
#                     end = date(2011,12,31)))  # TODO: vérifier années <=2011.

build_column('f7sz', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location",
                val_type = "monetary",
                cerfa_field = u'7SZ',
                start = date(2012, 1, 1)))  # TODO: vérifier années <=2011

# Aide aux créateurs et repreneurs d'entreprises
build_column('f7fy', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                cerfa_field = u'7FY',
                end = date(2011, 12, 31)))  # TODO: vérifier date <=2011

build_column('f7gy', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1",
                cerfa_field = u'7GY',
                end = date(2011, 12, 31)))  # TODO: vérifier date <=2011


# TODO: 7jy réutilisée en 2013
#
#     build_column('f7jy', IntCol(entity = 'foy',
#                     label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et ayant pris fin en n-1",
#                     cerfa_field = u'7JY',
#                     end = date(2011,12,31)))

build_column('f7jy', IntCol(entity = 'foy',
                label = u"Report de 1/9 des investissements réalisés l'année de perception des revenus déclarés -3 ou -4",
                cerfa_field = u'7JY',
                start = date(2013, 1, 1)))

build_column('f7hy', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
                cerfa_field = u'7HY',
                end = date(2011, 12, 31)))  # TODO: vérifier date <=2011

build_column('f7ky', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1",
                cerfa_field = u'7KY',
                end = date(2011, 12, 31)))  # TODO: vérifier date <=2011

# 7iy réutilisée en 2013
#
#     build_column('f7iy', IntCol(entity = 'foy',
#                     label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et n'ayant pas pris fin en n-1",
#                     cerfa_field = u'7IY',
#                     end = date(2011,12,31)))  # TODO: vérifier date <=2011

build_column('f7iy', IntCol(entity = 'foy',
                label = u"Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés",
                cerfa_field = u'7IY',
                start = date(2013, 1, 1)))

build_column('f7ly', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                cerfa_field = u'7LY'))  # 2012 et 2013 ok

build_column('f7my', IntCol(entity = 'foy',
                label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés",
                cerfa_field = u'7MY'))  # 2012 et 2013 ok

# Travaux de restauration immobilière
build_column('f7ra', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager",
                val_type = "monetary",
                cerfa_field = u'7RA'))  # 2012 et 2013 ok

build_column('f7rb', IntCol(entity = 'foy',
                label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé",
                val_type = "monetary",
                cerfa_field = u'7RB'))  # 2012 et 2013 ok


# TOOD: f7gw et f7gx ne se rapporte pas a de l'assurance vie en 2013
# Assurance-vie
#     build_column('f7gw', IntCol(entity = 'foy', label = u"", cerfa_field = u'7GW', end = date(2011,12,31)))  # TODO: cf pour <=2011
#     build_column('f7gx', IntCol(entity = 'foy', label = u"", cerfa_field = u'7GX', end = date(2011,12,31)))  # TODO: cf pour <=2011
# build_column('f7gy', IntCol()) existe ailleurs (n'existe pas en 2013 et 2012)

build_column('f7gw', IntCol(entity = 'foy',
                label = u"Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                cerfa_field = u'7GW',
                start = date(2013, 1, 1)))

build_column('f7gx', IntCol(entity = 'foy',
                label = u"Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt",
                cerfa_field = u'7GX',
                start = date(2013, 1, 1)))

# Investissements locatifs dans le secteur de touristique
build_column('f7xc', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1",
                val_type = "monetary",
                cerfa_field = u'7XC',
                end = date(2012, 12, 31)))

build_column('f7xd', BoolCol(entity = 'foy',
                 label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                 cerfa_field = u'7XD',
                 end = date(2012, 12, 31)))

build_column('f7xe', BoolCol(entity = 'foy',
                 label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans",
                 cerfa_field = u'7XE',
                 end = date(2012, 12, 31)))

build_column('f7xf', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XF'))

build_column('f7xh', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme",
                val_type = "monetary",
                cerfa_field = u'7XH',
                end = date(2012, 12, 31)))

build_column('f7xi', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XI'))

build_column('f7xj', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XJ'))

build_column('f7xk', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XK'))

build_column('f7xl', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans",
                val_type = "monetary",
                cerfa_field = u'7XL',
                end = date(2012, 12, 31)))

build_column('f7xm', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XM'))

# TODO: f7xn cf années <= à 2011 (possible erreur dans le label pour ces dates, à vérifier)
#      build_column('f7xn', IntCol(entity = 'foy',
#                     label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: investissement réalisé en n-1",
#                     val_type = "monetary",
#                     cerfa_field = u'7XN',
#                     end = date(2011,12,31)))

build_column('f7xn', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XN',
                start = date(2012, 1, 1)))

build_column('f7xo', IntCol(entity = 'foy',
                label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures",
                val_type = "monetary",
                cerfa_field = u'7XO'))

# Souscriptions au capital des PME
build_column('f7cf', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion",
                val_type = "monetary",
                cerfa_field = u'7CF'))

build_column('f7cl', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4",
                val_type = "monetary",
                cerfa_field = u'7CL'))

build_column('f7cm', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3",
                val_type = "monetary",
                cerfa_field = u'7CM'))

build_column('f7cn', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2",
                val_type = "monetary",
                cerfa_field = u'7CN'))

build_column('f7cc', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1",
                val_type = "monetary",
                cerfa_field = u'7CC'))  # TODO: nouvelle variable à intégrer dans OF

build_column('f7cu', IntCol(entity = 'foy',
                label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures",
                val_type = "monetary",
                cerfa_field = u'7CU'))

# TODO: en 2013 et 2012 plus de sofipêche (pourtant présent dans param à ces dates...), case 7gs réutilisée
# Souscription au capital d’une SOFIPECHE
#     build_column('f7gs', IntCol(entity = 'foy',
#                     label = u"Souscription au capital d’une SOFIPECHE",
#                     val_type = "monetary",
#                     cerfa_field = u'7GS',
#                     end = date(2011,12,31)))

build_column('f7gs', IntCol(entity = 'foy',
                label = u"Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon",
                val_type = "monetary",
                cerfa_field = u'7GS',
                start = date(2013, 1, 1)))

# Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
build_column('f7ua', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UA', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7ub', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UB', end = date(2011, 12, 31)))  # vérifier <=2011

# en 2013 et 2012, 7uc se rapporte à autre chose, réutilisation de la case
#    build_column('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UC', end = date(2011,12,31)))  # vérifier <=2011

build_column('f7uc', IntCol(entity = 'foy',
                label = u"Cotisations pour la défense des forêts contre l'incendie ",
                val_type = "monetary",
                cerfa_field = u'7UC',
                start = date(2012, 1, 1)))

build_column('f7ui', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UI', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7uj', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UJ', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7qb', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QB', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7qc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QC', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7qd', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QD', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7ql', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QL', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7qt', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QT', end = date(2011, 12, 31)))  # vérifier <=2011
build_column('f7qm', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7QM', end = date(2011, 12, 31)))  # vérifier <=2011

# Souscription de parts de fonds communs de placement dans l'innovation,
# de fonds d'investissement de proximité
build_column('f7gq', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds communs de placement dans l'innovation",
                val_type = "monetary",
                cerfa_field = u'7GQ'))

build_column('f7fq', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds d'investissement de proximité",
                val_type = "monetary",
                cerfa_field = u'7FQ'))

build_column('f7fm', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse",
                val_type = "monetary",
                cerfa_field = u'7FM'))

build_column('f7fl', IntCol(entity = 'foy',
                label = u"Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer",
                val_type = "monetary",
                cerfa_field = u'7FL'))

# Souscriptions au capital de SOFICA
# Différence de % selon l'année pour le sofica, mais il se peut que cela n'ait aucun impact (si les param sont bons) puisque les cases ne changent pas
#     build_column('f7gn', IntCol(entity = 'foy',
#                     label = u"Souscriptions au capital de SOFICA 48 %",
#                     val_type = "monetary",
#                     cerfa_field = u'7GN',
#                     end = date(2011,12,31)))  # TODO: vérifier <=2011
#     build_column('f7fn', IntCol(entity = 'foy',
#                     label = u"Souscriptions au capital de SOFICA 40 %",
#                     val_type = "monetary",
#                     cerfa_field = u'7FN',
#                     end = date(2011,12,31)))  # TODO: vérifier <=2011

build_column('f7gn', IntCol(entity = 'foy',
                label = u"Souscriptions au capital de SOFICA 36 %",
                val_type = "monetary",
                cerfa_field = u'7GN',
                start = date(2012, 1, 1)))

build_column('f7fn', IntCol(entity = 'foy',
                label = u"Souscriptions au capital de SOFICA 30 %",
                val_type = "monetary",
                cerfa_field = u'7FN',
                start = date(2012, 1, 1)))

# Intérêts d'emprunt pour reprise de société
build_column('f7fh', IntCol(entity = 'foy',
                label = u"Intérêts d'emprunt pour reprise de société",
                val_type = "monetary", cerfa_field = u'7FH'))

# Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée))
build_column('f7ff', IntCol(entity = 'foy',
                label = u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)",
                val_type = "monetary",
                cerfa_field = u'7FF'))

build_column('f7fg', IntCol(entity = 'foy',
                label = u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations",
                cerfa_field = u'7FG'))

# Travaux de conservation et de restauration d’objets classés monuments historiques
build_column('f7nz', IntCol(entity = 'foy',
                label = u"Travaux de conservation et de restauration d’objets classés monuments historiques",
                val_type = "monetary" ,
                cerfa_field = u'7NZ'))

# Dépenses de protection du patrimoine naturel
build_column('f7ka', IntCol(entity = 'foy',
                label = u"Dépenses de protection du patrimoine naturel",
                val_type = "monetary",
                cerfa_field = u'7KA'))

# Intérêts des prêts à la consommation (case UH))
# build_column('f7uh', IntCol(entity = 'foy',
#                 label = u"Intérêts des prêts à la consommation",
#                 val_type = "monetary",
#                 cerfa_field = u'7UH',
#                 end = date(2012, 12, 1)))  # verif <=2012

build_column('f7uh', IntCol(entity = 'foy',
                label = u"Dons et cotisations versés aux partis politiques",
                val_type = "monetary",
                cerfa_field = u'7UH',
                start = date(2013, 1, 1)))

# Investissements forestiers
build_column('f7un', IntCol(entity = 'foy',
                label = u"Investissements forestiers: acquisition",
                val_type = "monetary",
                cerfa_field = u'7UN'))

# Intérêts pour paiement différé accordé aux agriculteurs
build_column('f7um', IntCol(entity = 'foy',
                label = u"Intérêts pour paiement différé accordé aux agriculteurs",
                val_type = "monetary",
                cerfa_field = u'7UM'))

# Investissements locatifs neufs : Dispositif Scellier:
build_column('f7hj', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole",
                val_type = "monetary",
                cerfa_field = u'7HJ'))

build_column('f7hk', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM",
                val_type = "monetary",
                cerfa_field = u'7HK'))

build_column('f7hn', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010",
                val_type = "monetary",
                cerfa_field = u'7HN'))

build_column('f7ho', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010",
                val_type = "monetary",
                cerfa_field = u'7HO'))

build_column('f7hl', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)",
                val_type = "monetary",
                cerfa_field = u'7HL'))

build_column('f7hm', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds",
                val_type = "monetary",
                cerfa_field = u'7HM'))

build_column('f7hr', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 (métropole et DOM ne respectant pas les plafonds): report de 1/9 de l'investissement",
                val_type = "monetary",
                cerfa_field = u'7HR'))

build_column('f7hs', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM et respectant les plafonds: report de 1/9 de l'investissement",
                val_type = "monetary",
                cerfa_field = u'7HS'))

build_column('f7la', IntCol(entity = 'foy',
                label = u"Investissements locatifs neufs dispositif Scellier: report du solde de réduction d'impôt non encore imputé",
                val_type = "monetary",
                cerfa_field = u'7LA'))

# Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
build_column('f7ij', IntCol(entity = 'foy',
                label = u"Investissement destinés à la location meublée non professionnelle: engagement de réalisation de l'investissement en 2011",
                val_type = "monetary",
                cerfa_field = u'7IJ'))

build_column('f7il', IntCol(entity = 'foy',
                label = u"Investissement destinés à la location meublée non professionnelle: promesse d'achat en 2010",
                val_type = "monetary",
                cerfa_field = u'7IL'))

build_column('f7im', IntCol(entity = 'foy',
                label = u"Investissement destinés à la location meublée non professionnelle: investissement réalisés en 2010 avec promesse d'achat en 2009",
                val_type = "monetary",
                cerfa_field = u'7IM'))

build_column('f7ik', IntCol(entity = 'foy',
                label = u"Reports de 1/9 de l'investissement réalisé et achevé en 2009",
                val_type = "monetary",
                cerfa_field = u'7IK'))

build_column('f7is', IntCol(entity = 'foy',
                label = u"Report du solde de réduction d'impôt non encore imputé: année  n-4",
                val_type = "monetary",
                cerfa_field = u'7IS'))

# Investissements locatifs dans les résidences de tourisme situées dans une zone de
# revitalisation rurale

# """
# réutilisation de cases en 2013
# """
# build_column('f7gt', IntCol(entity = 'foy',
#                 label = u"Investissements locatifs dans les résidences de tourisme situées dans une zone de revitalisation rurale",
#                 val_type = "monetary",
#                 cerfa_field = u'7GT',
#                 end = date(2012, 12, 1)))  # vérif <=2012

build_column('f7gt', IntCol(entity = 'foy',
                label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010",
                val_type = "monetary",
                cerfa_field = u'7GT',
                start = date(2013, 1, 1)))  # vérif <=2012

# build_column('f7gu', IntCol(entity = 'foy',
#                 label = u"Investissements locatifs dans les résidences de tourisme situées dans une zone de revitalisation rurale",
#                 val_type = "monetary",
#                 cerfa_field = u'7GU',
#                 end = date(2012, 12, 1)))  # vérif <=2012

build_column('f7gu', IntCol(entity = 'foy',
                label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009",
                val_type = "monetary",
                cerfa_field = u'7GU',
                start = date(2013, 1, 1)))  # vérif <=2012

# build_column('f7gv', IntCol(entity = 'foy',
#                 label = u"Investissements locatifs dans les résidences de tourisme situées dans une zone de revitalisation rurale",
#                 val_type = "monetary",
#                 cerfa_field = u'7GV',
#                 end = date(2012, 12, 1)))  # vérif <=2012

build_column('f7gv', IntCol(entity = 'foy',
                label = u"Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna ",
                val_type = "monetary",
                cerfa_field = u'7GV',
                start = date(2013, 1, 1)))  # vérif <=2012

build_column('f7xg', IntCol(entity = 'foy', label = u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme",
                val_type = "monetary",
                cerfa_field = u'7XG',
                end = date(2012, 12, 1)))  # vérif <=2012

# Avoir fiscaux et crédits d'impôt
# f2ab déjà disponible
build_column('f8ta', IntCol(entity = 'foy',
                label = u"Retenue à la source en France ou impôt payé à l'étranger",
                val_type = "monetary",
                cerfa_field = u'8TA'))

build_column('f8tb', IntCol(entity = 'foy',
                label = u"Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)",  # TODO: différence de label entre les années à voir
                val_type = "monetary",
                cerfa_field = u'8TB'))

build_column('f8tf', IntCol(entity = 'foy',
                label = u"Reprises de réductions ou de crédits d'impôt",
                val_type = "monetary",
                cerfa_field = u'8TF'))

build_column('f8tg', IntCol(entity = 'foy',
                label = u"Crédits d'impôt en faveur des entreprises: Investissement en Corse",
                val_type = "monetary",
                cerfa_field = u'8TG'))

build_column('f8th', IntCol(entity = 'foy',
                label = u"Retenue à la source élus locaux",
                val_type = "monetary",
                cerfa_field = u'8TH'))

build_column('f8tc', IntCol(entity = 'foy',
                label = u"Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))",  # différence de label entre les années à voir
                val_type = "monetary",
                cerfa_field = u'8TC'))

build_column('f8td', IntCol(entity = 'foy',
                label = u"Contribution exceptionnelle sur les hauts revenus",
                cerfa_field = u'8TD'))

build_column('f8te', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé",
                val_type = "monetary",
                cerfa_field = u'8TE'))

build_column('f8to', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures",
                val_type = "monetary",
                cerfa_field = u'8TO'))

build_column('f8tp', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt",
                val_type = "monetary",
                cerfa_field = u'8TP'))

build_column('f8uz', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Famille",
                val_type = "monetary",
                cerfa_field = u'8UZ'))

build_column('f8tz', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Apprentissage",
                val_type = "monetary",
                cerfa_field = u'8TZ'))

build_column('f8wa', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Agriculture biologique",
                val_type = "monetary",
                cerfa_field = u'8WA'))

build_column('f8wb', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Prospection commerciale",
                val_type = "monetary",
                cerfa_field = u'8WB'))
# """
# réutilisation f8wc
# """
# build_column('f8wc', IntCol(entity = 'foy',
#                 label = u"Crédit d'impôt en faveur des entreprises: Nouvelles technologies",
#                 val_type = "monetary",
#                 cerfa_field = u'8WC',
#                 end = date(2012, 12, 1)))  # TODO: verif<=2012

build_column('f8wc', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Prêts sans intérêt",
                val_type = "monetary",
                cerfa_field = u'8WC',
                start = date(2013, 1, 1)))

build_column('f8wd', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise",
                val_type = "monetary",
                cerfa_field = u'8WD'))

build_column('f8we', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Intéressement",
                val_type = "monetary",
                cerfa_field = u'8WE'))

build_column('f8wr', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Métiers d'art",
                val_type = "monetary",
                cerfa_field = u'8WR'))

build_column('f8ws', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes",
                val_type = "monetary",
                cerfa_field = u'8WS',
                end = date(2012, 12, 1)))  # verif<=2012

build_column('f8wt', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs",
                val_type = "monetary",
                cerfa_field = u'8WT'))

build_column('f8wu', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Maître restaurateur",
                val_type = "monetary",
                cerfa_field = u'8WU'))

build_column('f8wv', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Débitants de tabac",
                val_type = "monetary",
                cerfa_field = u'8WV',
                end = date(2012, 12, 1)))  # verif<=2012

build_column('f8wx', IntCol(entity = 'foy',
                label = u"Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise",
                val_type = "monetary",
                cerfa_field = u'8WX',
                end = date(2012, 12, 1)))  # verif<=2012

build_column('f8wy', IntCol(entity = 'foy',
                label = u"",
                val_type = "monetary",
                cerfa_field = u'8WY',
                end = date(2012, 12, 1)))  # verif<=2012

# Acquisition de biens culturels
build_column('f7uo', IntCol(entity = 'foy',
                label = u"Acquisition de biens culturels",
                val_type = "monetary",
                cerfa_field = u'7UO'))

# Mécénat d'entreprise
build_column('f7us', IntCol(entity = 'foy',
                label = u"Réduction d'impôt mécénat d'entreprise",
                val_type = "monetary",
                cerfa_field = u'7US'))

# Crédits d’impôt pour dépenses en faveur de la qualité environnementale
# ('f7wf', IntCol() déjà disponible
# ('f7wh', IntCol() déjà disponible
# ('f7wk', IntCol() déjà disponible
# ('f7wq', IntCol() déjà disponible

build_column('f7sb', IntCol(entity = 'foy',
               label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %",
               val_type = "monetary",
               cerfa_field = u'7SB',
               end = date(2012, 12, 1)))  # TODO: verif<=2012

build_column('f7sc', IntCol(entity = 'foy',
               label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale",
               val_type = "monetary",
               cerfa_field = u'7SC',
               end = date(2012, 12, 1)))  # TODO: verif<=2012

# """
# réutilisation de case pour 2013
# """

# build_column('f7sd', IntCol(entity = 'foy',
#                 label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 40 %",
#                 val_type = "monetary",
#                 cerfa_field = u'7SD',
#                 end = date(2012, 12, 1)))  # TODO: verif<=2012

build_column('f7sd', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation",
                val_type = "monetary",
                cerfa_field = u'7SD',
                start = date(2013, 1, 1)))  # TODO: verif<=2012 et vérifier autres prog comportant f7sd

# build_column('f7se', IntCol(entity = 'foy',
#                 label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 50 %",
#                 val_type = "monetary",
#                 cerfa_field = u'7SE',
#                 end = date(2012, 12, 1)))  # TODO: verif<=2012

build_column('f7se', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz",
                val_type = "monetary",
                cerfa_field = u'7SE',
                start = date(2013, 1, 1)))  # TODO: verif<=2012

# build_column('f7sh', IntCol(entity = 'foy',
#                 label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 15 %",
#                 val_type = "monetary",
#                 cerfa_field = u'7SH',
#                 end = date(2012, 12, 1)))  # TODO: verif<=2012

build_column('f7sh', IntCol(entity = 'foy',
                label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)",
                val_type = "monetary",
                cerfa_field = u'7SH',
                start = date(2013, 1, 1)))  # TODO: verif<=2012

# ('f7wg', IntCol() déjà disponible

# Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???
# build_column('f7up', IntCol(entity = 'foy',
#                 label = u"Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ",
#                 val_type = "monetary",
#                 cerfa_field = u'7UP',
#                 end = date(2007, 12, 1)))  # TODO: vérif date de fin

build_column('f7up', IntCol(entity = 'foy',
                label = u"Crédit d'impôt pour investissements forestiers: travaux",
                val_type = "monetary",
                cerfa_field = u'7UP',
                start = date(2008, 1, 1)))  # TODO: vérif date début, ok pour 13

# build_column('f7uq', IntCol(entity = 'foy',
#                 label = u"Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL",
#                 val_type = "monetary",
#                 cerfa_field = u'7UQ',
#                 end = date(2007, 12, 1)))  # TODO: vérif date de fin

build_column('f7uq', IntCol(entity = 'foy',
                label = u"Crédit d'impôt pour investissements forestiers: contrat de gestion",
                val_type = "monetary",
                cerfa_field = u'7UQ',
                start = date(2008, 1, 1)))  # TODO: vérif date début, ok pour 13

# Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
build_column('f1ar', IntCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité",
                cerfa_field = u'1AR',
                end = date(2012, 12, 1)))  # TODO: vérifier <=2012

build_column('f1br', IntCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité",
                cerfa_field = u'1BR',
                end = date(2012, 12, 1)))  # TODO: vérifier <=2012

build_column('f1cr', IntCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité",
                cerfa_field = u'1CR',
                end = date(2012, 12, 1)))  # TODO: vérifier <=2012

build_column('f1dr', IntCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité",
                cerfa_field = u'1DR',
                end = date(2012, 12, 1)))  # TODO: vérifier <=2012

build_column('f1er', IntCol(entity = 'foy',
                label = u"Crédit d'impôt aide à la mobilité",
                cerfa_field = u'1ER',
                end = date(2012, 12, 1)))  # TODO: vérifier <=2012

# Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
build_column('f4tq', IntCol(entity = 'foy',
                label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail",
                val_type = "monetary",
                cerfa_field = u'4TQ'))  # vérif libéllé, en 2013=Montant des loyers courus du 01/01/1998 au 30/09/1998 provenant des immeubles
                                       # pour lesquels la cessation ou l'interruption de la location est intervenue en 2013 et qui ont été
                                       # soumis à la taxe additionnelle au droit de bail

# Crédits d’impôt pour dépenses en faveur de l’aide aux personnes
# f7wf
# f7wi
# f7wj
# f7wl
build_column('f7sf', IntCol(entity = 'foy',
                label = u"Appareils de régulation du chauffage, matériaux de calorifugeage",
                val_type = "monetary",
                cerfa_field = u'7SF'))

build_column('f7si', IntCol(entity = 'foy',
                label = u"Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)",
                val_type = "monetary",
                cerfa_field = u'7SI'))

# Auto-entrepreneur : versements libératoires d’impôt sur le revenu

build_column('f8uy', IntCol(entity = 'foy',
                label = u"Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé",
                val_type = "monetary",
                cerfa_field = u'8UY'))


# Revenus des professions non salariées

build_column('frag_exon', IntCol(entity = 'ind', label = u"Revenus agricoles exonérés (régime du forfait)", val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HN",
                                    QUIFOY['conj']: u"5IN",
                                    QUIFOY['pac1']: u"5JN", }))  # (f5hn, f5in, f5jn))

build_column('frag_impo', IntCol(entity = 'ind',
                     label = u"Revenus agricoles imposables (régime du forfait)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HO",
                                    QUIFOY['conj']: u"5IO",
                                    QUIFOY['pac1']: u"5JO", }))  # (f5ho, f5io, f5jo))

build_column('arag_exon', IntCol(entity = 'ind',
                     label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HB",
                                    QUIFOY['conj']: u"5IB",
                                    QUIFOY['pac1']: u"5JB", }))  # (f5hb, f5ib, f5jb))

build_column('arag_impg', IntCol(entity = 'ind',
                     label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HC",
                                    QUIFOY['conj']: u"5IC",
                                    QUIFOY['pac1']: u"5JC", }))  # (f5hc, f5ic, f5jc))

build_column('arag_defi', IntCol(entity = 'ind',
                     label = u"Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HF",
                                    QUIFOY['conj']: u"5IF",
                                    QUIFOY['pac1']: u"5JF", }))  # (f5hf, f5if, f5jf))

build_column('nrag_exon', IntCol(entity = 'ind',
                     label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HH",
                                    QUIFOY['conj']: u"5IH",
                                    QUIFOY['pac1']: u"5JH", }))  # (f5hh, f5ih, f5jh))

build_column('nrag_impg', IntCol(entity = 'ind',
                     label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HI",
                                    QUIFOY['conj']: u"5II",
                                    QUIFOY['pac1']: u"5JI", }))  # (f5hi, f5ii, f5ji))

build_column('nrag_defi', IntCol(entity = 'ind',
                     label = u"Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HL",
                                    QUIFOY['conj']: u"5IL",
                                    QUIFOY['pac1']: u"5JL", }))  # (f5hl, f5il, f5jl))

build_column('nrag_ajag', IntCol(entity = 'ind',
                     label = u"Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HM",
                                    QUIFOY['conj']: u"5IM",
                                    QUIFOY['pac1']: u"5JM", }))  # (f5hm, f5im, f5jm))

# Autoentrepreneur
build_column('ebic_impv', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5TA",
                                    QUIFOY['conj']: u"5UA",
                                    QUIFOY['pac1']: u"5VA", }))  # (f5ta, f5ua, f5va))

build_column('ebic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5TB",
                                    QUIFOY['conj']: u"5UB",
                                    QUIFOY['pac1']: u"5VB", }))  # (f5tb, f5ub, f5vb))

build_column('ebnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux imposables (régime auto-entrepreneur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5TE",
                                    QUIFOY['conj']: u"5UE",
                                    QUIFOY['pac1']: u"5VE", }))  # (f5te, f5ue, f5ve))

build_column('mbic_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KN",
                                    QUIFOY['conj']: u"5LN",
                                    QUIFOY['pac1']: u"5MN", }))  # (f5kn, f5ln, f5mn))

build_column('abic_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KB",
                                    QUIFOY['conj']: u"5LB",
                                    QUIFOY['pac1']: u"5MB", }))  # (f5kb, f5lb, f5mb))

build_column('nbic_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KH",
                                    QUIFOY['conj']: u"5LH",
                                    QUIFOY['pac1']: u"5MH", }))  # (f5kh, f5lh, f5mh))

build_column('mbic_impv', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KO",
                                    QUIFOY['conj']: u"5LO",
                                    QUIFOY['pac1']: u"5MO", }))  # (f5ko, f5lo, f5mo))

build_column('mbic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KP",
                                    QUIFOY['conj']: u"5LP",
                                    QUIFOY['pac1']: u"5MP", }))  # (f5kp, f5lp, f5mp))

build_column('abic_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                      val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KC",
                                    QUIFOY['conj']: u"5LC",
                                    QUIFOY['pac1']: u"5MC", }))  # (f5kc, f5lc, f5mc))

build_column('abic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KD",
                                    QUIFOY['conj']: u"5LD",
                                    QUIFOY['pac1']: u"5MD", },
                     end = date(2012, 12, 1)))  # (f5kd, f5ld, f5md))
                                                          # TODO: vérifier date fin

build_column('nbic_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KI",
                                    QUIFOY['conj']: u"5LI",
                                    QUIFOY['pac1']: u"5MI", }
                     ))  # (f5ki, f5li, f5mi))

# """
# réutilisation cases 2013
# """
build_column('nbic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux imposables: régime simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KJ",
                                    QUIFOY['conj']: u"5LJ",
                                    QUIFOY['pac1']: u"5MJ", },
                     end = date(2012, 12, 1)))  # (f5kj, f5lj, f5mj))
                                                          # TODO: vérifier date fin
build_column('nbic_mvct', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux moins-values nettes à court terme",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KJ",
                                    QUIFOY['conj']: u"5LJ",
                                    QUIFOY['pac1']: u"5MJ", },
                     start = date(2013, 1, 1)))  # (f5kj, f5lj, f5mj))
                                                          # vérifier date début #####à intégrer dans OF#######

build_column('abic_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KF",
                                    QUIFOY['conj']: u"5LF",
                                    QUIFOY['pac1']: u"5MF", }))  # (f5kf, f5lf, f5mf))

build_column('abic_defs', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KG",
                                    QUIFOY['conj']: u"5LG",
                                    QUIFOY['pac1']: u"5MG", },
                     end = date(2012, 12, 1)))  # (f5kg, f5lg, f5mg))
                                                          # vérif <=2012

build_column('nbic_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KL",
                                    QUIFOY['conj']: u"5LL",
                                    QUIFOY['pac1']: u"5ML", }))  # (f5kl, f5ll, f5ml))

build_column('nbic_defs', IntCol(entity = 'ind',
                     label = u"Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KL",
                                    QUIFOY['conj']: u"5LM",
                                    QUIFOY['pac1']: u"5MM", }))  # (f5km, f5lm, f5mm))

build_column('nbic_apch', IntCol(entity = 'ind',
                     label = u"Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KS",
                                    QUIFOY['conj']: u"5LS",
                                    QUIFOY['pac1']: u"5MS", }))  # (f5ks, f5ls, f5ms))

build_column('macc_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NN",
                                    QUIFOY['conj']: u"5ON",
                                    QUIFOY['pac1']: u"5PN", }))  # (f5nn, f5on, f5pn))

build_column('aacc_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NB",
                                    QUIFOY['conj']: u"5OB",
                                    QUIFOY['pac1']: u"5PB", }))  # (f5nb, f5ob, f5pb))

build_column('nacc_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NH",
                                    QUIFOY['conj']: u"5OH",
                                    QUIFOY['pac1']: u"5PH", }))  # (f5nh, f5oh, f5ph))

build_column('macc_impv', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NO",
                                    QUIFOY['conj']: u"5OO",
                                    QUIFOY['pac1']: u"5PO", }))  # (f5no, f5oo, f5po))

build_column('macc_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NP",
                                    QUIFOY['conj']: u"5OP",
                                    QUIFOY['pac1']: u"5PP", }))  # (f5np, f5op, f5pp))

build_column('aacc_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NC",
                                    QUIFOY['conj']: u"5OC",
                                    QUIFOY['pac1']: u"5PC", }))  # (f5nc, f5oc, f5pc))

build_column('aacc_imps', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5ND",
                                    QUIFOY['conj']: u"5OD",
                                    QUIFOY['pac1']: u"5PD", }))  # (f5nd, f5od, f5pd))

build_column('aacc_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NF",
                                    QUIFOY['conj']: u"5OF",
                                    QUIFOY['pac1']: u"5PF", }))  # (f5nf, f5of, f5pf))

build_column('aacc_defs', IntCol(entity = 'ind',
                     label = u"Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NG",
                                    QUIFOY['conj']: u"5OG",
                                    QUIFOY['pac1']: u"5PG", }))  # (f5ng, f5og, f5pg))

build_column('nacc_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NI",
                                    QUIFOY['conj']: u"5OI",
                                    QUIFOY['pac1']: u"5PI", }))  # (f5ni, f5oi, f5pi))

build_column('nacc_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NL",
                                    QUIFOY['conj']: u"5OL",
                                    QUIFOY['pac1']: u"5PL", }))  # (f5nl, f5ol, f5pl))

build_column('nacc_defs', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NM",
                                    QUIFOY['conj']: u"5OM",
                                    QUIFOY['pac1']: u"5PM", }))  # (f5nm, f5om, f5pm))

build_column('mncn_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KU",
                                    QUIFOY['conj']: u"5LU",
                                    QUIFOY['pac1']: u"5MU", }))  # (f5ku, f5lu, f5mu))

build_column('cncn_bene', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5SN",
                                    QUIFOY['conj']: u"5NS",
                                    QUIFOY['pac1']: u"5OS", }))  # (f5sn, f5ns, f5os))

build_column('cncn_defi', IntCol(entity = 'ind',
                     label = u"Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5SP",
                                    QUIFOY['conj']: u"5NU",
                                    QUIFOY['pac1']: u"5OU", }))  # (f5sp, f5nu, f5ou, f5sr))
                                                                  # pas de f5sr en 2013

build_column('mbnc_exon', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HP",
                                    QUIFOY['conj']: u"5IP",
                                    QUIFOY['pac1']: u"5JP", }))  # (f5hp, f5ip, f5jp))

build_column('abnc_exon', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QB",
                                    QUIFOY['conj']: u"5RB",
                                    QUIFOY['pac1']: u"5SB", }))  # (f5qb, f5rb, f5sb))

build_column('nbnc_exon', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QH",
                                    QUIFOY['conj']: u"5RH",
                                    QUIFOY['pac1']: u"5SH", }))  # (f5qh, f5rh, f5sh))

build_column('mbnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HQ",
                                    QUIFOY['conj']: u"5IQ",
                                    QUIFOY['pac1']: u"5JQ", }))  # (f5hq, f5iq, f5jq))

build_column('abnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QC",
                                    QUIFOY['conj']: u"5RC",
                                    QUIFOY['pac1']: u"5SC", }))  # (f5qc, f5rc, f5sc))

build_column('abnc_defi', IntCol(entity = 'ind',
                     label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QE",
                                    QUIFOY['conj']: u"5RE",
                                    QUIFOY['pac1']: u"5SE", }))  # (f5qe, f5re, f5se))

build_column('nbnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QI",
                                    QUIFOY['conj']: u"5RI",
                                    QUIFOY['pac1']: u"5SI", }))  # (f5qi, f5ri, f5si))

build_column('nbnc_defi', IntCol(entity = 'ind',
                     label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QK",
                                    QUIFOY['conj']: u"5RK",
                                    QUIFOY['pac1']: u"5SK", }))  # (f5qk, f5rk, f5sk))

build_column('mbic_mvct', IntCol(entity = 'foy',
                     label = u"Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = u'5HU',
                     end = date(2012, 12, 1)))  # (f5hu))
                                                          # vérif <=2012

build_column('macc_mvct', IntCol(entity = 'foy', label = u"Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = u'5IU'))  # (f5iu))

build_column('mncn_mvct', IntCol(entity = 'foy',
                     label = u"Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = u'JU'))  # (f5ju))

build_column('mbnc_mvct', IntCol(entity = 'foy', label = u"Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KZ",
                                    QUIFOY['conj']: u"5LZ",
                                    QUIFOY['pac1']: u"5MZ", }))  # (f5kz, f5lz , f5mz), f5lz , f5mz sont présentent en 2013
                                                                  # TODO: intégrer f5lz , f5mz à OF

build_column('frag_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles  à court terme (régime du forfait)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HW",
                                    QUIFOY['conj']: u"5IW",
                                    QUIFOY['pac1']: u"5JW", }))  # (f5hw, f5iw, f5jw))

build_column('mbic_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KX",
                                    QUIFOY['conj']: u"5LX",
                                    QUIFOY['pac1']: u"5MX", }))  # (f5kx, f5lx, f5mx))

build_column('macc_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NX",
                                    QUIFOY['conj']: u"5OX",
                                    QUIFOY['pac1']: u"5PX", }))  # (f5nx, f5ox, f5px))

build_column('mbnc_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)",
                      val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HV",
                                    QUIFOY['conj']: u"5IV",
                                    QUIFOY['pac1']: u"5JV", }))  # (f5hv, f5iv, f5jv))

build_column('mncn_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KY",
                                    QUIFOY['conj']: u"5LY",
                                    QUIFOY['pac1']: u"5MY", }))  # (f5ky, f5ly, f5my))

build_column('mbic_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KR",
                                    QUIFOY['conj']: u"5LR",
                                    QUIFOY['pac1']: u"5MR", }))  # (f5kr, f5lr, f5mr))

build_column('macc_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NR",
                                    QUIFOY['conj']: u"5OR",
                                    QUIFOY['pac1']: u"5PR", }))  # (f5nr, f5or, f5pr))

build_column('mncn_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KW",
                                    QUIFOY['conj']: u"5LW",
                                    QUIFOY['pac1']: u"5MW", }))  # (f5kw, f5lw, f5mw))

build_column('mbnc_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HS",
                                    QUIFOY['conj']: u"5IS",
                                    QUIFOY['pac1']: u"5JS", }))  # (f5hs, f5is, f5js))

build_column('frag_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles de cession taxables à 16% (régime du forfait)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HX",
                                    QUIFOY['conj']: u"5IX",
                                    QUIFOY['pac1']: u"5JX", }))  # (f5hx, f5ix, f5jx))

build_column('arag_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HE",
                                    QUIFOY['conj']: u"5IE",
                                    QUIFOY['pac1']: u"5JE", }))  # (f5he, f5ie, f5je))

build_column('nrag_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HK",
                                    QUIFOY['conj']: u"5LK",
                                    QUIFOY['pac1']: u"5JK", },
                     end = date(2012, 12, 1)))  # TODO: vérif <=2012))  # (f5hk, f5lk, f5jk))

build_column('mbic_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KQ",
                                    QUIFOY['conj']: u"5LQ",
                                    QUIFOY['pac1']: u"5MQ", }))  # (f5kq, f5lq, f5mq))

build_column('abic_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KE",
                                    QUIFOY['conj']: u"5LE",
                                    QUIFOY['pac1']: u"5ME", }))  # (f5ke, f5le, f5me))

build_column('nbic_pvce', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5IK",
                                    QUIFOY['conj']: u"5KK",
                                    QUIFOY['pac1']: u"5MK", }))  # (f5kk, f5ik, f5mk))

build_column('macc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NQ",
                                    QUIFOY['conj']: u"5OQ",
                                    QUIFOY['pac1']: u"5PQ", }))  # (f5nq, f5oq, f5pq))

build_column('aacc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NE",
                                    QUIFOY['conj']: u"5OE",
                                    QUIFOY['pac1']: u"5PE", }))  # (f5ne, f5oe, f5pe))

build_column('nacc_pvce', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NK",
                                    QUIFOY['conj']: u"5OK",
                                    QUIFOY['pac1']: u"5PK", }))  # (f5nk, f5ok, f5pk))

build_column('mncn_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KV",
                                    QUIFOY['conj']: u"5LV",
                                    QUIFOY['pac1']: u"5MV", }))  # (f5kv, f5lv, f5mv))

build_column('cncn_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5SO",
                                    QUIFOY['conj']: u"5NT",
                                    QUIFOY['pac1']: u"5OT", }))  # (f5so, f5nt, f5ot))

build_column('mbnc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HR",
                                    QUIFOY['conj']: u"5IR",
                                    QUIFOY['pac1']: u"5JR", }))  # (f5hr, f5ir, f5jr))

build_column('abnc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QD",
                                    QUIFOY['conj']: u"5RD",
                                    QUIFOY['pac1']: u"5SD", }))  # (f5qd, f5rd, f5sd))

build_column('nbnc_pvce', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QJ",
                                    QUIFOY['conj']: u"5RJ",
                                    QUIFOY['pac1']: u"5SJ", }))  # (f5qj, f5rj, f5sj))


# """
# CASES MANQUANTES PRESENTENT DANS LA DECLARATION DES REVENUS 2013 et 2012
# """
# # A CREER ET A INTEGRER DANS OF
#
# """
# ### VOS REVENUS
#
# #revenu de solidarité active
# pour le foyer:1BL
# 1ere PAC: 1CB
# 2ème PAC: 1DQ
#
# #pensions, retraites, rentes, rentes viagères à titre onéreux
# Pensions de retraite en capital taxables à 7.5%
# vous:1AT
# conj:1BT
#
# #gains de levée d'options, revenus éxonérés ou non imposables en France, revenus exceptionnels ou différés
#     #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 28/9/2012
#     imposables en salaires:
#     vous:1TT
#     conj:1UT
#
#     #gains et distributions provenant de parts ou actions de carried-interest, déclarés cases 1AJ ou 1BJ, soumis à la contribution salariale de 30 %
#     vous:1NY
#     conj:1OY
#
#     #agents d'assurance: salaires éxonérés
#     vous:1AQ
#     conj:1BQ
#
#     #salariés impatriés: salaires et primes éxonérés
#     vous:1DY
#     conj:1EY
#
#     #salaires imposables à l'étranger, non déclarés cases 1Aj ou 1BJ, retenus pour le calcul de la prime pour l'emploi
#     vous:1LZ
#     conj:1MZ
#
#     #sommes éxonérées transférées du CET au PERCO ou à un régime supplémentaire d'entreprise
#     vous: 1SM
#     conj:1DN
#
#     #fonctionnaires d'organisations internationales: rémunérations exonérées
#     vous: 1TY
#     conj:1UY
#     end = date(2012, 12, 31),
#
# #salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif
# (n'indiquez pas ces revenus ligne 8TI (2042) ni ligne 1LZ et 1MZ).
#
#     #total de vos salaires

build_column('sal_pen_exo_etr', IntCol(entity = 'ind',
                     label = u"Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"1AC",
                                    QUIFOY['conj']: u"1BC",
                                    QUIFOY['pac1']: u"1CC",
                                    QUIFOY['pac2']: u"1DC", },
                     start = date(2013, 1, 1),))

#     vous:1AC
#     conj:1BC
#     pac1:1CC
#     pac2:1DC
#     start = date(2013, 1, 1),
#
#     #montant de l'impôt acquitté à l'étranger
#     vous:1AD
#     conj:1BD
#     pac1:1CD
#     pac2:1DD
#     start = date(2013, 1, 1),
#
#     #frais rééls
#     vous:1AE
#     conj:1BE
#     pac1:1CE
#     pac2:1DE
#     start = date(2013, 1, 1),
#
#     #pour recevoir la PPE: activité à temps plein exercée à l'étranger toute l'année
#     vous:1AX
#     conj:1BX
#     pac1:1CX
#     pac2:1DX
#     start = date(2013, 1, 1),
#
#     #pour recevoir la PPE: sinon, nombre d'heures payées dans l'année
#     vous:1AG
#     conj:1BG
#     pac1:1CG
#     pac2:1DG
#     start = date(2013, 1, 1),
#
#     #pensions exonérées de source étrangère: total des pensions nettes encaissées
#     vous:1AH
#     conj:1BH
#     pac1:1CH
#     pac2:1DH
#     start = date(2013, 1, 1),
#
# #revenus exceptionnels ou différés à imposer selon le système du quotient
# montant total des revenus à imposer selon le système du quotient: 0XX
#
# #plus-values et gains divers
#     #gains de cession de bons de souscription de parts de créateurs d'entreprise taxable à 19 %:3SJ
#     #gains de cession de bons de souscription de parts de créateurs d'entreprise taxable à 30 %:3SK
#
#     #gains de cession de valeurs mobilières, de droits sociaux et assimilés:
#         #abattement net pour durée de détention appliquée:
#             #sur des plus-values:3SG
#             #sur des moins-values:3SH
#             start = date(2013, 1, 1),
#         #abattement net pour durée de détention renforcée appliquée:
#             #sur des plus-values:3SL
#             #sur des moins-values:3SM
#             start = date(2013, 1, 1),
#     #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 16.10.2007, soumis à la contribution salariale de 8 %
#         vous:3VO
#         conj:3SO
#         end = date(2012, 12, 31),
#     #gains de levée d'options sur titres et gains d'acquisition d'actions gratuites attribuées à compter du 16/10/2007, soumis à la contributin salariale de 10%:
#         vous:3VN
#         conj:3SN
#     #gains d'acquisition d'actions gratuites attribuées à compter du 16/10/2007, soumis à la contribution salariale de 2,5%
#         vous:3VS
#         conj:3SS
#         end = date(2012, 12, 31),
#     #impatriés: cessions de titres détenus à l'étranger (report de la déclaration 2047 IMP)
#         #plus-values exonérées (50 %):3VQ
#         #moins-values non imputables (50 %):3VR
#     #plus-values en report d'imposition (art 150-0 D ter du CGI):3WE
#         #plus-values taxables à 24 %:3SB
#     #plus-values en report d'imposition (art 150-0 B ter du CGI):3WH             start = date(2013, 1, 1),
#     #plus-values dont le report à expiré en 2012:
#         #plus-values taxables à 19 %:3SC    end = date(2012, 12, 31),
#     #transfert du domicile hors de France, report de la déclaration 2074 ET:
#         #plus-values et créances dont l'imposition est en sursis de paiement:
#             #plus-values imposables:3WA
#             #plus-values taxables à 19 %:3WF             start = date(2013, 1, 1),
#             #abattement pour durée de détention en cas de départ à la retraite d'un dirigeant:3WC    end = date(2012, 12, 31),
#         #plus-values et créances dont l'imposition ne bénéficie pas du sursis de paiement:
#             #plus-values imposables:3WB
#             #plus-values taxables à 19 %:3WG             start = date(2013, 1, 1),
#             #abattement pour durée de détention:3WD
#             #plus-values imposables (art 150-0 D ter bis du CGI):3WI            start = date(2013, 1, 1),
#             #plus-values taxables à 19 % (art 150-0 D ter bis du CGI):3WJ            start = date(2013, 1, 1),
#     #plus-values de cession de titres de jeunes entreprises innovantes exonérées:3VP
#     #plus-values exonérées de cession de participations supérieures à 25 % au sein du groupe familial:3VY
#     #plus-values de cession d'une résidence secondaire exonérée sous condition de remploi:3VW
#     #plus-values réalisées par les non-résidents:
#         #plus-values de cession de droits sociaux art 244 bis B du CGI et distributions de sociétés de capital-risque:3SE
#
# #revenus fonciers
#     #amortissement "Robien" et "Borloo neuf" déduit des revenus fonciers 2013 (investissements réalisés en 2009):4BY
#     #taxe sur les loyers élevés (report de la déclaration 2042 LE):4BH
#
# #revenus agricoles
#     #revenus des exploitants forestiers (régime du forfait)
#     vous:5HD
#     conj:5ID
#     pac1:5JD
#     #régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur:
#         #jeunes agriculteurs, abattement de 50% ou 100% :
#         vous:5HZ
#         conj:5IZ
#         pac1:5JZ
#     #déficits agricoles des années antérieures du foyer non encore déduits:
#     2007:5QF
#     2008:5QG
#     2009:5QN
#     2010:5QO
#     2011:5QP
#     2012:5QQ
#
# #revenus non commerciaux professionnels:
#     #régime de la déclaratin contrôlée, revenus bénéficiant de l'abattement association agrée ou viseur
#         #jeunes créateurs abattement 50 %:
#         vous:5QL
#         conj:5RL
#         pac1:5SL
#         #honoraires de prospection commerciale exonérs:
#         vous:5TF
#         conj:5UF
#         pac1:5VF
#     #régime de la déclaratin contrôlée, revenus ne bénéficiant pas de l'abattement association agrée
#         #honoraires de prospection commerciale exonérs:
#         vous:5TI
#         conj:5UI
#         pac1:5VI
#
# #revenus non commerciaux non professionnels
#     #régime déclaratif spécial ou micro BNC (recettes brutes sans déduction d'abattement)
#         #revenus nets exonérés
#         vous:5TH
#         conj:5UH
#         pac1:5VH
#     #régime de la déclaration contrôlée
#         #revenus imposables avec AA ou viseur
#         vous:5JG
#         conj:5RF
#         pac1:5SF
#         #déficits avec AA ou viseur
#         vous:5JJ
#         conj:5RG
#         pac1:5SG
#         #inventeurs et auteurs de logiciels: produits taxables à 16 % avec AA ou viseur
#         vous:5TC
#         conj:5UC
#         pac1:5VC
#         #jeunes créateurs abattement de 50 %, avec AA ou viseur
#         vous:5SV
#         conj:5SW
#         pac1:5SX
#     #déficits des années antérieures non encore déduite=s:
#     2007:5HT
#     2008:5IT
#     2009:5JT
#     2010:5KT
#     2011:5LT
#     2012:5MT
#
# #revenus à imposer aux prélèvements sociaux
#     #revenus nets:
#     vous:5HY
#     conj:5IY
#     pac1:5JY
#     #plus-values à long terme exonérées en cas de départ à la retraite
#     vous:5HG
#     conj:5IG
#
# #revenus industriels et commerciaux professionnels
#     #régime du bénéfice réel:
#         #locations meublées avec CGA ou viseur:
#         vous:5HA
#         conj:5IA
#         pac1:5JA
#         #locations meublées sans CGA:
#         vous:5KA
#         conj:5LA
#         pac1:5MA
#         #déficit locations meublées avec CGA ou viseur:
#         vous:5QA
#         conj:5RA
#         pac1:5SA
#
# #revenus industriels et commerciaux non professionnels
#     #déficits industriels et commerciaux non professionnels des années antérieures non encore déduits
#     2007:5RN
#     2008:5RO
#     2009:5RP
#     2010:5RQ
#     2011:5RR
#     2012:5RW
#
# #locations meublées non professionnelles
#     #régime du bénéfice réel
#         #revenus imposables avec CGA ou viseur:
#         vous:5NA
#         conj:5OA
#         pac1:5PA
#         #déficits avec CGA ou viseur:
#         vous:5NY
#         conj:5OY
#         pac1:5PY
#         #déficits sans CGA:
#         vous:5NZ
#         conj:5OZ
#         pac1:5PZ
#         #déficits des années antérieures non encore déduits:
#         2003:5GA
#         2004:5GB
#         2005:5GC
#         2006:5GD
#         2007:5GE
#         2008:5GF
#         2009:5GG
#         2010:5GH
#         2011:5GI
#         2012:5GJ
#
# ### CHARGES ET IMPUTATIONS DIVERSES
#
#     #epargne retraite PERP et produits assimilés (PREFON, COREM et C.G.O.S)
#         #vous souhaitez bénéficier du plafond de votre conjoint, cochez la case:6QR
#         #si vous êtes nouvellement domicilié en France en 2013 après avoir résidé à l'étranger au cours des 3 années précédentes:6QW
#         #Détermination du plafond de déduction pour les revenus 2013 au titre de l'Epargne Retraite (PERP, Préfon et assimilés):
#           Cotisations versées en 2013(ou 2012 pour les revenus 2012) aux régimes obligatoires d'entreprise de retraite  supplémentaire "article 83", PERCO et, pour leur montant total ou partiel,
#           celles versées aux régimes ou contrats facultatifs de retraite "Madelin" et "Madelin agricole":
#           vous:6QS
#           conj:6QT
#           pac1:6QU
#
# ### CHARGES OUVRANT DROIT A REDUCTION OU CREDIT D'IMPOT
#     #dons à des organismes d'intérêt général établis dans l'Etat européen:
#         #dons à des organismes d'aides aux personnes:7VA
#         #dons à des autres organismes:7VC
#     #dépenses en faveur de la qualité environnementale de l'habitation principale
#         #vous avez réalisé des dépenses d'isolation thermique des murs donnant sur l'extérieur, travaux effectués sur au moins la moitié de la surface totale des murs: 7WC
#         #vous avez réalisé des dépenses d'isolation thermique des toitures, travaux effectués sur la totalité de la toiture:7VG
#         #isolation thermique:
#             #matériaux d'isolation des murs (montant acquisition et pose):7SG
#             #matériaux d'isolation thermique des parois vitrées (montant):7SJ
#             #volets isolants (montant):7SK
#             #porte d'entrée donnant sur l'extérieur (montant):7SL
#         #equipement de production d'énergie utilisant une source d'énergie renouvelable
#             #Équipements de production d'électricité utilisant l'énergie radiative du soleil (panneaux photovoltaïques):7SM
#             #Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent:7SN
#             #Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent:7SO
#             #Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur:7SP
#             #Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur (y compris le coût de la pose de l'échangeur de chaleur souterrain):7SQ
#             #Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques):7SR
#             #Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires (chauffe-eaux solaires...):7SS
#             #Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (énergie éolienne, hydraulique…):7ST
#         #Autres dépenses
#             # Équipements de récupération et de traitement des eaux pluviales:7SU
#             #Diagnostic de performance énergétique:7SV
#             #Équipements de raccordement à un réseau de chaleur:7SW
#     #dépenses en faveur de la qualité environnementale de l'habitation principale cases manquantes sur la déclaration des revenus 2012
#         #vous avez réalisé une seule catégorie de travaux dans votre habitation principale située dans un immeuble collectif, portez le montant des dépenses dans les rubriques 7TT à 7TY en fonction du taux du crédit d'impôt  applicable
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 10%: 7TT    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 11%: 7TU    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 15%: 7TV    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 17%: 7TW    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 26%: 7TX    end = date(2012, 12, 31),
#             #Dépenses ouvrant droit au crédit d'impôt au taux de 32%: 7TY    end = date(2012, 12, 31),
#         #Vous avez réalisé un bouquet de travaux ou si votre habitation principale est une maison individuelle cochez les cases adéquates (7WH à 7VG) et portez le montant des dépenses aux rubriques concernées (7SD à 7SW)
#             #Vous avez réalisé des dépenses d'isolation thermique des parois vitrées
#                 #vous avez engagé les dépenses à compter du 4.4.2012: 7WS    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'acquisition de volets isolants
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 1.1.2012: 7WU    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses en 2012: 7WV    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'acquisition de portes d'entrée donnant sur l'extérieur
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 1.1.2012: 7WW    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses en 2012: 7WX    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'isolation thermique des murs donnant sur l'extérieur
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 4.4.2012: 7WA    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses du 4.4.2012 au 31.12.2012: 7WB    end = date(2012, 12, 31),
#             #Vous avez réalisé des dépenses d'isolation thermique des toitures
#                 #vous avez engagé les dépenses (accepté un devis et versé un acompte) avant le 4.4.2012: 7VE    end = date(2012, 12, 31),
#                 #vous avez engagé les dépenses du 4.4.2012 au 31.12.2012: 7VF    end = date(2012, 12, 31),
#     #dépenses en faveur de la qualité environnementale des habitations données en location
#         #montant du crédit d'impôt calculé:7SZ
#     #travaux de prévention des risques technologiques dans les logements données en location (report 2041 gr)
#         #dépenses réalisées en 2013:7WR
#     #travaux de restauration immobilière: loi Malraux
#         #opérations engagées avant le 1/1/2011:
#             #dans un secteur sauvegardé ou assimilé:7RD
#             #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7RC
#         #opérations engagées en 2012:
#             #dans un secteur sauvegardé ou assimilé:7RF
#             #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7RE
#         #opérations engagées en 2013:
#             #dans un secteur sauvegardé ou assimilé:7SY
#             #dans une zone de protection du patrimoine architectural, urbain et paysager (ZPPAUP) ou une aire de mise en valeur de l'architecture et du patrimoine (AMVAP):7SX
#     #dépenses de protection du patrimoine naturel
#         #report de réduction d'impôt non encore imputée de l'année 2010:7KB
#         #report de réduction d'impôt non encore imputée de l'année 2011:7KC
#         #report de réduction d'impôt non encore imputée de l'année 2012:7KD
#     #investissement locatifs: loi Duflot
#         #investissement réalisés et achevés en 2013:
#             #en métropole:7GH start = date(2013, 1, 1),
#             #outre-mer:7GI    start = date(2013, 1, 1),
#     #investissement locatifs neufs: loi Scellier
#         #investissement achevés ou acquis en 2013:
#             #investissements réalisés de 1/1/2013 au 31/03/2013 avec engagement de réalisation en 2012:
#                 #Métropole, logement BBC:7FA    start = date(2013, 1, 1),
#                 #Métropole, logement non-BBC:7FB    start = date(2013, 1, 1),
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7FC    start = date(2013, 1, 1),
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7FD    start = date(2013, 1, 1),
#             #investissements réalisés en 2012 avec engagement de réalisation de l'investissement à compter du 1/1/2012:
#                 #Métropole, logement BBC:7JA
#                 #Métropole, logement non-BBC:7JF
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JK
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JO
#             #investissements réalisés en 2012 avec engagement de réalisation de l'investissement en 2011:
#                 #Métropole, logement BBC:7JB
#                 #Métropole, logement non-BBC:7JG
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JL
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JP
#             #investissements réalisés en 2012, logement acquis en l'état de futur achévement avec contrat de réservation enregistré au plus tard le 31/12/2011:
#                 #investissements réalisés du 1/1/2012 au 31/3/2012:
#                     #Métropole, logement BBC:7JD
#                     #Métropole, logement non-BBC:7JH
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JM
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JQ
#                 #investissements réalisés du 1/4/2012 au 31/12/2012:
#                     #Métropole, logement BBC:7JE
#                     #Métropole, logement non-BBC:7JJ
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7JN
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7JR
#             #investissements réalisés en 2011 avec engagement de réalisation de l'investissement à compter du 1/1/2011:
#                 #Métropole, logement BBC:7NA
#                 #Métropole, logement non-BBC:7NF
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NK
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NP
#             #investissements réalisés en 2011 avec engagement de réalisation de l'investissement en 2010:
#                 #Métropole, logement BBC:7NB
#                 #Métropole, logement non-BBC:7NG
#                 #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NL
#                 #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NQ
#             #investissements réalisés en 2011, logement acquis en l'état de futur achévement avec contrat de réservation enregistré au plus tard le 31/12/2010:
#                 #investissements réalisés du 1/1/2011 au 31/1/2011:
#                     #Métropole, logement BBC:7NC
#                     #Métropole, logement non-BBC:7NH
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NM
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NR
#                 #investissements réalisés du 1/2/2011 au 31/3/2011:
#                     #Métropole, logement BBC:7ND
#                     #Métropole, logement non-BBC:7NI
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NN
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NS
#                 #investissements réalisés du 1/4/2011 au 31/12/2011:
#                     #Métropole, logement BBC:7NE
#                     #Métropole, logement non-BBC:7NJ
#                     #DOM, St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7NO
#                     #Polynésie, Nouvelle Calédonie, Wallis et Futuna:7NT
#             #report concernant les investissements achevés ou acquis au cours des années antérieures:
#                 #investissements achevés en 2012: report de 1/9 de la réduction d'impôt:
#                     #investissements réalisés en 2012:
#                         #investissements réalisés en 2012, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GJ    start = date(2013, 1, 1),
#                         #investissements réalisés en 2012 avec promesse d'achat en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GK    start = date(2013, 1, 1),
#                     #investissements réalisés en 2011:
#                         #investissements réalisés en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GL    start = date(2013, 1, 1),
#                         #investissements réalisés en 2011 avec promesse d'achat en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GP    start = date(2013, 1, 1),
#                     #investissements réalisés en 2010:
#                         #investissements réalisés en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7GS
#                 #investissements achevés en 2011: report de 1/9 de la réduction d'impôt:
#                     #investissements réalisés en 2011:
#                         #investissements réalisés en 2011, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7HA
#                         #investissements réalisés en 2011 avec promesse d'achat en 2010, en Métropole, dans les DOM, à St-Barthélemy, St-Martin, St-Pierre-et-Miquelon:7HB
#                     #investissements réalisés en 2010:
#                         #investissements réalisés en 2010, en Métropole et dans les DOM-COM:7HD
#                         #investissements réalisés en 2010 avec promesse d'achat avant le 1/1/2010, en Métropole et dans les DOM-COM:7HE
#                     #investissements réalisés en 2009, en Métropole et dans les DOM-COM:7HF
#                 #investissements réalisés et achevés en 2011: report de 1/5 de la réduction d'impôt:
#                     #investissement en Polynésie, Nouvelle Calédonie, dans les îles Wallis et Futuna:7HG
#                     #investissement en Polynésie, Nouvelle Calédonie, dans les îles Wallis et Futuna avec promesse d'achat en 2010:7HH
#             #investissements achevés en 2010:report de 1/9 de l'investissement:
#                 #investissement réalisés et achevés en 2010, en Métropole:7HV
#                 #investissement réalisés et achevés en 2010, dans les DOM-COM:7HW
#                 #investissement réalisés et achevés en 2010, en Métropole avec promesse d'achat avant le 1/1/2010:7HX
#                 #investissement réalisés et achevés en 2010, dans les DOM-COM avec promesse d'achat avant le 1/1/2010:7HZ
#             #investissements réalisés en 2009 et achevés en 2010:
#                 #investissement réalisés en 2009 et achevés en 2010, en Métropole en 2009, dans les DOM du 1/1/2009 au 26/5/2009, dans les DOM du 27/5/2009 au 30/12/2009 lorsqu'ils ne respectent pas les plafonds spécifiques:7HT
#                 #investissement réalisés et achevés en 2010, dans les DOM-COM du 27/5/2009 au 31/12/2009 respectant les plafonds spécifiques:7HU
#             #report du solde des réductions d'impôts non encore imputé
#                 #investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1/1/2010:
#                     #report de l'année 2010:7LB
#                     #report de l'année 2011:7LE
#                     #report de l'année 2012:7LM    start = date(2013, 1, 1),
#                 #investissements réalisés et achevés en 2010, ou réalisés en 2010 et achevés en 2011, ou rélisés et achevés en 2011 avec engagement en 2010:
#                     #report de l'année 2010:7LC
#                     #report de l'année 2011:7LD
#                     #report de l'année 2012:7LS    start = date(2013, 1, 1),
#                 #investissements réalisés et achevés en 2011: report du solde de réduction d'impôt de l'année 2011:7LF
#                 #investissements réalisés et achevés en 2011: report du solde de réduction d'impôt de l'année 2012:7LZ    start = date(2013, 1, 1),
#                 #investissements réalisés et achevés en 2012: report du solde de réduction d'impôt de l'année 2012:7MG    start = date(2013, 1, 1),
#     #investissement destinés à la location meublée non professionnelle: loi Censi-Bouvard
#             #investissement réalisés en 2013:
#                 #engagement de réalisation de l'investissement en 2013:7JT    start = date(2013, 1, 1),
#                 #engagement de réalisation de l'investissement en 2012:7JU    start = date(2013, 1, 1),
#             #investissement réalisés en 2012:
#                 #engagement de réalisation de l'investissement en 2012:7ID
#                 #promesse d'achat en 2011:7IE
#                 #logement acquis en l'état de futur achèvement avec contrat de réservation enregistré au plus tard le 31/12/2011:
#                     #investissement réalisé 1/1/2012 au 31/03/2012:7IF
#                     #investissement réalisé 1/4/2012 au 31/12/2012:7IG
#             #investissement réalisés en 2011:
#                 #logement acquis en l'état de futur achèvement avec contrat de réservation enregistré au plus tard le 31/12/2010:
#                     #investissement réalisé 1/1/2011 au 31/03/2011:7IN
#                     #investissement réalisé 1/4/2011 au 31/12/2011:7IV
#             #investissement réalisés en 2010:
#                 #promesse d'achat en 2009:7IW
#             #investissement réalisés en 2009:7IO
#     #report de 1/9 de la réduction d'impôt des:
#         #investissements réalisés et achevés en 2012
#             #réalisés en 2012:7JV    start = date(2013, 1, 1),
#             #réalisés en 2011 ou réalisés en 2012 avec promesse d'achat en 2011:7JW    start = date(2013, 1, 1),
#             #réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010:7JX    start = date(2013, 1, 1),
#         #investissements achevés en 2011: report de 1/9 de la réduction d'impôt:
#             #réalisés en 2011:7IA
#             #réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010:7IB
#             #réalisés en 2010 avec promesse d'achat en 2009 ou réalisés en 2009:7IC
#         #investissements achevés en 2010: report de 1/9 de l'investissement:
#             #réalisés en 2010:7IP
#             #réalisés en 2010 avec promesse d'achat en 2009:7IQ
#             #réalisés en 2009:7IR
#     #report du solde de réduction d'impôt non encore imputé:
#         #investissements réalisés et achevés en 2009, réalisés en 2009 et achevés en 2010, réalisés et achevés en 2010 avec engagement avant le 1/1/2010
#             #report du solde de réduction d'impôt de l'année 2010:7IU
#             #report du solde de réduction d'impôt de l'année 2011:7IX
#          #investissements réalisés et achevés en 2010, réalisés en 2010 et achevés en 2011, réalisés et achevés en 2011 avec engagement en 2010
#             #report du solde de réduction d'impôt de l'année 2010:7IT
#             #report du solde de réduction d'impôt de l'année 2011:7IH
#             #report du solde de réduction d'impôt de l'année 2012:7JC    start = date(2013, 1, 1),
#         #investissements réalisés et achevés en 2011, réalisés en 2011 et achevés en 2011 ou 2012, réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012
#             #report du solde de réduction d'impôt de l'année 2011:7IZ
#             #report du solde de réduction d'impôt de l'année 2012:7JI    start = date(2013, 1, 1),
#         #investissements réalisés et achevés en 2012
#             #report du solde de réduction d'impôt de l'année 2012:7JS    start = date(2013, 1, 1),
#     #Vos autres charges ouvrant droit à réduction d'impôt ou à crédit d'impôt
#         #sommes versées pour l'emploi d'un salarié à domicile
#             #si vous avez engagé les dépenses pour un ascendant bénéficiaire de l'APA:7DD
#             #souscription au capital de petites entreprises en phase  d'amorçage, de démarrage ou d'expansion: reports des versements 2012 (2011 pour la déclaration des revenus de 2012):7CQ
#             #investissements forestiers:
#                 #assurance:7UL
#                 #si les travaux sont consécutifs à un sinistre:7UT
#                 #report des dépenses de travaux de l'année 2009:
#                     #hors sinistre:7UU
#                     #après sinistre:7TE
#                 #report des dépenses de travaux de l'année 2010:
#                     #hors sinistre:7UV
#                     #après sinistre:7TF
#                 #report des dépenses de travaux de l'année 2011:
#                     #hors sinistre:7UW
#                     #après sinistre:7TG
#                 #report des dépenses de travaux de l'année 2012:
#                     #hors sinistre:7UX    start = date(2013, 1, 1),
#                     #après sinistre:7TH    start = date(2013, 1, 1),
#             #investissement locatif dans le secteur touristique:
#                 #acquisition d'un logement neuf:
#                     #report des dépenses d'investissement effectuées en 2010:7XP
#                     #report des dépenses d'investissement effectuées en 2012:7UY    start = date(2013, 1, 1),
#                 #réhabilitation d'un logement
#                     #report des dépenses d'investissement effectuées en 2010:7XQ
#                     #report des dépenses d'investissement effectuées en 2011:7XV
#                     #report des dépenses d'investissement effectuées en 2012:7UZ    start = date(2013, 1, 1),
#                 #Travaux de reconstruction, d'agrandissement, de réparation ou d'amélioration payés en 2012
#                     #Travaux engagés avant le 1.1.2011
#                         #Dans un village résidentiel de tourisme 7XA    end = date(2012, 12, 31),
#                         #Dans une résidence de tourisme classée ou un meublé tourisme 7XB    end = date(2012, 12, 31),
#                     #Travaux engagés à compter du 1.1.2012 :
#                         #Dans un village résidentiel de tourisme 7XX    end = date(2012, 12, 31),
#                         #Dans une résidence de tourisme classée ou un meublé tourisme 7XZ    end = date(2012, 12, 31),
#             #investissement locatif dans une résidence hôtelière à vocation sociale
#                 #report des dépenses d'investissement de 2010:7XR
#         #reprises de réductions d'impôt, autres imputations, conventions internationales, divers:
#             #crédit d'impôt compétitivité, emploi: montant non encore cédé:
#                 #entreprises bénéficiant de la restitution immédiate:8TL    start = date(2013, 1, 1),
#                 #autres entreprises:8UW    start = date(2013, 1, 1),
#             #investissement en Corse:
#                 #entreprises bénéficiant de le restitution immédiate:8TS
#             #élus locaux: indemnités de fonction soumises à la retenue à la source:
#                 vous:8BY
#                 conj:8CY
#              #Personnes domiciliées en France percevant des revenus de l'étranger
#                   #Revenus exonérés (y compris salaires et primes des détachés à l'étranger) retenus pour le calcul du taux effectif:8TI
#                   #Revenus d'activité et de remplacement de source étrangère:
#                       #Revenus imposables à la CSG et à la CRDS:
#                           #salaires au taux de 7,5 %:8TR
#                           #revenus non salariaux au taux de 7,5 %: 8TQ
#                           #pensions, indemnités de maladie, etc au taux de 6,6 %: 8TV
#                           #pensions, indemnités de maladie, etc au taux de 6.2 %: 8TW
#                           #pensions, indemnités de maladie, etc au taux de 3,8 %: 8TX
#                   #Revenus étrangers imposables en France, ouvrant droit à un crédit d'impôt égal au montant de l'impôt français:8TK
#              #Personnes non domiciliées en France:
#                   #Revenus de sources française et étrangère à prendre en compte pour le calcul du taux moyen d'imposition:8TM
#                   #Impôt sur plus-values en sursis de paiement en cas de transfert du domicile hors de france: 8TN
#              #Plus-values en report d'imposition non expiré: 8UT
#              #Crédit d'impôt égal aux prélèvements forfaitaires et retenues à la source non libératoires effectués à Mayotte en 2013: 8UV    start = date(2013, 1, 1),
#
# ###AUTRES CHARGES OUVRANT DROIT A REDUCTION D'IMPOT : Investissements outre-mer
# ###Pour la déclaration des revenus de 2013, les cases ont changé de nom, elles sont passées de 7.. à H.. (par ex:7QA à HQA)
#     #Vous optez pour le plafonnement des réductions d'impôt pour investissements outre-mer à 11% du revenu imposable (15% (1) ou 13% (2) pour certains investissements):HQA start = date(2013, 1, 1),
#                                                                                                                                                                         7QA end = date(2012, 12, 31),
#           (1).Investissements dans le logement social ; investissements immobiliers engagés avant le 1.1.2011 ; investissements dans le cadre d'une entreprise agréés avant le 5.12.2010.
#           (2).Investissements dans le logement (article 199 undecies A) engagés avant le 1.1.2012 et investissements dans le cadre d'une entreprise (article 199 undecies B) agréés avant le 28.9.2011.
#
#     #Investissements outre-mer dans le logement social : montant de la reduction d'impôt
#         #Investissements réalisés en 2013
#             #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %
#                 #En 2010: HRA    start = date(2013, 1, 1),
#                 #En 2011: HRB    start = date(2013, 1, 1),
#                 #En 2012: HRC    start = date(2013, 1, 1),
#             #Autres investissements: HRD    start = date(2013, 1, 1),
#         #Report de réductions d'impôt non imputées les années antérieures:
#             #Investissements réalisés en 2009: HKG    start = date(2013, 1, 1),
#             #Investissements réalisés en 2009: 7KG    end = date(2012, 12, 31),
#             #Investissements réalisés en 2010:
#                 #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HKH    start = date(2013, 1, 1),
#                                                                                                                                                                 7KH    end = date(2012, 12, 31),
#                 #Autres investissements: HKI    start = date(2013, 1, 1),
#                                          7KI    end = date(2012, 12, 31),
#             #Investissements réalisés en 2011:
#                 #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #En 2009: HQN    start = date(2013, 1, 1),
#                               7QN    end = date(2012, 12, 31),
#                     #En 2010: HQU    start = date(2013, 1, 1),
#                               7QU    end = date(2012, 12, 31),
#             #Autres investissements: HQK    start = date(2013, 1, 1),
#                                      7QK    end = date(2012, 12, 31),
#             #Investissements réalisés en 2012:
#                 #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #En 2009: HQJ    start = date(2013, 1, 1),
#                               7QJ    end = date(2012, 12, 31),
#                     #En 2010: HQS    start = date(2013, 1, 1),
#                               7QS    end = date(2012, 12, 31),
#                     #En 2011: HQW    start = date(2013, 1, 1),
#                               7QW    end = date(2012, 12, 31),
#                 #Autres investissements: HQX    start = date(2013, 1, 1),
#                                          7QX    end = date(2012, 12, 31),
#     #Investissements outre-mer dans le logement et autres secteurs d'activité : montant de la réduction d'impôt
#         #Investissements réalisés jusqu'au 31/12/2008: HQB    start = date(2013, 1, 1),
#                                                        7QB    end = date(2012, 12, 31),
#         #Investissements réalisés en 2009
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HQC    start = date(2013, 1, 1),
#                                                                                                                                                                7QC    end = date(2012, 12, 31),
#             #Autres investissements: HQL    start = date(2013, 1, 1),
#                                      7QL    end = date(2012, 12, 31),
#         #Investissements réalisés en 2010
#             #Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Avant 2009: HQT    start = date(2013, 1, 1),
#                              7QT    end = date(2012, 12, 31),
#                 #En 2009: HQM    start = date(2013, 1, 1),
#                           7QM    end = date(2012, 12, 31),
#             #Autres investissements: HQD    start = date(2013, 1, 1),
#                                      7QD    end = date(2012, 12, 31),
#         #Investissements réalisés en 2011:
#             #Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #avant 2009: HOA    start = date(2013, 1, 1),
#                              7OA    end = date(2012, 12, 31),
#                 #en 2009: HOB    start = date(2013, 1, 1),
#                           7OB    end = date(2012, 12, 31),
#                 #en 2010: HOC    start = date(2013, 1, 1),
#                           7OC    end = date(2012, 12, 31),
#             #Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #avant 2009: HOH    start = date(2013, 1, 1),
#                              7OH    end = date(2012, 12, 31),
#                 #en 2009: HOI    start = date(2013, 1, 1),
#                           7OI    end = date(2012, 12, 31),
#                 #en 2010: HOJ    start = date(2013, 1, 1),
#                           7OJ    end = date(2012, 12, 31),
#             #Autres investissements: HOK    start = date(2013, 1, 1),
#                                      7OK    end = date(2012, 12, 31),
#         #Investissements réalisés en 2012:
#             #Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #avant 2009: HOL    start = date(2013, 1, 1),
#                              7OL    end = date(2012, 12, 31),
#                 #en 2009: HOM    start = date(2013, 1, 1),
#                           7OM    end = date(2012, 12, 31),
#                 #en 2010: HON    start = date(2013, 1, 1),
#                           7ON    end = date(2012, 12, 31),
#             #Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #avant 2009: HOO    start = date(2013, 1, 1),
#                              7OO    end = date(2012, 12, 31),
#                 #en 2009: HOP    start = date(2013, 1, 1),
#                           7OP    end = date(2012, 12, 31),
#                 #en 2010: HOQ    start = date(2013, 1, 1),
#                           7OQ    end = date(2012, 12, 31),
#                 #en 2011: HOR    start = date(2013, 1, 1),
#                           7OR    end = date(2012, 12, 31),
#             #Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %
#                 #avant 2009: HOS    start = date(2013, 1, 1),
#                              7OS    end = date(2012, 12, 31),
#                 #en 2009: HOT    start = date(2013, 1, 1),
#                           7OT    end = date(2012, 12, 31),
#                 #en 2010: HOU    start = date(2013, 1, 1),
#                           7OU    end = date(2012, 12, 31),
#                 #en 2011: HOV    start = date(2013, 1, 1),
#                           7OV    end = date(2012, 12, 31),
#             #Autres investissements: HOW    start = date(2013, 1, 1),
#                                      7OW    end = date(2012, 12, 31),
#         #Investissements réalisés en 2013:
#             #Investissements immobiliers engagés avant le 1.1.2011: HOD    start = date(2013, 1, 1),
#             #Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #en 2010: HOE    start = date(2013, 1, 1),
#                 #en 2011: HOF    start = date(2013, 1, 1),
#             #Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #en 2010  HOG    start = date(2013, 1, 1),
#                 #en 2011  HOX    start = date(2013, 1, 1),
#                 #en 2012  HOY    start = date(2013, 1, 1),
#             #Autres investissements: HOZ    start = date(2013, 1, 1),
#     #Investissements outre-mer dans le cadre de l'entreprise:
#         #Investissements réalisés en 2012
#             #Investissements agréés avant le 28/9/2011
#                 #Investissements ayant fait l’objet avant 2009 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:7PM    end = date(2012, 12, 31),
#                 #Investissements ayant fait l’objet en 2009 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: 7PN    end = date(2012, 12, 31),
#                         #à hauteur de 60%: 7PO    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise:7PP    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:7PQ    end = date(2012, 12, 31),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2012:7PR    end = date(2012, 12, 31),
#                 #Investissements ayant fait l’objet en 2010 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: 7PS    end = date(2012, 12, 31),
#                         #à hauteur de 60%: 7PT    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise:7PU    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:7PV    end = date(2012, 12, 31),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2012:7PW    end = date(2012, 12, 31),
#                 #Investissements ayant fait l’objet en 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52.63%: 7PX    end = date(2012, 12, 31),
#                         #à hauteur de 62.5%: 7PY    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise:7RG    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:7RH    end = date(2012, 12, 31),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2012:7RI    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %: 7RJ    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 %: 7RK    end = date(2012, 12, 31),
#                         #à hauteur de 62,5 %: 7RL     end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: 7RM    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise avec exploitation directe :
#                         #montant de la réduction d'impôt calculée: 7RN    end = date(2012, 12, 31),
#                         #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7RO    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 %: 7RP    end = date(2012, 12, 31),
#                         #à hauteur de 62,5 %: 7RQ    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: 7RR    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise avec exploitation directe :
#                         #montant de la réduction d'impôt calculée: 7RS    end = date(2012, 12, 31),
#                         #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7RT    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 % 7RU    end = date(2012, 12, 31),
#                         #à hauteur de 62,5 % 7RV    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: 7RW    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise avec exploitation directe :
#                         #montant de la réduction d'impôt calculée: 7RX    end = date(2012, 12, 31),
#                         #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7RY    end = date(2012, 12, 31),
#                     #Investissements autres que ceux des lignes précédentes
#                         #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                             #à hauteur de 52,63 %: 7NU    end = date(2012, 12, 31),
#                             #à hauteur de 62,5 %: 7NV    end = date(2012, 12, 31),
#                         #investissements dans votre entreprise: 7NW    end = date(2012, 12, 31),
#                         #investissements dans votre entreprise avec exploitation directe :
#                             #montant de la réduction d'impôt calculée: 7NX    end = date(2012, 12, 31),
#                             #montant de la réduction d'impôt dont vous demandez l'imputation en 2012: 7NY    end = date(2012, 12, 31),
#         #Investissements réalisés en 2013
#             #Investissements agréés du 5.12.2010 au 27.9.2011, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #en 2010 à hauteur de 52,63%: HSA    start = date(2013, 1, 1),
#                     #en 2010 à hauteur de 62,5%: HSB    start = date(2013, 1, 1),
#                     #en 2011 à hauteur de 52,63%: HSF    start = date(2013, 1, 1),
#                     #en 2011 à hauteur de 62,5%: HSG    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise:
#                     #en 2010: HSC    start = date(2013, 1, 1),
#                     #en 2011: HSH    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise avec exploitation directe:
#                     #montant de la réduction d’impôt calculée:
#                         #en 2010: HSD    start = date(2013, 1, 1),
#                         #en 2011: HSI    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2013:
#                         #en 2010: HSE    start = date(2013, 1, 1),
#                         #en 2011: HSJ    start = date(2013, 1, 1),
#         #Autres investissements:
#             #Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt:
#                 #en 2010 à hauteur de 52,63%: HSK    start = date(2013, 1, 1),
#                 #en 2010 à hauteur de 62,5%: HSL    start = date(2013, 1, 1),
#                 #en 2011 à hauteur de 52,63%: HSP    start = date(2013, 1, 1),
#                 #en 2011 à hauteur de 62,5%: HSQ    start = date(2013, 1, 1),
#             #Investissements dans votre entreprise:
#                 #en 2010: HSM    start = date(2013, 1, 1),
#                 #en 2011: HSR    start = date(2013, 1, 1),
#             #Investissements dans votre entreprise avec exploitation directe:
#                 #montant de la réduction d’impôt calculée:
#                     #en 2010: HSN    start = date(2013, 1, 1),
#                     #en 2011: HSS    start = date(2013, 1, 1),
#                 #montant de la réduction d’impôt dont vous demandez l’imputation en 2013:
#                 #en 2010: HSO    start = date(2013, 1, 1),
#                 #en 2011: HST    start = date(2013, 1, 1),
#             #Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt:
#                     #à hauteur de 52,63%: HSU    start = date(2013, 1, 1),
#                     #à hauteur de 62,5%: HSV    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise: HSW    start = date(2013, 1, 1),
#                 #Investissements dans votre entreprise avec exploitation directe :
#                     #montant de la réduction d’impôt calculé: HSX    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2013: HSY    start = date(2013, 1, 1),
#         #Investissements autres que ceux des lignes précédentes
#             #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt:
#                 #à hauteur de 52,63%: HSZ    start = date(2013, 1, 1),
#                 #à hauteur de 62,5%: HTA    start = date(2013, 1, 1),
#             #Investissements dans votre entreprise:
#                 #Investissements dans votre entreprise avec exploitation directe : HTB    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt calculé: HTC    start = date(2013, 1, 1),
#                     #montant de la réduction d’impôt dont vous demandez l’imputation en 2013: HTD    start = date(2013, 1, 1),
#     #REPORT DE RÉDUCTIONS D'IMPÔT NON IMPUTÉES LES ANNEES ANTÉRIEURES
#         #Investissements réalisés en 2008: HQZ    start = date(2013, 1, 1),
#         #Investissements réalisés en 2009:
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HMM    start = date(2013, 1, 1),
#                                                                                                                                                                7MM    end = date(2012, 12, 31),
#             #Autres investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                 #à hauteur de 50%: HLG    start = date(2013, 1, 1),
#                                    7LG    end = date(2012, 12, 31),
#                 #à hauteur de 60%  HMA    start = date(2013, 1, 1),
#                                    7MA    end = date(2012, 12, 31),
#             #Autres investissements dans votre entreprise: HKS    start = date(2013, 1, 1),
#                                                            7KS    end = date(2012, 12, 31),
#         #Investissements réalisés en 2010:
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HMN    start = date(2013, 1, 1),
#                                                                                                                                                                7MN    end = date(2012, 12, 31),
#             #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 50%: HLH    start = date(2013, 1, 1),
#                                        7LH    end = date(2012, 12, 31),
#                     #à hauteur de 60%: HMB    start = date(2013, 1, 1),
#                                        7MB    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise: HKT    start = date(2013, 1, 1),
#                                                         7KT    end = date(2012, 12, 31),
#             #Autres investissements réalisés en 2010:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 50%: HLI    start = date(2013, 1, 1),
#                                        7LI    end = date(2012, 12, 31),
#                     #à hauteur de 60%:  HMC    start = date(2013, 1, 1),
#                                         7MC    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise: HKU    start = date(2013, 1, 1),
#                                                         7KU    end = date(2012, 12, 31),
#         #Investissements réalisés en 2011:
#             #Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010:
#                 #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HQV    start = date(2013, 1, 1),
#                                                                                                                                                                    7QV    end = date(2012, 12, 31),
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: HQO    start = date(2013, 1, 1),
#                                            7QO    end = date(2012, 12, 31),
#                         #à hauteur de 60%: HQP    start = date(2013, 1, 1),
#                                            7QP    end = date(2012, 12, 31),
#                     #investissements dans votre entreprise: HQR    start = date(2013, 1, 1),
#                                                             7QR    end = date(2012, 12, 31),
#                 #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50%: HQF    start = date(2013, 1, 1),
#                                            7QF    end = date(2012, 12, 31),
#                         #à hauteur de 60%: HQG    start = date(2013, 1, 1),
#                                            7QG    end = date(2012, 12, 31),
#                     #Investissements dans votre entreprise: HQI    start = date(2013, 1, 1),
#                                                             7QI    end = date(2012, 12, 31),
#         #Autres investissements:
#             #Investissements ayant fait l'objet avant 1.1.2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HQE    start = date(2013, 1, 1),
#                                                                                                                                                                    7QE    end = date(2012, 12, 31),
#             #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63%: HPA    start = date(2013, 1, 1),
#                                           7PA    end = date(2012, 12, 31),
#                     #à hauteur de 62,5%: HPB    start = date(2013, 1, 1),
#                                          7PB    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise HPD    start = date(2013, 1, 1),
#                                                        7PD    end = date(2012, 12, 31),
#             #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63%: HPE    start = date(2013, 1, 1),
#                                           7PE    end = date(2012, 12, 31),
#                     #à hauteur de 62,5%: HPF    start = date(2013, 1, 1),
#                                          7PF    end = date(2012, 12, 31),
#                 #Investissements dans votre entreprise: HPH    start = date(2013, 1, 1),
#                                                         7PH    end = date(2012, 12, 31),
#             #Investissements autres que ceux des lignes précédentes:
#                 #Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63%: HPI    start = date(2013, 1, 1),
#                                           7PI    end = date(2012, 12, 31),
#                     #à hauteur de 62,5%: HPJ    start = date(2013, 1, 1),
#                                          7PJ    end = date(2012, 12, 31),
#             #Investissements dans votre entreprise: HPL    start = date(2013, 1, 1),
#                                                     7PL    end = date(2012, 12, 31),
#         #Investissements réalisés en 2012:
#             #Investissements agréés avant le 28.9.2011:
#                 #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%: HPM    start = date(2013, 1, 1),
#                 #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50 %: HPN    start = date(2013, 1, 1),
#                         #à hauteur de 60 %: HPO    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise: HPP    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HPR    start = date(2013, 1, 1),
#                 #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 50 %: HPS    start = date(2013, 1, 1),
#                         #à hauteur de 60 %: HPT    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise: HPU    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HPW    start = date(2013, 1, 1),
#                 #Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%:
#                     #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                         #à hauteur de 52,63 %: HPX    start = date(2013, 1, 1),
#                         #à hauteur de 62,5 %: HPY    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise: HRG    start = date(2013, 1, 1),
#                     #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRI    start = date(2013, 1, 1),
#         #Autres investissements:
#             #Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %: HRJ    start = date(2013, 1, 1),
#             #Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63 %: HRK    start = date(2013, 1, 1),
#                     #à hauteur de 62,5 %: HRL    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise: HRM    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRO    start = date(2013, 1, 1),
#             #Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#                 #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                     #à hauteur de 52,63 %: HRP    start = date(2013, 1, 1),
#                     #à hauteur de 62,5 %: HRQ    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise: HRR    start = date(2013, 1, 1),
#                 #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRT    start = date(2013, 1, 1),
#         #Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %:
#             #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                 #à hauteur de 52,63 %: HRU    start = date(2013, 1, 1),
#                 #à hauteur de 62,5 %: HRV    start = date(2013, 1, 1),
#             #investissements dans votre entreprise: HRW    start = date(2013, 1, 1),
#             #investissements dans votre entreprise avec exploitation directe : montant de la réduction d'impôt dont vous demandez l'imputation en 2012: HRY    start = date(2013, 1, 1),
#         #Investissements autres que ceux des lignes précédentes:
#             #investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt:
#                #à hauteur de 52,63 %: HNU    start = date(2013, 1, 1),
#                #à hauteur de 62,5 %: HNV    start = date(2013, 1, 1),
#             #investissements dans votre entreprise: HNW    start = date(2013, 1, 1),
#             #investissements dans votre entreprise avec exploitation directe: HNY    start = date(2013, 1, 1),

# pfam only
build_column('inactif', BoolCol(entity = 'fam',
                    label = u"Parent inactif (PAJE-CLCA)"))

build_column('partiel1', BoolCol(entity = 'fam',
                     label = u"Parent actif à moins de 50% (PAJE-CLCA)"))

build_column('partiel2', BoolCol(entity = 'fam',
                     label = u"Parent actif entre 50% et 80% (PAJE-CLCA)"))

build_column('categ_inv', IntCol(label = u"Catégorie de handicap (AEEH)"))

build_column('opt_colca', BoolCol(entity = 'fam',
                      label = u"Opte pour le COLCA"))

build_column('empl_dir', BoolCol(entity = 'fam',
                     label = u"Emploi direct (CLCMG)"))

build_column('ass_mat', BoolCol(entity = 'fam',
                    label = u"Assistante maternelle (CLCMG)"))

build_column('gar_dom', BoolCol(entity = 'fam',
                    label = u"Garde à domicile (CLCMG)"))

# zones apl and calibration
build_column('tu99', EnumCol(label = u"Tranche d'unité urbaine",
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
                 survey_only = True))

build_column('tau99', EnumCol(label = u"tranche d'aire urbaine",
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
                  survey_only = True))

build_column('reg', EnumCol(label = u"Région",
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
                survey_only = True))

build_column('pol99', EnumCol(label = u"Catégorie de la commune au sein du découpage en aires et espaces urbains",
                  entity = 'men',
                  enum = Enum([u"Commune appartenant à un pôle urbain",
                               u"Commune monopolarisée (appartenant à une couronne périurbaine",
                               u"Commune monopolarisée",
                               u"Espace à dominante rurale"]),
                  survey_only = True))

build_column('cstotpragr', EnumCol(label = u"catégorie socio_professionelle agrégée de la personne de référence",
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
                       survey_only = True))

build_column('naf16pr', EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence",
                    entity = 'men',
                    enum = Enum([u"Sans objet",
                                 u"Non renseignée",
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
                    survey_only = True))  # 17 postes + 1 (-1: sans objet, 0: nonrenseigné)

build_column('nafg17npr', EnumCol(label = u"activité économique de l'établissement de l'emploi principal actuel de la personne de référence ",
                  entity = 'men',
                  enum = Enum([u"Sans objet",
                               u"Non renseignée",
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
                survey_only = True))


#    build_column('typmen15', EnumCol(label = u"Type de ménage",
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
#                                    u"Autres ménages, tous inactifs"],start = 1)))

build_column('ageq', EnumCol(label = u"âge quinquennal de la personne de référence",
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
                survey_only = True))


#    build_column('nbinde', EnumCol(label = u"taille du ménage",
#                     entity = 'men',
#                     enum = Enum([u"Une personne",
#                                  u"Deux personnes",
#                                  u"Trois personnes",
#                                  u"Quatre personnes",
#                                  u"Cinq personnes",
#                                  u"Six personnes et plus"], start = 1)))

build_column('ddipl', EnumCol(label = u"diplôme de la personne de référence",
                entity = 'men',
                enum = Enum([u"Non renseigné"
                             u"Diplôme supérieur",
                             u"Baccalauréat + 2 ans",
                             u"Baccalauréat ou brevet professionnel ou autre diplôme de ce niveau",
                             u"CAP, BEP ou autre diplôme de ce niveau",
                             u"Brevet des collèges",
                             u"Aucun diplôme ou CEP"], start = 1),
                survey_only = True))

build_column('act5', EnumCol(label = u"activité",
                 enum = Enum([u"Salarié",
                              u"Indépendant",
                              u"Chômeur",
                              u"Retraité",
                              u"Inactif"], start = 1),
                survey_only = True))  # 5 postes normalement TODO: check = 0

build_column('wprm_init', FloatCol(label = u"Effectifs", survey_only = True))

# # ISF ##

# # Immeubles bâtis ##
build_column('b1ab', IntCol(entity = 'foy', label = u"Valeur de la résidence principale avant abattement", val_type = "monetary"))
build_column('b1ac', IntCol(entity = 'foy', label = u"Valeur des autres immeubles avant abattement", val_type = "monetary"))
# # non bâtis ##
build_column('b1bc', IntCol(entity = 'foy', label = u"Immeubles non bâtis : bois, fôrets et parts de groupements forestiers", val_type = "monetary"))
build_column('b1be', IntCol(entity = 'foy', label = u"Immeubles non bâtis : biens ruraux loués à long termes", val_type = "monetary"))
build_column('b1bh', IntCol(entity = 'foy', label = u"Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers", val_type = "monetary"))
build_column('b1bk', IntCol(entity = 'foy', label = u"Immeubles non bâtis : autres biens", val_type = "monetary"))

# # droits sociaux- valeurs mobilières-liquidités- autres meubles ##
build_column('b1cl', IntCol(entity = 'foy', label = u"Parts et actions détenues par les salariés et mandataires sociaux", val_type = "monetary"))
build_column('b1cb', IntCol(entity = 'foy', label = u"Parts et actions de sociétés avec engagement de conservation de 6 ans minimum", val_type = "monetary"))
build_column('b1cd', IntCol(entity = 'foy', label = u"Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité", val_type = "monetary"))
build_column('b1ce', IntCol(entity = 'foy', label = u"Autres valeurs mobilières", val_type = "monetary"))
build_column('b1cf', IntCol(entity = 'foy', label = u"Liquidités", val_type = "monetary"))
build_column('b1cg', IntCol(entity = 'foy', label = u"Autres biens meubles", val_type = "monetary"))

build_column('b1co', IntCol(entity = 'foy', label = u"Autres biens meubles : contrats d'assurance-vie", val_type = "monetary"))

#    b1ch
#    b1ci
#    b1cj
#    b1ck


# # passifs et autres réduc ##
build_column('b2gh', IntCol(entity = 'foy', label = u"Total du passif et autres déductions", val_type = "monetary"))

# # réductions ##
build_column('b2mt', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary"))
build_column('b2ne', IntCol(entity = 'foy', label = u"Réductions pour investissements directs dans une société", val_type = "monetary"))
build_column('b2mv', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings" , val_type = "monetary"))
build_column('b2nf', IntCol(entity = 'foy', label = u"Réductions pour investissements par sociétés interposées, holdings", val_type = "monetary"))
build_column('b2mx', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FIP", val_type = "monetary"))
build_column('b2na', IntCol(entity = 'foy', label = u"Réductions pour investissements par le biais de FCPI ou FCPR", val_type = "monetary"))
build_column('b2nc', IntCol(entity = 'foy', label = u"Réductions pour dons à certains organismes d'intérêt général", val_type = "monetary"))

# #  montant impôt acquitté hors de France ##
build_column('b4rs', IntCol(entity = 'foy', label = u"Montant de l'impôt acquitté hors de France", val_type = "monetary"))

# # BOUCLIER FISCAL ##

build_column('rev_or', IntCol(entity = 'foy', label = u"", val_type = "monetary"))
build_column('rev_exo', IntCol(entity = 'foy', label = u"", val_type = "monetary"))

build_column('tax_fonc', IntCol(entity = 'foy', label = u"Taxe foncière", val_type = "monetary"))
build_column('restit_imp', IntCol(entity = 'foy', label = u"", val_type = "monetary"))

# to remove
build_column('champm', BoolCol(entity = 'men',
                   default = True,
                   survey_only = True,
                   ))

build_column('wprm', FloatCol(entity = 'men',
                  default = 1,
                  label = u"Effectifs",
                  survey_only = True,
                  ))

build_column('etr', IntCol())
build_column('coloc', BoolCol(label = u"Vie en colocation"))
build_column('csg_rempl', EnumCol(label = u"Taux retenu sur la CSG des revenus de remplacment",
             entity = 'ind',
             enum = Enum([u"Non renseigné/non pertinent",
                          u"Exonéré",
                          u"Taux réduit",
                          u"Taux plein"]),
            default = 3))

build_column('aer', IntCol(label = u"Allocation équivalent retraite (AER)"))  # L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
build_column('ass', IntCol(label = u"Allocation de solidarité spécifique (ASS)"))
build_column('f5sq', IntCol())

build_column('m_afeamam', IntCol(entity = 'men', survey_only = True))
build_column('m_agedm', IntCol(entity = 'men', survey_only = True))
build_column('m_clcam', IntCol(entity = 'men', survey_only = True))
build_column('m_colcam', IntCol(entity = 'men', survey_only = True))
build_column('m_mgamm', IntCol(entity = 'men', survey_only = True))
build_column('m_mgdomm', IntCol(entity = 'men', survey_only = True))
build_column('zthabm', IntCol(entity = 'men'))  # TODO: Devrait être renommée tax_hab

build_column('adoption', BoolCol(entity = "ind", label = u"Enfant adopté"))

# ('tax_hab', IntCol())
