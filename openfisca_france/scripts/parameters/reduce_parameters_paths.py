import logging
import os
import shutil
import yaml


PARENT_DIRECTORY = os.path.abspath('../..')
PATH_LENGTH_TO_IGNORE = len(PARENT_DIRECTORY)

PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'parameters')
PATH_MAX_LENGTH = 150

INDEX_FILENAME = 'index.yaml'

# Create logger
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


def clean_from_filename(relative_path):
    last_separator_index = relative_path.rfind(os.path.sep)
    if last_separator_index == -1:
        raise ValueError('Directory expected but none found in: ' + relative_path)
    return relative_path[:last_separator_index]


def list_long_paths(absolute_directory_path):
    long_paths = []

    for directory, _sub_directories, files in os.walk(absolute_directory_path):
        for f in files:
            file_path = os.path.join(directory, f)
            if (len(file_path) - PATH_LENGTH_TO_IGNORE) > PATH_MAX_LENGTH:
                path_extract = clean_from_filename(get_sub_parent_path(file_path, PARAMETERS_DIRECTORY))
                if path_extract not in long_paths:
                    long_paths.append(path_extract)

    return long_paths


def get_sub_parent_path(directory_path, parent_path):
    absolute_path = os.path.abspath(directory_path)
    return os.path.relpath(absolute_path, parent_path)


def get_raw_content(yaml_filepath):
    with open(yaml_filepath, 'r') as stream:
        return yaml.load(stream)


def harvest(item):
    '''
    Put into a dictionary the content of the file hierarchy starting at the given item.

    An 'index.yaml' file content is directly added to the current dictionary key.
    Any other file or a directory content in stored under a new key (file or directory name).

    @param item: A directory of yaml files or a yaml file.
    '''
    content = {}
    item_name = os.path.basename(item)

    if os.path.isdir(item):
        sub_items = os.listdir(item)
        sub_content = {}

        # Harvest index.yaml first if it exists
        index_content = None
        if INDEX_FILENAME in sub_items:
            index_content = harvest(os.path.join(item, INDEX_FILENAME))
            sub_items.remove(INDEX_FILENAME)

        for subitem in sub_items:
            sub_content.update(harvest(os.path.join(item, subitem)))

        # Add index content on top
        if index_content:
            sub_content.update(index_content)

        content[item_name] = sub_content

    else:
        if item_name == INDEX_FILENAME:
            content.update(get_raw_content(item))
        else:
            # Clean file name from extension
            item_name = os.path.splitext(item_name)[0]
            # Store content under cleaned file name section
            content[item_name] = get_raw_content(item)

    return content


def parse_and_clean(directory, paths_to_clean):
    items = os.listdir(directory)

    # Parse items in directory and harvest content for long paths
    for item in items:
        item_path = os.path.join(directory, item)
        functional_path = get_sub_parent_path(item_path, PARAMETERS_DIRECTORY)

        if os.path.isdir(item_path):
            if functional_path in paths_to_clean:
                yaml_path = os.path.join(directory, item + ".yaml")

                logger.info(os.linesep + "Cleaning long directory into: " + yaml_path)
                content = harvest(item_path)
                with open(yaml_path, 'w') as yaml_file:
                    yaml_file.write(yaml.dump(content[item], default_flow_style=False, allow_unicode=True))

                # Delete harvested directory
                logger.info("Deleting " + item_path)
                shutil.rmtree(item_path)

            else:
                parse_and_clean(item_path, paths_to_clean)


long_parameters_paths = list_long_paths(PARAMETERS_DIRECTORY)
logger.info("{} directories have files with more than {} characters in their paths starting from this directory: {}".format(len(long_parameters_paths), PATH_MAX_LENGTH, PARENT_DIRECTORY).encode('utf-8'))

while len(long_parameters_paths) > 0:
    parse_and_clean(PARAMETERS_DIRECTORY, long_parameters_paths)
    long_parameters_paths = list_long_paths(PARAMETERS_DIRECTORY)
