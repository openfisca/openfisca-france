import os
import shutil


# PARENT_DIRECTORY = os.path.abspath('../..')
# PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'parameters')

PARAMETERS_DIRECTORY = "/home/benjello/projets/baremes-ipp-yaml/parameters/"

absolute_directory_path = os.path.join(PARAMETERS_DIRECTORY, 'taxation_indirecte')

target_pattern = "_par_hl_boisson.yaml"
replacement = ".yaml"

for directory, _sub_directories, files in os.walk(absolute_directory_path):
    for f in files:
        old_file = f
        if target_pattern in f:
            new_file = old_file.replace(target_pattern, replacement)

            old_file_path = os.path.join(directory, f)
            new_file_path = os.path.join(directory, new_file)
            shutil.move(old_file_path, new_file_path)
            print(old_file_path)
            print(new_file_path)
            print("")
