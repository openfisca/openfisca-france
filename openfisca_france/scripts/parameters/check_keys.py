# CHECK DEUX DOCS TXT   
import regex as re


def check_keys(path1, path2):

    txt1 = []
    with open(path1,'r') as file1:
        for line in file1:
            key = re.findall(r"'\w+':", line)
            for i in range(len(key)):
                key_name = re.findall(r"\w+", key[i])
                for j in range(len(key_name)):
                    txt1.append(key_name[j])

    txt2 = []
    with open(path2,'r') as file2:
        for line in file2:
            key = re.findall(r"'\w+':", line)
            for i in range(len(key)):
                key_name = re.findall(r"\w+", key[i])
                for j in range(len(key_name)):
                    txt2.append(key_name[j])

    #print("TXT AVANT", txt1, "\n ET TXT APRES: ", txt2)

    missing = []
    for i in range(len(txt1)):
        key = txt1[i]
        if key not in txt2:
            missing.append(key)
        else:
            ind = txt2.index(key)
            txt2.pop(ind)
    en_trop = txt2

    return missing, en_trop

# Pour travailler avec PAT
path1 = "openfisca_france/scripts/parameters/Nodes_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Nodes_APRES.txt"
print("Nodes 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")

path1 = "openfisca_france/scripts/parameters/Cadre_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Cadre_APRES.txt"
print("Cadre 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")
#
path1 = "openfisca_france/scripts/parameters/Noncadre_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Noncadre_APRES.txt"
print("Non cadre 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")

path1 = "openfisca_france/scripts/parameters/Fonc_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Fonc_APRES.txt"
print("Fonc 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")

path1 = "openfisca_france/scripts/parameters/Fonc_etat_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Fonc_etat_APRES.txt"
print("Fonc Etat 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")

path1 = "openfisca_france/scripts/parameters/Fonc_colloc_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Fonc_colloc_APRES.txt"
print("Fonc Colloc 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")

path1 = "openfisca_france/scripts/parameters/Fonc_contract_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Fonc_contract_APRES.txt"
print("Fonc Contract 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"

path1 = "openfisca_france/scripts/parameters/Commun_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Commun_APRES.txt"
print("COMMUN 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"

path1 = "openfisca_france/scripts/parameters/Public_host_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Public_host_APRES.txt"
print("HOSPITALIER 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"

path1 = "openfisca_france/scripts/parameters/Public_host_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Public_host_APRES.txt"
print("TERRITOIRE 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"

path1 = "openfisca_france/scripts/parameters/pat_children_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/pat_children_APRES.txt"
print("PAT CHILDREN 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"

# Pour travailler avec SAL
path1 = "openfisca_france/scripts/parameters/SalNodes_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/SalNodes_APRES.txt"
print("Sal Nodes 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")
# 
path1 = "openfisca_france/scripts/parameters/SalCadre_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/SalCadre_APRES.txt"
print("Cadre 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")
# #
path1 = "openfisca_france/scripts/parameters/SalNoncadre_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/SalNoncadre_APRES.txt"
print("Non cadre 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")
# 
# path1 = "openfisca_france/scripts/parameters/Fonc_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/Fonc_APRES.txt"
# print("Fonc 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")
# 
# path1 = "openfisca_france/scripts/parameters/Fonc_etat_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/Fonc_etat_APRES.txt"
# print("Fonc Etat 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")
# 
# path1 = "openfisca_france/scripts/parameters/Fonc_colloc_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/Fonc_colloc_APRES.txt"
# print("Fonc Colloc 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1], "\n")
# 
# path1 = "openfisca_france/scripts/parameters/Fonc_contract_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/Fonc_contract_APRES.txt"
# print("Fonc Contract 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"
# 
# path1 = "openfisca_france/scripts/parameters/Commun_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/Commun_APRES.txt"
# print("COMMUN 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"
# 
# path1 = "openfisca_france/scripts/parameters/Public_host_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/Public_host_APRES.txt"
# print("HOSPITALIER 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"
# 
# path1 = "openfisca_france/scripts/parameters/Public_host_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/Public_host_APRES.txt"
# print("TERRITOIRE 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"
# 
# path1 = "openfisca_france/scripts/parameters/pat_children_AVANT.txt"
# path2 = "openfisca_france/scripts/parameters/pat_children_APRES.txt"
# print("PAT CHILDREN 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1]), "\n"
# 