# -*- coding: utf-8 -*-

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
    cerfa_field = {0: u"5QM",
        1: u"5RM",
                   }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Agents généraux d’assurances: indemnités de cessation d’activité"
    definition_period = YEAR


# """
# Revenus des professions non salariées
# """

# (f5nv, f5ov, f5pv)
class ppe_du_ns(Variable):
    cerfa_field = {0: u"5NV",
        1: u"5OV",
        2: u"5PV",
                   }
    value_type = int
    entity = Individu
    label = u"Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année"
    end = '2014-12-31'
    definition_period = YEAR


# (f5nw, f5ow, f5pw)
class ppe_tp_ns(Variable):
    cerfa_field = {0: u"5NW",
        1: u"5OW",
        2: u"5PW",
                   }
    value_type = bool
    entity = Individu
    label = u"Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière"
    end = '2014-12-31'
    definition_period = YEAR


# (f5hn, f5in, f5jn))
class frag_exon(Variable):
    cerfa_field = {0: u"5HN",
        1: u"5IN",
        2: u"5JN", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus agricoles exonérés (régime du forfait)"
    # start_date = date(2007, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


# (f5ho, f5io, f5jo))
class frag_impo(Variable):
    cerfa_field = {0: u"5HO",
        1: u"5IO",
        2: u"5JO", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus agricoles imposables (régime du forfait)"
    # start_date = date(2007, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


# (f5hb, f5ib, f5jb))
class arag_exon(Variable):
    cerfa_field = {0: u"5HB",
        1: u"5IB",
        2: u"5JB", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hc, f5ic, f5jc))
class arag_impg(Variable):
    cerfa_field = {0: u"5HC",
        1: u"5IC",
        2: u"5JC", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hf, f5if, f5jf))
class arag_defi(Variable):
    cerfa_field = {0: u"5HF",
        1: u"5IF",
        2: u"5JF", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hh, f5ih, f5jh))
class nrag_exon(Variable):
    cerfa_field = {0: u"5HH",
        1: u"5IH",
        2: u"5JH", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hi, f5ii, f5ji))
class nrag_impg(Variable):
    cerfa_field = {0: u"5HI",
        1: u"5II",
        2: u"5JI", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hl, f5il, f5jl))
class nrag_defi(Variable):
    cerfa_field = {0: u"5HL",
        1: u"5IL",
        2: u"5JL", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5hm, f5im, f5jm))
class nrag_ajag(Variable):
    cerfa_field = {0: u"5HM",
        1: u"5IM",
        2: u"5JM", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# """
# Autoentrepreneur
# """


# (f5ta, f5ua, f5va))
class ebic_impv(Variable):
    cerfa_field = {0: u"5TA",
        1: u"5UA",
        2: u"5VA", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur)"
    # start_date = date(2009, 1, 1)
    # end = '2016-12-31'
    definition_period = YEAR


# (f5tb, f5ub, f5vb))
class ebic_imps(Variable):
    cerfa_field = {0: u"5TB",
        1: u"5UB",
        2: u"5VB", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)"
    # start_date = date(2009, 1, 1)
    # end = '2016-12-31'
    definition_period = YEAR


# (f5te, f5ue, f5ve))
class ebnc_impo(Variable):
    cerfa_field = {0: u"5TE",
        1: u"5UE",
        2: u"5VE", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux (régime auto-entrepreneur ayant opté pour le versement libératoire)"
    # start_date = date(2009, 1, 1)
    # end = '2016-12-31'
    definition_period = YEAR


# (f5kn, f5ln, f5mn))
class mbic_exon(Variable):
    cerfa_field = {0: u"5KN",
        1: u"5LN",
        2: u"5MN", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)"
    definition_period = YEAR


# (f5kb, f5lb, f5mb))
class abic_exon(Variable):
    cerfa_field = {0: u"5KB",
        1: u"5LB",
        2: u"5MB", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5kh, f5lh, f5mh))
class nbic_exon(Variable):
    cerfa_field = {0: u"5KH",
        1: u"5LH",
        2: u"5MH", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)"
    definition_period = YEAR


# (f5ko, f5lo, f5mo))
class mbic_impv(Variable):
    cerfa_field = {0: u"5KO",
        1: u"5LO",
        2: u"5MO", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)"
    definition_period = YEAR


# (f5kp, f5lp, f5mp))
class mbic_imps(Variable):
    cerfa_field = {0: u"5KP",
        1: u"5LP",
        2: u"5MP", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)"
    definition_period = YEAR


# (f5kc, f5lc, f5mc))
class abic_impn(Variable):
    cerfa_field = {0: u"5KC",
        1: u"5LC",
        2: u"5MC", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5kd, f5ld, f5md))
