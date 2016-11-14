# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa


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

class f5qm(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QM",
        QUIFOY['conj']: u"5RM",
        }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Agents généraux d’assurances: indemnités de cessation d’activité"

  # (f5qm, f5rm )

# Revenus des professions non salariées
class ppe_du_ns(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NV",
        QUIFOY['conj']: u"5OV",
        QUIFOY['pac1']: u"5PV",
        }
    column = IntCol
    entity = Individu
    label = u"Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année"
    stop_date = date(2006, 12, 31)

  # (f5nv, f5ov, f5pv)

class ppe_tp_ns(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NW",
        QUIFOY['conj']: u"5OW",
        QUIFOY['pac1']: u"5PW",
        }
    column = BoolCol
    entity = Individu
    label = u"Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière"
    stop_date = date(2006, 12, 31)

  # (f5nw, f5ow, f5pw)

class frag_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HN",
        QUIFOY['conj']: u"5IN",
        QUIFOY['pac1']: u"5JN", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus agricoles exonérés (régime du forfait)"
    start_date = date(2007, 1, 1)

  # (f5hn, f5in, f5jn))

class frag_impo(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HO",
        QUIFOY['conj']: u"5IO",
        QUIFOY['pac1']: u"5JO", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus agricoles imposables (régime du forfait)"
    start_date = date(2007, 1, 1)

  # (f5ho, f5io, f5jo))

class arag_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HB",
        QUIFOY['conj']: u"5IB",
        QUIFOY['pac1']: u"5JB", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse"
    start_date = date(2007, 1, 1)

  # (f5hb, f5ib, f5jb))

class arag_impg(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HC",
        QUIFOY['conj']: u"5IC",
        QUIFOY['pac1']: u"5JC", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    start_date = date(2007, 1, 1)

  # (f5hc, f5ic, f5jc))

class arag_defi(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HF",
        QUIFOY['conj']: u"5IF",
        QUIFOY['pac1']: u"5JF", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    start_date = date(2007, 1, 1)

  # (f5hf, f5if, f5jf))

class nrag_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HH",
        QUIFOY['conj']: u"5IH",
        QUIFOY['pac1']: u"5JH", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse"
    start_date = date(2007, 1, 1)

  # (f5hh, f5ih, f5jh))

class nrag_impg(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HI",
        QUIFOY['conj']: u"5II",
        QUIFOY['pac1']: u"5JI", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    start_date = date(2007, 1, 1)

  # (f5hi, f5ii, f5ji))

class nrag_defi(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HL",
        QUIFOY['conj']: u"5IL",
        QUIFOY['pac1']: u"5JL", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    start_date = date(2007, 1, 1)

  # (f5hl, f5il, f5jl))

class nrag_ajag(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HM",
        QUIFOY['conj']: u"5IM",
        QUIFOY['pac1']: u"5JM", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    start_date = date(2007, 1, 1)

  # (f5hm, f5im, f5jm))

# Autoentrepreneur
class ebic_impv(Variable):
    cerfa_field = {QUIFOY['vous']: u"5TA",
        QUIFOY['conj']: u"5UA",
        QUIFOY['pac1']: u"5VA", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur)"
    start_date = date(2009, 1, 1)
    stop_date = date(2009, 12, 31)

  # (f5ta, f5ua, f5va))

class ebic_imps(Variable):
    cerfa_field = {QUIFOY['vous']: u"5TB",
        QUIFOY['conj']: u"5UB",
        QUIFOY['pac1']: u"5VB", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)"
    start_date = date(2009, 1, 1)
    stop_date = date(2009, 12, 31)

  # (f5tb, f5ub, f5vb))

class ebnc_impo(Variable):
    cerfa_field = {QUIFOY['vous']: u"5TE",
        QUIFOY['conj']: u"5UE",
        QUIFOY['pac1']: u"5VE", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux (régime auto-entrepreneur ayant opté pour le versement libératoire)"
    start_date = date(2009, 1, 1)
    stop_date = date(2009, 12, 31)

  # (f5te, f5ue, f5ve))

class mbic_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KN",
        QUIFOY['conj']: u"5LN",
        QUIFOY['pac1']: u"5MN", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)"

  # (f5kn, f5ln, f5mn))

class abic_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KB",
        QUIFOY['conj']: u"5LB",
        QUIFOY['pac1']: u"5MB", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)"

  # (f5kb, f5lb, f5mb))

class nbic_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KH",
        QUIFOY['conj']: u"5LH",
        QUIFOY['pac1']: u"5MH", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)"

  # (f5kh, f5lh, f5mh))

class mbic_impv(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KO",
        QUIFOY['conj']: u"5LO",
        QUIFOY['pac1']: u"5MO", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)"

  # (f5ko, f5lo, f5mo))

class mbic_imps(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KP",
        QUIFOY['conj']: u"5LP",
        QUIFOY['pac1']: u"5MP", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)"

  # (f5kp, f5lp, f5mp))

class abic_impn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KC",
        QUIFOY['conj']: u"5LC",
        QUIFOY['pac1']: u"5MC", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"

  # (f5kc, f5lc, f5mc))

class abic_imps(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KD",
        QUIFOY['conj']: u"5LD",
        QUIFOY['pac1']: u"5MD", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)"
    stop_date = date(2009, 12, 31)

  # (f5kd, f5ld, f5md))


class nbic_impn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KI",
        QUIFOY['conj']: u"5LI",
        QUIFOY['pac1']: u"5MI", }

    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)"

  # (f5ki, f5li, f5mi))

# """
# réutilisation cases 2013
# """
class nbic_imps(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KJ",
        QUIFOY['conj']: u"5LJ",
        QUIFOY['pac1']: u"5MJ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels imposables: régime simplifié sans CGA (régime du bénéfice réel)"
    stop_date = date(2009, 12, 31)

 # TODO: c'est 5HU pour les années anciennes

class nbic_mvct(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KJ",
        QUIFOY['conj']: u"5LJ",
        QUIFOY['pac1']: u"5MJ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux professionnels moins-values nettes à court terme"
    start_date = date(2012, 1, 1)

  # (f5kj, f5lj, f5mj))
                                                          # vérifier date début #####à intégrer dans OF#######

class abic_defn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KF",
        QUIFOY['conj']: u"5LF",
        QUIFOY['pac1']: u"5MF", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"

  # (f5kf, f5lf, f5mf))

class abic_defs(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KG",
        QUIFOY['conj']: u"5LG",
        QUIFOY['pac1']: u"5MG", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)"
    stop_date = date(2009, 12, 1)

  # (f5kg, f5lg, f5mg))
                                                          # vérif <=2012

class nbic_defn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KL",
        QUIFOY['conj']: u"5LL",
        QUIFOY['pac1']: u"5ML", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)"

  # (f5kl, f5ll, f5ml))

class nbic_defs(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KM",
        QUIFOY['conj']: u"5LM",
        QUIFOY['pac1']: u"5MM", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)"
    stop_date = date(2009, 12, 31)

  # (f5km, f5lm, f5mm))

class nbic_apch(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KS",
        QUIFOY['conj']: u"5LS",
        QUIFOY['pac1']: u"5MS", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)"

  # (f5ks, f5ls, f5ms))

class macc_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NN",
        QUIFOY['conj']: u"5ON",
        QUIFOY['pac1']: u"5PN", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)"

  # (f5nn, f5on, f5pn))

class aacc_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NB",
        QUIFOY['conj']: u"5OB",
        QUIFOY['pac1']: u"5PB", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)"

  # (f5nb, f5ob, f5pb))

class nacc_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NH",
        QUIFOY['conj']: u"5OH",
        QUIFOY['pac1']: u"5PH", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)"

  # (f5nh, f5oh, f5ph))

