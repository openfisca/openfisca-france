'''
EN: Look into folders to check path length and return an error if a too long path is found.
Also write too long path in a file.

FR: Ce script sert à estimer la longueur des chemins d'arborescence des paramètres,
afin de ne pas avoir de chemins > 150 caractères (incompatible Windows).
Il est à utiliser avant de contribuer à l'harmonisation.
⚠️ Il est également utilisé par la CI, dans l'étape de test sur Windows.
'''


import os
import logging


logging.basicConfig(level=logging.INFO)


def extract_paths_too_long(root_dir):
    '''
    Look into folders to check path length and return True if a too long path is found.
    '''
    path_too_long_detected = False
    maxlen = 0
    root_dir = root_dir.rstrip(os.sep)

    with open('path_too_long_list.txt', 'w') as outfile:
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
                    path_too_long_detected = True
                    logging.error(f'Path too long of {len(relative_file_path)-150} characters : {relative_file_path}')
                    outfile.write('{} here: {}\n'.format(
                        len(relative_file_path),
                        relative_file_path,
                        ))
    logging.info(f'Max length found : {maxlen} characters.')
    return path_too_long_detected


country_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
parameters_dir = os.path.join(country_dir, 'parameters')
if extract_paths_too_long(parameters_dir):
    # Return code 1 to indicate an error. Default is 0.
    exit(1)
# If no path are too long, the default return is 0: no error.
