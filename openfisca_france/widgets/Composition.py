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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from datetime import date, datetime
import os
import pickle

#from openfisca_core import model
from openfisca_qt.gui.qt.QtGui import (
    QApplication,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDockWidget,
    QDoubleSpinBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    )
from openfisca_qt.gui.qt.QtCore import QObject, SIGNAL, SLOT, QDate, Qt, Signal
from openfisca_qt.gui.qt.compat import to_qvariant
from openfisca_qt.gui.views.ui_composition import Ui_Menage
from openfisca_qt.gui.views.ui_logement import Ui_Logement
from openfisca_qt.widgets.InfoComp import InfoComp
from openfisca_qt.widgets.Declaration import Declaration
from openfisca_qt.gui.utils.qthelpers import create_action
from openfisca_qt.gui.config import CONF, get_icon
from openfisca_qt.plugins import OpenfiscaPluginWidget
from openfisca_qt.plugins.scenario import CompositionConfigPage
from openfisca_qt.gui.baseconfig import get_translation

from openfisca_france import CURRENCY  # , DATA_DIR


_ = get_translation('openfisca_qt')


class S:
    name = 0
    birth = 1
    decnum = 2
    decpos = 3
    decbtn = 4
    famnum = 5
    fampos = 6


class CompositionWidget(OpenfiscaPluginWidget, Ui_Menage):
    """
    Scenario Graph Widget
    """
    CONF_SECTION = 'composition'
    CONFIGWIDGET_CLASS = CompositionConfigPage
    FEATURES = QDockWidget.DockWidgetClosable | \
        QDockWidget.DockWidgetFloatable | \
        QDockWidget.DockWidgetMovable
    DISABLE_ACTIONS_WHEN_HIDDEN = False
    sig_option_changed = Signal(str, object)
    XAXIS_PROPERTIES = {
        'salaire_imposable': {
            'name': 'salaire_imposable',
            'typ_tot': {
                'salsuperbrut': 'Salaire super brut',
                'salbrut': 'Salaire brut',
                'salaire_imposable': 'Salaire imposable',
                'salaire_net': 'Salaire net'
                },
            'typ_tot_default': 'salaire_imposable',
            },
        'choi': {
            'name': 'cho',
            'col_name': 'choi',
            'typ_tot': {
                'chobrut': u"Chômage brut",
                'cho': u"Chômage",
                'chonet': u"Chômage net",
                },
            'typ_tot_default': 'cho'
            },
        'rsti': {
            'name': 'rst',
            'col_name': 'rsti',
            'typ_tot': {
                'rstbrut': u"Retraite brut",
                'rst': u"Retraite",
                'rstnet': u"Retraite net"
                },
            'typ_tot_default': 'rst'
            },
        'f2da': {
            'name': 'divpfl',
            'col_name': 'f2da',
            'typ_tot': {
                'rev_cap_brut': u"Revenus des capitaux",
                'rev_cap_net': u"Revenus des capitaux nets"
                },
            'typ_tot_default': 'rev_cap_brut',
            },
        'f2ee': {
            'name': 'intpfl',
            'col_name': 'f2ee',
            'typ_tot': {
                'rev_cap_brut': "Revenus des capitaux",
                'rev_cap_net': "Revenus des capitaux nets",
                },
            'typ_tot_default': 'rev_cap_brut'
            },
        'f2dc': {
            'name': 'divb',
            'col_name': 'f2dc',
            'typ_tot': {
                'rev_cap_brut': "Revenus des capitaux",
                'rev_cap_net': "Revenus des capitaux nets"
                },
            'typ_tot_default': 'rev_cap_brut'
            },
        'f2tr': {
            'name': 'intb',
            'col_name': 'f2tr',
            'typ_tot': {
                'rev_cap_brut': "Revenus des capitaux",
                'rev_cap_net': "Revenus des capitaux nets"
                },
            'typ_tot_default': 'rev_cap_brut'
            },
        'pensions_alimentaires_percues': {
            'name': 'pensions_alimentaires_percues',
            'col_name': 'pensions_alimentaires_percues',
            'typ_tot': {
                'pen': "Pensions"
                },
            'typ_tot_default': 'pen'
            },
        'f6gu': {
            'name': 'f6gu',
            'col_name': 'f6gu',
            'typ_tot': {
                'pen': "Pensions"
                },
            'typ_tot_default': 'pen'},
        'f4ba': {
            'name': 'f4ba',
            'col_name': 'f4ba',
            'typ_tot': {
                'fon': "Revenus fonciers"
                },
            'typ_tot_default': 'fon'
        },
    }

    def __init__(self, scenario = None, parent = None):
        super(CompositionWidget, self).__init__(parent)
        self.setupUi(self)
        if parent is not None:
            self.parent = parent

        self.setLayout(self.verticalLayout)
        # Initialize xaxes
        x_axis = self.get_option('x_axis')
        axes_names = []
        for col, axe in self.XAXIS_PROPERTIES.iteritems():
            self.x_axis_box.addItem(col, to_qvariant(axe["name"]))  # convert col to label by using tax_benefit_system
