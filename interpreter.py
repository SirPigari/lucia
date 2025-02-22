import difflib
import os
from env.Lib.Builtins import functions as b_functions
from env.Lib.Builtins import classes as b_classes
from env.Lib.Builtins import exceptions as b_exceptions
import importlib.util
import sys
import lexer
import pparser
import re
import math
import random
import builtins
import warnings

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


class Interpreter:
    def __init__(self, config):
        self.variables = {
            "LuciaException": b_exceptions.LuciaException,
            "ListPatternRecognitionWarning": b_exceptions.ListPatterRecognitionWarning,
            "RecursionLimitWarning": b_exceptions.RecursionLimitWarning,
        }
        self.config = config
        self.functions = {
            "print": {"is_builtin": True, "function": b_functions.print},
            "input": {"is_builtin": True, "function": b_functions.input},
            "len": {"is_builtin": True, "function": b_functions.len},
            "int": {"is_builtin": True, "function": b_functions.int},
            "float": {"is_builtin": True, "function": b_functions.float},
            "str": {"is_builtin": True, "function": b_functions.str},
            "range": {"is_builtin": True, "function": b_functions.range},
            "exit": {"is_builtin": True, "function": b_functions.exit},
            "help": {"is_builtin": True, "function": lambda c=None: b_functions.help(self.config, c)},
            "license": {"is_builtin": True, "function": lambda full=False: b_functions.license(self.config, full)},
            "readme": {"is_builtin": True, "function": lambda: b_functions.readme(self.config)},
            "modules": {"is_builtin": True, "function": lambda: b_functions.modules(self.config)},
            "credits": {"is_builtin": True, "function": lambda: b_functions.credits(self.config)},
            "keywords": {"is_builtin": True, "function": b_functions.keywords},
            "version": {"is_builtin": True, "function": lambda: b_functions.version(self.config)},
            "clear": {"is_builtin": True, "function": b_functions.clear},
        }
        self.objects = {}
        self.return_value = b_classes.Boolean(None)
        self.is_returning = False

    def debug_log(self, *args):
        if self.config.get('debug', False):
            if self.config.get('debug_mode', 'normal') == 'normal' or self.config.get('debug_mode', 'normal') == 'full':
                print(f"{hex_to_ansi(self.config["color_scheme"].get('debug', '#434343'))}{''.join(map(str, args))}\033[0m")

    def check_type(self, type_, expected=None, return_value=None):
        valid_types = {"int", "str", "bool", "void", "float", "any", "null", "list", "object"}

        if type_ == "void":
            type_ = "null"

        if expected == "void":
            expected = "null"

        if isinstance(type_, b_classes.Boolean):
            type_ = "bool"

        if isinstance(expected, b_classes.Boolean):
            expected = "bool"

        if isinstance(return_value, b_classes.Boolean):
            return_value = return_value.value

        if (type_ == "bool") and (expected == "void") and (return_value == "null"):
            return True

        if expected:
            if type_ == "any":
                return True
            if expected == "any":
                return True
            if expected not in valid_types:
                return self._handle_invalid_type(expected, valid_types)
            if type_ not in valid_types:
                return self._handle_invalid_type(type_, valid_types)

            if expected == "int" and type_ == "float":
                return True

            if expected == "float" and type_ == "int":
                return True

            if type_ != expected:
                raise TypeError(f"Expected type '{expected}', but got '{type_}'")

            return True

        if type_ in valid_types:
            return True

        self._handle_invalid_type(type_, valid_types)

    def _handle_invalid_type(self, type_, valid_types):
        closest_match = find_closest_match(valid_types, type_)
        if closest_match:
            raise TypeError(f"Type '{type_}' is not supported. Did you mean: '{closest_match}'?")
        raise TypeError(f"Type '{type_}' is not supported.")

    def get_type(self, value):
        if isinstance(value, int):
            return "int"
        elif isinstance(value, str):
            return "str"
        elif isinstance(value, bool):
            return "bool"
        elif value is None:
            return "null"
        elif isinstance(value, b_classes.Boolean):
            return "bool"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, list):
            return "list"
        else:
            return type(value).__name__

    def interpret(self, statements):
        for statement in statements:
            statement: dict = dict(statement)
            self.evaluate(statement)
            if self.is_returning:
                return self.return_value

    def evaluate(self, statement):
        if statement["type"] == "FUNCTIONDECLARATION":
            self.debug_log(f"<Function '{statement['name']}' declared.>")
            statement["is_builtin"] = False
            if (statement["name"] in self.functions) and statement["is_final"]:
                raise SyntaxError(f"Function '{statement['name']}' is already defined.")
            self.functions[statement["name"]] = statement
        elif statement["type"] == "VARIABLEDECLARATION":
            self.debug_log(f"<Variable '{statement['name']}' declared.>")
            self.variables[statement["name"]] = self.evaluate(statement["value"])
        elif statement["type"] == "NUMBER":
            return float(statement["value"])
        elif statement["type"] == "THROW":
            if statement["from"]["name"] in self.variables:
                exception = self.variables.get(statement["from"]["name"], statement["from"])
            elif hasattr(builtins, statement["from"]["name"]):
                exception = getattr(builtins, statement["from"]["name"])
            else:
                raise NameError(f"Name '{statement['from']['name']}' is not defined.")
            raise exception(self.evaluate(statement["value"]))
        elif statement["type"] == "IF":
            condition = self.evaluate(statement["condition"])
            if str(condition) == "true":
                self.interpret(statement["body"])
            elif statement.get("else_body"):
                self.interpret(statement["else_body"])
        elif statement["type"] == "FORGET":
            if statement["name"] in self.variables:
                del self.variables[statement["name"]]
            elif statement["name"] in self.functions:
                del self.functions[statement["name"]]
            elif statement["name"] in self.objects:
                del self.objects[statement["name"]]
            else:
                closest_match = find_closest_match(self.variables.keys(), statement["name"])
                if closest_match:
                    raise NameError(f"Name '{statement['name']}' is not defined. Did you mean: '{closest_match}'?")
                raise NameError(f"Name '{statement['name']}' is not defined.")
        elif statement["type"] == "RETURN":
            self.return_value = self.evaluate(statement["value"])
            self.debug_log(f"<Function returned '{self.return_value}'>")
            self.is_returning = True
            return self.return_value
        elif statement["type"] == "ASSIGNMENT":
            self.variables[statement["name"]] = self.evaluate(statement["value"])
            self.debug_log(f"<Variable '{statement['name']}' assigned to '{self.variables[statement['name']]}'")
        elif statement["type"] == "OBJECTDECLARATION":
            name = statement["name"]
            self.debug_log(f"<Object '{name}' declared>")
            self.objects[name] = {"functions": {}, "variables": {}}
            for function in statement["functions"]:
                function["is_builtin"] = False
                self.objects[name]["functions"][function["name"]] = function
            for variable in statement["variables"]:
                self.objects[name]["variables"][variable["name"]] = variable["value"]
            self.objects[name]["init"] = statement["init"]
        elif statement["type"] == "IMPORT":
            module_name = statement["module_name"]
            as_name = statement["as"]
            from_ = None if (statement["from"] is None) else self.evaluate(statement["from"])
            self.debug_log(f"<Module '{module_name}' imported from '{os.path.abspath(from_)}' as '{as_name}'>")
            self.import_module(module_name, as_name, from_)
        elif statement["type"] == "COMMENT":
            color = self.config.get("color_scheme", {}).get("comment", "#757575")
            ansi_color = hex_to_ansi(color)
            print(f"{ansi_color}<{statement["value"]}>\033[0m")
        elif statement["type"] == "NAMEDARG":
            return {statement["name"]: self.evaluate(statement["value"])}
        elif statement["type"] == "STRING":
            return str(statement["value"])
        elif statement["type"] == "TYPE":
            return str(statement["name"])
        elif statement["type"] == "BOOLEAN":
            return b_classes.Boolean(statement["value"], statement["literal_value"])
        elif statement["type"] == "CALL":
            self.debug_log(f"<Function '{statement['name']}' called>")
            name = statement["name"]
            pos_args = [self.evaluate(pos_arg) for pos_arg in statement["pos_arguments"]]
            named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                          statement["named_arguments"]}
            if name in self.functions:
                return self.call_function(name, pos_args, named_args)
            elif name in self.objects:
                return self.call_object_assignment(self.objects[name], statement["name"], pos_args, named_args, name)
            else:
                closest_match = find_closest_match(self.functions.keys(), name)
                if closest_match:
                    raise NameError(f"Name '{name}' is not defined. Did you mean: '{closest_match}'?")
                else:
                    raise NameError(f"Name '{name}' is not defined.")
        elif statement["type"] == "VARIABLE":
            self.debug_log(f"<Variable '{statement['name']}' accessed>")
            if statement["name"] == "null":
                return None
            if statement["name"] not in self.variables:
                if statement["name"] in self.functions:
                    raise NameError(f"Name '{statement['name']}' is not defined. Did you mean: '{statement['name']}()'?")
                if statement["name"] in self.objects:
                    if "STR" in self.objects[statement["name"]]["functions"]:
                        return b_classes.Object(self.variables[name], custom_str=str(
                            self.call_object_function(self.objects[statement["name"]], "STR", [], {}, self.objects[statement["name"]])))
                    return f"<object '__main__.{statement['name']}' at {id(self.objects[statement['name']])}>"
                closest_match = find_closest_match(self.variables.keys(), statement["name"])
                if closest_match:
                    raise NameError(f"Name '{statement['name']}' is not defined. Did you mean: '{closest_match}'?")
                raise NameError(f"Name '{statement['name']}' is not defined.")
            return self.variables[statement["name"]]
        elif statement["type"] == "ITERABLE":
            if statement["iterable_type"] == "LIST":
                l = []
                for element in statement["elements"]:
                    l.append(self.evaluate(element))
                return l
            elif statement["iterable_type"] == "LIST_COMPLETION":
                pattern = statement["pattern"]
                end = self.evaluate(statement["end"])

                pattern_values = [self.evaluate(p) for p in pattern]

                if len(pattern_values) == 1:
                    return range(int(pattern_values[0]), int(end)+1)

                differences = [pattern_values[i + 1] - pattern_values[i] for i in range(len(pattern_values) - 1)]

                if differences:
                    if all(d == differences[0] for d in differences):
                        step = differences[0]
                        start = pattern_values[0]
                        result = []
                        current = start

                        while current <= end:
                            result.append(current)
                            current += step

                        return result

                elif len(pattern_values) >= 2:
                    fibonacci_like = True
                    for i in range(len(pattern_values) - 2):
                        if pattern_values[i] + pattern_values[i + 1] != pattern_values[i + 2]:
                            fibonacci_like = False
                            break

                    if fibonacci_like:
                        start1, start2 = pattern_values[0], pattern_values[1]
                        result = [start1, start2]
                        while result[-1] <= end:
                            result.append(result[-2] + result[-1])

                        return result

                if self.config.get("warnings", True):
                    warnings.warn(f"List pattern was not recognized: {pattern_values}", b_exceptions.ListPatterRecognitionWarning)
                else:
                    return pattern_values + [end]
            else:
                raise SyntaxError(f"Unexpected iterable type: {statement['iterable_type']}")
        elif statement["type"] == "FOR":
            variable = statement["variable_name"]
            iterable = self.evaluate(statement["iterable"])
            for element in iterable:
                self.variables[variable] = element
                self.interpret(statement["body"])
        elif statement["type"] == "WHILE":
            condition = self.evaluate(statement["condition"])
            while b_classes.Boolean(condition).literal:
                result = self.interpret(statement["body"])
                condition = self.evaluate(statement["condition"])
        elif statement["type"] == "OPERATION":
            left = self.evaluate(statement["left"])
            right = self.evaluate(statement["right"])
            operator = statement["operator"]
            if operator == "+":
                return left + right
            elif operator == "-":
                return left - right
            elif operator == "*":
                return left * right
            elif operator == "/":
                return left / right
            elif operator == "^":
                return left ** right
            elif operator == "==":
                return b_classes.Boolean(left == right, left == right)
            elif operator == ">":
                return b_classes.Boolean(left > right)
            elif operator == "<":
                return b_classes.Boolean(left < right)
            elif operator == ">=":
                return b_classes.Boolean(left >= right)
            elif operator == "<=":
                return b_classes.Boolean(left <= right)
            elif operator == "!=":
                return b_classes.Boolean(left != right, left != right)
            elif operator == "&&":
                return b_classes.Boolean(left and right, left and right)
            elif operator == "||":
                return b_classes.Boolean(left or right, left or right)
            elif operator == "!":
                return b_classes.Boolean(not right, not right)
            else:
                raise SyntaxError(f"Unexpected operator: {operator}")
        elif statement["type"] == "PROPERTY":
            object_ = {}
            if statement["object_name"] in self.variables:
                object_ = self.variables[statement["object_name"]]
            elif statement["object_name"] in self.objects:
                object_ = self.objects[statement["object_name"]]
            elif hasattr(builtins, statement["object_name"]):
                object_ = getattr(builtins, statement["object_name"])
            else:
                raise NameError(f"Object '{statement['object_name']}' is not defined.")

            if statement["property"]["type"] == "CALL":
                self.debug_log(f"<Property '{statement['object_name']}.{statement['property']['name']}' called>")
                name_ = statement["property"]["name"]
                pos_args = [self.evaluate(pos_arg) for pos_arg in statement["property"]["pos_arguments"]]
                named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                              statement["property"]["named_arguments"]}
                return self.call_object_function(object_, name_, pos_args, named_args, statement["object_name"])
            elif statement["property"]["type"] == "VARIABLE":
                self.debug_log(f"<Property '{statement['object_name']}.{statement['property']['name']}' accessed>")
                if not isinstance(object_, dict):
                    object_ = dict(object_)
                if not object_:
                    raise NameError(f"Object '{statement['object_name']}' is not defined.")
                if statement["property"]["name"] in object_["variables"]:
                    return object_.get("variables", {}).get(statement["property"]["name"], b_classes.Boolean(None))
                elif statement["property"]["name"] in object_["functions"]:
                    return b_classes.Function(f"{statement["object_name"]}.{statement["property"]["name"]}", object_.get("functions", {}).get(statement["property"]["name"], b_classes.Boolean(None)))
                closest_match = find_closest_match(object_["variables"].keys(), statement["property"]["name"])
                if closest_match:
                    raise NameError(f"Variable '{statement['object_name']}.{statement['property']['name']}' is not defined. Did you mean: '{statement['object_name']}.{closest_match}'?")
                raise NameError(f"Variable '{statement['object_name']}.{statement['property']['name']}' is not defined.")
            else:
                raise SyntaxError(f"Unexpected property type: {statement['property']['type']}")
        else:
            raise SyntaxError(f"Unexpected statement: {statement}")

    def import_module(self, module_name, as_name=None, from_=None):
        original_module_name = as_name if as_name else module_name
        from_ = os.path.abspath(from_ or os.path.join(self.config.get("home_dir"), "Lib"))
        if not os.path.exists(from_):
            raise ImportError(f"Path '{from_}' does not exist.")
        module_path = os.path.join(from_, module_name)
        lib_dir = os.path.join(from_)
        module_files = os.listdir(module_path)

        if os.path.isdir(module_path):
            module_name = os.path.basename(module_name)
            module_files = os.listdir(module_path)

            if "__init__.lucia" in module_files:
                module_files.remove("__init__.lucia")
                module_files.insert(0, "__init__.lucia")
            if "__init__.py" in module_files:
                module_files.remove("__init__.py")
                module_files.insert(0, "__init__.py")

            for module in module_files:
                if f".{module.rsplit('.', 1)[1]}" in self.config["lucia_file_extensions"]:
                    with open(os.path.join(lib_dir, module_name, module), 'r', encoding='utf-8') as file:
                        code = file.read()
                    tokens = lexer.lexer(code, include_comments=self.config.get('print_comments', False))
                    parser = pparser.Parser(tokens)
                    parser.parse()
                    interpreter = Interpreter(self.config)
                    interpreter.interpret(parser.statements)

                    functions_to_update = {}
                    for f in interpreter.functions:
                        if interpreter.functions[f]["is_builtin"]:
                            functions_to_update[f] = interpreter.functions[f]
                        elif interpreter.functions[f]["is_public"]:
                            functions_to_update[f] = interpreter.functions[f]

                    alias_to_use = as_name or module_name
                    if not alias_to_use in self.objects:
                        self.objects[alias_to_use] = {"functions": {}, "variables": {}}
                    self.objects[alias_to_use]["functions"].update(functions_to_update)
                    self.objects[alias_to_use]["variables"].update(interpreter.variables)
                elif module.rsplit(".", 1)[1] == "py":
                    with open(os.path.join(lib_dir, module_name, module), 'r', encoding='utf-8') as file:
                        code = file.read()
                    globals_ = {**self.variables, **self.functions, "os": os, "importlib": importlib, "config": self.config, "sys": sys, "math": math, "random": random}
                    locals_ = {}
                    module_spec = importlib.util.spec_from_file_location(original_module_name, module_path)

                    if module_spec and module_spec.loader:
                        imported_module = importlib.util.module_from_spec(module_spec)
                        module_spec.loader.exec_module(imported_module)
                    exec(code, globals_, locals_)

                    functions_from_locals_ = {name: func for name, func in locals_.items() if callable(func)}
                    alias_to_use = as_name or module_name
                    if not alias_to_use in self.objects:
                        self.objects[alias_to_use] = {"functions": {}, "variables": {}}

                    for f in functions_from_locals_:
                        self.objects[alias_to_use]["functions"][f] = {"is_builtin": True,
                                                                      "function": functions_from_locals_[f]}

                    variables_from_locals_ = {name: value for name, value in locals_.items() if not callable(value)}
                    self.objects[alias_to_use]["variables"].update(variables_from_locals_)

        else:
            closest_match = find_closest_match(module_files, module_name)
            if closest_match:
                raise ImportError(f"No module named '{original_module_name}'. Did you mean: '{closest_match}'?")
            raise ImportError(f"No module named '{original_module_name}'.")

    def call_function(self, function_name, pos_args, named_args):
        if self.functions[function_name]["is_builtin"]:
            return self.functions[function_name]["function"](*pos_args, **named_args)

        body = self.functions[function_name]["body"]
        parameters = self.functions[function_name]["parameters"]
        return_type = self.evaluate(self.functions[function_name]["return_type"])
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
        i.functions = self.functions
        i.objects = self.objects
        i.interpret(body)
        self.check_type(self.get_type(i.return_value), return_type, i.return_value)
        return b_classes.Literal(i.return_value)

    def call_object_function(self, object_, function_name, pos_args, named_args, object_name=None):
        if not object_:
            raise NameError(f"Object '{object_name}' is not defined.")
        functions = object_["functions"]
        if not function_name in functions:
            closest_match = find_closest_match(functions.keys(), function_name)
            if closest_match:
                raise NameError(f"Function '{object_name}.{function_name}' is not defined. Did you mean: '{object_name}.{closest_match}'?")
            raise NameError(f"Function '{function_name}' is not defined.")
        if functions[function_name]["is_builtin"]:
            return functions[function_name]["function"](*pos_args, **named_args)

        body = functions[function_name]["body"]
        parameters = functions[function_name]["parameters"]
        return_type = self.evaluate(functions[function_name]["return_type"])
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
        i.functions = self.functions
        i.objects = self.objects
        i.interpret(body)
        return b_classes.Literal(i.return_value)

    def call_object_assignment(self, object_, name, pos_args, named_args, object_name=None):
        if not object_["init"]:
            if pos_args or named_args:
                raise TypeError(
                    f"Object {name}() takes from 0 positional arguments but {len(pos_args) + len(named_args)} were given")
            else:
                self.variables[name] = object_
                return b_classes.Object(self.variables[name])
        elif object_["init"]:
            self.debug_log(f"<Function '{name}.init' called>")
            body = object_["init"]["body"]
            parameters = object_["init"]["parameters"]

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
            i.variables = {**self.variables, **all_args, "this": object_}  # Merge all arguments into the variables environment
            i.functions = self.functions
            i.objects = self.objects
            i.interpret(body)
            for f in i.functions.keys():
                if (not i.functions[f]["is_builtin"]) and i.functions[f]["is_static"]:
                    object_["functions"][f] = i.functions[f]
                elif i.functions[f]["is_builtin"]:
                    object_["functions"][f] = i.functions[f]
                elif (not i.functions[f]["is_builtin"]) and (not i.functions[f]["is_static"]):
                    object_["functions"][f] = i.functions[f]
                    self.objects[name]["functions"][f] = i.functions[f]
            object_["variables"] = i.variables
            self.variables[name] = object_
            if "STR" in object_["functions"]:
                return b_classes.Object(self.variables[name], custom_str=str(self.call_object_function(object_, "STR", [], {}, object_name)))
            return b_classes.Object(self.variables[name])