class abic_imps(Variable):
    cerfa_field = {0: u"5KD",
        1: u"5LD",
        2: u"5MD", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)"
    end = '2009-12-31'
    definition_period = YEAR


# (f5ki, f5li, f5mi))
class nbic_impn(Variable):
    cerfa_field = {0: u"5KI",
        1: u"5LI",
        2: u"5MI", }

    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)"
    definition_period = YEAR


# """
# Réutilisation cases 2013
# """


# (f5kj, f5lj, f5mj))
class nbic_imps(Variable):
    cerfa_field = {0: u"5KJ",
        1: u"5LJ",
        2: u"5MJ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: régime simplifié sans CGA (régime du bénéfice réel)"
    end = '2009-12-31'
    definition_period = YEAR


# (f5kj, f5lj, f5mj))
# NB cette variable devrait s'appeler 'mbic_mvct' comme c'est une variable de régime micro (mais il
# existe déjà une variable mbic_mvct avec un autre cerfa_fiel (5HU) corresponsant à avant 2012...)
class nbic_mvct(Variable):
    cerfa_field = {0: u"5KJ",
        1: u"5LJ",
        2: u"5MJ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels moins-values nettes à court terme : régime micro-entreprise"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5kf, f5lf, f5mf))
class abic_defn(Variable):
    cerfa_field = {0: u"5KF",
        1: u"5LF",
        2: u"5MF", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5kg, f5lg, f5mg))
# vérif <=2012
class abic_defs(Variable):
    cerfa_field = {0: u"5KG",
        1: u"5LG",
        2: u"5MG", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)"
    end = '2009-12-01'
    definition_period = YEAR


# (f5kl, f5ll, f5ml))
class nbic_defn(Variable):
    cerfa_field = {0: u"5KL",
        1: u"5LL",
        2: u"5ML", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)"
    definition_period = YEAR


# (f5km, f5lm, f5mm))
class nbic_defs(Variable):
    cerfa_field = {0: u"5KM",
        1: u"5LM",
        2: u"5MM", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)"
    end = '2009-12-31'
    definition_period = YEAR


# (f5ks, f5ls, f5ms))
class nbic_apch(Variable):
    cerfa_field = {0: u"5KS",
        1: u"5LS",
        2: u"5MS", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5nn, f5on, f5pn))
class macc_exon(Variable):
    cerfa_field = {0: u"5NN",
        1: u"5ON",
        2: u"5PN", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)"
    definition_period = YEAR


# (f5nb, f5ob, f5pb))
class aacc_exon(Variable):
    cerfa_field = {0: u"5NB",
        1: u"5OB",
        2: u"5PB", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5nh, f5oh, f5ph))
class nacc_exon(Variable):
    cerfa_field = {0: u"5NH",
        1: u"5OH",
        2: u"5PH", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)"
    definition_period = YEAR


# (f5no, f5oo, f5po))
class macc_impv(Variable):
    cerfa_field = {0: u"5NO",
        1: u"5OO",
        2: u"5PO", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)"
    definition_period = YEAR


# (f5np, f5op, f5pp))
class macc_imps(Variable):
    cerfa_field = {0: u"5NP",
        1: u"5OP",
        2: u"5PP", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)"
    definition_period = YEAR


# (f5nc, f5oc, f5pc))
class aacc_impn(Variable):
    cerfa_field = {0: u"5NC",
        1: u"5OC",
        2: u"5PC", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5nd, f5od, f5pd)) #TODO: avant 2010
