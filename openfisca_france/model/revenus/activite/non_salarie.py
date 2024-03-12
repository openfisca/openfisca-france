from openfisca_core.periods import Period

from openfisca_france.model.base import *


# TODO: 5QL


# Nomenclature :
# première lettre :
#    e : auto-entrepreneur
#    m : micro entreprise, déclaratif spécial
#    n : bénéfice réel sans CGA
#    a : bénéfice réel avec CGA ou viseur
#    f : forfait
#    c : déclaration contrôlée)
# trois lettres suivantes, catégorie du revenu :
#    rag : agricole
#    bic : industriel et commercial pro
#    bnc : non commercial pro
#    acc : industriel et commercial non pro
#    ncn : non commercial non pro
# après l'underscore : abbréviation du label de la case

# (f5qm, f5rm )
class f5qm(Variable):
    cerfa_field = {0: '5QM',
        1: '5RM',
                   }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Agents généraux d’assurances: indemnités de cessation d’activité'
    definition_period = YEAR


# """
# Revenus des professions non salariées
# """

# (f5nv, f5ov, f5pv)
class ppe_du_ns(Variable):
    cerfa_field = {0: '5NV',
        1: '5OV',
        2: '5PV',
                   }
    value_type = int
    entity = Individu
    label = "Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année"
    end = '2014-12-31'
    definition_period = YEAR


# (f5nw, f5ow, f5pw)
class ppe_tp_ns(Variable):
    cerfa_field = {0: '5NW',
        1: '5OW',
        2: '5PW',
                   }
    value_type = bool
    entity = Individu
    label = "Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière"
    end = '2014-12-31'
    definition_period = YEAR