class macc_impv(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NO",
        QUIFOY['conj']: u"5OO",
        QUIFOY['pac1']: u"5PO", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)"

  # (f5no, f5oo, f5po))

class macc_imps(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NP",
        QUIFOY['conj']: u"5OP",
        QUIFOY['pac1']: u"5PP", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)"

  # (f5np, f5op, f5pp))

class aacc_impn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NC",
        QUIFOY['conj']: u"5OC",
        QUIFOY['pac1']: u"5PC", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"

  # (f5nc, f5oc, f5pc))

class aacc_imps(Variable):
    cerfa_field = {QUIFOY['vous']: u"5ND",
        QUIFOY['conj']: u"5OD",
        QUIFOY['pac1']: u"5PD", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations meublées non professionnelles (régime micro entreprise)"
    start_date = date(2011, 1, 1)

  # (f5nd, f5od, f5pd)) #TODO: avant 2010

class aacc_defn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NF",
        QUIFOY['conj']: u"5OF",
        QUIFOY['pac1']: u"5PF", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)"

  # (f5nf, f5of, f5pf))

class aacc_gits(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NG",
        QUIFOY['conj']: u"5OG",
        QUIFOY['pac1']: u"5PG", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)"
    start_date = date(2011, 1, 1)

  # (f5ng, f5og, f5pg))

