# coding: utf-8

import cookielib
from cStringIO import StringIO
import urllib
import urllib2
import urlparse
import re
import pdb

from lxml import etree

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    }
parser = etree.HTMLParser()
url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))


def go_to_next_page(parameters, response, form_element, form_to_take=1):
    response_url = response.geturl()
    request = urllib2.Request(urlparse.urljoin(response_url, form_element.get('action')), headers = headers)
    try:
        response = url_opener.open(request, urllib.urlencode(parameters, doseq = True))
    except urllib2.HTTPError as response:
        print "Erreur", response.code
        print response.read()
        raise
    html_page = response.read()
    tree = etree.parse(StringIO(html_page), parser)
    form_element = tree.xpath('//form')[form_to_take]
    return response, form_element, html_page


def _get_page_name(form_element):
    ''' determine la page sur laquelles on est via les questions qu'elle pose '''
    name_page = ''
    inputs = form_element.xpath("//input")
    input_pas_interessant = ['you_search', '', 'form_id', 'BCContinuer']
    inputs = [input for input in inputs
              if input.attrib.get('name', default='') not in input_pas_interessant]

    # distingue deux types de réponses
    inputs_radio = [input for input in inputs
                    if input.attrib['type'] == 'radio']
    inputs_not_radio = [input for input in inputs if input not in inputs_radio]

    ## regroupe les inputs radio:
    input_radio_names = [input.attrib['name'] for input in inputs_radio]
    for radio_name in set(input_radio_names):
        name_page += radio_name

    for input in inputs_not_radio:
        name = input.attrib['name']
        name_page += name

    return name_page

def _get_a_page(form_element):
    ''' determine la page sur laquelles on est
        - si la page existe (on a déjà vu les questions) on passe
        - sinon, on la créee'''
    page_question = []

    inputs = form_element.xpath("//input")
    input_pas_interessant = ['you_search', '', 'form_id', 'BCContinuer']
    inputs = [input for input in inputs
              if input.attrib.get('name', default='') not in input_pas_interessant]

    # distingue deux types de réponses
    inputs_radio = [input for input in inputs
                    if input.attrib['type'] == 'radio']
    inputs_not_radio = [input for input in inputs if input not in inputs_radio]

    ## regroupe les inputs radio:
    input_radio_names = [input.attrib['name'] for input in inputs_radio]
    for radio_name in set(input_radio_names):
        choices = [input.attrib['value'] for input in inputs_radio
                   if input.attrib['name'] == radio_name]
        page_question += [Question(radio_name, choices, 'radio')]

    for input in inputs_not_radio:
        name = input.attrib['name']
        if input.attrib['type'] == 'text':
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
                print name
                pdb.set_trace()
            page_question += [Question(name, values, 'text')]
        elif input.attrib['type'] == 'checkbox':
            page_question += [Question(name, ['false', 'true'], 'text')]
        elif input.attrib['type'] == 'submit':
            page_question += [Question(name, [name[2:]], 'submit')]
        else:
            print 'type non rencontré encore'
            print input.attrib['type']
            pdb.set_trace()

    return Page(page_question)



