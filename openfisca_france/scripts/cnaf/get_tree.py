# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 15:44:05 2014

@author: AEidelman
Pour avoir l'arbre des questions
"""
import pdb

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from formulaires_caf import Question, Page, Formulaire
url = "http://www.caf.fr/redirect/s/Redirect?page=aidesEtServicesSimuLogement"

question_collection = {}
page_collection = {}

## init
browser = webdriver.Firefox()
browser.get(url)
condition = browser.find_element_by_name(u'conditionsSimuLog')
condition.click()
BCCommencer = browser.find_element_by_name("BCCommencer")
BCCommencer.click()

input_pas_interessant = ['you_search', '', 'form_id', 'BCContinuer']


def _get_inputs(browser):
    inputs = browser.find_elements_by_xpath("//input")
    inputs = [input for input in inputs
              if input.get_attribute('name') not in input_pas_interessant]
    for input in inputs:
        print(input.get_attribute('name'), input.get_attribute('type'))
    return inputs

def continuer(browser):
    BCContinuer = browser.find_element_by_name("BCContinuer")
    BCContinuer.click()


def create_page_from_inputs(browser):
    ''' determine la page sur laquelles on est
        - si la page existe (on a déjà vu les questions) on passe
        - sinon, on la créee'''
    global page_collection
    page_question = []
    name_page = ''

    inputs = _get_inputs(browser)

    inputs_radio = [input for input in inputs
                    if input.get_attribute('type') == 'radio']
    inputs_not_radio = [input for input in inputs if input not in inputs_radio]

    ## regroupe les inputs radio:
    input_radio_names = [input.get_attribute('name') for input in inputs_radio]
    for radio_name in set(input_radio_names):
        name_page += radio_name
        choices = [input.get_attribute('value') for input in inputs_radio
                   if input.get_attribute('name') == radio_name]
        page_question += [Question(radio_name, choices, 'radio')]

    for input in inputs_not_radio:
        name = input.get_attribute('name')
        name_page += name
        if input.get_attribute('type') == 'text':
            values = []
            if name == 'CODEPOS':
                values = ['75012']
            if name == 'MTLOY':  # généraliser à MT dans le nom ?
                values = [str(100*x) for x in range(1, 10)]
            if 'dt' in name:  # dtNaiss
                values = ['04/06/' + str(1920 + 10*x) for x in range(10)]
            if 'Nbr' in name:   # Enfant
                values = [str(x) for x in range(4)]
            if name == 'MTMENEVAFOR':
                values = [str(1+100*x) for x in range(15)]
            if 'Ress' in name:
                if 'RessSal' in name or 'RessCho' in name:
                    values = [str(1000*x) for x in range(20)]
                else:  # if 'RessFR' in name or 'RessIJ' in name:
                    values = ['0']
            if values == []:
                print(name)
                pdb.set_trace()
            page_question += [Question(name, values, 'text')]
        elif input.get_attribute('type') == 'checkbox':
            page_question += [Question(name, ['false', 'true'], 'text')]
        else:
            print('type non rencontré encore')
            print(input.get_attribute('type'))
            pdb.set_trace()

    if name_page not in page_collection.keys():
        page_collection[name_page] = page_question

    print(name_page)
    return name_page

def fill_page(browser, name_page):
    questions = page_collection[name_page]
    for question in questions:
        try:
            print('question', question.name)
            champs = browser.find_elements_by_name(question.name)
            if question.type == 'text':
                assert len(champs) == 1
                champs[0].send_keys(question.possible_choices[0])
            if question.type == 'radio':
                if champs[0].is_displayed():
                    champs[0].click()
        except:
            import pdb
            pdb.set_trace()


while 'droit à une aide au logement' not in browser.page_source:
    name_page = create_page_from_inputs(browser)
    if name_page == '':
        break
    fill_page(browser, name_page)
    try:
        continuer(browser)
    except:
        pdb.set_trace()

xxx


conditions = Question('conditionsSimuLog', ["true"])
BCCommencer = Question("BCCommencer", ["Commencer"])
BCContinuer = Question("BCContinuer", ["Continuer"])
page0 = Page([conditions, BCCommencer])

CODEPOS = Question("CODEPOS", 'int', 'text')  # TODO:
page1 = Page([CODEPOS, BCContinuer])

logOcc = Question("logOcc", ["loc", "etudiant", "foy",
                             "accpart", "accpp",
                            ])
doubleRes = Question("doubleRes", ['false', 'true'])
page2 = Page([logOcc, doubleRes, BCContinuer])

logType = Question("logType", ["appartement", "chambre"])
logQui = Question('logQui', ['seul', 'conjoint', "autperson"])
logMeuble = Question('logMeuble', ['oui', 'non'])
page3 = Page([logType, logQui, logMeuble, BCContinuer])

loyer = Question("MTLOY", 'int')
page4 = Page([loyer, BCContinuer])

sitMatCpl = Question('sitMatCpl', ['oui', 'non'])
dtNaissR = Question("dtNaissR", 'date')
dtNaissC = Question("dtNaissC", 'date')
topGross = Question('topGross', ['oui', 'non'])
topGross4mois = Question('topGross4mois', ['oui', 'non'])
tecNbrEnfant = Question("tecNbrEnfant", 'int')
tecNbrAutre = Question("tecNbrAutre", 'int')
page5 = Page([sitMatCpl, dtNaissR, dtNaissC, topGross, topGross4mois,
              tecNbrEnfant, tecNbrAutre, BCContinuer])

actPro = Question('actPro', ['oui', 'non'])
beneRsa = Question('beneRsa', ['oui', 'non'])
page6 = Page([actPro, beneRsa, BCContinuer])

sitActNon = Question('sitActNon', ['chomage_imposable', 'ebo', 'etudiant', "parfoy",
                                   'retre', 'arrtrav', 'han', 'inc'
                                   'aut'])
page7 = Page([sitActNon, BCContinuer])

sitChoDuree = Question('sitChoDuree', ["inf2m", "sup2m"])
sitChoAlloc = Question('sitChoAlloc', ['are', 'ass', 'ata', 'aca',
                                       'asr', 'autind', 'attind', 'allnok'])
page8 = Page([sitChoDuree, sitChoAlloc, BCContinuer])


revPercuSeul = Question('revenusPercusSeul', 'int')
chomPercuSeul = Question('indemnitesChomagePercuesSeul', 'int')
ressPercuSeul = Question('RessourcesPercuesSeul', 'int')
pfPercuSeul = Question('pfPercusSeul', 'int')
page_rev = Page([revPercuSeul, chomPercuSeul,
                 ressPercuSeul, pfPercuSeul, BCContinuer])


logement = Formulaire(url, [Page([]), page0, page1, page2, page3,
                            page4, page5, page6, page7, page8])

if __name__ == '__main__':
    exemple = ['75012',
               'loc', 'false',
               "appartement", 'seul', 'non',
               '500',
               'oui', '01/04/1980', '05/03/1975', 'non', 'non', '2', '0',
               'oui', 'oui',
               'chomage_imposable',
               'sup2m', 'ass']

#    logement.set_choice(exemple)
    logement.get_tree()

#for sitPro in rsaSitPro.possible_choices:
#    exemple[-1] = sitPro
#    rsa.set_choice(exemple)
#    print('********* ' + sitPro)
#    rsa.fill_in()

#continue = "EtudiantSalarie",



#print html_page
#
#print etree.tostring(form_element)