class nacc_impn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NI",
        QUIFOY['conj']: u"5OI",
        QUIFOY['pac1']: u"5PI", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)"

  # (f5ni, f5oi, f5pi))

class aacc_defs(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NG",
        QUIFOY['conj']: u"5OG",
        QUIFOY['pac1']: u"5PG", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits de revenus industriels et commerciaux non professionnels avec CGA (régime simplifié du bénéfice réel)"
    stop_date = date(2009, 12, 31)



class nacc_meup(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NJ",
        QUIFOY['conj']: u"5OJ",
        QUIFOY['pac1']: u"5PJ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)"
    start_date = date(2012, 1, 1)

  # (f5nj, f5oj, f5pj)) #TODO: dates 5PJ, 5PG, 5PD, 5OM

class nacc_defn(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NL",
        QUIFOY['conj']: u"5OL",
        QUIFOY['pac1']: u"5PL", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)"

  # (f5nl, f5ol, f5pl))

class nacc_defs(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NM",
        QUIFOY['conj']: u"5OM",
        QUIFOY['pac1']: u"5PM", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations meublées non professionnelles: Gîtes ruraux et chambres d'hôtes déjà soumis aux prélèvements sociaux avec CGA (régime du bénéfice réel)"
    start_date = date(2012, 1, 1)

  # (f5nm, f5om, f5pm)) #TODO autres 5NM

class mncn_impo(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KU",
        QUIFOY['conj']: u"5LU",
        QUIFOY['pac1']: u"5MU", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)"

  # (f5ku, f5lu, f5mu))

class cncn_bene(Variable):
    cerfa_field = {QUIFOY['vous']: u"5SN",
        QUIFOY['conj']: u"5NS",
        QUIFOY['pac1']: u"5OS", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)"
    start_date = date(2006, 1, 1)

  # (f5sn, f5ns, f5os))

class cncn_defi(Variable):
    cerfa_field = {QUIFOY['vous']: u"5SP",
        QUIFOY['conj']: u"5NU",
        QUIFOY['pac1']: u"5OU", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)"
    start_date = date(2006, 1, 1)

  # (f5sp, f5nu, f5ou, f5sr))
                                                                  # pas de f5sr en 2013

class mbnc_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HP",
        QUIFOY['conj']: u"5IP",
        QUIFOY['pac1']: u"5JP", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)"

  # (f5hp, f5ip, f5jp))

class abnc_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QB",
        QUIFOY['conj']: u"5RB",
        QUIFOY['pac1']: u"5SB", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"

  # (f5qb, f5rb, f5sb))

class nbnc_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QH",
        QUIFOY['conj']: u"5RH",
        QUIFOY['pac1']: u"5SH", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"

  # (f5qh, f5rh, f5sh))

class mbnc_impo(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HQ",
        QUIFOY['conj']: u"5IQ",
        QUIFOY['pac1']: u"5JQ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)"

  # (f5hq, f5iq, f5jq))

class abnc_impo(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QC",
        QUIFOY['conj']: u"5RC",
        QUIFOY['pac1']: u"5SC", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"

  # (f5qc, f5rc, f5sc))

class abnc_defi(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QE",
        QUIFOY['conj']: u"5RE",
        QUIFOY['pac1']: u"5SE", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"

  # (f5qe, f5re, f5se))

class nbnc_impo(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QI",
        QUIFOY['conj']: u"5RI",
        QUIFOY['pac1']: u"5SI", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"

  # (f5qi, f5ri, f5si))

class nbnc_defi(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QK",
        QUIFOY['conj']: u"5RK",
        QUIFOY['pac1']: u"5SK", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)"

  # (f5qk, f5rk, f5sk))

class mbic_mvct(Variable):
    cerfa_field = u"5HU"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)"
    stop_date = date(2011, 12, 31)

  # (f5hu))
                                                          # vérif <=2012

class macc_mvct(Variable):
    cerfa_field = u"5IU"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)"

  # (f5iu))

class mncn_mvct(Variable):
    cerfa_field = u"JU"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)"

  # (f5ju))

class mbnc_mvct(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KZ", #TODO: pb cerfa field
        QUIFOY['conj']: u"5LZ",
        QUIFOY['pac1']: u"5MZ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)"
    start_date = date(2012, 1, 1)

  # (f5kz, f5lz , f5mz), f5lz , f5mz sont présentent en 2013


class frag_pvct(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HW",
        QUIFOY['conj']: u"5IW",
        QUIFOY['pac1']: u"5JW", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values agricoles  à court terme (régime du forfait)"
    start_date = date(2007, 1, 1)

  # (f5hw, f5iw, f5jw))

class mbic_pvct(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KX",
        QUIFOY['conj']: u"5LX",
        QUIFOY['pac1']: u"5MX", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)"

  # (f5kx, f5lx, f5mx))

class macc_pvct(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NX",
        QUIFOY['conj']: u"5OX",
        QUIFOY['pac1']: u"5PX", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)"

  # (f5nx, f5ox, f5px))

class mbnc_pvct(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HV",
        QUIFOY['conj']: u"5IV",
        QUIFOY['pac1']: u"5JV", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)"

  # (f5hv, f5iv, f5jv))

class mncn_pvct(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KY",
        QUIFOY['conj']: u"5LY",
        QUIFOY['pac1']: u"5MY", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)"

  # (f5ky, f5ly, f5my))

class mbic_mvlt(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KR",
        QUIFOY['conj']: u"5LR",
        QUIFOY['pac1']: u"5MR", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)"

  # (f5kr, f5lr, f5mr))

class macc_mvlt(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NR",
        QUIFOY['conj']: u"5OR",
        QUIFOY['pac1']: u"5PR", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)"

  # (f5nr, f5or, f5pr))

class mncn_mvlt(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KW",
        QUIFOY['conj']: u"5LW",
        QUIFOY['pac1']: u"5MW", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)"

  # (f5kw, f5lw, f5mw))

class mbnc_mvlt(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HS",
        QUIFOY['conj']: u"5IS",
        QUIFOY['pac1']: u"5JS", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)"

  # (f5hs, f5is, f5js))

class frag_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HX",
        QUIFOY['conj']: u"5IX",
        QUIFOY['pac1']: u"5JX", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values agricoles de cession taxables à 16% (régime du forfait)"
    start_date = date(2007, 1, 1)

  # (f5hx, f5ix, f5jx))

class arag_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HE",
        QUIFOY['conj']: u"5IE",
        QUIFOY['pac1']: u"5JE", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)"
    start_date = date(2007, 1, 1)

  # (f5he, f5ie, f5je))

class nrag_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HK",
        QUIFOY['conj']: u"5LK",
        QUIFOY['pac1']: u"5JK", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)"
    stop_date = date(2006, 12, 31)

  # TODO: vérif <=2012))  # (f5hk, f5lk, f5jk) codent autre chose sur d'autres années),

class mbic_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KQ",
        QUIFOY['conj']: u"5LQ",
        QUIFOY['pac1']: u"5MQ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)"

  # (f5kq, f5lq, f5mq))

class abic_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KE",
        QUIFOY['conj']: u"5LE",
        QUIFOY['pac1']: u"5ME", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)"

  # (f5ke, f5le, f5me))

class nbic_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5IK",
        QUIFOY['conj']: u"5KK",
        QUIFOY['pac1']: u"5MK", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)"
    start_date = date(2008, 1, 1)

  # (f5kk, f5ik, f5mk)) TODO: autre 5KK 2005/20006

class macc_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NQ",
        QUIFOY['conj']: u"5OQ",
        QUIFOY['pac1']: u"5PQ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)"

  # (f5nq, f5oq, f5pq))

class aacc_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NE",
        QUIFOY['conj']: u"5OE",
        QUIFOY['pac1']: u"5PE", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)"

  # (f5ne, f5oe, f5pe))

