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
                                        "value": 0,
                                        },
                                    "seuil": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    },
                                },
                            "public": {
                                "@type": "Node",
                                "description": "Salariés du secteur privé",
                                "children": {
                                    "taux_1": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_1": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_2": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_2": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_3": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_3": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_4": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_4": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_5": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_5": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_6": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_6": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_7": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_7": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_8": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_8": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_9": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_9": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_10": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_10": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "taux_11": {
                                        "@type": "Parameter",
                                        "description": "Taux",
                                        "format": "rate",
                                        "value": 0,
                                        },
                                    "seuil_11": {
                                        "@type": "Parameter",
                                        "description": "Seuil (en SMIC)",
                                        "format": "rate",
                                        "value": 0,
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
