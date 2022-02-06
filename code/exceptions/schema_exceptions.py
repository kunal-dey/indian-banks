class IfscFormatException(Exception):
    """
        Custom error raised when the IFSC code is not valid.
    """

    def __init__(self, value:str, message:str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)