class nacc_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NK",
        QUIFOY['conj']: u"5OK",
        QUIFOY['pac1']: u"5PK", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)"
    start_date = date(2009, 1, 1)
    stop_date = date(2010, 12, 31)

  # (f5nk, f5ok, f5pk)) TODO: 5NK 2005/2006

class mncn_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KV",
        QUIFOY['conj']: u"5LV",
        QUIFOY['pac1']: u"5MV", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)"

  # (f5kv, f5lv, f5mv))

class cncn_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5SO",
        QUIFOY['conj']: u"5NT",
        QUIFOY['pac1']: u"5OT", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)"
    start_date = date(2006, 1, 1)

  # (f5so, f5nt, f5ot))

class mbnc_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HR",
        QUIFOY['conj']: u"5IR",
        QUIFOY['pac1']: u"5JR", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)"

  # (f5hr, f5ir, f5jr))

class abnc_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QD",
        QUIFOY['conj']: u"5RD",
        QUIFOY['pac1']: u"5SD", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)"

  # (f5qd, f5rd, f5sd))

class nbnc_pvce(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QJ",
        QUIFOY['conj']: u"5RJ",
        QUIFOY['pac1']: u"5SJ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)"
    start_date = date(2009, 1, 1)

  # (f5qj, f5rj, f5sj)) #TODO 5*J 2005/2006 (qui se transforme en 5*D...)

class frag_fore(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HD",
        QUIFOY['conj']: u"5ID",
        QUIFOY['pac1']: u"5JD", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus des exploitants forestiers (régime du forfait)"
    start_date = date(2007, 1, 1)



class arag_sjag(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HZ",
        QUIFOY['conj']: u"5IZ",
        QUIFOY['pac1']: u"5JZ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Abattement pour les jeunes agriculteurs des revenus agricoles sans CGA (régime du bénéfice réel)"
    start_date = date(2011, 1, 1)



class abic_impm(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HA",
        QUIFOY['conj']: u"5IA",
        QUIFOY['pac1']: u"5JA", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations meublées imposables avec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)"
    start_date = date(2009, 1, 1)



class nbic_impm(Variable):
    cerfa_field = {QUIFOY['vous']: u"5KA",
        QUIFOY['conj']: u"5LA",
        QUIFOY['pac1']: u"5MA", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations meublées imposables sans CGA (régime du bénéfice réel)"
    start_date = date(2009, 1, 1)



class abic_defm(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QA",
        QUIFOY['conj']: u"5RA",
        QUIFOY['pac1']: u"5SA", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits de locations meubléesavec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)"
    start_date = date(2009, 1, 1)



class alnp_imps(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NA",
        QUIFOY['conj']: u"5OA",
        QUIFOY['pac1']: u"5PA", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Locations meublées non professionnelles imposables avec CGA ou viseur (régime du bénéfice réel)"
    start_date = date(2009, 1, 1)
    stop_date = date(2010, 12, 31)



class alnp_defs(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NY",
        QUIFOY['conj']: u"5OY",
        QUIFOY['pac1']: u"5PY", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits de locations meublées non professionnelles avec CGA ou viseur (régime du bénéfice réel)"
    start_date = date(2009, 1, 1)
    stop_date = date(2010, 12, 31)



class nlnp_defs(Variable):
    cerfa_field = {QUIFOY['vous']: u"5NZ",
        QUIFOY['conj']: u"5OZ",
        QUIFOY['pac1']: u"5PZ", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits de locations meublées non professionnelles imposables sans CGA (régime du bénéfice réel)"
    start_date = date(2009, 1, 1)
    stop_date = date(2010, 12, 31)



class cbnc_assc(Variable):
    cerfa_field = {QUIFOY['vous']: u"5QM",
        QUIFOY['conj']: u"5RM", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Agents généraux d'assurances : indemnités de cessation d'activité (revenus non commerciaux professionnels, régime de la déclaration contrôlée)"
    start_date = date(2006, 1, 1)



class abnc_proc(Variable):
    cerfa_field = {QUIFOY['vous']: u"5TF",
        QUIFOY['conj']: u"5UF",
        QUIFOY['pac1']: u"5VF", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Honoraires de prospection commerciale exonérés avec CGA ou viseur (revenus non commerciaux professionnels, régime de la déclaration contrôlée)"
    start_date = date(2009, 1, 1)



class nbnc_proc(Variable):
    cerfa_field = {QUIFOY['vous']: u"5TI",
        QUIFOY['conj']: u"5UI",
        QUIFOY['pac1']: u"5VI", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Honoraires de prospection commerciale exonérés sans CGA (revenus non commerciaux professionnels, régime de la déclaration contrôlée)"
    start_date = date(2009, 1, 1)



class mncn_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5TH",
        QUIFOY['conj']: u"5UH",
        QUIFOY['pac1']: u"5VH", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus nets exonérés non commerciaux non professionnels (régime déclaratif spécial ou micro BNC)"
    start_date = date(2009, 1, 1)



class cncn_exon(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HK",
        QUIFOY['conj']: u"5JK",
        QUIFOY['pac1']: u"5LK", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus nets exonérés non commerciaux non professionnels (régime de la déclaration contrôlée)"
    start_date = date(2008, 1, 1)



class cncn_aimp(Variable):
    cerfa_field = {QUIFOY['vous']: u"5JG",
        QUIFOY['conj']: u"5RF",
        QUIFOY['pac1']: u"5SF", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus imposables non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    start_date = date(2007, 1, 1)



class cncn_adef(Variable):
    cerfa_field = {QUIFOY['vous']: u"5JJ",
        QUIFOY['conj']: u"5RG",
        QUIFOY['pac1']: u"5SG", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Déficits non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    start_date = date(2007, 1, 1)



class cncn_info(Variable):
    cerfa_field = {QUIFOY['vous']: u"5TC",
        QUIFOY['conj']: u"5UC",
        QUIFOY['pac1']: u"5VC", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Inventeurs et auteurs de logiciels : produits taxables à 16%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    start_date = date(2009, 1, 1)



class cncn_jcre(Variable):
    cerfa_field = {QUIFOY['vous']: u"5SV",
        QUIFOY['conj']: u"5SW",
        QUIFOY['pac1']: u"5SX", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Jeunes créateurs : abattement de 50%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)"
    start_date = date(2006, 1, 1)



class revimpres(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HY",
        QUIFOY['conj']: u"5IY",
        QUIFOY['pac1']: u"5JY", }
    column = IntCol(val_type = "monetary")
    entity = Individu
    label = u"Revenus nets à imposer aux prélèvements sociaux"



class pveximpres(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HG",
        QUIFOY['conj']: u"5IG", }
    column = IntCol
    entity = Individu
    label = u"Plus-values à long terme exonérées en cas de départ à la retraite à imposer aux prélèvements sociaux"
    start_date = date(2006, 1, 1)




class pvtaimpres(Variable):
    cerfa_field = {QUIFOY['vous']: u"5HZ",
        QUIFOY['conj']: u"5IZ",
        QUIFOY['pac1']: u"5JZ", }
    column = IntCol
    entity = Individu
    label = u"Plus-values à long terme taxables à 16% à la retraite à imposer aux prélèvements sociaux"
    stop_date = date(2009, 12, 31)



class f5qf(Variable):
    cerfa_field = u"5QF"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-6)"
    start_date = date(2007, 1, 1)



class f5qg(Variable):
    cerfa_field = u"5QG"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-5)"
    start_date = date(2007, 1, 1)



class f5qn(Variable):
    cerfa_field = u"5QN"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-4)"
    start_date = date(2007, 1, 1)



class f5qo(Variable):
    cerfa_field = u"5QO"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-3)"
    start_date = date(2007, 1, 1)



class f5qp(Variable):
    cerfa_field = u"5QP"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-2)"
    start_date = date(2007, 1, 1)



class f5qq(Variable):
    cerfa_field = u"5QQ"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-1)"
    start_date = date(2007, 1, 1)



class f5ga(Variable):
    cerfa_field = u"5GA"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-10)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gb(Variable):
    cerfa_field = u"5GB"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-9)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gc(Variable):
    cerfa_field = u"5GC"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-8)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gd(Variable):
    cerfa_field = u"5GD"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-7)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5ge(Variable):
    cerfa_field = u"5GE"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-6)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gf(Variable):
    cerfa_field = u"5GF"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-5)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gg(Variable):
    cerfa_field = u"5GG"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-4)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gh(Variable):
    cerfa_field = u"5GH"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-3)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gi(Variable):
    cerfa_field = u"5GI"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-2)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5gj(Variable):
    cerfa_field = u"5GJ"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-1)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5rn(Variable):
    cerfa_field = u"5RN"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-6)"
    start_date = date(2010, 1, 1)
    stop_date = date(2010, 12, 31)



