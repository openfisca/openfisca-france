# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013 OpenFisca Team
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


from __future__ import division

from datetime import datetime
import itertools
import pickle

import numpy as np
from openfisca_core import __version__ as VERSION
from openfisca_core import model

from . import conv, ENTITIES_INDEX
from .model.data import InputDescription, QUIFAM, QUIFOY, QUIMEN


class Scenario(object):
    def __init__(self):
        super(Scenario, self).__init__()

        self.indiv = {}
        # indiv est un dict de dict. La clé est le noi de l'individu
        # Exemple :
        # 0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0,
        #     'birth': datetime.date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0}
        self.declar = {}
        # declar est un dict de dict. La clé est le noidec.
        self.famille = {}

        # menage est un dict de dict la clé est la pref
        self.menage = {0:{'loyer':500,'so':4, 'code_postal':69001, 'zone_apl':2, 'zthabm' :0}}

        # on ajoute un individu, déclarant et chef de famille
        self.addIndiv(0, datetime(1975,1,1).date(), 'vous', 'chef')

        self.nmen = None
        self.x_axis = None
        self.maxrev = None
        self.same_rev_couple = None
        self.year = None

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    def check_consistency(self):
        '''
        Vérifie que le ménage entré est valide
        '''
        for noi, vals in self.indiv.iteritems():
            age = self.year - vals['birth'].year
            if age < 0:
                return u"L'année de naissance doit être antérieure à celle de la simulation (voir Fichier->Paramètres pour régler la date de la simulation"
            if vals['quifoy'] in ('vous', 'conj'):
                if age < 18: return u'Le déclarant et son éventuel conjoint doivent avoir plus de 18 ans'
            else:
                if age > 25 and (vals['inv']==0): return u'Les personnes à charges doivent avoir moins de 25 ans si elles ne sont pas invalides'
            if vals['quifoy'] == 'conj' and not vals['quifam'] == 'part':
                return u"Un conjoint sur la déclaration d'impôt doit être le partenaire dans la famille"
        return ''

    @classmethod
    def json_to_attributes(cls, value, state = None):
        if value is None:
            return value, None
        if state is None:
            state = conv.default_state

        # First validation and conversion step
        attributes, error = conv.pipe(
            conv.test_isinstance(dict),
            conv.struct(
                dict(
                    declar = conv.pipe(
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance(basestring),
                                conv.input_to_int,
                                conv.test_greater_or_equal(0),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(
                                        (column.name, column.json_to_python)
                                        for column in InputDescription.columns
                                        if column.entity == 'foy'
                                        ),
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    famille = conv.pipe(
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance(basestring),
                                conv.input_to_int,
                                conv.test_greater_or_equal(0),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(
                                        (column.name, column.json_to_python)
                                        for column in InputDescription.columns
                                        if column.entity == 'fam'
                                        ),
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    indiv = conv.pipe(
                        conv.test_isinstance(list),
                        conv.uniform_sequence(
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            birth = conv.pipe(
                                                conv.test_isinstance(basestring),
                                                conv.iso8601_input_to_date,
                                                conv.not_none,
                                                ),
                                            noichef = conv.pipe(  # index de la famille (= index du chef de famille)
                                                conv.json_to_natural_int,
                                                conv.not_none,
                                                ),
                                            noidec = conv.pipe(  # index du foyer fiscal (= index du déclarant)
                                                conv.json_to_natural_int,
                                                conv.not_none,
                                                ),
                                            noipref = conv.pipe(  # index du ménage (index du premier individu)
                                                conv.json_to_natural_int,
                                                conv.not_none,
                                                ),
                                            quifam = conv.pipe(
                                                conv.test_isinstance(basestring),
                                                conv.test_in(QUIFAM._nums),
                                                conv.not_none,
                                                ),
                                            quifoy = conv.pipe(
                                                conv.test_isinstance(basestring),
                                                conv.test_in(QUIFOY._nums),
                                                conv.not_none,
                                                ),
                                            quimen = conv.pipe(
                                                conv.test_isinstance(basestring),
                                                conv.test_in(QUIMEN._nums),
                                                conv.not_none,
                                                ),
                                            ).iteritems(),
                                        (
                                            (column.name, column.json_to_python)
                                            for column in InputDescription.columns
                                            if column.entity == 'ind' and column.name not in ('age', 'agem', 'quifam',
                                                'quifoy', 'quimen')
                                            ),
                                        )),
                                    ),
                                ),
                            drop_none_items = True,
                            ),
                        conv.empty_to_none,
                        conv.function(lambda values: dict(enumerate(values))),
                        conv.not_none,
                        ),
                    menage = conv.pipe(
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance(basestring),
                                conv.input_to_int,
                                conv.test_greater_or_equal(0),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(
                                        (column.name, column.json_to_python)
                                        for column in InputDescription.columns
                                        if column.entity == 'men'
                                        ),
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    year = conv.pipe(
                        conv.test_isinstance(int),
                        conv.test_greater_or_equal(1900),  # TODO: Check that year is valid in params.
                        conv.not_none,
                        ),
                    ),
                ),
            )(value, state = state)
        if error is not None:
            return attributes, error

        # Second validation step
        indiv_indexes = sorted(attributes['indiv'].iterkeys())
        return conv.struct(
            dict(
                declar = conv.uniform_mapping(
                    conv.test_in(indiv_indexes),
                    conv.noop,
                    ),
                famille = conv.uniform_mapping(
                    conv.test_in(indiv_indexes),
                    conv.noop,
                    ),
                indiv = conv.uniform_mapping(
                    conv.noop,
                    conv.struct(
                        dict(
                            noichef = conv.test_in(indiv_indexes),  # index de la famille (= index du chef de famille)
                            noidec = conv.test_in(indiv_indexes),  # index du foyer fiscal (= index du déclarant)
                            noipref = conv.test_in(indiv_indexes),  # index du ménage (index du premier individu)
                            ),
                        default = conv.noop,
                        ),
                    ),
                menage = conv.uniform_mapping(
                    conv.test_in(indiv_indexes),
                    conv.noop,
                    ),
                ),
                default = conv.noop,
            )(attributes, state = state)

    def modify(self, noi, newQuifoy = None, newFoyer = None):
        oldFoyer, oldQuifoy = self.indiv[noi]['noidec'], self.indiv[noi]['quifoy']
        if newQuifoy == None: newQuifoy = oldQuifoy
        if newFoyer == None: newFoyer = oldFoyer
        if oldQuifoy == 'vous':
            toAssign = self.getIndiv(oldFoyer, 'noidec')
            del self.declar[oldFoyer]
            self._assignPerson(noi, quifoy = newQuifoy, foyer = newFoyer)
            for person in toAssign:
                oldPos = self.indiv[person]['quifoy']
                if oldPos == "vous": continue
                else: self.modify(person, newQuifoy = oldPos, newFoyer = 0)
        else:
            self._assignPerson(noi, quifoy = newQuifoy, foyer = newFoyer)
        self.genNbEnf()

    def modifyFam(self, noi, newQuifam = None, newFamille = None):
        oldFamille, oldQuifam = self.indiv[noi]['noichef'], self.indiv[noi]['quifam']
        if newQuifam == None: newQuifam = oldQuifam
        if newFamille == None: newFamille = oldFamille
        if oldQuifam == 'chef':
            toAssign = self.getIndiv(oldFamille, 'noichef')
            del self.famille[oldFamille]
            self._assignPerson(noi, quifam = newQuifam, famille = newFamille)
            for person in toAssign:
                oldQui = self.indiv[person]['quifam']
                if oldQui == "chef": continue
                else: self.modifyFam(person, newQuifam = oldQui, newFamille = 0)
        else:
            self._assignPerson(noi, quifam = newQuifam, famille = newFamille)
        self.genNbEnf()

    def hasConj(self, noidec):
        '''
        Renvoie True s'il y a un conjoint dans la déclaration 'noidec', sinon False
        '''
        for vals in self.indiv.itervalues():
            if (vals['noidec'] == noidec) and (vals['quifoy']=='conj'):
                return True
        return False

    def hasPart(self, noichef):
        '''
        Renvoie True s'il y a un conjoint dans la déclaration 'noidec', sinon False
        '''
        for vals in self.indiv.itervalues():
            if (vals['noichef'] == noichef) and (vals['quifam']=='part'):
                return True
        return False

    def _assignVous(self, noi):
        '''
        Ajoute la personne numéro 'noi' et crée son foyer
        '''
        self.indiv[noi]['quifoy'] = 'vous'
        self.indiv[noi]['noidec'] = noi
        self.declar.update({noi:{}})

    def _assignConj(self, noi, noidec):
        '''
        Ajoute la personne numéro 'noi' à la déclaration numéro 'noidec' en tant
        que 'conj' si declar n'a pas de conj. Sinon, cherche le premier foyer sans
        conjoint. Sinon, crée un nouveau foyer en tant que vous.
        '''
        decnum = noidec
        if (noidec not in self.declar) or self.hasConj(noidec):
            for k in self.declar:
                if not self.hasConj(k):
                    decnum = k
        if not self.hasConj(decnum):
            self.indiv[noi]['quifoy'] = 'conj'
            self.indiv[noi]['noidec'] = decnum
        else:
            self._assignVous(noi)

    def _assignPac(self, noi, noidec):
        '''
        Ajoute la personne numéro 'noi' et crée sa famille
        '''
        self.indiv[noi]['quifoy'] = 'pac0'
        self.indiv[noi]['noidec'] = noidec

    def _assignChef(self, noi):
        '''
        Désigne la personne numéro 'noi' comme chef de famille et crée une famille vide
        '''
        self.indiv[noi]['quifam'] = 'chef'
        self.indiv[noi]['noichef'] = noi
        self.famille.update({noi:{}})

    def _assignPart(self, noi, noichef):
        '''
        Ajoute la personne numéro 'noi' à la famille 'noichef' en tant
        que 'part' si noi n'a pas de part. Sinon, cherche la première famille sans
        'part'. Sinon, crée un nouvelle famille en tant que vous.
        '''
        famnum = noichef
        if (noichef not in self.famille) or self.hasPart(noichef):
            for k in self.famille:
                if not self.hasPart(k):
                    famnum = k
        if not self.hasPart(famnum):
            self.indiv[noi]['quifam'] = 'part'
            self.indiv[noi]['noichef'] = famnum
        else:
            self._assignChef(noi)

    def _assignEnfF(self, noi, noichef):
        '''
        Ajoute la personne numéro 'noi' à la déclaration famille 'noifam' en tant
        que 'enf'
        '''
        self.indiv[noi]['quifam'] = 'enf0'
        self.indiv[noi]['noichef'] = noichef

    def _assignPerson(self, noi, quifoy = None, foyer = None, quifam = None, famille = None):
        if quifoy is not None:
            if   quifoy     == 'vous': self._assignVous(noi)
            elif quifoy     == 'conj': self._assignConj(noi, foyer)
            elif quifoy[:3] == 'pac' : self._assignPac(noi, foyer)
        if quifam is not None:
            if   quifam     == 'chef': self._assignChef(noi)
            elif quifam     == 'part': self._assignPart(noi, famille)
            elif quifam[:3] == 'enf' : self._assignEnfF(noi, famille)
        self.genNbEnf()

    def rmvIndiv(self, noi):
        oldFoyer, oldQuifoy = self.indiv[noi]['noidec'], self.indiv[noi]['quifoy']
        oldFamille, oldQuifam = self.indiv[noi]['noichef'], self.indiv[noi]['quifam']
        if oldQuifoy == 'vous':
            toAssign = self.getIndiv(oldFoyer, 'noidec')
            for person in toAssign:
                if self.indiv[person]['quifoy']     == 'conj': self._assignPerson(person, quifoy = 'conj', foyer = 0)
                if self.indiv[person]['quifoy'][:3] == 'pac' : self._assignPerson(person, quifoy = 'pac' , foyer = 0)
            del self.declar[noi]
        if oldQuifam == 'chef':
            toAssign = self.getIndiv(oldFamille, 'noichef')
            for person in toAssign:
                if self.indiv[person]['quifam']     == 'part': self._assignPerson(person, quifam = 'part', famille = 0)
                if self.indiv[person]['quifam'][:3] == 'enf' : self._assignPerson(person, quifam = 'enf' , famille = 0)
            del self.famille[noi]
        del self.indiv[noi]
        self.genNbEnf()

    def getIndiv(self, noi, champ = 'noidec'):
        for person, vals in self.indiv.iteritems():
            if vals[champ] == noi:
                yield person

    def addIndiv(self, noi, birth, quifoy, quifam):
        self.indiv.update({noi:{'birth':birth,
                                'inv': 0,
                                'alt':0,
                                'activite':0,
                                'quifoy': 'none',
                                'quifam': 'none',
                                'noidec':  0,
                                'noichef': 0,
                                'noipref': 0}})

        self._assignPerson(noi, quifoy = quifoy, foyer = 0, quifam = quifam, famille = 0)
        self.updateMen()

    def nbIndiv(self):
        return len(self.indiv)

    def genNbEnf(self):
        for noi, vals in self.indiv.iteritems():
            if vals.has_key('statmarit'):
                statmarit = vals['statmarit']
            else: statmarit = 2
            if self.hasConj(noi) and (noi == vals['noidec']) and not statmarit in (1,5):
                statmarit = 1
            elif not self.hasConj(noi) and (noi == vals['noidec']) and not statmarit in (2,3,4):
                statmarit = 2
            # si c'est un conjoint, même statmarit que 'vous'
            if vals['quifoy'] == 'conj':
                statmarit = self.indiv[vals['noidec']]['statmarit']
            vals.update({'statmarit':statmarit})

        for noidec, vals in self.declar.iteritems():
            vals.update(self.NbEnfFoy(noidec))
        for noichef, vals in self.famille.iteritems():
            self.NbEnfFam(noichef)

    def NbEnfFoy(self, noidec):
        out = {'nbF': 0, 'nbG':0, 'nbH':0, 'nbI':0, 'nbR':0, 'nbJ':0, 'nbN':0}
        n = 0
        for vals in self.indiv.itervalues():
            if (vals['noidec']==noidec) and (vals['quifoy'][:3]=='pac'):
                n += 1
                if (self.year - vals['birth'].year >= 18) and vals['inv'] == 0:
                    out['nbJ'] += 1
                else:
                    if vals['alt'] == 0:
                        out['nbF'] += 1
                        if vals['inv'] == 1 : out['nbG'] +=1
                    elif vals['alt'] == 1:
                        out['nbH'] += 1
                        if vals['inv'] == 1: out['nbI'] += 1
                vals['quifoy'] = 'pac%d' % n
        return out

    def NbEnfFam(self, noichef):
        n = 0
        for vals in self.indiv.itervalues():
            if (vals['noichef']==noichef) and (vals['quifam'][:3]=='enf'):
                n += 1
                vals['quifam'] = 'enf%d' % n

    def updateMen(self):
        '''
        Il faut virer cela
        '''
        people = self.indiv
        for noi in xrange(self.nbIndiv()):
            if   noi == 0: quimen = 'pref'
            elif noi == 1: quimen = 'cref'
            else:  quimen = 'enf%d' % (noi-1)
            if 'quimen' not in people[noi].keys():
                people[noi].update({'quimen': quimen,
                                    'noipref': 0})
            else:
                people[noi].update({'noipref': 0})

    def __repr__(self):
        outstr = "INDIV" + '\n'
        for key, val in self.indiv.iteritems():
            outstr += str(key) + str(val) + '\n'
        outstr += "DECLAR" + '\n'
        for key, val in self.declar.iteritems():
            outstr += str(key) + str(val) + '\n'
        outstr += "FAMILLE" + '\n'
        for key, val in self.famille.iteritems():
            outstr += str(key) + str(val) + '\n'
        outstr += "MENAGE" + '\n'
        for key, val in self.menage.iteritems():
            outstr += str(key) + str(val) + '\n'
        return outstr

    def saveFile(self, fileName):
        outputFile = open(fileName, 'wb')
        pickle.dump({'version': VERSION, 'indiv': self.indiv, 'declar': self.declar, 'famille': self.famille, 'menage': self.menage}, outputFile)
        outputFile.close()

    def openFile(self, fileName):
        inputFile = open(fileName, 'rb')
        S = pickle.load(inputFile)
        inputFile.close()
        self.indiv = S['indiv']
        self.declar = S['declar']
        self.menage = S['menage']

    def populate_datatable(self, datatable):
        '''
        Popualte a datatable from a given scenario
        '''
        from pandas import DataFrame, concat
        import numpy as np
        scenario = self

        if self.nmen is None:
            raise Exception('france.Scenario: self.nmen should be not None')

        nmen = self.nmen
        same_rev_couple = self.same_rev_couple
        datatable.NMEN = nmen
        datatable._nrows = datatable.NMEN*len(scenario.indiv)
        datesim = datatable.datesim
        datatable.table = DataFrame()

        idmen = np.arange(60001, 60001 + nmen)

        for noi, dct in scenario.indiv.iteritems():
            birth = dct['birth']
            age = datesim.year- birth.year
            agem = 12*(datesim.year- birth.year) + datesim.month - birth.month
            noidec = dct['noidec']
            quifoy = datatable.description.get_col('quifoy').enum[dct['quifoy']]
            quifam = datatable.description.get_col('quifam').enum[dct['quifam']]
            noichef = dct['noichef']
            quimen = datatable.description.get_col('quimen').enum[dct['quimen']]

            dct = {'noi': noi*np.ones(nmen),
                   'age': age*np.ones(nmen),
                   'agem': agem*np.ones(nmen),
                   'quimen': quimen*np.ones(nmen),
                   'quifoy': quifoy*np.ones(nmen),
                   'quifam': quifam*np.ones(nmen),
                   'idmen': idmen,
                   'idfoy': idmen*100 + noidec,
                   'idfam': idmen*100 + noichef}

            datatable.table = concat([datatable.table, DataFrame(dct)], ignore_index = True)

        datatable.gen_index(ENTITIES_INDEX)

        for name in datatable.col_names:
            if not name in datatable.table:
                datatable.table[name] = datatable.description.get_col(name)._default

        entity = 'men'
        nb = datatable.index[entity]['nb']
        for noi, dct in scenario.indiv.iteritems():
            for var, val in dct.iteritems():
                if var in ('birth', 'noipref', 'noidec', 'noichef', 'quifoy', 'quimen', 'quifam'):
                    continue
                if not datatable.index[entity][noi] is None:
                    datatable.set_value(var, np.ones(nb)*val, entity, noi)
            del var, val

        entity = 'foy'
        nb = datatable.index[entity]['nb']
        for noi, dct in scenario.declar.iteritems():
            for var, val in dct.iteritems():
                if not datatable.index[entity][noi] is None:
                    datatable.set_value(var, np.ones(nb)*val, entity, noi)
            del var, val

        entity = 'men'
        nb = datatable.index[entity]['nb']
        for noi, dct in scenario.menage.iteritems():
            for var, val in dct.iteritems():
                if not datatable.index[entity][noi] is None:
                    datatable.set_value(var, np.ones(nb)*val, entity, noi)
            del var, val

        if nmen>1:
            if self.maxrev is None:
                raise Exception('france.Scenario: self.maxrev should not be None')
            maxrev = self.maxrev
            datatable.MAXREV = maxrev

            x_axis = self.x_axis
            if x_axis is None:
                raise Exception('france.Scenario: self.x_axis should not be None')
            var = None
            for axe in model.x_axes.itervalues():
                if axe.name == x_axis:
                    datatable.XAXIS = var = axe.col_name
            if var is None:
                datatable.XAXIS = x_axis
                var = x_axis

            vls = np.linspace(0, maxrev, nmen)
            if same_rev_couple is True:
                entity = 'men'
                datatable.set_value(var, 0.5*vls, entity, opt = 0)
                datatable.set_value(var, 0.5*vls, entity, opt = 1)
            else:
                datatable.set_value(var, vls, entity, opt = 0)
            datatable._isPopulated = True

