import os
import sys
import re
import time
import decimal

str_ = str
int_ = int
float_ = float
range_ = range
len_ = len
print_ = print

import sys
import decimal

def print(*args, end='\n'):
    print_(*args, end=end)



def input(prompt=''):
    sys.stdout.write(prompt)
    return sys.stdin.readline().strip()


def hex_to_ansi(hex_color, is_bg=False):
    if not hex_color or hex_color.lower() == "reset":
        return "\033[0m"

    match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
    if not match:
        return "\033[0m"

    r, g, b = tuple(int_(match.group(1)[i:i + 2], 16) for i in (0, 2, 4))

    if is_bg:
        return f"\033[48;2;{r};{g};{b}m"  # Background color
    return f"\033[38;2;{r};{g};{b}m"  # Foreground color

def wait(ms):
    if isinstance(ms, str_):
        if ms.endswith("ms"):
            ms = ms[:-2]
        elif ms.endswith("s"):
            ms = ms[:-1] + "000"
        elif ms.endswith("m"):
            ms = ms[:-1] + "000"
        else:
            raise ValueError("The time argument must be in milliseconds (ms), seconds (s), or minutes (m)")
    ms = int(ms)
    if ms < 0:
        raise ValueError("The time argument must be a non-negative number")
    time.sleep(ms / 1000)

def styled_print(text, fg_color, *, bg_color=None, bold=False, underline=False, italic=False, strikethrough=False, blink=False, reverse=False, link=None, end="\n"):
    style = hex_to_ansi(fg_color)
    if bg_color:
        style += hex_to_ansi(bg_color, is_bg=True)

    if bold:
        style += "\033[1m"
    if italic:
        style += "\033[3m"
    if underline:
        style += "\033[4m"
    if blink:
        style += "\033[5m"
    if reverse:
        style += "\033[7m"
    if strikethrough:
        style += "\033[9m"

    if link:
        text = f"[{text}]({link})"

    reset = "\033[0m"
    print(f"{style}{text}{reset}", end=end)

def len(obj):
    return len_(obj)

def declen(obj):
    if hasattr(obj, "__declen__"):
        return obj.__declen__()
    if hasattr(obj, "value"):
        if hasattr(obj.value, "__declen__"):
            return obj.value.__declen__()
    else:
        raise TypeError(f"Object of type '{type(obj).__name__}' has no 'declen'.")

def str(obj):
    return str_(obj)

def int(*args):
    if not args:
        return 0
    return int_(*args)

def float(obj):
    return float_(obj)

def range(start, stop=None, step=1):
    try:
        start, stop, step = int(start), int(stop), int(step)
    except ValueError:
        raise TypeError("Function range() takes only integers as arguments.")
    if stop is None:
        stop = start
        start = 0
    return range_(start, stop, step)

def exit():
    raise SystemExit


def help(config=None, func=None):
    info = {
        "print": {
            "example": "print(3.14, 'Hello', True, x + y)",
            "description": "Outputs the given arguments to the console."
        },
        "input": {
            "example": "input('Enter your name: ')",
            "description": "Reads a line of input from the user."
        },
        "len": {
            "example": "len([1, 2, 3])",
            "description": "Returns the number of items in an object."
        },
        "declen": {
            "example": "declen(3.14159)",
            "description": "Returns the decimal length of a float."
        },
        "wait": {
            "example": "wait(1000)",
            "description": "Pauses the program for the specified number of milliseconds."
        },
        "int": {
            "example": "int('42')",
            "description": "Converts a value to an integer."
        },
        "float": {
            "example": "float('3.14')",
            "description": "Converts a value to a float."
        },
        "str": {
            "example": "str(42)",
            "description": "Converts a value to a string."
        },
        "range": {
            "example": "range(1, 10, 2)",
            "description": "Creates a range object."
        },
        "exit": {
            "example": "exit()",
            "description": "Exits the program."
        },
        "help": {
            "example": "help('print')",
            "description": "Displays help information for a command."
        },
        "license": {
            "example": "license()",
            "description": "Displays the license information."
        },
        "numver": {
            "example": "numver()",
            "description": "Displays the version number."
        },
        "readme": {
            "example": "readme()",
            "description": "Displays the README file content."
        },
        "modules": {
            "example": "modules()",
            "description": "Displays the available modules."
        },
        "keywords": {
            "example": "keywords()",
            "description": "Displays the available keywords."
        },
        "credits": {
            "example": "credits()",
            "description": "Displays the credits information."
        },
        "version": {
            "example": "version()",
            "description": "Displays the version information."
        },
        "clear": {
            "example": "clear()",
            "description": "Clears the console."
        },
        "styledprint": {
            "example": "styledprint('Hello', '#FF5733', bold=True)",
            "description": "Prints styled text to the console."
        },
        "signature": {
            "example": "signature(function)",
            "description": "Displays the signature of a function."
        },
        "type": {
            "example": "type(variable)",
            "description": "Returns the type of an object."
        },
        "File": {
            "example": "File('path/to/file.txt')",
            "description": "Represents a file object."
        },
        "setprec": {
            "example": "setprec(2)",
            "description": "Sets the precision for decimal operations."
        },
        "getprec": {
            "example": "getprec()",
            "description": "Gets the current precision for decimal operations."
        },
        "id": {
            "example": "id(variable)",
            "description": "Returns the identity of an object."
        },
    }

    if func:
        if func in info:
            sys.stdout.write(f"{func} Function Help:\n")
            sys.stdout.write(f"   Example: {info[func]['example']}\n")
            sys.stdout.write(f"   Description: {info[func]['description']}\n\n")
        else:
            sys.stdout.write(f"Function '{func}' not found. Try another or check available functions.\n")
        return

    version = config.get("version", "version unknown")
    content = f"""
Welcome to Lucia-{version}!

If you're new to Lucia, start with the tutorial:
https://github.com/SirPigari/lucia/tree/main/env/Docs/introduction.md

- Need help? Enter 'help("{{module or function name}}")' (without the '{{}}') to get the information about module or function.
- Want to see available modules or keywords? Use 'modules()' or 'keywords()'.
- Ready to exit? Type 'exit()' to leave the Lucia REPL.

Happy coding!
"""
    sys.stdout.write(content)

