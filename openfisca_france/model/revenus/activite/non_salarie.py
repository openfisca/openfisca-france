# -*- coding: utf-8 -*-

from ...base import *  # noqa


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

build_column('f5qm', IntCol(entity = 'ind',
                label = u"Agents généraux d’assurances: indemnités de cessation d’activité",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"5QM",
                               QUIFOY['conj']: u"5RM",
                               }))  # (f5qm, f5rm )

# Revenus des professions non salariées
build_column('ppe_du_ns', IntCol(entity = 'ind', label = u"Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année",
                     end = date(2006, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5NV",
                                    QUIFOY['conj']: u"5OV",
                                    QUIFOY['pac1']: u"5PV",
                               }))  # (f5nv, f5ov, f5pv)

build_column('ppe_tp_ns', BoolCol(entity = 'ind', label = u"Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière",
                      end = date(2006, 12, 31),
                      cerfa_field = {QUIFOY['vous']: u"5NW",
                                     QUIFOY['conj']: u"5OW",
                                     QUIFOY['pac1']: u"5PW",
                                     }))  # (f5nw, f5ow, f5pw)

build_column('frag_exon', IntCol(entity = 'ind', label = u"Revenus agricoles exonérés (régime du forfait)", val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HN",
                                    QUIFOY['conj']: u"5IN",
                                    QUIFOY['pac1']: u"5JN", }))  # (f5hn, f5in, f5jn))

build_column('frag_impo', IntCol(entity = 'ind',
                     label = u"Revenus agricoles imposables (régime du forfait)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HO",
                                    QUIFOY['conj']: u"5IO",
                                    QUIFOY['pac1']: u"5JO", }))  # (f5ho, f5io, f5jo))

build_column('arag_exon', IntCol(entity = 'ind',
                     label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HB",
                                    QUIFOY['conj']: u"5IB",
                                    QUIFOY['pac1']: u"5JB", }))  # (f5hb, f5ib, f5jb))

build_column('arag_impg', IntCol(entity = 'ind',
                     label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HC",
                                    QUIFOY['conj']: u"5IC",
                                    QUIFOY['pac1']: u"5JC", }))  # (f5hc, f5ic, f5jc))

build_column('arag_defi', IntCol(entity = 'ind',
                     label = u"Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HF",
                                    QUIFOY['conj']: u"5IF",
                                    QUIFOY['pac1']: u"5JF", }))  # (f5hf, f5if, f5jf))

build_column('nrag_exon', IntCol(entity = 'ind',
                     label = u"Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HH",
                                    QUIFOY['conj']: u"5IH",
                                    QUIFOY['pac1']: u"5JH", }))  # (f5hh, f5ih, f5jh))

build_column('nrag_impg', IntCol(entity = 'ind',
                     label = u"Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HI",
                                    QUIFOY['conj']: u"5II",
                                    QUIFOY['pac1']: u"5JI", }))  # (f5hi, f5ii, f5ji))

build_column('nrag_defi', IntCol(entity = 'ind',
                     label = u"Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HL",
                                    QUIFOY['conj']: u"5IL",
                                    QUIFOY['pac1']: u"5JL", }))  # (f5hl, f5il, f5jl))

build_column('nrag_ajag', IntCol(entity = 'ind',
                     label = u"Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HM",
                                    QUIFOY['conj']: u"5IM",
                                    QUIFOY['pac1']: u"5JM", }))  # (f5hm, f5im, f5jm))

# Autoentrepreneur
build_column('ebic_impv', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     end = date(2009, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5TA",
                                    QUIFOY['conj']: u"5UA",
                                    QUIFOY['pac1']: u"5VA", }))  # (f5ta, f5ua, f5va))

build_column('ebic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     end = date(2009, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5TB",
                                    QUIFOY['conj']: u"5UB",
                                    QUIFOY['pac1']: u"5VB", }))  # (f5tb, f5ub, f5vb))

build_column('ebnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux (régime auto-entrepreneur ayant opté pour le versement libératoire)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     end = date(2009, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5TE",
                                    QUIFOY['conj']: u"5UE",
                                    QUIFOY['pac1']: u"5VE", }))  # (f5te, f5ue, f5ve))

