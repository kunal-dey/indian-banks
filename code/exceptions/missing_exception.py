class MissingValueException(Exception):
    def __init__(self, value:str):
        self.message = f"{value} is missing."
        super().__init__()
