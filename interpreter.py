import difflib
import os
from env.Lib.Builtins import functions as b_functions
from env.Lib.Builtins import classes as b_classes
import importlib.util
import sys
import lexer
import pparser
import re
import math

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
        self.variables = {}
        self.config = config
        self.functions = {
            "print": {"is_builtin": True, "function": b_functions.print},
            "input": {"is_builtin": True, "function": b_functions.input},
            "len": {"is_builtin": True, "function": b_functions.len},
            "int": {"is_builtin": True, "function": b_functions.int},
            "float": {"is_builtin": True, "function": b_functions.float},
            "str": {"is_builtin": True, "function": b_functions.str},
        }
        self.objects = {}
        self.return_value = None

    def check_type(self, type_, expected=None, return_value=None):
        valid_types = {"int", "str", "bool", "void", "float", "any"}


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
        else:
            return type(value).__name__

    def interpret(self, statements):
        for statement in statements:
            statement: dict = dict(statement)
            if statement["type"] == "FUNCTIONDECLARATION":
                statement["is_builtin"] = False
                self.functions[statement["name"]] = statement
            elif statement["type"] == "VARIABLEDECLARATION":
                self.variables[statement["name"]] = self.evaluate(statement["value"])
            elif statement["type"] == "OPERATION":
                self.evaluate(statement)
            elif statement["type"] == "IF":
                condition = self.evaluate(statement["condition"])
                if str(condition) == "true":
                    self.interpret(statement["body"])
                elif statement.get("else_body"):
                    self.interpret(statement["else_body"])
            elif statement["type"] == "CALL":
                self.evaluate(statement)
            elif statement["type"] == "COMMENT":
                color = self.config.get("color_scheme", {}).get("comment", "#757575")
                ansi_color = hex_to_ansi(color)
                print(f"{ansi_color}<{statement["value"]}>\033[0m")
            elif statement["type"] == "PROPERTY":
                self.evaluate(statement)
            elif statement["type"] == "BOOLEAN":
                return b_classes.Boolean(statement["value"], statement["literal_value"])
            elif statement["type"] == "RETURN":
                self.return_value = self.evaluate(statement["value"])
            elif statement["type"] == "IMPORT":
                module_name = statement["module_name"]
                as_name = statement["as"]
                self.import_module(module_name, as_name)
            elif statement["type"] == "ASSIGNMENT":
                self.variables[statement["name"]] = self.evaluate(statement["value"])
            else:
                raise SyntaxError(f"Unexpected statement: {statement}")

    def evaluate(self, statement):
        if statement["type"] == "NUMBER":
            return float(statement["value"])
        elif statement["type"] == "NAMEDARG":
            return {statement["name"]: self.evaluate(statement["value"])}
        elif statement["type"] == "STRING":
            return str(statement["value"])
        elif statement["type"] == "TYPE":
            return str(statement["name"])
        elif statement["type"] == "BOOLEAN":
            return b_classes.Boolean(statement["value"], statement["literal_value"])
        elif statement["type"] == "CALL":
            name = statement["name"]
            pos_args = [self.evaluate(pos_arg) for pos_arg in statement["pos_arguments"]]
            named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                          statement["named_arguments"]}
            if name in self.functions:
                return self.call_function(name, pos_args, named_args)
            else:
                closest_match = find_closest_match(self.functions.keys(), name)
                if closest_match:
                    raise NameError(f"Name '{name}' is not defined. Did you mean: '{closest_match}'?")
                else:
                    raise NameError(f"Name '{name}' is not defined.")
        elif statement["type"] == "VARIABLE":
            if statement["name"] == "null":
                return None
            if statement["name"] not in self.variables:
                if statement["name"] in self.functions:
                    raise NameError(f"Name '{statement['name']}' is not defined. Did you mean: '{statement['name']}()'?")
                if statement["name"] in self.objects:
                    return f"<Object at {id(self.objects[statement['name']])}>"
                closest_match = find_closest_match(self.variables.keys(), statement["name"])
                if closest_match:
                    raise NameError(f"Name '{statement['name']}' is not defined. Did you mean: '{closest_match}'?")
                raise NameError(f"Name '{statement['name']}' is not defined.")
            return self.variables[statement["name"]]
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
                return left > right
            elif operator == "<":
                return left < right
            elif operator == ">=":
                return left >= right
            elif operator == "<=":
                return left <= right
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
            object_ = self.objects.get(statement["object_name"], {})
            if statement["property"]["type"] == "CALL":
                name_ = statement["property"]["name"]
                pos_args = [self.evaluate(pos_arg) for pos_arg in statement["property"]["pos_arguments"]]
                named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                              statement["property"]["named_arguments"]}
                return self.call_object_function(object_, name_, pos_args, named_args, statement["object_name"])
            elif statement["property"]["type"] == "VARIABLE":
                if not object_:
                    raise NameError(f"Object '{statement['object_name']}' is not defined.")
                if not statement["property"]["name"] in object_["variables"]:
                    closest_match = find_closest_match(object_["variables"].keys(), statement["property"]["name"])
                    if closest_match:
                        raise NameError(f"Variable '{statement['object_name']}.{statement['property']['name']}' is not defined. Did you mean: '{statement['object_name']}.{closest_match}'?")
                    raise NameError(f"Variable '{statement['object_name']}.{statement['property']['name']}' is not defined.")
                return object_.get("variables", {}).get(statement["property"]["name"], None)
        else:
            raise SyntaxError(f"Unexpected statement: {statement}")

    def import_module(self, module_name, as_name=None):
        original_module_name = as_name if as_name else module_name
        module_path = os.path.join(self.config["home_dir"], 'Lib', module_name)
        lib_dir = os.path.join(self.config["home_dir"], 'Lib')
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
                    globals_ = {**self.variables, **self.functions, "os": os, "importlib": importlib, "config": self.config, "sys": sys, "math": math}
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
        return i.return_value

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
        return_type = functions[function_name]["return_type"]
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
        return i.return_value