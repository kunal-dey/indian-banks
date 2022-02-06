class DbConnectionException(Exception):
    """
        Custom error raised when the database connection fails.
    """

    def __init__(self,
                 message:str = "An error occured from our side."):
        self.message = message
        super().__init__(message)