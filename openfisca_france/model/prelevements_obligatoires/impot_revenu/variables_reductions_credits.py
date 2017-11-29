# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa


# Dons à des organismes établis en France
class f7ud(Variable):
    cerfa_field = u"7UD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dons à des organismes d'aide aux personnes en difficulté"
    definition_period = YEAR


class f7uf(Variable):
    cerfa_field = u"7UF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général"
    definition_period = YEAR

 # début/fin ?

class f7xs(Variable):
    cerfa_field = u"7XS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5"
    definition_period = YEAR


class f7xt(Variable):
    cerfa_field = u"7XT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4"
    definition_period = YEAR


class f7xu(Variable):
    cerfa_field = u"7XU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class f7xw(Variable):
    cerfa_field = u"7XW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2"
#    start_date = date(2007, 1, 1)
    definition_period = YEAR


class f7xy(Variable):
    cerfa_field = u"7XY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1"
#    start_date = date(2008, 1, 1)
    definition_period = YEAR


class f7va(Variable):
    cerfa_field = u"7VA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dons à des organismes d'aides aux personnes établis dans un Etat européen"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7vc(Variable):
    cerfa_field = u"7VC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dons à des autres organismes établis dans un Etat européen"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR

  # f7va, f7vc 2011 ou 2013 ?

# Cotisations syndicales des salariées et pensionnés
class f7ac(Variable):
    cerfa_field = {QUIFOY['vous']: u"7AC",
        QUIFOY['conj']: u"7AE",
        QUIFOY['pac1']: u"7AG",
        }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Cotisations syndicales des salariées et pensionnés"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

  # f7ac, f7ae, f7ag

# Salarié à domicile
class f7db(Variable):
    cerfa_field = u"7DB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés"
#    start_date = date(2007, 1, 1)
    definition_period = YEAR


class f7df(Variable):
    cerfa_field = u"7DF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés"
    definition_period = YEAR


class f7dq(Variable):
    cerfa_field = u"7DQ"
    value_type = bool
    entity = FoyerFiscal
    label = u"Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7dg(Variable):
    cerfa_field = u"7DG"
    value_type = bool
    entity = FoyerFiscal
    label = u"Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés"
    definition_period = YEAR


class f7dl(Variable):
    cerfa_field = u"7DL"
    value_type = int
    entity = FoyerFiscal
    label = u"Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés"
    definition_period = YEAR


# Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale
class f7uh_2007(Variable):
    cerfa_field = u"7UH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêts payés la première année de remboursement du prêt pour l'habitation principale"
#    start_date = date(2007, 1, 1)
    end = '2007-12-31'
    definition_period = YEAR


class f7vy(Variable):
    cerfa_field = u"7VY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité"
#    start_date = date(2008, 1, 1)
    definition_period = YEAR


class f7vz(Variable):
    cerfa_field = u"7VZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes"
#    start_date = date(2008, 1, 1)
    definition_period = YEAR


class f7vx(Variable):
    cerfa_field = u"7VX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011"
    definition_period = YEAR


class f7vw(Variable):
    cerfa_field = u"7VW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7vv(Variable):
    cerfa_field = u"7VV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR

  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

class f7vu(Variable):
    cerfa_field = u"7VU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR

  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

class f7vt(Variable):
    cerfa_field = u"7VT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR

  # TODO: variable non présente dans OF, à intégrer partout où c'est nécessaire

# Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
class f7cd(Variable):
    cerfa_field = u"7CD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne"
    definition_period = YEAR


class f7ce(Variable):
    cerfa_field = u"7CE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne"
    definition_period = YEAR


# Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus
class f7ga(Variable):
    cerfa_field = u"7GA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge"
    definition_period = YEAR


class f7gb(Variable):
    cerfa_field = u"7GB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge"
    definition_period = YEAR


class f7gc(Variable):
    cerfa_field = u"7GC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge"
    definition_period = YEAR


class f7ge(Variable):
    cerfa_field = u"7GE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée"
    definition_period = YEAR


class f7gf(Variable):
    cerfa_field = u"7GF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée"
    definition_period = YEAR


class f7gg(Variable):
    cerfa_field = u"7GG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée"
    definition_period = YEAR


# Nombre d'enfants à charge poursuivant leurs études
class f7ea(Variable):
    cerfa_field = u"7EA"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'enfants à charge poursuivant leurs études au collège"
    definition_period = YEAR


class f7eb(Variable):
    cerfa_field = u"7EB"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège"
    definition_period = YEAR


class f7ec(Variable):
    cerfa_field = u"7EC"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'enfants à charge poursuivant leurs études au lycée"
    definition_period = YEAR


class f7ed(Variable):
    cerfa_field = u"7ED"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée"
    definition_period = YEAR


class f7ef(Variable):
    cerfa_field = u"7EF"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur"
    definition_period = YEAR


class f7eg(Variable):
    cerfa_field = u"7EG"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur"
    definition_period = YEAR


# Intérêts des prêts étudiants
class f7td(Variable):
    cerfa_field = u"7TD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés"
#    start_date = date(2008, 1, 1)
    definition_period = YEAR


class f7vo(Variable):
    cerfa_field = u"7VO"
    value_type = int
    is_period_size_independent = True
    entity = FoyerFiscal
    label = u"Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class f7uk(Variable):
    cerfa_field = u"7UK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés"
    definition_period = YEAR


# Primes de rente survie, contrats d'épargne handicap
class f7gz(Variable):
    cerfa_field = u"7GZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Primes de rente survie, contrats d'épargne handicap"
    definition_period = YEAR


# Prestations compensatoires
class f7wm(Variable):
    cerfa_field = u"7WM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Prestations compensatoires: Capital fixé en substitution de rente"
    definition_period = YEAR


class f7wn(Variable):
    cerfa_field = u"7WN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés"
    definition_period = YEAR


class f7wo(Variable):
    cerfa_field = u"7WO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué"
    definition_period = YEAR


class f7wp(Variable):
    cerfa_field = u"7WP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1"
    definition_period = YEAR