class aacc_imps(Variable):
    cerfa_field = {0: u"5ND",
        1: u"5OD",
        2: u"5PD", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations meublées non professionnelles (régime micro entreprise)"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


# (f5nf, f5of, f5pf))
class aacc_defn(Variable):
    cerfa_field = {0: u"5NF",
        1: u"5OF",
        2: u"5PF", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5ng, f5og, f5pg))
class aacc_gits(Variable):
    cerfa_field = {0: u"5NG",
        1: u"5OG",
        2: u"5PG", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


# (f5ni, f5oi, f5pi))
class nacc_impn(Variable):
    cerfa_field = {0: u"5NI",
        1: u"5OI",
        2: u"5PI", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)"
    definition_period = YEAR


# (f5ng, f5og, f5pg))
class aacc_defs(Variable):
    cerfa_field = {0: u"5NG",
        1: u"5OG",
        2: u"5PG", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits de revenus industriels et commerciaux non professionnels avec CGA (régime simplifié du bénéfice réel)"
    end = '2009-12-31'
    definition_period = YEAR


# (f5nj, f5oj, f5pj)) #TODO: dates 5PJ, 5PG, 5PD, 5OM
class nacc_meup(Variable):
    cerfa_field = {0: u"5NJ",
        1: u"5OJ",
        2: u"5PJ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5nl, f5ol, f5pl))
class nacc_defn(Variable):
    cerfa_field = {0: u"5NL",
        1: u"5OL",
        2: u"5PL", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)"
    definition_period = YEAR


# (f5nm, f5om, f5pm)) #TODO autres 5NM
class nacc_defs(Variable):
    cerfa_field = {0: u"5NM",
        1: u"5OM",
        2: u"5PM", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations meublées non professionnelles: Gîtes ruraux et chambres d'hôtes déjà soumis aux prélèvements sociaux avec CGA (régime du bénéfice réel)"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5ku, f5lu, f5mu))
class mncn_impo(Variable):
    cerfa_field = {0: u"5KU",
        1: u"5LU",
        2: u"5MU", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5sn, f5ns, f5os))
class cncn_bene(Variable):
    cerfa_field = {0: u"5SN",
        1: u"5NS",
        2: u"5OS", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


# (f5sp, f5nu, f5ou, f5sr))
# pas de f5sr en 2013
class cncn_defi(Variable):
    cerfa_field = {0: u"5SP",
        1: u"5NU",
        2: u"5OU", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


# (f5hp, f5ip, f5jp))
class mbnc_exon(Variable):
    cerfa_field = {0: u"5HP",
        1: u"5IP",
        2: u"5JP", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5qb, f5rb, f5sb))
class abnc_exon(Variable):
    cerfa_field = {0: u"5QB",
        1: u"5RB",
        2: u"5SB", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qh, f5rh, f5sh))
class nbnc_exon(Variable):
    cerfa_field = {0: u"5QH",
        1: u"5RH",
        2: u"5SH", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"
    definition_period = YEAR


# (f5hq, f5iq, f5jq))
class mbnc_impo(Variable):
    cerfa_field = {0: u"5HQ",
        1: u"5IQ",
        2: u"5JQ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5qc, f5rc, f5sc))
class abnc_impo(Variable):
    cerfa_field = {0: u"5QC",
        1: u"5RC",
        2: u"5SC", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qe, f5re, f5se))
class abnc_defi(Variable):
    cerfa_field = {0: u"5QE",
        1: u"5RE",
        2: u"5SE", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qi, f5ri, f5si))
class nbnc_impo(Variable):
    cerfa_field = {0: u"5QI",
        1: u"5RI",
        2: u"5SI", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"
    definition_period = YEAR


# (f5qk, f5rk, f5sk))
class nbnc_defi(Variable):
    cerfa_field = {0: u"5QK",
        1: u"5RK",
        2: u"5SK", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"
    definition_period = YEAR


# (f5hu))
# vérif <=2012
class mbic_mvct(Variable):
    cerfa_field = u"5HU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)"
    end = '2011-12-31'
    definition_period = YEAR


# (f5iu))
class macc_mvct(Variable):
    cerfa_field = u"5IU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)"
    definition_period = YEAR


# (f5ju))
class mncn_mvct(Variable):
    cerfa_field = u"5JU"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5kz, f5lz , f5mz), f5lz , f5mz sont présentent en 2013
class mbnc_mvct(Variable):
    cerfa_field = {0: u"5KZ",  # TODO: pb cerfa field
        1: u"5LZ",
        2: u"5MZ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)"
    # start_date = date(2012, 1, 1)
    definition_period = YEAR


# (f5hw, f5iw, f5jw))
class frag_pvct(Variable):
    cerfa_field = {0: u"5HW",
        1: u"5IW",
        2: u"5JW", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values agricoles  à court terme (régime du forfait)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5kx, f5lx, f5mx))
class mbic_pvct(Variable):
    cerfa_field = {0: u"5KX",
        1: u"5LX",
        2: u"5MX", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)"
    definition_period = YEAR


# (f5nx, f5ox, f5px))
class macc_pvct(Variable):
    cerfa_field = {0: u"5NX",
        1: u"5OX",
        2: u"5PX", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)"
    definition_period = YEAR


# (f5hv, f5iv, f5jv))
class mbnc_pvct(Variable):
    cerfa_field = {0: u"5HV",
        1: u"5IV",
        2: u"5JV", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5ky, f5ly, f5my))
class mncn_pvct(Variable):
    cerfa_field = {0: u"5KY",
        1: u"5LY",
        2: u"5MY", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5kr, f5lr, f5mr))
class mbic_mvlt(Variable):
    cerfa_field = {0: u"5KR",
        1: u"5LR",
        2: u"5MR", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)"
    definition_period = YEAR


# (f5nr, f5or, f5pr))
class macc_mvlt(Variable):
    cerfa_field = {0: u"5NR",
        1: u"5OR",
        2: u"5PR", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)"
    definition_period = YEAR


# (f5kw, f5lw, f5mw))
class mncn_mvlt(Variable):
    cerfa_field = {0: u"5KW",
        1: u"5LW",
        2: u"5MW", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5hs, f5is, f5js))
class mbnc_mvlt(Variable):
    cerfa_field = {0: u"5HS",
        1: u"5IS",
        2: u"5JS", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5hx, f5ix, f5jx))