class f5ro(Variable):
    cerfa_field = u"5RO"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-5)"



class f5rp(Variable):
    cerfa_field = u"5RP"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-4)"



class f5rq(Variable):
    cerfa_field = u"5RQ"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-3)"



class f5rr(Variable):
    cerfa_field = u"5RR"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-2)"



class f5rw(Variable):
    cerfa_field = u"5RW"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-1)"



class f5ht(Variable):
    cerfa_field = u"5HT"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-6)"
    start_date = date(2007, 1, 1)



class f5it(Variable):
    cerfa_field = u"5IT"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-5)"
    start_date = date(2007, 1, 1)



class f5jt(Variable):
    cerfa_field = u"5JT"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-4)"
    start_date = date(2007, 1, 1)



class f5kt(Variable):
    cerfa_field = u"5KT"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-3)"
    start_date = date(2007, 1, 1)



class f5lt(Variable):
    cerfa_field = u"5LT"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-2)"
    start_date = date(2007, 1, 1)



class f5mt(Variable):
    cerfa_field = u"5MT"
    column = IntCol(val_type = "monetary")
    entity = FoyerFiscal
    label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-1)"
    start_date = date(2007, 1, 1)



class f5sq(Variable):
    column = IntCol
    entity = Individu




# TODO: Introduit par mes aides à consolider

