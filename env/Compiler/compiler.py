import sys
import os
import json
import re
import time
import env
import warnings

WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\..\\"))

if hasattr(sys, 'frozen'):
	sys.path += [os.path.abspath(sys._MEIPASS)]
	os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
	WORKING_DIR = os.path.dirname(os.path.abspath(sys.executable))
	if os.getcwd().endswith('bin') or os.getcwd().endswith('Compiler'):
		os.chdir(os.path.abspath("../../"))
		WORKING_DIR = os.path.abspath(os.path.join(WORKING_DIR, "..\\..\\"))
	else:
		os.chdir(WORKING_DIR)

os.chdir(WORKING_DIR)
sys.path += [WORKING_DIR, os.path.join(WORKING_DIR, 'env')]

import interpreter
import pparser
import lexer
import env.Compiler.AssemblyGenerator as AssemblyCodeGeneratorModule
from env.Compiler.AssemblyGenerator import AssemblyCodeGenerator

class CompilerError(Exception):
	pass

class CompilerWarning(Warning):
	pass


def clear_exit(code=0):
	globals_copy = globals().copy()
	for var in globals_copy:
		if var not in ('sys', 'clear_exit'):
			del globals()[var]

	sys.exit(code)


def hex_to_ansi(hex_color):
	if not hex_color or hex_color.lower() == "reset":
		return "\033[0m"
	match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
	if not match:
		return "\033[0m"
	r, g, b = [int(match.group(1)[i:i+2], 16) for i in (0, 2, 4)]
	return f"\033[38;2;{r};{g};{b}m"

def check_config():
	if not isinstance(config, dict) or not isinstance(color_map, dict):
		raise TypeError(f"Config file must be a JSON object. Run '{os.path.abspath('../activate.py')}' to activate the environment.")
	if config.get('moded', False):
		return
	if not config.get('version', None):
		raise EnvironmentError(f"File 'config.json' is corrupted. Entry 'version' is missing. Run '{os.path.abspath('../activate.py')}' to activate the environment.")
	if not color_map:
		raise EnvironmentError(f"File 'config.json' is corrupted. Entry 'color_scheme' is missing. Run '{os.path.abspath('../activate.py')}' to activate the environment.")
	if not config.get('debug_mode', None) in ['normal', 'full', 'minimal']:
		raise EnvironmentError(f"File 'config.json' is corrupted. Entry 'debug_mode' must be either 'normal', 'full' or 'minimal'. Run '{os.path.abspath('../activate.py')}' to activate the environment.")
	for key in ["debug", "use_lucia_traceback", "print_comments", "recursion_limit", "home_dir"]:
		if config.get(key, PLACEHOLDER) is PLACEHOLDER:
			raise EnvironmentError(f"File '{CONFIG_PATH}' is corrupted. Entry '{key}' is missing. Run '{os.path.abspath('../activate.py')}' to activate the environment.")

def debug_log(*args):
	if config.get('debug', False):
		print(f"{hex_to_ansi(color_map.get('debug', '#434343'))}{''.join(map(str, args))}\033[0m")

def activate():
	os.chdir(WORKING_DIR)
	os.system("../activate.py")

CONFIG_PATH = os.path.join(WORKING_DIR, 'env', 'config.json')
with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
	try:
		config = json.load(config_file)
	except json.JSONDecodeError:
		activate()
		print(f"{hex_to_ansi('#F44350')}Config file is corrupted. Environment has been activated.\033[0m")
		clear_exit(1)
color_map = config.get('color_scheme', {})
FILE_PATH = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None

sys.path += [CONFIG_PATH, config.get('home_dir', os.path.join(WORKING_DIR, 'env'))]
sys.path = list(dict.fromkeys(sys.path))

recursion_limit = config.get('recursion_limit', 9999)
sys.setrecursionlimit((recursion_limit * 3) + 9)
if recursion_limit > 10000:
	if config.get('warnings', True):
		if config.get('use_lucia_traceback', True):
			print(f"{hex_to_ansi(color_map.get('warning', '#FFC107'))}-> File '{__file__}', warning:\nRecursionLimitWarning: Recursion limit is unusually high.\033[0m")
		else:
			warnings.warn("Recursion limit is unusually high.", env.Lib.Builtins.old.exceptions.RecursionLimitWarning)
PLACEHOLDER = object()

check_config()

expected_env = os.path.join(WORKING_DIR, 'env')
if config.get('home_dir', PLACEHOLDER) != expected_env:
	if config.get("moded", False):
		print(f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Environment is not activated. Use 'env\\activate.py' to activate the environment. Please run the file again.\033[0m")
		activate()


args = sys.argv[1:]
FILE = None


for i, arg in enumerate(args):
	if i == len(args) - 1:
		FILE = arg
		break

FILE = os.path.abspath(FILE)


if not FILE:
	raise FileNotFoundError("No file specified.")

if not os.path.exists(FILE):
	raise FileNotFoundError(f"File '{FILE}' not found.")

with open(FILE, 'r') as f:
	code = f.read()

os.chdir(config.get('home_dir', WORKING_DIR))

tokens = lexer.lexer(code)
parser = pparser.Parser(tokens, config)
ast = parser.parse()

try:
	with open("output.json", "w") as f:
		f.write(json.dumps(ast, indent=4))
	assembler = AssemblyCodeGenerator()
	assembly_code = assembler.generate(ast)
	with open("output.asm", "w") as f:
		f.write(assembly_code)
	print("Compilation successful.")
except Exception as e:
	raise CompilerError(f"An error occurred while compiling: {str(e)}")