# (f5hn, f5in, f5jn))
class frag_exon(Variable):
    cerfa_field = {0: '5HN',
        1: '5IN',
        2: '5JN', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles exonérés (régime du forfait)'
    # start_date = date(2007, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


# (f5ha, f5ia, f5ja))
class arag_info(Variable):
    cerfa_field = {0: '5HA',
        1: '5IA',
        2: '5JA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles: revenus nets de la cession ou concession de brevets et assimilés'
    # start_date = date(2019, 1, 1)
    definition_period = YEAR


# (f5hd, f5id, f5jd))
class coupe_bois(Variable):
    cerfa_field = {0: '5HD',
        1: '5ID',
        2: '5JD', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus forfaitaire provenant des coupes de bois'
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# (f5xa, f5ya, f5za))
class mrag_exon(Variable):
    cerfa_field = {0: '5XA',
        1: '5YA',
        2: '5ZA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles exonérés (régime micro BA)'
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# (f5ho, f5io, f5jo))
class frag_impo(Variable):
    cerfa_field = {0: '5HO',
        1: '5IO',
        2: '5JO', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles imposables (régime du forfait)'
    # start_date = date(2007, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


# (f5xb, f5yb, f5zb))
class mrag_impo(Variable):
    cerfa_field = {0: '5XB',
        1: '5YB',
        2: '5ZB', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles imposables (régime micro BA)'
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# (f5xc, f5yc, f5zc)
class date_creation(Variable):
    cerfa_field = {0: '5XC',
        1: '5YC',
        2: '5ZC',
                   }
    value_type = int
    entity = Individu
    label = 'Revenus agricoles : Année de création de l’activité'
    # start_date = date(2016, 1, 1)
    end = '2017-12-31'
    definition_period = YEAR


# (f5xd, f5yd, f5zd))
class frag_impo_n2(Variable):
    cerfa_field = {0: '5XD',
        1: '5YD',
        2: '5ZD', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles, forfait ou microBA année n-2'
    # start_date = date(2016, 1, 1)
    end = '2017-12-31'
    definition_period = YEAR


# (f5xe, f5ye, f5ze))
class frag_impo_n1(Variable):
    cerfa_field = {0: '5XE',
        1: '5YE',
        2: '5ZE', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles, forfait ou microBA année n-1'
    # start_date = date(2016, 1, 1)
    end = '2017-12-31'
    definition_period = YEAR


# (f5xf, f5yf, f5zf))
class arag_impo_n2(Variable):
    cerfa_field = {0: '5XF',
        1: '5YF',
        2: '5ZF', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles, régime du bénéfice réel année n-2'
    # start_date = date(2016, 1, 1)
    end = '2017-12-31'
    definition_period = YEAR


# (f5xg, f5yg, f5zg))
class arag_impo_n1(Variable):
    cerfa_field = {0: '5XG',
        1: '5YG',
        2: '5ZG', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus agricoles, régime du bénéfice réel année n-1'
    # start_date = date(2016, 1, 1)
    end = '2016-12-31'
    definition_period = YEAR


# (f5hb, f5ib, f5jb))
class arag_exon(Variable):
    cerfa_field = {0: '5HB',
        1: '5IB',
        2: '5JB', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hc, f5ic, f5jc))
class arag_impg(Variable):
    cerfa_field = {0: '5HC',
        1: '5IC',
        2: '5JC', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hf, f5if, f5jf))
class arag_defi(Variable):
    cerfa_field = {0: '5HF',
        1: '5IF',
        2: '5JF', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hh, f5ih, f5jh))
class nrag_exon(Variable):
    cerfa_field = {0: '5HH',
        1: '5IH',
        2: '5JH', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse"
    # start_date = date(2007, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5hi, f5ii, f5ji))
class nrag_impg(Variable):
    cerfa_field = {0: '5HI',
        1: '5II',
        2: '5JI', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5hl, f5il, f5jl))
class nrag_defi(Variable):
    cerfa_field = {0: '5HL',
        1: '5IL',
        2: '5JL', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5hm, f5im, f5jm))
class nrag_ajag(Variable):
    cerfa_field = {0: '5HM',
        1: '5IM',
        2: '5JM', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# """
# Autoentrepreneur
# """


# (f5ta, f5ua, f5va))
class ebic_impv(Variable):
    cerfa_field = {0: '5TA',
        1: '5UA',
        2: '5VA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur ayant opté pour le versement libératoire)'
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


# (f5tb, f5ub, f5vb))
class ebic_imps(Variable):
    cerfa_field = {0: '5TB',
        1: '5UB',
        2: '5VB', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur ayant opté pour le versement libératoire)'
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


# (f5te, f5ue, f5ve))
class ebnc_impo(Variable):
    cerfa_field = {0: '5TE',
        1: '5UE',
        2: '5VE', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus non commerciaux (régime auto-entrepreneur ayant opté pour le versement libératoire)'
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


# (f5kn, f5ln, f5mn))
class mbic_exon(Variable):
    cerfa_field = {0: '5KN',
        1: '5LN',
        2: '5MN', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)'
    definition_period = YEAR


# (f5kb, f5lb, f5mb))
class abic_exon(Variable):
    cerfa_field = {0: '5KB',
        1: '5LB',
        2: '5MB', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5kh, f5lh, f5mh))
class nbic_exon(Variable):
    cerfa_field = {0: '5KH',
        1: '5LH',
        2: '5MH', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)'
    end = '2022-12-31'
    definition_period = YEAR


# (f5ko, f5lo, f5mo))
class mbic_impv(Variable):
    cerfa_field = {0: '5KO',
        1: '5LO',
        2: '5MO', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)'
    definition_period = YEAR


# (f5kp, f5lp, f5mp))
class mbic_imps(Variable):
    cerfa_field = {0: '5KP',
        1: '5LP',
        2: '5MP', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)'
    definition_period = YEAR


# (f5kc, f5lc, f5mc))
class abic_impn(Variable):
    cerfa_field = {0: '5KC',
        1: '5LC',
        2: '5MC', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5kd, f5ld, f5md))
class abic_imps(Variable):
    cerfa_field = {0: '5KD',
        1: '5LD',
        2: '5MD', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)'
    end = '2009-12-31'
    definition_period = YEAR


# (f5ki, f5li, f5mi))
class nbic_impn(Variable):
    cerfa_field = {0: '5KI',
        1: '5LI',
        2: '5MI', }

    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)'
    end = '2022-12-31'
    definition_period = YEAR


# (f5ui, f5vi, f5wi))
class abic_info(Variable):
    cerfa_field = {0: '5UI',
        1: '5VI',
        2: '5WI', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels : Revenus nets de la cession ou concession de brevets et assimilés'
    # start_date = date(2019, 1, 1)
    definition_period = YEAR


# """
# Réutilisation cases 2013
# """


# (f5kj, f5lj, f5mj))
class nbic_imps(Variable):
    cerfa_field = {0: '5KJ',
        1: '5LJ',
        2: '5MJ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels imposables: régime simplifié sans CGA (régime du bénéfice réel)'
    end = '2009-12-31'
    definition_period = YEAR


# (f5kj, f5lj, f5mj))
# NB cette variable devrait s'appeler 'mbic_mvct' comme c'est une variable de régime micro (mais il
# existe déjà une variable mbic_mvct avec un autre cerfa_fiel (5HU) corresponsant à avant 2012...)
class nbic_mvct(Variable):
    cerfa_field = {0: '5KJ',
        1: '5LJ',
        2: '5MJ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux professionnels moins-values nettes à court terme : régime micro-entreprise'
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5kf, f5lf, f5mf))
class abic_defn(Variable):
    cerfa_field = {0: '5KF',
        1: '5LF',
        2: '5MF', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5kg, f5lg, f5mg))
# vérif <=2012
class abic_defs(Variable):
    cerfa_field = {0: '5KG',
        1: '5LG',
        2: '5MG', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)'
    end = '2009-12-01'
    definition_period = YEAR


# (f5kl, f5ll, f5ml))
class nbic_defn(Variable):
    cerfa_field = {0: '5KL',
        1: '5LL',
        2: '5ML', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)'
    end = '2022-12-31'
    definition_period = YEAR


# (f5km, f5lm, f5mm))
class nbic_defs(Variable):
    cerfa_field = {0: '5KM',
        1: '5LM',
        2: '5MM', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime simplifié du bénéfice réel)'
    end = '2009-12-31'
    definition_period = YEAR


# TODO : ajouter dans formules
class nlnp_imps(Variable):
    cerfa_field = {0: '5KM',
        1: '5LM',
        2: '5MM', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Locations meublées non professionnelles: Gîtes ruraux et chambres d'hôtes déjà soumis aux prélèvements sociaux sans CGA (régime du bénéfice réel)"
    # start_date = date(2012, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5ks, f5ls, f5ms))
class nbic_apch(Variable):
    cerfa_field = {0: '5KS',
        1: '5LS',
        2: '5MS', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)'
    end = '2017-12-31'
    definition_period = YEAR


# (f5nn, f5on, f5pn))
class macc_exon(Variable):
    cerfa_field = {0: '5NN',
        1: '5ON',
        2: '5PN', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)'
    definition_period = YEAR


# (f5nb, f5ob, f5pb))
class aacc_exon(Variable):
    cerfa_field = {0: '5NB',
        1: '5OB',
        2: '5PB', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5tf, f5uf, f5vf))
class aacc_info(Variable):
    cerfa_field = {0: '5TF',
        1: '5UF',
        2: '5VF', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non-professionnels : Revenus nets de la cession ou concession de brevets et assimilés'
    # start_date = date(2019, 1, 1)
    definition_period = YEAR


# (f5nh, f5oh, f5ph))
class nacc_exon(Variable):
    cerfa_field = {0: '5NH',
        1: '5OH',
        2: '5PH', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)'
    end = '2022-12-31'
    definition_period = YEAR


# (f5no, f5oo, f5po))
class macc_impv(Variable):
    cerfa_field = {0: '5NO',
        1: '5OO',
        2: '5PO', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)'
    definition_period = YEAR


# (f5np, f5op, f5pp))
class macc_imps(Variable):
    cerfa_field = {0: '5NP',
        1: '5OP',
        2: '5PP', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)'
    definition_period = YEAR


# (f5nc, f5oc, f5pc))
class aacc_impn(Variable):
    cerfa_field = {0: '5NC',
        1: '5OC',
        2: '5PC', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5nd, f5od, f5pd)) #TODO: avant 2010
class aacc_imps(Variable):
    cerfa_field = {0: '5ND',
        1: '5OD',
        2: '5PD', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Locations meublées non professionnelles (régime micro entreprise)'
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


# (f5nf, f5of, f5pf))
class aacc_defn(Variable):
    cerfa_field = {0: '5NF',
        1: '5OF',
        2: '5PF', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5ng, f5og, f5pg))
class aacc_gits(Variable):
    cerfa_field = {0: '5NG',
        1: '5OG',
        2: '5PG', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


# (f5ni, f5oi, f5pi))
class nacc_impn(Variable):
    cerfa_field = {0: '5NI',
        1: '5OI',
        2: '5PI', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)'
    end = '2022-12-31'
    definition_period = YEAR


# (f5ng, f5og, f5pg))
class aacc_defs(Variable):
    cerfa_field = {0: '5NG',
        1: '5OG',
        2: '5PG', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits de revenus industriels et commerciaux non professionnels avec CGA (régime simplifié du bénéfice réel)'
    end = '2009-12-31'
    definition_period = YEAR


# (f5nj, f5oj, f5pj)) #TODO: dates 5PJ, 5PG, 5PD, 5OM
class nacc_meup(Variable):
    cerfa_field = {0: '5NJ',
        1: '5OJ',
        2: '5PJ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Locations meublées non professionnelles: Locations meublées et chambre d'hôtes déjà soumises aux prélèvements sociaux (régime micro entreprise)"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5nw, f5ow, f5pw))
class nacc_meuc(Variable):
    cerfa_field = {0: '5NW',
        1: '5OW',
        2: '5PW', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Locations meublées non professionnelles: cas général des locations déjà soumises aux prélèvements sociaux (régime micro entreprise)'
    # start_date = (2017,1,1)
    definition_period = YEAR


# (f5nl, f5ol, f5pl))
class nacc_defn(Variable):
    cerfa_field = {0: '5NL',
        1: '5OL',
        2: '5PL', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)'
    end = '2022-12-31'
    definition_period = YEAR


# (f5nm, f5om, f5pm)) #TODO autres 5NM
class nacc_pres(Variable):
    cerfa_field = {0: '5NM',
        1: '5OM',
        2: '5PM', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Locations meublées non professionnelles: Gîtes ruraux et chambres d'hôtes déjà soumis aux prélèvements sociaux avec CGA (régime du bénéfice réel)"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5ku, f5lu, f5mu))
class mncn_impo(Variable):
    cerfa_field = {0: '5KU',
        1: '5LU',
        2: '5MU', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5sn, f5ns, f5os))
class cncn_bene(Variable):
    cerfa_field = {0: '5SN',
        1: '5NS',
        2: '5OS', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)'
    # start_date = date(2006, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5sp, f5nu, f5ou, f5sr))
# pas de f5sr en 2013
class cncn_defi(Variable):
    cerfa_field = {0: '5SP',
        1: '5NU',
        2: '5OU', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)'
    # start_date = date(2006, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5hp, f5ip, f5jp))
class mbnc_exon(Variable):
    cerfa_field = {0: '5HP',
        1: '5IP',
        2: '5JP', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5qb, f5rb, f5sb))
class abnc_exon(Variable):
    cerfa_field = {0: '5QB',
        1: '5RB',
        2: '5SB', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qh, f5rh, f5sh))
class nbnc_exon(Variable):
    cerfa_field = {0: '5QH',
        1: '5RH',
        2: '5SH', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"
    end = '2022-12-31'
    definition_period = YEAR


# (f5hq, f5iq, f5jq))
class mbnc_impo(Variable):
    cerfa_field = {0: '5HQ',
        1: '5IQ',
        2: '5JQ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5qa, f5ra, f5sa))
class abnc_info(Variable):
    cerfa_field = {0: '5QA',
        1: '5RA',
        2: '5SA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus non-commerciaux professionnels imposables: Revenus nets de la cession ou concession de brevets et assimilés (régime de déclaration controlée)'
    # start_date = date(2019, 1, 1)
    definition_period = YEAR


# (f5qc, f5rc, f5sc))
class abnc_impo(Variable):
    cerfa_field = {0: '5QC',
        1: '5RC',
        2: '5SC', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qe, f5re, f5se))
class abnc_defi(Variable):
    cerfa_field = {0: '5QE',
        1: '5RE',
        2: '5SE', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qi, f5ri, f5si))
class nbnc_impo(Variable):
    cerfa_field = {0: '5QI',
        1: '5RI',
        2: '5SI', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"
    end = '2022-12-31'
    definition_period = YEAR


# (f5qk, f5rk, f5sk))
class nbnc_defi(Variable):
    cerfa_field = {0: '5QK',
        1: '5RK',
        2: '5SK', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"
    end = '2022-12-31'
    definition_period = YEAR


# (f5hu))
# vérif <=2012
class mbic_mvct(Variable):
    cerfa_field = '5HU'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)'
    end = '2011-12-31'
    definition_period = YEAR


# (f5iu))
class macc_mvct(Variable):
    cerfa_field = '5IU'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)'
    definition_period = YEAR


# (f5ju))
class mncn_mvct(Variable):
    cerfa_field = '5JU'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5kz, f5lz , f5mz), f5lz , f5mz sont présentent en 2013
class mbnc_mvct(Variable):
    cerfa_field = {0: '5KZ',  # TODO: pb cerfa field
        1: '5LZ',
        2: '5MZ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)'
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5hw, f5iw, f5jw))
class frag_pvct(Variable):
    cerfa_field = {0: '5HW',
        1: '5IW',
        2: '5JW', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values agricoles  à court terme (régime du forfait)'
    # start_date = date(2007, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


# (f5kx, f5lx, f5mx))
class mbic_pvct(Variable):
    cerfa_field = {0: '5KX',
        1: '5LX',
        2: '5MX', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)'
    definition_period = YEAR


# (f5nx, f5ox, f5px))
class macc_pvct(Variable):
    cerfa_field = {0: '5NX',
        1: '5OX',
        2: '5PX', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)'
    definition_period = YEAR


# (f5hv, f5iv, f5jv))
class mbnc_pvct(Variable):
    cerfa_field = {0: '5HV',
        1: '5IV',
        2: '5JV', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5ky, f5ly, f5my))
class mncn_pvct(Variable):
    cerfa_field = {0: '5KY',
        1: '5LY',
        2: '5MY', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5kr, f5lr, f5mr))
class mbic_mvlt(Variable):
    cerfa_field = {0: '5KR',
        1: '5LR',
        2: '5MR', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)'
    definition_period = YEAR


# (f5nr, f5or, f5pr))
class macc_mvlt(Variable):
    cerfa_field = {0: '5NR',
        1: '5OR',
        2: '5PR', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)'
    definition_period = YEAR


# (f5kw, f5lw, f5mw))
class mncn_mvlt(Variable):
    cerfa_field = {0: '5KW',
        1: '5LW',
        2: '5MW', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5hs, f5is, f5js))
class mbnc_mvlt(Variable):
    cerfa_field = {0: '5HS',
        1: '5IS',
        2: '5JS', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5hx, f5ix, f5jx))
class frag_pvce(Variable):
    cerfa_field = {0: '5HX',
        1: '5IX',
        2: '5JX', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values agricoles de cession (régime du forfait ou MICRO BA) taxables à 16%'
    # start_date = date(2007, 1, 1)
    end = '2016-12-31'
    definition_period = YEAR


# (f5hw, f5iw, f5jw))
class mrag_pvct(Variable):
    cerfa_field = {0: '5HW',
        1: '5IW',
        2: '5JW', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values agricoles (régime microBA) à court-terme'
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# (f5hx, f5ix, f5jx))
class mrag_pvce(Variable):
    cerfa_field = {0: '5HX',
        1: '5IX',
        2: '5JX', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values agricoles (régime microBA) à long-terme taxable selon droit commun'
    # start_date = date(2017, 1, 1)
    definition_period = YEAR


# (f5xo, f5yo, f5zo))
class mrag_mvct(Variable):
    cerfa_field = {0: '5XO',
        1: '5YO',
        2: '5ZO', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Moins-values agricoles (régime microBA) à court-terme'
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# (f5xn, f5yn, f5zn))
class mrag_mvlt(Variable):
    cerfa_field = {0: '5XN',
        1: '5YN',
        2: '5ZN', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Moins-values agricoles (régime microBA) à long-terme'
    # start_date = date(2016, 1, 1)
    definition_period = YEAR


# (f5he, f5ie, f5je))
class arag_pvce(Variable):
    cerfa_field = {0: '5HE',
        1: '5IE',
        2: '5JE', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Plus-values agricoles de cession taxables au régime de droit commun (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# TODO: vérif <=2012))  # (f5hk, f5lk, f5jk) codent autre chose sur d'autres années),
class nrag_pvce(Variable):
    cerfa_field = {0: '5HK',
        1: '5LK',
        2: '5JK', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    end = '2006-12-31'
    definition_period = YEAR


# (f5kq, f5lq, f5mq))
class mbic_pvce(Variable):
    cerfa_field = {0: '5KQ',
        1: '5LQ',
        2: '5MQ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables selon droit commun (régime micro entreprise)'
    definition_period = YEAR


# (f5ke, f5le, f5me))
class abic_pvce(Variable):
    cerfa_field = {0: '5KE',
        1: '5LE',
        2: '5ME', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values industrielles et commerciales de cession taxables selon droit commun avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5kk, f5ik, f5mk)) TODO: autre 5KK 2005/20006
class nbic_pvce(Variable):
    cerfa_field = {0: '5IK',
        1: '5KK',
        2: '5MK', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)'
    # start_date = date(2008, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5nq, f5oq, f5pq))
class macc_pvce(Variable):
    cerfa_field = {0: '5NQ',
        1: '5OQ',
        2: '5PQ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables selon droit commun (régime micro entreprise)'
    definition_period = YEAR


# (f5ne, f5oe, f5pe))
class aacc_pvce(Variable):
    cerfa_field = {0: '5NE',
        1: '5OE',
        2: '5PE', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values industrielles et commerciales non professionnelles de cession taxables selon droit commun avec CGA ou viseur (régime du bénéfice réel)'
    definition_period = YEAR


# (f5nk, f5ok, f5pk)) TODO: 5NK 2005/2006
class nacc_pvce(Variable):
    cerfa_field = {0: '5NK',
        1: '5OK',
        2: '5PK', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)'
    # start_date = date(2009, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


# (f5kv, f5lv, f5mv))
class mncn_pvce(Variable):
    cerfa_field = {0: '5KV',
        1: '5LV',
        2: '5MV', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values non commerciales non professionnelles de cession taxables selon droit commun (régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5so, f5nt, f5ot))
class cncn_pvce(Variable):
    cerfa_field = {0: '5SO',
        1: '5NT',
        2: '5OT', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values nettes non commerciales non professionnelles taxables au taux de droit commun (régime de la déclaration controlée)'
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


# (f5hr, f5ir, f5jr))
class mbnc_pvce(Variable):
    cerfa_field = {0: '5HR',
        1: '5IR',
        2: '5JR', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Plus-values non commerciales professionnelles de cession taxables selon droit commun(régime déclaratif spécial ou micro BNC)'
    definition_period = YEAR


# (f5qd, f5rd, f5sd))
class abnc_pvce(Variable):
    cerfa_field = {0: '5QD',
        1: '5RD',
        2: '5SD', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = "Plus-values non commerciaux professionnels de cession taxables selon droit commun (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qj, f5rj, f5sj)) #TODO 5*J 2005/2006 (qui se transforme en 5*D...)
class nbnc_pvce(Variable):
    cerfa_field = {0: '5QJ',
        1: '5RJ',
        2: '5SJ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)'
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class frag_fore(Variable):
    cerfa_field = {0: '5HD',
        1: '5ID',
        2: '5JD', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus des exploitants forestiers (régime du forfait)'
    # start_date = date(2007, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class arag_sjag(Variable):
    cerfa_field = {0: '5HZ',
        1: '5IZ',
        2: '5JZ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Abattement pour les jeunes agriculteurs des revenus agricoles sans CGA (régime du bénéfice réel)'
    # start_date = date(2011, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


class abic_impm(Variable):
    cerfa_field = {0: '5HA',
        1: '5IA',
        2: '5JA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Locations meublées imposables avec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)'
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class nbic_impm(Variable):
    cerfa_field = {0: '5KA',
        1: '5LA',
        2: '5MA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Locations meublées imposables sans CGA (régime du bénéfice réel)'
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class abic_defm(Variable):
    cerfa_field = {0: '5QA',
        1: '5RA',
        2: '5SA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits de locations meubléesavec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)'
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class alnp_imps(Variable):
    cerfa_field = {0: '5NA',
        1: '5OA',
        2: '5PA', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Locations meublées non professionnelles imposables avec CGA ou viseur (régime du bénéfice réel)'
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class alnp_defs(Variable):
    cerfa_field = {0: '5NY',
        1: '5OY',
        2: '5PY', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits de locations meublées non professionnelles avec CGA ou viseur (régime du bénéfice réel)'
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class nlnp_defs(Variable):
    cerfa_field = {0: '5NZ',
        1: '5OZ',
        2: '5PZ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits de locations meublées non professionnelles imposables sans CGA (régime du bénéfice réel)'
    # start_date = date(2009, 1, 1)
    end = '2022-12-31'
    definition_period = YEAR


class abnc_proc(Variable):
    cerfa_field = {0: '5TF',
        1: '5UF',
        2: '5VF', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Honoraires de prospection commerciale exonérés avec CGA ou viseur (revenus non commerciaux professionnels, régime de la déclaration contrôlée)'
    # start_date = date(2009, 1, 1)
    end = '2017-12-31'
    definition_period = YEAR


class nbnc_proc(Variable):
    cerfa_field = {0: '5TI',
        1: '5UI',
        2: '5VI', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Honoraires de prospection commerciale exonérés sans CGA (revenus non commerciaux professionnels, régime de la déclaration contrôlée)'
    # start_date = date(2009, 1, 1)
    end = '2017-12-31'
    definition_period = YEAR


class mncn_exon(Variable):
    cerfa_field = {0: '5TH',
        1: '5UH',
        2: '5VH', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus nets exonérés non commerciaux non professionnels (régime déclaratif spécial ou micro BNC)'
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class cncn_exon(Variable):
    cerfa_field = {0: '5HK',
        1: '5JK',
        2: '5LK', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus nets exonérés non commerciaux non professionnels (régime de la déclaration contrôlée)'
    # start_date = date(2008, 1, 1)
    definition_period = YEAR


class cncn_aimp(Variable):
    cerfa_field = {0: '5JG',
        1: '5RF',
        2: '5SF', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus imposables non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class cncn_adef(Variable):
    cerfa_field = {0: '5JJ',
        1: '5RG',
        2: '5SG', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Déficits non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class cncn_info(Variable):
    cerfa_field = {0: '5TC',
        1: '5UC',
        2: '5VC', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Inventeurs et auteurs de logiciels : produits taxables aux taux de droit commun revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)'
    # start_date = date(2009, 1, 1)
    end = '2018-12-31'
    definition_period = YEAR


class cncn_info_red1(Variable):
    cerfa_field = {0: '5TC',
        1: '5UC',
        2: '5VC', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Inventeurs et auteurs de logiciels : – produits taxables à 10%, déjà soumis aux CS, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)'
    # start_date = date(2019, 1, 1)
    definition_period = YEAR


class cncn_info_red2(Variable):
    cerfa_field = {0: '5QJ',
        1: '5RJ',
        2: '5SJ', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Inventeurs et auteurs de logiciels : – produits taxables à 10%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)'
    # start_date = date(2019, 1, 1)
    definition_period = YEAR


class cncn_jcre(Variable):
    cerfa_field = {0: '5SV',
        1: '5SW',
        2: '5SX', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Jeunes créateurs : abattement de 50%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)'
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class revimpres(Variable):
    cerfa_field = {0: '5HY',
        1: '5IY',
        2: '5JY', }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = 'Revenus nets à imposer aux prélèvements sociaux'
    definition_period = YEAR


class pveximpres(Variable):
    cerfa_field = {0: '5HG',
        1: '5IG', }
    value_type = int
    entity = Individu
    label = 'Plus-values à long terme exonérées en cas de départ à la retraite à imposer aux prélèvements sociaux'
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class pvtaimpres(Variable):
    cerfa_field = {0: '5HZ',
        1: '5IZ',
        2: '5JZ', }
    value_type = int
    entity = Individu
    label = 'Plus-values à long terme taxables à 16% à la retraite à imposer aux prélèvements sociaux'
    end = '2009-12-31'
    definition_period = YEAR


class f5qf(Variable):
    cerfa_field = '5QF'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus agricoles des années antérieures non encore déduits (n-6)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qg(Variable):
    cerfa_field = '5QG'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus agricoles des années antérieures non encore déduits (n-5)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qn(Variable):
    cerfa_field = '5QN'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus agricoles des années antérieures non encore déduits (n-4)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qo(Variable):
    cerfa_field = '5QO'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus agricoles des années antérieures non encore déduits (n-3)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qp(Variable):
    cerfa_field = '5QP'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus agricoles des années antérieures non encore déduits (n-2)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qq(Variable):
    cerfa_field = '5QQ'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus agricoles des années antérieures non encore déduits (n-1)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5ga(Variable):
    cerfa_field = '5GA'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-10)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gb(Variable):
    cerfa_field = '5GB'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-9)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gc(Variable):
    cerfa_field = '5GC'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-8)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gd(Variable):
    cerfa_field = '5GD'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-7)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5ge(Variable):
    cerfa_field = '5GE'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-6)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gf(Variable):
    cerfa_field = '5GF'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-5)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gg(Variable):
    cerfa_field = '5GG'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-4)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gh(Variable):
    cerfa_field = '5GH'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-3)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gi(Variable):
    cerfa_field = '5GI'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-2)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gj(Variable):
    cerfa_field = '5GJ'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-1)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5rn(Variable):
    cerfa_field = '5RN'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-6)'
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5ro(Variable):
    cerfa_field = '5RO'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-5)'
    definition_period = YEAR


class f5rp(Variable):
    cerfa_field = '5RP'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-4)'
    definition_period = YEAR


class f5rq(Variable):
    cerfa_field = '5RQ'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-3)'
    definition_period = YEAR


class f5rr(Variable):
    cerfa_field = '5RR'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-2)'
    definition_period = YEAR


class f5rw(Variable):
    cerfa_field = '5RW'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-1)'
    definition_period = YEAR


class f5ht(Variable):
    cerfa_field = '5HT'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-6)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5it(Variable):
    cerfa_field = '5IT'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-5)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5jt(Variable):
    cerfa_field = '5JT'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-4)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5kt(Variable):
    cerfa_field = '5KT'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-3)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5lt(Variable):
    cerfa_field = '5LT'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-2)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5mt(Variable):
    cerfa_field = '5MT'
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = 'Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-1)'
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5sq(Variable):
    cerfa_field = '5SQ'
    value_type = int
    entity = Individu
    definition_period = YEAR
    label = 'Déficits des années antérieures non encore déduits'
    end = '2006-12-31'


# """
# Input variables
# """


# Input mensuel


class rpns_auto_entrepreneur_CA_achat_revente(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = "Chiffre d'affaires en tant qu'auto-entrepreneur avec versement libératoire domaine ventes et assimilées "
    definition_period = MONTH

    def formula(individu, period):
        chiffre_affaire = individu('ebic_impv', period, options = [DIVIDE])

        return chiffre_affaire


class rpns_auto_entrepreneur_CA_bic(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = "Chiffre d'affaires en tant qu'auto-entrepreneur avec versement libératoire domaine prestations de service et locations meublées "
    definition_period = MONTH

    def formula(individu, period):
        chiffre_affaire = individu('ebic_imps', period, options = [DIVIDE])

        return chiffre_affaire


class rpns_auto_entrepreneur_CA_bnc(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = "Chiffre d'affaires en tant qu'auto-entrepreneur avec versement libératoire domaine non commercial"
    definition_period = MONTH

    def formula(individu, period):
        chiffre_affaire = individu('ebnc_impo', period, options = [DIVIDE])

        return chiffre_affaire


class rpns_auto_entrepreneur_chiffre_affaires(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = "Chiffre d'affaires en tant qu'auto-entrepreneur avec versement libératoire"
    definition_period = MONTH

    def formula(individu, period):
        rpns_auto_entrepreneur_CA_achat_revente = individu('rpns_auto_entrepreneur_CA_achat_revente', period)
        rpns_auto_entrepreneur_CA_bic = individu('rpns_auto_entrepreneur_CA_bic', period)
        rpns_auto_entrepreneur_CA_bnc = individu('rpns_auto_entrepreneur_CA_bnc', period)

        return rpns_auto_entrepreneur_CA_achat_revente + rpns_auto_entrepreneur_CA_bic + rpns_auto_entrepreneur_CA_bnc

# Input annuel


class rpns_micro_entreprise_CA_bnc_imp(Variable):
    value_type = float
    entity = Individu
    label = "Chiffre d'affaires micro-entreprise domaine non commercial, revenus imposables"
    definition_period = YEAR

    def formula(individu, period):
        mbnc_impo = individu('mbnc_impo', period)
        mncn_impo = individu('mncn_impo', period)

        return mbnc_impo + mncn_impo


class rpns_micro_entreprise_CA_bnc_exon(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus nets exonérés des  micro-entreprise domaine non commercial'
    definition_period = YEAR

    def formula(individu, period):
        mbnc_exon = individu('mbnc_exon', period)
        mncn_exon = individu('mncn_exon', period)

        return mbnc_exon + mncn_exon


class rpns_micro_entreprise_CA_bic_vente_imp(Variable):
    value_type = float
    entity = Individu
    label = "Chiffre d'affaires micro-entreprise domaine vente et assimilée, revenus imposables"
    definition_period = YEAR

    def formula(individu, period):
        mbic_impv = individu('mbic_impv', period)
        macc_impv = individu('macc_impv', period)

        return mbic_impv + macc_impv


class rpns_micro_entreprise_CA_bic_service_imp(Variable):
    value_type = float
    entity = Individu
    label = "Chiffre d'affaires micro-entreprise domaine service et locations, revenus imposables"
    definition_period = YEAR

    def formula(individu, period):
        mbic_imps = individu('mbic_imps', period)
        macc_imps = individu('macc_imps', period)
        aacc_imps = individu('aacc_imps', period)
        aacc_gits = individu('aacc_gits', period)
        nacc_meuc = individu('nacc_meuc', period)
        nacc_meup = individu('nacc_meup', period)

        return mbic_imps + macc_imps + aacc_imps + aacc_gits + nacc_meuc + nacc_meup


class rpns_micro_entreprise_bic_exon(Variable):
    value_type = float
    entity = Individu
    label = 'Revenus nets exonérés des micro-entreprise domaine bic'
    definition_period = YEAR

    def formula(individu, period):
        mbic_exon = individu('mbic_exon', period)
        macc_exon = individu('macc_exon', period)

        return mbic_exon + macc_exon


class rpns_micro_entreprise_chiffre_affaires(Variable):
    value_type = float
    entity = Individu
    label = "Chiffre d'affaires en micro-entreprise"
    definition_period = YEAR

    def formula(individu, period):
        rpns_micro_entreprise_CA_bnc_imp = individu('rpns_micro_entreprise_CA_bnc_imp', period)
        rpns_micro_entreprise_CA_bic_vente_imp = individu('rpns_micro_entreprise_CA_bic_vente_imp', period)
        rpns_micro_entreprise_CA_bic_service_imp = individu('rpns_micro_entreprise_CA_bic_service_imp', period)

        return rpns_micro_entreprise_CA_bnc_imp + rpns_micro_entreprise_CA_bic_vente_imp + rpns_micro_entreprise_CA_bic_service_imp


class TypesTnsTypeActivite(Enum):
    __order__ = 'achat_revente bic bnc'  # Needed to preserve the enum order in Python 2
    achat_revente = 'achat_revente'
    bic = 'bic'
    bnc = 'bnc'


# Input sur le dernier exercice. Par convention, sur l'année dernière.
class rpns_autres_revenus(Variable):
    value_type = float
    entity = Individu
    label = 'Autres revenus non salariés'
    definition_period = YEAR

    def formula(individu, period):
        abic_exon = individu('abic_exon', period)
        nbic_exon = individu('nbic_exon', period)
        abic_impn = individu('abic_impn', period)
        nbic_impn = individu('nbic_impn', period)
        aacc_exon = individu('aacc_exon', period)
        nacc_exon = individu('nacc_exon', period)
        aacc_impn = individu('aacc_impn', period)
        nacc_impn = individu('nacc_impn', period)
        alnp_imps = individu('alnp_imps', period)
        nacc_pvce = individu('nacc_pvce', period)
        abnc_exon = individu('abnc_exon', period)
        nbnc_exon = individu('nbnc_exon', period)
        abnc_impo = individu('abnc_impo', period)
        nbnc_impo = individu('nbnc_impo', period)
        cncn_exon = individu('cncn_exon', period)
        nbic_pvce = individu('nbic_pvce', period)
        cncn_aimp = individu('cncn_aimp', period)
        cncn_bene = individu('cncn_bene', period)

        return (abic_exon + nbic_exon + abic_impn + nbic_impn + aacc_exon
                + nacc_exon + aacc_impn + nacc_impn + alnp_imps + nacc_pvce
                + abnc_exon + nbnc_exon + abnc_impo + nbnc_impo + cncn_exon
                + nbic_pvce + cncn_aimp + cncn_bene)


class rpns_autres_revenus_chiffre_affaires(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = "Chiffre d'affaire pour les TNS non agricoles autres que les AE et ME"
    definition_period = MONTH

    # les chiffres d'affaire ne sont pas dans les cases fiscales


class tns_autres_revenus_type_activite(Variable):
    value_type = Enum
    possible_values = TypesTnsTypeActivite
    default_value = TypesTnsTypeActivite.achat_revente
    entity = Individu
    label = "Type d'activité de l'entreprise non AE ni ME"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class tns_avec_employe(Variable):
    value_type = bool
    entity = Individu
    set_input = set_input_dispatch_by_period
    label = "Le TNS a au moins un employé. Ne s'applique pas pour les agricoles ni auto-entrepreneurs ni micro entreprise"
    definition_period = MONTH


# Input annuel


class rpns_benefice_exploitant_agricole(Variable):
    value_type = float
    entity = Individu
    label = 'Dernier bénéfice agricole'
    definition_period = YEAR

    def formula_2016_01_01(individu, period):
        rpns_revenus_microBA_agricole = individu('rpns_revenus_microBA_agricole', period)
        arag_exon = individu('arag_exon', period)
        arag_impg = individu('arag_impg', period)
        return rpns_revenus_microBA_agricole + arag_exon + arag_impg

    def formula(individu, period):
        rpns_revenus_forfait_agricole = individu('rpns_revenus_forfait_agricole', period)
        arag_exon = individu('arag_exon', period)
        arag_impg = individu('arag_impg', period)
        return rpns_revenus_forfait_agricole + arag_exon + arag_impg


# Computed variables


class travailleur_non_salarie(Variable):
    label = "L'individu a une activité professionnelle non salariée"
    value_type = bool
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        this_year_and_last_year = Period(('year', period.start.offset('first-of', 'year'), 2)).offset(-1)
        rpns_auto_entrepreneur_chiffre_affaires = individu('rpns_auto_entrepreneur_chiffre_affaires', period) != 0
        rpns_micro_entreprise_chiffre_affaires = individu('rpns_micro_entreprise_chiffre_affaires', this_year_and_last_year, options = [ADD]) != 0
        rpns_autres_revenus = individu('rpns_autres_revenus', this_year_and_last_year, options = [ADD]) != 0
        rpns_benefice_exploitant_agricole = individu('rpns_benefice_exploitant_agricole', this_year_and_last_year, options = [ADD]) != 0
        rpns_autres_revenus_chiffre_affaires = individu('rpns_autres_revenus_chiffre_affaires', this_year_and_last_year, options = [ADD]) != 0

        result = (
            rpns_auto_entrepreneur_chiffre_affaires
            + rpns_micro_entreprise_chiffre_affaires
            + rpns_autres_revenus
            + rpns_benefice_exploitant_agricole
            + rpns_autres_revenus_chiffre_affaires
            )

        return result


class rpns_auto_entrepreneur_benefice(Variable):
    value_type = float
    label = "Bénéfice en tant qu'auto-entrepreneur avec versement libératoire"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2008_01_01(individu, period, parameters):
        rpns_auto_entrepreneur_CA_achat_revente = individu('rpns_auto_entrepreneur_CA_achat_revente', period)
        rpns_auto_entrepreneur_CA_bic = individu('rpns_auto_entrepreneur_CA_bic', period)
        rpns_auto_entrepreneur_CA_bnc = individu('rpns_auto_entrepreneur_CA_bnc', period)

        bareme = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        benefice = ((rpns_auto_entrepreneur_CA_achat_revente * (1 - bareme.microentreprise.regime_micro_bnc.marchandises.taux))
                    + (rpns_auto_entrepreneur_CA_bnc * (1 - bareme.microentreprise.regime_micro_bnc.taux))
                    + (rpns_auto_entrepreneur_CA_bic * (1 - bareme.microentreprise.regime_micro_bnc.services.taux)))

        return benefice


class rpns_micro_entreprise_benefice(Variable):
    value_type = float
    label = 'Bénéfice de la micro entreprise'
    entity = Individu
    definition_period = YEAR
    set_input = set_input_divide_by_period

    def formula_2008_01_01(individu, period, parameters):
        rpns_micro_entreprise_CA_bnc_imp = individu('rpns_micro_entreprise_CA_bnc_imp', period)
        rpns_micro_entreprise_CA_bic_vente_imp = individu('rpns_micro_entreprise_CA_bic_vente_imp', period)
        rpns_micro_entreprise_CA_bic_service_imp = individu('rpns_micro_entreprise_CA_bic_service_imp', period)
        rpns_micro_entreprise_CA_bnc_exon = individu('rpns_micro_entreprise_CA_bnc_exon', period)
        rpns_micro_entreprise_bic_exon = individu('rpns_micro_entreprise_bic_exon', period)

        bareme = parameters(period).impot_revenu.calcul_revenus_imposables.rpns.micro

        benefice = ((rpns_micro_entreprise_CA_bic_vente_imp * (1 - bareme.microentreprise.regime_micro_bnc.marchandises.taux))
                    + (rpns_micro_entreprise_CA_bnc_imp * (1 - bareme.microentreprise.regime_micro_bnc.taux))
                    + (rpns_micro_entreprise_CA_bic_service_imp * (1 - bareme.microentreprise.regime_micro_bnc.services.taux))
                    + rpns_micro_entreprise_CA_bnc_exon
                    + rpns_micro_entreprise_bic_exon)

        return benefice


# The following formulas take into account 'cotisation sociales'. However, it seems that for all prestations,
# the 'base ressources' are only using the 'benefice', without deducting the 'cotisation sociales'.
# Although this rule seems unfair towards independent workers, we are now applying it for all presations and therefore
# we are not using the following formulas for calculating prestations_sociales.
# This seemingly unfair method is however explained by the fact that the rate allowing to go from 'CA' to 'base_ressources' already takes into account
# the 'cotisations sociales', as both are directly computed from the same 'CA'. The main point of 'versement liberatoire' and 'micro-social' is to avoid to compute a true 'benefice',
# and so doing it in two steps would not be more accurate (it would be indeed unfair if the computed 'benefices' were actual 'benefices' before 'cotisations sociales' :
# in this case, one could however take a real 'benefice' taxation scheme).


class rpns_auto_entrepreneur_revenus_net(Variable):
    value_type = float
    label = "Revenu d'un auto-entrepreneur avec versement libératoire"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2008_01_01(individu, period, parameters):
        rpns_auto_entrepreneur_benefice = individu('rpns_auto_entrepreneur_benefice', period)
        rpns_auto_entrepreneur_CA_achat_revente = individu('rpns_auto_entrepreneur_CA_achat_revente', period)
        rpns_auto_entrepreneur_CA_bic = individu('rpns_auto_entrepreneur_CA_bic', period)
        rpns_auto_entrepreneur_CA_bnc = individu('rpns_auto_entrepreneur_CA_bnc', period)
        bareme_cs_ae = parameters(period).prelevements_sociaux.professions_liberales.auto_entrepreneur

        rpns_auto_entrepreneur_charges_sociales = (
            (bareme_cs_ae.formation_professionnelle.ventecom_chiffre_affaires + bareme_cs_ae.cotisations_prestations.vente) * rpns_auto_entrepreneur_CA_achat_revente
            + (bareme_cs_ae.formation_professionnelle.artisans_hors_alsace_chiffre_affaires + bareme_cs_ae.cotisations_prestations.cipav) * rpns_auto_entrepreneur_CA_bic
            + (bareme_cs_ae.formation_professionnelle.servicecom_chiffre_affaires + bareme_cs_ae.cotisations_prestations.service) * rpns_auto_entrepreneur_CA_bnc
            )

        return rpns_auto_entrepreneur_benefice - rpns_auto_entrepreneur_charges_sociales


class rpns_micro_entreprise_revenus_net(Variable):
    value_type = float
    label = "Revenu d'un TNS dans une micro-entreprise"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        rpns_micro_entreprise_benefice = individu('rpns_micro_entreprise_benefice', period, options = [DIVIDE])
        bareme_cs_me = parameters(period).prelevements_sociaux.professions_liberales.auto_entrepreneur
        rpns_micro_entreprise_charges_sociales = (
            (rpns_micro_entreprise_CA_bic_vente_imp * (bareme_cs_me.formation_professionnelle.ventecom_chiffre_affaires + bareme_cs_me.cotisations_prestations.vente))
            + (rpns_micro_entreprise_CA_bnc_imp * (bareme_cs_me.formation_professionnelle.artisans_hors_alsace_chiffre_affaires + bareme_cs_me.cotisations_prestations.cipav))
            + (rpns_micro_entreprise_CA_bic_service_imp * (bareme_cs_me.formation_professionnelle.servicecom_chiffre_affaires + bareme_cs_me.cotisations_prestations.service))
            )
        revenus = rpns_micro_entreprise_benefice - rpns_micro_entreprise_charges_sociales

        return revenus