#            self.x_axis_box.addItem(axe.label, to_qvariant(axe.name))
            axes_names.append(axe["name"])
        self.x_axis_box.setCurrentIndex(axes_names.index(x_axis))

        self.initialize_plugin()
        # Initialize maxrev # make it country dependant
        self.maxrev_box.setMinimum(0)
        self.maxrev_box.setMaximum(100000000)
        self.maxrev_box.setSingleStep(1000)
        self.maxrev_box.setSuffix(CURRENCY)
        maxrev = self.get_option('maxrev')
        self.maxrev_box.setValue(maxrev)
        self.maxrev = maxrev

        if scenario is not None:
            self.set_scenario(scenario)

        self.connect(self.open_btn, SIGNAL('clicked()'), self.load)
        self.connect(self.save_btn, SIGNAL('clicked()'), self.save)
        self.connect(self.add_btn, SIGNAL('clicked()'), self.addPerson)
        self.connect(self.rmv_btn, SIGNAL('clicked()'), self.rmvPerson)
        self.connect(self.lgt_btn, SIGNAL('clicked()'), self.openLogement)
        self.connect(self.inf_btn, SIGNAL('clicked()'), self.openInfoComp)
        self.connect(self.reset_btn, SIGNAL('clicked()'), self.resetScenario)
        self.connect(self.x_axis_box, SIGNAL('currentIndexChanged(int)'), self.set_x_axis)
        self.connect(self.maxrev_box, SIGNAL('valueChanged(int)'), self.set_maxrev)
        self.connect(self, SIGNAL('compoChanged()'), self.changed)
        self._listPerson = []
        self.addPref()
        self.rmv_btn.setEnabled(False)
        self.emit(SIGNAL("ok()"))

    #------ Public API ---------------------------------------------

    def set_scenario(self, scenario):
        """
        Set scenario_simualtion
        """
        # TODO fix this
        x_axis = self.get_option('x_axis')
        maxrev = self.maxrev
        nmen = self.get_option('nmen')
        self.nmen = nmen
        value = CONF.get('parameters', 'datesim')
        datesim = datetime.strptime(value, "%Y-%m-%d").date()

        self.scenario = scenario
        self.scenario.year = datesim.year

    def set_x_axis(self):
        '''
        Sets the varying variable of the scenario
        '''
        widget = self.x_axis_box
        if isinstance(widget, QComboBox):
            data = widget.itemData(widget.currentIndex())
            x_axis = unicode(data)
            self.scenario.x_axis = x_axis
            self.set_option('x_axis', x_axis)
        self.emit(SIGNAL('compoChanged()'))

    def set_maxrev(self):
        '''
        Sets the varying variable of the scenario
        '''
        widget = self.maxrev_box

        if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
            maxrev = widget.value()
            print "in set_maxrev :", maxrev
            self.scenario.maxrev = maxrev
            self.set_option('maxrev', maxrev)
            self.maxrev = maxrev

        self.emit(SIGNAL('compoChanged()'))

    def changed(self):
        self.disconnectAll()
