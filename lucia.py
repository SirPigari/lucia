import sys
import os
import json
import re
import time
import env
import warnings
import platform

WORKING_DIR = os.path.dirname(__file__)
VERSION = "1.3"
CALL_PATH = os.getcwd()

if hasattr(sys, 'frozen'):
    sys.path += [os.path.abspath(sys._MEIPASS)]
    os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
    WORKING_DIR = os.path.dirname(os.path.abspath(sys.executable))
    if os.getcwd().endswith('bin'):
        os.chdir(os.path.abspath("../../"))
        WORKING_DIR = os.path.abspath(os.path.join(WORKING_DIR, "..\\..\\"))
    else:
        os.chdir(WORKING_DIR)

os.chdir(WORKING_DIR)
sys.path += [WORKING_DIR, os.path.join(WORKING_DIR, 'env')]

import interpreter
import pparser
import lexer
from env.Lib.Builtins.exceptions import WrappedException

def clear_exit(code=0):
    globals_copy = globals().copy()
    for var in globals_copy:
        if var not in ('sys', 'clear_exit'):
            del globals()[var]

    sys.exit(code)


def hex_to_ansi(hex_color):
    if not config.get("supports_color", False):
        return ""
    if not hex_color or hex_color.lower() == "reset":
        return "\033[0m"
    match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
    if not match:
        return "\033[0m"
    r, g, b = [int(match.group(1)[i:i + 2], 16) for i in (0, 2, 4)]
    return f"\033[38;2;{r};{g};{b}m"


def check_config():
    if not isinstance(config, dict) or not isinstance(color_map, dict):
        raise TypeError(
            f"Config file must be a JSON object. Run '{os.path.abspath('.\\env\\activate.py')}' to activate the environment.")
    if config.get('moded', False):
        return
    if not config.get('version', None):
        raise EnvironmentError(
            f"File 'config.json' is corrupted. Entry 'version' is missing. Run '{os.path.abspath('.\\env\\activate.py')}' to activate the environment.")
    if not color_map:
        raise EnvironmentError(
            f"File 'config.json' is corrupted. Entry 'color_scheme' is missing. Run '{os.path.abspath('.\\env\\activate.py')}' to activate the environment.")
    if not config.get('debug_mode', None) in ['normal', 'full', 'minimal']:
        raise EnvironmentError(
            f"File 'config.json' is corrupted. Entry 'debug_mode' must be either 'normal', 'full' or 'minimal'. Run '{os.path.abspath('.\\env\\activate.py')}' to activate the environment.")
    for key in ["debug", "use_lucia_traceback", "print_comments", "recursion_limit", "home_dir"]:
        if config.get(key, PLACEHOLDER) is PLACEHOLDER:
            raise EnvironmentError(
                f"File '{CONFIG_PATH}' is corrupted. Entry '{key}' is missing. Run '{os.path.abspath('.\\env\\activate.py')}' to activate the environment.")


def debug_log(*args):
    if config.get('debug', False):
        print(f"{hex_to_ansi(color_map.get('debug', '#434343'))}{''.join(map(str, args))}{hex_to_ansi("reset")}")


def input_exec():
    global interpreter_, pparser, lexer
    code = input(
        f"{hex_to_ansi("reset")}{hex_to_ansi(color_map.get('input_arrows', '#136163'))}>>> {hex_to_ansi("reset")}{hex_to_ansi(color_map.get('input_text', '#BCBEC4'))}")
    print(f"{hex_to_ansi("reset")}{hex_to_ansi(color_map.get('output_text', '#BCBEC4'))}", end="")
    if code == "exit":
        print("Use 'exit()' to exit.")
        return
    tokens = lexer.lexer(code, include_comments=config.get('print_comments', False))
    if not tokens:
        if config.get('debug_mode', 'normal') == 'full' or config.get('debug_mode', 'normal') == 'minimal':
            debug_log(f"Statements generated: []")
        return
    if config.get('debug_mode', 'normal') == 'full' or config.get('debug_mode', 'normal') == 'minimal':
        debug_log(f"Tokens generated: {[token for token in tokens if token[0] != 'WHITESPACE']}")
    parser = pparser.Parser(tokens, config)
    parser.parse()
    if config.get('debug_mode', 'normal') == 'full' or config.get('debug_mode', 'normal') == 'minimal':
        debug_log(f"Statements generated: {parser.statements}")
    interpreter_.interpret(parser.statements)


