# -*- coding: utf-8 -*-

from ...base import *  # noqa


# Dons à des organismes établis en France
class f7ud(Variable):
    cerfa_field = u"7UD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dons à des organismes d'aide aux personnes en difficulté"



class f7uf(Variable):
    cerfa_field = u"7UF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général"

 # début/fin ?

class f7xs(Variable):
    cerfa_field = u"7XS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5"



class f7xt(Variable):
    cerfa_field = u"7XT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4"



class f7xu(Variable):
    cerfa_field = u"7XU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3"
    start_date = date(2006, 1, 1)



class f7xw(Variable):
    cerfa_field = u"7XW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2"
    start_date = date(2007, 1, 1)



class f7xy(Variable):
    cerfa_field = u"7XY"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1"
    start_date = date(2008, 1, 1)



class f7va(Variable):
    cerfa_field = u"7VA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dons à des organismes d'aides aux personnes établis dans un Etat européen"
    start_date = date(2011, 1, 1)



class f7vc(Variable):
    cerfa_field = u"7VC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dons à des autres organismes établis dans un Etat européen"
    start_date = date(2011, 1, 1)

  # f7va, f7vc 2011 ou 2013 ?

# Cotisations syndicales des salariées et pensionnés
class f7ac(Variable):
    cerfa_field = {QUIFOY['vous']: u"7AC",
        QUIFOY['conj']: u"7AE",
        QUIFOY['pac1']: u"7AG",
        }
    column = IntCol(val_type = "monetary")
    entity_class = Individus
    label = u"Cotisations syndicales des salariées et pensionnés"
    start_date = date(2013, 1, 1)

  # f7ac, f7ae, f7ag

# Salarié à domicile
class f7db(Variable):
    cerfa_field = u"7DB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés"
    start_date = date(2007, 1, 1)



class f7df(Variable):
    cerfa_field = u"7DF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés"



class f7dq(Variable):
    cerfa_field = u"7DQ"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés"
    start_date = date(2009, 1, 1)



class f7dg(Variable):
    cerfa_field = u"7DG"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés"



class f7dl(Variable):
    cerfa_field = u"7DL"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés"



# Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
class f7uh_2007(Variable):
    cerfa_field = u"7UH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêts payés la première année de remboursement du prêt pour l'habitation principale"
    start_date = date(2007, 1, 1)
    stop_date = date(2007, 12, 31)



class f7vy(Variable):
    cerfa_field = u"7VY"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité"
    start_date = date(2008, 1, 1)



class f7vz(Variable):
    cerfa_field = u"7VZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes"
    start_date = date(2008, 1, 1)



class f7vx(Variable):
    cerfa_field = u"7VX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011"



class f7vw(Variable):
    cerfa_field = u"7VW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité"
    start_date = date(2010, 1, 1)



class f7vv(Variable):
    cerfa_field = u"7VV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes"
    start_date = date(2011, 1, 1)

  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

class f7vu(Variable):
    cerfa_field = u"7VU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité"
    start_date = date(2011, 1, 1)

  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

class f7vt(Variable):
    cerfa_field = u"7VT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes"
    start_date = date(2012, 1, 1)

  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

# Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
class f7cd(Variable):
    cerfa_field = u"7CD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne"



class f7ce(Variable):
    cerfa_field = u"7CE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne"



# Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus
class f7ga(Variable):
    cerfa_field = u"7GA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge"



class f7gb(Variable):
    cerfa_field = u"7GB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge"



class f7gc(Variable):
    cerfa_field = u"7GC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge"



class f7ge(Variable):
    cerfa_field = u"7GE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée"



class f7gf(Variable):
    cerfa_field = u"7GF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée"



class f7gg(Variable):
    cerfa_field = u"7GG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée"



# Nombre d'enfants à charge poursuivant leurs études
class f7ea(Variable):
    cerfa_field = u"7EA"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge poursuivant leurs études au collège"



class f7eb(Variable):
    cerfa_field = u"7EB"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège"



class f7ec(Variable):
    cerfa_field = u"7EC"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge poursuivant leurs études au lycée"



class f7ed(Variable):
    cerfa_field = u"7ED"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée"



class f7ef(Variable):
    cerfa_field = u"7EF"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur"



class f7eg(Variable):
    cerfa_field = u"7EG"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur"



# Intérêts des prêts étudiants
class f7td(Variable):
    cerfa_field = u"7TD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés"
    start_date = date(2008, 1, 1)



class f7vo(Variable):
    cerfa_field = u"7VO"
    column = PeriodSizeIndependentIntCol
    entity_class = FoyersFiscaux
    label = u"Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés"
    start_date = date(2006, 1, 1)



class f7uk(Variable):
    cerfa_field = u"7UK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés"



# Primes de rente survie, contrats d'épargne handicap
class f7gz(Variable):
    cerfa_field = u"7GZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Primes de rente survie, contrats d'épargne handicap"



# Prestations compensatoires
class f7wm(Variable):
    cerfa_field = u"7WM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Prestations compensatoires: Capital fixé en substitution de rente"



class f7wn(Variable):
    cerfa_field = u"7WN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés"



class f7wo(Variable):
    cerfa_field = u"7WO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué"



class f7wp(Variable):
    cerfa_field = u"7WP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1"



# Dépenses en faveur de la qualité environnementale de l'habitation principale
class f7we(Variable):
    cerfa_field = u"7WE"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés"
    start_date = date(2009, 1, 1)



class f7wg(Variable):
    cerfa_field = u"7WG"
    column = BoolCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1"
    start_date = date(2012, 1, 1)



class f7wa(Variable):
    cerfa_field = u"7WA"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs avant le 03/04/2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7wb(Variable):
    cerfa_field = u"7WB"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs à compter du 04/04/2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7wc(Variable):
    cerfa_field = u"7WC"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique sur plus de la moitié de la surface des murs extérieurs"
    start_date = date(2012, 1, 1)



class f7ve(Variable):
    cerfa_field = u"7VE"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture avant le 04/04/2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7vf(Variable):
    cerfa_field = u"7VF"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture à compter du 04/04/2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7vg(Variable):
    cerfa_field = u"7VG"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de toute la toiture"
    start_date = date(2012, 1, 1)



class f7sg(Variable):
    cerfa_field = u"7SG"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des murs (acquisitionn et pose)"
    start_date = date(2012, 1, 1)



class f7sj(Variable):
    cerfa_field = u"7SJ"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des parois vitrées"
    start_date = date(2012, 1, 1)



class f7sk(Variable):
    cerfa_field = u"7SK"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Volets isolants"
    start_date = date(2012, 1, 1)



class f7sl(Variable):
    cerfa_field = u"7SL"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Portes d'entrées donnant sur l'extérieur"
    start_date = date(2012, 1, 1)



class f7sm(Variable):
    cerfa_field = u"7SM"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de production d'électricité utilisant l'énergie radiative du soleil"
    start_date = date(2012, 1, 1)



class f7sn(Variable):
    cerfa_field = u"7SN"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent"
    start_date = date(2012, 1, 1)



class f7so(Variable):
    cerfa_field = u"7SO"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent"
    start_date = date(2012, 1, 1)



class f7sp(Variable):
    cerfa_field = u"7SP"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur"
    start_date = date(2012, 1, 1)



class f7sq(Variable):
    cerfa_field = u"7SQ"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur"
    start_date = date(2012, 1, 1)



