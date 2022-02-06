from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from utils.blacklist import BLACKLIST


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            "access_token":new_token
        }, 200
