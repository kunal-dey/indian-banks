from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from utils.config_files import CONFIG

from utils.blacklist import BLACKLIST
from utils.create_user_table import create_user_table

from resources.user.user_login import UserLogin
from resources.user.user_register import UserRegister
from resources.user.user_logout import UserLogout
from resources.token_refresh import TokenRefresh
from resources.branch import BranchResource
from resources.bank import BankResource


app = Flask(__name__)
app.secret_key = CONFIG['app']['secret']
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] =True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
api = Api(app)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    create_user_table()


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'msg': "The token has expired.",
        'error': 'invalid_token'
    }), 401

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(extra,decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.invalid_token_loader
def invalid_token_callback(err):
    return jsonify({
        'msg': 'Signature verification failed.',
        'error': 'invalid_token'
    })

@jwt.unauthorized_loader
def unauthorized_token_callback(val):
    return jsonify({
        'msg':'You are unauthorized to access it. Kindly login.',
        'error':'authorization_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description':f"{jwt_payload['type']} token has been revoked",
        'error': 'token_revoked'
    }), 401

@app.route("/")
def home():
    return {
        "msg":"Welcome to the Bank Branches API."
    }

api.add_resource(BankResource,"/banks/<string:ifsc_code>")
api.add_resource(BranchResource,"/branches/<string:bank_name>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == "__main__":
    app.run(port=5000)