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


from ...base import *  # noqa



build_column('sali', IntCol(label = u"Revenus d'activité imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AJ",
                               QUIFOY['conj']: u"1BJ",
                               QUIFOY['pac1']: u"1CJ",
                               QUIFOY['pac2']: u"1DJ",
                               QUIFOY['pac3']: u"1EJ",
                               }))  # (f1aj, f1bj, f1cj, f1dj, f1ej)

build_column('fra', IntCol(label = u"Frais réels",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AK",
                              QUIFOY['conj']: u"1BK",
                              QUIFOY['pac1']: u"1CK",
                              QUIFOY['pac2']: u"1DK",
                              QUIFOY['pac3']: u"1EK",
                              }))  # (f1ak, f1bk, f1ck, f1dk, f1ek)


build_column('hsup', IntCol(label = u"Heures supplémentaires : revenus exonérés connus",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = {QUIFOY['vous']: u"1AU",
                               QUIFOY['conj']: u"1BU",
                               QUIFOY['pac1']: u"1CU",
                               QUIFOY['pac2']: u"1DU",
                               }))  # (f1au, f1bu, f1cu, f1du, f1eu)

build_column('ppe_du_sa', IntCol(label = u"Prime pour l'emploi des salariés: nombre d'heures payées dans l'année",
                     cerfa_field = {QUIFOY['vous']: u"1AV",
                                    QUIFOY['conj']: u"1BV",
                                    QUIFOY['pac1']: u"1CV",
                                    QUIFOY['pac2']: u"1DV",
                                    QUIFOY['pac3']: u"1QV",
                                    }))  # (f1av, f1bv, f1cv, f1dv, f1qv)

build_column('ppe_tp_sa', BoolCol(label = u"Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière",
                      cerfa_field = {QUIFOY['vous']: u"1AX",
                                     QUIFOY['conj']: u"1BX",
                                     QUIFOY['pac1']: u"1CX",
                                     QUIFOY['pac2']: u"1DX",
                                     QUIFOY['pac3']: u"1QX",
                                     }))  # (f1ax, f1bx, f1cx, f1dx, f1qx)


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

#    build_column('code_risque', EnumCol(label = u"Code risque pour les accidents du travail"))  # TODO: Complete label, add enum and relevant default.

build_column(
    'exposition_accident',
    EnumCol(
        label = u"Exposition au risque pour les accidents du travail",
        enum = Enum([
            u"Faible",
            u"Moyen",
            u"Élevé",
            u"Très élevé",
            ])
        )
    )