# Dépenses en faveur de la qualité environnementale de l'habitation principale
class f7we(Variable):
    cerfa_field = u"7WE"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7wg(Variable):
    cerfa_field = u"7WG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7wa(Variable):
    cerfa_field = u"7WA"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs avant le 03/04/2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7wb(Variable):
    cerfa_field = u"7WB"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs à compter du 04/04/2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7wc(Variable):
    cerfa_field = u"7WC"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique sur plus de la moitié de la surface des murs extérieurs"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ve(Variable):
    cerfa_field = u"7VE"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture avant le 04/04/2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7vf(Variable):
    cerfa_field = u"7VF"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture à compter du 04/04/2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7vg(Variable):
    cerfa_field = u"7VG"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de toute la toiture"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sg(Variable):
    cerfa_field = u"7SG"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des murs (acquisitionn et pose)"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sj(Variable):
    cerfa_field = u"7SJ"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des parois vitrées"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sk(Variable):
    cerfa_field = u"7SK"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Volets isolants"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sl(Variable):
    cerfa_field = u"7SL"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Portes d'entrées donnant sur l'extérieur"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sm(Variable):
    cerfa_field = u"7SM"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de production d'électricité utilisant l'énergie radiative du soleil"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sn(Variable):
    cerfa_field = u"7SN"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7so(Variable):
    cerfa_field = u"7SO"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sp(Variable):
    cerfa_field = u"7SP"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sq(Variable):
    cerfa_field = u"7SQ"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sr(Variable):
    cerfa_field = u"7SR"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques)"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ss(Variable):
    cerfa_field = u"7SS"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7st(Variable):
    cerfa_field = u"7ST"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (éolien, hydraulique)"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7su(Variable):
    cerfa_field = u"7SU"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de récupération et de traitement des eaux pluviales"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sv(Variable):
    cerfa_field = u"7SV"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Diagnostic de performance énergétique"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sw(Variable):
    cerfa_field = u"7SW"
    value_type = int
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de raccordement à un réseau de chaleur"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


              # TODO, nouvelle variable à intégrer dans OF (cf ancien nom déjà utilisé)
                                # TODO vérifier pour les années précédentes
# TODO: CHECK
# Intérêts d'emprunts
#     build_column('f7wg', IntCol(entity = 'foy', label = u"Intérêts d'emprunts", val_type = "monetary", cerfa_field = u'7')) # cf pour quelle année
#
class f7wq(Variable):
    cerfa_field = u"7WQ"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées du 01/01/2012 au 03/04/2012"
#    start_date = date(2010, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7ws(Variable):
    cerfa_field = u"7WS"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolations des parois vitrées à compter du 04/04/2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7wt(Variable):
    cerfa_field = u"7WT"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement "
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7wu(Variable):
    cerfa_field = u"7WU"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets avant 2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7wv(Variable):
    cerfa_field = u"7WV"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets en 2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7ww(Variable):
    cerfa_field = u"7WW"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes avant 2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7wx(Variable):
    cerfa_field = u"7WX"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes en 2012"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7wh(Variable):
    cerfa_field = u"7WH"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7wk(Variable):
    cerfa_field = u"7WK"
    value_type = bool
    entity = FoyerFiscal
    label = u"Votre habitation principale est une maison individuelle"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7wf(Variable):
    cerfa_field = u"7WF"
    value_type = bool
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1"
    end = '2013-12-31'
    definition_period = YEAR


# Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale
class f7wi(Variable):
    cerfa_field = u"7WI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction"
    end = '2012-12-31'
    definition_period = YEAR


class f7wj(Variable):
    cerfa_field = u"7WJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées"
    definition_period = YEAR


class f7wl(Variable):
    cerfa_field = u"7WL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7wr(Variable):
    cerfa_field = u"7WR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de l'aide aux personnes réalisées dans des habitations données en location : travaux de prévention des risques technologiques"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Investissements dans les DOM-TOM dans le cadre d'une entrepise
class f7ur(Variable):
    cerfa_field = u"7UR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements réalisés en n-1, total réduction d’impôt"
    end = '2008-12-31'
    definition_period = YEAR


class f7oz(Variable):
    cerfa_field = u"7OZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6"
    end = '2011-12-31'
    definition_period = YEAR

  # TODO: vérifier les années antérieures

class f7pz(Variable):
    cerfa_field = u"7PZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures"
    end = '2013-12-31'
    definition_period = YEAR


class f7qz(Variable):
    cerfa_field = u"7QZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures"
    end = '2012-12-31'
    definition_period = YEAR


class f7rz(Variable):
    cerfa_field = u"7RZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3"
    end = '2010-12-31'
    definition_period = YEAR


class f7qv(Variable):
    cerfa_field = u"7QV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010, nvestissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%"
    end = '2011-12-31'
    definition_period = YEAR


class f7qo(Variable):
    cerfa_field = u"7QO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 50%"
    end = '2009-12-31'
    definition_period = YEAR


class f7qp(Variable):
    cerfa_field = u"7QP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 60%"
    end = '2009-12-31'
    definition_period = YEAR


class f7pa(Variable):
    cerfa_field = u"7PA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%"
    end = '2011-12-31'
    definition_period = YEAR


class f7pb(Variable):
    cerfa_field = u"7PB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%"
    end = '2011-12-31'
    definition_period = YEAR


class f7pc(Variable):
    cerfa_field = u"7PC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée"
    end = '2011-12-31'
    definition_period = YEAR


class f7pd(Variable):
    cerfa_field = u"7PD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011"
    end = '2011-12-31'
    definition_period = YEAR


class f7qe(Variable):
    cerfa_field = u"7QE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet avant 1.1.2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%"
    end = '2009-12-31'
    definition_period = YEAR


class f7pe(Variable):
    cerfa_field = u"7PE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%"
    end = '2011-12-31'
    definition_period = YEAR


class f7pf(Variable):
    cerfa_field = u"7PF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%"
    end = '2011-12-31'
    definition_period = YEAR


class f7pg(Variable):
    cerfa_field = u"7PG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée"
    end = '2011-12-31'
    definition_period = YEAR


class f7ph(Variable):
    cerfa_field = u"7PH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011"
    end = '2011-12-31'
    definition_period = YEAR


class f7pi(Variable):
    cerfa_field = u"7PI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%"
    end = '2011-12-31'
    definition_period = YEAR


class f7pj(Variable):
    cerfa_field = u"7PJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%"
    end = '2011-12-31'
    definition_period = YEAR


class f7pk(Variable):
    cerfa_field = u"7PK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt calculée"
    end = '2011-12-31'
    definition_period = YEAR


class f7pl(Variable):
    cerfa_field = u"7PL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011"
    end = '2011-12-31'
    definition_period = YEAR


class f7pm(Variable):
    cerfa_field = u"7PM"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%"
    end = '2013-12-31'
    definition_period = YEAR


class f7pn(Variable):
    cerfa_field = u"7PN"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %"
    end = '2013-12-31'
    definition_period = YEAR


