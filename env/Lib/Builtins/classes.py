import decimal

def Literal(__literal):
    if isinstance(__literal, str):
        return Str(__literal)
    elif isinstance(__literal, int):
        return Int(__literal)
    elif isinstance(__literal, float):
        return Float(__literal)
    elif isinstance(__literal, bool):
        return Boolean(__literal)
    elif isinstance(__literal, Boolean):
        return __literal
    elif isinstance(__literal, list):
        return List(__literal)
    elif isinstance(__literal, dict):
        return Map(__literal)
    elif isinstance(__literal, Object):
        return Object(__literal)
    elif isinstance(__literal, Function):
        return Function(__literal)
    elif isinstance(__literal, Variable):
        return Variable(name="_", value=__literal)
    else:
        raise TypeError(f"Unsupported literal type: {type(__literal).__name__}")


class Boolean:
    def __init__(self, value, literal=None):
        og_val = value
        value = str(value).strip().lower()
        if value == 'true':
            self.value = 'true'
            self.literal = True
        elif value == 'false':
            self.value = 'false'
            self.literal = False
        elif value == 'null':
            self.value = 'null'
            self.literal = None
        elif value == 'none':
            self.value = 'null'
            self.literal = None
        else:
            self.value = og_val
            self.literal = literal
        if literal is not None:
            self.literal = literal

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Boolean):
            return self.literal == other.literal
        return self.literal == other

    def __ne__(self, other):
        if isinstance(other, Boolean):
            return self.literal != other.literal
        return self.literal != other

    def __and__(self, other):
        if isinstance(other, Boolean):
            return Boolean(str(self.literal and other.literal), self.literal and other.literal)
        return Boolean(str(self.literal and other), self.literal and other)

    def __or__(self, other):
        if isinstance(other, Boolean):
            return Boolean(str(self.literal or other.literal), self.literal or other.literal)
        return Boolean(str(self.literal or other), self.literal or other)

    def __invert__(self):
        return Boolean(str(not self.literal), not self.literal)

    def __lt__(self, other):
        if isinstance(other, Boolean):
            return self.literal < other.literal
        return self.literal < other

    def __le__(self, other):
        if isinstance(other, Boolean):
            return self.literal <= other.literal
        return self.literal <= other

    def __gt__(self, other):
        if isinstance(other, Boolean):
            return self.literal > other.literal
        return self.literal > other

    def __ge__(self, other):
        if isinstance(other, Boolean):
            return self.literal >= other.literal
        return self.literal >= other


class Object:
    def __init__(self, value=None, name=None, custom_str=None, is_builtin=False, object=None):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self._data = {}
        self.custom_str = custom_str
        self.is_builtin = is_builtin
        if self.is_builtin:
            self.object = object
        if value:
            if isinstance(value, dict):
                self._data = value
            elif isinstance(value, Object):
                self._data = value.get_data()
            else:
                raise TypeError(f"Expected dictionary or Object, got {type(value).__name__}")

    def __str__(self):
        if self.custom_str:
            return self.custom_str
        return f"<object '{self.name}' at {id(self)}>"

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    def get_data(self):
        return self._data

    def get(self, key, default=None):
        return self._data.get(key, default)

    def setdefault(self, key, default=None):
        return self._data.setdefault(key, default)

    def pop(self, key, default=None):
        return self._data.pop(key, default)

    def popitem(self):
        return self._data.popitem()

    def clear(self):
        self._data.clear()

    def update(self, other=None, **kwargs):
        if other is not None:
            if isinstance(other, dict):
                self._data.update(other)
            elif isinstance(other, Object):
                self._data.update(other.get_data())
            else:
                raise TypeError(f"Expected dictionary or Object, got {type(other).__name__}")
        if kwargs:
            self._data.update(kwargs)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def __eq__(self, other):
        if isinstance(other, Object):
            return self._data == other.get_data()
        return False

    def __ne__(self, other):
        if isinstance(other, Object):
            return self._data != other.get_data()
        return True

    def __repr__(self):
        return f"Object(name={self.name}, data={repr(self._data)})"


