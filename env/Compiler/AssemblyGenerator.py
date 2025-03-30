class AssemblyCodeGenerator:
	def __init__(self):
		self.instructions = []
		self.label_counter = 0
		self.var_counter = 0
		self.function_counter = 0

	def _generate_label(self):
		self.label_counter += 1
		return f"label_{self.label_counter}"

	def _generate_var(self):
		self.var_counter += 1
		return f"var_{self.var_counter}"

	def generate(self, ast):
		for node in ast:
			self.traverse(node)
		return "\n".join(self.instructions)

	def traverse(self, node):
		if node['type'] == 'VARIABLEDECLARATION':
			self.handle_variable_declaration(node)
		elif node['type'] == 'ASSIGNMENT':
			self.handle_assignment(node)
		elif node['type'] == 'OPERATION':
			self.handle_operation(node)
		elif node['type'] == 'NUMBER':
			self.handle_number(node)
		elif node['type'] == 'VARIABLE':
			self.handle_variable(node)
		elif node['type'] == 'FUNCTIONDECLARATION':
			self.handle_function_declaration(node)
		elif node['type'] == 'RETURN':
			self.handle_return(node)
		else:
			raise ValueError(f"Unsupported node type: {node['type']}")

	def handle_variable_declaration(self, node):
		var_name = node["name"]
		value = self.evaluate_expression(node["value"])
		self.instructions.append(f"ALLOC {var_name}")
		self.instructions.append(f"STORE {value} -> {var_name}")

	def handle_assignment(self, node):
		var_name = node["name"]
		value = self.evaluate_expression(node["value"])
		self.instructions.append(f"STORE {value} -> {var_name}")

	def handle_operation(self, node):
		left = self.evaluate_expression(node["left"])
		right = self.evaluate_expression(node["right"])
		operator = node["operator"]
		result_var = self._generate_var()

		if operator == "-":
			self.instructions.append(f"SUB {left}, {right} -> {result_var}")
		elif operator == "+":
			self.instructions.append(f"ADD {left}, {right} -> {result_var}")
		elif operator == "*":
			self.instructions.append(f"MUL {left}, {right} -> {result_var}")
		elif operator == "/":
			self.instructions.append(f"DIV {left}, {right} -> {result_var}")
		else:
			raise ValueError(f"Unsupported operator: {operator}")

		return result_var

	def handle_number(self, node):
		return node["value"]

	def handle_variable(self, node):
		return node["name"]

	def handle_function_declaration(self, node):
		func_name = node["name"]
		self.instructions.append(f"ALLOC {func_name}")

		# Handle function parameters
		for param in node["parameters"]:
			param_name = param["name"]
			self.instructions.append(f"ALLOC {param_name}")

		# Process the function body
		self.instructions.append(f"FUNC {func_name}")
		for statement in node["body"]:
			self.traverse(statement)
		self.instructions.append(f"ENDFUNC {func_name}")

	def handle_return(self, node):
		return_value = self.evaluate_expression(node["value"])
		self.instructions.append(f"RETURN {return_value}")

	def evaluate_expression(self, expr):
		if expr['type'] == 'NUMBER':
			return self.handle_number(expr)
		elif expr['type'] == 'VARIABLE':
			return self.handle_variable(expr)
		elif expr['type'] == 'OPERATION':
			return self.handle_operation(expr)
		else:
			raise ValueError(f"Unsupported expression type: {expr['type']}")