class f7po(Variable):
    cerfa_field = u"7PO"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %"
    end = '2013-12-31'
    definition_period = YEAR


class f7pp(Variable):
    cerfa_field = u"7PP"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise"
    end = '2013-12-31'
    definition_period = YEAR


class f7pq(Variable):
    cerfa_field = u"7PQ"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    end = '2013-12-31'
    definition_period = YEAR


class f7pr(Variable):
    cerfa_field = u"7PR"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    end = '2013-12-31'
    definition_period = YEAR


class f7ps(Variable):
    cerfa_field = u"7PS"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %"
    end = '2013-12-31'
    definition_period = YEAR


class f7pt(Variable):
    cerfa_field = u"7PT"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %"
    end = '2013-12-31'
    definition_period = YEAR


class f7pu(Variable):
    cerfa_field = u"7PU"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise"
    end = '2013-12-31'
    definition_period = YEAR


class f7pv(Variable):
    cerfa_field = u"7PV"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
    end = '2013-12-31'
    definition_period = YEAR


class f7pw(Variable):
    cerfa_field = u"7PW"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
    end = '2013-12-31'
    definition_period = YEAR


class f7px(Variable):
    cerfa_field = u"7PX"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt  à hauteur de 52,63 %"
    end = '2013-12-31'
    definition_period = YEAR


class f7py(Variable):
    cerfa_field = u"7PY"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rg(Variable):
    cerfa_field = u"7RG"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rh(Variable):
    cerfa_field = u"7RH"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ri(Variable):
    cerfa_field = u"7RI"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rj(Variable):
    cerfa_field = u"7RJ"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rk(Variable):
    cerfa_field = u"7RK"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rl(Variable):
    cerfa_field = u"7RL"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rm(Variable):
    cerfa_field = u"7RM"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rn(Variable):
    cerfa_field = u"7RN"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ro(Variable):
    cerfa_field = u"7RO"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rp(Variable):
    cerfa_field = u"7RP"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rq(Variable):
    cerfa_field = u"7RQ"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rr(Variable):
    cerfa_field = u"7RR"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rs(Variable):
    cerfa_field = u"7RS"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rt(Variable):
    cerfa_field = u"7RT"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ru(Variable):
    cerfa_field = u"7RU"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rv(Variable):
    cerfa_field = u"7RV"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rw(Variable):
    cerfa_field = u"7RW"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rx(Variable):
    cerfa_field = u"7RX"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ry(Variable):
    cerfa_field = u"7RY"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7nu(Variable):
    cerfa_field = u"7NU"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7nv(Variable):
    cerfa_field = u"7NV"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7nw(Variable):
    cerfa_field = u"7NW"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7nx(Variable):
    cerfa_field = u"7NX"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ny(Variable):
    cerfa_field = u"7NY"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR

 #TODO: 7N* : end ?

class f7mn(Variable):
    cerfa_field = u"7MN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%"
#    start_date = date(2011, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7lh(Variable):
    cerfa_field = u"7LH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%"
    end = '2011-12-31'
    definition_period = YEAR


class f7mb(Variable):
    cerfa_field = u"7MB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%"
#    start_date = date(2011, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7kt(Variable):
    cerfa_field = u"7KT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt, Investissements dans votre entreprise"
#    start_date = date(2011, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7li(Variable):
    cerfa_field = u"7LI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7mc(Variable):
    cerfa_field = u"7MC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%"
#    start_date = date(2011, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7ku(Variable):
    cerfa_field = u"7KU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements dans votre entreprise"
#    start_date = date(2011, 1, 1)
    end = '2011-12-31'
    definition_period = YEAR


# TODO: 7sz se rapporte à des choses différentes en 2012 et 2013 par rapport aux années précédentes, cf pour les années antérieures

class f7sz(Variable):
    cerfa_field = u"7SZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class fhsa(Variable):
    cerfa_field = u"HSA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 52,63%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsb(Variable):
    cerfa_field = u"HSB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 62,5%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsf(Variable):
    cerfa_field = u"HSF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 52,63%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsg(Variable):
    cerfa_field = u"HSG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 62,5%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsc(Variable):
    cerfa_field = u"HSC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsh(Variable):
    cerfa_field = u"HSH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsd(Variable):
    cerfa_field = u"HSD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsi(Variable):
    cerfa_field = u"HSI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhse(Variable):
    cerfa_field = u"HSE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsj(Variable):
    cerfa_field = u"HSJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsk(Variable):
    cerfa_field = u"HSK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 52,63%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsl(Variable):
    cerfa_field = u"HSL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 62,5%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsp(Variable):
    cerfa_field = u"HSP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 52,63%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsq(Variable):
    cerfa_field = u"HSQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 62,5%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsm(Variable):
    cerfa_field = u"HSM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsr(Variable):
    cerfa_field = u"HSR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsn(Variable):
    cerfa_field = u"HSN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhss(Variable):
    cerfa_field = u"HSS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhso(Variable):
    cerfa_field = u"HSO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhst(Variable):
    cerfa_field = u"HST"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsu(Variable):
    cerfa_field = u"HSU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsv(Variable):
    cerfa_field = u"HSV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsw(Variable):
    cerfa_field = u"HSW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsx(Variable):
    cerfa_field = u"HSX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsy(Variable):
    cerfa_field = u"HS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhsz(Variable):
    cerfa_field = u"HSZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhta(Variable):
    cerfa_field = u"HTA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhtb(Variable):
    cerfa_field = u"HTB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhtc(Variable):
    cerfa_field = u"HTC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhtd(Variable):
    cerfa_field = u"HTD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Aide aux créateurs et repreneurs d'entreprises
class f7fy(Variable):
    cerfa_field = u"7FY"
    value_type = int
    entity = FoyerFiscal
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1"
    end = '2011-12-31'
    definition_period = YEAR


class f7gy(Variable):
    cerfa_field = u"7GY"
    value_type = int
    entity = FoyerFiscal
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1"
#    start_date = date(2006, 1, 1)
    end = '2011-12-31'
    definition_period = YEAR


class f7hy(Variable):
    cerfa_field = u"7HY"
    value_type = int
    entity = FoyerFiscal
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1"
#    start_date = date(2009, 1, 1)
    end = '2011-12-31'
    definition_period = YEAR


class f7ky(Variable):
    cerfa_field = u"7KY"
    value_type = int
    entity = FoyerFiscal
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1"
#    start_date = date(2009, 1, 1)
    end = '2011-12-31'
    definition_period = YEAR


