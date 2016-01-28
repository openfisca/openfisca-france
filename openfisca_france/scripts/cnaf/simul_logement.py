# coding: utf-8

from formulaires_caf import Question, Page, Formulaire
url = "http://www.caf.fr/redirect/s/Redirect?page=aidesEtServicesSimuLogement"

conditions = Question('conditionsSimuLog', ["true"])
BCCommencer = Question("BCCommencer", ["Commencer"])
BCContinuer = Question("BCContinuer", ["Continuer"])
page0 = Page([conditions, BCCommencer])

CODEPOS = Question("CODEPOS", 'int')  # TODO:
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
    exemple = ["FranceMetro",
               'SEUL', "01/06/2003",
               'MON', "01/06/1960", '', '0', '2', '0',
               "EnActivite",
               '0', '0', '0', '0']
    exemple = ['75012',
               'loc', 'false',
               "appartement", 'seul', 'non',
               '500',
               'oui', '01/04/1980', '05/03/1975', 'non', 'non', '2', '0',
               'oui', 'oui',
               'chomage_imposable',
               'sup2m', 'ass']


    logement.set_choice(exemple)
    logement.fill_in()

#for sitPro in rsaSitPro.possible_choices:
#    exemple[-1] = sitPro
#    rsa.set_choice(exemple)
#    print('********* ' + sitPro)
#    rsa.fill_in()

#continue = "EtudiantSalarie",



#print html_page
#
#print etree.tostring(form_element)



