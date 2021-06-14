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

    missing = []
    for i in range(len(txt1)):
        key = txt1[i]
        if key not in txt2:
            missing.append(key)
        else:
            ind = txt2.index(key)
            txt2.pop(ind)
    en_trop = txt2

    #print(txt1, "\n ET APRES: ", txt2)
    return missing, en_trop

path1 = "openfisca_france/scripts/parameters/Nodes_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Nodes_APRES.txt"
print("Nodes 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1])

path1 = "openfisca_france/scripts/parameters/Cadre_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Cadre_APRES.txt"
print("Cadre 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1])
#
path1 = "openfisca_france/scripts/parameters/Noncadre_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Noncadre_APRES.txt"
print("Non cadre 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1])

path1 = "openfisca_france/scripts/parameters/Fonc_AVANT.txt"
path2 = "openfisca_france/scripts/parameters/Fonc_APRES.txt"
print("Fonc 😱  Missing: ", check_keys(path1, path2)[0], "\n", "😱  En trop", check_keys(path1, path2)[1])