def execute_file(file_path, exit=True):
    try:
        global interpreter, pparser, lexer
        if os.path.exists(file_path):
            file_path = os.path.abspath(file_path)
        else:
            file_path = os.path.join(CALL_PATH, file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        tokens = lexer.lexer(code, include_comments=config.get('print_comments', False))
        if config.get('debug_mode', 'normal') == 'full' or config.get('debug_mode', 'normal') == 'minimal':
            debug_log(f"Tokens generated: {[token for token in tokens if token[0] != 'WHITESPACE']}")
            if not tokens:
                debug_log(f"Statements generated: []")
                return
        parser = pparser.Parser(tokens, config)
    except Exception as e:
        raise RuntimeError(f"Failed to execute file '{file_path}'. Error: {e}")
    try:
        parser.parse()
        if config.get('debug_mode', 'normal') == 'full' or config.get('debug_mode', 'normal') == 'minimal':
            debug_log(f"Statements generated: {parser.statements}")
        interpreter_ = interpreter.Interpreter(config, file_path)
    except SyntaxError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Failed to parse file '{file_path}'. Error: {e}")
    interpreter_.interpret(parser.statements)


def activate():
    if config.get("moded", False):
        print(
            f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Environment is moded and cannot be activated. Set 'moded' to false to activate enviroment.{hex_to_ansi("reset")}")
        return
    ENV_PATH = os.path.join(WORKING_DIR, 'env')
    config_to_place = {
        "moded": False,
        "debug": False,
        "debug_mode": "normal",
        "supports_color": True,
        "use_lucia_traceback": True,
        "warnings": True,
        "use_predefs": True,
        "print_comments": False,
        "execute_code_blocks": {
            "C": True,
            "ASM": True,
            "PY": True
        },
        "lucia_file_extensions": [".lucia", ".luc", ".lc", ".l"],
        "home_dir": ENV_PATH,
        "recursion_limit": 9999,
        "version": VERSION,
        "color_scheme": {
            "exception": "#F44350",
            "warning": "#FFC107",
            "debug": "#434343",
            "comment": "#757575",
            "input_arrows": "#136163",
            "input_text": "#BCBEC4",
            "output_text": "#BCBEC4",
            "info": "#9209B3"
        }
    }

    os.remove(os.path.join(ENV_PATH, "config.json"))

    with open(f"{ENV_PATH}/config.json", "w") as file:
        json.dump(config_to_place, file, indent=2)

    print(f"{hex_to_ansi(config_to_place.get("info", "#9209B3"))}Environment activated.{hex_to_ansi("reset")}")


def handle_exception(exception, file_name, exit=True):
    exception = WrappedException(exception)
    if isinstance(exception, Warning):
        print(f"{hex_to_ansi(color_map.get('warning', '#FFC107'))}-> File '{file_name}' warning:\n{exception}{hex_to_ansi("reset")}")
        return
    else:
        print(
            f"{hex_to_ansi(color_map.get('exception', '#F44350'))}-> File '{file_name}' got traceback:\n{exception}{hex_to_ansi("reset")}")
    if exit:
        clear_exit(1)


def handle_file_exec(file_path, exit=True):
    if config.get("use_lucia_traceback", True):
        try:
            execute_file(file_path, exit)
        except SystemExit:
            clear_exit(0)
        except Warning as w:
            handle_exception(w, file_path, exit=False)
        except Exception as e:
            handle_exception(e, file_path, exit)
    else:
        execute_file(file_path, exit)


CONFIG_PATH = os.path.join(WORKING_DIR, 'env', 'config.json')
config = {"version": VERSION}
if "--no-color" in sys.argv:
    config['supports_color'] = False
with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
    try:
        config = json.load(config_file)
        if "--no-color" in sys.argv:
            config['supports_color'] = False
    except json.JSONDecodeError:
        activate()
        print(f"{hex_to_ansi('#F44350')}Config file is corrupted. Environment has been activated.{hex_to_ansi("reset")}")
        clear_exit(1)
    except FileNotFoundError:
        activate()
        print(f"{hex_to_ansi('#F44350')}Config file not found. Environment has been activated.{hex_to_ansi('reset')}")
        clear_exit(1)
color_map = config.get('color_scheme', {})
FILE_PATH = None
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg == sys.executable:
            continue
        if not arg.startswith("-"):
            FILE_PATH = arg
            break

sys.path += [CONFIG_PATH, config.get('home_dir', os.path.join(WORKING_DIR, 'env'))]
sys.path = list(dict.fromkeys(sys.path))

recursion_limit = config.get('recursion_limit', 9999)
sys.setrecursionlimit((recursion_limit * 3) + 9)
if recursion_limit > 10000:
    if config.get('warnings', True):
        if config.get('use_lucia_traceback', True):
            print(
                f"{hex_to_ansi(color_map.get('warning', '#FFC107'))}-> File '{__file__}', warning:\nRecursionLimitWarning: Recursion limit is unusually high.{hex_to_ansi("reset")}")
        else:
            warnings.warn("Recursion limit is unusually high.", env.Lib.Builtins.old.exceptions.RecursionLimitWarning)
PLACEHOLDER = object()

check_config()

if "--activate" in sys.argv:
    try:
        activate()
    except Exception as e:
        print(
            f"{hex_to_ansi(color_map.get('exception', '#F44350'))}Failed to activate environment:\n{e}{hex_to_ansi("reset")}")
        clear_exit(1)
    clear_exit(0)

expected_env = os.path.join(WORKING_DIR, 'env')
if config.get('home_dir', PLACEHOLDER) != expected_env:
    if not config.get('moded', False):
        print(
            f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Environment is not activated. Use 'env\\activate.py' to activate the environment. Please run the file again.{hex_to_ansi("reset")}")
        activate()
        clear_exit(0)
    else:
        print(
            f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Environment is moded. Use 'env\\activate.py' to activate the environment. Please run the file again.{hex_to_ansi("reset")}")
        clear_exit(0)


os.chdir(config.get('home_dir', WORKING_DIR))
if (len(sys.argv) > 1) and (not ("--no-title" in sys.argv)):
    os.system(f"title Lucia-{config.get('version', '(version unknown)')}")

if len(sys.argv) > 1:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(
            f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Lucia-{config.get('version', '(version unknown)')} Interpreter\nUsage: lucia.py [file_path]\n{hex_to_ansi("reset")}")
        clear_exit(0)
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"Lucia-{config.get('version', '(version unknown)')}")
        clear_exit(0)
    if "--config" in sys.argv:
        print(f"Config file path: {CONFIG_PATH}")
        clear_exit(0)
    if "--no-color" in sys.argv or "--nocolor" in sys.argv or "--nc" in sys.argv or "-nc" in sys.argv:
        config['supports_color'] = False
    if "--home" in sys.argv:
        print(f"Home directory: {config.get('home_dir', os.path.join(WORKING_DIR, 'env'))}")
        clear_exit(0)
    if "--test-all-tests" in sys.argv:
        path = os.path.join(config.get('home_dir', WORKING_DIR), 'Docs\\tests')
        lucia_ext = config.get('lucia_file_extensions', [".lucia", ".luc", ".lc", ".l"])
        for file in os.listdir(path):
            if "." + file.rsplit(os.path.extsep, 1)[-1] in lucia_ext:
                print(f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Running test '{file}'...\n{hex_to_ansi("reset")}")
                try:
                    handle_file_exec(os.path.join(path, file), exit=False)
                except Exception as e:
                    print(
                        f"{hex_to_ansi(color_map.get('exception', '#F44350'))}Test '{file}' failed with error:\n{type(e).__name__}: {e}\n{hex_to_ansi("reset")}")
            else:
                print(f"{hex_to_ansi(color_map.get('warning', '#FFC107'))}Skipping test '{file}'...\n{hex_to_ansi("reset")}")
        print(f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}All tests have been executed.{hex_to_ansi("reset")}")
        clear_exit(0)
    if "--activate" in sys.argv:
        try:
            activate()
        except Exception as e:
            print(f"{hex_to_ansi(color_map.get('exception', '#F44350'))}Failed to activate environment:\n{e}{hex_to_ansi("reset")}")
            clear_exit(1)
        clear_exit(0)
    if "--info" in sys.argv:
        info = {
            "version": config.get('version', '(version unknown)'),
            "home_dir": config.get('home_dir', os.path.join(WORKING_DIR, 'env')),
            "config_path": CONFIG_PATH,
        }
        for key, value in info.items():
            print(f"{key}: {value}")

        clear_exit(0)
    if "--timer" in sys.argv:
        start_time = time.time()
        handle_file_exec(FILE_PATH)
        print(
            f"\n{hex_to_ansi(color_map.get('info', '#D10CFF'))}Execution time: {time.time() - start_time:.4f} seconds{hex_to_ansi("reset")}")
        clear_exit(0)

if FILE_PATH:
    handle_file_exec(FILE_PATH)
    clear_exit(0)
else:
    interpreter_ = interpreter.Interpreter(config, repl=True)
    print(
        f"{hex_to_ansi(color_map.get('info', '#D10CFF'))}Lucia-{config.get('version', '(version unknown)')} REPL\nType 'exit()' to exit or 'help()' for help.{hex_to_ansi("reset")}")
    while True:
        if config.get('use_lucia_traceback', True):
            try:
                input_exec()
            except SystemExit:
                break
            except KeyboardInterrupt:
                print()
                clear_exit(0)
            except (Exception, Warning) as e:
                handle_exception(e, "<stdin>", exit=False)
        else:
            input_exec()
    clear_exit()