class f7sr(Variable):
    cerfa_field = u"7SR"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques)"
    start_date = date(2012, 1, 1)



class f7ss(Variable):
    cerfa_field = u"7SS"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires"
    start_date = date(2012, 1, 1)



class f7st(Variable):
    cerfa_field = u"7ST"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (éolien, hydraulique)"
    start_date = date(2012, 1, 1)



class f7su(Variable):
    cerfa_field = u"7SU"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de récupération et de traitement des eaux pluviales"
    start_date = date(2012, 1, 1)



class f7sv(Variable):
    cerfa_field = u"7SV"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Diagnostic de performance énergétique"
    start_date = date(2012, 1, 1)



class f7sw(Variable):
    cerfa_field = u"7SW"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de raccordement à un réseau de chaleur"
    start_date = date(2012, 1, 1)



              # TODO, nouvelle variable à intégrer dans OF (cf ancien nom déjà utilisé)
                                # TODO vérifier pour les années précédentes
# TODO: CHECK
# Intérêts d'emprunts
#     build_column('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary", cerfa_field = u'7')) # cf pour quelle année
#
class f7wq(Variable):
    cerfa_field = u"7WQ"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées du 01/01/2012 au 03/04/2012"
    start_date = date(2010, 1, 1)
    stop_date = date(2012, 12, 31)



class f7ws(Variable):
    cerfa_field = u"7WS"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolations des parois vitrées à compter du 04/04/2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7wt(Variable):
    cerfa_field = u"7WT"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement "
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7wu(Variable):
    cerfa_field = u"7WU"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets avant 2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7wv(Variable):
    cerfa_field = u"7WV"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets en 2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7ww(Variable):
    cerfa_field = u"7WW"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes avant 2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7wx(Variable):
    cerfa_field = u"7WX"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes en 2012"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7wh(Variable):
    cerfa_field = u"7WH"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus"
    start_date = date(2013, 1, 1)



class f7wk(Variable):
    cerfa_field = u"7WK"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Votre habitation principale est une maison individuelle"
    start_date = date(2009, 1, 1)



class f7wf(Variable):
    cerfa_field = u"7WF"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1"
    stop_date = date(2013, 12, 31)



# Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
class f7wi(Variable):
    cerfa_field = u"7WI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction"
    stop_date = date(2012, 12, 31)



class f7wj(Variable):
    cerfa_field = u"7WJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées"



class f7wl(Variable):
    cerfa_field = u"7WL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques"
    start_date = date(2010, 1, 1)



class f7wr(Variable):
    cerfa_field = u"7WR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans des habitations données en location : travaux de prévention des risques technologiques"
    start_date = date(2013, 1, 1)



# Investissements dans les DOM-TOM dans le cadre d'une entrepise
class f7ur(Variable):
    cerfa_field = u"7UR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements réalisés en n-1, total réduction d’impôt"
    stop_date = date(2008, 12, 31)



class f7oz(Variable):
    cerfa_field = u"7OZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6"
    stop_date = date(2011, 12, 31)

  # TODO: vérifier les années antérieures

class f7pz(Variable):
    cerfa_field = u"7PZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures"
    stop_date = date(2013, 12, 31)



class f7qz(Variable):
    cerfa_field = u"7QZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures"
    stop_date = date(2012, 12, 31)



class f7rz(Variable):
    cerfa_field = u"7RZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3"
    stop_date = date(2010, 12, 31)



class f7qv(Variable):
    cerfa_field = u"7QV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010, nvestissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%"
    stop_date = date(2011, 12, 31)



class f7qo(Variable):
    cerfa_field = u"7QO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 50%"
    stop_date = date(2009, 12, 31)



class f7qp(Variable):
    cerfa_field = u"7QP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 60%"
    stop_date = date(2009, 12, 31)



class f7pa(Variable):
    cerfa_field = u"7PA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%"
    stop_date = date(2011, 12, 31)



class f7pb(Variable):
    cerfa_field = u"7PB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%"
    stop_date = date(2011, 12, 31)



class f7pc(Variable):
    cerfa_field = u"7PC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée"
    stop_date = date(2011, 12, 31)



class f7pd(Variable):
    cerfa_field = u"7PD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011"
    stop_date = date(2011, 12, 31)



class f7qe(Variable):
    cerfa_field = u"7QE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet avant 1.1.2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%"
    stop_date = date(2009, 12, 31)



class f7pe(Variable):
    cerfa_field = u"7PE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%"
    stop_date = date(2011, 12, 31)



class f7pf(Variable):
    cerfa_field = u"7PF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%"
    stop_date = date(2011, 12, 31)



class f7pg(Variable):
    cerfa_field = u"7PG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée"
    stop_date = date(2011, 12, 31)



class f7ph(Variable):
    cerfa_field = u"7PH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011"
    stop_date = date(2011, 12, 31)



class f7pi(Variable):
    cerfa_field = u"7PI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%"
    stop_date = date(2011, 12, 31)



class f7pj(Variable):
    cerfa_field = u"7PJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%"
    stop_date = date(2011, 12, 31)



class f7pk(Variable):
    cerfa_field = u"7PK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt calculée"
    stop_date = date(2011, 12, 31)



class f7pl(Variable):
    cerfa_field = u"7PL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011"
    stop_date = date(2011, 12, 31)



class f7pm(Variable):
    cerfa_field = u"7PM"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%"
    stop_date = date(2013, 12, 31)



class f7pn(Variable):
    cerfa_field = u"7PN"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %"
    stop_date = date(2013, 12, 31)



class f7po(Variable):
    cerfa_field = u"7PO"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %"
    stop_date = date(2013, 12, 31)



class f7pp(Variable):
    cerfa_field = u"7PP"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise"
    stop_date = date(2013, 12, 31)



class f7pq(Variable):
    cerfa_field = u"7PQ"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    stop_date = date(2013, 12, 31)



class f7pr(Variable):
    cerfa_field = u"7PR"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    stop_date = date(2013, 12, 31)



class f7ps(Variable):
    cerfa_field = u"7PS"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %"
    stop_date = date(2013, 12, 31)



class f7pt(Variable):
    cerfa_field = u"7PT"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %"
    stop_date = date(2013, 12, 31)



class f7pu(Variable):
    cerfa_field = u"7PU"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise"
    stop_date = date(2013, 12, 31)



class f7pv(Variable):
    cerfa_field = u"7PV"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    stop_date = date(2013, 12, 31)



class f7pw(Variable):
    cerfa_field = u"7PW"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    stop_date = date(2013, 12, 31)



class f7px(Variable):
    cerfa_field = u"7PX"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt  à hauteur de 52,63 %"
    stop_date = date(2013, 12, 31)



class f7py(Variable):
    cerfa_field = u"7PY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
    start_date = date(2012, 1, 1)



class f7rg(Variable):
    cerfa_field = u"7RG"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise"
    start_date = date(2012, 1, 1)



class f7rh(Variable):
    cerfa_field = u"7RH"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    start_date = date(2012, 1, 1)



class f7ri(Variable):
    cerfa_field = u"7RI"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    start_date = date(2012, 1, 1)



class f7rj(Variable):
    cerfa_field = u"7RJ"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %"
    start_date = date(2012, 1, 1)



class f7rk(Variable):
    cerfa_field = u"7RK"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
    start_date = date(2012, 1, 1)



