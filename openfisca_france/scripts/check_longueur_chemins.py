'''
Ce script sert à estimer la longueur des chemins d'arborescence des paramètres,
afin de ne pas avoir de chemins > 150 caractères (incompatible Windows).
Il est à utiliser avant de contribuer à l'harmonisation
'''


import os
import logging


logging.basicConfig(level=logging.INFO)


def extract_paths_too_long(root_dir):
    chemin_trop_long_trouve = False
    maxlen = 0
    root_dir = root_dir.rstrip(os.sep)

    with open('chemins_trop_longs.txt', 'w') as outfile:
        for path, dirs, files in os.walk(root_dir):
            relative_path = path[len(root_dir) + 1:]
            for dir in dirs:
                if dir.startswith('.'):
                    # Ignore hidden directories.
                    dirs.remove(dir)
            for file in files:
                if file.startswith('.'):
                    # Ignore hidden files.
                    continue
                relative_file_path = os.path.join(relative_path, file)
                maxlen = max(maxlen, len(relative_file_path))
                if len(relative_file_path) > 150:
                    chemin_trop_long_trouve = True
                    logging.error(f"Chemin trop long de {len(relative_file_path)-150} caractères : {relative_file_path}")
                    outfile.write('{} here: {}\n'.format(
                        len(relative_file_path),
                        relative_file_path,
                        ))
    logging.info(f"Longueur maximale trouvée : {maxlen} caractères.")
    return chemin_trop_long_trouve


country_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
parameters_dir = os.path.join(country_dir, 'parameters')
if extract_paths_too_long(parameters_dir):
    # Retourne une erreur
    exit(1)
else:
    # Retourne 0 pour indiquer qu'il n'y a pas de chemin trop long
    exit(0)