build_column('mbic_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KN",
                                    QUIFOY['conj']: u"5LN",
                                    QUIFOY['pac1']: u"5MN", }))  # (f5kn, f5ln, f5mn))

build_column('abic_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KB",
                                    QUIFOY['conj']: u"5LB",
                                    QUIFOY['pac1']: u"5MB", }))  # (f5kb, f5lb, f5mb))

build_column('nbic_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KH",
                                    QUIFOY['conj']: u"5LH",
                                    QUIFOY['pac1']: u"5MH", }))  # (f5kh, f5lh, f5mh))

build_column('mbic_impv', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KO",
                                    QUIFOY['conj']: u"5LO",
                                    QUIFOY['pac1']: u"5MO", }))  # (f5ko, f5lo, f5mo))

build_column('mbic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KP",
                                    QUIFOY['conj']: u"5LP",
                                    QUIFOY['pac1']: u"5MP", }))  # (f5kp, f5lp, f5mp))

build_column('abic_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                      val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KC",
                                    QUIFOY['conj']: u"5LC",
                                    QUIFOY['pac1']: u"5MC", }))  # (f5kc, f5lc, f5mc))

build_column('abic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KD",
                                    QUIFOY['conj']: u"5LD",
                                    QUIFOY['pac1']: u"5MD", },
                     end = date(2009, 12, 31)))  # (f5kd, f5ld, f5md))


build_column('nbic_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KI",
                                    QUIFOY['conj']: u"5LI",
                                    QUIFOY['pac1']: u"5MI", }
                     ))  # (f5ki, f5li, f5mi))

# """
# réutilisation cases 2013
# """
build_column('nbic_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels imposables: régime simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KJ",
                                    QUIFOY['conj']: u"5LJ",
                                    QUIFOY['pac1']: u"5MJ", },
                     end = date(2009, 12, 31))) # TODO: c'est 5HU pour les années anciennes

build_column('nbic_mvct', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux professionnels moins-values nettes à court terme",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KJ",
                                    QUIFOY['conj']: u"5LJ",
                                    QUIFOY['pac1']: u"5MJ", },
                     start = date(2012, 1, 1)))  # (f5kj, f5lj, f5mj))
                                                          # vérifier date début #####à intégrer dans OF#######

build_column('abic_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KF",
                                    QUIFOY['conj']: u"5LF",
                                    QUIFOY['pac1']: u"5MF", }))  # (f5kf, f5lf, f5mf))

build_column('abic_defs', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KG",
                                    QUIFOY['conj']: u"5LG",
                                    QUIFOY['pac1']: u"5MG", },
                     end = date(2009, 12, 1)))  # (f5kg, f5lg, f5mg))
                                                          # vérif <=2012

build_column('nbic_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KL",
                                    QUIFOY['conj']: u"5LL",
                                    QUIFOY['pac1']: u"5ML", }))  # (f5kl, f5ll, f5ml))

build_column('nbic_defs', IntCol(entity = 'ind',
                     label = u"Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     end = date(2009, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5KM",
                                    QUIFOY['conj']: u"5LM",
                                    QUIFOY['pac1']: u"5MM", }))  # (f5km, f5lm, f5mm))

build_column('nbic_apch', IntCol(entity = 'ind',
                     label = u"Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KS",
                                    QUIFOY['conj']: u"5LS",
                                    QUIFOY['pac1']: u"5MS", }))  # (f5ks, f5ls, f5ms))

build_column('macc_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NN",
                                    QUIFOY['conj']: u"5ON",
                                    QUIFOY['pac1']: u"5PN", }))  # (f5nn, f5on, f5pn))

build_column('aacc_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NB",
                                    QUIFOY['conj']: u"5OB",
                                    QUIFOY['pac1']: u"5PB", }))  # (f5nb, f5ob, f5pb))

build_column('nacc_exon', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NH",
                                    QUIFOY['conj']: u"5OH",
                                    QUIFOY['pac1']: u"5PH", }))  # (f5nh, f5oh, f5ph))

