from flask_restful import Resource
from flask import request
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from passlib.hash import pbkdf2_sha256

from exceptions.missing_exception import MissingValueException
from exceptions.db_connection_exceptions import DbConnectionException

from models.user import UserModel

class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            if "username" not in data.keys():
                raise MissingValueException("username")
            elif "password" not in data.keys():
                raise MissingValueException("password")
            
        except MissingValueException as miss:
            return {
                "msg":miss.message
            }
        try:
            user_model = UserModel.find_by_username(username=data["username"])
        except DbConnectionException as err:
            return {
                "msg":err.message
            }, 500
        
        if user_model and pbkdf2_sha256.verify(data["password"],user_model.user.password):
            access_token = create_access_token(
                user_model.user.id,
                fresh=True, 
                expires_delta=timedelta(minutes=15)
            )
            refresh_token = create_refresh_token(
                user_model.user.id,
                expires_delta=timedelta(days=5)
            )
            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            }, 200
        
        return {'msg':'Invalid credentials.'}, 401
