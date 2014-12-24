# coding: utf-8

import cookielib
from cStringIO import StringIO
import urllib
import urllib2
import urlparse
import re

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


class Formulaire(object):

    def __init__(self, url, pages):
        self.url = url        
        self.pages = pages
        self.tree = None
        

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

    def get_parameters_serie(self):
        return [page.get_parameters() for page in self.pages]

    def fill_in(self):
        response, form_element = self.init()
        parameters_serie = self.get_parameters_serie()
        for parameters in parameters_serie:
            print parameters
            response, form_element, html = go_to_next_page(parameters, response, form_element)         
        
        if '&euro' in html and "loyer" not in html:   
            look = html[:(html.index('&euro') - 1)]
            montant = int(re.search('(\d+)$', look).group(0))        
            return montant
  
        for input_element in form_element.xpath('.//input'):
            print etree.tostring(input_element)


class Page(object):

    def __init__(self, questions, number=0):
        self.questions = questions
        self.number = number

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


class Question(object):

    def __init__(self, name, possible_choices):
        self.name = name
        self.possible_choices = possible_choices
        self.choice = None

    def set_choice(self, choice):
        if self.possible_choices not in ["date", 'int']:
            if choice not in self.possible_choices:
                raise Exception('le choix ' + choice + ' ne va pas pour ' + self.name)
        if self.possible_choices == "date":
            pass  # TODO: check on form
        self.choice = choice