build_column('macc_impv', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NO",
                                    QUIFOY['conj']: u"5OO",
                                    QUIFOY['pac1']: u"5PO", }))  # (f5no, f5oo, f5po))

build_column('macc_imps', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NP",
                                    QUIFOY['conj']: u"5OP",
                                    QUIFOY['pac1']: u"5PP", }))  # (f5np, f5op, f5pp))

build_column('aacc_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NC",
                                    QUIFOY['conj']: u"5OC",
                                    QUIFOY['pac1']: u"5PC", }))  # (f5nc, f5oc, f5pc))

build_column('aacc_imps', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles (régime micro entreprise)",
                     val_type = "monetary",
                     start = date(2011, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5ND",
                                    QUIFOY['conj']: u"5OD",
                                    QUIFOY['pac1']: u"5PD", }))  # (f5nd, f5od, f5pd)) #TODO: avant 2010

build_column('aacc_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NF",
                                    QUIFOY['conj']: u"5OF",
                                    QUIFOY['pac1']: u"5PF", }))  # (f5nf, f5of, f5pf))

build_column('aacc_gits', IntCol(entity = 'ind',
                     label = u"Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)",
                     val_type = "monetary",
                     start = date(2011, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5NG",
                                    QUIFOY['conj']: u"5OG",
                                    QUIFOY['pac1']: u"5PG", }))  # (f5ng, f5og, f5pg))

build_column('nacc_impn', IntCol(entity = 'ind',
                     label = u"Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NI",
                                    QUIFOY['conj']: u"5OI",
                                    QUIFOY['pac1']: u"5PI", }))  # (f5ni, f5oi, f5pi))

build_column('aacc_defs', IntCol(entity = 'ind',
                     label = u"Déficits de revenus industriels et commerciaux non professionnels avec CGA (régime simplifié du bénéfice réel)",
                     val_type = "monetary",
                     end = date(2009, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5NG",
                                    QUIFOY['conj']: u"5OG",
                                    QUIFOY['pac1']: u"5PG", }))

build_column('nacc_meup', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)",
                     val_type = "monetary",
                     start = date(2012, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5NJ",
                                    QUIFOY['conj']: u"5OJ",
                                    QUIFOY['pac1']: u"5PJ", }))  # (f5nj, f5oj, f5pj)) #TODO: dates 5PJ, 5PG, 5PD, 5OM

build_column('nacc_defn', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NL",
                                    QUIFOY['conj']: u"5OL",
                                    QUIFOY['pac1']: u"5PL", }))  # (f5nl, f5ol, f5pl))

build_column('nacc_defs', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles: Gîtes ruraux et chambres d'hôtes déjà soumis aux prélèvements sociaux avec CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2012, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5NM",
                                    QUIFOY['conj']: u"5OM",
                                    QUIFOY['pac1']: u"5PM", }))  # (f5nm, f5om, f5pm)) #TODO autres 5NM

build_column('mncn_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KU",
                                    QUIFOY['conj']: u"5LU",
                                    QUIFOY['pac1']: u"5MU", }))  # (f5ku, f5lu, f5mu))

build_column('cncn_bene', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)",
                     val_type = "monetary",
                     start = date(2006, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5SN",
                                    QUIFOY['conj']: u"5NS",
                                    QUIFOY['pac1']: u"5OS", }))  # (f5sn, f5ns, f5os))

build_column('cncn_defi', IntCol(entity = 'ind',
                     label = u"Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)",
                     val_type = "monetary",
                     start = date(2006, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5SP",
                                    QUIFOY['conj']: u"5NU",
                                    QUIFOY['pac1']: u"5OU", }))  # (f5sp, f5nu, f5ou, f5sr))
                                                                  # pas de f5sr en 2013

build_column('mbnc_exon', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HP",
                                    QUIFOY['conj']: u"5IP",
                                    QUIFOY['pac1']: u"5JP", }))  # (f5hp, f5ip, f5jp))

build_column('abnc_exon', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QB",
                                    QUIFOY['conj']: u"5RB",
                                    QUIFOY['pac1']: u"5SB", }))  # (f5qb, f5rb, f5sb))

