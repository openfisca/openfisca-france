
Openfisca variables naming guidelines
===========================

General philosophy
------------------

Openfisca variables names should, as much as possible, be understandable by an external contributor who is **curious** about the French tax and benefits systems, **without necessarly being an expert**.

One should be able to get a rough idea of the meaning of a variable by reading its name, or by quickly researching it on Google.

A particular effort should be made on variables highly likely to be reused somewhere else in the code.

Examples:

> **Good naming**

> `als_etudiant`: I don't know what `als` stands for. I look it up on Google, and I see ALS are a form of Aides Logement. I thus know this variable should be the amount of ALS for a student. This is enough to tell me if it is interesting in my context.

----------

> **Bad naming**

>`apje_temp`: I could find the meaning of APJE online, but the temp suffix remains a mystery.

>`rto_net`. I can guess it's an amout after some kind of deduction, but looking RTO on Google doesn't give me anything.


Do's and don'ts
---------------

### Acronyms

Acronyms are ok as long as they are broadly accepted and their meaning is quickly findable online.
>**OK**: RSA, RFR

>**KO**: PAC

### Abbreviations

Abbreviations should be avoided unless they are undoubtedly transparent.
>**OK**: nb_parents

>**KO**: nb_par, isol


### Scopes and prefixes

To show a variable belongs to a specific scope, it is better to use a prefix rather than a suffix.
>**OK**: rsa_nb_enfants

>**KO**: nb_enfants_rsa

Not specifying the scope of a specific variable should be avoided, as it is confusing for other users.
>**OK**: ir_nb_pac

>**KO**: nb_pac

### Entity suffixes

It happens that several variables have the same meaning, but for different entitities (individus, familles, etc.). Standard suffixes should be used to distinguish them.
>**OK**: ass_base_ressources_i, statut_occupation_logement_famille


Legacy
------
Many variables on the current codebase of Openfisca France do not respect the guidelines presented here. An exhautsive and global renaming is not considered as of today.

However, new variables should be compliant with these guidelines, and legacy ones should progressively and opportunistically be renamed.
