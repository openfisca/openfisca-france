# coding: utf-8

from formulaires_caf import Question, Page, Formulaire
url = "http://www.caf.fr/redirect/s/Redirect?page=aidesEtServicesTestRsa"

conditionsRsa = Question('conditionsRsa', ["true"])
BCCommencer = Question("BCCommencer", ["Commencer"])
BCContinuer = Question("BCContinuer", ["Continuer"])
page0 = Page([conditionsRsa, BCCommencer])

residez = Question("residez", ["FranceMetro", 'Autres'])  # TODO:
page1 = Page([residez, BCContinuer])

seulOuCouple = Question("seulOuCouple", ["SEUL", "COUPLE"])
DateIsole = Question("DateIsole", 'date')
page2 = Page([seulOuCouple, DateIsole, BCContinuer])

typePers = Question("typePers", ['MME', 'MON'])
NOM = Question("NOM", ['Martin'])
PRENOM = Question("PRENOM", ['Alain'])
dateNaissance = Question("dateNaissance", 'date')
naissance = Question("naissance", ['', 'True'])
enfantMoins3 = Question("enfantMoins3", 'int')
enfantPlus3 = Question("enfantPlus3", 'int')
enfantPlus14 = Question("enfantPlus14", 'int')
page3 = Page([typePers, NOM, PRENOM, dateNaissance, naissance,
              enfantMoins3, enfantPlus3, enfantPlus14, BCContinuer])

rsaSitPro = Question("rsaSitPro", ["EtudiantEleve", "EtudiantSalarie",
                                   "Disponibilite", "Sabbatique", "Parental",
                                   "SansActivite", "Eti", "EnActivite"])
page4 = Page([rsaSitPro, BCContinuer])


revPercuSeul = Question('revenusPercusSeul', 'int')
chomPercuSeul = Question('indemnitesChomagePercuesSeul', 'int')
ressPercuSeul = Question('RessourcesPercuesSeul', 'int')
pfPercuSeul = Question('pfPercusSeul', 'int')
page_rev = Page([revPercuSeul, chomPercuSeul,
                 ressPercuSeul, pfPercuSeul, BCContinuer])

rsa = Formulaire(url, [Page([]), page0, page1, page2, page3, page4, page_rev])


# TODO: a mettre
def check_formulaire(formulaire):
    if formulaire["seulOuCouple"] == "COUPLE":
        assert formulaire["DateIsole"] == ""
        
if __name__ == '__main__':
    exemple = ["FranceMetro",
               'SEUL', "01/06/2003",
               'MON', "01/06/1960", '', '0', '2', '0',
               "EnActivite",
               '0', '0', '0', '0']
    rsa.set_choice(exemple)
    rsa.fill_in()

#for sitPro in rsaSitPro.possible_choices:
#    exemple[-1] = sitPro
#    rsa.set_choice(exemple)
#    print('********* ' + sitPro)
#    rsa.fill_in()

#continue = "EtudiantSalarie",



#print html_page
#
#print etree.tostring(form_element)



