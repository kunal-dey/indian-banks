from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from exceptions.db_connection_exceptions import DbConnectionException
from exceptions.schema_exceptions import IfscFormatException

from schemas.input_schemas.ifsc import Ifsc

from models.bank import BankModel


class BankResource(Resource):
    #@jwt_required()
    def get(self, ifsc_code:str):
        try:
            ifsc = Ifsc(ifsc_code=ifsc_code.upper())
        except IfscFormatException as err:
            return {
                "data":err.value,
                "msg":err.message
            }, 400
        try:
            banks = BankModel.find_by_ifsc(
                ifsc=ifsc,
                limit=request.args["limit"] if 'limit' in request.args.to_dict().keys() else None,
                offset=request.args["offset"] if 'offset' in request.args.to_dict().keys() else None
                )
        except DbConnectionException as err:
            return{
                "msg": err.message
            }, 500

        return {
            "data":(
                banks[0].dict() if len(banks) == 1 else [
                    bank.dict() for bank in banks
                ]
            ) if banks else None,
            "msg": f"Bank Details for IFSC code {ifsc_code}" if banks else "The item is not present"
        }, 200 if banks else 404