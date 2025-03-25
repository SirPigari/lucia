class LuciaException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

class KeyError(LuciaException):
    pass

class LuciaWarning(Warning):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

class ListPatterRecognitionWarning(LuciaWarning):
    pass

class RecursionLimitWarning(LuciaWarning):
    pass


class WrappedException(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(str(original_exception))

    def __str__(self):
        return f"{self.original_exception.__class__.__name__}: {str(self.original_exception)}"