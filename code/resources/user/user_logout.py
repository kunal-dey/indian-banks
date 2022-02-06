from flask_restful import Resource
from flask_jwt_extended import  jwt_required, get_jwt

from utils.blacklist import BLACKLIST


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {
            "msg": "Successfully logged out."
        }, 200
