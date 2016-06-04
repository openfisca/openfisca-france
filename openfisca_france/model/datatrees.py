# -*- coding: utf-8 -*-

import collections


columns_name_tree_by_entity = collections.OrderedDict([
    ('ind', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'date_naissance',  # Date de naissance
                    'statut_marital',  # Statut marital
                    'salaire_de_base',  # Salaire de base, en général appelé salaire brut, la 1ère ligne sur la fiche de paie
                    'chomage_imposable',  # Autres revenus imposables (chômage, préretraite)
                    'retraite_imposable',  # Pensions, retraites, rentes connues imposables
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Traitements, salaires, primes pour l'emploi et rentes"""),
                ('children', [
                    'activite',  # Activité
                    'frais_reels',  # Frais réels
                    'hsup',  # Heures supplémentaires : revenus exonérés connus
                    'ppe_tp_sa',  # Prime pour l'emploi des salariés: indicateur de travail à temps plein sur l'année entière
                    'ppe_tp_ns',  # Prime pour l'emploi des non-salariés: indicateur de travail à temps plein sur l'année entière
                    'ppe_du_sa',  # Prime pour l'emploi des salariés: nombre d'heures payées dans l'année
                    'ppe_du_ns',  # Prime pour l'emploi des non-salariés: nombre de jours travaillés dans l'année
                    'chomeur_longue_duree',  # Demandeur d'emploi inscrit depuis plus d'un an
                    'taux_csg_remplacement',  # Taux retenu sur la CSG des revenus de remplacment
                    'pensions_alimentaires_percues',  # Pensions alimentaires perçues
                    'pensions_alimentaires_percues_decl',  # Pension déclarée
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Auto-entrepreneur (ayant opté pour le versement libératoire)"""),
                ('children', [
                    'ebic_impv',  # Revenus industriels et commerciaux professionnels imposables: vente de marchandises et assimilées (régime auto-entrepreneur)
                    'ebic_imps',  # Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime auto-entrepreneur)
                    'ebnc_impo',  # Revenus non commerciaux (régime auto-entrepreneur ayant opté pour le versement libératoire)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus agricoles"""),
                ('children', [
                    'frag_exon',  # Revenus agricoles exonérés (régime du forfait)
                    'frag_impo',  # Revenus agricoles imposables (régime du forfait)
                    'frag_pvct',  # Plus-values agricoles  à court terme (régime du forfait)
                    'frag_pvce',  # Plus-values agricoles de cession taxables à 16% (régime du forfait)
                    'arag_exon',  # Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur), activités exercées en Corse
                    'arag_impg',  # Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'arag_defi',  # Déficits agricoles (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'arag_pvce',  # Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    'nrag_exon',  # Revenus agricoles exonérés yc plus-values (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur), activités exercées en Corse
                    'nrag_impg',  # Revenus agricoles imposables, cas général moyenne triennale (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)
                    'nrag_defi',  # Déficits agricoles (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)
                    'nrag_pvce',  # Plus-values agricoles de cession taxables à 16% (Régime du bénéfice réel, revenus ne bénéficiant pas de l'abattement CGA ou viseur)
                    'nrag_ajag',  # Jeunes agriculteurs, Abattement de 50% ou 100% (Régime du bénéfice réel, revenus bénéficiant de l'abattement CGA ou viseur)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus industriels et commerciaux professionnels"""),
                ('children', [
                    'mbic_exon',  # Revenus industriels et commerciaux professionnels nets exonérés (régime micro entreprise)
                    'mbic_impv',  # Revenus industriels et commerciaux professionnels imposables: vente de marchandises (régime micro entreprise)
                    'mbic_imps',  # Revenus industriels et commerciaux professionnels imposables: prestations de services et locations meublées (régime micro entreprise)
                    'mbic_pvct',  # Plus-values industrielles et commerciales professionnels imposables: plus-values nettes à court terme (régime micro entreprise)
                    'mbic_mvlt',  # Moins-values industrielles et commerciales professionnels à long terme (régime micro entreprise)
                    'mbic_pvce',  # Plus-values industrielles et commerciales professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)
                    'abic_exon',  # Revenus industriels et commerciaux nets exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_exon',  # Revenus industriels et commerciaux nets exonérés yc plus-values sans CGA (régime du bénéfice réel)
                    'abic_impn',  # Revenus industriels et commerciaux imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'abic_imps',  # Revenus industriels et commerciaux imposables: régime simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_impn',  # Revenus industriels et commerciaux professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nbic_imps',  # Revenus industriels et commerciaux professionnels imposables: régime simplifié sans CGA (régime du bénéfice réel)
                    'abic_defn',  # Déficits industriels et commerciaux: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'abic_defs',  # Déficits industriels et commerciaux: simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_defn',  # Déficits industriels et commerciaux: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nbic_defs',  # Locations déjà soumises aux prélèvements sociaux sans CGA (régime du bénéfice réel)
                    'nbic_apch',  # Artisans pêcheurs : abattement 50% avec CGA ou viseur (régime du bénéfice réel)
                    'abic_pvce',  # Plus-values industrielles et commerciales de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)
                    'nbic_pvce',  # Revenus non commerciaux non professionnels exonérés sans AA (régime de la déclaration controlée)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus industriels et commerciaux non professionnels"""),
                ('children', [
                    'macc_exon',  # Revenus industriels et commerciaux non professionnels nets exonérés (régime micro entreprise)
                    'aacc_exon',  # Revenus industriels et commerciaux non professionnels exonérés yc plus-values avec CGA ou viseur (régime du bénéfice réel)
                    'nacc_exon',  # Revenus industriels et commerciaux non professionnels exonérés yc plus-values sans CGA (régime du bénéfice réel)
                    'macc_impv',  # Revenus industriels et commerciaux non professionnels imposables: vente de marchandises et assimilées (régime micro entreprise)
                    'macc_imps',  # Revenus industriels et commerciaux non professionnels imposables: prestations de services (régime micro entreprise)
                    'aacc_impn',  # Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'aacc_imps',  # Locations meublées non professionnelles (régime micro entreprise)
                    'aacc_defn',  # Déficits industriels et commerciaux non professionnels: régime normal ou simplifié avec CGA ou viseur (régime du bénéfice réel)
                    'aacc_defs',  # Déficits de revenus industriels et commerciaux non professionnels avec CGA (régime simplifié du bénéfice réel)
                    'nacc_impn',  # Revenus industriels et commerciaux non professionnels imposables: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nacc_defn',  # Déficits industriels et commerciaux non professionnels: régime normal ou simplifié sans CGA (régime du bénéfice réel)
                    'nacc_defs',  # Locations meublées non professionnelles: Gîtes ruraux et chambres d'hôtes déjà soumis aux prélèvements sociaux avec CGA (régime du bénéfice réel)
                    'macc_pvct',  # Plus-values industrielles et commerciales non professionnelles imposables: plus-values nettes à court terme (régime micro entreprise)
                    'macc_mvlt',  # Moins-values industrielles et commerciales non professionnelles à long terme (régime micro entreprise)
                    'macc_pvce',  # Plus-values industrielles et commerciales non professionnelles imposables: plus-values de cession taxables à 16% (régime micro entreprise)
                    'aacc_pvce',  # Plus-values industrielles et commerciales non professionnelles de cession taxables à 16% avec CGA ou viseur (régime du bénéfice réel)
                    'nacc_pvce',  # Locations meublées non professionnelles: Revenus imposables sans CGA (régime du bénéfice réel)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus non commerciaux professionnels"""),
                ('children', [
                    'mbnc_exon',  # Revenus non commerciaux professionnels nets exonérés (régime déclaratif spécial ou micro BNC)
                    'abnc_exon',  # Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_exon',  # Revenus non commerciaux professionnels exonérés (yc compris plus-values) (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)
                    'mbnc_impo',  # Revenus non commerciaux professionnels imposables (régime déclaratif spécial ou micro BNC)
                    'abnc_impo',  # Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'abnc_defi',  # Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_impo',  # Revenus non commerciaux professionnels imposables (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)
                    'nbnc_defi',  # Déficits non commerciaux professionnels (régime de la déclaration controlée, revenus ne bénéficiant pas de l'abattement association agrée)
                    'mbnc_pvct',  # Plus-values non commerciales professionnelles imposables et Plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)
                    'mbnc_mvlt',  # Moins-values non commerciales professionnelles à long terme (régime déclaratif spécial ou micro BNC)
                    'mbnc_pvce',  # Plus-values non commerciales professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)
                    'abnc_pvce',  # Plus-values non commerciaux professionnels de cession taxables à 16% (régime de la déclaration controlée, revenus bénéficiant de l'abattement association agrée ou viseur)
                    'nbnc_pvce',  # Déficits industriels et commerciaux: locations meublées sans CGA (régime du bénéfice réel)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus non commerciaux non professionnels"""),
                ('children', [
                    'mncn_impo',  # Revenus non commerciaux non professionnels imposables (régime déclaratif spécial ou micro BNC)
                    'cncn_bene',  # Revenus non commerciaux non professionnels imposables sans AA (régime de la déclaration controlée)
                    'cncn_defi',  # Déficits non commerciaux non professionnels sans AA (régime de la déclaration controlée)
                    'mncn_pvct',  # Plus-values non commerciales non professionnelles imposables et plus-values nettes à court terme (régime déclaratif spécial ou micro BNC)
                    'mncn_mvlt',  # Moins-values non commerciales non professionnelles à long terme (régime déclaratif spécial ou micro BNC)
                    'mncn_pvce',  # Plus-values non commerciales non professionnelles de cession taxables à 16% (régime déclaratif spécial ou micro BNC)
                    'cncn_pvce',  # Plus-values non commerciales non professionnelles taxables à 16% avec AA ou viseur (régime de la déclaration controlée)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""adoption""",  # Enfant adopté
                    u"""garde_alternee""",  # Enfant en garde alternée
                    u"""enceinte""",  # Est enceinte
                    u"""handicap""",  # handicap
                    u"""rempli_obligation_scolaire""",  # Rempli l'obligation scolaire
                    u"""coloc""",  # Vie en colocation
                    u"""logement_chambre""",  # Le logement est considéré comme une chambre
                    u"""etr""",
                    u"""f6ps""",  # Plafond de déduction épargne retraite (plafond calculé sur les revenus perçus en n-1)
                    u"""f6rs""",  # Cotisations d'épargne retraite versées au titre d'un PERP, PREFON, COREM et C.G.O.S
                    u"""f6ss""",  # Rachat de cotisations PERP, PREFON, COREM et C.G.O.S
                    u"""f7ac""",  # Cotisations syndicales des salariées et pensionnés
                    u"""elig_creimp_jeunes""",  # Éligible au crédit d'impôt jeunes
                    u"""jei_date_demande""",  # Date de demande (et d'octroi) du statut de jeune entreprise innovante (JEI)
                    u"""stage_duree_heures""",  # Nombre d'heures effectuées en stage
                    u"""stage_gratification_taux""",  # Taux de gratification (en plafond de la Sécurité sociale)
                    u"""scolarite""",  # Scolarité de l'enfant : collège, lycée...
                    u"""boursier""",  # Élève ou étudiant boursier
                    u"""inapte_travail""",  # Reconnu inapte au travail
                    u"""taux_incapacite""",  # Taux d'incapacité
                    u"""ass_precondition_remplie""",  # Éligible à l'ASS
                    u"""categ_inv""",  # Catégorie de handicap (AEEH)
                    u"""pensions_alimentaires_versees_individu""",  # Pensions alimentaires versées pour un individu
                    u"""gains_exceptionnels""",  # Gains exceptionnels
                    u"""allocation_aide_retour_emploi""",  # Allocation d'aide au retour à l'emploi
                    u"""allocation_securisation_professionnelle""",  # Allocation de sécurisation professionnelle
                    u"""prime_forfaitaire_mensuelle_reprise_activite""",  # Prime forfaitaire mensuelle pour la reprise d'activité
                    u"""indemnites_volontariat""",  # Indemnités de volontariat
                    u"""dedommagement_victime_amiante""",  # Dédommagement versé aux victimes de l'amiante
                    u"""prestation_compensatoire""",  # Dédommagement versé aux victimes de l'amiante
                    u"""pensions_invalidite""",  # Pensions d'invalidité
                    u"""bourse_enseignement_sup""",  # Bourse de l'enseignement supérieur
                    u"""f5qm""",  # Agents généraux d’assurances: indemnités de cessation d’activité
                    u"""nbic_mvct""",  # Revenus industriels et commerciaux professionnels moins-values nettes à court terme
                    u"""aacc_gits""",  # Location de gîtes ruraux, chambres d'hôtes et meublés de tourisme (régime micro entreprise)
                    u"""nacc_meup""",  # Locations meublées non professionnelles: Locations déjà soumises aux prélèvements sociaux (régime micro entreprise)
                    u"""mbnc_mvct""",  # Moins-values non commerciales professionnelles nettes à court terme (régime déclaratif spécial ou micro BNC)
                    u"""frag_fore""",  # Revenus des exploitants forestiers (régime du forfait)
                    u"""arag_sjag""",  # Abattement pour les jeunes agriculteurs des revenus agricoles sans CGA (régime du bénéfice réel)
                    u"""abic_impm""",  # Locations meublées imposables avec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)
                    u"""nbic_impm""",  # Locations meublées imposables sans CGA (régime du bénéfice réel)
                    u"""abic_defm""",  # Déficits de locations meubléesavec CGA ou viseur (régime du bénéfice réel pour les revenus industriels et commerciaux professionnels)
                    u"""alnp_imps""",  # Locations meublées non professionnelles imposables avec CGA ou viseur (régime du bénéfice réel)
                    u"""alnp_defs""",  # Déficits de locations meublées non professionnelles avec CGA ou viseur (régime du bénéfice réel)
                    u"""nlnp_defs""",  # Déficits de locations meublées non professionnelles imposables sans CGA (régime du bénéfice réel)
                    u"""cbnc_assc""",  # Agents généraux d'assurances : indemnités de cessation d'activité (revenus non commerciaux professionnels, régime de la déclaration contrôlée)
                    u"""abnc_proc""",  # Honoraires de prospection commerciale exonérés avec CGA ou viseur (revenus non commerciaux professionnels, régime de la déclaration contrôlée)
                    u"""nbnc_proc""",  # Honoraires de prospection commerciale exonérés sans CGA (revenus non commerciaux professionnels, régime de la déclaration contrôlée)
                    u"""mncn_exon""",  # Revenus nets exonérés non commerciaux non professionnels (régime déclaratif spécial ou micro BNC)
                    u"""cncn_exon""",  # Revenus nets exonérés non commerciaux non professionnels (régime de la déclaration contrôlée)
                    u"""cncn_aimp""",  # Revenus imposables non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)
                    u"""cncn_adef""",  # Déficits non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)
                    u"""cncn_info""",  # Inventeurs et auteurs de logiciels : produits taxables à 16%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)
                    u"""cncn_jcre""",  # Jeunes créateurs : abattement de 50%, revenus non commerciaux non professionnels avec CGA (régime de la déclaration contrôlée)
                    u"""revimpres""",  # Revenus nets à imposer aux prélèvements sociaux
                    u"""pveximpres""",  # Plus-values à long terme exonérées en cas de départ à la retraite à imposer aux prélèvements sociaux
                    u"""pvtaimpres""",  # Plus-values à long terme taxables à 16% à la retraite à imposer aux prélèvements sociaux
                    u"""f5sq""",
                    u"""tns_auto_entrepreneur_chiffre_affaires""",  # Chiffre d'affaires en tant qu'auto-entrepreneur
                    u"""tns_micro_entreprise_chiffre_affaires""",  # Chiffre d'affaires en de micro-entreprise
                    u"""tns_auto_entrepreneur_type_activite""",  # Type d'activité de l'auto-entrepreneur
                    u"""tns_micro_entreprise_type_activite""",  # Type d'activité de la micro-entreprise
                    u"""tns_autres_revenus""",  # Autres revenus non salariés
                    u"""tns_autres_revenus_chiffre_affaires""",  # Chiffre d'affaire pour les TNS non agricoles autres que les AE et ME
                    u"""tns_autres_revenus_type_activite""",  # Type d'activité de l'entreprise non AE ni ME
                    u"""tns_avec_employe""",  # Le TNS a au moins un employé. Ne s'applique pas pour les agricoles ni auto-entrepreneurs ni micro entreprise
                    u"""tns_benefice_exploitant_agricole""",  # Dernier bénéfice agricole
                    u"""indemnites_stage""",  # Indemnités de stage
                    u"""revenus_stage_formation_pro""",  # Revenus de stage de formation professionnelle
                    u"""bourse_recherche""",  # Bourse de recherche
                    u"""sal_pen_exo_etr""",  # Salaires et pensions exonérés de source étrangère retenus pour le calcul du taux effectif
                    u"""nbsala""",  # Nombre de salariés dans l'établissement de l'emploi actuel
                    u"""tva_ent""",  # L'entreprise employant le salarié paye de la TVA
                    u"""exposition_accident""",  # Exposition au risque pour les accidents du travail
                    u"""allegement_fillon_mode_recouvrement""",  # Mode de recouvrement des allègements Fillon
                    u"""allegement_cotisation_allocations_familiales_mode_recouvrement""",  # Mode de recouvrement de l'allègement de la cotisation d'allocations familiales
                    u"""apprentissage_contrat_debut""",  # Date de début du contrat d'apprentissage
                    u"""arrco_tranche_a_taux_employeur""",  # Taux ARRCO tranche A employeur) propre à l'entreprise
                    u"""arrco_tranche_a_taux_salarie""",  # Taux ARRCO tranche A salarié) propre à l'entreprise
                    u"""assujettie_taxe_salaires""",  # Entreprise assujettie à la taxe sur les salaires
                    u"""avantage_en_nature_valeur_reelle""",  # Avantages en nature (Valeur réelle)
                    u"""indemnites_compensatrices_conges_payes""",
                    u"""contrat_de_travail""",  # Type contrat de travail
                    u"""contrat_de_travail_debut""",  # Date d'arrivée dans l'entreprise
                    u"""contrat_de_travail_fin""",  # Date de départ de l'entreprise
                    u"""contrat_de_travail_duree""",  # Type (durée determinée ou indéterminée) du contrat de travail
                    u"""cotisation_sociale_mode_recouvrement""",  # Mode de recouvrement des cotisations sociales
                    u"""depcom_entreprise""",  # Localisation entreprise (depcom)
                    u"""code_postal_entreprise""",  # Localisation entreprise (Code postal)
                    u"""effectif_entreprise""",  # Effectif de l'entreprise
                    u"""entreprise_assujettie_cet""",  # Entreprise assujettie à la contribution économique territoriale
                    u"""entreprise_assujettie_is""",  # Entreprise assujettie à l'impôt sur les sociétés (IS)
                    u"""entreprise_assujettie_tva""",  # Entreprise assujettie à la TVA
                    u"""entreprise_benefice""",  # Bénéfice de l'entreprise
                    u"""entreprise_bilan""",  # Bilan de l'entreprise
                    u"""entreprise_chiffre_affaire""",  # Chiffre d'affaire de l'entreprise
                    u"""entreprise_creation""",  # Date de création de l'entreprise
                    u"""nombre_tickets_restaurant""",  # Nombre de tickets restaurant
                    u"""nouvelle_bonification_indiciaire""",  # Nouvelle bonification indicaire
                    u"""prevoyance_obligatoire_cadre_taux_employe""",  # Taux de cotisation employeur pour la prévoyance obligatoire des cadres
                    u"""prevoyance_obligatoire_cadre_taux_employeur""",  # Taux de cotisation employeur pour la prévoyance obligatoire des cadres
                    u"""primes_salaires""",  # Indemnités, primes et avantages en argent
                    u"""prise_en_charge_employeur_prevoyance_complementaire""",  # Part salariale des cotisations de prévoyance complémentaire prise en charge par l'employeur
                    u"""prise_en_charge_employeur_retraite_complementaire""",  # Part salariale des cotisations de retraite complémentaire prise en charge par l'employeur
                    u"""prise_en_charge_employeur_retraite_supplementaire""",  # Part salariale des cotisations de retraite supplémentaire prise en charge par l'employeur
                    u"""ratio_alternants""",  # Ratio d'alternants dans l'effectif moyen
                    u"""redevable_taxe_apprentissage""",  # Entreprise redevable de la taxe d'apprentissage
                    u"""remboursement_transport_base""",  # Base pour le calcul du remboursement des frais de transport
                    u"""indemnites_forfaitaires""",  # Indemnités forfaitaires (transport, nourriture)
                    u"""titre_restaurant_taux_employeur""",  # Taux de participation de l'employeur au titre restaurant
                    u"""titre_restaurant_valeur_unitaire""",  # Valeur faciale unitaire du titre restaurant
                    u"""titre_restaurant_volume""",  # Volume des titres restaurant
                    u"""traitement_indiciaire_brut""",  # Traitement indiciaire brut (TIB)
                    u"""categorie_salarie""",  # Catégorie de salarié
                    u"""heures_duree_collective_entreprise""",  # Durée mensuelle collective dans l'entreprise (heures, temps plein)
                    u"""heures_non_remunerees_volume""",  # Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)
                    u"""heures_remunerees_volume""",  # Volume des heures rémunérées contractuellement (heures/mois, temps partiel)
                    u"""forfait_heures_remunerees_volume""",  # Volume des heures rémunérées à un forfait heures
                    u"""forfait_jours_remuneres_volume""",  # Volume des heures rémunérées à forfait jours
                    u"""volume_jours_ijss""",  # Volume des jours pour lesquels sont versés une idemnité journalière par la sécurité sociale
                    u"""epargne_non_remuneree""",  # Épargne non rémunérée
                    u"""interets_epargne_sur_livrets""",  # Intérêts versés pour l'épargne sur livret
                    u"""revenus_capital""",  # Revenus du capital
                    u"""revenus_locatifs""",  # Revenus locatifs
                    u"""valeur_locative_immo_non_loue""",  # Valeur locative des biens immobiliers possédés et non loués
                    u"""valeur_locative_terrains_non_loue""",  # Valeur locative des terrains possédés et non loués
                    u"""f1tv""",  # Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 1 et 2 ans
                    u"""f1tw""",  # Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 2 et 3 ans
                    u"""f1tx""",  # Gains de levée d'options sur titres en cas de cession ou de conversion au porteur dans le délai d'indisponibilité: entre 3 et 4 ans
                    u"""f3vd""",  # Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 18 %
                    u"""f3vf""",  # Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 41 %
                    u"""f3vi""",  # Gains de levée d'options sur titres et gains d'acquisition d'actions taxables à 30 %
                    u"""f3vj""",  # Gains imposables sur option dans la catégorie des salaires
                    u"""f3va""",  # Abattement pour durée de détention des titres en cas de départ à la retraite d'un dirigeant appliqué sur des plus-values
                    u"""chomage_brut""",  # Chômage brut
                    u"""indemnites_chomage_partiel""",  # Indemnités de chômage partiel
                    u"""retraite_brute""",  # Retraite brute
                    u"""aer""",  # Allocation équivalent retraite (AER)
                    u"""retraite_combattant""",  # Retraite du combattant
                    u"""indemnites_journalieres_maternite""",  # Indemnités journalières de maternité
                    u"""indemnites_journalieres_paternite""",  # Indemnités journalières de paternité
                    u"""indemnites_journalieres_adoption""",  # Indemnités journalières d'adoption
                    u"""indemnites_journalieres_maladie""",  # Indemnités journalières de maladie
                    u"""indemnites_journalieres_accident_travail""",  # Indemnités journalières d'accident du travail
                    u"""indemnites_journalieres_maladie_professionnelle""",  # Indemnités journalières de maladie professionnelle
                    ]),
                ]),
            ]),
        ])),
    ('fam', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    u"""inactif""",  # Parent inactif (PAJE-CLCA)
                    u"""partiel1""",  # Parent actif à moins de 50% (PAJE-CLCA)
                    u"""partiel2""",  # Parent actif entre 50% et 80% (PAJE-CLCA)
                    u"""opt_colca""",  # Opte pour le COLCA
                    u"""empl_dir""",  # Emploi direct (CLCMG)
                    u"""ass_mat""",  # Assistante maternelle (CLCMG)
                    u"""gar_dom""",  # Garde à domicile (CLCMG)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""proprietaire_proche_famille""",  # Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint
                    u"""paje_prepare""",  # Prestation Partagée d’éducation de l’Enfant (PreParE)
                    ]),
                ]),
            ]),
        ])),
    ('foy', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    u"""jour_xyz""",  # Jours décomptés au titre de cette déclaration
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Situations particulières"""),
                ('children', [
                    'caseK',  # Situation pouvant donner droit à une demi-part supplémentaire: vous avez eu un enfant décédé après l’âge de 16 ans ou par suite de faits de guerre
                    'caseL',  # Situation pouvant donner droit à une demi-part supplémentaire: vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant au moins 5 ans durant la période où vous viviez seul
                    'caseE',  # Situation pouvant donner droit à une demi-part supplémentaire : vous vivez seul au 1er janvier de l'année de perception des revenus et vous avez élevé un enfant pendant moins de 5 ans durant la période où vous viviez seul
                    'caseN',  # Vous ne viviez pas seul au 1er janvier de l'année de perception des revenus
                    'caseP',  # Titulaire d'une pension pour une invalidité d'au moins 40 % ou d'une carte d'invalidité d'au moins 80%
                    'caseF',  # Situation pouvant donner droit à une demi-part supplémentaire : conjoint titulaire d'une pension ou d'une carte d'invalidité (vivant ou décédé l'année de perception des revenus)
                    'caseW',  # Vous ou votre conjoint (même s'il est décédé), âgés de plus de 75 ans, êtes titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre
                    'caseS',  # Vous êtes mariés/pacsés et l'un des deux déclarants âgé de plus de 75 ans est titulaire de la carte du combattant ou d'une pension militaire d'invalidité ou de victime de guerre
                    'caseG',  # Titulaire d'une pension de veuve de guerre
                    'caseH',  # Année de naissance des enfants à charge en garde alternée
                    'nbN',  # Nombre d'enfants mariés/pacsés et d'enfants non mariés chargés de famille
                    'nbR',  # Nombre de titulaires (autres que les enfants) de la carte invalidité d'au moins 80 %
                    'caseT',  # Vous êtes parent isolé au 1er janvier de l'année de perception des revenus
                    'rfr_n_2',  # Revenu fiscal de référence année n - 2
                    'nbptr_n_2',  # Nombre de parts année n - 2
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Traitements, salaires, primes pour l'emploi, pensions et rentes"""),
                ('children', [
                    'f1aw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : Moins de 50 ans
                    'f1bw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 50 à 59 ans
                    'f1cw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : De 60 à 69 ans
                    'f1dw',  # Rentes viagères à titre onéreux perçues par le foyer par âge d'entrée en jouissance : A partir de 70 ans
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus des valeurs et capitaux mobiliers"""),
                ('children', [
                    'f2da',  # Revenus des actions et parts soumis au prélèvement libératoire de 21 %
                    'f2dh',  # Produits d’assurance-vie et de capitalisation soumis au prélèvement libératoire de 7.5 %
                    'f2ee',  # Autres produits de placement soumis aux prélèvements libératoires
                    'f2dc',  # Revenus des actions et parts donnant droit à abattement
                    'f2fu',  # Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise donnant droit à abattement
                    'f2ch',  # Produits des contrats d'assurance-vie et de capitalisation d'une durée d'au moins 6 ou 8 ans donnant droit à abattement
                    'f2ts',  # Revenus de valeurs mobilières, produits des contrats d'assurance-vie d'une durée inférieure à 8 ans et distributions (n'ouvrant pas droit à abattement)
                    'f2go',  # Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (n'ouvrant pas droit à abattement)
                    'f2tr',  # Produits de placements à revenu fixe, intérêts et autres revenus assimilés (n'ouvrant pas droit à abattement)
                    'f2cg',  # Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux sans CSG déductible
                    'f2bh',  # Revenus des lignes 2DC, 2CH, 2TS, 2TR déjà soumis au prélèvement sociaux avec CSG déductible
                    'f2ca',  # Frais et charges déductibles
                    'f2aa',  # Déficits des années antérieures non encore déduits
                    'f2ab',  # Crédits d'impôt sur valeurs étrangères
                    'f2al',  # Déficits des années antérieures non encore déduits
                    'f2am',  # Déficits des années antérieures non encore déduits
                    'f2an',  # Déficits des années antérieures non encore déduits
                    'f2aq',  # Déficits des années antérieures non encore déduits
                    'f2ar',  # Déficits des années antérieures non encore déduits
                    'f2as',  # Déficits des années antérieures non encore déduits: année 2012
                    'f2gr',  # Revenus distribués dans le PEA (pour le calcul du crédit d'impôt de 50 %)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Plus-values de cession de valeurs mobilières, droits sociaux et gains assimilés"""),
                ('children', [
                    'f3vc',  # Produits et plus-values exonérés provenant de structure de capital-risque
                    'f3ve',  # Plus-values réalisées par les non-résidents pour lesquelles vous demandez le remboursement de l'excédent du prélèvement de 45 %
                    'f3vl',  # Distributions par des sociétés de capital-risque taxables à 19 %
                    'f3vm',  # Clôture du PEA avant l'expiration de la 2e année: gains taxables à 22.5 %
                    'f3vg',  # Plus-value imposable sur gains de cession de valeurs mobilières, de droits sociaux et gains assimilés
                    'f3vh',  # Perte de l'année de perception des revenus
                    'f3vt',  # Clôture du PEA  entre la 2e et la 5e année: gains taxables à 19 %
                    'f3vu',
                    'f3vv',  # Plus-values réalisées par les non-résidents: montant du prélèvement de 45 % déjà versé
                    'f3si',
                    'f3sa',
                    'f3sf',
                    'f3sd',
                    'f3vz',  # Plus-values imposables sur cessions d’immeubles ou de biens meubles
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Revenus fonciers"""),
                ('children', [
                    'f4ba',  # Revenus fonciers imposables
                    'f4bb',  # Déficit imputable sur les revenus fonciers
                    'f4bc',  # Déficit imputable sur le revenu global
                    'f4bd',  # Déficits antérieurs non encore imputés
                    'f4be',  # Micro foncier: recettes brutes sans abattement
                    'f4bf',  # Primes d'assurance pour loyers impayés des locations conventionnées
                    'f4bl',
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Charges déductibles"""),
                ('children', [
                    'f6de',  # CSG déductible calculée sur les revenus du patrimoine
                    'f6gi',  # Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 1er enfant
                    'f6gj',  # Pensions alimentaires versées à des enfants majeurs (décision de justice définitive avant 2006): 2eme enfant
                    'f6el',  # Autres pensions alimentaires versées à des enfants majeurs: 1er enfant
                    'f6em',  # Autres pensions alimentaires versées à des enfants majeurs: 2eme enfant
                    'f6gp',  # Autres pensions alimentaires versées décision de justice définitive avant 2006 (mineurs, ascendants)
                    'f6gu',  # Autres pensions alimentaires versées (mineurs, ascendants)
                    'f6eu',  # Frais d'accueil de personnes de plus de 75 ans dans le besoin
                    'f6ev',  # Nombre de personnes de plus de 75 ans dans le besoin accueillies sous votre toit
                    'f6dd',  # Déductions diverses
                    'f6aa',  # Souscriptions en faveur du cinéma ou de l’audiovisuel
                    'f6cc',  # Souscriptions au capital des SOFIPÊCHE
                    'f6eh',
                    'f6da',  # Pertes en capital consécutives à la souscription au capital de sociétés nouvelles ou de sociétés en difficulté
                    'f6cb',  # Dépenses de grosses réparations effectuées par les nus-propriétaires (dépenses réalisées au cours de l'année de perception des revenus)
                    'f6hj',  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    'f6gh',  # Sommes à ajouter au revenu imposable
                    'f6fa',  # Deficits globaux des années antérieures non encore déduits les années précédentes: année de perception des revenus -6
                    'f6fb',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -5
                    'f6fc',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -4
                    'f6fd',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -3
                    'f6fe',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -2
                    'f6fl',  # Deficits globaux des années antérieures non encore déduits: année de perception des revenus -1
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Charges déductibles (autres)"""),
                ('children', [
                    'f7ud',  # Dons à des organismes d'aide aux personnes en difficulté
                    'f7uf',  # Dons à d'autres oeuvres d'utilité publique ou fiscalement assimilables aux oeuvres d'intérêt général
                    'f7xs',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -5
                    'f7xt',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -4
                    'f7xu',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -3
                    'f7xw',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -2
                    'f7xy',  # Report des années antérieures des dons (report des réductions et crédits d'impôt): année de perception des revenus -1
                    'f7db',  # Sommes versées pour l'emploi d'un salarié à domicile par les personnes ayant excercé une activité professionnelle ou ayant été demandeur d'emploi l'année de perception des revenus déclarés
                    'f7df',  # Sommes versées pour l'emploi d'un salarié à domicile par les personnes retraités, ou inactives l'année de perception des revenus déclarés
                    'f7dq',  # Emploi direct pour la première fois d'un salarié à domicile durant l'année de perception des revenus déclarés
                    'f7dg',  # Vous, votre conjoint ou une personne à votre charge à une carte d'invalidité d'au moins 80 % l'année de perception des revenus déclarés
                    'f7dl',  # Nombre d'ascendants bénéficiaires de l'APA, âgés de plus de 65 ans, pour lesquels des dépenses ont été engagées l'année de perception des revenus déclarés
                    'f7vy',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): Première annuité
                    'f7vz',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements anciens (acquis entre le 06/05/2007 et le 30/09/2011) ou neufs (acquis entre le 06/05/2007 et le 31/12/2009): annuités suivantes
                    'f7vx',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs BBC acquis ou construits du 01/01/2009 au 30/09/2011
                    'f7vw',  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: première annuité
                    'f7cd',  # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 1ere personne
                    'f7ce',  # Dépenses d'accueil dans un établissement pour personnes âgées dépendantes: 2éme personne
                    'f7ga',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge
                    'f7gb',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge
                    'f7gc',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge
                    'f7ge',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 1er enfant à charge en résidence alternée
                    'f7gf',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 2ème enfant à charge en résidence alternée
                    'f7gg',  # Frais de garde des enfants de moins de 6 ans au 01/01 de l'année de perception des revenus: 3ème enfant à charge en résidence alternée
                    'f7ea',  # Nombre d'enfants à charge poursuivant leurs études au collège
                    'f7eb',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études au collège
                    'f7ec',  # Nombre d'enfants à charge poursuivant leurs études au lycée
                    'f7ed',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études au lycée
                    'f7ef',  # Nombre d'enfants à charge poursuivant leurs études dans l'enseignement supérieur
                    'f7eg',  # Nombre d'enfants à charge en résidence alternée poursuivant leurs études dans l'enseignement supérieur
                    'f7td',  # Intérêts des prêts étudiants versés avant l'année de perception des revenus déclarés
                    'f7vo',  # Nombre d'années de remboursement du prêt étudiant avant l'année de perception des revenus déclarés
                    'f7uk',  # Intérêts des prêts étudiants versés durant l'année de perception des revenus déclarés
                    'f7gz',  # Primes de rente survie, contrats d'épargne handicap
                    'f7wm',  # Prestations compensatoires: Capital fixé en substitution de rente
                    'f7wn',  # Prestations compensatoires: Sommes versées l'année de perception des revenus déclarés
                    'f7wo',  # Prestations compensatoires: Sommes totales décidées par jugement l'année de perception des revenus déclarés ou capital reconstitué
                    'f7wp',  # Prestations compensatoires: Report des sommes décidées l'année de perception des revenus -1
                    'f7we',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés
                    'f7wq',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées du 01/01/2012 au 03/04/2012
                    'f7wh',  # Dépenses en faveur de la qualité environnementale de l'habitation principale (logement achevé depuis plus de 2 ans): bouquet de travaux réalisé pendant l'année de perception des revenus
                    'f7wk',  # Votre habitation principale est une maison individuelle
                    'f7wf',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées avant le 01/01/n-1
                    'f7wi',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: Ascenseurs électriques à traction
                    'f7wj',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: équipements spécialement conçus pour les personnes âgées ou handicapées
                    'f7wl',  # Dépenses en faveur de l'aide aux personnes réalisées dans l'habitation principale: travaux de prévention des risques technologiques
                    'f7ur',  # Investissements réalisés en n-1, total réduction d’impôt
                    'f7oz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-6
                    'f7pz',  # Investissements outre-mer réalisés en 2007 dans le cadre d'une entreprise: report de réduction d'impôt non imputée les années antérieures
                    'f7qz',  # Investissements outre-mer réalisés en 2008 dans le casdre d'une entreprise: report de réduction d'impôt non imputée les années antérieures
                    'f7rz',  # Investissements outre-mer: report de réduction d'impôt non imputée les années antérieures année n-3
                    'f7sz',  # Dépenses en faveur de la qualité environnementale des logements donnés en location
                    'f7fy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées avant l'année n-1 et ayant pris fin en année n-1
                    'f7gy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées avant l'année n-1 et ayant pris fin en année n-1
                    'f7jy',  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2010 avec promesse d'achat en 2009 ou réalisés en 2009
                    'f7hy',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions signées en n-1 et n'ayant pas pris fin en n-1
                    'f7ky',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions signées en n-1 et ayant pris fin en n-1
                    'f7iy',  # Report du solde de réduction d'impôt non encore imputé sur les investissements réalisés
                    'f7ly',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés: conventions ayant pas pris fin l'année de perception des revenus déclarés
                    'f7my',  # Aide aux créateurs et repreneurs d'entreprises, nombre de créateurs aidés dont handicapés: conventions ayant pas pris fin l'année de perception des revenus déclarés
                    'f7ra',  # Travaux de restauration immobilière dans une zone de protection du patrimoine architectural, urbain et paysager
                    'f7rb',  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    'f7gw',  # Investissements achevés en n-2 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt
                    'f7gx',  # Investissements achevés en n-2 avec promesse d'achat en n-3 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna : report de 1/5 de la réduction d'impôt
                    'f7xc',  # Investissements locatifs dans le secteur de touristique: prix d'acquisition ou de revient d'un logement neuf acquis ou achevé en n-1
                    'f7xd',  # Investissements locatifs dans le secteur de touristique: logement neuf, demande d'étalement du solde de la réduction d'impôt sur 6 ans
                    'f7xe',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, demande d'étalement du solde de la réduction d'impôt sur 6 ans
                    'f7xf',  # Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures
                    'f7xh',  # Investissements locatifs dans le secteur de touristique: travaux de reconstruction, agrandissement, réparation dans une résidence de tourisme classée ou un meublé de tourisme
                    'f7xi',  # Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures
                    'f7xj',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report des dépenses d'investissement des années antérieures
                    'f7xk',  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    'f7xl',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, prix de revient d'un logement réhabilité en n-1 et achevé depuis moins de 15 ans
                    'f7xm',  # Investissements locatifs dans le secteur de touristique: réhabilitation d'un logement, report de dépenses des travaux de réhabilitation achevés les années antérieures
                    'f7xn',  # Investissements locatifs dans le secteur de touristique, logement neuf: report des dépenses d'investissement des années antérieures
                    'f7xo',  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    'f7cf',  # Souscriptions au capital des PME non cotées, petites entreprises en phase de démarrage, ou d'expansion
                    'f7cl',  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -4
                    'f7cm',  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -3
                    'f7cn',  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -2
                    'f7cu',  # Souscriptions au capital des PME non cotées, montant versé au titre de souscriptions antérieures
                    'f7gs',  # Reports concernant les investissements achevés ou acquis au cours des années antérieures: Investissements réalisés en n-3 en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon
                    'f7ua',
                    'f7ub',
                    'f7uc',  # Cotisations pour la défense des forêts contre l'incendie
                    'f7ui',
                    'f7uj',
                    'f7qb',
                    'f7qc',
                    'f7qd',
                    'f7ql',
                    'f7qt',
                    'f7qm',
                    'f7gq',  # Souscription de parts de fonds communs de placement dans l'innovation
                    'f7fq',  # Souscription de parts de fonds d'investissement de proximité
                    'f7fm',  # Souscription de parts de fonds d'investissement de proximité investis en Corse
                    'f7fl',  # Souscription de parts de fonds d'investissement de proximité investis outre-mer par des personnes domiciliées outre-mer
                    'f7gn',  # Souscriptions au capital de SOFICA 36 %
                    'f7fn',  # Souscriptions au capital de SOFICA 30 %
                    'f7fh',  # Intérêts d'emprunt pour reprise de société
                    'f7ff',  # Frais de comptabilité et d'adhésion à un CGA (centre de gestion agréée) ou à une AA (association agréée)
                    'f7fg',  # Frais de comptabilité et d'adhésion à un CGA ou à une AA: nombre d'exploitations
                    'f7nz',  # Travaux de conservation et de restauration d’objets classés monuments historiques
                    'f7ka',  # Dépenses de protection du patrimoine naturel
                    'f7wg',  # Dépenses en faveur de la qualité environnementale de l'habitation principale: éco-prêt à taux zéro avec offre de prêt émise l'année de perception des revenus déclarés -1
                    'f7uh',  # Dons et cotisations versés aux partis politiques
                    'f7un',  # Investissements forestiers: acquisition
                    'f7um',  # Intérêts pour paiement différé accordé aux agriculteurs
                    'f7hj',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole
                    'f7hk',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM
                    'f7hn',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 en métropole avec promesse d'achat avant le 1er janvier 2010
                    'f7ho',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2010 dans les DOM-COM avec promesse d'achat avant le 1er janvier 2010
                    'f7hl',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 (métropole et DOM ne respectant pas les plafonds)
                    'f7hm',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés en 2009 dans les DOM et respectant les plafonds
                    'f7hr',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques
                    'f7hs',  # Investissements locatifs neufs dispositif Scellier: investissements réalisés et achevés en 2009 dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques
                    'f7la',  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2009
                    'f7ij',  # Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, engagement de réalisation de l'investissement en 2011
                    'f7il',  # Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2011 et achevés en 2012, promesse d'achat en 2010
                    'f7im',  # Investissement destinés à la location meublée non professionnelle: Investissements réalisés en 2010 et achevés en 2012 avec promesse d'achat en 2009
                    'f7ik',  # Investissements destinés à la location meublée non professionnelle : Reports de 1/9 de l'investissement réalisé et achevé en 2009
                    'f7is',  # Investissements destinés à la location meublée non professionnelle : Report du solde de réduction d'impôt non encore imputé: année  n-4
                    'f7gt',  # Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2010
                    'f7xg',  # Investissement locatif dans le secteur touristique, travaux réalisés dans un village résidentiel de tourisme
                    'f7gu',  # Scellier: report de 1/9 de la réduction d'impôt des investissements achevés en 2012 avec promesse d'achat en 2009
                    'f7gv',  # Scellier: report de 1/5 de la réduction d'impôt des investissements réalisés et achevés en 2012 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres imputations et divers"""),
                ('children', [
                    'f8ta',  # Retenue à la source en France ou impôt payé à l'étranger
                    'f8tb',  # Crédit d'impôt recherche (entreprises bénéficiant de la restitution immédiate)
                    'f8tf',  # Reprises de réductions ou de crédits d'impôt
                    'f8tg',  # Crédits d'impôt en faveur des entreprises: Investissement en Corse
                    'f8th',  # Retenue à la source élus locaux
                    'f8tc',  # Crédit d'impôt autres entreprises (recherche non encore remboursé (années antérieures))
                    'f8td',  # Revenus non imposables dépassent la moitié du RFR
                    'f8te',  # Crédit d'impôt en faveur des entreprises: adhésion à un groupement de prévention agréé
                    'f8to',  # Crédit d'impôt en faveur des entreprises: investissement en Corse, report non imputé les années antérieures
                    'f8tp',  # Crédit d'impôt en faveur des entreprises: investissement en Corse, reprise de crédit d'impôt
                    'f8uz',  # Crédit d'impôt en faveur des entreprises: Famille
                    'f8tz',  # Crédit d'impôt en faveur des entreprises: Apprentissage
                    'f8wa',  # Crédit d'impôt en faveur des entreprises: Agriculture biologique
                    'f8wb',  # Crédit d'impôt en faveur des entreprises: Prospection commerciale
                    'f8wc',  # Crédit d'impôt en faveur des entreprises: Prêts sans intérêt
                    'f8wd',  # Crédit d'impôt en faveur des entreprises: Formation des chefs d'entreprise
                    'f8we',  # Crédit d'impôt en faveur des entreprises: Intéressement
                    'f8wr',  # Crédit d'impôt en faveur des entreprises: Métiers d'art
                    'f8ws',  # Crédit d'impôt en faveur des entreprises: Emploi de salariés réservistes
                    'f8wt',  # Crédit d'impôt en faveur des entreprises: Remplacement pour congé des agriculteurs
                    'f8wu',  # Crédit d'impôt en faveur des entreprises: Maître restaurateur
                    'f8wv',  # Crédit d'impôt en faveur des entreprises: Débitants de tabac
                    'f8wx',  # Crédit d'impôt en faveur des entreprises: Formation des salariés à l'économie d'entreprise
                    'f7uo',  # Acquisition de biens culturels
                    'f7us',  # Réduction d'impôt mécénat d'entreprise
                    'f7sb',  # Dépenses en faveur de la qualité environnementale des logements donnés en location: crédit à 25 %
                    'f7sd',  # Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à condensation
                    'f7se',  # Dépenses en faveur de la qualité environnementale de l'habitation principale, économie d'énergie: chaudières à micro-cogénération gaz
                    'f7sh',  # Dépenses en faveur de la qualité environnementale de l'habitation principale, isolation thermique: matériaux d'isolation des toitures (acquisition et pose)
                    'f7sc',  # Crédits d’impôt pour dépenses en faveur de la qualité environnementale
                    'f7up',  # Crédit d'impôt pour investissements forestiers: travaux
                    'f7uq',  # Crédit d'impôt pour investissements forestiers: contrat de gestion
                    'f1ar',  # Crédit d'impôt aide à la mobilité : le déclarant déménage à plus de 200 km pour son emploi
                    'f1br',  # Crédit d'impôt aide à la mobilité : le conjoint déménage à plus de 200 km pour son emploi
                    'f1cr',  # Crédit d'impôt aide à la mobilité : la 1ère personne à charge déménage à plus de 200 km pour son emploi
                    'f1dr',  # Crédit d'impôt aide à la mobilité : la 2è personne à charge déménage à plus de 200 km pour son emploi
                    'f1er',  # Crédit d'impôt aide à la mobilité : la 3è personne à charge déménage à plus de 200 km pour son emploi
                    'f2bg',  # Crédits d'impôt 'directive épargne' et autres crédits d'impôt restituables
                    'f4tq',  # Crédit d’impôt représentatif de la taxe additionnelle au droit de bail
                    'f7sf',  # Crédit de travaux en faveur d'aides aux personnes pour des logements en location (avant 2012 ) / Appareils de régulation du chauffage, matériaux de calorifugeage (après 2011)
                    'f7si',  # Matériaux d’isolation des planchers bas sur sous-sol, sur vide sanitaire ou sur passage couvert (acquisition et pose)
                    'f8uy',  # Auto-entrepreneur : versements libératoires d’impôt sur le revenu dont le remboursement est demandé
                    'mbic_mvct',  # Moins-values industrielles et commerciales nettes à court terme du foyer (régime micro entreprise)
                    'macc_mvct',  # Moins-values industrielles et commerciales non professionnelles nettes à court terme du foyer (régime micro entreprise)
                    'mncn_mvct',  # Moins-values non commerciales non professionnelles nettes à court terme du foyer (régime déclaratif spécial ou micro BNC)
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Impôt de solidarité sur la fortune"""),
                ('children', [
                    'b1ab',  # Valeur de la résidence principale avant abattement
                    'b1ac',  # Valeur des autres immeubles avant abattement
                    'b1bc',  # Immeubles non bâtis : bois, fôrets et parts de groupements forestiers
                    'b1be',  # Immeubles non bâtis : biens ruraux loués à long termes
                    'b1bh',  # Immeubles non bâtis : parts de groupements fonciers agricoles et de groupements agricoles fonciers
                    'b1bk',  # Immeubles non bâtis : autres biens
                    'b1cl',  # Parts et actions détenues par les salariés et mandataires sociaux
                    'b1cb',  # Parts et actions de sociétés avec engagement de conservation de 6 ans minimum
                    'b1cd',  # Droits sociaux de sociétés dans lesquelles vous exercez une fonction ou une activité
                    'b1ce',  # Autres valeurs mobilières
                    'b1cf',  # Liquidités
                    'b1cg',  # Autres biens meubles
                    'b1co',  # Autres biens meubles : contrats d'assurance-vie
                    'b2gh',  # Total du passif et autres déductions
                    'b2mt',  # Réductions pour investissements directs dans une société
                    'b2ne',  # Réductions pour investissements directs dans une société
                    'b2mv',  # Réductions pour investissements par sociétés interposées, holdings
                    'b2nf',  # Réductions pour investissements par sociétés interposées, holdings
                    'b2mx',  # Réductions pour investissements par le biais de FIP
                    'b2na',  # Réductions pour investissements par le biais de FCPI ou FCPR
                    'b2nc',  # Réductions pour dons à certains organismes d'intérêt général
                    'b4rs',  # Montant de l'impôt acquitté hors de France
                    'rev_or',
                    'rev_exo',
                    'tax_fonc',  # Taxe foncière
                    'restit_imp',
                    ]),
                ]),
            collections.OrderedDict([
                ('label', u"""Autres"""),
                ('children', [
                    u"""f6hk""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    u"""f6hl""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    u"""f6hm""",  # Dépenses de grosses réparations effectuées par les nus-propriétaires: report des dépenses des années antérieures
                    u"""rfr_n_1""",  # Revenu fiscal de référence année n - 1
                    u"""f7va""",  # Dons à des organismes d'aides aux personnes établis dans un Etat européen
                    u"""f7vc""",  # Dons à des autres organismes établis dans un Etat européen
                    u"""f7uh_2007""",  # Intérêts payés la première année de remboursement du prêt pour l'habitation principale
                    u"""f7vv""",  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2010 au 31/12/2010: annuités suivantes
                    u"""f7vu""",  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: première annuité
                    u"""f7vt""",  # Intérêt des emprunts contractés pour l'acquisition ou la construction de l'habitation principale: logements neufs non-BBC acquis ou construits du 01/01/2011 au 30/09/2011: annuités suivantes
                    u"""f7wa""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs avant le 03/04/2012
                    u"""f7wb""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique des murs à compter du 04/04/2012
                    u"""f7wc""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique sur plus de la moitié de la surface des murs extérieurs
                    u"""f7ve""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture avant le 04/04/2012
                    u"""f7vf""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de la toiture à compter du 04/04/2012
                    u"""f7vg""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: travaux d'isolation thermique de toute la toiture
                    u"""f7sg""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des murs (acquisitionn et pose)
                    u"""f7sj""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Matériaux d'isolation thermique des parois vitrées
                    u"""f7sk""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Volets isolants
                    u"""f7sl""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Portes d'entrées donnant sur l'extérieur
                    u"""f7sm""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de production d'électricité utilisant l'énergie radiative du soleil
                    u"""f7sn""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses remplaçant un appareil équivalent
                    u"""f7so""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Appareils de chauffage au bois ou autres biomasses ne remplaçant pas un appareil équivalent
                    u"""f7sp""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur autres que air/air et autres que géothermiques dont la finalité essentielle est la production de chaleur
                    u"""f7sq""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur géothermiques dont la finalité essentielle est la production de chaleur
                    u"""f7sr""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Pompes à chaleur (autres que air/air) dédiées à la production d'eau chaude sanitaire (chauffe-eaux thermodynamiques)
                    u"""f7ss""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de fourniture d'eau chaude sanitaire fonctionnant à l'énergie solaire et dotés de capteurs solaires
                    u"""f7st""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Autres équipements de production d'énergie utilisant une source d'énergie renouvelable (éolien, hydraulique)
                    u"""f7su""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de récupération et de traitement des eaux pluviales
                    u"""f7sv""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Diagnostic de performance énergétique
                    u"""f7sw""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: Équipements de raccordement à un réseau de chaleur
                    u"""f7ws""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolations des parois vitrées à compter du 04/04/2012
                    u"""f7wt""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: dépenses d'isolation thermique des parois vitrées réalisées sur au moins la moitié des fenêtres du logement
                    u"""f7wu""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets avant 2012
                    u"""f7wv""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de volets en 2012
                    u"""f7ww""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes avant 2012
                    u"""f7wx""",  # Dépenses en faveur de la qualité environnementale de l'habitation principale: achat de portes en 2012
                    u"""f7wr""",  # Dépenses en faveur de l'aide aux personnes réalisées dans des habitations données en location : travaux de prévention des risques technologiques
                    u"""f7qv""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010, nvestissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%
                    u"""f7qo""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 50%
                    u"""f7qp""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements immobliliers engagés avant le 1.1.2011 et investissements ayant reçu un agrément avant le 5.12.2010 à hauteur de 60%
                    u"""f7pa""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%
                    u"""f7pb""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%
                    u"""f7pc""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée
                    u"""f7pd""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011
                    u"""f7qe""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet avant 1.1.2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%
                    u"""f7pe""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%
                    u"""f7pf""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%
                    u"""f7pg""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt calculée
                    u"""f7ph""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011
                    u"""f7pi""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63%
                    u"""f7pj""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5%
                    u"""f7pk""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt calculée
                    u"""f7pl""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise, montant de la réduction d' impôt dont vous demandez l'imputation en 2011
                    u"""f7pm""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%
                    u"""f7pn""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %
                    u"""f7po""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %
                    u"""f7pp""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise
                    u"""f7pq""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée
                    u"""f7pr""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012
                    u"""f7ps""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50 %
                    u"""f7pt""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60 %
                    u"""f7pu""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise
                    u"""f7pv""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée
                    u"""f7pw""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012
                    u"""f7px""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt  à hauteur de 52,63 %
                    u"""f7py""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %
                    u"""f7rg""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise
                    u"""f7rh""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée
                    u"""f7ri""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2012, Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50%, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012
                    u"""f7rj""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %
                    u"""f7rk""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %
                    u"""f7rl""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %
                    u"""f7rm""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise
                    u"""f7rn""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée
                    u"""f7ro""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012
                    u"""f7rp""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %
                    u"""f7rq""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %
                    u"""f7rr""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise
                    u"""f7rs""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée
                    u"""f7rt""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2010 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012
                    u"""f7ru""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %
                    u"""f7rv""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %
                    u"""f7rw""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise
                    u"""f7rx""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée
                    u"""f7ry""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements ayant fait l'objet en 2011 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 %, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012
                    u"""f7nu""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 52,63 %
                    u"""f7nv""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 62,5 %
                    u"""f7nw""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise
                    u"""f7nx""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt calculée
                    u"""f7ny""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, investissements dans votre entreprise avec exploitation directe, montant de la réduction d'impôt dont vous demandez l'imputation en 2012
                    u"""f7mn""",  # Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet avant 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%
                    u"""f7lh""",  # Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%
                    u"""f7mb""",  # Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements ayant fait l'objet en 2009 d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un accompte d'au moins 50%, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%
                    u"""f7kt""",  # Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt, Investissements dans votre entreprise
                    u"""f7li""",  # Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 50%
                    u"""f7mc""",  # Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Autres investissements réalisés en 2010, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt à hauteur de 60%
                    u"""f7ku""",  # Investissements outre-mer dans le cadre de l'entreprise REPORT : Investissements réalisés en 2010, Investissements dans votre entreprise
                    u"""fhsa""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 52,63%
                    u"""fhsb""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2010 à hauteur de 62,5%
                    u"""fhsf""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 52,63%
                    u"""fhsg""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d'impôt en 2011 à hauteur de 62,5%
                    u"""fhsc""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2010
                    u"""fhsh""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise en 2011
                    u"""fhsd""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2010
                    u"""fhsi""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculée en 2011
                    u"""fhse""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010
                    u"""fhsj""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements réalisés en 2013, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011
                    u"""fhsk""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 52,63%
                    u"""fhsl""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2010 à hauteur de 62,5%
                    u"""fhsp""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 52,63%
                    u"""fhsq""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2010 ou 2011 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt en 2011 à hauteur de 62,5%
                    u"""fhsm""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2010
                    u"""fhsr""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise en 2011
                    u"""fhsn""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2010
                    u"""fhss""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe en 2011
                    u"""fhso""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2010
                    u"""fhst""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013, en 2011
                    u"""fhsu""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%
                    u"""fhsv""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%
                    u"""fhsw""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise
                    u"""fhsx""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé
                    u"""fhsy""",  # Investissements outre-mer dans le cadre de l'entreprise : Autres investissements, Investissements ayant fait l’objet en 2012 d’une demande d’agrément, d’une déclaration d’ouverture de chantier ou d’un acompte d’au moins 50 %, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013
                    u"""fhsz""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 52,63%
                    u"""fhta""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements donnés en location à une entreprise exploitante à laquelle vous rétrocédez la réduction d’impôt à hauteur de 62,5%
                    u"""fhtb""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise
                    u"""fhtc""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt calculé
                    u"""fhtd""",  # Investissements outre-mer dans le cadre de l'entreprise : Investissements autres que ceux des lignes précédentes, Investissements dans votre entreprise avec exploitation directe, montant de la réduction d’impôt dont vous demandez l’imputation en 2013
                    u"""f7rc""",  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    u"""f7rd""",  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    u"""f7re""",  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    u"""f7rf""",  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    u"""f7sx""",  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    u"""f7sy""",  # Travaux de restauration immobilière dans un secteur sauvegardé ou assimilé
                    u"""f7xa""",  # Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans un village résidentiel de tourisme
                    u"""f7xb""",  # Investissements locatifs dans le secteur de touristique: travaux engagés avant 2011 dans une résidence de tourisme classée ou meublée
                    u"""f7xp""",  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    u"""f7xq""",  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    u"""f7xr""",  # Investissements locatifs dans une résidence hôtelière à vocation sociale: report des dépenses d'investissement des années antérieures
                    u"""f7xv""",  # Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures
                    u"""f7xx""",  # Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans un village résidentiel de tourisme
                    u"""f7xz""",  # Investissements locatifs dans le secteur de touristique: travaux engagés après 2012 dans une résidence de tourisme classée ou un meublé tourisme
                    u"""f7uy""",  # Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures
                    u"""f7uz""",  # Investissements locatifs dans le secteur de touristique: Report des dépenses d'investissement des années antérieures
                    u"""f7cc""",  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1
                    u"""f7cq""",  # Souscriptions au capital des PME non cotées, report de versement de l'année de perception des revenus -1pour les start-up
                    u"""f7qk""",
                    u"""f7qn""",
                    u"""f7kg""",
                    u"""f7qu""",
                    u"""f7ki""",
                    u"""f7qj""",
                    u"""f7qw""",
                    u"""f7qx""",
                    u"""f7qf""",
                    u"""f7qg""",
                    u"""f7qh""",
                    u"""f7qi""",
                    u"""f7qq""",
                    u"""f7qr""",
                    u"""f7qs""",
                    u"""f7mm""",
                    u"""f7lg""",
                    u"""f7ma""",
                    u"""f7ks""",
                    u"""f7kh""",
                    u"""f7oa""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009
                    u"""f7ob""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009
                    u"""f7oc""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010
                    u"""f7oh""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% avant 2009
                    u"""f7oi""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2009
                    u"""f7oj""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2011, Investissements immobiliers engagés en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010
                    u"""f7ok""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2011, Autres investissements
                    u"""f7ol""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009
                    u"""f7om""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009
                    u"""f7on""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé avant le 1.1.2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010
                    u"""f7oo""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009
                    u"""f7op""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009
                    u"""f7oq""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010
                    u"""f7or""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2011, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011
                    u"""f7os""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % avant 2009
                    u"""f7ot""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2009
                    u"""f7ou""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010
                    u"""f7ov""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011
                    u"""f7ow""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2012,
                    u"""fhod""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés avant le 1.1.2011
                    u"""fhoe""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010
                    u"""fhof""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers  que vous avez engagé en 2012, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011
                    u"""fhog""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2010
                    u"""fhox""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2011
                    u"""fhoy""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2013, Investissements immobiliers engagés en 2012 ou 2013, ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50% en 2012
                    u"""fhoz""",  # Investissements outre-mer dans le logement : Investissements réalisés en 2013, Autres investissements
                    u"""fhra""",  # Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2010
                    u"""fhrb""",  # Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2011
                    u"""fhrc""",  # Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Investissements ayant fait l'objet d'une demande d'agrément, d'une déclaration d'ouverture de chantier ou d'un acompte d'au moins 50 % en 2012
                    u"""fhrd""",  # Investissements outre-mer dans le logement social : Investissements réalisés en 2013, Autres investissements
                    u"""f7kb""",  # Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)
                    u"""f7kc""",  # Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)
                    u"""f7kd""",  # Dépenses de protection du patrimoine naturel (excédent de réduction d’impôt d’années antérieures qui n’a pu être imputé)
                    u"""f7ul""",  # Investissements forestiers
                    u"""f7uu""",  # Investissements forestiers
                    u"""f7uv""",  # Investissements forestiers
                    u"""f7uw""",  # Investissements forestiers
                    u"""f7th""",  # Investissements forestiers
                    u"""f7ux""",  # Investissements forestiers
                    u"""f7tg""",  # Investissements forestiers
                    u"""f7tf""",  # Investissements forestiers
                    u"""f7ut""",  # Investissements forestiers
                    u"""f7lb""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2010
                    u"""f7lc""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2010
                    u"""f7ld""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report de l'année 2011
                    u"""f7le""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report de l'année 2011
                    u"""f7lf""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011
                    u"""f7ls""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010
                    u"""f7lm""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2009 ou 2010 ou réalisés et achevés en 2010 avec engagement avant le 1.1.2010
                    u"""f7lz""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Report du solde de réduction d'impôt de l'année 2012
                    u"""f7mg""",  # Investissements locatifs neufs dispositif Scellier: Report du solde des réductions d'impôts non encore imputé, Investissements réalisés et achevés en 2012 : report du solde de réduction d'impôt de l'année 2012
                    u"""f7na""",  # Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, métropole, BBC
                    u"""f7nb""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011,
                    u"""f7nc""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, BBC
                    u"""f7nd""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, BBC
                    u"""f7ne""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, BBC
                    u"""f7nf""",  # Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011,
                    u"""f7ng""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011,
                    u"""f7nh""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, métropole, non-BBC
                    u"""f7ni""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, métropole, non-BBC
                    u"""f7nj""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, métropole, non-BBC
                    u"""f7nk""",  # Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7nl""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7nm""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7nn""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7no""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7np""",  # Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7nq""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2010, réalisés en 2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7nr""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.1.2011 au 31.1.2011, Investissement réalisé du 1.1.2011 au 31.1.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7ns""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.2.2011 au 31.3.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7nt""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, Investissement réalisé du 1.4.2011 au 31.12.2011, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7hv""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole
                    u"""f7hw""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM
                    u"""f7hx""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 en métropole avec promesse d'achat avant le 1.1.2010
                    u"""f7hz""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2010 dans les DOM COM avec promesse d'achat avant le 1.1.2010
                    u"""f7ht""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, en métropole en 2009; dans les DOM du 1.1.2009 au 26.5.2009 ; dans les DOM du 27.5.2009 au 30.12.2009 lorsqu'ils ne respectent pas les plafonds spécifiques
                    u"""f7hu""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2009, Investissements réalisés en 2009 et achevés en 2010, dans les DOM COM du 27.5.2009 au 31.12.2009 respectant les plafonds spécifiques
                    u"""f7ha""",  # Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011
                    u"""f7hb""",  # Investissements locatifs neufs dispositif Scellier: Investissements achevés et réalisés en 2011, avec promesse d'achat en 2010
                    u"""f7hg""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna
                    u"""f7hh""",  # Investissements locatifs neufs dispositif Scellier: réductions investissements réalisés et achevés en 2011 en Polynésie française, Nouvelle Calédonie, dans les îles Walllis et Futuna avec promesse d'achat en 2010
                    u"""f7hd""",  # Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, réalisés en 2010, en métropole et dans les DOM-COM
                    u"""f7he""",  # Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, en métropole et dans les DOM-COM avec promesse d'achat avant le 1.1.2010
                    u"""f7hf""",  # Investissements locatifs neufs dispositif Scellier: Investissements achevés en 2011, Investissements réalisés en 2009 en métropole et dans les DOM-COM
                    u"""f7ja""",  # Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, BBC
                    u"""f7jb""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, BBC
                    u"""f7jd""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, BBC
                    u"""f7je""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, BBC
                    u"""f7jf""",  # Investissements locatifs neufs dispositif Scellier : investissements réalisés et engagés en 2012, métropole, non-BBC
                    u"""f7jg""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, métropole, non-BBC
                    u"""f7jh""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, métropole, non-BBC
                    u"""f7jj""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, métropole, non-BBC
                    u"""f7jk""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7jl""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7jm""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7jn""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, DOM, Saint-Barthélémy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7jo""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7jp""",  # Investissements locatifs neufs dispositif Scellier : investissements engagés en 2011, réalisés en 2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7jq""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.1.2012 au 31.3.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7jr""",  # Investissements locatifs neufs dispositif Scellier : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, Investissement réalisé du 1.4.2012 au 31.12.2012, Polynésie Française, Nouvelle Calédonie, Wallis et Futuna
                    u"""f7gj""",  # Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7gk""",  # Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés et réalisés en 2012, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2011
                    u"""f7gl""",  # Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7gp""",  # Investissements locatifs neufs dispositif Scellier : Reports concernant les investissements achevés ou acquis au cours des années antérieures, Investissements achevés en 2012 et réalisés en 2011, en métropole, dans les DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon, avec promesse d'achat en 2010s
                    u"""f7fa""",  # Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, BBC
                    u"""f7fb""",  # Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, métropole, non-BBC
                    u"""f7fc""",  # Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013, DOM, à Saint-Barthélemy, Saint-Martin, Saint-Pierre-et-Miquelon
                    u"""f7fd""",  # Investissements locatifs neufs dispositif Scellier : Investissements achevés ou acquis en 2013, réalisés du 1.1.2013 au 31.3.2013 en Polynésie, en Nouvelle Calédonie et à Wallis et Futuna
                    u"""f7in""",  # Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.1.2011 au 31.3.2011
                    u"""f7iv""",  # Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2010, investissement réalisé du 1.4.2011 au 31.12.2011
                    u"""f7iw""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2012
                    u"""f7io""",  # Investissements destinés à la location meublée non professionnelle :
                    u"""f7ip""",  # Investissements destinés à la location meublée non professionnelle :
                    u"""f7ir""",  # Investissements destinés à la location meublée non professionnelle :
                    u"""f7iq""",  # Investissements destinés à la location meublée non professionnelle :
                    u"""f7iu""",  # Investissements destinés à la location meublée non professionnelle :
                    u"""f7it""",  # Investissements destinés à la location meublée non professionnelle :
                    u"""f7ia""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011
                    u"""f7ib""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010
                    u"""f7ic""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2010 et achevés en 2011 avec promesse d'achat en 2009 ou réalisés en 2009
                    u"""f7id""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Engagement de réalisation de l'investissement en 2012
                    u"""f7ie""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Promesse d'achat en 2011
                    u"""f7if""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.1.2012 au 31.3.2012, investissement réalisé du 1.1.2012 au 31.3.2012
                    u"""f7ig""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, Investissements destinés à la location meublée non professionnelle : Logement acquis en l'état futur d'achèvement avec contrat de réservation enregistré au plus tard le 31.12.2011, investissement réalisé du 1.4.2012 au 31.12.2012
                    u"""f7ix""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2009; réalisés en 2009 et achevés en 2010; réalisés et achevés en 2010 avec engagement avant le 1.1.2010, Report du solde de réduction d'impôt de l'année 2011
                    u"""f7ih""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2011
                    u"""f7iz""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 : report du solde de réduction d'impôt de l'année 2011
                    u"""f7jt""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2013
                    u"""f7ju""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés en 2013, Engagement de réalisation de l'investissement en 2012
                    u"""f7jv""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2012
                    u"""f7jw""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 ou réalisés en 2012 avec promesse d'achat en 2011
                    u"""f7jx""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2012, réalisés en 2011 avec promesse d'achat en 2010 ou réalisés en 2010
                    u"""f7jc""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2010 ; réalisés en 2010 et achevés en 2011 ; réalisés et achevés en 2011 avec engagement en 2010, Report du solde de réduction d'impôt de l'année 2012
                    u"""f7ji""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d'impôt de l'année 2012
                    u"""f7js""",  # Investissements destinés à la location meublée non professionnelle : Investissements réalisés et achevés en 2011 ; réalisés en 2011 et achevés en 2011 ou 2012 ; réalisés en 2012 avec promesse d'achat en 2011 et achevés en 2012, Report du solde de réduction d’impôt de l’année 2012
                    u"""f7te""",  # Dépenses d'investissement forestier
                    u"""f7tu""",  # Dépenses de travaux dans l'habitation principale
                    u"""f7tt""",  # Dépenses de travaux dans l'habitation principale
                    u"""f7tv""",  # Dépenses de travaux dans l'habitation principale
                    u"""f7tx""",  # Dépenses de travaux dans l'habitation principale
                    u"""f7ty""",  # Dépenses de travaux dans l'habitation principale
                    u"""f7tw""",  # Dépenses de travaux dans l'habitation principale
                    u"""f7gh""",  # Investissements locatifs intermédiaires en métropole
                    u"""f7gi""",  # Investissements locatifs intermédiaires outre-mer
                    u"""f8tl""",  # Crédit d'impôt compétitivité emploi (CICE), entreprises bénéficiant de la restitution immédiate
                    u"""f8ts""",  # Crédit d'impôt en faveur des entreprises: investissement en Corse, crédit d'impôt
                    u"""f8uw""",  # Crédit d'impôt compétitivité emploi (CICE), autres entreprises
                    u"""f8wc__2008""",  # Crédit d'impôt en faveur des entreprises: Nouvelles technologies
                    u"""elig_creimp_exc_2008""",  # Éligibilité au crédit d'impôt exceptionnel sur les revenus 2008
                    u"""f8td_2002_2005""",  # Contribution exceptionnelle sur les hauts revenus
                    u"""f8ti""",  # Revenus de l'étranger exonérés d'impôt
                    u"""f8tk""",  # Revenus de l'étranger imposables
                    u"""f5qf""",  # Déficits des revenus agricoles des années antérieures non encore déduits (n-6)
                    u"""f5qg""",  # Déficits des revenus agricoles des années antérieures non encore déduits (n-5)
                    u"""f5qn""",  # Déficits des revenus agricoles des années antérieures non encore déduits (n-4)
                    u"""f5qo""",  # Déficits des revenus agricoles des années antérieures non encore déduits (n-3)
                    u"""f5qp""",  # Déficits des revenus agricoles des années antérieures non encore déduits (n-2)
                    u"""f5qq""",  # Déficits des revenus agricoles des années antérieures non encore déduits (n-1)
                    u"""f5ga""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-10)
                    u"""f5gb""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-9)
                    u"""f5gc""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-8)
                    u"""f5gd""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-7)
                    u"""f5ge""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-6)
                    u"""f5gf""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-5)
                    u"""f5gg""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-4)
                    u"""f5gh""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-3)
                    u"""f5gi""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-2)
                    u"""f5gj""",  # Déficits des revenus de locations meublées non professionnelles années antérieures non encore déduits (n-1)
                    u"""f5rn""",  # Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-6)
                    u"""f5ro""",  # Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-5)
                    u"""f5rp""",  # Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-4)
                    u"""f5rq""",  # Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-3)
                    u"""f5rr""",  # Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-2)
                    u"""f5rw""",  # Déficits des revenus industriels et commerciaux non professionnelles années antérieures non encore déduits (n-1)
                    u"""f5ht""",  # Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-6)
                    u"""f5it""",  # Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-5)
                    u"""f5jt""",  # Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-4)
                    u"""f5kt""",  # Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-3)
                    u"""f5lt""",  # Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-2)
                    u"""f5mt""",  # Déficits des revenus non commerciaux non professionnelles années antérieures non encore déduits (n-1)
                    u"""f2ck""",  # Crédit d'impôt égal au prélèvement forfaitaire déjà versé
                    u"""f2dm""",  # Impatriés: revenus de capitaux mobiliers perçus à l'étranger, abattement de 50 %
                    u"""f3vv_end_2010""",  # Pertes ouvrant droit au crédit d’impôt de 19 %
                    ]),
                ]),
            ]),
        ])),
    ('men', collections.OrderedDict([
        ('children', [
            collections.OrderedDict([
                ('label', u"""Principal"""),
                ('children', [
                    'loyer',  # Loyer
                    'statut_occupation_logement',  # Statut d'occupation
                    'depcom',  # Code INSEE (depcom) du lieu de résidence
                    ]),
                ]),
            ]),
        ])),
    ])