build_column('nbnc_exon', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QH",
                                    QUIFOY['conj']: u"5RH",
                                    QUIFOY['pac1']: u"5SH", }))  # (f5qh, f5rh, f5sh))

build_column('mbnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HQ",
                                    QUIFOY['conj']: u"5IQ",
                                    QUIFOY['pac1']: u"5JQ", }))  # (f5hq, f5iq, f5jq))

build_column('abnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QC",
                                    QUIFOY['conj']: u"5RC",
                                    QUIFOY['pac1']: u"5SC", }))  # (f5qc, f5rc, f5sc))

build_column('abnc_defi', IntCol(entity = 'ind',
                     label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QE",
                                    QUIFOY['conj']: u"5RE",
                                    QUIFOY['pac1']: u"5SE", }))  # (f5qe, f5re, f5se))

build_column('nbnc_impo', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QI",
                                    QUIFOY['conj']: u"5RI",
                                    QUIFOY['pac1']: u"5SI", }))  # (f5qi, f5ri, f5si))

build_column('nbnc_defi', IntCol(entity = 'ind',
                     label = u"Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QK",
                                    QUIFOY['conj']: u"5RK",
                                    QUIFOY['pac1']: u"5SK", }))  # (f5qk, f5rk, f5sk))

build_column('mbic_mvct', IntCol(entity = 'foy',
                     label = u"Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = u'5HU',
                     end = date(2011, 12, 31)))  # (f5hu))
                                                          # vérif <=2012

build_column('macc_mvct', IntCol(entity = 'foy', label = u"Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = u'5IU'))  # (f5iu))

build_column('mncn_mvct', IntCol(entity = 'foy',
                     label = u"Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = u'JU'))  # (f5ju))

build_column('mbnc_mvct', IntCol(entity = 'ind', label = u"Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     start = date(2012, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5KZ", #TODO: pb cerfa field
                                    QUIFOY['conj']: u"5LZ",
                                    QUIFOY['pac1']: u"5MZ", }))  # (f5kz, f5lz , f5mz), f5lz , f5mz sont présentent en 2013


build_column('frag_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles  à court terme (régime du forfait)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HW",
                                    QUIFOY['conj']: u"5IW",
                                    QUIFOY['pac1']: u"5JW", }))  # (f5hw, f5iw, f5jw))

build_column('mbic_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KX",
                                    QUIFOY['conj']: u"5LX",
                                    QUIFOY['pac1']: u"5MX", }))  # (f5kx, f5lx, f5mx))

build_column('macc_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NX",
                                    QUIFOY['conj']: u"5OX",
                                    QUIFOY['pac1']: u"5PX", }))  # (f5nx, f5ox, f5px))

build_column('mbnc_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HV",
                                    QUIFOY['conj']: u"5IV",
                                    QUIFOY['pac1']: u"5JV", }))  # (f5hv, f5iv, f5jv))

build_column('mncn_pvct', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KY",
                                    QUIFOY['conj']: u"5LY",
                                    QUIFOY['pac1']: u"5MY", }))  # (f5ky, f5ly, f5my))

build_column('mbic_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KR",
                                    QUIFOY['conj']: u"5LR",
                                    QUIFOY['pac1']: u"5MR", }))  # (f5kr, f5lr, f5mr))

build_column('macc_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NR",
                                    QUIFOY['conj']: u"5OR",
                                    QUIFOY['pac1']: u"5PR", }))  # (f5nr, f5or, f5pr))

build_column('mncn_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KW",
                                    QUIFOY['conj']: u"5LW",
                                    QUIFOY['pac1']: u"5MW", }))  # (f5kw, f5lw, f5mw))

build_column('mbnc_mvlt', IntCol(entity = 'ind',
                     label = u"Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)", val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HS",
                                    QUIFOY['conj']: u"5IS",
                                    QUIFOY['pac1']: u"5JS", }))  # (f5hs, f5is, f5js))

build_column('frag_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles de cession taxables à 16% (régime du forfait)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HX",
                                    QUIFOY['conj']: u"5IX",
                                    QUIFOY['pac1']: u"5JX", }))  # (f5hx, f5ix, f5jx))