class f7iy(Variable):
    cerfa_field = u"7IY"
    value_type = int
    entity = FoyerFiscal
    label = u"Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7ly(Variable):
    cerfa_field = u"7LY"
    value_type = int
    entity = FoyerFiscal
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR

  # 2012 et 2013 ok

class f7my(Variable):
    cerfa_field = u"7MY"
    value_type = int
    entity = FoyerFiscal
    label = u"Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR

  # 2012 et 2013 ok

# Travaux de restauration immobilière
class f7ra(Variable):
    cerfa_field = u"7RA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR

  # 2012 et 2013 ok

class f7rb(Variable):
    cerfa_field = u"7RB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7rc(Variable):
    cerfa_field = u"7RC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7rd(Variable):
    cerfa_field = u"7RD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7re(Variable):
    cerfa_field = u"7RE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7rf(Variable):
    cerfa_field = u"7RF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7sx(Variable):
    cerfa_field = u"7SX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7sy(Variable):
    cerfa_field = u"7SY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

 # 2012 et 2013 ok

class f7gw(Variable):
    cerfa_field = u"7GW"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7gx(Variable):
    cerfa_field = u"7GX"
    value_type = int
    entity = FoyerFiscal
    label = u"Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Investissements locatifs dans le secteur de touristique
class f7xa(Variable):
    cerfa_field = u"7XA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans un village résidentiel de tourisme"
#    start_date = date(2011, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7xb(Variable):
    cerfa_field = u"7XB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans une résidence de tourisme classée ou meublée"
#    start_date = date(2011, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7xc(Variable):
    cerfa_field = u"7XC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1"
    end = '2012-12-31'
    definition_period = YEAR


class f7xd(Variable):
    cerfa_field = u"7XD"
    value_type = bool
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans"
#    start_date = date(2009, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7xe(Variable):
    cerfa_field = u"7XE"
    value_type = bool
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans"
#    start_date = date(2009, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7xf(Variable):
    cerfa_field = u"7XF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures"
    definition_period = YEAR


class f7xh(Variable):
    cerfa_field = u"7XH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme"
    end = '2012-12-31'
    definition_period = YEAR


class f7xi(Variable):
    cerfa_field = u"7XI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7xj(Variable):
    cerfa_field = u"7XJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7xk(Variable):
    cerfa_field = u"7XK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7xl(Variable):
    cerfa_field = u"7XL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans"
    end = '2012-12-31'
    definition_period = YEAR


class f7xm(Variable):
    cerfa_field = u"7XM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures"
    definition_period = YEAR


# TODO: f7xn cf années < à 2011 (possible erreur dans le label pour ces dates, à vérifier)
class f7xn(Variable):
    cerfa_field = u"7XN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7xo(Variable):
    cerfa_field = u"7XO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
#    start_date = date(2008, 1, 1)
    definition_period = YEAR


class f7xp(Variable):
    cerfa_field = u"7XP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7xq(Variable):
    cerfa_field = u"7XQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7xr(Variable):
    cerfa_field = u"7XR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7xv(Variable):
    cerfa_field = u"7XV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7xx(Variable):
    cerfa_field = u"7XX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans un village résidentiel de tourisme"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7xz(Variable):
    cerfa_field = u"7XZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans une résidence de tourisme classée ou un meublé tourisme"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7uy(Variable):
    cerfa_field = u"7UY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7uz(Variable):
    cerfa_field = u"7UZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Souscriptions au capital des PME
class f7cf(Variable):
    cerfa_field = u"7CF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion"
    definition_period = YEAR


class f7cl(Variable):
    cerfa_field = u"7CL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4"
    definition_period = YEAR


class f7cm(Variable):
    cerfa_field = u"7CM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3"
    definition_period = YEAR


class f7cn(Variable):
    cerfa_field = u"7CN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2"
    definition_period = YEAR


class f7cc(Variable):
    cerfa_field = u"7CC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7cq(Variable):
    cerfa_field = u"7CQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4 pour les start-up"
#    start_date = date(2013, 1, 1) # TO CHECK : before 2013, F7CQ was something else...
    definition_period = YEAR


class f7cr(Variable):
    cerfa_field = u"7CR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3 pour les start-up"
#    start_date = date(2014, 1, 1)
    definition_period = YEAR


class f7cv(Variable):
    cerfa_field = u"7CV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2 pour les start-up"
#    start_date = date(2015, 1, 1)
    definition_period = YEAR


class f7cx(Variable):
    cerfa_field = u"7CX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1 pour les start-up"
#    start_date = date(2016, 1, 1)
    definition_period = YEAR


class f7cu(Variable):
    cerfa_field = u"7CU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures"
    definition_period = YEAR


# TODO: en 2013 et 2012 plus de sofipêche (pourtant présent dans param à ces dates...), case 7gs réutilisée

class f7gs(Variable):
    cerfa_field = u"7GS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
class f7ua(Variable):
    cerfa_field = u"7UA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2007-12-31'
    definition_period = YEAR

class f7ub(Variable):
    cerfa_field = u"7UB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2007-12-31'
    definition_period = YEAR


# En 2013 les "7" sont remplacés par des "H" dans les CERFA-FIELDS
# en 2013 et 2012, 7uc se rapporte à autre chose, réutilisation de la case
#    build_column('f7uc', IntCol(entity = 'foy', label = u"", val_type = "monetary", cerfa_field = u'7UC', end = date(2011,12,31)))  # vérifier <=2011

class f7uc(Variable):
    cerfa_field = u"7UC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Cotisations pour la défense des forêts contre l'incendie "
    definition_period = YEAR


class f7ui(Variable):
    cerfa_field = u"7UI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    # end = '2008-12-31'
    definition_period = YEAR


class f7uj(Variable):
    cerfa_field = u"7UJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2007-12-31'
    definition_period = YEAR


class f7qb(Variable):
    cerfa_field = u"7QB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2011-12-31'
    definition_period = YEAR


class f7qc(Variable):
    cerfa_field = u"7QC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2011-12-31'
    definition_period = YEAR


class f7qd(Variable):
    cerfa_field = u"7QD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2011-12-31'
    definition_period = YEAR


class f7qk(Variable):
    cerfa_field = u"7QK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2009-12-31'
    definition_period = YEAR


class f7qn(Variable):
    cerfa_field = u"7QN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2010-12-31'
    definition_period = YEAR


class f7kg(Variable):
    cerfa_field = u"7KG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2010-12-31'
    definition_period = YEAR


