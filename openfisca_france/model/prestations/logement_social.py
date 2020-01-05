from numpy import char, isin, logical_not as not_, select

from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_france.entities import Famille, Menage

paris_communes_limitrophes = [
    b'75056',  # Paris
    b'93001',  # Bagnolet
    b'93006',  # Boulogne-Billancourt
    b'94018',  # Charenton-le-Pont
    b'92024',  # Clichy-la-Garenne
    b'94033',  # Fontenay-sous-Bois
    b'94037',  # Gentilly
    b'92040',  # Issy-les-Moulineaux
    b'94041',  # Ivry-sur-Seine
    b'94042',  # Joinville-le-Pont
    b'94043',  # Le Kremlin-Bicêtre
    b'93045',  # Les Lilas
    b'93061',  # Le Pré-Saint-Gervais
    b'92044',  # Levallois-Perret
    b'92046',  # Malakoff
    b'93048',  # Montreuil
    b'92049',  # Montrouge
    b'92051',  # Neuilly-sur-Seine
    b'94052',  # Nogent-sur-Marne
    b'93055',  # Pantin
    b'92062',  # Puteaux
    b'92064',  # Saint-Cloud
    b'93066',  # Saint-Denis
    b'94067',  # Saint-Mandé
    b'94069',  # Saint-Maurice
    b'93070',  # Saint-Ouen
    b'92073',  # Suresnes
    b'92075',  # Vanves
    b'94080',  # Vincennes
    ]

departements_idf = [
    b'75',
    b'77',
    b'78',
    b'91',
    b'92',
    b'93',
    b'94',
    b'95',
    ]


class ZoneLogementSocial(Enum):
    __order__ = 'paris_communes_limitrophes ile_de_france autres_regions'
    paris_communes_limitrophes = "Paris et communes limitrophes"
    ile_de_france = "Île-de-France hors Paris et communes limitrophes"
    autres_regions = "Autres régions"


class zone_logement_social(Variable):
    value_type = Enum
    possible_values = ZoneLogementSocial
    default_value = ZoneLogementSocial.autres_regions
    entity = Menage
    definition_period = MONTH
    label = "Zone logement social"

    def formula(menage, period):
        depcom = menage('depcom', period)
        in_paris_communes_limitrophes = isin(depcom, paris_communes_limitrophes)
        in_idf = isin(char.ljust(depcom, 2), departements_idf)

        return select(
            [
                in_paris_communes_limitrophes,
                in_idf
                ],
            [
                ZoneLogementSocial.paris_communes_limitrophes,
                ZoneLogementSocial.ile_de_france,
                ],
            default = ZoneLogementSocial.autres_regions
            )


class CategorieMenageLogementSocial(Enum):
    __order__ = 'categorie_1 categorie_2 categorie_3 categorie_4 categorie_5 categorie_6'
    categorie_1 = "Une personne seule"
    categorie_2 = "Deux personnes ne comportant aucune pers. à charge à l'exclusion des jeunes ménages"
    categorie_3 = "Trois personnes ou une pers. seule avec une pers. à charge ou jeune ménage sans personne à charge"
    categorie_4 = "Quatre personnes ou une pers. seule avec deux pers. à charge"
    categorie_5 = "Cinq personnes ou une pers. seule avec trois pers. à charge"
    categorie_6 = "Six personnes ou une pers. seule avec quatre pers. à charge"


class logement_social_categorie_menage(Variable):
    entity = Famille
    value_type = Enum
    possible_values = CategorieMenageLogementSocial
    default_value = CategorieMenageLogementSocial.categorie_1
    definition_period = MONTH
    label = "Catégorie de ménage pour déterminer le plafond de ressources"
    reference = [
        "Arrêté du 29 juillet 1987 relatif aux plafonds de ressources des bénéficiaires de la législation sur les habitations à loyer modéré et des nouvelles aides de l'Etat en secteur locatif",
        "https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000000294318"
        ]

    def formula(famille, period, parameters):

        nb_personnes = famille.nb_persons()
        personnes_a_charge = famille('al_nb_personnes_a_charge', period)
        personne_seule = (famille.nb_persons(Famille.PARENT) == 1) * (personnes_a_charge == 0)

        # Jeune ménage : Couple marié, concubins ou pacsés, sans personne à charge,
        # dont la somme des âges des deux conjoints est inférieure ou égale à 55 ans
        age = famille.members('age', period)
        sum_age = famille.sum(age, role = Famille.PARENT)
        jeune_menage = (not_(personne_seule) * (sum_age <= 55))

        return select(
            [
                personne_seule,
                # Deux personnes ne comportant aucune personne à charge, à l'exclusion des jeunes ménages.
                ((nb_personnes == 2) * (personnes_a_charge == 0) * not_(jeune_menage)),
                # Trois personnes, ou une personne seule avec une personne à charge, ou jeune ménage sans personne à charge.
                (personnes_a_charge == 1) + (jeune_menage * (personnes_a_charge == 0)),
                # Quatre personnes, ou une personne seule avec deux personnes à charge.
                (personnes_a_charge == 2),
                # Cinq personnes, ou une personne seule avec trois personnes à charge.
                (personnes_a_charge == 3)
                ],
            [
                CategorieMenageLogementSocial.categorie_1,
                CategorieMenageLogementSocial.categorie_2,
                CategorieMenageLogementSocial.categorie_3,
                CategorieMenageLogementSocial.categorie_4,
                CategorieMenageLogementSocial.categorie_5
                ],
            default = CategorieMenageLogementSocial.categorie_6
            )


class logement_social_plafond_ressources(Variable):
    entity = Famille
    value_type = float
    definition_period = MONTH
    label = "Plafonds de ressources des bénéficiaires de la législation sur les habitations à loyer modéré et des nouvelles aides de l'Etat en secteur locatif"
    reference = [
        "Arrêté du 22 décembre 2016 modifiant l'arrêté du 29 juillet 1987 relatif aux plafonds de ressources des bénéficiaires de la législation sur les habitations à loyer modéré et des nouvelles aides de l'Etat en secteur locatif ",
        "https://www.legifrance.gouv.fr/eli/arrete/2016/12/22/LHAL1629455A/jo/texte",
        ]

    def formula(famille, period, parameters):
        logement_social = parameters(period).logement_social.plai

        categorie_menage = famille('logement_social_categorie_menage', period)
        zone_logement_social = famille.demandeur.menage('zone_logement_social', period)
        personnes_a_charge = famille('al_nb_personnes_a_charge', period)

        # On détermine le nombre de personnes à charge supplémentaires au-dessus de 4
        personnes_a_charge_supplementaires = (personnes_a_charge > 4) * (personnes_a_charge - 4)

        plafond_ressources_par_categorie = logement_social.plafond_ressources.par_categorie_de_menage[categorie_menage]
        par_personne_supplementaire = logement_social.plafond_ressources.par_personne_supplementaire[zone_logement_social]

        return plafond_ressources_par_categorie[zone_logement_social] + (personnes_a_charge_supplementaires * par_personne_supplementaire)


class logement_social_eligible(Variable):
    entity = Famille
    value_type = bool
    definition_period = MONTH
    label = "Logement social - Éligibilité"

    def formula_2017(famille, period, parameters):

        logement_social_plafond_ressources = famille('logement_social_plafond_ressources', period)
        revenu_fiscal_de_reference = famille.demandeur.foyer_fiscal('rfr', period.n_2)

        return revenu_fiscal_de_reference <= logement_social_plafond_ressources
