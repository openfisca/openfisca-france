import os, glob
from imp import find_module, load_module

EXTENSIONS_PATH = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))

extensions_parameters = []

def import_extension(extension_directory):
	extension_name = os.path.basename(os.path.normpath(extension_directory))
	py_files = glob.glob(os.path.join(extension_directory, "*.py"))
	module_names = [
		os.path.basename(f)[:-3]
		for f in py_files
		if not os.path.basename(f).startswith('_')
		]
	for module_name in module_names:
		module = find_module(module_name, [extension_directory])
		load_module(module_name, *module)
	param_file = os.path.join(extension_directory, 'parameters.xml')
	if os.path.isfile(param_file):
		extensions_parameters.append(param_file)

for extension_dir in EXTENSIONS_DIRECTORIES:
	import_extension(extension_dir)