class f7rl(Variable):
    cerfa_field = u"7RL"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
    start_date = date(2012, 1, 1)



class f7rm(Variable):
    cerfa_field = u"7RM"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise"
    start_date = date(2012, 1, 1)



class f7rn(Variable):
    cerfa_field = u"7RN"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    start_date = date(2012, 1, 1)



class f7ro(Variable):
    cerfa_field = u"7RO"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    start_date = date(2012, 1, 1)



class f7rp(Variable):
    cerfa_field = u"7RP"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
    start_date = date(2012, 1, 1)



class f7rq(Variable):
    cerfa_field = u"7RQ"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
    start_date = date(2012, 1, 1)



class f7rr(Variable):
    cerfa_field = u"7RR"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise"
    start_date = date(2012, 1, 1)



class f7rs(Variable):
    cerfa_field = u"7RS"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    start_date = date(2012, 1, 1)



class f7rt(Variable):
    cerfa_field = u"7RT"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    start_date = date(2012, 1, 1)



class f7ru(Variable):
    cerfa_field = u"7RU"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
    start_date = date(2012, 1, 1)



class f7rv(Variable):
    cerfa_field = u"7RV"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
    start_date = date(2012, 1, 1)



class f7rw(Variable):
    cerfa_field = u"7RW"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise"
    start_date = date(2012, 1, 1)



class f7rx(Variable):
    cerfa_field = u"7RX"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    start_date = date(2012, 1, 1)



class f7ry(Variable):
    cerfa_field = u"7RY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    start_date = date(2012, 1, 1)



class f7nu(Variable):
    cerfa_field = u"7NU"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
    start_date = date(2012, 1, 1)



class f7nv(Variable):
    cerfa_field = u"7NV"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
    start_date = date(2012, 1, 1)



class f7nw(Variable):
    cerfa_field = u"7NW"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise"
    start_date = date(2012, 1, 1)



class f7nx(Variable):
    cerfa_field = u"7NX"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    start_date = date(2012, 1, 1)



class f7ny(Variable):
    cerfa_field = u"7NY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    start_date = date(2012, 1, 1)

 #TODO: 7N* : end ?

class f7mn(Variable):
    cerfa_field = u"7MN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%"
    start_date = date(2011, 1, 1)
    stop_date = date(2012, 12, 31)



class f7lh(Variable):
    cerfa_field = u"7LH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%"
    stop_date = date(2011, 12, 31)



class f7mb(Variable):
    cerfa_field = u"7MB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%"
    start_date = date(2011, 1, 1)
    stop_date = date(2012, 12, 31)



class f7kt(Variable):
    cerfa_field = u"7KT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt, Investissements dans votre entreprise"
    start_date = date(2011, 1, 1)
    stop_date = date(2012, 12, 31)



class f7li(Variable):
    cerfa_field = u"7LI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%"
    start_date = date(2011, 1, 1)



class f7mc(Variable):
    cerfa_field = u"7MC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%"
    start_date = date(2011, 1, 1)
    stop_date = date(2012, 12, 31)



class f7ku(Variable):
    cerfa_field = u"7KU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements dans votre entreprise"
    start_date = date(2011, 1, 1)
    stop_date = date(2011, 12, 31)



# TODO: 7sz se rapporte à des choses différentes en 2012 et 2013 par rapport aux années précédentes, cf pour les années antérieures

class f7sz(Variable):
    cerfa_field = u"7SZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location"
    start_date = date(2006, 1, 1)



class fhsa(Variable):
    cerfa_field = u"HSA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 52,63%"
    start_date = date(2013, 1, 1)



class fhsb(Variable):
    cerfa_field = u"HSB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 62,5%"
    start_date = date(2013, 1, 1)



class fhsf(Variable):
    cerfa_field = u"HSF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 52,63%"
    start_date = date(2013, 1, 1)



class fhsg(Variable):
    cerfa_field = u"HSG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 62,5%"
    start_date = date(2013, 1, 1)



class fhsc(Variable):
    cerfa_field = u"HSC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2010"
    start_date = date(2013, 1, 1)



class fhsh(Variable):
    cerfa_field = u"HSH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2011"
    start_date = date(2013, 1, 1)



class fhsd(Variable):
    cerfa_field = u"HSD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2010"
    start_date = date(2013, 1, 1)



class fhsi(Variable):
    cerfa_field = u"HSI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2011"
    start_date = date(2013, 1, 1)



class fhse(Variable):
    cerfa_field = u"HSE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010"
    start_date = date(2013, 1, 1)



class fhsj(Variable):
    cerfa_field = u"HSJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011"
    start_date = date(2013, 1, 1)



class fhsk(Variable):
    cerfa_field = u"HSK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 52,63%"
    start_date = date(2013, 1, 1)



class fhsl(Variable):
    cerfa_field = u"HSL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 62,5%"
    start_date = date(2013, 1, 1)



class fhsp(Variable):
    cerfa_field = u"HSP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 52,63%"
    start_date = date(2013, 1, 1)



class fhsq(Variable):
    cerfa_field = u"HSQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 62,5%"
    start_date = date(2013, 1, 1)



class fhsm(Variable):
    cerfa_field = u"HSM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2010"
    start_date = date(2013, 1, 1)



class fhsr(Variable):
    cerfa_field = u"HSR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2011"
    start_date = date(2013, 1, 1)



class fhsn(Variable):
    cerfa_field = u"HSN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2010"
    start_date = date(2013, 1, 1)



class fhss(Variable):
    cerfa_field = u"HSS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2011"
    start_date = date(2013, 1, 1)



class fhso(Variable):
    cerfa_field = u"HSO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010"
    start_date = date(2013, 1, 1)



class fhst(Variable):
    cerfa_field = u"HST"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011"
    start_date = date(2013, 1, 1)



class fhsu(Variable):
    cerfa_field = u"HSU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%"
    start_date = date(2013, 1, 1)



class fhsv(Variable):
    cerfa_field = u"HSV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%"
    start_date = date(2013, 1, 1)



class fhsw(Variable):
    cerfa_field = u"HSW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise"
    start_date = date(2013, 1, 1)



class fhsx(Variable):
    cerfa_field = u"HSX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé"
    start_date = date(2013, 1, 1)



class fhsy(Variable):
    cerfa_field = u"HS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013"
    start_date = date(2013, 1, 1)



class fhsz(Variable):
    cerfa_field = u"HSZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%"
    start_date = date(2013, 1, 1)



class fhta(Variable):
    cerfa_field = u"HTA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%"
    start_date = date(2013, 1, 1)



class fhtb(Variable):
    cerfa_field = u"HTB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise"
    start_date = date(2013, 1, 1)



class fhtc(Variable):
    cerfa_field = u"HTC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé"
    start_date = date(2013, 1, 1)



class fhtd(Variable):
    cerfa_field = u"HTD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013"
    start_date = date(2013, 1, 1)



# Aide aux créateurs et repreneurs d'entreprises
class f7fy(Variable):
    cerfa_field = u"7FY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1"
    stop_date = date(2011, 12, 31)



class f7gy(Variable):
    cerfa_field = u"7GY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1"
    start_date = date(2006, 1, 1)
    stop_date = date(2011, 12, 31)



class f7hy(Variable):
    cerfa_field = u"7HY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1"
    start_date = date(2009, 1, 1)
    stop_date = date(2011, 12, 31)



