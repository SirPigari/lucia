class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.statements = []

    @property
    def token(self):
        if self.pos >= len(self.tokens):
            return None
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
        if self.token is None:
            return None

        if self.token[0] == 'IDENTIFIER' and self.token[1] in ('void', 'int', 'float', 'string', 'bool', 'any'):
            return self.parse_type()

        if self.token == ('IDENTIFIER', 'for'):
            return self.parse_for_loop()

        if self.token[0] == 'SEPARATOR' and self.token[1] == '(':
            self.next()
            expression = self.parse_expression()
            self.next()
            self.check_for('SEPARATOR', ')')
            self.next()
            return expression

        if self.token == ('OPERATOR', '!'):
            self.next()
            return {"type": "OPERATION", "left": {"type": "BOOLEAN", "value": "null", "literal_value": None}, "operator": "!", "right": self.parse_expression()}

        if self.token[0] in ('NUMBER', 'STRING', 'BOOLEAN') and self.get_next()[0] == 'OPERATOR':
            return self.parse_operation()

        # Check for function declaration (fun <name> ...)
        if self.token[0] == 'IDENTIFIER' and self.token[1] in ["fun", "async", "public", "static", "private", "mutable", "final"]:
            return self.parse_function_declaration()

        if self.token[0] == 'IDENTIFIER' and self.token[1] == 'if':
            return self.parse_if_statement()

        if self.token[0] == 'BOOLEAN':
            value = self.token[1]
            literal_value = True if value == 'true' else False if value == 'false' else None if value == 'null' else "Undefined"
            self.next()
            return {"type": "BOOLEAN", "value": value, "literal_value": literal_value}

        if self.token[0] == 'IDENTIFIER' and self.get_next() and self.get_next()[0] == 'SEPARATOR' and \
                self.get_next()[1] == '(':
            return self.parse_function_call()

        if self.token[0] == 'IDENTIFIER' and self.get_next() and self.get_next() == ('SEPARATOR', '.'):
            return self.parse_property()

        if self.token == ('IDENTIFIER', 'import'):
            return self.parse_import_statement()

        if self.token[0] == 'IDENTIFIER' and self.token[1] == 'return':
            return self.parse_return_statement()

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
        self.next()
        as_name = module_name
        if self.token == ('IDENTIFIER', 'as'):
            self.next()
            as_name = self.token[1]
            self.next()
        return {
            "type": "IMPORT",
            "module_name": module_name,
            "as": as_name
        }

    def parse_variable_declaration(self):
        name = self.token[1]
        self.next()
        self.next()
        variable_type = self.token[1]
        self.next()
        self.next()
        value = self.parse_expression()
        return {
            "type": "VARIABLEDECLARATION",
            "name": name,
            "value": value,
            "variable_type": variable_type
        }

    def parse_function_declaration(self):
        modifiers = {"async": False, "public": None, "mutable": False, "final": False}

        while self.token and self.token[0] == 'IDENTIFIER' and self.token[1] in ('async', 'public', 'static', 'private', 'mutable', 'final'):
            if self.token[1] == 'async':
                modifiers["async"] = True
            elif self.token[1] == 'public':
                modifiers["public"] = True
            elif self.token[1] == 'static':
                modifiers["mutable"] = False
            elif self.token[1] == 'private':
                modifiers["public"] = False
            elif self.token[1] == 'mutable':
                modifiers["mutable"] = True
            elif self.token[1] == 'final':
                modifiers["final"] = True
            self.next()

        self.check_for('IDENTIFIER', 'fun')
        self.next()
        name = self.token[1]
        self.next()
        self.check_for('SEPARATOR', '(')
        parameters = self.parse_parameters()
        self.check_for('OPERATOR', '->')
        self.next()
        return_type = self.parse_return_type()
        self.check_for('SEPARATOR', '{')
        self.next()
        body = self.parse_body()
        self.check_for('SEPARATOR', '}')
        self.next()

        return {
            "type": "FUNCTIONDECLARATION",
            "name": name,
            "parameters": parameters,
            "return_type": return_type,
            "body": body,
            "is_async": modifiers["async"],
            "is_mutable": modifiers["mutable"],
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
        while self.token and not (self.token[0] == 'SEPARATOR' and self.token[1] == '}'):
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
        if self.token[0] == 'IDENTIFIER' and self.token[1] in ('void', 'int', 'float', 'string', 'bool', 'any'):
            return self.parse_type()
        else:
            raise SyntaxError(f"Return type '{self.token[1]}' is not supported.")

    def parse_return_statement(self):
        self.next()  # Skip 'return'
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
        self.check_for('SEPARATOR', '{')
        self.next()
        body = self.parse_body()
        self.check_for('SEPARATOR', '}')
        self.next()
        else_body = []
        if self.token == ('IDENTIFIER', 'else'):
            self.next()
            if self.token == ('IDENTIFIER', 'if'):
                else_body = [self.parse_if_statement()]
            else:
                self.check_for('SEPARATOR', '{')
                self.next()
                else_body = self.parse_body()
                self.check_for('SEPARATOR', '}')
                self.next()
        return {
            "type": "IF",
            "condition": condition,
            "body": body,
            "else_body": else_body
        }