build_column('arag_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HE",
                                    QUIFOY['conj']: u"5IE",
                                    QUIFOY['pac1']: u"5JE", }))  # (f5he, f5ie, f5je))

build_column('nrag_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HK",
                                    QUIFOY['conj']: u"5LK",
                                    QUIFOY['pac1']: u"5JK", },
                     end = date(2006, 12, 31)))  # TODO: vérif <=2012))  # (f5hk, f5lk, f5jk) codent autre chose sur d'autres années),

build_column('mbic_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KQ",
                                    QUIFOY['conj']: u"5LQ",
                                    QUIFOY['pac1']: u"5MQ", }))  # (f5kq, f5lq, f5mq))

build_column('abic_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KE",
                                    QUIFOY['conj']: u"5LE",
                                    QUIFOY['pac1']: u"5ME", }))  # (f5ke, f5le, f5me))

build_column('nbic_pvce', IntCol(entity = 'ind',
                     label = u"Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)",
                     val_type = "monetary",
                     start = date(2008, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5IK",
                                    QUIFOY['conj']: u"5KK",
                                    QUIFOY['pac1']: u"5MK", }))  # (f5kk, f5ik, f5mk)) TODO: autre 5KK 2005/20006

build_column('macc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NQ",
                                    QUIFOY['conj']: u"5OQ",
                                    QUIFOY['pac1']: u"5PQ", }))  # (f5nq, f5oq, f5pq))

build_column('aacc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5NE",
                                    QUIFOY['conj']: u"5OE",
                                    QUIFOY['pac1']: u"5PE", }))  # (f5ne, f5oe, f5pe))

build_column('nacc_pvce', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     end = date(2010, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5NK",
                                    QUIFOY['conj']: u"5OK",
                                    QUIFOY['pac1']: u"5PK", }))  # (f5nk, f5ok, f5pk)) TODO: 5NK 2005/2006

build_column('mncn_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5KV",
                                    QUIFOY['conj']: u"5LV",
                                    QUIFOY['pac1']: u"5MV", }))  # (f5kv, f5lv, f5mv))

build_column('cncn_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)",
                     val_type = "monetary",
                     start = date(2006, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5SO",
                                    QUIFOY['conj']: u"5NT",
                                    QUIFOY['pac1']: u"5OT", }))  # (f5so, f5nt, f5ot))

build_column('mbnc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HR",
                                    QUIFOY['conj']: u"5IR",
                                    QUIFOY['pac1']: u"5JR", }))  # (f5hr, f5ir, f5jr))

build_column('abnc_pvce', IntCol(entity = 'ind',
                     label = u"Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5QD",
                                    QUIFOY['conj']: u"5RD",
                                    QUIFOY['pac1']: u"5SD", }))  # (f5qd, f5rd, f5sd))

build_column('nbnc_pvce', IntCol(entity = 'ind',
                     label = u"Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5QJ",
                                    QUIFOY['conj']: u"5RJ",
                                    QUIFOY['pac1']: u"5SJ", }))  # (f5qj, f5rj, f5sj)) #TODO 5*J 2005/2006 (qui se transforme en 5*D...)

build_column('frag_fore', IntCol(entity = 'ind',
                     label = u"Revenus des exploitants forestiers (régime du forfait)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HD",
                                    QUIFOY['conj']: u"5ID",
                                    QUIFOY['pac1']: u"5JD", }))

build_column('arag_sjag', IntCol(entity = 'ind',
                     label = u"Abattement pour les jeunes agriculteurs des revenus agricoles sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2011, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HZ",
                                    QUIFOY['conj']: u"5IZ",
                                    QUIFOY['pac1']: u"5JZ", }))

build_column('abic_impm', IntCol(entity = 'ind',
                     label = u"Locations meublées imposables avec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HA",
                                    QUIFOY['conj']: u"5IA",
                                    QUIFOY['pac1']: u"5JA", }))