class f7ky(Variable):
    cerfa_field = u"7KY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1"
    start_date = date(2009, 1, 1)
    stop_date = date(2011, 12, 31)



class f7iy(Variable):
    cerfa_field = u"7IY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés"
    start_date = date(2013, 1, 1)



class f7ly(Variable):
    cerfa_field = u"7LY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés"
    start_date = date(2010, 1, 1)

  # 2012 et 2013 ok

class f7my(Variable):
    cerfa_field = u"7MY"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés"
    start_date = date(2010, 1, 1)

  # 2012 et 2013 ok

# Travaux de restauration immobilière
class f7ra(Variable):
    cerfa_field = u"7RA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager"
    start_date = date(2009, 1, 1)

  # 2012 et 2013 ok

class f7rb(Variable):
    cerfa_field = u"7RB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
    start_date = date(2009, 1, 1)



class f7rc(Variable):
    cerfa_field = u"7RC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
    start_date = date(2011, 1, 1)



class f7rd(Variable):
    cerfa_field = u"7RD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
    start_date = date(2011, 1, 1)



class f7re(Variable):
    cerfa_field = u"7RE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
    start_date = date(2012, 1, 1)



class f7rf(Variable):
    cerfa_field = u"7RF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
    start_date = date(2012, 1, 1)



class f7sx(Variable):
    cerfa_field = u"7SX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
    start_date = date(2013, 1, 1)



class f7sy(Variable):
    cerfa_field = u"7SY"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
    start_date = date(2013, 1, 1)

 # 2012 et 2013 ok

class f7gw(Variable):
    cerfa_field = u"7GW"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt"
    start_date = date(2013, 1, 1)



class f7gx(Variable):
    cerfa_field = u"7GX"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt"
    start_date = date(2013, 1, 1)



# Investissements locatifs dans le secteur de touristique
class f7xa(Variable):
    cerfa_field = u"7XA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans un village résidentiel de tourisme"
    start_date = date(2011, 1, 1)
    stop_date = date(2012, 12, 31)



class f7xb(Variable):
    cerfa_field = u"7XB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans une résidence de tourisme classée ou meublée"
    start_date = date(2011, 1, 1)
    stop_date = date(2012, 12, 31)



class f7xc(Variable):
    cerfa_field = u"7XC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1"
    stop_date = date(2012, 12, 31)



class f7xd(Variable):
    cerfa_field = u"7XD"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans"
    start_date = date(2009, 1, 1)
    stop_date = date(2012, 12, 31)



class f7xe(Variable):
    cerfa_field = u"7XE"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans"
    start_date = date(2009, 1, 1)
    stop_date = date(2012, 12, 31)



class f7xf(Variable):
    cerfa_field = u"7XF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures"



class f7xh(Variable):
    cerfa_field = u"7XH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme"
    stop_date = date(2012, 12, 31)



class f7xi(Variable):
    cerfa_field = u"7XI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures"
    start_date = date(2010, 1, 1)



class f7xj(Variable):
    cerfa_field = u"7XJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures"
    start_date = date(2010, 1, 1)



class f7xk(Variable):
    cerfa_field = u"7XK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
    start_date = date(2010, 1, 1)



class f7xl(Variable):
    cerfa_field = u"7XL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans"
    stop_date = date(2012, 12, 31)



class f7xm(Variable):
    cerfa_field = u"7XM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures"



# TODO: f7xn cf années < à 2011 (possible erreur dans le label pour ces dates, à vérifier)
class f7xn(Variable):
    cerfa_field = u"7XN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures"
    start_date = date(2012, 1, 1)



class f7xo(Variable):
    cerfa_field = u"7XO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
    start_date = date(2008, 1, 1)



class f7xp(Variable):
    cerfa_field = u"7XP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
    start_date = date(2011, 1, 1)



class f7xq(Variable):
    cerfa_field = u"7XQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
    start_date = date(2011, 1, 1)



class f7xr(Variable):
    cerfa_field = u"7XR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
    start_date = date(2011, 1, 1)



class f7xv(Variable):
    cerfa_field = u"7XV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures"
    start_date = date(2012, 1, 1)



class f7xx(Variable):
    cerfa_field = u"7XX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans un village résidentiel de tourisme"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7xz(Variable):
    cerfa_field = u"7XZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans une résidence de tourisme classée ou un meublé tourisme"
    start_date = date(2012, 1, 1)



class f7uy(Variable):
    cerfa_field = u"7UY"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures"
    start_date = date(2013, 1, 1)



class f7uz(Variable):
    cerfa_field = u"7UZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures"
    start_date = date(2013, 1, 1)



# Souscriptions au capital des PME
class f7cf(Variable):
    cerfa_field = u"7CF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion"



class f7cl(Variable):
    cerfa_field = u"7CL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4"



class f7cm(Variable):
    cerfa_field = u"7CM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3"



class f7cn(Variable):
    cerfa_field = u"7CN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2"



class f7cc(Variable):
    cerfa_field = u"7CC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1"
    start_date = date(2013, 1, 1)



class f7cq(Variable):
    cerfa_field = u"7CQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1pour les start-up"
    start_date = date(2011, 1, 1)



class f7cu(Variable):
    cerfa_field = u"7CU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures"



# TODO: en 2013 et 2012 plus de sofipêche (pourtant présent dans param à ces dates...), case 7gs réutilisée

class f7gs(Variable):
    cerfa_field = u"7GS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2013, 1, 1)



# Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
class f7ua(Variable):
    cerfa_field = u"7UA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2007, 12, 31)


class f7ub(Variable):
    cerfa_field = u"7UB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2007, 12, 31)



# En 2013 les "7" sont remplacés par des "H" dans les CERFA-FIELDS
# en 2013 et 2012, 7uc se rapporte à autre chose, réutilisation de la case
#    build_column('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UC', end = date(2011,12,31)))  # vérifier <=2011

class f7uc(Variable):
    cerfa_field = u"7UC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Cotisations pour la défense des forêts contre l'incendie "



class f7ui(Variable):
    cerfa_field = u"7UI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2008, 12, 31)


class f7uj(Variable):
    cerfa_field = u"7UJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2007, 12, 31)


class f7qb(Variable):
    cerfa_field = u"7QB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2011, 12, 31)


class f7qc(Variable):
    cerfa_field = u"7QC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2011, 12, 31)


class f7qd(Variable):
    cerfa_field = u"7QD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2011, 12, 31)


class f7qk(Variable):
    cerfa_field = u"7QK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2009, 12, 31)


class f7qn(Variable):
    cerfa_field = u"7QN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2010, 12, 31)


class f7kg(Variable):
    cerfa_field = u"7KG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2010, 12, 31)


class f7ql(Variable):
    cerfa_field = u"7QL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2011, 12, 31)


class f7qt(Variable):
    cerfa_field = u"7QT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2011, 12, 31)


class f7qm(Variable):
    cerfa_field = u"7QM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    stop_date = date(2011, 12, 31)


class f7qu(Variable):
    cerfa_field = u"7QU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7ki(Variable):
    cerfa_field = u"7KI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qj(Variable):
    cerfa_field = u"7QJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qw(Variable):
    cerfa_field = u"7QW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qx(Variable):
    cerfa_field = u"7QX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qf(Variable):
    cerfa_field = u"7QF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qg(Variable):
    cerfa_field = u"7QG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qh(Variable):
    cerfa_field = u"7QH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qi(Variable):
    cerfa_field = u"7QI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qq(Variable):
    cerfa_field = u"7QQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qr(Variable):
    cerfa_field = u"7QR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7qs(Variable):
    cerfa_field = u"7QS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7mm(Variable):
    cerfa_field = u"7MM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    start_date = date(2010, 1, 1)
    stop_date = date(2012, 12, 31)


