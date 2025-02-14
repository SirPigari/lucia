import lexer
import pparser
import interpreter
import sys
import json
import os
import re


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'env/config.json')
config = json.load(open(CONFIG_PATH, 'r', encoding='utf-8'))
color_map = config.get('color_scheme', {})
FILE_PATH = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None

# set the recursion_limit to recursion_limit * 3 + 9
recursion_limit = (config.get('recursion_limit', 9999) * 3) + 9
sys.setrecursionlimit(recursion_limit)

def check_config():
    if not isinstance(config, dict):
        raise TypeError("Config file must be a JSON object.")
    if not isinstance(color_map, dict):
        raise TypeError("Color scheme must be a JSON object.")
    needs = ["debug", "use_lucia_traceback", "print_comments", "recursion_limit", "home_dir"]
    for need in needs:
        if not hasattr(config, need):
            raise EnvironmentError(f"File '{CONFIG_PATH}' is corrupted.")

os.chdir(config.get('home_dir', os.path.dirname(__file__)))


def hex_to_ansi(hex_color):
    if not hex_color or hex_color.lower() == "reset":
        return "\033[0m"

    match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
    if not match:
        return "\033[0m"

    r, g, b = tuple(int(match.group(1)[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

def debug_log(*args):
    if config.get('debug', False):
        ansi_color = hex_to_ansi(color_map.get('debug', '#434343'))
        print(f"{ansi_color}{''.join(map(str, args))}\033[0m")

def execute_file(file_path):
    global config, interpreter, pparser, lexer
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    tokens = lexer.lexer(code, include_comments=config.get('print_comments', False))
    debug_log(f"Tokens generated: {tokens}")
    parser = pparser.Parser(tokens)
    parser.parse()
    debug_log(f"Statements generated: {parser.statements}")
    interpreter = interpreter.Interpreter(config)
    interpreter.interpret(parser.statements)

if FILE_PATH:
    if config.get("use_lucia_traceback", True):
        try:
            execute_file(FILE_PATH)
        except RecursionError as e:
            exception_type = type(e).__name__
            hex_color = color_map.get('exception', '#F44350')
            ansi_color = hex_to_ansi(hex_color)
            if str(e) == "maximum recursion depth exceeded":
                print(f"{ansi_color}-> File '{os.path.abspath(__file__)}', Got traceback:\n{exception_type}: Maximum recursion depth ({config.get("recursion_limit", 9999)}) exceeded\033[0m")
            else:
                print(f"{ansi_color}-> File '{os.path.abspath(__file__)}', Got traceback:\n{exception_type}: {str(e).title()}\033[0m")
        except RuntimeError as e:
            exception_type = type(e).__name__
            hex_color = color_map.get('exception', '#F44350')
            ansi_color = hex_to_ansi(hex_color)
            print(f"{ansi_color}-> File '{os.path.abspath(__file__)}', Got traceback:\n{exception_type}: {e}\033[0m")
        except Exception as e:
            exception_type = type(e).__name__
            hex_color = color_map.get('exception', '#F44350')
            ansi_color = hex_to_ansi(hex_color)
            print(f"{ansi_color}-> File '{FILE_PATH}', Got traceback:\n{exception_type}: {e}\033[0m")
    else:
        execute_file(FILE_PATH)