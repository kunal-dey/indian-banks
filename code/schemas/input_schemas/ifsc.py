from pydantic import BaseModel, validator

from exceptions.schema_exceptions import IfscFormatException


class Ifsc(BaseModel):

    ifsc_code: str

    @validator("ifsc_code")
    @classmethod
    def valid_ifsc_code(cls, value):
        """
            Validator to check whether the ifsc code is valid or not.
        """
        if len(value) != 11:
            raise IfscFormatException(value, "Ifsc code must contain 11 digits.")
        if value[4] != '0':
            raise IfscFormatException(value, "The fifth digit must be numeric (kept 0).")
        return value

    class Config:
        """Pydantic Config class"""

        allow_mutation = False
        anystr_upper = True
    