class f7ql(Variable):
    cerfa_field = u"7QL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2011-12-31'
    definition_period = YEAR


class f7qt(Variable):
    cerfa_field = u"7QT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2011-12-31'
    definition_period = YEAR


class f7qm(Variable):
    cerfa_field = u"7QM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    end = '2011-12-31'
    definition_period = YEAR


class f7qu(Variable):
    cerfa_field = u"7QU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7ki(Variable):
    cerfa_field = u"7KI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qj(Variable):
    cerfa_field = u"7QJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qw(Variable):
    cerfa_field = u"7QW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qx(Variable):
    cerfa_field = u"7QX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qf(Variable):
    cerfa_field = u"7QF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qg(Variable):
    cerfa_field = u"7QG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qh(Variable):
    cerfa_field = u"7QH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qi(Variable):
    cerfa_field = u"7QI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qq(Variable):
    cerfa_field = u"7QQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qr(Variable):
    cerfa_field = u"7QR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7qs(Variable):
    cerfa_field = u"7QS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7mm(Variable):
    cerfa_field = u"7MM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
#    start_date = date(2010, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7lg(Variable):
    cerfa_field = u"7LG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7ma(Variable):
    cerfa_field = u"7MA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7ks(Variable):
    cerfa_field = u"7KS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7kh(Variable):
    cerfa_field = u"7KH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    definition_period = YEAR


class f7oa(Variable):
    cerfa_field = u"7OA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ob(Variable):
    cerfa_field = u"7OB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7oc(Variable):
    cerfa_field = u"7OC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7oh(Variable):
    cerfa_field = u"7OH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7oi(Variable):
    cerfa_field = u"7OI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7oj(Variable):
    cerfa_field = u"7OJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ok(Variable):
    cerfa_field = u"7OK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2011, Autres investissements"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ol(Variable):
    cerfa_field = u"7OL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7om(Variable):
    cerfa_field = u"7OM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7on(Variable):
    cerfa_field = u"7ON"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7oo(Variable):
    cerfa_field = u"7OO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7op(Variable):
    cerfa_field = u"7OP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7oq(Variable):
    cerfa_field = u"7OQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7or(Variable):
    cerfa_field = u"7OR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7os(Variable):
    cerfa_field = u"7OS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ot(Variable):
    cerfa_field = u"7OT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ou(Variable):
    cerfa_field = u"7OU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ov(Variable):
    cerfa_field = u"7OV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ow(Variable):
    cerfa_field = u"7OW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2012, "
#    start_date = date(2012, 1, 1)
    definition_period = YEAR

 #TODO: 7O* : end ?

class fhod(Variable):
    cerfa_field = u"HOD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés avant le 1.1.2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhoe(Variable):
    cerfa_field = u"HOE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhof(Variable):
    cerfa_field = u"HOF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhog(Variable):
    cerfa_field = u"HOG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhox(Variable):
    cerfa_field = u"HOX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhoy(Variable):
    cerfa_field = u"HOY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhoz(Variable):
    cerfa_field = u"HOZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement : Investissements réalisés en 2013, Autres investissements"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

# Investissements outre-mer dans le logement social

class fhra(Variable):
    cerfa_field = u"HRA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhrb(Variable):
    cerfa_field = u"HRB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhrc(Variable):
    cerfa_field = u"HRC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class fhrd(Variable):
    cerfa_field = u"HRD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Autres investissements"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Souscription de parts de fonds communs de placement dans l'innovation,
# de fonds d'investissement de proximité
class f7gq(Variable):
    cerfa_field = u"7GQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscription de parts de fonds communs de placement dans l'innovation"
    definition_period = YEAR


class f7fq(Variable):
    cerfa_field = u"7FQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscription de parts de fonds d'investissement de proximité"
    definition_period = YEAR


class f7fm(Variable):
    cerfa_field = u"7FM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscription de parts de fonds d'investissement de proximité investis en Corse"
#    start_date = date(2007, 1, 1)
    definition_period = YEAR


class f7fl(Variable):
    cerfa_field = u"7FL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


# Souscriptions au capital de SOFICA
class f7gn(Variable):
    cerfa_field = u"7GN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital de SOFICA 36 %"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class f7fn(Variable):
    cerfa_field = u"7FN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Souscriptions au capital de SOFICA 30 %"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


# Intérêts d'emprunt pour reprise de société
class f7fh(Variable):
    cerfa_field = u"7FH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêts d'emprunt pour reprise de société"
    definition_period = YEAR


# Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée))
class f7ff(Variable):
    cerfa_field = u"7FF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)"
    definition_period = YEAR


class f7fg(Variable):
    cerfa_field = u"7FG"
    value_type = int
    entity = FoyerFiscal
    label = u"Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations"
    definition_period = YEAR


# Travaux de conservation et de restauration d’objets classés monuments historiques
class f7nz(Variable):
    cerfa_field = u"7NZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Travaux de conservation et de restauration d’objets classés monuments historiques"
#    start_date = date(2008, 1, 1)
    definition_period = YEAR


# Dépenses de protection du patrimoine naturel
class f7ka(Variable):
    cerfa_field = u"7KA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de protection du patrimoine naturel"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7kb(Variable):
    cerfa_field = u"7KB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7kc(Variable):
    cerfa_field = u"7KC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7kd(Variable):
    cerfa_field = u"7KD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7uh(Variable):
    cerfa_field = u"7UH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dons et cotisations versés aux partis politiques"
#    start_date = date(2007, 1, 1)
    definition_period = YEAR

 #TODO: séparer en plusieurs variables (même case pour plusieurs variables selon les années)

# Investissements forestiers
class f7un(Variable):
    cerfa_field = u"7UN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers: acquisition"
    definition_period = YEAR


class f7ul(Variable):
    cerfa_field = u"7UL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7uu(Variable):
    cerfa_field = u"7UU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7uv(Variable):
    cerfa_field = u"7UV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7uw(Variable):
    cerfa_field = u"7UW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7th(Variable):
    cerfa_field = u"7TH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

class f7ti(Variable):
    cerfa_field = u"7TI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2014, 1, 1)
    definition_period = YEAR

class f7tj(Variable):
    cerfa_field = u"7TJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2015, 1, 1)
    definition_period = YEAR

class f7tk(Variable):
    cerfa_field = u"7TK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2015, 1, 1)
    definition_period = YEAR

class f7tm(Variable):
    cerfa_field = u"7TM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2016, 1, 1)
    definition_period = YEAR