class f7lg(Variable):
    cerfa_field = u"7LG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    start_date = date(2010, 1, 1)


class f7ma(Variable):
    cerfa_field = u"7MA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    start_date = date(2010, 1, 1)


class f7ks(Variable):
    cerfa_field = u"7KS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux


class f7kh(Variable):
    cerfa_field = u"7KH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux



class f7oa(Variable):
    cerfa_field = u"7OA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009"
    start_date = date(2011, 1, 1)



class f7ob(Variable):
    cerfa_field = u"7OB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009"
    start_date = date(2011, 1, 1)



class f7oc(Variable):
    cerfa_field = u"7OC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010"
    start_date = date(2011, 1, 1)



class f7oh(Variable):
    cerfa_field = u"7OH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009"
    start_date = date(2011, 1, 1)



class f7oi(Variable):
    cerfa_field = u"7OI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009"
    start_date = date(2011, 1, 1)



class f7oj(Variable):
    cerfa_field = u"7OJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010"
    start_date = date(2011, 1, 1)



class f7ok(Variable):
    cerfa_field = u"7OK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Autres investissements"
    start_date = date(2011, 1, 1)



class f7ol(Variable):
    cerfa_field = u"7OL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009"
    start_date = date(2012, 1, 1)



class f7om(Variable):
    cerfa_field = u"7OM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009"
    start_date = date(2012, 1, 1)



class f7on(Variable):
    cerfa_field = u"7ON"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
    start_date = date(2012, 1, 1)



class f7oo(Variable):
    cerfa_field = u"7OO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009"
    start_date = date(2012, 1, 1)



class f7op(Variable):
    cerfa_field = u"7OP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009"
    start_date = date(2012, 1, 1)



class f7oq(Variable):
    cerfa_field = u"7OQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
    start_date = date(2012, 1, 1)



class f7or(Variable):
    cerfa_field = u"7OR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
    start_date = date(2012, 1, 1)



class f7os(Variable):
    cerfa_field = u"7OS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009"
    start_date = date(2012, 1, 1)



class f7ot(Variable):
    cerfa_field = u"7OT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009"
    start_date = date(2012, 1, 1)



class f7ou(Variable):
    cerfa_field = u"7OU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
    start_date = date(2012, 1, 1)



class f7ov(Variable):
    cerfa_field = u"7OV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
    start_date = date(2012, 1, 1)



class f7ow(Variable):
    cerfa_field = u"7OW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, "
    start_date = date(2012, 1, 1)

 #TODO: 7O* : end ?

class fhod(Variable):
    cerfa_field = u"HOD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés avant le 1.1.2011"
    start_date = date(2013, 1, 1)



class fhoe(Variable):
    cerfa_field = u"HOE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
    start_date = date(2013, 1, 1)



class fhof(Variable):
    cerfa_field = u"HOF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
    start_date = date(2013, 1, 1)




class fhog(Variable):
    cerfa_field = u"HOG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010"
    start_date = date(2013, 1, 1)




class fhox(Variable):
    cerfa_field = u"HOX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2011"
    start_date = date(2013, 1, 1)




class fhoy(Variable):
    cerfa_field = u"HOY"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2012"
    start_date = date(2013, 1, 1)




class fhoz(Variable):
    cerfa_field = u"HOZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Autres investissements"
    start_date = date(2013, 1, 1)



# Investissements outre-mer dans le logement social

class fhra(Variable):
    cerfa_field = u"HRA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
    start_date = date(2013, 1, 1)



class fhrb(Variable):
    cerfa_field = u"HRB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
    start_date = date(2013, 1, 1)



class fhrc(Variable):
    cerfa_field = u"HRC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2012"
    start_date = date(2013, 1, 1)



class fhrd(Variable):
    cerfa_field = u"HRD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Autres investissements"
    start_date = date(2013, 1, 1)



# Souscription de parts de fonds communs de placement dans l'innovation,
# de fonds d'investissement de proximité
class f7gq(Variable):
    cerfa_field = u"7GQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscription de parts de fonds communs de placement dans l'innovation"



class f7fq(Variable):
    cerfa_field = u"7FQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscription de parts de fonds d'investissement de proximité"



class f7fm(Variable):
    cerfa_field = u"7FM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse"
    start_date = date(2007, 1, 1)



class f7fl(Variable):
    cerfa_field = u"7FL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer"
    start_date = date(2011, 1, 1)



# Souscriptions au capital de SOFICA
class f7gn(Variable):
    cerfa_field = u"7GN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital de SOFICA 36 %"
    start_date = date(2006, 1, 1)



class f7fn(Variable):
    cerfa_field = u"7FN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Souscriptions au capital de SOFICA 30 %"
    start_date = date(2006, 1, 1)



# Intérêts d'emprunt pour reprise de société
class f7fh(Variable):
    cerfa_field = u"7FH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêts d'emprunt pour reprise de société"



# Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée))
class f7ff(Variable):
    cerfa_field = u"7FF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)"



class f7fg(Variable):
    cerfa_field = u"7FG"
    column = IntCol
    entity_class = FoyersFiscaux
    label = u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations"



# Travaux de conservation et de restauration d’objets classés monuments historiques
class f7nz(Variable):
    cerfa_field = u"7NZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Travaux de conservation et de restauration d’objets classés monuments historiques"
    start_date = date(2008, 1, 1)



# Dépenses de protection du patrimoine naturel
class f7ka(Variable):
    cerfa_field = u"7KA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de protection du patrimoine naturel"
    start_date = date(2010, 1, 1)



class f7kb(Variable):
    cerfa_field = u"7KB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)"
    start_date = date(2011, 1, 1)



class f7kc(Variable):
    cerfa_field = u"7KC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)"
    start_date = date(2012, 1, 1)



class f7kd(Variable):
    cerfa_field = u"7KD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)"
    start_date = date(2013, 1, 1)



class f7uh(Variable):
    cerfa_field = u"7UH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dons et cotisations versés aux partis politiques"
    start_date = date(2007, 1, 1)

 #TODO: séparer en plusieurs variables (même case pour plusieurs variables selon les années)

# Investissements forestiers
class f7un(Variable):
    cerfa_field = u"7UN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers: acquisition"



class f7ul(Variable):
    cerfa_field = u"7UL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2011, 1, 1)



class f7uu(Variable):
    cerfa_field = u"7UU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2010, 1, 1)



class f7uv(Variable):
    cerfa_field = u"7UV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2011, 1, 1)



class f7uw(Variable):
    cerfa_field = u"7UW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2012, 1, 1)



class f7th(Variable):
    cerfa_field = u"7TH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2013, 1, 1)



class f7ux(Variable):
    cerfa_field = u"7UX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2013, 1, 1)



class f7tg(Variable):
    cerfa_field = u"7TG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2012, 1, 1)



class f7tf(Variable):
    cerfa_field = u"7TF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2011, 1, 1)
    stop_date = date(2013, 12, 31)



class f7ut(Variable):
    cerfa_field = u"7UT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements forestiers"
    start_date = date(2009, 1, 1)