class frag_pvce(Variable):
    cerfa_field = {0: u"5HX",
        1: u"5IX",
        2: u"5JX", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values agricoles de cession (régime du forfait)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# (f5he, f5ie, f5je))
class arag_pvce(Variable):
    cerfa_field = {0: u"5HE",
        1: u"5IE",
        2: u"5JE", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


# TODO: vérif <=2012))  # (f5hk, f5lk, f5jk) codent autre chose sur d'autres années),
class nrag_pvce(Variable):
    cerfa_field = {0: u"5HK",
        1: u"5LK",
        2: u"5JK", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    end = '2006-12-31'
    definition_period = YEAR


# (f5kq, f5lq, f5mq))
class mbic_pvce(Variable):
    cerfa_field = {0: u"5KQ",
        1: u"5LQ",
        2: u"5MQ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)"
    definition_period = YEAR


# (f5ke, f5le, f5me))
class abic_pvce(Variable):
    cerfa_field = {0: u"5KE",
        1: u"5LE",
        2: u"5ME", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5kk, f5ik, f5mk)) TODO: autre 5KK 2005/20006
class nbic_pvce(Variable):
    cerfa_field = {0: u"5IK",
        1: u"5KK",
        2: u"5MK", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)"
    # start_date = date(2008, 1, 1)
    definition_period = YEAR


# (f5nq, f5oq, f5pq))
class macc_pvce(Variable):
    cerfa_field = {0: u"5NQ",
        1: u"5OQ",
        2: u"5PQ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)"
    definition_period = YEAR


# (f5ne, f5oe, f5pe))
class aacc_pvce(Variable):
    cerfa_field = {0: u"5NE",
        1: u"5OE",
        2: u"5PE", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)"
    definition_period = YEAR


# (f5nk, f5ok, f5pk)) TODO: 5NK 2005/2006
class nacc_pvce(Variable):
    cerfa_field = {0: u"5NK",
        1: u"5OK",
        2: u"5PK", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


# (f5kv, f5lv, f5mv))
class mncn_pvce(Variable):
    cerfa_field = {0: u"5KV",
        1: u"5LV",
        2: u"5MV", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5so, f5nt, f5ot))
class cncn_pvce(Variable):
    cerfa_field = {0: u"5SO",
        1: u"5NT",
        2: u"5OT", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


# (f5hr, f5ir, f5jr))
class mbnc_pvce(Variable):
    cerfa_field = {0: u"5HR",
        1: u"5IR",
        2: u"5JR", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)"
    definition_period = YEAR


# (f5qd, f5rd, f5sd))
class abnc_pvce(Variable):
    cerfa_field = {0: u"5QD",
        1: u"5RD",
        2: u"5SD", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"
    definition_period = YEAR


# (f5qj, f5rj, f5sj)) #TODO 5*J 2005/2006 (qui se transforme en 5*D...)
class nbnc_pvce(Variable):
    cerfa_field = {0: u"5QJ",
        1: u"5RJ",
        2: u"5SJ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)"
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class frag_fore(Variable):
    cerfa_field = {0: u"5HD",
        1: u"5ID",
        2: u"5JD", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus des exploitants forestiers (régime du forfait)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class arag_sjag(Variable):
    cerfa_field = {0: u"5HZ",
        1: u"5IZ",
        2: u"5JZ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Abattement pour les jeunes agriculteurs des revenus agricoles sans CGA (régime du bénéfice réel)"
    # start_date = date(2011, 1, 1)
    definition_period = YEAR


class abic_impm(Variable):
    cerfa_field = {0: u"5HA",
        1: u"5IA",
        2: u"5JA", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations meublées imposables avec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)"
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class nbic_impm(Variable):
    cerfa_field = {0: u"5KA",
        1: u"5LA",
        2: u"5MA", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations meublées imposables sans CGA (régime du bénéfice réel)"
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class abic_defm(Variable):
    cerfa_field = {0: u"5QA",
        1: u"5RA",
        2: u"5SA", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits de locations meubléesavec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)"
    # start_date = date(2009, 1, 1)
    end = '2015-12-31'
    definition_period = YEAR


class alnp_imps(Variable):
    cerfa_field = {0: u"5NA",
        1: u"5OA",
        2: u"5PA", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Locations meublées non professionnelles imposables avec CGA ou viseur (régime du bénéfice réel)"
    # start_date = date(2009, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class alnp_defs(Variable):
    cerfa_field = {0: u"5NY",
        1: u"5OY",
        2: u"5PY", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits de locations meublées non professionnelles avec CGA ou viseur (régime du bénéfice réel)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class nlnp_defs(Variable):
    cerfa_field = {0: u"5NZ",
        1: u"5OZ",
        2: u"5PZ", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits de locations meublées non professionnelles imposables sans CGA (régime du bénéfice réel)"
    # start_date = date(2009, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class cbnc_assc(Variable):
    cerfa_field = {0: u"5QM",
        1: u"5RM", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Agents généraux d'assurances : indemnités de cessation d'activité (revenus non commerciaux professionnels, régime de la déclaration contrôlée)"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class abnc_proc(Variable):
    cerfa_field = {0: u"5TF",
        1: u"5UF",
        2: u"5VF", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Honoraires de prospection commerciale exonérés avec CGA ou viseur (revenus non commerciaux professionnels, régime de la déclaration contrôlée)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class nbnc_proc(Variable):
    cerfa_field = {0: u"5TI",
        1: u"5UI",
        2: u"5VI", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Honoraires de prospection commerciale exonérés sans CGA (revenus non commerciaux professionnels, régime de la déclaration contrôlée)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class mncn_exon(Variable):
    cerfa_field = {0: u"5TH",
        1: u"5UH",
        2: u"5VH", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus nets exonérés non commerciaux non professionnels (régime déclaratif spécial ou micro BNC)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class cncn_exon(Variable):
    cerfa_field = {0: u"5HK",
        1: u"5JK",
        2: u"5LK", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus nets exonérés non commerciaux non professionnels (régime de la déclaration contrôlée)"
    # start_date = date(2008, 1, 1)
    definition_period = YEAR


class cncn_aimp(Variable):
    cerfa_field = {0: u"5JG",
        1: u"5RF",
        2: u"5SF", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus imposables non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class cncn_adef(Variable):
    cerfa_field = {0: u"5JJ",
        1: u"5RG",
        2: u"5SG", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Déficits non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class cncn_info(Variable):
    cerfa_field = {0: u"5TC",
        1: u"5UC",
        2: u"5VC", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Inventeurs et auteurs de logiciels : produits taxables à 16%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    # start_date = date(2009, 1, 1)
    definition_period = YEAR


class cncn_jcre(Variable):
    cerfa_field = {0: u"5SV",
        1: u"5SW",
        2: u"5SX", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Jeunes créateurs : abattement de 50%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class revimpres(Variable):
    cerfa_field = {0: u"5HY",
        1: u"5IY",
        2: u"5JY", }
    value_type = int
    unit = 'currency'
    entity = Individu
    label = u"Revenus nets à imposer aux prélèvements sociaux"
    definition_period = YEAR


class pveximpres(Variable):
    cerfa_field = {0: u"5HG",
        1: u"5IG", }
    value_type = int
    entity = Individu
    label = u"Plus-values à long terme exonérées en cas de départ à la retraite à imposer aux prélèvements sociaux"
    # start_date = date(2006, 1, 1)
    definition_period = YEAR


class pvtaimpres(Variable):
    cerfa_field = {0: u"5HZ",
        1: u"5IZ",
        2: u"5JZ", }
    value_type = int
    entity = Individu
    label = u"Plus-values à long terme taxables à 16% à la retraite à imposer aux prélèvements sociaux"
    end = '2009-12-31'
    definition_period = YEAR


class f5qf(Variable):
    cerfa_field = u"5QF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-6)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qg(Variable):
    cerfa_field = u"5QG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-5)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qn(Variable):
    cerfa_field = u"5QN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-4)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qo(Variable):
    cerfa_field = u"5QO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-3)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qp(Variable):
    cerfa_field = u"5QP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-2)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5qq(Variable):
    cerfa_field = u"5QQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-1)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5ga(Variable):
    cerfa_field = u"5GA"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-10)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gb(Variable):
    cerfa_field = u"5GB"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-9)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gc(Variable):
    cerfa_field = u"5GC"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-8)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gd(Variable):
    cerfa_field = u"5GD"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-7)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5ge(Variable):
    cerfa_field = u"5GE"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-6)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gf(Variable):
    cerfa_field = u"5GF"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-5)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gg(Variable):
    cerfa_field = u"5GG"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-4)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gh(Variable):
    cerfa_field = u"5GH"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-3)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gi(Variable):
    cerfa_field = u"5GI"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-2)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5gj(Variable):
    cerfa_field = u"5GJ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-1)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5rn(Variable):
    cerfa_field = u"5RN"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-6)"
    # start_date = date(2010, 1, 1)
    end = '2010-12-31'
    definition_period = YEAR


class f5ro(Variable):
    cerfa_field = u"5RO"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-5)"
    definition_period = YEAR


class f5rp(Variable):
    cerfa_field = u"5RP"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-4)"
    definition_period = YEAR


class f5rq(Variable):
    cerfa_field = u"5RQ"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-3)"
    definition_period = YEAR


class f5rr(Variable):
    cerfa_field = u"5RR"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-2)"
    definition_period = YEAR


class f5rw(Variable):
    cerfa_field = u"5RW"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-1)"
    definition_period = YEAR


class f5ht(Variable):
    cerfa_field = u"5HT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-6)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5it(Variable):
    cerfa_field = u"5IT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-5)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5jt(Variable):
    cerfa_field = u"5JT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-4)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5kt(Variable):
    cerfa_field = u"5KT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-3)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5lt(Variable):
    cerfa_field = u"5LT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-2)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5mt(Variable):
    cerfa_field = u"5MT"
    value_type = int
    unit = 'currency'
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-1)"
    # start_date = date(2007, 1, 1)
    definition_period = YEAR


class f5sq(Variable):
    value_type = int
    entity = Individu
    definition_period = YEAR


# TODO: Introduit par mes aides à consolider

# """
# Input variables
# """


# Input mensuel


class tns_auto_entrepreneur_chiffre_affaires(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaires en tant qu'auto-entrepreneur"
    definition_period = MONTH


# Input annuel


class tns_micro_entreprise_chiffre_affaires(Variable):
    value_type = float
    entity = Individu
    label = u"Chiffre d'affaires en de micro-entreprise"
    definition_period = YEAR


class TypesTnsTypeActivite(Enum):
    __order__ = 'achat_revente bic bnc'  # Needed to preserve the enum order in Python 2
    achat_revente = u'achat_revente'
    bic = u'bic'
    bnc = u'bnc'


# TODO remove this ugly ETERNITY
class tns_auto_entrepreneur_type_activite(Variable):
    value_type = Enum
    possible_values = TypesTnsTypeActivite
    default_value = TypesTnsTypeActivite.achat_revente
    entity = Individu
    label = u"Type d'activité de l'auto-entrepreneur"
    definition_period = ETERNITY


# TODO remove this ugly ETERNITY
class tns_micro_entreprise_type_activite(Variable):
    value_type = Enum
    possible_values = TypesTnsTypeActivite
    default_value = TypesTnsTypeActivite.achat_revente
    entity = Individu
    label = u"Type d'activité de la micro-entreprise"
    definition_period = ETERNITY


# Input sur le dernier exercice. Par convention, sur l'année dernière.
class tns_autres_revenus(Variable):
    value_type = float
    entity = Individu
    label = u"Autres revenus non salariés"
    definition_period = YEAR


class tns_autres_revenus_chiffre_affaires(Variable):
    value_type = float
    entity = Individu
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaire pour les TNS non agricoles autres que les AE et ME"
    definition_period = MONTH


class tns_autres_revenus_type_activite(Variable):
    value_type = Enum
    possible_values = TypesTnsTypeActivite
    default_value = TypesTnsTypeActivite.achat_revente
    entity = Individu
    label = u"Type d'activité de l'entreprise non AE ni ME"
    definition_period = MONTH


class tns_avec_employe(Variable):
    value_type = bool
    entity = Individu
    set_input = set_input_dispatch_by_period
    label = u"Le TNS a au moins un employé. Ne s'applique pas pour les agricoles ni auto-entrepreneurs ni micro entreprise"
    definition_period = MONTH


# Input annuel


class tns_benefice_exploitant_agricole(Variable):
    value_type = float
    entity = Individu
    label = u"Dernier bénéfice agricole"
    definition_period = YEAR


# Computed variables


class travailleur_non_salarie(Variable):
    label = u"L'individu a une activité professionnelle non salariée"
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        this_year_and_last_year = period.start.offset('first-of', 'year').period('year', 2).offset(-1)
        tns_auto_entrepreneur_chiffre_affaires = individu('tns_auto_entrepreneur_chiffre_affaires', period) != 0
        tns_micro_entreprise_chiffre_affaires = individu('tns_micro_entreprise_chiffre_affaires', this_year_and_last_year, options = [ADD]) != 0
        tns_autres_revenus = individu('tns_autres_revenus', this_year_and_last_year, options = [ADD]) != 0
        tns_benefice_exploitant_agricole = individu('tns_benefice_exploitant_agricole', this_year_and_last_year, options = [ADD]) != 0
        tns_autres_revenus_chiffre_affaires = individu('tns_autres_revenus_chiffre_affaires', this_year_and_last_year, options = [ADD]) != 0

        result = (
            tns_auto_entrepreneur_chiffre_affaires
            + tns_micro_entreprise_chiffre_affaires
            + tns_autres_revenus
            + tns_benefice_exploitant_agricole
            + tns_autres_revenus_chiffre_affaires
            )

        return result


# Auxiliary function
def compute_benefice_auto_entrepreneur_micro_entreprise(bareme, type_activite, chiffre_affaire):
    abatt_fp_me = bareme.micro_entreprise.abattement_forfaitaire_fp
    benefice = chiffre_affaire * (
        1
        - (type_activite == TypesTnsTypeActivite.achat_revente) * abatt_fp_me.achat_revente
        - (type_activite == TypesTnsTypeActivite.bic) * abatt_fp_me.bic
        - (type_activite == TypesTnsTypeActivite.bnc) * abatt_fp_me.bnc
        )

    return benefice


class tns_auto_entrepreneur_benefice(Variable):
    value_type = float
    label = u"Bénéfice en tant qu'auto-entrepreneur"
    entity = Individu
    definition_period = MONTH

    def formula_2008_01_01(individu, period, parameters):
        tns_auto_entrepreneur_type_activite = individu('tns_auto_entrepreneur_type_activite', period)
        tns_auto_entrepreneur_chiffre_affaires = individu('tns_auto_entrepreneur_chiffre_affaires', period)
        bareme = parameters(period).tns

        benefice = compute_benefice_auto_entrepreneur_micro_entreprise(
            bareme, tns_auto_entrepreneur_type_activite, tns_auto_entrepreneur_chiffre_affaires)
        return benefice


class tns_micro_entreprise_benefice(Variable):
    value_type = float
    label = u"Bénéfice de la micro entreprise"
    entity = Individu
    definition_period = YEAR

    def formula_2008_01_01(individu, period, parameters):
        tns_micro_entreprise_type_activite = individu('tns_micro_entreprise_type_activite', period)
        tns_micro_entreprise_chiffre_affaires = individu('tns_micro_entreprise_chiffre_affaires', period)
        bareme = parameters(period).tns

        benefice = compute_benefice_auto_entrepreneur_micro_entreprise(
            bareme, tns_micro_entreprise_type_activite, tns_micro_entreprise_chiffre_affaires)
        return benefice


# The following formulas take into account 'cotisation sociales'. However, it seems that for all prestations,
# the 'base ressources' are only using the 'benefice', without deducting the 'cotisation sociales'.
# Although this rule seems unfair towards independent workers, we are now applying it for all presations and therefore
# we are not using the following formulas for calculating prestations.


class tns_auto_entrepreneur_revenus_net(Variable):
    value_type = float
    label = u"Revenu d'un auto-entrepreneur"
    entity = Individu
    definition_period = MONTH

    def formula_2008_01_01(individu, period, parameters):
        tns_auto_entrepreneur_benefice = individu('tns_auto_entrepreneur_benefice', period)
        tns_auto_entrepreneur_type_activite = individu('tns_auto_entrepreneur_type_activite', period)
        tns_auto_entrepreneur_chiffre_affaires = individu('tns_auto_entrepreneur_chiffre_affaires', period)
        bareme_cs_ae = parameters(period).tns.auto_entrepreneur
        taux_cotisations_sociales_sur_CA = (
            (tns_auto_entrepreneur_type_activite == TypesTnsTypeActivite.achat_revente) * bareme_cs_ae.achat_revente
            + (tns_auto_entrepreneur_type_activite == TypesTnsTypeActivite.bic) * bareme_cs_ae.bic
            + (tns_auto_entrepreneur_type_activite == TypesTnsTypeActivite.bnc) * bareme_cs_ae.bnc
            )
        tns_auto_entrepreneur_charges_sociales = taux_cotisations_sociales_sur_CA * tns_auto_entrepreneur_chiffre_affaires
        revenus = tns_auto_entrepreneur_benefice - tns_auto_entrepreneur_charges_sociales

        return revenus


class tns_micro_entreprise_revenus_net(Variable):
    value_type = float
    label = u"Revenu d'un TNS dans une micro-entreprise"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        tns_micro_entreprise_benefice = individu('tns_micro_entreprise_benefice', period)
        taux_cotisations_sociales = parameters(period).tns.micro_entreprise.cotisations_sociales
        tns_micro_entreprise_charges_sociales = tns_micro_entreprise_benefice * taux_cotisations_sociales
        revenus = tns_micro_entreprise_benefice - tns_micro_entreprise_charges_sociales

        return revenus
