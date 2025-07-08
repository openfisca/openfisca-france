#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa: T201
'''
Script pour extraire les variables des fichiers de tests YAML et les exporter en CSV.
'''

import os
import yaml
import csv
import re
from collections import defaultdict

OUTPUT_DIR = './openfisca_france/scripts/output/'

def extract_variable_labels_from_python_files(model_directory):
    '''
    Extrait les labels des variables depuis les fichiers Python du modèle OpenFisca.

    Args:
        model_directory: Chemin vers le répertoire openfisca_france/model

    Returns:
        Dict {variable_name: label}
    '''
    variable_labels = {}

    # Parcourir tous les fichiers Python dans le répertoire model
    for root, dirs, files in os.walk(model_directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Trouver toutes les classes qui héritent de Variable
                    class_pattern = r'class\s+(\w+)\s*\(\s*Variable\s*\):'
                    classes = re.finditer(class_pattern, content)

                    for match in classes:
                        variable_name = match.group(1)
                        class_start = match.start()

                        # Chercher le label dans la définition de la classe
                        # On prend les lignes suivant la définition de classe jusqu'à la prochaine classe ou fonction
                        lines = content[class_start:].split('\n')
                        label = None

                        for line in lines[1:]:  # Ignorer la ligne de définition de classe
                            # Arrêter si on trouve une nouvelle classe ou fonction
                            if isinstance(line.strip(), str) and (
                                    line.strip().startswith('class ') or
                                    line.strip().startswith('def ')):
                                break

                            # Chercher la ligne contenant le label
                            if 'label' in line and '=' in line:
                                # Extraire le label en gérant correctement les guillemets
                                try:
                                    # Trouver la position du signe =
                                    eq_pos = line.find('=')
                                    if eq_pos == -1:
                                        continue

                                    # Prendre la partie après le =
                                    value_part = line[eq_pos + 1:].strip()
                                    if isinstance(value_part, int):
                                        continue

                                    # Gérer les différents types de quotes
                                    if value_part.startswith('"""'):
                                        # Triple quotes double
                                        if (value_part.endswith('"""') and
                                                len(value_part) > 6):
                                            label = value_part[3:-3]
                                        elif '"""' in value_part[3:]:
                                            end_pos = value_part.find('"""', 3)
                                            label = value_part[3:end_pos]
                                    elif value_part.startswith("'''"):
                                        # Triple quotes simple
                                        if (value_part.endswith("'''") and
                                                len(value_part) > 6):
                                            label = value_part[3:-3]
                                        elif "'''" in value_part[3:]:
                                            end_pos = value_part.find("'''", 3)
                                            label = value_part[3:end_pos]
                                    elif value_part.startswith('"'):
                                        # Guillemets doubles - chercher la fin en gérant les échappements
                                        i = 1
                                        while i < len(value_part):
                                            if value_part[i] == '"' and (
                                                    i == 1 or value_part[i - 1] != '\\'):
                                                label = value_part[1:i]
                                                break
                                            i += 1
                                    elif value_part.startswith("'"):
                                        # Guillemets simples - chercher la fin en gérant les échappements
                                        i = 1
                                        while i < len(value_part):
                                            if value_part[i] == "'" and (
                                                    i == 1 or value_part[i - 1] != '\\'):
                                                label = value_part[1:i]
                                                break
                                            i += 1
                                except Exception:
                                    pass

                                if label:
                                    break

                        if label:
                            variable_labels[variable_name] = label

                except Exception as e:
                    print(f"Erreur lors de l'analyse du fichier {file_path}: {e}")

    return variable_labels


def extract_variables_from_input(input_data):
    '''
    Extrait toutes les variables d'une section input avec leur entité.
    '''
    variables = {}  # {variable_name: entity}

    def extract_from_dict(data, entity, exclude_keys=None):
        if exclude_keys is None:
            exclude_keys = {
                'declarants',
                'personnes_a_charge',
                'enfants',
                'parents',
                'personne_de_reference',
            }

        if isinstance(data, dict):
            for key, value in data.items():
                # Ignorer les clés qui sont des références à des individus ou des structures
                if isinstance(key, str) and (
                        key.startswith('ind') or key in exclude_keys):
                    continue

                # Ignorer les variables qui commencent par 4 chiffres suivis d'un tiret (ex: 2011-10)
                if re.match(r'^\d{4}', str(key)):
                    continue

                # Ajouter la variable avec son entité
                variables[key] = entity

                # Récursion pour les valeurs qui sont des dictionnaires
                if isinstance(value, dict):
                    extract_from_dict(value, entity, exclude_keys)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            extract_from_dict(item, entity, exclude_keys)

    # Analyser chaque entité
    for entity_name, entity_data in input_data.items():
        if entity_name in ['foyer_fiscal', 'famille', 'menage']:
            # Pour ces entités, extraire directement les variables
            extract_from_dict(entity_data, entity_name)
        elif entity_name == 'individus':
            # Pour les individus, analyser chaque individu
            if isinstance(entity_data, dict):
                for individu_id, individu_data in entity_data.items():
                    if isinstance(individu_data, dict):
                        extract_from_dict(individu_data, 'individus')

    return variables


def main():
    # Répertoires
    tests_dir = './tests'
    model_dir = './openfisca_france/model'
    csv_filename = OUTPUT_DIR + 'input_variable.csv'

    print('Extraction des labels des variables depuis les fichiers Python...')
    variable_labels = extract_variable_labels_from_python_files(model_dir)
    print(f'Trouvé {len(variable_labels)} labels de variables')

    print('Extraction des variables des fichiers de tests YAML...')
    print(f'Répertoire analysé: {tests_dir}')

    all_variables = {}  # {variable_name: {entity, files_using_it, examples}}
    file_count = 0

    # Parcourir tous les fichiers YAML
    for root, dirs, files in os.walk(tests_dir):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, tests_dir)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)

                    # S'assurer que data est une liste
                    if not isinstance(data, list):
                        data = [data] if data else []

                    # Analyser chaque test dans le fichier
                    file_variables = set()
                    for test_case in data:
                        if isinstance(test_case, dict) and 'input' in test_case:
                            variables = extract_variables_from_input(test_case['input'])

                            for var_name, entity in variables.items():
                                file_variables.add(var_name)

                                if var_name not in all_variables:
                                    all_variables[var_name] = {
                                        'entity': entity,
                                        'files': set(),
                                        'count': 0,
                                    }

                                all_variables[var_name]['files'].add(relative_path)
                                all_variables[var_name]['count'] += 1

                    file_count += 1
                    if file_count % 100 == 0:
                        print(f'Traité {file_count} fichiers...')

                except Exception as e:
                    print(f'Erreur avec le fichier {file_path}: {e}')
                    raise e
    if file_count == 0:
        print(f'Aucun fichier YAML trouvé dans le répertoire {tests_dir}.')
        return
    print('\nAnalyse terminée!')
    print(f'Fichiers traités: {file_count}')
    print(f'Variables uniques trouvées: {len(all_variables)}')

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'variable',
            'entite',
            'label',
            'nb_fichiers',
            'nb_utilisations',
            'exemples_fichiers',
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Écrire l'en-tête
        writer.writeheader()

        # Trier les variables par ordre alphabétique
        for var_name in sorted(all_variables.keys()):
            var_info = all_variables[var_name]

            # Récupérer le label depuis les fichiers Python
            label = variable_labels.get(var_name, '')

            # Limiter les exemples de fichiers à 3 pour éviter des cellules trop longues
            example_files = list(var_info['files'])[:3]
            if len(var_info['files']) > 3:
                example_files.append(f'... et {len(var_info["files"]) - 3} autres')

            writer.writerow({
                'variable': var_name,
                'entite': var_info['entity'],
                'label': label,
                'nb_fichiers': len(var_info['files']),
                'nb_utilisations': var_info['count'],
                'exemples_fichiers': '; '.join(example_files),
            })

    print(f'\nFichier CSV créé: {csv_filename}')

    # Afficher un résumé
    print(f'\n{"=" * 60}')
    print('RÉSUMÉ')
    print(f'{"=" * 60}')

    # Compter par entité
    entity_counts = defaultdict(int)
    for var_info in all_variables.values():
        entity_counts[var_info['entity']] += 1

    print("Variables d'entrées utilisées dans les tests YAML, par entité:")
    for entity, count in sorted(entity_counts.items()):
        print(f'  - {entity}: {count} variables')

    # Top 10 des variables d'entrées les plus utilisées
    print("\nTop 10 des variables d'entrées les plus utilisées dans les tests YAML:")
    most_used = sorted(
        all_variables.items(), key=lambda x: x[1]['count'], reverse=True
    )[:10]
    for var_name, var_info in most_used:
        print(
            f"  - {var_name}: {var_info['count']} utilisations dans {len(var_info['files'])} fichiers"
        )


if __name__ == '__main__':
    main()