class f7to(Variable):
    cerfa_field = u"7TO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2016, 1, 1)
    definition_period = YEAR

class f7ux(Variable):
    cerfa_field = u"7UX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

class f7vm(Variable):
    cerfa_field = u"7VM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2016, 1, 1)
    definition_period = YEAR

class f7vn(Variable):
    cerfa_field = u"7VN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2016, 1, 1)
    definition_period = YEAR

class f7vp(Variable):
    cerfa_field = u"7VP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2016, 1, 1)
    definition_period = YEAR

class f7tg(Variable):
    cerfa_field = u"7TG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7tf(Variable):
    cerfa_field = u"7TF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2011, 1, 1)
    end = '2013-12-31'
    definition_period = YEAR


class f7ut(Variable):
    cerfa_field = u"7UT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements forestiers"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


# Intérêts pour paiement différé accordé aux agriculteurs
class f7um(Variable):
    cerfa_field = u"7UM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Intérêts pour paiement différé accordé aux agriculteurs"
    definition_period = YEAR


# Investissements locatifs neufs : Dispositif Scellier:
class f7hj(Variable):
    cerfa_field = u"7HJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7hk(Variable):
    cerfa_field = u"7HK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7hn(Variable):
    cerfa_field = u"7HN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7ho(Variable):
    cerfa_field = u"7HO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7hl(Variable):
    cerfa_field = u"7HL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7hm(Variable):
    cerfa_field = u"7HM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7hr(Variable):
    cerfa_field = u"7HR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7hs(Variable):
    cerfa_field = u"7HS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7la(Variable):
    cerfa_field = u"7LA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2009"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7lb(Variable):
    cerfa_field = u"7LB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2010"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7lc(Variable):
    cerfa_field = u"7LC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2010"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ld(Variable):
    cerfa_field = u"7LD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7le(Variable):
    cerfa_field = u"7LE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7lf(Variable):
    cerfa_field = u"7LF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ls(Variable):
    cerfa_field = u"7LS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7lm(Variable):
    cerfa_field = u"7LM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7lz(Variable):
    cerfa_field = u"7LZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Report du solde de réduction d'impôt de l'année 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7mg(Variable):
    cerfa_field = u"7MG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2012 : report du solde de réduction d'impôt de l'année 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7na(Variable):
    cerfa_field = u"7NA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, métropole, BBC"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nb(Variable):
    cerfa_field = u"7NB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nc(Variable):
    cerfa_field = u"7NC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, BBC"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nd(Variable):
    cerfa_field = u"7ND"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, BBC"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ne(Variable):
    cerfa_field = u"7NE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, BBC"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nf(Variable):
    cerfa_field = u"7NF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ng(Variable):
    cerfa_field = u"7NG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nh(Variable):
    cerfa_field = u"7NH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, non-BBC"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ni(Variable):
    cerfa_field = u"7NI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, non-BBC"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nj(Variable):
    cerfa_field = u"7NJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, non-BBC"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nk(Variable):
    cerfa_field = u"7NK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nl(Variable):
    cerfa_field = u"7NL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nm(Variable):
    cerfa_field = u"7NM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nn(Variable):
    cerfa_field = u"7NN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7no(Variable):
    cerfa_field = u"7NO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7np(Variable):
    cerfa_field = u"7NP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nq(Variable):
    cerfa_field = u"7NQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nr(Variable):
    cerfa_field = u"7NR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ns(Variable):
    cerfa_field = u"7NS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7nt(Variable):
    cerfa_field = u"7NT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7hv(Variable):
    cerfa_field = u"7HV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7hw(Variable):
    cerfa_field = u"7HW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7hx(Variable):
    cerfa_field = u"7HX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole avec promesse d'achat avant le 1.1.2010"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7hz(Variable):
    cerfa_field = u"7HZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM avec promesse d'achat avant le 1.1.2010"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ht(Variable):
    cerfa_field = u"7HT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7hu(Variable):
    cerfa_field = u"7HU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ha(Variable):
    cerfa_field = u"7HA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7hb(Variable):
    cerfa_field = u"7HB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011, avec promesse d'achat en 2010"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7hg(Variable):
    cerfa_field = u"7HG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7hh(Variable):
    cerfa_field = u"7HH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna avec promesse d'achat en 2010"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7hd(Variable):
    cerfa_field = u"7HD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, réalisés en 2010, en métropole et dans les DOM-COM"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7he(Variable):
    cerfa_field = u"7HE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, en métropole et dans les DOM-COM avec promesse d'achat avant le 1.1.2010"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7hf(Variable):
    cerfa_field = u"7HF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, Investissements réalisés en 2009 en métropole et dans les DOM-COM"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ja(Variable):
    cerfa_field = u"7JA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, BBC"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jb(Variable):
    cerfa_field = u"7JB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, BBC"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jd(Variable):
    cerfa_field = u"7JD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, BBC"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7je(Variable):
    cerfa_field = u"7JE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, BBC "
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jf(Variable):
    cerfa_field = u"7JF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, non-BBC"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jg(Variable):
    cerfa_field = u"7JG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, non-BBC"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jh(Variable):
    cerfa_field = u"7JH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, non-BBC"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jj(Variable):
    cerfa_field = u"7JJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, non-BBC"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jk(Variable):
    cerfa_field = u"7JK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jl(Variable):
    cerfa_field = u"7JL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jm(Variable):
    cerfa_field = u"7JM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jn(Variable):
    cerfa_field = u"7JN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jo(Variable):
    cerfa_field = u"7JO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jp(Variable):
    cerfa_field = u"7JP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jq(Variable):
    cerfa_field = u"7JQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jr(Variable):
    cerfa_field = u"7JR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7gj(Variable):
    cerfa_field = u"7GJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7gk(Variable):
    cerfa_field = u"7GK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7gl(Variable):
    cerfa_field = u"7GL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7gp(Variable):
    cerfa_field = u"7GP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2010s"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7fa(Variable):
    cerfa_field = u"7FA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, BBC"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7fb(Variable):
    cerfa_field = u"7FB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, non-BBC"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7fc(Variable):
    cerfa_field = u"7FC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7fd(Variable):
    cerfa_field = u"7FD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences
