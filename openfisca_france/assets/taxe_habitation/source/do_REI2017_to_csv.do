/***************************************************************************************/
/*** Mise en forme du fichier REI 2017 et 2018 pour OpenFisca
     Nécessite Stata version 14                        *********************************/
/***************************************************************************************/

clear
set more off
cap log close

**** Chemin des REI 2017 et REI 2018 en local. Le fichier REI 2017 en .xlsx est accessible en ligne sur https://www.data.gouv.fr/fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-3/
global input_2017 = ""
global input_2018 = ""

**** Chemin d'export du fichier csv
global export_2017 = ""
global export_2018 = ""

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
