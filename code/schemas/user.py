from lib2to3.pgen2.token import OP
from typing import Optional
from pydantic import BaseModel, root_validator, validator
from exceptions.password_format_exception import PasswordFormatException
from passlib.hash import pbkdf2_sha256

from exceptions.type_exception import TypeException

def _check_upper_character(val: str):
    for character in val:
        if character.isupper():
            return character.isupper()
    return False

def _check_lower_character(val: str):
    for character in val:
        if character.islower():
            return character.islower()
    return False

def _check_numbers(val: str):
    for character in val:
        if character in '0123456789':
            return True
    return False



class User(BaseModel):
    id: Optional[int]
    from_request: bool
    username: str
    password: str

    @validator("password")
    @classmethod
    def valid_ifsc_code(cls, value, values):
        """
            Validator to check whether the password contains required characters
        """

        if 'from_request' in values and values['from_request']:
            if len(value) < 8:
                raise PasswordFormatException("Password must be of atleast 8 characters long.")

            if not _check_numbers(val=value):
                raise  PasswordFormatException("Password must contain a number.")

            if not _check_upper_character(val=value):
                raise PasswordFormatException("Password must contain a capital letter.")

            if not _check_lower_character(val=value):
                raise PasswordFormatException("Password must contain a small letter.")

        return pbkdf2_sha256.hash(value)


    @classmethod
    def from_db(cls, _id: int, username: str, password: str):
        return cls(id=_id, username=username, password=password, from_request=False)

    class Config:
        """Pydantic Config class"""

        allow_mutation = False
