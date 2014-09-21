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



from openfisca_core.reforms import Reform
import openfisca_france


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test_parametric_reform(year = 2015):
    reform_parameters = {
        "@context": "http://openfisca.fr/contexts/dated-legislation.jsonld",
        "@type": "Node",
        "children": {
            "plfr2104": {
                "@type": "Node",
                "description": "Projet de loi de finance 2014",
                "children": {
                    "reduction_impot_exceptionnelle": {
                        "@type": "Node",
                        "description": "Réduction d'impôt exceptionnelle",
                        "children": {
                            "montant_plafond": {
                                "@type": "Parameter",
                                "description": "Montant plafond par part pour les deux premières parts",
                                "format": "integer",
                                "unit": "currency",
                                "value": 350,
                                },
                            "seuil": {
                                "@type": "Parameter",
                                "description": "Seuil (à partir duquel la réduction décroît) par part pour les deux premières parts",
                                "format": "integer",
                                "unit": "currency",
                                "value": 13795,
                            },
                            "majoration_seuil": {
                                "@type": "Parameter",
                                "description": "Majoration du seuil par demi-part supplémentaire",
                                "format": "integer",
                                "unit": "currency",
                                "value": 3536,
                                },
                            },
                        },
                    },
                },
            "plfrss2014": {
                "@type": "Node",
                "description": "Projet de loi de financement de la sécurité sociale rectificative 2014",
                "children": {
                    "exonerations_bas_salaires": {
                        "@type": "Node",
                        "description": "Exonérations de cotiastions salariées sur les bas salaires",
                        "children": {
                            "prive": {
                                "@type": "Node",
                                "description": "Salariés du secteur privé",
                                "children": {
                                    "taux": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.03,
                                        },
                                    "seuil": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 1.3 ,
                                        },
                                    },
                                },
                            "public": {
                                "@type": "Node",
                                "description": "Salariés du secteur public",
                                "children": {
                                    "taux_1": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.02,
                                        },
                                    "seuil_1": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 312,
                                        },
                                    "taux_2": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.018,
                                        },
                                    "seuil_2": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 328,
                                        },
                                    "taux_3": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.016,
                                        },
                                    "seuil_3": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 343,
                                        },
                                    "taux_4": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.014,
                                        },
                                    "seuil_4": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 359,
                                        },
                                    "taux_5": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.012,
                                        },
                                    "seuil_5": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 375,
                                        },
                                    "taux_6": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.01,
                                        },
                                    "seuil_6": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 390,
                                        },
                                    "taux_7": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.008,
                                        },
                                    "seuil_7": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 406,
                                        },
                                    "taux_8": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.007,
                                        },
                                    "seuil_8": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 421,
                                        },
                                    "taux_9": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.006,
                                        },
                                    "seuil_9": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 437,
                                        },
                                    "taux_10": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.005,
                                        },
                                    "seuil_10": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 453,
                                        },
                                    "taux_11": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0.002,
                                        },
                                    "seuil_11": {
                                        "@type": "Parameter",
                                        "description": "Indice majoré plafond",
                                        "format": "integer",
                                        "value": 468,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_parametric_reform(2014)
