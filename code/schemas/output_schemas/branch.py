from pydantic import BaseModel

from schemas.input_schemas.ifsc import Ifsc


class Branch(BaseModel):

    ifsc: Ifsc
    district: str
    state: str
    address: str
    branch_name:str

    @classmethod
    def from_db(cls, 
        branch_name:str,
        ifsc_code:str,
        district: str,
        state: str,
        address: str):
        return cls(branch_name=branch_name, address=address,
                    district=district, state=state, ifsc=Ifsc(ifsc_code=ifsc_code))

    class Config:
        """Pydantic Config class"""
        anystr_upper = True
        allow_mutation = False