#        self.scenario.genNbEnf()
        self.populate()
        self.action_compute.setEnabled(True)
        self.emit(SIGNAL('changed()'))
        self.connectAll()

    def nbRow(self):
        return self.scenario.nbIndiv()

    def populate(self):
        self.populateBirth()
        self.populateQuifoyCombo()
        self.populateFoyerCombo()
        self.populateQuifamCombo()
        self.populateFamilleCombo()

    def populateBirth(self):
        for noi, vals in self.scenario.indiv.iteritems():
            birth = QDate(vals['birth'])
            self._listPerson[noi][S.birth].setDate(birth)

    def populateFoyerCombo(self):
        declarKeys = self.scenario.declar.keys()
        for noi, vals in self.scenario.indiv.iteritems():
            noidec = vals['noidec']
            box = self._listPerson[noi][S.decnum]
            box.clear()
            button = self._listPerson[noi][S.decbtn]
            button.setText('Foyer %d' % (noidec + 1))
            if vals['quifoy'] == 'vous':
                box.addItems(['%d' % (noidec + 1)])
                button.setEnabled(True)
            else:
                box.addItems(['%d' % (k + 1) for k in declarKeys])
                button.setEnabled(False)
                box.setCurrentIndex(declarKeys.index(noidec))

    def populateQuifoyCombo(self):
        for noi, vals in self.scenario.indiv.iteritems():
            quifoy = vals['quifoy']
            # retrieve the foyer combobox of individu number noi
            box = self._listPerson[noi][S.decpos]
            # set the combobox to 'vous' 'conj' or 'pac'
            if quifoy == 'vous':
                box.setCurrentIndex(0)
            elif quifoy == 'conj':
                box.setCurrentIndex(1)
            elif quifoy[:3] == 'pac':
                box.setCurrentIndex(2)

    def populateFamilleCombo(self):
        familleKeys = self.scenario.famille.keys()
        for noi, vals in self.scenario.indiv.iteritems():
            noichef = vals['noichef']
            box = self._listPerson[noi][S.famnum]
            box.clear()
            if vals['quifam'] == 'parent 1':
                box.addItems(['%d' % (noichef + 1)])
            else:
                box.addItems(['%d' % (k + 1) for k in familleKeys])
                box.setCurrentIndex(familleKeys.index(noichef))

    def populateQuifamCombo(self):
        for noi, vals in self.scenario.indiv.iteritems():
            quifam = vals['quifam']
            # retrieve the foyer combobox of individu number noi
            box = self._listPerson[noi][S.fampos]
            # set the combobox to 'parent 1' 'parent 2' or 'enfant'
            if quifam == 'chef':
                box.setCurrentIndex(0)
            elif quifam == 'part':
                box.setCurrentIndex(1)
            elif quifam[:3] == 'enf':
                box.setCurrentIndex(2)

    def birthChanged(self, date):
        senderNoi = int(self.sender().objectName()[3])
        self.scenario.indiv[senderNoi].update({'birth': date.toPyDate()})
        self.emit(SIGNAL('compoChanged()'))

    def foyerChanged(self):
        sender = self.sender()
        noi = int(sender.objectName()[3])
        newfoyer = int(sender.currentText()[-1]) - 1
        self.scenario.modify(noi, newFoyer = newfoyer)
        self.emit(SIGNAL('compoChanged()'))

    def quifoyChanged(self, newQuifoy):
        senderNoi = int(self.sender().objectName()[3])
        self.scenario.modify(senderNoi, newQuifoy = newQuifoy)
        self.emit(SIGNAL('compoChanged()'))

    def familleChanged(self):
        sender = self.sender()
        noi = int(sender.objectName()[3])
        newfamille = int(sender.currentText()[-1]) - 1
        self.scenario.modifyFam(noi, newFamille = newfamille)
        self.emit(SIGNAL('compoChanged()'))

    def quifamChanged(self, newFam):
        if newFam == 'parent 1':
            qui = 'chef'
        elif newFam == 'parent 2':
            qui = 'part'
        elif newFam == 'enfant':
            qui = 'enf'
        senderNoi = int(self.sender().objectName()[3])
        self.scenario.modifyFam(senderNoi, newQuifam = qui)
        self.emit(SIGNAL('compoChanged()'))

    def addPref(self):
        noi = 0
        self._listPerson.append([QLabel('%d' % (noi + 1), self),
                                 QDateEdit(self),
                                 QComboBox(self),
                                 QComboBox(self),
                                 QPushButton(self),
                                 QComboBox(self),
                                 QComboBox(self)])

        temp = self._listPerson[0]

        temp[S.birth].setDisplayFormat(QApplication.translate("Page01", "dd MMM yyyy", None, QApplication.UnicodeUTF8))
        temp[S.birth].setObjectName('Bir%d' % noi)
        temp[S.birth].setCurrentSection(QDateEdit.YearSection)

        temp[S.decpos].setObjectName('Dec%d' % noi)
        temp[S.decpos].addItems(['vous'])
        temp[S.decpos].setEnabled(False)

        temp[S.decnum].setObjectName('Foy%d' % noi)
        temp[S.decnum].setEnabled(False)

        temp[S.fampos].addItems(['parent 1'])
        temp[S.fampos].setObjectName('Fam%d' % noi)
        temp[S.fampos].setEnabled(False)

        temp[S.famnum].setObjectName('Fam%d' % noi)
        temp[S.famnum].setEnabled(False)

        temp[S.decbtn].setObjectName('But%d' % noi)

        for i in xrange(7):
            self.gridLayout.addWidget(temp[i], noi + 2, i)
            self.gridLayout.setAlignment(temp[i], Qt.AlignCenter)

        self.emit(SIGNAL('compoChanged()'))

    def addPerson(self):
        noi = self.nbRow()
        self.addRow()
        if noi == 1:
            self.scenario.addIndiv(noi, birth = date(1975, 1, 1), quifoy = 'conj', quifam = 'part')
        else:
            self.scenario.addIndiv(noi, birth = date(2000, 1, 1), quifoy = 'pac', quifam = 'enf')
        self.emit(SIGNAL('compoChanged()'))

    def addRow(self):
        noi = len(self._listPerson)
        self._listPerson.append(
            [
                QLabel('%d' % (noi + 1), self),
                QDateEdit(self),
                QComboBox(self),
                QComboBox(self),
                QPushButton(self),
                QComboBox(self),
                QComboBox(self)
                ]
            )
        temp = self._listPerson[-1]

        temp[S.birth].setDisplayFormat(QApplication.translate("Page01", "dd MMM yyyy", None, QApplication.UnicodeUTF8))
        temp[S.birth].setObjectName('Bir%d' % noi)
        temp[S.birth].setCurrentSection(QDateEdit.YearSection)

        temp[S.decpos].setObjectName('Dec%d' % noi)
        temp[S.decpos].addItems(['vous', 'conj', 'pac'])

        temp[S.decnum].setObjectName('Foy%d' % noi)

        temp[S.fampos].setObjectName('Fam%d' % noi)
        temp[S.fampos].addItems(['parent 1', 'parent 2', 'enfant'])

        temp[S.famnum].setObjectName('Fam%d' % noi)

        temp[S.decbtn].setObjectName('But%d' % noi)

        for i in xrange(7):
            self.gridLayout.addWidget(temp[i], noi + 2, i)
            self.gridLayout.setAlignment(temp[i], Qt.AlignCenter)

        self.rmv_btn.setEnabled(True)
        if len(self.scenario.indiv) == 9:
            self.add_btn.setEnabled(False)

    def rmvPerson(self, noi = None):
        if noi is None:
            noi = self.nbRow() - 1
        self.scenario.rmvIndiv(noi)
        self.rmvRow()
        self.add_btn.setEnabled(True)

        self.emit(SIGNAL('compoChanged()'))

    def rmvRow(self):
        '''
        Enlève le dernier individu et l'efface dans le foyer
        '''
        toDel = self._listPerson.pop()
        for widget in toDel:
            widget.setParent(None)
        if len(self.scenario.indiv) == 1:
            self.rmv_btn.setEnabled(False)

    def resetScenario(self):
        '''
        Resets scenario
        '''
        while self.nbRow() > 1:
            self.rmvPerson()
        self.simulation.reset_scenario
        self.emit(SIGNAL('compoChanged()'))

    def openDeclaration(self):
        """
        Open the declaration widget
        """
        noi = int(self.sender().objectName()[3])
        self.scenario.genNbEnf()
        msg = self.scenario.check_consistency()
        if msg:
            QMessageBox.critical(self, u"Ménage non valide",
                                 msg,
                                 QMessageBox.Ok, QMessageBox.NoButton)
            return False
        self._declaration = Declaration(self, noi)
        self._declaration.exec_()
        self.emit(SIGNAL('compoChanged()'))

    def openLogement(self):
        self._logement = Logement(self.scenario, self)
        self._logement.exec_()
        self.emit(SIGNAL('compoChanged()'))

    def openInfoComp(self):
        self._infocomp = InfoComp(self.scenario, self)
        self._infocomp.exec_()
        self.emit(SIGNAL('compoChanged()'))

    def disconnectAll(self):
        for person in self._listPerson:
            QObject.disconnect(person[S.birth], SIGNAL('dateChanged(QDate)'), self.birthChanged)
            QObject.disconnect(person[S.decpos], SIGNAL('currentIndexChanged(QString)'), self.quifoyChanged)
            QObject.disconnect(person[S.decnum], SIGNAL('currentIndexChanged(int)'), self.foyerChanged)
            QObject.disconnect(person[S.fampos], SIGNAL('currentIndexChanged(QString)'), self.quifamChanged)
            QObject.disconnect(person[S.famnum], SIGNAL('currentIndexChanged(int)'), self.familleChanged)
            QObject.disconnect(person[S.decbtn], SIGNAL('clicked()'), self.openDeclaration)

    def connectAll(self):
        for person in self._listPerson:
            QObject.connect(person[S.birth], SIGNAL('dateChanged(QDate)'), self.birthChanged)
            QObject.connect(person[S.decpos], SIGNAL('currentIndexChanged(QString)'), self.quifoyChanged)
            QObject.connect(person[S.decnum], SIGNAL('currentIndexChanged(int)'), self.foyerChanged)
            QObject.connect(person[S.fampos], SIGNAL('currentIndexChanged(QString)'), self.quifamChanged)
            QObject.connect(person[S.famnum], SIGNAL('currentIndexChanged(int)'), self.familleChanged)
            QObject.connect(person[S.decbtn], SIGNAL('clicked()'), self.openDeclaration)

    def load(self):
        cas_type_dir = self.get_option('import_dir')
        fileName = QFileDialog.getOpenFileName(self,
                                               _("Open a test case"),
                                               cas_type_dir,
                                               u"Cas type OpenFisca (*.ofct)")
        if not fileName == '':
            n = len(self.scenario.indiv)
            try:
                self.scenario.openFile(fileName)
                while n < self.nbRow():
                    self.addRow()
                    n += 1
                while n > self.nbRow():
                    self.rmvRow()
                    n -= 1
                self.emit(SIGNAL('compoChanged()'))
                self.emit(SIGNAL("ok()"))
            except Exception, e:
                QMessageBox.critical(
                    self, "Erreur", u"Erreur lors de l'ouverture du fichier : le fichier n'est pas reconnu : \n " + e,
                    QMessageBox.Ok, QMessageBox.NoButton)

    def save(self):
        cas_type_dir = self.get_option('export_dir')
        default_fileName = os.path.join(cas_type_dir, 'sans-titre')
        fileName = QFileDialog.getSaveFileName(self,
                                               _("Save a test case"),
                                               default_fileName,
                                               u"Cas type OpenFisca (*.ofct)")
        if not fileName == '':
            self.scenario.saveFile(fileName)

    def compute(self):
        """
        Computing the test case
        """
        self.starting_long_process(_("Computing test case ..."))
        # TODO
        # Consistency check on scenario