def modules(config=None):
    modules_list = os.listdir(f"{config.get("home_dir", ".")}\\Lib")
    sys.stdout.write("Available modules:\n")
    for module in modules_list:
        sys.stdout.write(f" - {module}\n")
    sys.stdout.write("\n")

def keywords():
    keywords_list = [
        # Control Flow Keywords
        {"name": "Control Flow Keywords", "description": "Keywords used to control the flow of execution.", "keywords": {
            "if": "Starts a conditional statement, executing a block if the condition is true.",
            "else": "Provides an alternative block of code if the 'if' condition is false.",
            "for": "Defines a loop that iterates over a range or collection.",
            "while": "Defines a loop that runs as long as a condition is true.",
            "return": "Exits a function and optionally returns a value.",
            "forget": "Forgets the variable or function from the current scope.",
        }},

        # Function and Modifier Keywords
        {"name": "Function and Modifier Keywords", "description": "Keywords used to define functions and modify their behavior.", "keywords": {
            "fun": "Defines a function.",
            "async": "Marks a function as asynchronous.",
            "public": "Declares a function or variable as publicly accessible.",
            "private": "Restricts access to a function or variable within the same scope.",
            "static": "Indicates that a function or variable belongs to the class rather than instances.",
            "mutable": "Allows modification of a variable.",
            "final": "Prevents further modification or overriding of a function/variable.",
        }},

        # Data Type Keywords
        {"name": "Data Type Keywords", "description": "Keywords used to define data types and values.", "keywords": {
            "void": "Specifies that a function does not return a value.",
            "int": "Represents an integer type.",
            "float": "Represents a floating-point number.",
            "string": "Represents a sequence of characters.",
            "bool": "Represents a boolean value (true or false).",
            "any": "Represents a generic type that can hold any value.",
        }},

        # Logical and Boolean Keywords
        {"name": "Logical and Boolean Keywords", "description": "Keywords used for logical operations and boolean values.", "keywords": {
            "true": "Represents a boolean 'true' value.",
            "false": "Represents a boolean 'false' value.",
            "null": "Represents an absence of value.",
            "!": "Logical NOT operator, used for negation.",
        }},

        # Importing Modules
        {"name": "Importing Modules", "description": "Keywords used to import external modules.", "keywords": {
            "import": "Used to import external modules.",
            "as": "Used to rename an imported module.",
        }},
    ]

    sys.stdout.write("Available keywords:\n")
    for category in keywords_list:
        sys.stdout.write(f"\n - {category['name']}:\n")
        for keyword, description in category["keywords"].items():
            sys.stdout.write(f"   - {keyword}: {description}\n")
    sys.stdout.write("\n")


def license(config=None, full=False):
    file = open(f"{config.get('home_dir', '.')}\\..\\LICENSE", "r")
    content = file.readlines()
    line_num = 1
    cont = ""
    for line in content:
        cont += f"{line}"
        line_num += 1
        if line_num == 7:
            break
    file.close()
    if full:
        sys.stdout.write("".join(content))
    else:
        sys.stdout.write(cont)
    sys.stdout.write("\n")

def credits(config=None):
    file = open(f"{config.get('home_dir', '.')}\\CREDITS.md", "r")
    content = file.read()
    file.close()
    sys.stdout.write(content)
    sys.stdout.write("\n")

def readme(config=None):
    file = open(f"{config.get('home_dir', '.')}\\..\\README.md", "r")
    content = file.read()
    file.close()
    sys.stdout.write(content)
    sys.stdout.write("\n")

def version(config=None):
    version = config.get("version", "version unknown")
    return f"Lucia-{version}"

def numver(config):
    version = config.get("version", "version unknown")
    return version

def clear():
    os.system("cls")

def read_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        c = file.read()
    return c