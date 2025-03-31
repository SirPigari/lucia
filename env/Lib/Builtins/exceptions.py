class LuciaException(Exception):
    pass

class KeyError(LuciaException):
    pass

class LuciaWarning(Warning):
    pass

class PredefDisabledWarning(LuciaWarning):
    pass

class ListPatternRecognitionWarning(LuciaWarning):
    pass

class RecursionLimitWarning(LuciaWarning):
    pass


class WrappedException(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(str(original_exception))

    def __str__(self):
        return f"{self.original_exception.__class__.__name__}: {str(self.original_exception)}"