# Intérêts pour paiement différé accordé aux agriculteurs
class f7um(Variable):
    cerfa_field = u"7UM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Intérêts pour paiement différé accordé aux agriculteurs"



# Investissements locatifs neufs : Dispositif Scellier:
class f7hj(Variable):
    cerfa_field = u"7HJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole"
    start_date = date(2009, 1, 1)



class f7hk(Variable):
    cerfa_field = u"7HK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM"
    start_date = date(2009, 1, 1)



class f7hn(Variable):
    cerfa_field = u"7HN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010"
    start_date = date(2010, 1, 1)



class f7ho(Variable):
    cerfa_field = u"7HO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010"
    start_date = date(2010, 1, 1)



class f7hl(Variable):
    cerfa_field = u"7HL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)"
    start_date = date(2010, 1, 1)



class f7hm(Variable):
    cerfa_field = u"7HM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds"
    start_date = date(2010, 1, 1)



class f7hr(Variable):
    cerfa_field = u"7HR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques"
    start_date = date(2010, 1, 1)



class f7hs(Variable):
    cerfa_field = u"7HS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques"
    start_date = date(2010, 1, 1)



class f7la(Variable):
    cerfa_field = u"7LA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2009"
    start_date = date(2010, 1, 1)



class f7lb(Variable):
    cerfa_field = u"7LB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2010"
    start_date = date(2011, 1, 1)



class f7lc(Variable):
    cerfa_field = u"7LC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2010"
    start_date = date(2011, 1, 1)



class f7ld(Variable):
    cerfa_field = u"7LD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2011"
    start_date = date(2012, 1, 1)



class f7le(Variable):
    cerfa_field = u"7LE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2011"
    start_date = date(2012, 1, 1)



class f7lf(Variable):
    cerfa_field = u"7LF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011"
    start_date = date(2012, 1, 1)



class f7ls(Variable):
    cerfa_field = u"7LS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010"
    start_date = date(2013, 1, 1)



class f7lm(Variable):
    cerfa_field = u"7LM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010"
    start_date = date(2013, 1, 1)



class f7lz(Variable):
    cerfa_field = u"7LZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Report du solde de réduction d'impôt de l'année 2012"
    start_date = date(2013, 1, 1)



class f7mg(Variable):
    cerfa_field = u"7MG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2012 : report du solde de réduction d'impôt de l'année 2012"
    start_date = date(2013, 1, 1)



class f7na(Variable):
    cerfa_field = u"7NA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, métropole, BBC"
    start_date = date(2011, 1, 1)



class f7nb(Variable):
    cerfa_field = u"7NB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, "
    start_date = date(2011, 1, 1)



class f7nc(Variable):
    cerfa_field = u"7NC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, BBC"
    start_date = date(2011, 1, 1)



class f7nd(Variable):
    cerfa_field = u"7ND"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, BBC"
    start_date = date(2011, 1, 1)



class f7ne(Variable):
    cerfa_field = u"7NE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, BBC"
    start_date = date(2011, 1, 1)



class f7nf(Variable):
    cerfa_field = u"7NF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, "
    start_date = date(2011, 1, 1)



class f7ng(Variable):
    cerfa_field = u"7NG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, "
    start_date = date(2011, 1, 1)



class f7nh(Variable):
    cerfa_field = u"7NH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, non-BBC"
    start_date = date(2011, 1, 1)



class f7ni(Variable):
    cerfa_field = u"7NI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, non-BBC"
    start_date = date(2011, 1, 1)



class f7nj(Variable):
    cerfa_field = u"7NJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, non-BBC"
    start_date = date(2011, 1, 1)



class f7nk(Variable):
    cerfa_field = u"7NK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2011, 1, 1)



class f7nl(Variable):
    cerfa_field = u"7NL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2011, 1, 1)



class f7nm(Variable):
    cerfa_field = u"7NM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2011, 1, 1)



class f7nn(Variable):
    cerfa_field = u"7NN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2011, 1, 1)



class f7no(Variable):
    cerfa_field = u"7NO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2011, 1, 1)



class f7np(Variable):
    cerfa_field = u"7NP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2011, 1, 1)



class f7nq(Variable):
    cerfa_field = u"7NQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2011, 1, 1)



class f7nr(Variable):
    cerfa_field = u"7NR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2011, 1, 1)



class f7ns(Variable):
    cerfa_field = u"7NS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2011, 1, 1)



class f7nt(Variable):
    cerfa_field = u"7NT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2011, 1, 1)



class f7hv(Variable):
    cerfa_field = u"7HV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole"
    start_date = date(2011, 1, 1)



class f7hw(Variable):
    cerfa_field = u"7HW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM"
    start_date = date(2011, 1, 1)



class f7hx(Variable):
    cerfa_field = u"7HX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole avec promesse d'achat avant le 1.1.2010"
    start_date = date(2011, 1, 1)



class f7hz(Variable):
    cerfa_field = u"7HZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM avec promesse d'achat avant le 1.1.2010"
    start_date = date(2011, 1, 1)



class f7ht(Variable):
    cerfa_field = u"7HT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques"
    start_date = date(2011, 1, 1)



class f7hu(Variable):
    cerfa_field = u"7HU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques"
    start_date = date(2011, 1, 1)



class f7ha(Variable):
    cerfa_field = u"7HA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011"
    start_date = date(2012, 1, 1)



class f7hb(Variable):
    cerfa_field = u"7HB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011, avec promesse d'achat en 2010"
    start_date = date(2012, 1, 1)



class f7hg(Variable):
    cerfa_field = u"7HG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna"
    start_date = date(2012, 1, 1)



class f7hh(Variable):
    cerfa_field = u"7HH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna avec promesse d'achat en 2010"
    start_date = date(2012, 1, 1)



class f7hd(Variable):
    cerfa_field = u"7HD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, réalisés en 2010, en métropole et dans les DOM-COM"
    start_date = date(2012, 1, 1)



class f7he(Variable):
    cerfa_field = u"7HE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, en métropole et dans les DOM-COM avec promesse d'achat avant le 1.1.2010"
    start_date = date(2012, 1, 1)



class f7hf(Variable):
    cerfa_field = u"7HF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, Investissements réalisés en 2009 en métropole et dans les DOM-COM"
    start_date = date(2012, 1, 1)



class f7ja(Variable):
    cerfa_field = u"7JA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, BBC"
    start_date = date(2012, 1, 1)



class f7jb(Variable):
    cerfa_field = u"7JB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, BBC"
    start_date = date(2012, 1, 1)



class f7jd(Variable):
    cerfa_field = u"7JD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, BBC"
    start_date = date(2012, 1, 1)



class f7je(Variable):
    cerfa_field = u"7JE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, BBC "
    start_date = date(2012, 1, 1)



class f7jf(Variable):
    cerfa_field = u"7JF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, non-BBC"
    start_date = date(2012, 1, 1)



class f7jg(Variable):
    cerfa_field = u"7JG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, non-BBC"
    start_date = date(2012, 1, 1)



class f7jh(Variable):
    cerfa_field = u"7JH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, non-BBC"
    start_date = date(2012, 1, 1)



class f7jj(Variable):
    cerfa_field = u"7JJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, non-BBC"
    start_date = date(2012, 1, 1)



class f7jk(Variable):
    cerfa_field = u"7JK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2012, 1, 1)



class f7jl(Variable):
    cerfa_field = u"7JL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2012, 1, 1)



