import os
import sys

str_ = str
int_ = int
float_ = float
range_ = range
len_ = len

def print(*args, end='\n'):
    args2 = []
    for arg in args:
        arg = str(arg)
        try:
            float_value = float(arg)
            if float_value.is_integer():
                arg = str(int(float_value))
            else:
                arg = str(float_value)
        except ValueError:
            pass
        args2.append(arg)
    sys.stdout.write(f"{' '.join(args2)}{end}")

def input(prompt=''):
    sys.stdout.write(prompt)
    return sys.stdin.readline().strip()

def len(obj):
    return len_(obj)

def str(obj):
    return str_(obj)

def int(obj):
    if not obj:
        return 0
    return int_(obj)

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


def help(config=None, command=None):
    info = {
        "print": {
            "example": "print(3.14, 'Hello', True, x + y)",
            "description": "Outputs the given arguments to the console."
        },
    }

    if command:
        if command in info:
            sys.stdout.write(f"\n{command} Command Help:\n")
            sys.stdout.write(f"   Example: {info[command]['example']}\n")
            sys.stdout.write(f"   Description: {info[command]['description']}\n\n")
        else:
            sys.stdout.write(f"Command '{command}' not found. Try another or check available commands.\n")
        return

    version = config.get("version", "version unknown")
    content = f"""
Welcome to Lucia-{version}!

If you're new to Lucia, start with the tutorial:
https://github.com/SirPigari/lucia/tree/main/env/Docs/tutorial.md

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

def clear():
    os.system("cls")

def read_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        c = file.read()
    return c