# Input variables

# Input mensuel
class tns_auto_entrepreneur_chiffre_affaires(Variable):
    column = FloatCol
    entity = Individu
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaires en tant qu'auto-entrepreneur"

# Input annuel
class tns_micro_entreprise_chiffre_affaires(Variable):
    column = FloatCol
    entity = Individu
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaires en de micro-entreprise"

enum_tns_type_activite = Enum([u'achat_revente', u'bic', u'bnc'])


# TODO remove this ugly is_permanent
class tns_auto_entrepreneur_type_activite(Variable):
    column = EnumCol(enum = enum_tns_type_activite)
    entity = Individu
    is_permanent = True
    label = u"Type d'activité de l'auto-entrepreneur"

# TODO remove this ugly is_permanent
class tns_micro_entreprise_type_activite(Variable):
    column = EnumCol(enum = enum_tns_type_activite)
    entity = Individu
    is_permanent = True
    label = u"Type d'activité de la micro-entreprise"

# Input sur le dernier exercice. Par convention, sur l'année dernière.
class tns_autres_revenus(Variable):
    column = FloatCol
    entity = Individu
    set_input = set_input_divide_by_period
    label = u"Autres revenus non salariés"

class tns_autres_revenus_chiffre_affaires(Variable):
    column = FloatCol
    entity = Individu
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaire pour les TNS non agricoles autres que les AE et ME"