class Variable:
    def __init__(self, name, value=None, mods=None, type_="any"):
        self.name = name
        self.value = value
        self.type = type_
        if not mods:
            mods = {"is_final": False, "is_public": True, "is_static": False}
        self.modifiers = mods

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<variable '{self.name}' at {id(self)}>"

    def evaluate(self):
        return self.value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self.value)

    def __hash__(self):
        return hash(self.value)

    def __iter__(self):
        return iter(self.value)

    def type(self):
        return type(self.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        if isinstance(self.value, (dict, list)):
            return self.value[key]
        raise TypeError(f"Variable '{self.name}' does not support indexing (not a list or dict)")

    def __setitem__(self, key, value):
        if isinstance(self.value, (dict, list)):
            self.value[key] = value
        else:
            raise TypeError(f"Cannot assign value to index '{key}' in variable '{self.name}' (not a list or dict)")

    def get(self, key, default=None):
        if isinstance(self.value, dict):
            return self.value.get(key, default)
        raise TypeError(f"Variable '{self.name}' does not support key-value access (not a dict)")

    def setdefault(self, key, default=None):
        if isinstance(self.value, dict):
            return self.value.setdefault(key, default)
        raise TypeError(f"Variable '{self.name}' does not support key-value access (not a dict)")

    # Arithmetic operators (returning value)
    def __add__(self, other):
        if isinstance(other, Variable):
            return self.value + other.value
        return self.value + other

    def __sub__(self, other):
        if isinstance(other, Variable):
            return self.value - other.value
        return self.value - other

    def __mul__(self, other):
        if isinstance(other, Variable):
            return self.value * other.value
        return self.value * other

    def __truediv__(self, other):
        if isinstance(other, Variable):
            return self.value / other.value
        return self.value / other

    def __floordiv__(self, other):
        if isinstance(other, Variable):
            return self.value // other.value
        return self.value // other

    def __mod__(self, other):
        if isinstance(other, Variable):
            return self.value % other.value
        return self.value % other

    def __pow__(self, other):
        if isinstance(other, Variable):
            return self.value ** other.value
        return self.value ** other

    # Comparison operators (returning Boolean value)
    def __eq__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value == other.value)
        return Boolean(self.value == other)

    def __ne__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value != other.value)
        return Boolean(self.value != other)

    def __lt__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value < other.value)
        return Boolean(self.value < other)

    def __le__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value <= other.value)
        return Boolean(self.value <= other)

    def __gt__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value > other.value)
        return Boolean(self.value > other)

    def __ge__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value >= other.value)
        return Boolean(self.value >= other)

    # Logical operators (returning Boolean value)
    def __and__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value and other.value)
        return Boolean(self.value and other)

    def __or__(self, other):
        if isinstance(other, Variable):
            return Boolean(self.value or other.value)
        return Boolean(self.value or other)

    def __not__(self):
        return Boolean(not self.value)

    # In-place arithmetic operators (modifies the value in-place and returns it)
    def __iadd__(self, other):
        if isinstance(other, Variable):
            self.value += other.value
        else:
            self.value += other
        return self.value

    def __isub__(self, other):
        if isinstance(other, Variable):
            self.value -= other.value
        else:
            self.value -= other
        return self.value

    def __imul__(self, other):
        if isinstance(other, Variable):
            self.value *= other.value
        else:
            self.value *= other
        return self.value

    def __itruediv__(self, other):
        if isinstance(other, Variable):
            self.value /= other.value
        else:
            self.value /= other
        return self.value

    def __ifloordiv__(self, other):
        if isinstance(other, Variable):
            self.value //= other.value
        else:
            self.value //= other
        return self.value

    def __imod__(self, other):
        if isinstance(other, Variable):
            self.value %= other.value
        else:
            self.value %= other
        return self.value

    def __ipow__(self, other):
        if isinstance(other, Variable):
            self.value **= other.value
        else:
            self.value **= other
        return self.value


class Decimal(decimal.Decimal):
    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def __len__(self):
        return len(str(self))

    def __declen__(self) -> int:
        decimals = str(self).split(".")[-1]
        return len(str(decimals))

    def __add__(self, other):
        return Decimal(super().__add__(Decimal(other)))

    def __sub__(self, other):
        return Decimal(super().__sub__(Decimal(other)))

    def __mul__(self, other):
        return Decimal(super().__mul__(Decimal(other)))

    def __truediv__(self, other):
        return Decimal(super().__truediv__(Decimal(other)))

    def __floordiv__(self, other):
        return Decimal(super().__floordiv__(Decimal(other)))

    def __mod__(self, other):
        return Decimal(super().__mod__(Decimal(other)))

    def __pow__(self, other, modulo=None):
        return Decimal(super().__pow__(Decimal(other), modulo))

    def __eq__(self, other):
        return super().__eq__(Decimal(other))

    def __ne__(self, other):
        return super().__ne__(Decimal(other))

    def __lt__(self, other):
        return super().__lt__(Decimal(other))

    def __le__(self, other):
        return super().__le__(Decimal(other))

    def __gt__(self, other):
        return super().__gt__(Decimal(other))

    def __ge__(self, other):
        return super().__ge__(Decimal(other))

    def __neg__(self):
        return Decimal(super().__neg__())

    def __abs__(self):
        return Decimal(super().__abs__())

    def __float__(self):
        return float(str(self))


class Function:
    def __init__(self, name=None, parameters=None, body=None, mods=None, return_type=None, is_builtin=False, function=None):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self.parameters = parameters
        self.body = body
        self.modifiers = mods
        self.return_type = return_type
        self.is_builtin = is_builtin
        if self.is_builtin:
            self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __str__(self):
        return f"<function '{self.name}' at {id(self)}>"


class Float(float):
    pass

class Int(int):
    pass

class Str(str):
    pass

class List(list):
    pass

class Map(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = self


class File:
    def __init__(self, name, mode='r', encoding='utf-8'):
        self.name = name
        self.mode = mode
        self.encoding = encoding
        try:
            self.file = open(name, mode, encoding=encoding)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{name}' not found.")

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        if exc_val:
            raise exc_val

class TestContext:
    def __init__(self):
        pass

    def __str__(self):
        return f"<TestContext at {id(self)}>"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self