build_column('nbic_impm', IntCol(entity = 'ind',
                     label = u"Locations meublées imposables sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5KA",
                                    QUIFOY['conj']: u"5LA",
                                    QUIFOY['pac1']: u"5MA", }))

build_column('abic_defm', IntCol(entity = 'ind',
                     label = u"Déficits de locations meubléesavec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5QA",
                                    QUIFOY['conj']: u"5RA",
                                    QUIFOY['pac1']: u"5SA", }))

build_column('alnp_imps', IntCol(entity = 'ind',
                     label = u"Locations meublées non professionnelles imposables avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     end = date(2010, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5NA",
                                    QUIFOY['conj']: u"5OA",
                                    QUIFOY['pac1']: u"5PA", }))

build_column('alnp_defs', IntCol(entity = 'ind',
                     label = u"Déficits de locations meublées non professionnelles avec CGA ou viseur (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     end = date(2010, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5NY",
                                    QUIFOY['conj']: u"5OY",
                                    QUIFOY['pac1']: u"5PY", }))

build_column('nlnp_defs', IntCol(entity = 'ind',
                     label = u"Déficits de locations meublées non professionnelles imposables sans CGA (régime du bénéfice réel)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     end = date(2010, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5NZ",
                                    QUIFOY['conj']: u"5OZ",
                                    QUIFOY['pac1']: u"5PZ", }))

build_column('cbnc_assc', IntCol(entity = 'ind',
                     label = u"Agents généraux d'assurances : indemnités de cessation d'activité (revenus non commerciaux professionnels, régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2006, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5QM",
                                    QUIFOY['conj']: u"5RM", }))

build_column('abnc_proc', IntCol(entity = 'ind',
                     label = u"Honoraires de prospection commerciale exonérés avec CGA ou viseur (revenus non commerciaux professionnels, régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5TF",
                                    QUIFOY['conj']: u"5UF",
                                    QUIFOY['pac1']: u"5VF", }))

build_column('nbnc_proc', IntCol(entity = 'ind',
                     label = u"Honoraires de prospection commerciale exonérés sans CGA (revenus non commerciaux professionnels, régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5TI",
                                    QUIFOY['conj']: u"5UI",
                                    QUIFOY['pac1']: u"5VI", }))

build_column('mncn_exon', IntCol(entity = 'ind',
                     label = u"Revenus nets exonérés non commerciaux non professionnels (régime déclaratif spécial ou micro BNC)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5TH",
                                    QUIFOY['conj']: u"5UH",
                                    QUIFOY['pac1']: u"5VH", }))

build_column('cncn_exon', IntCol(entity = 'ind',
                     label = u"Revenus nets exonérés non commerciaux non professionnels (régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2008, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HK",
                                    QUIFOY['conj']: u"5JK",
                                    QUIFOY['pac1']: u"5LK", }))

build_column('cncn_aimp', IntCol(entity = 'ind',
                     label = u"Revenus imposables non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5JG",
                                    QUIFOY['conj']: u"5RF",
                                    QUIFOY['pac1']: u"5SF", }))

build_column('cncn_adef', IntCol(entity = 'ind',
                     label = u"Déficits non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2007, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5JJ",
                                    QUIFOY['conj']: u"5RG",
                                    QUIFOY['pac1']: u"5SG", }))

build_column('cncn_info', IntCol(entity = 'ind',
                     label = u"Inventeurs et auteurs de logiciels : produits taxables à 16%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2009, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5TC",
                                    QUIFOY['conj']: u"5UC",
                                    QUIFOY['pac1']: u"5VC", }))

build_column('cncn_jcre', IntCol(entity = 'ind',
                     label = u"Jeunes créateurs : abattement de 50%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)",
                     val_type = "monetary",
                     start = date(2006, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5SV",
                                    QUIFOY['conj']: u"5SW",
                                    QUIFOY['pac1']: u"5SX", }))

build_column('revimpres', IntCol(entity = 'ind',
                     label = u"Revenus nets à imposer aux prélèvements sociaux",
                     val_type = "monetary",
                     cerfa_field = {QUIFOY['vous']: u"5HY",
                                    QUIFOY['conj']: u"5IY",
                                    QUIFOY['pac1']: u"5JY", }))

