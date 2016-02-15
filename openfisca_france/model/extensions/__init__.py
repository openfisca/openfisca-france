import os, glob
from importlib import import_module

EXTENSIONS_PATH = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))

extensions_parameters = []

def import_extension(extension_directory):
	extension_name = os.path.basename(os.path.normpath(extension_directory))
	py_files = glob.glob(os.path.join(extension_directory, "*.py"))
	modules = [
		os.path.basename(f)[:-3]
		for f in py_files
		if not os.path.basename(f).startswith('_')
		]
	for module in modules:
		import_module('.' + module, __package__ + '.' + extension_name)
	extensions_parameters.append(os.path.join(extension_directory, extension_name + '.xml'))

for extension_dir in EXTENSIONS_DIRECTORIES:
	import_extension(extension_dir)
