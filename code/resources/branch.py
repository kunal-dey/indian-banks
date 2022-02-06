from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from exceptions.db_connection_exceptions import DbConnectionException

from models.branch import BranchModel


class BranchResource(Resource):
    @jwt_required()
    def get(self, bank_name):
        if 'city' not in request.args.to_dict().keys():
            return {
                "msg":"City is required as a query parameter."
            }, 403

        try:
            city= request.args["city"]
            branches = BranchModel.find_by_bank_and_city(
                bank_name=bank_name,
                city=request.args["city"],
                limit=request.args["limit"] if 'limit' in request.args.to_dict().keys() else None,
                offset=request.args["offset"] if 'offset' in request.args.to_dict().keys() else None
            )
        except DbConnectionException as err:
            return {
                "msg": err.message
            }, 500

        return {
            "data":[
                    branch.dict() for branch in branches
                ] if branches else None,
            "msg": f"""
                Bank Details for the Bank-{bank_name} in city {city}
            """ if branches else "The item is not present"
        }, 200 if branches else 404
