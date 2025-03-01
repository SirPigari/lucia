import difflib
import os
from env.Lib.Builtins import functions as b_functions
from env.Lib.Builtins import classes as b_classes
from env.Lib.Builtins import exceptions as b_exceptions
from env.Lib.Builtins import variables as b_variables
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

    if isinstance(value, b_classes.Variable):
        return get_type(value.value)

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

def warn(message, category, stacklevel=3):
    if config.get('warnings', True):
        if config.get('use_lucia_traceback', True):
            print(
                f"{hex_to_ansi(color_map.get('warning', '#FFC107'))}-> File '{__file__}', warning:\n{category}: {message}\033[0m")
        else:
            warnings.warn(message, category, stacklevel=stacklevel)


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
            "TestContext": b_classes.Object(is_builtin=True, object=b_classes.TestContext, name="TestContext"),
        }

        self.config = config
        self.return_value = b_classes.Boolean(None)
        self.is_returning = False
        self.stack = []

    def check_stack(self):
        stack_len = len(self.stack)
        max_recursion = self.config.get('recursion_limit', 9999)
        if stack_len > max_recursion:
            raise RecursionError(f"Maximum recursion depth exceeded. (Max: {max_recursion}, Current: {stack_len})")
        if stack_len == max_recursion:
            warn("Recursion limit reached.", b_exceptions.RecursionLimitWarning)

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

            if {type_, expected} == {"int", "bool"}:
                if return_value in {0, 1, "null"}:
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
            "RETURN": self.handle_return,
            "TYPE": lambda s: str(s["name"]),

            # VARIABLES
            "VARIABLEDECLARATION": self.handle_variable_declaration,
            "STRING": lambda s: str(s["value"]),
            "NUMBER": lambda s: float(s["value"]),
            "BOOLEAN": lambda s: b_classes.Boolean(s["value"], s["literal_value"]),
            "VARIABLE": self.handle_variable,
            "ASSIGNMENT": self.handle_assignment,
            "OPERATION": self.handle_operation,
            "ITERABLE": self.handle_iterable,

            # STATEMENTS
            "THROW": self.handle_throw,
            "IF": self.handle_if_statement,
            "FORGET": self.handle_forget,
            "FOR": self.handle_for_loop,
            "WHILE": self.handle_while_loop,
            "WITH": self.handle_with,
            "IMPORT": self.handle_import,

            # OBJECTS
            "PROPERTY": self.handle_property,
            "OBJECTDECLARATION": self.handle_object_declaration,

            # OTHER
            "COMMENT": self.handle_comment,
            "NAMEDARG": lambda s: {s["name"]: self.evaluate(s["value"])},
            "ASSIGNMENT_INDEX": self.handle_assignment_index,
            "INDEX": self.handle_index,
        }

        if not isinstance(statement, dict):
            print(statement)
            raise SyntaxError(f"Unexpected statement: {statement}")
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
        self.check_stack()
        if statement["name"] not in self.variables:
            closest_match = find_closest_match(self.variables.keys(), statement["name"])
            if closest_match:
                raise NameError(f"Name '{statement["name"]}' is not defined. Did you mean: '{closest_match}'?")
            else:
                raise NameError(f"Name '{statement["name"]}' is not defined.")
        obj = self.variables[statement["name"]]
        if isinstance(obj, b_classes.Function):
            pos_args = [self.evaluate(pos_arg) for pos_arg in statement["pos_arguments"]]
            named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                          statement["named_arguments"]}
            return self.call_function(obj, pos_args, named_args)
        elif isinstance(obj, b_classes.Object):
            pos_args = [self.evaluate(pos_arg) for pos_arg in statement["pos_arguments"]]
            named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                          statement["named_arguments"]}
            return self.call_object_declaration(obj, pos_args, named_args)
        elif isinstance(obj, b_classes.Variable):
            if isinstance(obj.value, b_classes.Function):
                pos_args = [self.evaluate(pos_arg) for pos_arg in statement["pos_arguments"]]
                named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                              statement["named_arguments"]}
                return self.call_function(obj.value, pos_args, named_args, custom_name=statement["name"])
            elif isinstance(obj.value, b_classes.Object):
                pos_args = [self.evaluate(pos_arg) for pos_arg in statement["pos_arguments"]]
                named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                              statement["named_arguments"]}
                return self.call_object_declaration(obj.value, pos_args, named_args, custom_name=statement["name"])
            else:
                raise TypeError(f"Object '{obj.name}' is not callable.")
        else:
            raise TypeError(f"Object '{obj.name}' is not callable.")

    def call_function(self, function, pos_args, named_args, custom_name=None):
        name = f"'{function.name}'"
        if custom_name:
            name = f"'{custom_name}' (reassigned from '{function.name}')"
        self.debug_log(f"<Function {name} called.>")
        if function.is_builtin:
            self.stack.append({"name": name, "variables": self.variables, "return_value": self.return_value,
                               "is_returning": self.is_returning})
            self.check_stack()
            ret = function.function(*pos_args, **named_args)
            self.stack.pop()
            return ret

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
        self.stack.append({"name": name, "variables": i.variables, "return_value": i.return_value,
                           "is_returning": i.is_returning})
        self.check_stack()
        i.stack = self.stack
        i.interpret(body)
        self.check_type(get_type(i.return_value), return_type, i.return_value)
        self.variables = self.stack[-1]["variables"]
        self.return_value = self.stack[-1]["return_value"]
        self.is_returning = self.stack[-1]["is_returning"]
        self.stack.pop()
        return b_classes.Literal(i.return_value)

    def handle_return(self, statement):
        return_value = self.evaluate(statement["value"])
        if not self.stack:
            raise ValueError("Stack is empty, unable to access previous function context.")
        self.debug_log(f"<Function {self.stack[-1].get("name", null)} returned {return_value}>")
        self.is_returning = True
        self.return_value = return_value
        return self.return_value

    def handle_variable_declaration(self, statement):
        type = self.evaluate(statement["variable_type"])
        value = self.evaluate(statement["value"])
        self.check_type(type)
        self.debug_log(f"<Variable '{statement['name']}' declared.>")
        self.variables[statement["name"]] = b_classes.Variable(statement["name"], value)
        return self.variables[statement["name"]]

    def handle_variable(self, statement):
        name = statement["name"]
        if name not in self.variables:
            closest_match = find_closest_match(self.variables.keys(), name)
            if closest_match:
                raise NameError(f"Name '{name}' is not defined. Did you mean: '{closest_match}'?")
            else:
                raise NameError(f"Name '{name}' is not defined.")
        return self.variables[name]

    def handle_assignment(self, statement):
        name = statement["name"]
        if name not in self.variables:
            self.variables[name] = b_classes.Variable(name, self.evaluate(statement["value"]))
        value = self.evaluate(statement["value"])
        self.debug_log(f"<Variable '{name}' assigned to {value}>")
        if isinstance(self.variables[name], b_classes.Variable):
            self.variables[name].value = value
        else:
            self.variables[name] = b_classes.Variable(name, value)
        return self.variables[name]

    def handle_operation(self, statement):
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
        elif operator == "%":
            return left % right
        elif operator == "==":
            return b_classes.Boolean(left == right)
        elif operator == ">":
            return b_classes.Boolean(left > right)
        elif operator == "<":
            return b_classes.Boolean(left < right)
        elif operator == ">=":
            return b_classes.Boolean(left >= right)
        elif operator == "<=":
            return b_classes.Boolean(left <= right)
        elif operator == "!=":
            return b_classes.Boolean(left != right)
        elif operator == "&&":
            return b_classes.Boolean(left and right)
        elif operator == "||":
            return b_classes.Boolean(left or right)
        elif operator == "!":
            return b_classes.Boolean(not right)
        elif operator == "+=":
            if not isinstance(left, b_classes.Variable):
                raise TypeError(f"Cannot assign to non-variable '{left}'")
            left.value += right
            return left
        elif operator == "-=":
            if not isinstance(left, b_classes.Variable):
                raise TypeError(f"Cannot assign to non-variable '{left}'")
            left.value -= right
            return left
        elif operator == "*=":
            if not isinstance(left, b_classes.Variable):
                raise TypeError(f"Cannot assign to non-variable '{left}'")
            left.value *= right
            return left
        elif operator == "/=":
            if not isinstance(left, b_classes.Variable):
                raise TypeError(f"Cannot assign to non-variable '{left}'")
            left.value /= right
            return left
        else:
            raise SyntaxError(f"Unexpected operator: {operator}")

    def handle_iterable(self, statement):
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
                return b_classes.List(range(int(pattern_values[0]), int(end) + 1))

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

                    return b_classes.List(result)

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

                    return b_classes.List(result)

            if self.config.get("warnings", True):
                warnings.warn(f"List pattern was not recognized: {pattern_values}",
                              b_exceptions.ListPatterRecognitionWarning)
            else:
                return b_classes.List(pattern_values + [end])
        elif statement["iterable_type"] == "MAP":
            map_ = {}
            keys = statement["keys"]
            values = statement["values"]
            for i, key in enumerate(keys):
                map_[self.evaluate(key)] = self.evaluate(values[i])
            return b_classes.Map({self.evaluate(key): self.evaluate(value) for key, value in zip(keys, values)})
        else:
            raise SyntaxError(f"Unexpected iterable type: {statement['iterable_type']}")

    def handle_throw(self, statement):
        self.debug_log(f"<Exception thrown: {statement["from"]["name"]}>")
        if statement["from"]["name"] in self.variables:
            if isinstance(self.variables[statement["from"]["name"]], b_classes.Function):
                exception = self.variables[statement["from"]["name"]].function
            elif isinstance(self.variables[statement["from"]["name"]], b_classes.Object):
                exception = self.variables[statement["from"]["name"]].object
            else:
                exception = self.variables.get(statement["from"]["name"], statement["from"])
        elif hasattr(builtins, statement["from"]["name"]):
            exception = getattr(builtins, statement["from"]["name"])
        else:
            raise NameError(f"Name '{statement['from']['name']}' is not defined.")
        raise exception(self.evaluate(statement["value"]))

    def handle_if_statement(self, statement):
        condition = self.evaluate(statement["condition"])
        self.debug_log(f"<If statement with condition {condition}>")
        if condition == true:
            self.debug_log(f"<If statement is true>")
            self.interpret(statement["body"])
        elif statement.get("else_body"):
            self.debug_log(f"<Else statement is {condition}>")
            self.interpret(statement["else_body"])

    def handle_forget(self, statement):
        if statement["name"] not in self.variables:
            closest_match = find_closest_match(self.variables.keys(), statement["name"])
            if closest_match:
                raise NameError(f"Name '{statement["name"]}' is not defined. Did you mean: '{closest_match}'?")
            else:
                raise NameError(f"Name '{statement["name"]}' is not defined.")
        del self.variables[statement["name"]]

    def handle_for_loop(self, statement):
        variable = statement["variable_name"]
        iterable = list(self.evaluate(statement["iterable"]))
        self.debug_log(f"<For loop with variable {variable} and iterable {iterable}>")
        for element in iterable:
            self.variables[variable] = b_classes.Variable(variable, element)
            self.interpret(statement["body"])

    def handle_while_loop(self, statement):
        condition = self.evaluate(statement["condition"])
        while condition == true:
            self.debug_log(f"<While loop with condition {condition}>")
            self.interpret(statement["body"])
            condition = self.evaluate(statement["condition"])

    def handle_with(self, statement):
        self.debug_log(f"<With statement with context {statement["with"]}>")
        with self.evaluate(statement["with"]) as obj:
            self.variables[statement["as"]] = obj
            self.interpret(statement["body"])

    def handle_import(self, statement):
        module_name = statement["module_name"]
        as_name = statement["as"]
        from_ = None if (statement["from"] is None) else self.evaluate(statement["from"])
        self.debug_log(f"<Module '{module_name}' imported from '{os.path.abspath(from_)}' as '{as_name}'>")
        return self.import_module(module_name, as_name, from_)

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

                    variables_to_update = {}
                    for f in interpreter.variables:
                        if isinstance(interpreter.variables[f], b_classes.Function):
                            if interpreter.variables[f].is_builtin:
                                variables_to_update[f] = interpreter.variables[f]
                            elif interpreter.variables[f].modifiers["is_public"]:
                                variables_to_update[f] = interpreter.variables[f]
                        elif isinstance(interpreter.variables[f], b_classes.Variable):
                            variables_to_update[f] = interpreter.variables[f]
                        elif isinstance(interpreter.variables[f], b_classes.Object):
                            variables_to_update[f] = interpreter.variables[f]
                        else:
                            raise TypeError(f"Object '{f}' is not supported.")

                    alias_to_use = as_name or module_name
                    if not alias_to_use in self.variables:
                        self.variables[alias_to_use] = b_classes.Object(name=alias_to_use)
                    self.variables[alias_to_use]._data.update(variables_to_update)
                elif module.rsplit(".", 1)[1] == "py":
                    with open(os.path.join(lib_dir, module_name, module), 'r', encoding='utf-8') as file:
                        code = file.read()
                    variables_to_globals = {}
                    for v in self.variables:
                        if isinstance(self.variables[v], b_classes.Variable):
                            variables_to_globals[v] = self.variables[v].value
                        elif isinstance(self.variables[v], b_classes.Object):
                            variables_to_globals[v] = self.variables[v]
                        elif isinstance(self.variables[v], b_classes.Function):
                            if self.variables[v].is_builtin:
                                variables_to_globals[v] = self.variables[v].function
                        else:
                            raise TypeError(f"Object '{v}' is not supported.")
                    globals_ = {**self.variables, "os": os, "importlib": importlib, "config": self.config, "sys": sys, "math": math, "random": random}
                    locals_ = {}
                    module_spec = importlib.util.spec_from_file_location(original_module_name, module_path)

                    if module_spec and module_spec.loader:
                        imported_module = importlib.util.module_from_spec(module_spec)
                        module_spec.loader.exec_module(imported_module)
                    exec(code, globals_, locals_)

                    functions_from_locals_ = {name: func for name, func in locals_.items() if callable(func)}
                    alias_to_use = as_name or module_name
                    if not alias_to_use in self.variables:
                        self.variables[alias_to_use] = b_classes.Object(name=alias_to_use)

                    for f in functions_from_locals_:
                        self.variables[alias_to_use]._data[f] = b_classes.Function(is_builtin=True, function=functions_from_locals_[f], name=f)

                    variables_from_locals_ = {name: value for name, value in locals_.items() if not callable(value)}
                    self.variables[alias_to_use]._data.update(variables_from_locals_)

        else:
            closest_match = find_closest_match(module_files, module_name)
            if closest_match:
                raise ImportError(f"No module named '{original_module_name}'. Did you mean: '{closest_match}'?")
            raise ImportError(f"No module named '{original_module_name}'.")

    def handle_property(self, statement):
        if not statement["object_name"] in self.variables:
            closest_match = find_closest_match(self.variables.keys(), statement["object_name"])
            if closest_match:
                raise NameError(f"Object '{statement['object_name']}' is not defined. Did you mean: '{closest_match}'?")
            raise NameError(f"Object '{statement['object_name']}' is not defined.")

        object_ = self.variables[statement["object_name"]]

        if statement["property"]["type"] == "CALL":
            self.debug_log(f"<Property '{statement['object_name']}.{statement['property']['name']}' called>")
            name_ = statement["property"]["name"]
            pos_args = [self.evaluate(pos_arg) for pos_arg in statement["property"]["pos_arguments"]]
            named_args = {named_arg["name"]: self.evaluate(named_arg["value"]) for named_arg in
                          statement["property"]["named_arguments"]}
            return self.call_object_function(object_, name_, pos_args, named_args, statement["object_name"])
        elif statement["property"]["type"] == "VARIABLE":
            self.debug_log(f"<Property '{statement['object_name']}.{statement['property']['name']}' accessed>")
            if not object_:
                raise NameError(f"Object '{statement['object_name']}' is not defined.")
            if statement["property"]["name"] in object_._data:
                return object_._data.get(statement["property"]["name"], b_classes.Boolean(None))
            elif statement["property"]["name"] in object_._data:
                return b_classes.Function(f"{statement["object_name"]}.{statement["property"]["name"]}",
                                          object_.get("functions", {}).get(statement["property"]["name"],
                                                                           b_classes.Boolean(None)))
            closest_match = find_closest_match(object_["variables"].keys(), statement["property"]["name"])
            if closest_match:
                raise NameError(
                    f"Variable '{statement['object_name']}.{statement['property']['name']}' is not defined. Did you mean: '{statement['object_name']}.{closest_match}'?")
            raise NameError(f"Variable '{statement['object_name']}.{statement['property']['name']}' is not defined.")
        else:
            print(statement)
            raise SyntaxError(f"Unexpected property type: {statement['property']['type']}")

    def call_object_function(self, object_, function_name, pos_args, named_args, object_name=None, custom_name=None):
        function = object_._data.get(function_name, b_classes.Boolean(None))
        name = f"'{function_name}'"
        if isinstance(function, b_classes.Function):
            if function.is_builtin:
                self.stack.append({"name": name, "variables": self.variables, "return_value": self.return_value,
                                   "is_returning": self.is_returning})
                self.check_stack()
                ret = function.function(*pos_args, **named_args)
                self.stack.pop()
                return ret
            return self.call_function(function, pos_args, named_args, custom_name=custom_name)

        body = function["body"]
        parameters = function["parameters"]
        return_type = self.evaluate(function["return_type"])
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
        self.stack.append({"name": name, "variables": i.variables, "return_value": i.return_value,
                           "is_returning": i.is_returning})
        self.check_stack()
        i.stack = self.stack
        i.interpret(body)
        self.check_type(get_type(i.return_value), return_type, i.return_value)
        self.variables = self.stack[-1]["variables"]
        self.return_value = self.stack[-1]["return_value"]
        self.is_returning = self.stack[-1]["is_returning"]
        self.stack.pop()
        return b_classes.Literal(i.return_value)

    def handle_object_declaration(self, statement):
        name = statement["name"]
        self.debug_log(f"<Object '{name}' declared>")
        self.variables[name] = b_classes.Object(name=name)
        for function in statement["functions"]:
            self.variables[name]._data[function["name"]] = function
        for variable in statement["variables"]:
            self.objects[name]._data[variable["name"]] = variable
        self.variables[name]._data["init"] = statement["init"]

    def handle_comment(self, statement):
        color = self.config.get("color_scheme", {}).get("comment", "#757575")
        ansi_color = hex_to_ansi(color)
        print(f"{ansi_color}<{statement["value"]}>\033[0m")

    def handle_assignment_index(self, statement):
        name = statement["name"]
        index = self.evaluate(statement["index"])
        value = self.evaluate(statement["value"])
        try:
            index = int(index)
            value = int(value)
        except ValueError:
            pass
        self.debug_log(f"<Variable '{name}' assigned at index {index} to {value}>")
        if name in self.variables:
            if isinstance(self.variables[name], list):
                try:
                    index = int(index)
                except ValueError:
                    raise TypeError(f"Expected type 'int' for index, but got '{self.get_type(index)}'")
                if len(self.variables[name]) <= index:
                    raise IndexError(f"Index out of range: {index}")
                if index < 0:
                    self.variables[name][index + len(self.variables[name])] = value
                else:
                    self.variables[name][index] = value
            elif isinstance(self.variables[name], dict):
                self.variables[name][index] = value
            else:
                self.variables[name][index] = value
        else:
            raise NameError(f"Name '{name}' is not defined.")

    def handle_index(self, statement):
        index = self.evaluate(statement["index"])
        name = statement["name"]
        try:
            index = int(index)
        except ValueError:
            pass
        if name in self.variables:
            iterable = self.variables[name]
        elif name in self.objects:
            iterable = self.objects[name]
        elif hasattr(builtins, name):
            iterable = getattr(builtins, name)
        else:
            raise NameError(f"Name '{name}' is not defined.")
        if isinstance(iterable, list):
            try:
                index = int(index)
            except ValueError:
                raise TypeError(f"Expected type 'int' for index, but got '{self.get_type(index)}'")
            if len(iterable) <= index:
                raise IndexError(f"Index out of range: {index}")
            if index < 0:
                return iterable[index + len(iterable)]
        elif isinstance(iterable, dict):
            if index not in iterable:
                raise b_exceptions.KeyError(f"Key '{index}' not found in '{name}'.")
        return iterable[index]