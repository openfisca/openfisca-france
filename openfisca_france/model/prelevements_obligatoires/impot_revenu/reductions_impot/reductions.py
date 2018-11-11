# -*- coding: utf-8 -*-

from numpy import (
    minimum,
    sum as sum_,
    )

from openfisca_france.model.base import (
    FoyerFiscal,
    Variable,
    YEAR,
    )


class reductions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Réductions d'impôt sur le revenu"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Renvoie la somme des réductions d'impôt à intégrer pour l'année 2002
        '''
        impot_net = foyer_fiscal('ip_net', period)

        reductions = (
            # Depuis 2002
            'accult', 'adhcga', 'assvie', 'cappme', 'cotsyn',
            'daepad', 'dfppce', 'doment', 'domlog', 'donapd',
            'ecpess', 'garext', 'intemp', 'invfor', 'invrev',
            'prcomp', 'rsceha', 'saldom', 'spfcpi',
            # Introduites en 2003
            'mecena', 'repsoc',
            # Introduites en 2004
            'intcon', 'invlst',
            # Introduites en 2005
            'intagr',
            # Introduites en 2006
            'creaen', 'deffor', 'sofica',
            # Introduites en 2008
            'mohist',
            # Introduites en 2009
            'domsoc', 'ecodev', 'locmeu', 'resimm', 'scelli',
            'sofipe',
            # Introduites en 2010
            'patnat',
            # Introduites en 2013
            'duflot',
            'reduction_impot_exceptionnelle',
            # Introduites en 2014
            'rpinel',
            # Introduites en 2017
            'rehab',
            )

        montant = sum_(foyer_fiscal(reduction, period) for reduction in reductions)

        return minimum(impot_net, montant)