class tns_autres_revenus_type_activite(Variable):
    column = EnumCol(enum = enum_tns_type_activite)
    entity = Individu
    is_permanent = True
    label = u"Type d'activité de l'entreprise non AE ni ME"

class tns_avec_employe(Variable):
    column = BoolCol
    entity = Individu
    set_input = set_input_dispatch_by_period
    label = u"Le TNS a au moins un employé. Ne s'applique pas pour les agricoles ni auto-entrepreneurs ni micro entreprise"

# Input annuel
class tns_benefice_exploitant_agricole(Variable):
    column = FloatCol
    entity = Individu
    set_input = set_input_dispatch_by_period
    label = u"Dernier bénéfice agricole"


# Computed variables

class travailleur_non_salarie(Variable):
    label = u"L'individu a une activité professionnelle non salariée"
    column = BoolCol
    entity = Individu

    def function(self, simulation, period):
        period = period.this_month
        this_year_and_last_year = period.start.offset('first-of', 'year').period('year', 2).offset(-1)
        tns_auto_entrepreneur_chiffre_affaires = simulation.calculate('tns_auto_entrepreneur_chiffre_affaires', period) != 0
        tns_micro_entreprise_chiffre_affaires = simulation.calculate_add('tns_micro_entreprise_chiffre_affaires', this_year_and_last_year) != 0
        tns_autres_revenus = simulation.calculate_add('tns_autres_revenus', this_year_and_last_year) != 0
        tns_benefice_exploitant_agricole = simulation.calculate_add('tns_benefice_exploitant_agricole', this_year_and_last_year) != 0
        tns_autres_revenus_chiffre_affaires = simulation.calculate_add('tns_autres_revenus_chiffre_affaires', this_year_and_last_year) != 0

        result = (
            tns_auto_entrepreneur_chiffre_affaires + tns_micro_entreprise_chiffre_affaires +
            tns_autres_revenus + tns_benefice_exploitant_agricole + tns_autres_revenus_chiffre_affaires
        )

        return period, result


