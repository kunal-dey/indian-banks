from flask_restful import Resource
from flask import request

from exceptions.password_format_exception import PasswordFormatException

from exceptions.missing_exception import MissingValueException
from exceptions.db_connection_exceptions import DbConnectionException

from models.user import UserModel

from schemas.user import User


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            if "username" not in data.keys():
                raise MissingValueException("username")
            elif "password" not in data.keys():
                raise MissingValueException("password")
            
        except MissingValueException as miss:
            return {
                "msg":miss.message
            }, 401
        try:
            if UserModel.find_by_username(username=data["username"]):
                return {
                    "msg":f"An user with username {data['username']} already exists."
                }, 400
        except DbConnectionException as err:
            return {
                "msg":err.message
            }, 500

        try:
            user_model = UserModel(
                user=User(
                    username=data["username"],
                    password=data["password"],
                    from_request=True
                )
            )
        except PasswordFormatException as err:
            return {
                "msg":err.message
            }, 400

        try:
            user_model.save_to_db()
        except DbConnectionException as err:
            return {
                "msg":err.message
            }, 500
        
        return {
            "msg":f"User with username {user_model.user.username} has been added.",
        }, 201
