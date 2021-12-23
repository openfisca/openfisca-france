"""
Ce script sert à estimer la longueur des chemins d'arborescence des paramètres,
afin de ne pas avoir de chemins > 150 caractères (incompatible Windows).
Il est à utiliser avant de contribuer à l'harmonisation
"""


import os


def extract_paths_too_long(root_dir):
    root_dir = root_dir.rstrip(os.sep)

    with open("chemins_trop_longs.txt", "w") as outfile:
        for path, dirs, files in os.walk(root_dir):
            relative_path = path[len(root_dir) + 1:]
            for dir in dirs:
                if dir.startswith("."):
                    # Ignore hidden directories.
                    dirs.remove(dir)
            for file in files:
                if file.startswith("."):
                    # Ignore hidden files.
                    continue
                relative_file_path = os.path.join(relative_path, file)
                if len(relative_file_path) > 150:
                    outfile.write("{} here: {}\n".format(
                        len(relative_file_path),
                        relative_file_path,
                        ))


country_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
parameters_dir = os.path.join(country_dir, "parameters")
extract_paths_too_long(parameters_dir)
