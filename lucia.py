import sys
import os
import json
import re

sys.path += [os.path.dirname(__file__), os.path.join(os.path.dirname(__file__), 'env')]

import lexer
import pparser
import interpreter

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'env', 'config.json')
config = json.load(open(CONFIG_PATH, 'r', encoding='utf-8'))
color_map = config.get('color_scheme', {})
FILE_PATH = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None

sys.path += [CONFIG_PATH, config.get('home_dir', os.path.join(os.path.dirname(__file__), 'env'))]
sys.path = list(dict.fromkeys(sys.path))

sys.setrecursionlimit((config.get('recursion_limit', 9999) * 3) + 9)
PLACEHOLDER = object()

def check_config():
    if not isinstance(config, dict) or not isinstance(color_map, dict):
        raise TypeError("Config file must be a JSON object.")
    if not config.get('version', None):
        raise EnvironmentError("File 'config.json' is corrupted. Entry 'version' is missing.")
    if not color_map:
        raise EnvironmentError("File 'config.json' is corrupted. Entry 'color_scheme' is missing.")
    if not config.get('debug_mode', None) in ['normal', 'full', 'minimal']:
        raise EnvironmentError("File 'config.json' is corrupted. Entry 'debug_mode' must be either 'normal', 'full' or 'minimal'.")
    for key in ["debug", "use_lucia_traceback", "print_comments", "recursion_limit", "home_dir"]:
        if config.get(key, PLACEHOLDER) is PLACEHOLDER:
            raise EnvironmentError(f"File '{CONFIG_PATH}' is corrupted. Entry '{key}' is missing.")

check_config()
os.chdir(config.get('home_dir', os.path.dirname(__file__)))

def hex_to_ansi(hex_color):
    if not hex_color or hex_color.lower() == "reset":
        return "\033[0m"
    match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
    if not match:
        return "\033[0m"
    r, g, b = [int(match.group(1)[i:i+2], 16) for i in (0, 2, 4)]
    return f"\033[38;2;{r};{g};{b}m"

def debug_log(*args):
    if config.get('debug', False):
        print(f"{hex_to_ansi(color_map.get('debug', '#434343'))}{''.join(map(str, args))}\033[0m")

def input_exec():
    global interpreter_, pparser, lexer
    code = input(f"\033[0m{hex_to_ansi(color_map.get('input_arrows', '#136163'))}>>>\033[0m{hex_to_ansi(color_map.get('input_text', '#BCBEC4'))} ")
    print(f"\033[0m{hex_to_ansi(color_map.get('output_text', '#BCBEC4'))}", end="")
    if code == "exit":
        print("Use 'exit()' to exit.")
        return
    tokens = lexer.lexer(code, include_comments=config.get('print_comments', False))
    debug_log(f"Tokens generated: {tokens}")
    parser = pparser.Parser(tokens)
    parser.parse()
    debug_log(f"Statements generated: {parser.statements}")
    interpreter_.interpret(parser.statements)

def execute_file(file_path):
    global interpreter, pparser, lexer
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    tokens = lexer.lexer(code, include_comments=config.get('print_comments', False))
    if config.get('debug_mode', 'normal') == 'full' or config.get('debug_mode', 'normal') == 'minimal':
        debug_log(f"Tokens generated: {tokens}")
    parser = pparser.Parser(tokens)
    parser.parse()
    if config.get('debug_mode', 'normal') == 'full' or config.get('debug_mode', 'normal') == 'minimal':
        debug_log(f"Statements generated: {parser.statements}")
    interpreter_ = interpreter.Interpreter(config)
    interpreter_.interpret(parser.statements)

def handle_exception(exception, file_name, exit=True):
    exception_type = type(exception).__name__
    color = color_map.get('exception', '#F44350') if isinstance(exception, (RecursionError, RuntimeError, Exception)) else color_map.get('warning', '#FFC107')
    print(f"{hex_to_ansi(color)}-> File '{file_name}', Got traceback:\n{exception_type}: {exception}\33[0m")
    if exit:
        sys.exit(1)

if FILE_PATH:
    if config.get("use_lucia_traceback", True):
        try:
            execute_file(FILE_PATH)
        except (RecursionError, Warning, RuntimeError, Exception) as e:
            handle_exception(e, FILE_PATH)
        except SystemExit:
            sys.exit(0)
    else:
        execute_file(FILE_PATH)
else:
    interpreter_ = interpreter.Interpreter(config)
    print(f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Lucia-{config.get('version', '(version unknown)')} REPL\nType 'exit()' to exit or 'help()' for help.\033[0m")
    while True:
        if config.get('use_lucia_traceback', True):
            try:
                input_exec()
            except (RecursionError, Warning, RuntimeError, Exception) as e:
                handle_exception(e, "<stdin>", exit=False)
            except SystemExit:
                break
        else:
            input_exec()
    sys.exit(0)
