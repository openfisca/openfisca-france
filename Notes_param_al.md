Aujourd'hui les aides au logement sont listées comme suit dans les paramètres:

```txt
aides_logement/
├── action_logement
├── allocations_logement
├── logement_social
├── reduction_loyer_solidarite
└── ressources
```

Si l'on se concentre sur l’aide personnalisée au logement (APL) et
l’allocation de logement (AL) qui se subdivise elle-même en une AL familiale (ALF)
et une AL sociale (ALS) qui sont regroupées sous le terme "allocations_logement".
Peut être serait-il plus judicieux des les renommer "aides personnelles au logement"
comme dans le [document du ministère chargé du logement](https://www.ecologie.gouv.fr/sites/default/files/les_aides_personnelles_au_logement_element_de_calcul_septembre_2021.pdf) ?

Le détail des sous-sections des "allocations_logement" est :

```txt
allocations_logement/
├── al_assistant_journaliste (abattements spécifiques aux assistants maternel et familial et aux journalistes)
├── al_charge (Majoration forfaitaire comptabilisée pour tous dans le calcul des aides au logement au titre des charges du logement)
├── al_etudiant (Montant considéré comme loyer pour les étudiants en RU)
├── al_loc1 (Plafonds de loyer (avant la réforme de 2001))
├── al_loc2 (Plafonds de loyer (après la réforme de 2001))
├── al_min (Montant minimum versé)
├── al_pac (Conditions d'une personne vivant au foyer pour être considérée à charge)
├── al_param (Paramètres de calcul pour les accédants et les étudiants logés en résidence universitaire)
├── al_param_accal (Pas de titre)
├── al_param_accapl (Paramètres de calcul de l'aide personalisée au logement (APL) pour les accédants à la propriété)
├── al_param_acc_univ (Paramètres de calcul pour les accédants et les étudiants logés en résidence universitaire, aides pour le logement (APL))
├── al_param_r0 (Paramètres de calcul du montant forfaitaire R0 (que l'on déduit des ressources) - secteur locatif (après 2001))
├── al_plaf_acc (Plafonds d'annuités de remboursement pour les accédants à la propriété des allocations logement (AL))
├── al_plaf_logement_foyer (Plafonds d'équivalence de loyer et de charges locatives pour les personnes résidant dans un logement-foyer)
├── autres (description: Autres dispositions communes)
```

Quelques remarques en vue de l'homogénéisation:

Côté openfisca
- `al_param` utilisé
- `al_param_accal` utilisé
- `al_param_accapl` utilisé
- `al_param_acc_univ` présent mais pas utilisé

Côté barèmes IPP manquent:
 - `al_param`
 - `al_param_accal`
 - `al_assistant_journaliste`
 - `autres`

`al_param` et `al_param_acc_univ` ont l'air similaires
`al_etudiant` et `al_plaf_logement_foyer` sont en partie similaires

Ordre [Barèmes IPP](https://www.ipp.eu/baremes-ipp/prestations-sociales/)
- `al_pac`
- `al_param_acc_univ`
- `al_param_r0`
- `al_param_accapl`
- `al_plaf_acc`
- `al_loc1`
- `al_loc2`
- `al_plaf_logement_foyer`
- `al_etudiant`
- `al_min`
- `al_rls` (ailleurs mais peut-être à réintégrer dans allocations logements)

Premières étapes:

- Fusionner `al_param` et `al_param_acc_univ`
- Fusionner `al_etudiant` et `al_plaf_logement_foyer`
- Rassembler loyers (`al_loc1` et `al_loc2`)
- Rassembler les abatements et renommer `al_assistant_journaliste`
- Retirer les préfixe `al`

Dans un second temps quand ce sera débrousaillé, réorganiser par secteur et (AL ou APL)