class f7ij(Variable):
    cerfa_field = u"7IJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, engagement de réalisation de l'investissement en 2011"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7il(Variable):
    cerfa_field = u"7IL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, promesse d'achat en 2010"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7im(Variable):
    cerfa_field = u"7IM"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2010 et achevés en 2012 avec promesse d'achat en 2009"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7ik(Variable):
    cerfa_field = u"7IK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Reports de 1/9 de l'investissement réalisé et achevé en 2009"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7in(Variable):
    cerfa_field = u"7IN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.1.2011 au 31.3.2011"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7iv(Variable):
    cerfa_field = u"7IV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.4.2011 au 31.12.2011"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7iw(Variable):
    cerfa_field = u"7IW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2012"
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7io(Variable):
    cerfa_field = u"7IO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ip(Variable):
    cerfa_field = u"7IP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7ir(Variable):
    cerfa_field = u"7IR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7iq(Variable):
    cerfa_field = u"7IQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7iu(Variable):
    cerfa_field = u"7IU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7it(Variable):
    cerfa_field = u"7IT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : "
#    start_date = date(2011, 1, 1)
    definition_period = YEAR


class f7is(Variable):
    cerfa_field = u"7IS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Report du solde de réduction d'impôt non encore imputé: année  n-4"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7ia(Variable):
    cerfa_field = u"7IA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ib(Variable):
    cerfa_field = u"7IB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ic(Variable):
    cerfa_field = u"7IC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2011 avec promesse d'achat en 2009 ou réalisés en 2009"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7id(Variable):
    cerfa_field = u"7ID"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Engagement de réalisation de l'investissement en 2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ie(Variable):
    cerfa_field = u"7IE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Promesse d'achat en 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7if(Variable):
    cerfa_field = u"7IF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.1.2012 au 31.3.2012, investissement réalisé du 1.1.2012 au 31.3.2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ig(Variable):
    cerfa_field = u"7IG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.4.2012 au 31.12.2012"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ix(Variable):
    cerfa_field = u"7IX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2009; réalisés en 2009 et achevés en 2010; réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report du solde de réduction d'impôt de l'année 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7ih(Variable):
    cerfa_field = u"7IH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7iz(Variable):
    cerfa_field = u"7IZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7jt(Variable):
    cerfa_field = u"7JT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2013"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7ju(Variable):
    cerfa_field = u"7JU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7jv(Variable):
    cerfa_field = u"7JV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7jw(Variable):
    cerfa_field = u"7JW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 ou réalisés en 2012 avec promesse d'achat en 2011"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7jx(Variable):
    cerfa_field = u"7JX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7jy(Variable):
    cerfa_field = u"7JY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2010 avec promesse d'achat en 2009 ou réalisés en 2009"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7jc(Variable):
    cerfa_field = u"7JC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7ji(Variable):
    cerfa_field = u"7JI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d'impôt de l'année 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7js(Variable):
    cerfa_field = u"7JS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d’impôt de l’année 2012"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


# Investissements locatifs dans les résidences de tourisme situées dans une zone de
# revitalisation rurale

# """
# réutilisation de cases en 2013
# """

class f7gt(Variable):
    cerfa_field = u"7GT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

  # vérif <=2012

class f7gu(Variable):
    cerfa_field = u"7GU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

  # vérif <=2012

class f7gv(Variable):
    cerfa_field = u"7GV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna "
#    start_date = date(2013, 1, 1)
    definition_period = YEAR

  # vérif <=2012

class f7xg(Variable):
    cerfa_field = u"7XG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme"
    end = '2012-12-01'
    definition_period = YEAR

  # vérif <=2012

# Crédits d'impôts en f7
# Acquisition de biens culturels
class f7uo(Variable):
    cerfa_field = u"7UO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Acquisition de biens culturels"
    definition_period = YEAR


# Mécénat d'entreprise
class f7us(Variable):
    cerfa_field = u"7US"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Réduction d'impôt mécénat d'entreprise"
    definition_period = YEAR


# Crédits d’impôt pour dépenses en faveur de la qualité environnementale

class f7sb(Variable):
    cerfa_field = u"7SB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %"
#    start_date = date(2009, 1, 1)
    end = '2011-12-31'
    definition_period = YEAR


class f7sc(Variable):
    cerfa_field = u"7SC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédits d’impôt pour dépenses en faveur de la qualité environnementale"
#    start_date = date(2009, 1, 1)
    end = '2009-12-01'
    definition_period = YEAR


# """
# réutilisation de case pour 2013
# """

class f7sd(Variable):
    cerfa_field = u"7SD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7se(Variable):
    cerfa_field = u"7SE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7sh(Variable):
    cerfa_field = u"7SH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


# ('f7wg', IntCol() déjà disponible

# Crédit d'impôt pour dépense d'acquisition ou de transformation d'un véhicule GPL ou mixte en 2007 et investissements forestiers aprés ???

class f7up(Variable):
    cerfa_field = u"7UP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt pour investissements forestiers: travaux"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


class f7uq(Variable):
    cerfa_field = u"7UQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt pour investissements forestiers: contrat de gestion"
#    start_date = date(2009, 1, 1)
    definition_period = YEAR


# Déclaration de déménagement correspondant à un crédit d'impôt aide à la mobilité
class f1ar(Variable):
    cerfa_field = u"1AR"
    value_type = bool
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité : le déclarant déménage à plus de 200 km pour son emploi"
    end = '2008-12-31'
    definition_period = YEAR


#TODO: QUIFOY
class f1br(Variable):
    cerfa_field = u"1BR"
    value_type = bool
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité : le conjoint déménage à plus de 200 km pour son emploi"
    end = '2008-12-31'
    definition_period = YEAR


class f1cr(Variable):
    cerfa_field = u"1CR"
    value_type = bool
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité : la 1ère personne à charge déménage à plus de 200 km pour son emploi"
    end = '2008-12-31'
    definition_period = YEAR


class f1dr(Variable):
    cerfa_field = u"1DR"
    value_type = bool
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité : la 2è personne à charge déménage à plus de 200 km pour son emploi"
    end = '2008-12-31'
    definition_period = YEAR


class f1er(Variable):
    cerfa_field = u"1ER"
    value_type = bool
    entity = FoyerFiscal
    label = u"Crédit d'impôt aide à la mobilité : la 3è personne à charge déménage à plus de 200 km pour son emploi"
    end = '2006-12-31'
    definition_period = YEAR


# Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
class f4tq(Variable):
    cerfa_field = u"4TQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d’impôt représentatif de la taxe additionnelle au droit de bail"
    definition_period = YEAR

  # vérif libéllé, en 2013=Montant des loyers courus du 01/01/1998 au 30/09/1998 provenant des immeubles
                                       # pour lesquels la cessation ou l'interruption de la location est intervenue en 2013 et qui ont été
                                       # soumis à la taxe additionnelle au droit de bail