# Auxiliary function
def compute_benefice_auto_entrepreneur_micro_entreprise(bareme, type_activite, chiffre_affaire):
    abatt_fp_me = bareme.micro_entreprise.abattement_forfaitaire_fp
    benefice = chiffre_affaire * (
        1 -
        (type_activite == 0) * abatt_fp_me.achat_revente -
        (type_activite == 1) * abatt_fp_me.bic -
        (type_activite == 2) * abatt_fp_me.bnc)

    return benefice


class tns_auto_entrepreneur_benefice(DatedVariable):
    column = FloatCol
    label = u"Bénéfice en tant qu'auto-entrepreneur"
    entity = Individu

    @dated_function(start = date(2008, 1, 1))
    def function(self, simulation, period):
        period = period.this_month
        tns_auto_entrepreneur_type_activite = simulation.calculate('tns_auto_entrepreneur_type_activite', period)
        tns_auto_entrepreneur_chiffre_affaires = simulation.calculate('tns_auto_entrepreneur_chiffre_affaires', period)
        bareme = simulation.legislation_at(period.start).tns

        benefice = compute_benefice_auto_entrepreneur_micro_entreprise(
            bareme, tns_auto_entrepreneur_type_activite, tns_auto_entrepreneur_chiffre_affaires)
        return period, benefice


class tns_micro_entreprise_benefice(DatedVariable):
    column = FloatCol
    label = u"Bénéfice de la micro entreprise"
    entity = Individu

    @dated_function(start = date(2008, 1, 1))
    def function(self, simulation, period):
        period = period.this_year
        tns_micro_entreprise_type_activite = simulation.calculate('tns_micro_entreprise_type_activite', period)
        tns_micro_entreprise_chiffre_affaires = simulation.calculate('tns_micro_entreprise_chiffre_affaires', period)
        bareme = simulation.legislation_at(period.start).tns

        benefice = compute_benefice_auto_entrepreneur_micro_entreprise(
            bareme, tns_micro_entreprise_type_activite, tns_micro_entreprise_chiffre_affaires)
        return period, benefice

# The following formulas take into account 'cotisation sociales'. However, it seems that for all prestations,
# the 'base ressources' are only using the 'benefice', without deducting the 'cotisation sociales'.
# Although this rule seems unfair towards independent workers, we are now applying it for all presations and therefore
# we are not using the following formulas for calculating prestations.
class tns_auto_entrepreneur_revenus_net(DatedVariable) :
    column = FloatCol
    label = u"Revenu d'un auto-entrepreneur"
    entity = Individu

    @dated_function(start = date(2008, 1, 1))
    def function(self, simulation, period):
        period = period.this_month
        tns_auto_entrepreneur_benefice = simulation.calculate('tns_auto_entrepreneur_benefice', period)
        tns_auto_entrepreneur_type_activite = simulation.calculate('tns_auto_entrepreneur_type_activite', period)
        tns_auto_entrepreneur_chiffre_affaires = simulation.calculate('tns_auto_entrepreneur_chiffre_affaires', period)
        bareme_cs_ae = simulation.legislation_at(period.start).tns.auto_entrepreneur
        taux_cotisations_sociales_sur_CA = (
            (tns_auto_entrepreneur_type_activite == 0) * bareme_cs_ae.achat_revente +
            (tns_auto_entrepreneur_type_activite == 1) * bareme_cs_ae.bic +
            (tns_auto_entrepreneur_type_activite == 2) * bareme_cs_ae.bnc)
        tns_auto_entrepreneur_charges_sociales = taux_cotisations_sociales_sur_CA * tns_auto_entrepreneur_chiffre_affaires
        revenus = tns_auto_entrepreneur_benefice - tns_auto_entrepreneur_charges_sociales

        return period, revenus


class tns_micro_entreprise_revenus_net(Variable) :
    column = FloatCol
    label = u"Revenu d'un TNS dans une micro-entreprise"
    entity = Individu

    def function(self, simulation, period):
        period = period.this_month
        tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', period)
        taux_cotisations_sociales = simulation.legislation_at(period.start).tns.micro_entreprise.cotisations_sociales
        tns_micro_entreprise_charges_sociales = tns_micro_entreprise_benefice * taux_cotisations_sociales
        revenus = tns_micro_entreprise_benefice - tns_micro_entreprise_charges_sociales

        return period, revenus