build_column('pveximpres', IntCol(entity = 'ind',
                     label = u"Plus-values à long terme exonérées en cas de départ à la retraite à imposer aux prélèvements sociaux",
                     start = date(2006, 1, 1),
                     cerfa_field = {QUIFOY['vous']: u"5HG",
                                    QUIFOY['conj']: u"5IG", }))


build_column('pvtaimpres', IntCol(entity = 'ind',
                     label = u"Plus-values à long terme taxables à 16% à la retraite à imposer aux prélèvements sociaux",
                     end = date(2009, 12, 31),
                     cerfa_field = {QUIFOY['vous']: u"5HZ",
                                    QUIFOY['conj']: u"5IZ",
                                    QUIFOY['pac1']: u"5JZ", }))

build_column('f5qf', IntCol(entity = 'foy',
                label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-6)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5QF'))

build_column('f5qg', IntCol(entity = 'foy',
                label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-5)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5QG'))

build_column('f5qn', IntCol(entity = 'foy',
                label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-4)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5QN'))

build_column('f5qo', IntCol(entity = 'foy',
                label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-3)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5QO'))

build_column('f5qp', IntCol(entity = 'foy',
                label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-2)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5QP'))

build_column('f5qq', IntCol(entity = 'foy',
                label = u"Déficits des revenus agricoles des années antérieures non encore déduits (n-1)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5QQ'))

build_column('f5ga', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-10)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GA'))

build_column('f5gb', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-9)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GB'))

build_column('f5gc', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-8)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GC'))

build_column('f5gd', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-7)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GD'))

build_column('f5ge', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-6)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GE'))

build_column('f5gf', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-5)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GF'))

build_column('f5gg', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-4)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GG'))

build_column('f5gh', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-3)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GH'))

build_column('f5gi', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-2)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GI'))

build_column('f5gj', IntCol(entity = 'foy',
                label = u"Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-1)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5GJ'))

build_column('f5rn', IntCol(entity = 'foy',
                label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-6)",
                val_type = "monetary",
                start = date(2010, 1, 1),
                end = date(2010, 12, 31),
                cerfa_field = u'5RN'))

build_column('f5ro', IntCol(entity = 'foy',
                label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-5)",
                val_type = "monetary",
                cerfa_field = u'5RO'))

build_column('f5rp', IntCol(entity = 'foy',
                label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-4)",
                val_type = "monetary",
                cerfa_field = u'5RP'))

build_column('f5rq', IntCol(entity = 'foy',
                label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-3)",
                val_type = "monetary",
                cerfa_field = u'5RQ'))

build_column('f5rr', IntCol(entity = 'foy',
                label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-2)",
                val_type = "monetary",
                cerfa_field = u'5RR'))

build_column('f5rw', IntCol(entity = 'foy',
                label = u"Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-1)",
                val_type = "monetary",
                cerfa_field = u'5RW'))

build_column('f5ht', IntCol(entity = 'foy',
                label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-6)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5HT'))

build_column('f5it', IntCol(entity = 'foy',
                label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-5)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5IT'))

build_column('f5jt', IntCol(entity = 'foy',
                label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-4)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5JT'))

build_column('f5kt', IntCol(entity = 'foy',
                label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-3)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5KT'))

build_column('f5lt', IntCol(entity = 'foy',
                label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-2)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5LT'))

build_column('f5mt', IntCol(entity = 'foy',
                label = u"Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-1)",
                val_type = "monetary",
                start = date(2007, 1, 1),
                cerfa_field = u'5MT'))

build_column('f5sq', IntCol())


# TODO: Introduit par mes aides à consolider

# Input variables

# Input mensuel
class tns_auto_entrepreneur_chiffre_affaires(Variable):
    column = FloatCol
    entity_class = Individus
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaires en tant qu'auto-entrepreneur"

# Input annuel
class tns_micro_entreprise_chiffre_affaires(Variable):
    column = FloatCol
    entity_class = Individus
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaires en de micro-entreprise"

enum_tns_type_activite = Enum([u'achat_revente', u'bic', u'bnc'])


# TODO remove this ugly is_permanent
class tns_auto_entrepreneur_type_activite(Variable):
    column = EnumCol(enum = enum_tns_type_activite)
    entity_class = Individus
    is_permanent = True
    label = u"Type d'activité de l'auto-entrepreneur"

# TODO remove this ugly is_permanent
class tns_micro_entreprise_type_activite(Variable):
    column = EnumCol(enum = enum_tns_type_activite)
    entity_class = Individus
    is_permanent = True
    label = u"Type d'activité de la micro-entreprise"

# Input sur le dernier exercice. Par convention, sur l'année dernière.
class tns_autres_revenus(Variable):
    column = FloatCol
    entity_class = Individus
    set_input = set_input_divide_by_period
    label = u"Autres revenus non salariés"

class tns_autres_revenus_chiffre_affaires(Variable):
    column = FloatCol
    entity_class = Individus
    set_input = set_input_divide_by_period
    label = u"Chiffre d'affaire pour les TNS non agricoles autres que les AE et ME"

class tns_autres_revenus_type_activite(Variable):
    column = EnumCol(enum = enum_tns_type_activite)
    entity_class = Individus
    is_permanent = True
    label = u"Type d'activité de l'entreprise non AE ni ME"

class tns_employe(Variable):
    column = BoolCol
    entity_class = Individus
    set_input = set_input_dispatch_by_period
    label = u"Le TNS a au moins un employé. Ne s'applique pas pour les agricoles ni auto-entrepreneurs ni micro entreprise"

# Input annuel
class tns_benefice_exploitant_agricole(Variable):
    column = FloatCol
    entity_class = Individus
    set_input = set_input_dispatch_by_period
    label = u"Dernier bénéfice agricole"


# Computed variables

class travailleur_non_salarie(Variable):
    label = u"L'individu a une activité professionnelle non salariée"
    column = BoolCol
    entity_class = Individus

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


class tns_auto_entrepreneur_benefice(Variable):
    column = FloatCol
    label = u"Bénéfice en tant qu'auto-entrepreneur"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        tns_auto_entrepreneur_type_activite = simulation.calculate('tns_auto_entrepreneur_type_activite', period)
        tns_auto_entrepreneur_chiffre_affaires = simulation.calculate('tns_auto_entrepreneur_chiffre_affaires', period)
        bareme = simulation.legislation_at(period.start).tns

        benefice = compute_benefice_auto_entrepreneur_micro_entreprise(bareme, tns_auto_entrepreneur_type_activite, tns_auto_entrepreneur_chiffre_affaires)
        return period, benefice


class tns_micro_entreprise_benefice(Variable) :
    column = FloatCol
    label = u"Bénéfice de la micro entreprise"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_year
        tns_micro_entreprise_type_activite = simulation.calculate('tns_micro_entreprise_type_activite', period)
        tns_micro_entreprise_chiffre_affaires = simulation.calculate('tns_micro_entreprise_chiffre_affaires', period)
        bareme = simulation.legislation_at(period.start).tns

        benefice =  compute_benefice_auto_entrepreneur_micro_entreprise(bareme, tns_micro_entreprise_type_activite, tns_micro_entreprise_chiffre_affaires)
        return period, benefice

# The following formulas take into account 'cotisation sociales'. However, it seems that for all prestations, the 'base ressources' are only using the 'benefice', without deducting the 'cotisation sociales'. Although this rule seems unfair towards independent workers, we are now applying it for all presations and therefore we are not using the following formulas for calculating prestations.

class tns_auto_entrepreneur_revenus_net(Variable) :
    column = FloatCol
    label = u"Revenu d'un auto-entrepreneur"
    entity_class = Individus

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
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', period)
        taux_cotisations_sociales = simulation.legislation_at(period.start).tns.micro_entreprise.cotisations_sociales
        tns_micro_entreprise_charges_sociales = tns_micro_entreprise_benefice * taux_cotisations_sociales
        revenus = tns_micro_entreprise_benefice - tns_micro_entreprise_charges_sociales

        return period, revenus