class f7jm(Variable):
    cerfa_field = u"7JM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2012, 1, 1)



class f7jn(Variable):
    cerfa_field = u"7JN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2012, 1, 1)



class f7jo(Variable):
    cerfa_field = u"7JO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2012, 1, 1)



class f7jp(Variable):
    cerfa_field = u"7JP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2012, 1, 1)



class f7jq(Variable):
    cerfa_field = u"7JQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2012, 1, 1)



class f7jr(Variable):
    cerfa_field = u"7JR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
    start_date = date(2012, 1, 1)



class f7gj(Variable):
    cerfa_field = u"7GJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2013, 1, 1)



class f7gk(Variable):
    cerfa_field = u"7GK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2011"
    start_date = date(2013, 1, 1)



class f7gl(Variable):
    cerfa_field = u"7GL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2013, 1, 1)



class f7gp(Variable):
    cerfa_field = u"7GP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2010s"
    start_date = date(2013, 1, 1)



class f7fa(Variable):
    cerfa_field = u"7FA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, BBC"
    start_date = date(2013, 1, 1)



class f7fb(Variable):
    cerfa_field = u"7FB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, non-BBC"
    start_date = date(2013, 1, 1)



class f7fc(Variable):
    cerfa_field = u"7FC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
    start_date = date(2013, 1, 1)



class f7fd(Variable):
    cerfa_field = u"7FD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna"
    start_date = date(2013, 1, 1)



# Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
class f7ij(Variable):
    cerfa_field = u"7IJ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, engagement de réalisation de l'investissement en 2011"
    start_date = date(2009, 1, 1)



class f7il(Variable):
    cerfa_field = u"7IL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, promesse d'achat en 2010"
    start_date = date(2010, 1, 1)



class f7im(Variable):
    cerfa_field = u"7IM"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2010 et achevés en 2012 avec promesse d'achat en 2009"
    start_date = date(2010, 1, 1)



class f7ik(Variable):
    cerfa_field = u"7IK"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Reports de 1/9 de l'investissement réalisé et achevé en 2009"
    start_date = date(2010, 1, 1)



class f7in(Variable):
    cerfa_field = u"7IN"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.1.2011 au 31.3.2011"
    start_date = date(2011, 1, 1)



class f7iv(Variable):
    cerfa_field = u"7IV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.4.2011 au 31.12.2011"
    start_date = date(2011, 1, 1)



class f7iw(Variable):
    cerfa_field = u"7IW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2012"
    start_date = date(2011, 1, 1)



class f7io(Variable):
    cerfa_field = u"7IO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : "
    start_date = date(2011, 1, 1)



class f7ip(Variable):
    cerfa_field = u"7IP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : "
    start_date = date(2011, 1, 1)



class f7ir(Variable):
    cerfa_field = u"7IR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : "
    start_date = date(2011, 1, 1)



class f7iq(Variable):
    cerfa_field = u"7IQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : "
    start_date = date(2011, 1, 1)



class f7iu(Variable):
    cerfa_field = u"7IU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : "
    start_date = date(2011, 1, 1)



class f7it(Variable):
    cerfa_field = u"7IT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : "
    start_date = date(2011, 1, 1)



class f7is(Variable):
    cerfa_field = u"7IS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Report du solde de réduction d'impôt non encore imputé: année  n-4"
    start_date = date(2010, 1, 1)



class f7ia(Variable):
    cerfa_field = u"7IA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011"
    start_date = date(2012, 1, 1)



class f7ib(Variable):
    cerfa_field = u"7IB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010"
    start_date = date(2012, 1, 1)



class f7ic(Variable):
    cerfa_field = u"7IC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2011 avec promesse d'achat en 2009 ou réalisés en 2009"
    start_date = date(2012, 1, 1)



class f7id(Variable):
    cerfa_field = u"7ID"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Engagement de réalisation de l'investissement en 2012"
    start_date = date(2012, 1, 1)



class f7ie(Variable):
    cerfa_field = u"7IE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Promesse d'achat en 2011"
    start_date = date(2012, 1, 1)



class f7if(Variable):
    cerfa_field = u"7IF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.1.2012 au 31.3.2012, investissement réalisé du 1.1.2012 au 31.3.2012"
    start_date = date(2012, 1, 1)



class f7ig(Variable):
    cerfa_field = u"7IG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.4.2012 au 31.12.2012"
    start_date = date(2012, 1, 1)



class f7ix(Variable):
    cerfa_field = u"7IX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2009; réalisés en 2009 et achevés en 2010; réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report du solde de réduction d'impôt de l'année 2011"
    start_date = date(2012, 1, 1)



class f7ih(Variable):
    cerfa_field = u"7IH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2011"
    start_date = date(2012, 1, 1)



class f7iz(Variable):
    cerfa_field = u"7IZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011"
    start_date = date(2012, 1, 1)



class f7jt(Variable):
    cerfa_field = u"7JT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2013"
    start_date = date(2013, 1, 1)



class f7ju(Variable):
    cerfa_field = u"7JU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2012"
    start_date = date(2013, 1, 1)



class f7jv(Variable):
    cerfa_field = u"7JV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2012"
    start_date = date(2013, 1, 1)



class f7jw(Variable):
    cerfa_field = u"7JW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 ou réalisés en 2012 avec promesse d'achat en 2011"
    start_date = date(2013, 1, 1)



class f7jx(Variable):
    cerfa_field = u"7JX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010"
    start_date = date(2013, 1, 1)



class f7jy(Variable):
    cerfa_field = u"7JY"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2010 avec promesse d'achat en 2009 ou réalisés en 2009"
    start_date = date(2013, 1, 1)



class f7jc(Variable):
    cerfa_field = u"7JC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2012"
    start_date = date(2013, 1, 1)



class f7ji(Variable):
    cerfa_field = u"7JI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d'impôt de l'année 2012"
    start_date = date(2013, 1, 1)



class f7js(Variable):
    cerfa_field = u"7JS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d’impôt de l’année 2012"
    start_date = date(2013, 1, 1)



# Investissements locatifs dans les résidences de tourisme situées dans une zone de
# revitalisation rurale

# """
# réutilisation de cases en 2013
# """

class f7gt(Variable):
    cerfa_field = u"7GT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010"
    start_date = date(2013, 1, 1)

  # vérif <=2012

class f7gu(Variable):
    cerfa_field = u"7GU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009"
    start_date = date(2013, 1, 1)

  # vérif <=2012

class f7gv(Variable):
    cerfa_field = u"7GV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna "
    start_date = date(2013, 1, 1)

  # vérif <=2012

class f7xg(Variable):
    cerfa_field = u"7XG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme"
    stop_date = date(2012, 12, 1)

  # vérif <=2012

# Crédits d'impôts en f7
# Acquisition de biens culturels
class f7uo(Variable):
    cerfa_field = u"7UO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Acquisition de biens culturels"



# Mécénat d'entreprise
class f7us(Variable):
    cerfa_field = u"7US"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Réduction d'impôt mécénat d'entreprise"



# Crédits d’impôt pour dépenses en faveur de la qualité environnementale

class f7sb(Variable):
    cerfa_field = u"7SB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %"
    start_date = date(2009, 1, 1)
    stop_date = date(2011, 12, 31)



class f7sc(Variable):
    cerfa_field = u"7SC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale"
    start_date = date(2009, 1, 1)
    stop_date = date(2009, 12, 1)


# """
# réutilisation de case pour 2013
# """