class Formulaire(object):

    def __init__(self, url, pages):
        self.reference = url
        self.pages = pages
        self.pages_collections = {}


    def set_choice(self, choices):
        ''' met une serie de réponse pour le formulaire
            pas besoin de mettre quand on a une seule
            réponse possible
        '''
        i = 0
        for page in self.pages:
            for question in page.questions:
                if len(question.possible_choices) > 1:
                    # cette condition inclue les dates
                    if i > len(choices):
                        raise Exception('Il faut plus de choix pour remplir le formulaire')
                    question.set_choice(choices[i])
                    i += 1
                else:
                    question.set_choice(question.possible_choices[0])

        self.check_pages()


    def check_pages(self):
        for page in self.pages:
            page.check_page()


    def init(self):
        # premiere page
        request = urllib2.Request(self.url, headers = headers)
        response = url_opener.open(request)
        html_page = response.read()
        tree = etree.parse(StringIO(html_page), parser)
        form_element = tree.xpath('//form')[1]
        return response, form_element


    def get_a_tree(self):
        response, form_element = self.init()
        init = {'BCCommencer': 'Commencer', 'conditionsSimuLog': 'true'}
        response, form_element, html = go_to_next_page(init, response, form_element)

        while 'droit à une aide au logement' not in html:
            # on cherche la page, ou bien on la crée
            name_page = _get_page_name(form_element)
            if 'otre conjoint'  in html.title():
                print 'Votre conjoint'
                import pdb
                pdb.set_trace()
            if name_page not in self.pages_collections:
                page_question = _get_a_page(form_element)
                self.pages_collections[name_page] = page_question
                page_question.init_choices()

            else:
                page_question = self.pages_collections[name_page]
                print name_page
                page_question.set_next_choices()


            parameters = page_question.get_parameters()
            parameters["BCContinuer"] = "Continuer"
            response, form_element, html = go_to_next_page(parameters, response, form_element)

#            if 'droit à une aide au logement'  in html:
        look = html[:(html.index('&euro') - 1)]
        montant = re.findall("\d+.\d+", look[-10:])[0]
        montant = montant.replace(',', '.')
        montant = float(montant)
        print montant

        print ('fin de boucle')
        import pdb
        pdb.set_trace()


    def get_parameters_serie(self):
        return [page.get_parameters() for page in self.pages]

    def fill_in(self):
        ''' remplir un formulaire avec les données de parameters'''
        response, form_element = self.init()
        parameters_serie = self.get_parameters_serie()
        for parameters in parameters_serie:
            print parameters
            response, form_element, html = go_to_next_page(parameters, response, form_element)

        if '&euro' in html and "loyer" not in html:
            look = html[:(html.index('&euro') - 1)]
            montant = re.findall("\d+.\d+", look[-10:])[0]
            montant = montant.replace(',', '.')
            montant = float(montant)
            return montant

        for input_element in form_element.xpath('.//input'):
            print etree.tostring(input_element)



class Page(object):

    def __init__(self, questions, number=0):
        self.questions = questions
        self.number = number
        self.suite = {}

    def get_parameters(self):
        dico = {}
        for question in self.questions:
            if question.choice is None:
                raise Exception('Il faut donne une valeur à ' + question.name)
            else:
                dico[question.name] = question.choice
        return dico

    def check_page(self):
        pass

    def init_choices(self):
        for question in self.questions:
            question.choice = question.possible_choices[0]

    def set_next_choices(self):
        for question in self.questions[::-1]:
            if question.possible_choices is None:
                raise Exception('Il faut donner des valeurs à ' + question.name)
            if question.choice is not None:
                old_idx = question.possible_choices.index(question.choice)
                if old_idx < len(question.possible_choices) - 1:
                    question.choice = question.possible_choices[old_idx + 1]
                    break
            # si on est là c'est qu'on bien qu'on est au bout
            # des possibilité pour la question
            # a ce moment, là on remet au début et on décale la question d'après
            question.choice = question.possible_choices[0]

    def boucle_bouclee(self):
        ''' test si on a tout le monde à zéro ce qui arrive quand on
            initialise et quand on a fait le tour des possibilités sinon '''
        return all([question.choice == question.possible_choices[0]
                    for question in self.questions])




class Question(object):

    def __init__(self, name, possible_choices, type='radio'):
        self.name = name
        self.possible_choices = possible_choices
        self.choice = None
        self.type = type

    def set_choice(self, choice):
        if self.possible_choices not in ["date", 'int']:
            if choice not in self.possible_choices:
                raise Exception('le choix ' + choice + ' ne va pas pour ' + self.name)
        if self.possible_choices == "date":
            pass  # TODO: check on form
        self.choice = choice

url = "http://www.caf.fr/redirect/s/Redirect?page=aidesEtServicesSimuLogement"
logement = Formulaire(url, [Page([])])
logement.get_a_tree()
