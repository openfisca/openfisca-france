from openfisca_france.model.base import (
    calculate_output_divide,
    FoyerFiscal,
    max_,
    Variable,
    YEAR,
    )


class contribution_differentielle_hauts_revenus_ressources(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Ressources considérées par la contribution différentielle sur les hauts revenus'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200465/2025-02-16'
    definition_period = YEAR
    calculate_output = calculate_output_divide

    def formula_2025_01_01(foyer_fiscal, period, parameters):
        # Attention, c'est le PLF 2025 sur revenus 2025 à cause du vote définitif en 2025 !
        # Conformément au A du IV de l'article 10 de la loi n° 2025-127 du 14 février 2025, les I et II de l'article précité sont applicables à l'imposition des revenus de l'année 2025.

        # II. – Le revenu mentionné au I s’entend du revenu fiscal de référence défini au 1° du IV de l’article 1417,
        rfr = foyer_fiscal('rfr', period)

        # [leximpact : condition abattements, exonérations]
        # diminué du montant des abattements mentionnés au a bis du même 1°,
        # autres que ceux mentionnés aux 1 ter ou 1 quater de l’article 150-0 D,
        # des bénéfices exonérés mentionnés au b du même 1° du IV de l’article 1417,
        # et des plus-values mentionnées au I de l’article 150-0 B ter pour lesquelles le report d’imposition expire.

        # [leximpact : condition revenus exceptionnels]
        # Pour la détermination du revenu mentionné au présent II,
        # les revenus qui, par leur nature, ne sont pas susceptibles d’être recueillis annuellement
        # et dont le montant dépasse la moyenne des revenus nets d’après lesquels le contribuable
        # a été soumis à l’impôt sur le revenu au titre des trois dernières années,
        # sont retenus pour le quart de leur montant.

        # [leximpact : condition changement de situation familiale]
        # Pour l’appréciation de la condition relative au montant,
        # et en cas de modification de la situation de famille du contribuable
        # au cours de l’année d’imposition ou des deux années précédentes,
        # les règles prévues au 2 du II de l’article 223 sexies sont applicables en retenant,
        # pour chaque année, le revenu mentionné au présent II.

        return rfr


class contribution_differentielle_hauts_revenus_eligible(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Éligibilité à la contribution différentielle sur les hauts revenus'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200465/2025-02-16'
    definition_period = YEAR
    calculate_output = calculate_output_divide

    def formula_2025_01_01(foyer_fiscal, period, parameters):  # Sur revenus 2025
        # I. - Il est institué une contribution à la charge des contribuables
        # domiciliés fiscalement en France au sens de l’article 4 B (hypothèse = toujours vrai)
        # dont le revenu du foyer fiscal tel que défini au II
        contribution_differentielle_hauts_revenus_ressources = foyer_fiscal(
            'contribution_differentielle_hauts_revenus_ressources', period
            )
        # est supérieur à 250 000 € pour les contribuables célibataires, veufs, séparés ou divorcés
        # et à 500 000 € pour les contribuables soumis à imposition commune.
        cdhr_parameters = parameters(
            period
            ).impot_revenu.contributions_exceptionnelles.contribution_differentielle_hauts_revenus
        # info : montants de seuils égaux aux seuils du barème CEHR mais usage différent
        seuil_celibataire = cdhr_parameters.seuil_celibataire
        seuil_couple = cdhr_parameters.seuil_couple
        nb_adult = foyer_fiscal('nb_adult', period)

        revenu_celibataire_eligible = (nb_adult == 1) * (
            contribution_differentielle_hauts_revenus_ressources > seuil_celibataire
            )
        revenu_couple_eligible = (nb_adult == 2) * (
            contribution_differentielle_hauts_revenus_ressources > seuil_couple
            )

        return revenu_celibataire_eligible + revenu_couple_eligible


class contribution_differentielle_hauts_revenus_majoration(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Majoration de la contribution différentielle sur les hauts revenus'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200465/2025-02-16'
    definition_period = YEAR
    calculate_output = calculate_output_divide

    def formula_2025_01_01(foyer_fiscal, period, parameters):
        # [Majoration à ip_net + pfu + prelevement_forfaitaire_liberatoire + contribution_exceptionnelle_hauts_revenus]
        # III. - 2° (...)
        # majoré de 1 500 € par personne à charge au sens des articles
        majoration_impot_pac = parameters(
            period
            ).impot_revenu.contributions_exceptionnelles.contribution_differentielle_hauts_revenus.majoration_impot_pac
        nb_pac = foyer_fiscal('nb_pac', period)
        # 196 à 196 B et de 12 500 € pour les contribuables soumis à imposition commune.
        majoration_impot_couple = parameters(
            period
            ).impot_revenu.contributions_exceptionnelles.contribution_differentielle_hauts_revenus.majoration_impot_couple
        nb_adult = foyer_fiscal('nb_adult', period)
        return nb_pac * majoration_impot_pac + (nb_adult == 2) * majoration_impot_couple


class contribution_differentielle_hauts_revenus_majoration_impot(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Majoration de la contribution différentielle sur les hauts revenus'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200465/2025-02-16'
    definition_period = YEAR
    calculate_output = calculate_output_divide

    def formula_2025_01_01(foyer_fiscal, period, parameters):
        # [Ajout à ip_net + pfu + prelevement_forfaitaire_liberatoire + contribution_exceptionnelle_hauts_revenus]
        # IV A 2 et VII ; les cases qui ne sont pas dans openfisca ne sont pas ajoutées, et certaines n'ont pas été encore reliées
        f8wt = foyer_fiscal('f8wt', period)
        f8tb = foyer_fiscal('f8tb', period)
        f8tl = foyer_fiscal('f8tl', period)
        f8tp = foyer_fiscal('f8tp', period)
        f8uz = foyer_fiscal('f8uz', period)
        f8wa = foyer_fiscal('f8wa', period)
        f8wd = foyer_fiscal('f8wd', period)
        f8wr = foyer_fiscal('f8wr', period)
        f8wc = foyer_fiscal('f8wc', period)
        f8te = foyer_fiscal('f8te', period)
        interets_emprunt_reprise_societe = foyer_fiscal('interets_emprunt_reprise_societe', period)
        f7ik = foyer_fiscal('f7ik', period)
        f7il = foyer_fiscal('f7il', period)
        f7gq = foyer_fiscal('f7gq', period)
        f7gr = foyer_fiscal('f7gr', period)
        f7fq = foyer_fiscal('f7fq', period)
        f7ft = foyer_fiscal('f7ft', period)
        f7fm = foyer_fiscal('f7fm', period)
        f7fl = foyer_fiscal('f7fl', period)
        f7fy = foyer_fiscal('f7fy', period)
        reduction_d_impot_majorantes = (f8wt + f8tb + f8tl + f8tp + f8uz
            + f8wa + f8wd + f8wr + f8wc + f8te + interets_emprunt_reprise_societe
            + f7ik + f7il + f7gq + f7gr + f7fq + f7ft + f7fm + f7fl + f7fy)
        return reduction_d_impot_majorantes


class contribution_differentielle_hauts_revenus_decote(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Décote de la contribution différentielle sur les hauts revenus'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200465/2025-02-16'
    definition_period = YEAR
    calculate_output = calculate_output_divide
    documentation = '''
    Selon 'Évaluations préalables des articles du projet de loi' :
    Pour atténuer l’effet de seuil lié à l’entrée dans le champ de cette nouvelle contribution, un mécanisme de décote
    est prévu. Ce mécanisme, qui vise à éviter les ressauts d’imposition potentiellement excessifs, bénéficiera aux
    contribuables célibataires, veufs, séparés ou divorcés dont le RFR est compris entre 250 000 € et 330 000 € et aux
    contribuables soumis à imposition commune dont le RFR est compris entre 500 000 € et 660 000 €.
    '''

    def formula_2025_01_01(foyer_fiscal, period, parameters):  # Sur revenus 2025
        # (12) « V. – Toutefois, lorsque le revenu mentionné au II est inférieur ou égal à 330 000 € pour les contribuables célibataires,
        # veufs, séparés ou divorcés et à 660 000 € pour les contribuables soumis à imposition commune,
        contribution_differentielle_hauts_revenus_ressources = foyer_fiscal(
            'contribution_differentielle_hauts_revenus_ressources', period
            )
        cdhr_parameters = parameters(
            period
            ).impot_revenu.contributions_exceptionnelles.contribution_differentielle_hauts_revenus

        nb_adult = foyer_fiscal('nb_adult', period)
        celibataire = nb_adult == 1
        couple = nb_adult == 2

        condition_revenus_celibataire = celibataire * (
            contribution_differentielle_hauts_revenus_ressources
            <= cdhr_parameters.plafond_revenus_decote_celibataire
            )
        condition_revenus_couple = couple * (
            contribution_differentielle_hauts_revenus_ressources
            <= cdhr_parameters.plafond_revenus_decote_couple
            )

        # le montant résultant de l’application du 1° du III est diminué de la différence, [différence calculée dans contribution_differentielle_hauts_revenus]
        # lorsqu’elle est positive, entre ce montant (impot_cible)
        # et 82,5 % de la différence entre ce revenu et 250 000 € pour les contribuables célibataires,
        # veufs, séparés ou divorcés ou 500 000 € pour les contribuables soumis à imposition commune.
        taux = cdhr_parameters.taux_cdhr
        contribution_differentielle_hauts_revenus_ressources = foyer_fiscal(
            'contribution_differentielle_hauts_revenus_ressources', period
            )
        impot_cible = (
            contribution_differentielle_hauts_revenus_ressources * taux
            )  # = cdhr théorique cible

        decote_celibataire = max_(
            0,
            impot_cible
            - (  # 'ce montant'
                cdhr_parameters.taux_decote
                * (
                    celibataire
                    * (
                        contribution_differentielle_hauts_revenus_ressources
                        - cdhr_parameters.seuil_celibataire
                        )
                    )
                ),
            )

        decote_couple = max_(
            0,
            impot_cible
            - (
                cdhr_parameters.taux_decote
                * (
                    couple
                    * (
                        contribution_differentielle_hauts_revenus_ressources
                        - cdhr_parameters.seuil_couple
                        )
                    )
                ),
            )

        # ajout de l'éligibilité (non répétée dans le texte de loi) pour mettre la décote à zéro si non éligible
        contribution_differentielle_hauts_revenus_eligible = foyer_fiscal(
            'contribution_differentielle_hauts_revenus_eligible', period
            )
        return contribution_differentielle_hauts_revenus_eligible * (
            (condition_revenus_celibataire * decote_celibataire)
            + (condition_revenus_couple * decote_couple)
            )


class contribution_differentielle_hauts_revenus(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Contribution différentielle sur les hauts revenus (CDHR)'
    reference = 'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200465/2025-02-16'
    definition_period = YEAR
    calculate_output = calculate_output_divide

    def formula_2025_01_01(foyer_fiscal, period, parameters):  # Sur revenus 2025
        contribution_differentielle_hauts_revenus_eligible = foyer_fiscal(
            'contribution_differentielle_hauts_revenus_eligible', period
            )

        # III. – La contribution mentionnée au I est égale à la différence, lorsqu’elle est positive, entre :
        # (8) « 1° le montant résultant de l’application d’un taux de 20 % au revenu défini au II ;
        taux = parameters(
            period
            ).impot_revenu.contributions_exceptionnelles.contribution_differentielle_hauts_revenus.taux_cdhr
        contribution_differentielle_hauts_revenus_ressources = foyer_fiscal(
            'contribution_differentielle_hauts_revenus_ressources', period
            )

        # [on soustrait la décote définie en V]
        contribution_differentielle_hauts_revenus_decote = foyer_fiscal(
            'contribution_differentielle_hauts_revenus_decote', period
            )
        impot_cible_apres_decote = (
            contribution_differentielle_hauts_revenus_ressources * taux
            ) - contribution_differentielle_hauts_revenus_decote

        # (9) « 2° et le montant résultant de la somme de l’impôt sur le revenu et de la contribution prévue à l’article
        # 223 sexies tels que définis au IV,
        # ainsi que des prélèvements libératoires de l’impôt sur le revenu
        # mentionnés au c du 1° du IV de l’article 1417,
        irpp_economique = foyer_fiscal('irpp_economique', period)

        impot_avant_creation_cdhr = (
            - irpp_economique
            + foyer_fiscal(
                'contribution_differentielle_hauts_revenus_majoration', period
                )
            + foyer_fiscal(
                'contribution_differentielle_hauts_revenus_majoration_impot', period
                )
            )
        contribution_differentielle_hauts_revenus_montant = max_(
            impot_cible_apres_decote - impot_avant_creation_cdhr, 0
            )

        # IV. – L’impôt sur le revenu mentionné au 2° du III est majoré de l’avantage en impôt procuré par [les
        # réductions d’impôt prévues à l’article 199 quater B], à l’article 199 undecies B, à l’exception des vingt-sixième à dernier alinéas du I, à l’article 238 bis
        # et à l’article 107 de la loi n° 2021-1104 du 22 août 2021 portant lutte contre le dérèglement climatique et renforcement de la résilience face à ses effets,
        # ainsi que de l’avantage en impôt procuré par les crédits d’impôt prévus à [l’article 200 undecies], [aux articles 244 quater B à 244 quater W](244 B bis et 244 W)
        # et [aux articles 27 et 151 de la loi n° 2020-1721 du 29 décembre 2020 de finances pour 2021] et par les crédits d’impôt prévus par les conventions fiscales internationales, dans la limite de l’impôt dû (8fv, mais pas seul).
        # (11) « La contribution mentionnée au 2° du III est déterminée sans qu’il soit fait application du 1 du II de l’article 223 sexies.
        #
        # [leximpact : V = décote ajoutée plus haut]
        # (12) « V. – Toutefois, lorsque le revenu mentionné au II est inférieur ou égal à 330 000 € pour les contribuables célibataires,
        # veufs, séparés ou divorcés et à 660 000 € pour les contribuables soumis à imposition commune,
        # le montant résultant de l’application du 1° du III est diminué de la différence, lorsqu’elle est positive,
        # entre ce montant et 82,5 % de la différence entre ce revenu et 250 000 € pour les contribuables célibataires,
        # veufs, séparés ou divorcés ou 500 000 € pour les contribuables soumis à imposition commune.
        #
        # (13) « VI. – La contribution est déclarée, contrôlée et recouvrée selon les mêmes règles
        # et sous les mêmes garanties et sanctions qu’en matière d’impôt sur le revenu. »
        # II.- Le montant de l’impôt sur le revenu mentionné au 2° du III de l’article 224 du code général des impôts
        # est également majoré de l’avantage en impôt procuré par les réductions d’impôt et, dans la limite de l’impôt dû, des crédits d’impôt prévus par :
        # (15) 1° les articles 199 decies E, 199 decies EA, 199 decies F, 199 decies G, 199 decies I, [199 terdecies-0 B], [199 sexvicies] et 199 septvicies du même code ;
        # (16) 2° [les articles 199 terdecies-0 A], 199 terdecies-0 A bis, 199 terdecies-0 A ter, 199 terdecies-0 AA,
        # 199 terdecies-0 AB et [(199 terdecies-0 C)] du même code, à raison des versements effectués au titre de souscriptions réalisées jusqu’au 31 décembre 2024 ;
        # (17) 3° les articles 199 undecies A, les vingt-sixième à dernier alinéas du I de l’article 199 undecies B,
        # les articles 199 undecies C et 199 novovicies du même code, à raison des investissements réalisés jusqu’au 31 décembre 2024 ;
        # (18) 4° les articles 199 duovicies, 200 quater A et 200 quater C du même code, à raison des dépenses payées jusqu’au 31 décembre 2024 ;
        # (19) 5° l’article 199 tervicies du même code, à raison des dépenses payées et des souscriptions réalisées jusqu’au 31 décembre 2024 ;
        # (20) 6° l’article 199 tricies du même code, à raison des logements donnés en location dans le cadre d’une des conventions mentionnées
        # aux articles L. 321-4 ou L. 321-8 du code de la construction et de l’habitation dont la date d’enregistrement
        # de la demande de conventionnement par l’Agence nationale de l’habitat est intervenue au plus tard le 31 décembre 2024 ;
        # (21) 7° l’article 200 quindecies du même code à raison des opérations forestières réalisées jusqu’au 31 décembre 2024.
        # (22) III.- A. – Les I et II sont applicables à compter de l’imposition des revenus de l’année 2024 et jusqu’à l’imposition des revenus de l’année 2026.
        # (23) B. – Pour l’imposition des revenus de l’année 2024, les revenus soumis aux prélèvements libératoires mentionnés
        # au c du 1° du IV de l’article 1417 du code général des impôts ne sont pas pris en compte pour la détermination
        # du revenu défini au II de l’article 224 du même code et ces prélèvements libératoires ne sont pas retenus
        # pour déterminer le montant défini au 2° du III de l’article 224 du même code.

        return (
            contribution_differentielle_hauts_revenus_eligible
            * contribution_differentielle_hauts_revenus_montant
            )
