def get_type_default(type_):
    if type_ == "int":
        return {"type": "NUMBER", "value": 0}
    if type_ == "float":
        return {"type": "NUMBER", "value": 0.0}
    if type_ == "string":
        return {"type": "STRING", "value": ""}
    if type_ == "bool":
        return {"type": "BOOLEAN", "value": "false", "literal_value": None}
    if type_ == "any":
        return {"type": "BOOLEAN", "value": "null", "literal_value": None}
    if type_ == "map":
        return {"type": "ITERABLE", "iterable_type": "MAP", "keys": [], "values": []}
    if type_ == "list":
        return {"type": "ITERABLE", "iterable_type": "LIST", "elements": []}
    if type_ == "list_completion":
        return {"type": "ITERABLE", "iterable_type": "LIST_COMPLETION", "pattern": [], "end": None}
    return {"type": "BOOLEAN", "value": "null", "literal_value": None}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.statements = []

    @property
    def token(self):
        if self.pos >= len(self.tokens):
            return (None, None)
        return self.tokens[self.pos]

    def next(self):
        self.pos += 1
        # print(self.token)
        return self.token

    def get_next(self):
        if self.pos + 1 >= len(self.tokens):
            return None
        return self.tokens[self.pos + 1]

    def parse(self):
        while self.pos < len(self.tokens):
            s = self.parse_expression()
            if s:
                self.statements.append(s)
        return self.statements

    def parse_expression(self):
        if self.token == (None, None):
            self.next()
            return None

        if self.token == ('IDENTIFIER', 'if'):
            return self.parse_if_statement()

        if self.token == ('IDENTIFIER', 'try'):
            return self.parse_try_statement()

        if self.token == ('IDENTIFIER', 'object'):
            return self.parse_object()

        if self.token == ('IDENTIFIER', 'init'):
            return self.parse_object_init()

        if self.token == ('IDENTIFIER', 'while'):
            return self.parse_while_loop()

        if self.token[0] == 'IDENTIFIER' and self.token[1] in ('void', 'int', 'float', 'string', 'bool', 'any'):
            return self.parse_type()

        if self.token == ('IDENTIFIER', 'for'):
            return self.parse_for_loop()

        if self.token[0] == 'IDENTIFIER' and self.token[1] in ["fun", "async", "public", "static", "private", "mutable", "final"]:
            return self.parse_function_declaration()

        if self.token[0] == 'IDENTIFIER' and self.token[1] == 'forget':
            return self.parse_forget_statement()

        if self.token == ('IDENTIFIER', 'import'):
            return self.parse_import_statement()

        if self.token == ('IDENTIFIER', 'with'):
            return self.parse_with_statement()

        if self.token == ('IDENTIFIER', 'throw'):
            return self.parse_throw_statement()

        if self.token[0] == 'IDENTIFIER' and self.token[1] == 'return':
            return self.parse_return_statement()

        if self.token[0] == 'IDENTIFIER' and self.get_next() and self.get_next()[0] == 'SEPARATOR' and \
                self.get_next()[1] == '(':
            return self.parse_function_call()

        if self.token == ('SEPARATOR', '['):
            self.next()
            elements = []
            while self.token != ('SEPARATOR', ']'):
                elements.append(self.parse_expression())
                if self.token == ('SEPARATOR', ']'):
                    break
                if self.token == ('SEPARATOR', '...'):
                    self.check_for('SEPARATOR', '...')
                    self.next()
                    end = self.parse_expression()
                    self.check_for('SEPARATOR', ']')
                    self.next()
                    return {"type": "ITERABLE", "iterable_type": "LIST_COMPLETION", "pattern": elements, "end": end}
                self.check_for('SEPARATOR', ',')
                self.next()
            self.next()
            return {"type": "ITERABLE", "iterable_type": "LIST", "elements": elements}

        if self.token == ('SEPARATOR', '{'):
            self.next()
            keys = []
            values = []
            while self.token != ('SEPARATOR', '}'):
                keys.append(self.parse_expression())
                self.check_for('SEPARATOR', ':')
                self.next()
                values.append(self.parse_expression())
                if self.token == ('SEPARATOR', '}'):
                    break
                self.check_for('SEPARATOR', ',')
                self.next()
            self.check_for('SEPARATOR', '}')
            self.next()
            return {"type": "ITERABLE", "iterable_type": "MAP", "keys": keys, "values": values}

        if self.token[0] == 'IDENTIFIER' and self.get_next() and self.get_next() == ('SEPARATOR', '['):
            return self.parse_indexing()

        if self.token == ('SEPARATOR', '('):
            self.next()
            expression = self.parse_expression()
            self.next()
            self.check_for('SEPARATOR', ')')
            self.next()
            return expression

        if self.token == ('OPERATOR', '!'):
            self.next()
            return {"type": "OPERATION", "left": {"type": "BOOLEAN", "value": "null", "literal_value": None}, "operator": "!", "right": self.parse_expression()}

        if self.token[0] in ('NUMBER', 'STRING', 'BOOLEAN') and self.get_next() and self.get_next()[0] == 'OPERATOR':
            return self.parse_operation()

        if self.token[0] == 'BOOLEAN':
            value = self.token[1]
            literal_value = True if value == 'true' else False if value == 'false' else None if value == 'null' else "Undefined"
            self.next()
            return {"type": "BOOLEAN", "value": value, "literal_value": literal_value}

        if self.token[0] == 'IDENTIFIER' and self.get_next() and self.get_next() == ('SEPARATOR', '.'):
            return self.parse_property()

        # Check for variable declaration or assignment
        elif self.token[0] == 'IDENTIFIER' and self.get_next() and self.get_next()[0] == 'SEPARATOR' and \
                self.get_next()[1] == ':':
            return self.parse_variable_declaration()

        elif self.token[0] in ('NUMBER', 'IDENTIFIER', 'STRING') and self.get_next() and self.get_next() == ('OPERATOR', '='):
            return self.parse_assignment()

        # Check for number, string, or variable to parse as an operation
        elif self.token[0] in ('NUMBER', 'IDENTIFIER', 'STRING'):
            return self.parse_operation()

        elif self.token[0] in ('COMMENT_SINGLE', 'COMMENT_MULTI', 'COMMENT_INLINE'):
            t = self.token[1]
            self.next()
            return {"type": "COMMENT", "value": t}
        else:
            raise SyntaxError(f"Unexpected token: {self.token}")

    def parse_property(self):
        object_name = self.token[1]
        self.next()
        self.check_for('SEPARATOR', '.')
        self.next()
        property_name = self.parse_expression()
        return {
            "type": "PROPERTY",
            "object_name": object_name,
            "property": property_name
        }

    def parse_assignment(self):
        name = self.token[1]
        self.next()
        self.next()
        value = self.parse_expression()
        return {
            "type": "ASSIGNMENT",
            "name": name,
            "value": value
        }

    def parse_import_statement(self):
        self.check_for('IDENTIFIER', 'import')
        self.next()
        module_name = self.token[1]
        as_name = module_name
        from_ = {"type": "STRING", "value": ".\\Lib"}
        self.next()
        while self.token:
            if self.token == ('IDENTIFIER', 'as'):
                self.next()
                as_name = self.token[1]
                self.next()
            elif self.token == ('IDENTIFIER', 'from'):
                self.next()
                from_ = self.parse_expression()
            else:
                break
        return {
            "type": "IMPORT",
            "module_name": module_name,
            "as": as_name,
            "from": from_
        }

    def parse_variable_declaration(self):
        name = self.token[1]
        self.next()
        self.next()
        variable_type = self.parse_type()
        is_final = False
        value = get_type_default(variable_type["name"])
        if self.token == ('OPERATOR', '|'):
            self.next()
            while self.token[1] in ("final", "mutable"):
                if self.token[1] == "final":
                    is_final = True
                if self.token[1] == "mutable":
                    is_final = False
                self.next()
        if self.token == ('OPERATOR', '='):
            self.next()
            value = self.parse_expression()
        return {
            "type": "VARIABLEDECLARATION",
            "name": name,
            "value": value,
            "variable_type": variable_type,
            "is_final": is_final
        }

    def parse_function_declaration(self):
        modifiers = {"async": False, "public": None, "static": False, "final": False}

        while self.token and self.token[0] == 'IDENTIFIER' and self.token[1] in ('async', 'public', 'static', 'private', 'mutable', 'final'):
            if self.token[1] == 'async':
                modifiers["async"] = True
            elif self.token[1] == 'public':
                modifiers["public"] = True
            elif self.token[1] == 'static':
                modifiers["static"] = True
            elif self.token[1] == 'private':
                modifiers["public"] = False
            elif self.token[1] == 'mutable':
                modifiers["final"] = False
            elif self.token[1] == 'final':
                modifiers["final"] = True
            self.next()

        if self.token == ('IDENTIFIER', 'fun'):
            self.check_for('IDENTIFIER', 'fun')
            self.next()
        name = self.token[1]
        self.next()
        self.check_for('SEPARATOR', '(')
        parameters = self.parse_parameters()
        self.check_for('OPERATOR', '->')
        self.next()
        return_type = self.parse_return_type()
        if self.token == ('SEPARATOR', ':'):
            self.next()
        body = self.parse_body()
        self.check_for('IDENTIFIER', 'end')
        self.next()

        return {
            "type": "FUNCTIONDECLARATION",
            "name": name,
            "parameters": parameters,
            "return_type": return_type,
            "body": body,
            "is_async": modifiers["async"],
            "is_static": modifiers["static"],
            "is_final": modifiers["final"],
            "is_public": modifiers["public"]
        }

    def parse_parameters(self):
        self.check_for('SEPARATOR', '(')
        self.next()
        parameters = []
        while self.token != ('SEPARATOR', ')'):
            name = self.token[1]
            self.next()
            variable_type = "any"
            default_value = None
            if self.token == ('SEPARATOR', ':'):
                self.next()
                variable_type = self.token[1]
                self.next()
            if self.token == ('OPERATOR', '='):
                self.next()
                default_value = self.parse_expression()
            parameters.append({"name": name, "variable_type": variable_type, "default_value": default_value})
            if self.token == ('SEPARATOR', ')'):
                break
            self.check_for('SEPARATOR', ',')
            self.next()
        self.next()
        return parameters

    def parse_body(self):
        body = []
        if self.token == ('SEPARATOR', ':'):
            self.next()
        while self.token and not (self.token == ('IDENTIFIER', 'end')):
            body.append(self.parse_expression())
        return body

    def parse_function_call(self):
        name = self.token[1]
        self.next()
        self.check_for('SEPARATOR', '(')
        self.next()
        pos_arguments, named_arguments = self.parse_arguments()
        self.check_for('SEPARATOR', ')')
        self.next()
        return {
            "type": "CALL",
            "name": name,
            "pos_arguments": pos_arguments,
            "named_arguments": named_arguments
        }

    def parse_arguments(self):
        pos_args = []
        named_args = []
        while self.token != ('SEPARATOR', ')'):
            if self.token[0] == 'IDENTIFIER' and self.get_next() and self.get_next() == ('OPERATOR', '='):
                name = self.token[1]
                self.next()
                self.next()
                value = self.parse_expression()
                named_args.append({"type": "NAMEDARG", "name": name, "value": value})
            else:
                pos_args.append(self.parse_expression())
            if self.token == ('SEPARATOR', ')'):
                break
            self.check_for('SEPARATOR', ',')
            self.next()
        return pos_args, named_args

    def parse_statement(self):
        if self.token[0] == 'IDENTIFIER' and self.token[1] == 'return':
            return self.parse_return_statement()
        elif self.token[0] == 'IDENTIFIER':
            return self.parse_variable_declaration()
        else:
            return self.parse_operation()

    def parse_return_type(self):
        if self.token[0] == 'IDENTIFIER':
            return self.parse_type()
        else:
            raise SyntaxError(f"Return type '{self.token[1]}' is not supported.")

    def parse_return_statement(self):
        self.next()
        value = {"type": "BOOLEAN", "value": "null", "literal_value": None}
        if self.token and self.token != ('IDENTIFIER', 'end'):
            value = self.parse_expression()
        return {
            "type": "RETURN",
            "value": value
        }

    def parse_operation(self):
        left = self.parse_operand()
        while self.token and self.token[0] == 'OPERATOR':
            operator = self.token[1]
            self.next()
            right = self.parse_operand()
            left = {"type": "OPERATION", "left": left, "operator": operator, "right": right}
        return left

    def parse_operand(self):
        if self.token[0] == 'NUMBER':
            value = {"type": "NUMBER", "value": float(self.token[1])}
        elif self.token[0] == 'IDENTIFIER':
            value = {"type": "VARIABLE", "name": self.token[1]}
        elif self.token[0] == 'STRING':
            value = {"type": "STRING", "value": self.token[1].strip('"')}
        elif self.token[0] == 'BOOLEAN':
            value_ = self.token[1]
            literal_value = True if value_ == 'true' else False if value_ == 'false' else None if value_ == 'null' else "Undefined"
            self.next()
            value = {"type": "BOOLEAN", "value": value_, "literal_value": literal_value}
        else:
            raise SyntaxError(f"Unexpected token: {self.token}")
        self.next()
        return value

    def check_for(self, token_type, value=None):
        if not self.token:
            raise SyntaxError("Unexpected end of input")
        if not value:
            if self.token[0] != token_type:
                raise SyntaxError(f"Expected '{token_type}' but got '{self.token[0]}'")
        else:
            if self.token[0] != token_type or self.token[1] != value:
                raise SyntaxError(f"Expected '{value}' but got '{self.token[1]}'")

    def parse_type(self):
        type_name = self.token[1]
        self.next()
        return {
            "type": "TYPE",
            "name": type_name
        }

    def parse_if_statement(self):
        self.check_for('IDENTIFIER', 'if')
        self.next()
        self.check_for('SEPARATOR', '(')
        self.next()
        condition = self.parse_expression()
        self.check_for('SEPARATOR', ')')
        self.next()
        self.check_for('SEPARATOR', ':')
        self.next()
        body = self.parse_body()
        self.check_for('IDENTIFIER', 'end')
        self.next()
        else_body = []
        if self.token == ('IDENTIFIER', 'else'):
            self.next()
            if self.token == ('IDENTIFIER', 'if'):
                else_body = [self.parse_if_statement()]
            else:
                self.check_for('SEPARATOR', ':')
                self.next()
                else_body = self.parse_body()
                self.check_for('IDENTIFIER', 'end')
                self.next()
        return {
            "type": "IF",
            "condition": condition,
            "body": body,
            "else_body": else_body
        }

    def parse_for_loop(self):
        self.check_for('IDENTIFIER', 'for')
        self.next()
        self.check_for('SEPARATOR', '(')
        self.next()
        variable = self.token[1]
        self.next()
        self.check_for('IDENTIFIER', 'in')
        self.next()
        iterable = self.parse_expression()
        self.check_for('SEPARATOR', ')')
        self.next()
        self.check_for('SEPARATOR', ':')
        self.next()
        body = self.parse_body()
        self.check_for('IDENTIFIER', 'end')
        self.next()
        return {
            "type": "FOR",
            "variable_name": variable,
            "iterable": iterable,
            "body": body
        }

    def parse_while_loop(self):
        self.check_for('IDENTIFIER', 'while')
        self.next()
        self.check_for('SEPARATOR', '(')
        self.next()
        condition = self.parse_expression()
        self.check_for('SEPARATOR', ')')
        self.next()
        self.check_for('SEPARATOR', ':')
        self.next()
        body = self.parse_body()
        self.check_for('IDENTIFIER', 'end')
        self.next()
        return {
            "type": "WHILE",
            "condition": condition,
            "body": body
        }

    def parse_throw_statement(self):
        self.check_for('IDENTIFIER', 'throw')
        value = {'type': 'BOOLEAN', 'value': 'null', 'literal_value': None}
        from_ = {'type': 'VARIABLE', 'name': 'LuciaException'}
        self.next()
        if self.token:
            value = self.parse_expression()
            if self.token == ('IDENTIFIER', 'from'):
                self.next()
                from_ = self.parse_expression()
        return {
            "type": "THROW",
            "value": value,
            "from": from_,
        }

    def parse_object(self):
        self.check_for('IDENTIFIER', 'object')
        self.next()
        name = self.token[1]
        self.next()
        self.check_for('SEPARATOR', ':')
        self.next()
        functions, variables, init = self.parse_object_body()
        self.next()
        return {
            "type": "OBJECTDECLARATION",
            "name": name,
            "functions": functions,
            "variables": variables,
            "init": init
        }

    def parse_object_init(self):
        self.check_for('IDENTIFIER', 'init')
        self.next()
        parameters = self.parse_parameters()
        self.check_for('SEPARATOR', ':')
        self.next()
        body = self.parse_body()
        self.next()
        return {
            "type": "OBJECTINIT",
            "parameters": parameters,
            "body": body
        }

    def parse_object_body(self):
        functions = []
        variables = []
        init = {}
        while self.token and not (self.token == ('IDENTIFIER', 'end')):
            if self.token[0] == 'IDENTIFIER' and self.token[1] in ["fun", "async", "public", "static", "private", "mutable", "final"]:
                functions.append(self.parse_function_declaration())
            elif self.token == ('IDENTIFIER', 'init'):
                init = self.parse_object_init()
            elif self.token == ('IDENTIFIER', 'object'):
                variables.append(self.parse_object())
            elif self.token == ('IDENTIFIER', 'return'):
                return self.parse_return_statement()
            else:
                variables.append(self.parse_variable_declaration())
        return functions, variables, init

    def parse_forget_statement(self):
        self.check_for('IDENTIFIER', 'forget')
        self.next()
        name = self.token[1]
        self.next()
        return {
            "type": "FORGET",
            "name": name
        }

    def parse_indexing(self):
        name = self.token[1]
        self.next()
        self.check_for('SEPARATOR', '[')
        self.next()
        index = self.parse_expression()
        self.check_for('SEPARATOR', ']')
        self.next()
        if self.token == ('OPERATOR', '='):
            self.next()
            value = self.parse_expression()
            return {
                "type": "ASSIGNMENT_INDEX",
                "name": name,
                "index": index,
                "value": value
            }
        return {
            "type": "INDEX",
            "name": name,
            "index": index
        }

    def parse_with_statement(self):
        self.check_for('IDENTIFIER', 'with')
        self.next()
        self.check_for('SEPARATOR', '(')
        self.next()
        with_ = self.parse_expression()
        self.check_for('SEPARATOR', ')')
        self.next()
        as_ = None
        if self.token == ('IDENTIFIER', 'as'):
            self.next()
            as_ = self.token[1]
            self.next()
        self.check_for('SEPARATOR', ':')
        self.next()
        body = self.parse_body()
        self.check_for('IDENTIFIER', 'end')
        self.next()
        return {
            "type": "WITH",
            "with": with_,
            "as": as_,
            "body": body
        }

    def parse_try_statement(self):
        self.check_for('IDENTIFIER', 'try')
        self.next()
        self.check_for('SEPARATOR', ':')
        self.next()
        body = self.parse_body()
        self.check_for('IDENTIFIER', 'end')
        self.next()
        self.check_for('IDENTIFIER', 'catch')
        self.next()
        self.check_for('SEPARATOR', '(')
        self.next()
        self.check_for('IDENTIFIER')
        except_name = self.token[1]
        self.next()
        self.check_for('SEPARATOR', ')')
        self.next()
        self.check_for('SEPARATOR', ':')
        self.next()
        except_body = self.parse_body()
        self.check_for('IDENTIFIER', 'end')
        self.next()
        return {
            "type": "TRY",
            "body": body,
            "exception_variable": except_name,
            "catch_body": except_body
        }