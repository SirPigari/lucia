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
        return Object(__literal)
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
    def __init__(self, value=None, name=None, custom_str=None):
        if not name:
            name = self.__class__.__name__
        self.name = name
        self._data = {}
        self.custom_str = custom_str
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


class Function:
    def __init__(self, name, body=None):
        self.name = name
        self._data = body

    def __str__(self):
        return f"<function '{self.name}' at {id(self)}>"

    def __repr__(self):
        return f"Function(name={self.name}, body={self._data})"

class Variable:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return f"<variable '{self.name}' at {id(self)}>"


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