# Crédits d’impôt pour dépenses en faveur de l’aide aux personnes

class f7sf(Variable):
    cerfa_field = u"7SF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit de travaux en faveur d'aides aux personnes pour des logements en location (avant 2012 ) / Appareils de régulation du chauffage, matériaux de calorifugeage (après 2011)"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7si(Variable):
    cerfa_field = u"7SI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f7te(Variable):
    cerfa_field = u"7TE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses d'investissement forestier"
#    start_date = date(2010, 1, 1)
    definition_period = YEAR


class f7tu(Variable):
    cerfa_field = u"7TU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de travaux dans l'habitation principale"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7tt(Variable):
    cerfa_field = u"7TT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de travaux dans l'habitation principale"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7tv(Variable):
    cerfa_field = u"7TV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de travaux dans l'habitation principale"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7tx(Variable):
    cerfa_field = u"7TX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de travaux dans l'habitation principale"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7ty(Variable):
    cerfa_field = u"7TY"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de travaux dans l'habitation principale"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


class f7tw(Variable):
    cerfa_field = u"7TW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Dépenses de travaux dans l'habitation principale"
#    start_date = date(2012, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR


# Réduction d'impôts sur les investissements locatifs intermédiaires (loi Duflot)

class f7gh(Variable):
    cerfa_field = u"7GH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs intermédiaires en métropole"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7gi(Variable):
    cerfa_field = u"7GI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs intermédiaires outre-mer"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f7ek(Variable):
    cerfa_field = u"7EK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs intermÃ©diaires du 1.1 au 31.8.2014 en mÃ©tropole"
#    start_date = date(2014, 1, 1)
    definition_period = YEAR


class f7el(Variable):
    cerfa_field = u"7EL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Investissements locatifs intermÃ©diaires du 1.1 au 31.8.2014 en outre-mer"
#    start_date = date(2014, 1, 1)
    definition_period = YEAR


class f7fi(Variable):
    cerfa_field = u"7FI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report concernant les investissements rÃ©alisÃ©s et achevÃ©s en 2013 en mÃ©tropole et outre-mer"
#    start_date = date(2014, 1, 1)
    definition_period = YEAR

class f7fk(Variable):
    cerfa_field = u"7FK"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report concernant les investissements rÃ©alisÃ©s et achevÃ©s en 2014 en mÃ©tropole et outre-mer"
#    start_date = date(2015, 1, 1)
    definition_period = YEAR

class f7fr(Variable):
    cerfa_field = u"7FR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Report concernant les investissements rÃ©alisÃ©s et achevÃ©s en 2015 en mÃ©tropole et outre-mer"
#    start_date = date(2016, 1, 1)
    definition_period = YEAR


# section 8

class f8tc(Variable):
    cerfa_field = u"8TC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))"
    end = '2008-12-31'
    definition_period = YEAR


class f8tb(Variable):
    cerfa_field = u"8TB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)"
    definition_period = YEAR


class f8te(Variable):
    cerfa_field = u"8TE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé"
    definition_period = YEAR


class f8tf(Variable):
    cerfa_field = u"8TF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Reprises de réductions ou de crédits d'impôt"
    definition_period = YEAR


class f8tg(Variable):
    cerfa_field = u"8TG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédits d'impôt en faveur des entreprises: Investissement en Corse"
    definition_period = YEAR


class f8tl(Variable):
    cerfa_field = u"8TL"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt compétitivité emploi (CICE), entreprises bénéficiant de la restitution immédiate"
    definition_period = YEAR


class f8to(Variable):
    cerfa_field = u"8TO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures"
    definition_period = YEAR


class f8tp(Variable):
    cerfa_field = u"8TP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt"
    definition_period = YEAR


class f8ts(Variable):
    cerfa_field = u"8TS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: investissement en Corse, crédit d'impôt"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f8uz(Variable):
    cerfa_field = u"8UZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Famille"
    definition_period = YEAR


class f8uw(Variable):
    cerfa_field = u"8UW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt compétitivité emploi (CICE), autres entreprises"
#    start_date = date(2013, 1, 1)
    definition_period = YEAR


class f8tz(Variable):
    cerfa_field = u"8TZ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Apprentissage"
    definition_period = YEAR


class f8wa(Variable):
    cerfa_field = u"8WA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Agriculture biologique"
    definition_period = YEAR


class f8wb(Variable):
    cerfa_field = u"8WB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Prospection commerciale"
    definition_period = YEAR


class f8wc__2008(Variable):
    cerfa_field = u"8WC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Nouvelles technologies"
    end = '2008-12-31'
    definition_period = YEAR


class f8wc(Variable):
    cerfa_field = u"8WC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Prêts sans intérêt"
#    start_date = date(2012, 1, 1)
    definition_period = YEAR


class f8wd(Variable):
    cerfa_field = u"8WD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class f8we(Variable):
    cerfa_field = u"8WE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Intéressement"
#    start_date = date(2008, 1, 1)
    definition_period = YEAR


class f8wr(Variable):
    cerfa_field = u"8WR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Métiers d'art"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class f8ws(Variable):
    cerfa_field = u"8WS"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes"
#    start_date = date(2006, 1, 1)
    end = '2009-12-31'
    definition_period = YEAR

  # verif<=2012

class f8wt(Variable):
    cerfa_field = u"8WT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class f8wu(Variable):
    cerfa_field = u"8WU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Maître restaurateur"
#    start_date = date(2006, 1, 1)
    definition_period = YEAR


class f8wv(Variable):
    cerfa_field = u"8WV"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Débitants de tabac"
#    start_date = date(2007, 1, 1)
    end = '2012-12-31'
    definition_period = YEAR

  # verif<=2012

class f8wx(Variable):
    cerfa_field = u"8WX"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise"
#    start_date = date(2007, 1, 1)
    end = '2009-12-31'
    definition_period = YEAR

  # verif<=2012

class elig_creimp_exc_2008(Variable):
    default_value = 1
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Éligibilité au crédit d'impôt exceptionnel sur les revenus 2008"
#    start_date = date(2008, 1, 1)
    end = '2008-12-31'
    definition_period = YEAR


class elig_creimp_jeunes(Variable):
    value_type = bool
    entity = Individu
    label = u"Éligible au crédit d'impôt jeunes"
#    start_date = date(2005, 1, 1)
    end = '2008-01-01'
    definition_period = YEAR

 #Sert à savoir si son secteur d'activité permet au jeune de bénéficier du crédit impôts jeunes
