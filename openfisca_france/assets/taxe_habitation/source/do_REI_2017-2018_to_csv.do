/***************************************************************************************/
/*** Mise en forme des fichiers REI 2017 à 2022 pour OpenFisca
     Nécessite Stata version 14                        *********************************/
/***************************************************************************************/

clear
set more off
cap log close

**** Chemin des REI en local. Les fichiers REI en .xlsx sont accessibles en ligne sur https://www.data.gouv.fr/fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-3/
global input_2017 = ""
global input_2018 = ""
global input_2019 = ""
global input_2020 = ""
global input_2021 = ""
global input_2022 = ""

**** Chemin d'export du fichier csv
global export_2017 = ""
global export_2018 = ""
global export_2019 = ""
global export_2020 = ""
global export_2021 = ""
global export_2022 = ""

*2017-2018
forval i=2017/2018 {
	set excelxlsxlargefile on
	import excel using "${input_`i'}.xlsx", firstrow clear
	keep DEP COM SIREPCI Q03 LIBCOM H12 H32 J21 J23 J31* J33* J41* J43* J51* J53* J61* J63*
	compress

	foreach var of varlist H* J* {
		replace `var' = 0 if `var'==.
	}
	gen code_insee_commune = trim(DEP) + trim(COM)

	gen taux_com   = H12/100
	gen taux_epci  = H32/100

	gen valeur_locative_moyenne_com  = J21
	gen valeur_locative_moyenne_epci = J23

	* Pour certaines intercom, il n'y a pas de quotité ajustée mais seulement une quotité simple. Surement due aux interco créées après 2010 (qui est l'année du transfert de la TH départementale justifiant cet ajustement). Donc, si la valeur ajustée est nulle, on prend la quotité simple
	gen abt_general_base_com       = cond(J51A~=0,J51A,J51)
	gen abt_general_base_epci      = cond(J53A~=0,J53A,J53)
	gen abt_pac_1_2_com            = cond(J31A~=0,J31A,J31)
	gen abt_pac_1_2_epci           = cond(J33A~=0,J33A,J33)
	gen abt_pac_3pl_com            = cond(J41A~=0,J41A,J41)
	gen abt_pac_3pl_epci           = cond(J43A~=0,J43A,J43)
	gen abt_condition_modeste_com  = cond(J61A~=0,J61A,J61)
	gen abt_condition_modeste_epci = cond(J63A~=0,J63A,J63)

	keep code_insee_commune taux_* valeur_locative_moyenne_* abt_*
	foreach var of varlist  taux_* valeur_locative_moyenne_* abt_* {
		replace `var' = 0 if `var'==.
	}

	sort     code_insee_commune
	outsheet code_insee_commune taux_* valeur_locative_moyenne_* abt_* using "${export_`i'}.csv", comma replace
}
*2019-2020
forval i=2019/2020 {
	set excelxlsxlargefile on
	import excel using "${input_`i'}.xlsx", firstrow clear
	keep DEPARTEMENT COMMUNE NUMEROSIRENDELEPCI THCOMMUNETAUXNET THINTERCOMMUNALITETAUXAPP THVLMOYENNEUTILISEEPOUR IJ  THQUOTITEDESABATTEMENTSAVA THQUOTITEDESABATTEMENTSAJ IL THQUOTITEDESABATTEMENTSAJU IO IP IQ IR IS IT IU IV IW IX IY IZ
	
	compress

	foreach var of varlist THCOMMUNETAUXNET THINTERCOMMUNALITETAUXAPP THQUOTITEDESABATTEMENTSAVA THQUOTITEDESABATTEMENTSAJ IL THQUOTITEDESABATTEMENTSAJU IO IP IQ IR IS IT IU IV IW IX IY IZ {
		replace `var' = 0 if `var'==.
	}
	gen code_insee_commune = trim(DEPARTEMENT) + trim(COMMUNE)

	gen taux_com   = THCOMMUNETAUXNET/100
	gen taux_epci  = THINTERCOMMUNALITETAUXAPP/100

	
	gen valeur_locative_moyenne_com  = THVLMOYENNEUTILISEEPOUR
	gen valeur_locative_moyenne_epci = IJ
	
	
	* Pour certaines intercom, il n'y a pas de quotité ajustée mais seulement une quotité simple. Surement due aux interco créées après 2010 (qui est l'année du transfert de la TH départementale justifiant cet ajustement). Donc, si la valeur ajustée est nulle, on prend la quotité simple
	gen abt_general_base_com       = cond(IU~=0,IU,IS)
	gen abt_general_base_epci      = cond(IV~=0,IV,IT)
	gen abt_pac_1_2_com            = cond(THQUOTITEDESABATTEMENTSAJ~=0,THQUOTITEDESABATTEMENTSAJ,THQUOTITEDESABATTEMENTSAVA)
	gen abt_pac_1_2_epci           = cond(THQUOTITEDESABATTEMENTSAJU~=0,THQUOTITEDESABATTEMENTSAJU,IL)
	gen abt_pac_3pl_com            = cond(IQ~=0,IQ,IO)
	gen abt_pac_3pl_epci           = cond(IR~=0,IR,IP)
	gen abt_condition_modeste_com  = cond(IY~=0,IY,IW)
	gen abt_condition_modeste_epci = cond(IZ~=0,IZ,IX)

	keep code_insee_commune taux_* valeur_locative_moyenne_* abt_*
	foreach var of varlist  taux_* valeur_locative_moyenne_* abt_* {
		replace `var' = 0 if `var'==.
	}

	sort     code_insee_commune
	outsheet code_insee_commune taux_* valeur_locative_moyenne_* abt_* using "${export_`i'}.csv", comma replace
}

