class Boolean:
    def __init__(self, value, literal=None):
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
            if bool(value):
                self.value = 'true'
                self.literal = True
            else:
                self.value = 'false'
                self.literal = False
        if literal is not None:
            self.literal = literal

    def __str__(self):
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
