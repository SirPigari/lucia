class LuciaException(Exception):
    pass

class KeyError(LuciaException):
    pass

class LuciaWarning(Warning):
    pass

class ListPatterRecognitionWarning(LuciaWarning):
    pass

class RecursionLimitWarning(LuciaWarning):
    pass