*2021
set excelxlsxlargefile on
import excel using "${input_2021}.xlsx", firstrow clear
keep DEPARTEMENT COMMUNE NUMEROSIRENDELEPCI THCOMMUNETAUXNET THINTERCOMMUNALITETAUXAPP THVLMOYENNEUTILISEEPOUR HV  THQUOTITEDESABATTEMENTSAVA THQUOTITEDESABATTEMENTSAJ IL THQUOTITEDESABATTEMENTSAJU IB IC ID IE IF IG IH II IJ IK IL IM

compress

foreach var of varlist THCOMMUNETAUXNET THINTERCOMMUNALITETAUXAPP THVLMOYENNEUTILISEEPOUR HV THQUOTITEDESABATTEMENTSAVA THQUOTITEDESABATTEMENTSAJ IL THQUOTITEDESABATTEMENTSAJU IB IC ID IE IF IG IH II IJ IK IL IM {
	replace `var' = 0 if `var'==.
}
gen code_insee_commune = trim(DEPARTEMENT) + trim(COMMUNE)

gen taux_com   = THCOMMUNETAUXNET/100
gen taux_epci  = THINTERCOMMUNALITETAUXAPP/100


gen valeur_locative_moyenne_com  = THVLMOYENNEUTILISEEPOUR
gen valeur_locative_moyenne_epci = HV

* Pour certaines intercom, il n'y a pas de quotité ajustée mais seulement une quotité simple. Surement due aux interco créées après 2010 (qui est l'année du transfert de la TH départementale justifiant cet ajustement). Donc, si la valeur ajustée est nulle, on prend la quotité simple
gen abt_general_base_com       = cond(IH~=0,IH,IF)
gen abt_general_base_epci      = cond(II~=0,II,IG)
gen abt_pac_1_2_com            = cond(THQUOTITEDESABATTEMENTSAJ~=0,THQUOTITEDESABATTEMENTSAJ,THQUOTITEDESABATTEMENTSAVA)
gen abt_pac_1_2_epci           = cond(THQUOTITEDESABATTEMENTSAJU~=0,THQUOTITEDESABATTEMENTSAJU,IL)
gen abt_pac_3pl_com            = cond(ID~=0,ID,IB)
gen abt_pac_3pl_epci           = cond(IE~=0,IE,IC)
gen abt_condition_modeste_com  = cond(IL~=0,IL,IJ)
gen abt_condition_modeste_epci = cond(IM~=0,IM,IK)

keep code_insee_commune taux_* valeur_locative_moyenne_* abt_*
foreach var of varlist  taux_* valeur_locative_moyenne_* abt_* {
	replace `var' = 0 if `var'==.
}

sort     code_insee_commune
outsheet code_insee_commune taux_* valeur_locative_moyenne_* abt_* using "${export_2021}.csv", comma replace


*2022
set excelxlsxlargefile on
import excel using "${input_2022}.xlsx", firstrow clear
keep DEPARTEMENT COMMUNE NUMEROSIRENDELEPCI THCOMMUNETAUXNET THINTERCOMMUNALITETAUXAPP THVLMOYENNEUTILISEEPOUR IG  THQUOTITEDESABATTEMENTSAVA THQUOTITEDESABATTEMENTSAJ II THQUOTITEDESABATTEMENTSAJU IL IM IN IO IP IQ IR IS IT IU IV IW

compress

foreach var of varlist THCOMMUNETAUXNET THINTERCOMMUNALITETAUXAPP THVLMOYENNEUTILISEEPOUR IG THQUOTITEDESABATTEMENTSAVA THQUOTITEDESABATTEMENTSAJ II THQUOTITEDESABATTEMENTSAJU IL IM IN IO IP IQ IR IS IT IU IV IW {
	replace `var' = 0 if `var'==.
}
gen code_insee_commune = trim(DEPARTEMENT) + trim(COMMUNE)

gen taux_com   = THCOMMUNETAUXNET/100
gen taux_epci  = THINTERCOMMUNALITETAUXAPP/100


gen valeur_locative_moyenne_com  = THVLMOYENNEUTILISEEPOUR
gen valeur_locative_moyenne_epci = IG

* Pour certaines intercom, il n'y a pas de quotité ajustée mais seulement une quotité simple. Surement due aux interco créées après 2010 (qui est l'année du transfert de la TH départementale justifiant cet ajustement). Donc, si la valeur ajustée est nulle, on prend la quotité simple
gen abt_general_base_com       = cond(IR~=0,IR,IP)
gen abt_general_base_epci      = cond(IS~=0,IS,IQ)
gen abt_pac_1_2_com            = cond(THQUOTITEDESABATTEMENTSAJ~=0,THQUOTITEDESABATTEMENTSAJ,THQUOTITEDESABATTEMENTSAVA)
gen abt_pac_1_2_epci           = cond(THQUOTITEDESABATTEMENTSAJU~=0,THQUOTITEDESABATTEMENTSAJU,II)
gen abt_pac_3pl_com            = cond(IN~=0,IN,IL)
gen abt_pac_3pl_epci           = cond(IO~=0,IO,IM)
gen abt_condition_modeste_com  = cond(IV~=0,IV,IT)
gen abt_condition_modeste_epci = cond(IW~=0,IW,IU)

keep code_insee_commune taux_* valeur_locative_moyenne_* abt_*
foreach var of varlist  taux_* valeur_locative_moyenne_* abt_* {
	replace `var' = 0 if `var'==.
}

sort     code_insee_commune
outsheet code_insee_commune taux_* valeur_locative_moyenne_* abt_* using "${export_2022}.csv", comma replace