#        msg = self.scenario.check_consistency()
#        if msg:
#            QMessageBox.critical(self, u"Ménage non valide",
#                                 msg,
#                                 QMessageBox.Ok, QMessageBox.NoButton)
#            return False
        # If it is consistent starts the computation

        self.action_compute.setEnabled(False)

#        P, P_default = self.main.parameters.getParam(), self.main.parameters.getParam(defaut = True)
#        self.simulation.set_param(P, P_default)

        import openfisca_france
        TaxBenefitSystem = openfisca_france.init_country()
        tax_benefit_system = TaxBenefitSystem()

        axes = [
            dict(
                count = self.nmen,
                name = 'salaire_imposable',
                max = self.maxrev,
                min = 0,
                ),
            ]

        test_case = {
            "familles": {
                "fam0": {
                    "parents": ['ind0'],
                    "enfants": [],
                    },
                },
            "foyers_fiscaux": {
                "foy0": {
                    "declarants": ['ind0'],
                    "personnes_a_charge": [],
                    }
                },
            "individus": {
                "ind0": {
                    "activite": 0,
                    "birth": '1970-01-01',
                    "statmarit": 2,
                    },
                },
            "menages": {
                "men0": {
                    "personne_de_reference": 'ind0',
                    "conjoint": None,
                    "enfants": [],
                    "autres": [],
                    },
                }
            }

        self.scenario = tax_benefit_system.new_scenario().init_from_attributes(
            axes = axes,
            test_case = test_case,
            year = 2013,
            )
        print self.scenario.test_case
        self.scenario.simulation = self.scenario.new_simulation(debug = True)
        self.scenario.simulation.compute('revdisp')

        self.main.scenario = self.scenario
        self.main.refresh_test_case_plugins()
        self.ending_long_process(_("Test case results are updated"))

    def set_reform(self, reform):
        '''
        Toggle reform mode for test case  # TODO should be in another widget
        '''
        if (not reform) and self.action_set_reform.isChecked():
            self.action_set_reform.toggle()
        if (not self.action_set_reform.isChecked()) and reform:
            self.action_set_reform.toggle()

        self.scenario.set_config(reforme = reform, maxrev=self.maxrev)
        self.action_compute.setEnabled(True)

    def set_single(self, is_single = True):
        if is_single:
            self.scenario.set_config(nmen = 1, mode = 'castype') # TODO: this might be removed ??
            self.action_compute.setEnabled(True)
            self.action_set_bareme.setChecked(False)
        else:
            self.action_set_bareme.setChecked(True)
            self.set_bareme()
        self.action_compute.setEnabled(True)

    def set_bareme(self, is_bareme = True):
        if is_bareme:
            nmen = self.get_option('nmen')
            self.scenario.set_config(nmen = nmen, mode = 'bareme') # # TODO: this might be removed ??
            self.action_compute.setEnabled(True)
            self.action_set_single.setChecked(False)
        else:
            self.action_set_single.setChecked(True)
            self.set_single()
        self.action_compute.setEnabled(True)

    #------ OpenfiscaPluginMixin API ---------------------------------------------

    def apply_plugin_settings(self, options):
        """
        Apply configuration file's plugin settings
        """
        if 'maxrev' in options:
            maxrev = self.get_option('maxrev')
            self.maxrev_box.setValue(maxrev)
            self.maxrev = maxrev
            print "in apply setting :", self.maxrev
        if 'x_axis' in options:
            x_axis = self.get_option('x_axis')
            axes_names = [
                axe.name
                for axe in self.XAXIS_PROPERTIES.itervalues()
                ]
            self.x_axis_box.setCurrentIndex(axes_names.index(x_axis))

    #------ OpenfiscaPluginWidget API ---------------------------------------------
    def get_plugin_title(self):
        """
        Return plugin title
        Note: after some thinking, it appears that using a method
        is more flexible here than using a class attribute
        """
        return _("Composer")

    def get_plugin_icon(self):
        """
        Return plugin icon (QIcon instance)
        Note: this is required for plugins creating a main window
              (see OpenfiscaPluginMixin.create_mainwindow)
              and for configuration dialog widgets creation
        """
        return get_icon('OpenFisca22.png')

    def get_plugin_actions(self):
        """
        Return a list of actions related to plugin
        Note: these actions will be enabled when plugin's dockwidget is visible
              and they will be disabled when it's hidden
        """

        for index, (qobject, context, name, default) in enumerate(self.main.shortcut_data):
            if context == "Composer":
                self.main.shortcut_data.pop(index)
                qobject.deleteLater()
                del name, default

        # File menu actions and shortcuts

        self.open_action = create_action(
            self,
            _("&Open composition..."),
            icon='fileopen.png',
            tip =_("Open composition file"),
            triggered=self.load
            )
        self.register_shortcut(
            self.open_action,
            context = "Composer",
            name = _("Open composition file"),
            default="Ctrl+O"
            )

        self.save_action = create_action(
            self,
            _("&Save composition"),
            icon='filesave.png',
            tip=_("Save current composition"),
            triggered=self.save
            )

        self.register_shortcut(
            self.save_action,
            context="Composer",
            name=_("Save current composition"),
            default="Ctrl+S"
            )

        self.file_menu_actions = [self.open_action, self.save_action]
        self.main.file_menu_actions += self.file_menu_actions

        self.action_compute = create_action(
            self,
            _('Compute test case'),
            icon = 'calculator_green.png',
            triggered = self.compute
            )
        self.register_shortcut(
            self.action_compute,
            context = 'Composer',
            name = _('Compute test case'),
            default = 'F9'
            )

        self.action_set_bareme = create_action(
            self,
            _('Varying revenues'),
            icon = 'bareme22.png',
            toggled = self.set_bareme
            )
        self.action_set_single = create_action(
            self,
            _('Single test case'),
            icon = 'castype22.png',
            toggled = self.set_single
            )

        self.action_set_reform = create_action(
            self,
            _('Reform mode'),
            icon = 'comparison22.png',
            toggled = self.set_reform,
            tip = u"Différence entre la situation simulée et la situation actuelle"
            )

        self.run_menu_actions = [self.action_compute, self.action_set_bareme,
                                 self.action_set_single, self.action_set_reform,
                                 None]

        self.main.run_menu_actions += self.run_menu_actions
        self.main.test_case_toolbar_actions += self.run_menu_actions

        return self.file_menu_actions + self.run_menu_actions

    def register_plugin(self):
        """
        Register plugin in OpenFisca's main window
        """

        self.main.add_dockwidget(self)
        self.action_set_bareme.trigger()

    def refresh_plugin(self):
        '''
        Update Scenario Table
        '''
        pass

    def closing_plugin(self, cancelable=False):
        """
        Perform actions before parent main window is closed
        Return True or False whether the plugin may be closed immediately or not
        Note: returned value is ignored if *cancelable* is False
        """
        return True