class f7sd(Variable):
    cerfa_field = u"7SD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation"
    start_date = date(2009, 1, 1)



class f7se(Variable):
    cerfa_field = u"7SE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz"
    start_date = date(2009, 1, 1)



class f7sh(Variable):
    cerfa_field = u"7SH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)"
    start_date = date(2010, 1, 1)


# ('f7wg', IntCol() déjà disponible

# Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???

class f7up(Variable):
    cerfa_field = u"7UP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt pour investissements forestiers: travaux"
    start_date = date(2009, 1, 1)



class f7uq(Variable):
    cerfa_field = u"7UQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt pour investissements forestiers: contrat de gestion"
    start_date = date(2009, 1, 1)



# Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
class f1ar(Variable):
    cerfa_field = u"1AR"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt aide à la mobilité : le déclarant déménage à plus de 200 km pour son emploi"
    stop_date = date(2080, 12, 31)


#TODO: QUIFOY
class f1br(Variable):
    cerfa_field = u"1BR"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt aide à la mobilité : le conjoint déménage à plus de 200 km pour son emploi"
    stop_date = date(2008, 12, 31)



class f1cr(Variable):
    cerfa_field = u"1CR"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt aide à la mobilité : la 1ère personne à charge déménage à plus de 200 km pour son emploi"
    stop_date = date(2008, 12, 31)



class f1dr(Variable):
    cerfa_field = u"1DR"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt aide à la mobilité : la 2è personne à charge déménage à plus de 200 km pour son emploi"
    stop_date = date(2008, 12, 31)



class f1er(Variable):
    cerfa_field = u"1ER"
    column = BoolCol
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt aide à la mobilité : la 3è personne à charge déménage à plus de 200 km pour son emploi"
    stop_date = date(2006, 12, 31)



# Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
class f4tq(Variable):
    cerfa_field = u"4TQ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail"

  # vérif libéllé, en 2013=Montant des loyers courus du 01/01/1998 au 30/09/1998 provenant des immeubles
                                       # pour lesquels la cessation ou l'interruption de la location est intervenue en 2013 et qui ont été
                                       # soumis à la taxe additionnelle au droit de bail

# Crédits d’impôt pour dépenses en faveur de l’aide aux personnes

class f7sf(Variable):
    cerfa_field = u"7SF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit de travaux en faveur d'aides aux personnes pour des logements en location (avant 2012 ) / Appareils de régulation du chauffage, matériaux de calorifugeage (après 2011)"
    start_date = date(2012, 1, 1)



class f7si(Variable):
    cerfa_field = u"7SI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)"
    start_date = date(2012, 1, 1)



class f7te(Variable):
    cerfa_field = u"7TE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses d'investissement forestier"
    start_date = date(2010, 1, 1)



class f7tu(Variable):
    cerfa_field = u"7TU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de travaux dans l'habitation principale"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7tt(Variable):
    cerfa_field = u"7TT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de travaux dans l'habitation principale"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7tv(Variable):
    cerfa_field = u"7TV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de travaux dans l'habitation principale"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7tx(Variable):
    cerfa_field = u"7TX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de travaux dans l'habitation principale"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7ty(Variable):
    cerfa_field = u"7TY"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de travaux dans l'habitation principale"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



class f7tw(Variable):
    cerfa_field = u"7TW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Dépenses de travaux dans l'habitation principale"
    start_date = date(2012, 1, 1)
    stop_date = date(2012, 12, 31)



# Réduction d'impôts sur les investissements locatifs intermédiaires (loi Duflot)

class f7gh(Variable):
    cerfa_field = u"7GH"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs intermédiaires en métropole"
    start_date = date(2013, 1, 1)



class f7gi(Variable):
    cerfa_field = u"7GI"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Investissements locatifs intermédiaires outre-mer"
    start_date = date(2013, 1, 1)




# section 8

class f8tc(Variable):
    cerfa_field = u"8TC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))"
    stop_date = date(2008, 12, 31)



class f8tb(Variable):
    cerfa_field = u"8TB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)"



class f8te(Variable):
    cerfa_field = u"8TE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé"



class f8tf(Variable):
    cerfa_field = u"8TF"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Reprises de réductions ou de crédits d'impôt"



class f8tg(Variable):
    cerfa_field = u"8TG"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédits d'impôt en faveur des entreprises: Investissement en Corse"



class f8tl(Variable):
    cerfa_field = u"8TL"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt compétitivité emploi (CICE), entreprises bénéficiant de la restitution immédiate"



class f8to(Variable):
    cerfa_field = u"8TO"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures"



class f8tp(Variable):
    cerfa_field = u"8TP"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt"



class f8ts(Variable):
    cerfa_field = u"8TS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, crédit d'impôt"
    start_date = date(2012, 1, 1)



class f8uz(Variable):
    cerfa_field = u"8UZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Famille"



class f8uw(Variable):
    cerfa_field = u"8UW"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt compétitivité emploi (CICE), autres entreprises"
    start_date = date(2013, 1, 1)



class f8tz(Variable):
    cerfa_field = u"8TZ"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Apprentissage"



class f8wa(Variable):
    cerfa_field = u"8WA"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Agriculture biologique"



class f8wb(Variable):
    cerfa_field = u"8WB"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Prospection commerciale"



class f8wc__2008(Variable):
    cerfa_field = u"8WC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Nouvelles technologies"
    stop_date = date(2008, 12, 31)



class f8wc(Variable):
    cerfa_field = u"8WC"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Prêts sans intérêt"
    start_date = date(2012, 1, 1)



class f8wd(Variable):
    cerfa_field = u"8WD"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise"
    start_date = date(2006, 1, 1)



class f8we(Variable):
    cerfa_field = u"8WE"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Intéressement"
    start_date = date(2008, 1, 1)



class f8wr(Variable):
    cerfa_field = u"8WR"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Métiers d'art"
    start_date = date(2006, 1, 1)



class f8ws(Variable):
    cerfa_field = u"8WS"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes"
    start_date = date(2006, 1, 1)
    stop_date = date(2009, 12, 31)

  # verif<=2012

class f8wt(Variable):
    cerfa_field = u"8WT"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs"
    start_date = date(2006, 1, 1)



class f8wu(Variable):
    cerfa_field = u"8WU"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Maître restaurateur"
    start_date = date(2006, 1, 1)



class f8wv(Variable):
    cerfa_field = u"8WV"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Débitants de tabac"
    start_date = date(2007, 1, 1)
    stop_date = date(2012, 12, 31)

  # verif<=2012

class f8wx(Variable):
    cerfa_field = u"8WX"
    column = IntCol(val_type = "monetary")
    entity_class = FoyersFiscaux
    label = u"Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise"
    start_date = date(2007, 1, 1)
    stop_date = date(2009, 12, 31)

  # verif<=2012

class elig_creimp_exc_2008(Variable):
    column = IntCol(
        default = 1,
        val_type = "monetary",
        )
    entity_class = FoyersFiscaux
    label = u"Éligibilité au crédit d'impôt exceptionnel sur les revenus 2008"
    start_date = date(2008, 1, 1)
    stop_date = date(2008, 12, 31)



class elig_creimp_jeunes(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Éligible au crédit d'impôt jeunes"
    start_date = date(2005, 1, 1)
    stop_date = date(2008, 1, 1)

 #Sert à savoir si son secteur d'activité permet au jeune de bénéficier du crédit impôts jeunes
