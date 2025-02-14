class ListPatterRecognitionWarning(Warning):
    """Warning for when a list pattern is recognized."""
    def __init__(self, message, *args):
        super().__init__(message, *args)

    def __str__(self):
        return self.args[0]