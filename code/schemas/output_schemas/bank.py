from pydantic import BaseModel


class Bank(BaseModel):

    branch_name:str
    address: str
    city:str
    district: str
    state: str
    bank_name:str

    @classmethod
    def from_db(cls, 
        branch_name:str,
        address: str,
        city:str,
        district: str,
        state: str,
        bank_name:str):
        return cls(branch_name=branch_name, address=address,
                    city=city, district=district, state=state, bank_name=bank_name)

    class Config:
        """Pydantic Config class"""
        anystr_upper = True
        allow_mutation =False
    


