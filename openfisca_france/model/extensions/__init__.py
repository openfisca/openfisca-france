import os, glob
from imp import find_module, load_module

EXTENSIONS_PATH = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))

extensions_parameters = []

def import_extension(path):
	if path.endswith('.git'):
		import tempfile, subprocess
		temp_dir = tempfile.mkdtemp()
		clone_command = ' '.join(['git clone', path, temp_dir, '--quiet'])
		return_code = subprocess.call(clone_command, shell = True)
		if return_code > 0: raise IOError("Error loading extension from git repository " + path)
		import_extension_from_dir(temp_dir)
	else:
		import_extension_from_dir(path)

def import_extension_from_dir(extension_directory):
	if not os.path.isdir(extension_directory): raise IOError("Error loading extension: the extension directory " + extension_directory + " doesn't exist.")
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

def unload_all_extensions():
	import openfisca_france
	reload(openfisca_france.entities)
	extensions_parameters = []
	openfisca_france.init_tax_benefit_system()

for extension_dir in EXTENSIONS_DIRECTORIES:
	import_extension(extension_dir)
