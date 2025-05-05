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
    return str(" ".join(str(arg) for arg in args))



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

def exit(c=0):
    if c == 0:
        sys.exit(0)
    else:
        raise SystemExit(c)


def help(config=None, func=None):
    info = {
        "print": {
            "type": "function",
            "example": "print(3.14, 'Hello', True, x + y)",
            "description": "Outputs the given arguments to the console."
        },
        "input": {
            "type": "function",
            "example": "input('Enter your name: ')",
            "description": "Reads a line of input from the user."
        },
        "len": {
            "type": "function",
            "example": "len([1, 2, 3])",
            "description": "Returns the number of items in an object."
        },
        "declen": {
            "type": "function",
            "example": "declen(3.14159)",
            "description": "Returns the decimal length of a float."
        },
        "wait": {
            "type": "function",
            "example": "wait(1000)",
            "description": "Pauses the program for the specified number of milliseconds."
        },
        "int": {
            "type": "function",
            "example": "int('42')",
            "description": "Converts a value to an integer."
        },
        "float": {
            "type": "function",
            "example": "float('3.14')",
            "description": "Converts a value to a float."
        },
        "str": {
            "type": "function",
            "example": "str(42)",
            "description": "Converts a value to a string."
        },
        "range": {
            "type": "function",
            "example": "range(1, 10, 2)",
            "description": "Creates a range object."
        },
        "exit": {
            "type": "function",
            "example": "exit()",
            "description": "Exits the program."
        },
        "help": {
            "type": "function",
            "example": "help('print')",
            "description": "Displays help information for a command."
        },
        "license": {
            "type": "function",
            "example": "license()",
            "description": "Displays the license information."
        },
        "numver": {
            "type": "function",
            "example": "numver()",
            "description": "Displays the version number."
        },
        "readme": {
            "type": "function",
            "example": "readme()",
            "description": "Displays the README file content."
        },
        "modules": {
            "type": "function",
            "example": "modules()",
            "description": "Displays the available modules."
        },
        "keywords": {
            "type": "function",
            "example": "keywords()",
            "description": "Displays the available keywords."
        },
        "credits": {
            "type": "function",
            "example": "credits()",
            "description": "Displays the credits information."
        },
        "version": {
            "type": "function",
            "example": "version()",
            "description": "Displays the version information."
        },
        "clear": {
            "type": "function",
            "example": "clear()",
            "description": "Clears the console."
        },
        "styledprint": {
            "type": "function",
            "example": "styledprint('Hello', '#FF5733', bold=True)",
            "description": "Prints styled text to the console."
        },
        "signature": {
            "type": "function",
            "example": "signature(function)",
            "description": "Displays the signature of a function."
        },
        "type": {
            "type": "function",
            "example": "type(variable)",
            "description": "Returns the type of an object."
        },
        "File": {
            "type": "object",
            "example": "File('path/to/file.txt')",
            "description": "Represents a file object."
        },
        "setprec": {
            "type": "function",
            "example": "setprec(2)",
            "description": "Sets the precision for decimal operations."
        },
        "getprec": {
            "type": "function",
            "example": "getprec()",
            "description": "Gets the current precision for decimal operations."
        },
        "id": {
            "type": "function",
            "example": "id(variable)",
            "description": "Returns the identity of an object."
        },
        "expect": {
            "type": "function",
            "example": "expect(function_call, expected_value)",
            "description": "Checks if the function call returns the expected value."
        },
        "fetch": {
            "type": "function",
            "example": "fetch('https://api.example.com/data')",
            "description": "Fetches data from a URL."
        },
        "finalize": {
            "type": "function",
            "example": "finalize(function)",
            "description": "Finalizes a function, making it immutable."
        },

        # modules
        "config": {
            "type": "module",
            "example": "import config",
            "description": "Module for configuration management."
        },
        "config.get_config": {
            "type": "module function",
            "example": "config.get_config(key, default)",
            "description": "Retrieves the configuration value for the given key."
        },
        "config.set_config": {
            "type": "module function",
            "example": "config.set_config(key, value)",
            "description": "Sets the configuration value for the given key."
        },
        "config.save": {
            "type": "module function",
            "example": "config.save()",
            "description": "Saves the current configuration to a file."
        },
        "config.get_color": {
            "type": "module function",
            "example": "config.get_color(color)",
            "description": "Retrieves the color value for the given color key."
        },

        "math": {
            "type": "module",
            "example": "import math",
            "description": "Module for mathematical operations."
        },
        "math.sqrt": {
            "type": "module function",
            "example": "math.sqrt(16)",
            "description": "Returns the square root of a number."
        },
        "math.sin": {
            "type": "module function",
            "example": "math.sin(math.pi / 2)",
            "description": "Returns the sine of an angle in radians."
        },
        "math.cos": {
            "type": "module function",
            "example": "math.cos(math.pi)",
            "description": "Returns the cosine of an angle in radians."
        },

        "os": {
            "type": "module",
            "example": "import os",
            "description": "Module for operating system interactions."
        },
        "os.getcwd": {
            "type": "module function",
            "example": "os.getcwd()",
            "description": "Returns the current working directory."
        },
        "os.listdir": {
            "type": "module function",
            "example": "os.listdir('.')",
            "description": "Lists the files and directories in the specified path."
        },
        "os.title": {
            "type": "module function",
            "example": "os.title('My Title')",
            "description": "Sets the console window title."
        },
        "os.start": {
            "type": "module function",
            "example": "os.start('command')",
            "description": "Starts a command in the operating system."
        },

        "console": {
            "type": "module",
            "example": "import console",
            "description": "Module for console operations."
        },
        "console.overwrite": {
            "type": "module function",
            "example": "console.overwrite('Hello World')",
            "description": "Clears the current line in the terminal and prints new text."
        },
        "console.log": {
            "type": "module function",
            "example": "console.log('Hello World')",
            "description": "Standard print function alias."
        },
        "console.supports_color": {
            "type": "module function",
            "example": "console.supports_color()",
            "description": "Checks if the terminal supports colored output."
        },
        "console.debug": {
            "type": "module function",
            "example": "console.debug('Debug message')",
            "description": "Prints debug messages with configurable color."
        },
        "console.info": {
            "type": "module function",
            "example": "console.info('Info message')",
            "description": "Prints informational messages with configurable color."
        },
        "console.error": {
            "type": "module function",
            "example": "console.error('Error message')",
            "description": "Prints error messages with configurable color."
        },
        "console.fatal": {
            "type": "module function",
            "example": "console.fatal('Fatal error message')",
            "description": "Prints fatal error messages with a darkened color."
        },
        "console.warn": {
            "type": "module function",
            "example": "console.warn('Warning message')",
            "description": "Prints warning messages with configurable color."
        },
        "console.progress_bar": {
            "type": "module function",
            "example": "console.progress_bar(range(10))",
            "description": "Displays a progress bar for an iterable."
        },
        "console.styled_print": {
            "type": "module function",
            "example": "console.styled_print('Hello', '#FF5733')",
            "description": "Prints styled text with foreground and background color options."
        },
        "console.clear": {
            "type": "module function",
            "example": "console.clear()",
            "description": "Clears the terminal screen."
        },
        "console.hex_to_ansi": {
            "type": "module function",
            "example": "console.hex_to_ansi('#FF5733')",
            "description": "Converts a hex color to ANSI escape code."
        },

        "python": {
            "type": "module",
            "example": "import python",
            "description": "Module for Python-specific operations."
        },
        "python.pyexec": {
            "type": "module function",
            "example": "python.pyexec('print(42)')",
            "description": "Executes Python code in the current context."
        },
        "python.pyeval": {
            "type": "module function",
            "example": "python.pyeval('3.14')",
            "description": "Evaluates Python code and returns the result."
        },
        "python.pycompile": {
            "type": "module function",
            "example": "python.pycompile('print(42)', 'test.py', 'exec')",
            "description": "Compiles Python code into a code object."
        },
        "python.pygetattr": {
            "type": "module function",
            "example": "python.pygetattr(obj, 'attribute')",
            "description": "Gets an attribute from an object."
        },
        "python.pysetattr": {
            "type": "module function",
            "example": "python.pysetattr(obj, 'attribute', value)",
            "description": "Sets an attribute on an object."
        },
        "python.pydelattr": {
            "type": "module function",
            "example": "python.pydelattr(obj, 'attribute')",
            "description": "Deletes an attribute from an object."
        },
        "python.pyhasattr": {
            "type": "module function",
            "example": "python.pyhasattr(obj, 'attribute')",
            "description": "Checks if an object has a specific attribute."
        },
        "python.pytype": {
            "type": "module function",
            "example": "python.pytype(obj)",
            "description": "Returns the type of an object."
        },
        "python.pycall": {
            "type": "module function",
            "example": "python.pycall(obj, arg1, arg2)",
            "description": "Calls a callable object with the specified arguments."
        },
        "python.pybool": {
            "type": "module function",
            "example": "python.pybool(obj)",
            "description": "Returns the boolean value of an object."
        },
        "python.pyversion": {
            "type": "module function",
            "example": "python.pyversion()",
            "description": "Returns the current Python version."
        },

        "random": {
            "type": "module",
            "example": "import random",
            "description": "Module for generating random numbers."
        },
        "random.randint": {
            "type": "module function",
            "example": "random.randint(1, 10)",
            "description": "Returns a random integer between two specified values."
        },
        "random.choice": {
            "type": "module function",
            "example": "random.choice([1, 2, 3])",
            "description": "Returns a random element from a non-empty sequence."
        },
        "random.shuffle": {
            "type": "module function",
            "example": "random.shuffle([1, 2, 3])",
            "description": "Shuffles the elements of a list in place."
        },
        "random.seed": {
            "type": "module function",
            "example": "random.seed(42)",
            "description": "Initializes the random number generator."
        },
        "random.randbool": {
            "type": "module function",
            "example": "random.randbool(0.5)",
            "description": "Returns a random boolean value based on the specified chance."
        },
        "random.getstate": {
            "type": "module function",
            "example": "random.getstate()",
            "description": "Returns the current state of the random number generator."
        },
        "random.setstate": {
            "type": "module function",
            "example": "random.setstate(state)",
            "description": "Restores the state of the random number generator."
        },
        "random.getrandbits": {
            "type": "module function",
            "example": "random.getrandbits(8)",
            "description": "Returns an integer with the specified number of random bits."
        },
        "random.randrange": {
            "type": "module function",
            "example": "random.randrange(1, 10, 2)",
            "description": "Returns a randomly selected element from the specified range."
        },
        "random.uniform": {
            "type": "module function",
            "example": "random.uniform(1.0, 10.0)",
            "description": "Returns a random float between two specified values."
        },

        "requests": {
            "type": "module",
            "example": "import requests",
            "description": "Module for making HTTP requests."
        },
        "requests.get": {
            "type": "module function",
            "example": "requests.get('https://api.example.com')",
            "description": "Sends a GET request to the specified URL."
        },
        "requests.post": {
            "type": "module function",
            "example": "requests.post('https://api.example.com', data={'key': 'value'})",
            "description": "Sends a POST request to the specified URL."
        },
        "requests.put": {
            "type": "module function",
            "example": "requests.put('https://api.example.com', data={'key': 'value'})",
            "description": "Sends a PUT request to the specified URL."
        },
        "requests.delete": {
            "type": "module function",
            "example": "requests.delete('https://api.example.com')",
            "description": "Sends a DELETE request to the specified URL."
        },
        "requests.head": {
            "type": "module function",
            "example": "requests.head('https://api.example.com')",
            "description": "Sends a HEAD request to the specified URL."
        },
        "requests.patch": {
            "type": "module function",
            "example": "requests.patch('https://api.example.com', data={'key': 'value'})",
            "description": "Sends a PATCH request to the specified URL."
        },
        "requests.options": {
            "type": "module function",
            "example": "requests.options('https://api.example.com')",
            "description": "Sends an OPTIONS request to the specified URL."
        },
        "requests.setHeaders": {
            "type": "module function",
            "example": "requests.setHeaders({'User-Agent': 'my-app'})",
            "description": "Sets custom headers for the requests."
        },
        "requests.getHeaders": {
            "type": "module function",
            "example": "requests.getHeaders()",
            "description": "Gets the current headers for the requests."
        },
        "requests.setBaseUrl": {
            "type": "module function",
            "example": "requests.setBaseUrl('https://api.example.com')",
            "description": "Sets the base URL for the requests."
        },
        "requests.getBaseUrl": {
            "type": "module function",
            "example": "requests.getBaseUrl()",
            "description": "Gets the current base URL for the requests."
        },
        "requests.allowFetch": {
            "type": "module function",
            "example": "requests.allowFetch(true)",
            "description": "Allows fetching data from external URLs."
        },
        "requests.clearHeaders": {
            "type": "module function",
            "example": "requests.clearHeaders()",
            "description": "Clears all custom headers for the requests."
        },
        "requests.ping": {
            "type": "module function",
            "example": "requests.ping('https://api.example.com')",
            "description": "Pings the specified URL to check its availability. Returns true if reachable, false otherwise."
        },

        "time": {
            "type": "module",
            "example": "import time",
            "description": "Module for time-related operations."
        },
        "time.sleep": {
            "type": "module function",
            "example": "time.sleep(1)",
            "description": "Suspends execution for the specified number of seconds."
        },
        "time.now": {
            "type": "module function",
            "example": "time.now()",
            "description": "Returns the current local date and time."
        },
        "time.today": {
            "type": "module function",
            "example": "time.today()",
            "description": "Returns the current local date."
        },
        "time.utcnow": {
            "type": "module function",
            "example": "time.utcnow()",
            "description": "Returns the current UTC date and time."
        },
        "time.localtime": {
            "type": "module function",
            "example": "time.localtime()",
            "description": "Returns the current local time."
        },
        "time.strftime": {
            "type": "module function",
            "example": "time.strftime('%Y-%m-%d %H:%M:%S')",
            "description": "Formats a date or time according to the given format string."
        },
        "time.strptime": {
            "type": "module function",
            "example": "time.strptime('2023-10-01', '%Y-%m-%d')",
            "description": "Parses a date string according to the given format string."
        },
        "time.time": {
            "type": "module function",
            "example": "time.time()",
            "description": "Returns the current time in seconds since the epoch."
        },
        "time.mktime": {
            "type": "module function",
            "example": "time.mktime((2023, 10, 1, 0, 0, 0, 0, 0, 0))",
            "description": "Converts a time tuple to seconds since the epoch."
        },
        "time.asctime": {
            "type": "module function",
            "example": "time.asctime()",
            "description": "Converts a time tuple to a string."
        },

        "test": {
            "type": "module",
            "example": "import test",
            "description": "Module for testing operations."
        },
        "test.testAll": {
            "type": "module function",
            "example": "test.testAll()",
            "description": "Runs all tests in the test module."
        },
        "test.test": {
            "type": "module function",
            "example": "test.test()",
            "description": "Returns 0"
        },
    }

    if callable(func):
        func = getattr(func, "name", repr(func))

    if func:
        func = func.removesuffix("()")
        if func in info:
            sys.stdout.write(f"'{func}' {info[func].get("type", "Function").capitalize()} Help:\n")
            sys.stdout.write(f"   Example: {info[func]['example']}\n")
            sys.stdout.write(f"   Description: {info[func]['description']}\n")
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
    valid_modules = set()
    for m in modules_list:
        if m in ["__pycache__", "site-packages", "venv", "Builtins"]:
            continue
        module_files = os.listdir(f"{config.get('home_dir', '.')}\\Lib\\{m}")
        for f in module_files:
            if os.path.isdir(f"{config.get('home_dir', '.')}\\Lib\\{m}\\{f}"):
                continue
            if f".{f.rsplit('.', 1)[1]}" in config["lucia_file_extensions"]:
                valid_modules.add(m)
            elif f.rsplit(".", 1)[1] == "py":
                valid_modules.add(m)
    sys.stdout.write("Available modules:\n")
    valid_modules = sorted(valid_modules)
    for module in valid_modules:
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


def expect(function_call, expected_value=None):
    float = type(3.14)

    class ExpectationError(Exception):
        pass

    try:
        result = function_call

        if expected_value is None:
            return result

        def normalize_type(value):
            while hasattr(value, "value"):
                value = value.value
            if isinstance(value, float) and value.is_integer():
                return int(value)
            if isinstance(value, decimal.Decimal):
                return float(value)
            if isinstance(value, list):
                return [normalize_type(item) for item in value]
            return value

        result = normalize_type(result)
        if expected_value is not None:
            expected_value = normalize_type(expected_value)

        if expected_value == 0 and result is None:
            return True

        if expected_value is not None:
            if result != expected_value:
                raise ExpectationError(f"Expected {repr(expected_value)}, but got {repr(result)}")
        elif result is not None:
            raise ExpectationError(f"Expected no return value (null), but got {repr(result)}")
    except ExpectationError as e:
        raise ExpectationError(str(e))
    except Exception as e:
        if expected_value is not None:
            raise ValueError(f"Expected {expected_value}, but an error was raised: {str(e)}")
        else:
            print(f"Expected no error, but an error was raised: {str(e)}")


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