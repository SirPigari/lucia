import difflib
import os
from env.Lib.Builtins.new import functions as b_functions
from env.Lib.Builtins.new import classes as b_classes
from env.Lib.Builtins.new import exceptions as b_exceptions
from env.Lib.Builtins.new import variables as b_variables
import importlib.util
import sys
import lexer
import pparser
import re
import math
import random
import builtins
import warnings

false = b_classes.Boolean(False)
true = b_classes.Boolean(True)
null = b_classes.Boolean(None)

def find_closest_match(word_list, target_word):
    if not word_list:
        return None

    word_list = list(word_list)

    closest_match = difflib.get_close_matches(target_word, word_list, n=1)
    return closest_match[0] if closest_match else None

def hex_to_ansi(hex_color):
    if not hex_color or hex_color.lower() == "reset":
        return "\033[0m"

    match = re.fullmatch(r'#?([A-Fa-f0-9]{6})', hex_color)
    if not match:
        return "\033[0m"

    r, g, b = tuple(int(match.group(1)[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def get_type(value):
    type_mapping = {
        int: "int",
        str: "str",
        bool: "bool",
        float: "float",
        list: "list",
        dict: "map",
        b_classes.Boolean: "bool",
        b_classes.Object: "object",
        b_classes.Function: "function",
        b_classes.List: "list",
        b_classes.Map: "map",
    }

    if value is None:
        return "null"

    for base_type, type_name in type_mapping.items():
        if isinstance(value, base_type):
            return type_name

    return type(value).__name__


def _handle_invalid_type(type_, valid_types):
    closest_match = find_closest_match(valid_types, type_)
    if closest_match:
        raise TypeError(f"Type '{type_}' is not supported. Did you mean: '{closest_match}'?")
    raise TypeError(f"Type '{type_}' is not supported.")


class Interpreter:
    def __init__(self, config):
        self.variables = {
            "print": b_classes.Function(is_builtin=True, function=b_functions.print, name="print"),
            "input": b_classes.Function(is_builtin=True, function=b_functions.input, name="input"),
            "len": b_classes.Function(is_builtin=True, function=b_functions.len, name="len"),
            "int": b_classes.Function(is_builtin=True, function=b_functions.int, name="int"),
            "float": b_classes.Function(is_builtin=True, function=b_functions.float, name="float"),
            "str": b_classes.Function(is_builtin=True, function=b_functions.str, name="str"),
            "range": b_classes.Function(is_builtin=True, function=b_functions.range, name="range"),
            "exit": b_classes.Function(is_builtin=True, function=b_functions.exit, name="exit"),
            "help": b_classes.Function(is_builtin=True, function=lambda c=None: b_functions.help(self.config, c), name="help"),
            "license": b_classes.Function(is_builtin=True, function=lambda full=False: b_functions.license(self.config, full), name="license"),
            "readme": b_classes.Function(is_builtin=True, function=lambda: b_functions.readme(self.config), name="readme"),
            "modules": b_classes.Function(is_builtin=True, function=lambda: b_functions.modules(self.config), name="modules"),
            "credits": b_classes.Function(is_builtin=True, function=lambda: b_functions.credits(self.config), name="credits"),
            "keywords": b_classes.Function(is_builtin=True, function=b_functions.keywords, name="keywords"),
            "version": b_classes.Function(is_builtin=True, function=lambda: b_functions.version(self.config), name="version"),
            "clear": b_classes.Function(is_builtin=True, function=b_functions.clear, name="clear"),
            "File": b_classes.Object(is_builtin=True, object=b_classes.File, name="File"),
            "LuciaException": b_classes.Object(is_builtin=True, object=b_exceptions.LuciaException, name="LuciaException"),
            "ListPatternRecognitionWarning": b_classes.Object(is_builtin=True, object=b_exceptions.ListPatterRecognitionWarning, name="ListPatternRecognitionWarning"),
            "RecursionLimitWarning": b_classes.Object(is_builtin=True, object=b_exceptions.RecursionLimitWarning, name="RecursionLimitWarning"),
        }

        self.config = config
        self.return_value = b_classes.Boolean(None)
        self.is_returning = False
        self.stack = []

    def debug_log(self, *args):
        if self.config.get('debug', False):
            if self.config.get('debug_mode', 'normal') == 'normal' or self.config.get('debug_mode', 'normal') == 'full':
                print(f"{hex_to_ansi(self.config["color_scheme"].get('debug', '#434343'))}{''.join(map(str, args))}\033[0m")

    def check_type(self, type_, expected=None, return_value=None):
        valid_types = b_variables.VALID_TYPES

        types_mapping = {
            "void": "null",
            b_classes.List: "list",
            b_classes.Map: "map",
            b_classes.Function: "function",
            b_classes.Object: "object",
        }

        type_ = types_mapping.get(type_, type_)
        expected = types_mapping.get(expected, expected)

        if isinstance(type_, b_classes.Boolean):
            type_ = "bool"
        if isinstance(expected, b_classes.Boolean):
            expected = "bool"
        if isinstance(return_value, b_classes.Boolean):
            return_value = return_value.value

        if type_ == "bool" and expected == "null" and return_value == "null":
            return True

        if expected:
            if "any" in {type_, expected}:
                return True
            if expected not in valid_types or type_ not in valid_types:
                return _handle_invalid_type(expected if expected not in valid_types else type_, valid_types)

            if {type_, expected} == {"int", "float"}:
                return True

            if type_ != expected:
                raise TypeError(f"Expected type '{expected}', but got '{type_}'")

            return True

        return type_ in valid_types or _handle_invalid_type(type_, valid_types)

    def interpret(self, statements):
        for statement in statements:
            statement: dict = dict(statement)
            self.evaluate(statement)
            if self.is_returning:
                return self.return_value


    def evaluate(self, statement):
        statement_mapping = {
            # FUNCTIONS
            "FUNCTIONDECLARATION": self.handle_function_declaration,
            "CALL": self.handle_call,
            "TYPE": lambda s: str(s["name"]),

            # VARIABLES
            "VARIABLEDECLARATION": self.handle_variable_declaration,
            "STRING": lambda s: str(s["value"]),
            "NUMBER": lambda s: float(s["value"]),
            "BOOLEAN": lambda s: b_classes.Boolean(s["value"], s["literal_value"]),
            # "THROW": self.handle_throw,
            # "IF": self.handle_if_statement,
            # "FORGET": self.handle_forget,
            # "RETURN": self.handle_return,
            # "ASSIGNMENT": self.handle_assignment,
            # "OBJECTDECLARATION": self.handle_object_declaration,
            # "IMPORT": self.handle_import,
            # "COMMENT": self.handle_comment,
            # "NAMEDARG": lambda s: {s["name"]: self.evaluate(s["value"])},
            # "VARIABLE": self.handle_variable,
            # "ASSIGNMENT_INDEX": self.handle_assignment_index,
            # "ITERABLE": self.handle_iterable,
            # "INDEX": self.handle_index,
            # "FOR": self.handle_for_loop,
            # "WHILE": self.handle_while_loop,
            # "OPERATION": self.handle_operation,
            # "WITH": self.handle_with,
            # "PROPERTY": self.handle_property,
        }

        statement_type = statement["type"]
        if statement_type not in statement_mapping:
            raise SyntaxError(f"Unexpected statement: {statement}")
        handler = statement_mapping[statement_type]
        return handler(statement)

    def handle_function_declaration(self, statement):
        self.debug_log(f"<Function '{statement['name']}' declared.>")
        name = statement["name"]
        args = statement["parameters"]
        body = statement["body"]
        return_type = statement["return_type"]
        modifiers = {"is_static": statement.get("is_static", False), "is_async": statement.get("is_async", False), "is_final": statement.get("is_final", False), "is_public": statement.get("is_public", True)}
        if name in self.variables:
            fun = self.variables[name]
            if isinstance(fun, b_classes.Function):
                if fun.modifiers["is_final"]:
                    raise PermissionError(f"Function '{name}' is final and cannot be re-declared.")
            raise NameError(f"Function '{name}' is already declared.")
        self.variables[name] = b_classes.Function(name, args, body, modifiers, return_type)
        return self.variables[name]

    def handle_call(self, statement):
        if statement["name"] not in self.variables:
            closest_match = find_closest_match(self.functions.keys(), name)
            if closest_match:
                raise NameError(f"Name '{name}' is not defined. Did you mean: '{closest_match}'?")
            else:
                raise NameError(f"Name '{name}' is not defined.")
        obj = self.variables[statement["name"]]
        if isinstance(obj, b_classes.Function):
            pos_args = [self.evaluate(pos_arg) for pos_arg in statement["pos_arguments"]]
            named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                          statement["named_arguments"]}
            return self.call_function(obj, pos_args, named_args)

    def call_function(self, function, pos_args, named_args):
        name = function.name
        self.debug_log(f"<Function '{name}' called.>")
        if function.is_builtin:
            return function.function(*pos_args, **named_args)

        body = function.body
        parameters = function.parameters
        return_type = self.evaluate(function.return_type)
        self.check_type(return_type)

        total_args = len(pos_args) + len(named_args)
        required_params = [param for param in parameters if param['default_value'] is None]

        if total_args < len(required_params):
            raise TypeError(f"Expected {len(required_params)} arguments, but got {total_args}")
        if total_args > len(parameters):
            raise TypeError(
                f"{function_name}() takes from {len(required_params)} to {len(parameters)} positional arguments but {total_args} were given")

        all_args = {}

        for i, parameter in enumerate(parameters):
            param_name = parameter['name']
            param_type = parameter['variable_type']
            default_value = parameter['default_value']

            if param_name in named_args:
                if not self.check_type(self.get_type(named_args[param_name]), param_type):
                    raise TypeError(
                        f"Expected type '{param_type}' for argument '{param_name}', but got '{self.get_type(named_args[param_name])}'")
                all_args[param_name] = named_args[param_name]
            elif i < len(pos_args):
                all_args[param_name] = pos_args[i]
            elif default_value is not None:
                all_args[param_name] = default_value
            else:
                raise TypeError(f"Missing required positional argument: '{param_name}'")

        i = Interpreter(self.config)
        i.variables = {**self.variables, **all_args}  # Merge all arguments into the variables environment
        i.interpret(body)
        self.check_type(get_type(i.return_value), return_type, i.return_value)
        return b_classes.Literal(i.return_value)


    def handle_variable_declaration(self, statement):
        name = statement["name"]
        value = self.evaluate(statement["value"])
        if name in self.variables:
            raise NameError(f"Variable '{name}' is already declared.")
        self.variables[name] = value
        return self.variables[name]