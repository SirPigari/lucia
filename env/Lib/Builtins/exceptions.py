def MakeException(name, base=Exception):
    cls = type(name, (base,), {
        '__init__': lambda self, message: super(cls, self).__init__(message),
        '__str__': lambda self: f'{self.args[0]}' if self.args else f'{self.__class__.__name__}'
    })
    return cls
def MakeWarning(name, base=Warning):
    cls = type(name, (base,), {
        '__init__': lambda self, message: super(cls, self).__init__(message),
        '__str__': lambda self: f'{self.args[0]}' if self.args else f'{self.__class__.__name__}'
    })
    return cls

class LuciaException(Exception):
    def __type__(self):
        return type(self.original_exception)
    pass

class KeyError(LuciaException):
    pass

class CRuntimeError(LuciaException):
    pass

class LuciaWarning(Warning):
    @property
    def __type__(self):
        return type(self.original_exception)
    pass

class PredefDisabledWarning(LuciaWarning):
    pass

class ListPatternRecognitionWarning(LuciaWarning):
    pass

class RecursionLimitWarning(LuciaWarning):
    pass

class CCodeDisabledWarning(LuciaWarning):
    pass

class TCCWarning(LuciaWarning):
    pass


class WrappedException(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(str(original_exception))

    @property
    def __type__(self):
        return type(self.original_exception)

    def __str__(self):
        return f"{self.original_exception.__class__.__name__}: {str(self.original_exception)}"