#
#        OpenfiscaPluginWidget.visibility_changed(self, enable)
#        if self.dockwidget.isWindow():
#            self.dock_toolbar.show()
#        else:
#            self.dock_toolbar.hide()
#        if enable:
#            self.refresh_plugin()


def get_zone(code, filename = None):
    '''
    Gets commune name and zone apl from postal code
    '''
    if filename is None:
        code_file = open(os.path.join(DATA_DIR, 'code_apl'), 'r')
    else:
        code_file = open(filename, 'r')
    code_dict = pickle.load(code_file)
    code_file.close()
    if str(code) in code_dict:
        commune = code_dict[str(code)]
        return commune
    else:
        return None


class Logement(QDialog, Ui_Logement):
    def __init__(self, scenario, parent = None):
        super(Logement, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.scenario = scenario
        self.spinCP.setValue(scenario.menage[0]['code_postal'])
        self.spinLoyer.setValue(scenario.menage[0]['loyer'])
        self.comboSo.setCurrentIndex(scenario.menage[0]['statut_occupation'] - 1)  # -1 because 0 is "non renseigné"
        self.spinTH.setValue(scenario.menage[0]['taxe_habitation'])  # -1 because 0 is "non renseigné"

        def update_ville(code):
            commune = get_zone(code)
            if commune is not None:
                self.bbox.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                commune = ("Ce code postal n'est pas reconnu", '2')
                self.bbox.button(QDialogButtonBox.Ok).setEnabled(False)

            self.commune.setText(commune[0])
            self.spinZone.setValue(int(commune[1]))

        update_ville(self.spinCP.value())

        self.connect(self.spinCP, SIGNAL('valueChanged(int)'), update_ville)

        def update_th(value):
            self.spinTH.setValue(int(value))

        self.connect(self.spinTH, SIGNAL('valueChanged(int)'), update_th)

        def so_changed(value):
            if value in (0, 1):
                self.spinLoyer.setValue(0)
                self.spinLoyer.setEnabled(False)
            else:
                self.spinLoyer.setValue(500)
                self.spinLoyer.setEnabled(True)

        self.connect(self.comboSo, SIGNAL('currentIndexChanged(int)'), so_changed)
        self.connect(self.bbox, SIGNAL("accepted()"), SLOT("accept()"))
        self.connect(self.bbox, SIGNAL("rejected()"), SLOT("reject()"))

    def accept(self):
        self.scenario.menage[0].update({
            'loyer': int(self.spinLoyer.value()),
            'statut_occupation': int(self.comboSo.currentIndex() + 1),  # +1 because 0 is "non renseigné"
            'zone_apl': int(self.spinZone.value()),
            'code_postal': int(self.spinCP.value()),
            'taxe_habitation': int(self.spinTH.value())
            })
        QDialog.accept(self)
