# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date
import os

from openfisca_core import columns, legislations
from openfisca_core.reforms import Reform

from .. import entities
from ..model.base import *
from ..model.prelevements_obligatoires.impot_revenu import reductions_impot


dir_path = os.path.dirname(__file__)


# TODO: les baisses de charges n'ont pas été codées car annulées (toute ou en partie ?)
# par le Conseil constitutionnel

class plfr2014(Reform):
    name = u'Projet de Loi de Finances Rectificative 2014'

    class reduction_impot_exceptionnelle(Variable):
        definition_period = YEAR

        def formula_2013_01_01(self, simulation, period):
            janvier = period.first_month

            nb_adult = simulation.calculate('nb_adult', period)
            nb_parents = simulation.calculate('nb_parents', period = janvier)
            rfr = simulation.calculate('rfr', period)
            params = simulation.legislation_at(period.start).plfr2014.reduction_impot_exceptionnelle
            plafond = params.seuil * nb_adult + (nb_parents - nb_adult) * 2 * params.majoration_seuil
            montant = params.montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

    class reductions(Variable):
        label = u"Somme des réductions d'impôt à intégrer pour l'année 2013"
        definition_period = YEAR

        def formula_2013_01_01(self, simulation, period):
            accult = simulation.calculate('accult', period)
            adhcga = simulation.calculate('adhcga', period)
            cappme = simulation.calculate('cappme', period)
            creaen = simulation.calculate('creaen', period)
            daepad = simulation.calculate('daepad', period)
            deffor = simulation.calculate('deffor', period)
            dfppce = simulation.calculate('dfppce', period)
            doment = simulation.calculate('doment', period)
            domlog = simulation.calculate('domlog', period)
            donapd = simulation.calculate('donapd', period)
            duflot = simulation.calculate('duflot', period)
            ecpess = simulation.calculate('ecpess', period)
            garext = simulation.calculate('garext', period)
            intagr = simulation.calculate('intagr', period)
            invfor = simulation.calculate('invfor', period)
            invlst = simulation.calculate('invlst', period)
            ip_net = simulation.calculate('ip_net', period)
            locmeu = simulation.calculate('locmeu', period)
            mecena = simulation.calculate('mecena', period)
            mohist = simulation.calculate('mohist', period)
            patnat = simulation.calculate('patnat', period)
            prcomp = simulation.calculate('prcomp', period)
            reduction_impot_exceptionnelle = simulation.calculate('reduction_impot_exceptionnelle', period)
            repsoc = simulation.calculate('repsoc', period)
            resimm = simulation.calculate('resimm', period)
            rsceha = simulation.calculate('rsceha', period)
            saldom = simulation.calculate('saldom', period)
            scelli = simulation.calculate('scelli', period)
            sofica = simulation.calculate('sofica', period)
            spfcpi = simulation.calculate('spfcpi', period)
            total_reductions = accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + \
                donapd + duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist + patnat + \
                prcomp + repsoc + resimm + rsceha + saldom + scelli + sofica + spfcpi + reduction_impot_exceptionnelle
            return min_(ip_net, total_reductions)

    def apply(self):
        for variable in [self.reduction_impot_exceptionnelle, self.reductions]:
            self.update_variable(variable)
        self.modify_legislation_json(modifier_function = modify_legislation_json)


def modify_legislation_json(reference_legislation_json_copy):
    file_path = os.path.join(dir_path, 'plfr2014.yaml')
    plfr2014_legislation_subtree = legislations.load_file(name='plfr2014', file_path=file_path)

    file_path = os.path.join(dir_path, 'plfrss2014.yaml')
    plfrss2014_legislation_subtree = legislations.load_file(name='plfrss2014', file_path=file_path)

    reference_legislation_json_copy.add_child('plfr2014', plfr2014_legislation_subtree)
    reference_legislation_json_copy.add_child('plfrss2014', plfrss2014_legislation_subtree)
    return reference_legislation_json_copy
