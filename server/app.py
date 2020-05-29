from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class

from dotenv import load_dotenv
load_dotenv(".env", verbose=True)
from database import db_session, init_db
from blacklist import BLACKLIST
from resources.user import (
    User, Signup, Login, Logout, TokenRefresh, CurrentUser, Resend
)
from resources.confirmation import Confirmation
from resources.log import LogList, Log
from resources.source import SourceList, Source
from resources.authorization import AuthorizationList, Authorization
from resources.flow import FlowList, Flow
from resources.file import Upload
from resources.google import GoogleLogin, GoogleAuthorize
from services.uploads import UPLOAD_SET

app = Flask(__name__)
# Default config
app.config.from_pyfile("default_config.py")
# Update new parameters in config
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 10 * 1024 * 1024 * 1024) # 10GB max size upload
configure_uploads(app, UPLOAD_SET)
api = Api(app)
jwt = JWTManager(app)
CORS(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (decrypted_token["jti"] in BLACKLIST)  # Here we blacklist particular JWTs that have been created in the past.

api.add_resource(SourceList, "/sources")
api.add_resource(Source, "/sources/<int:source_id>")
api.add_resource(AuthorizationList, "/authorizations")
api.add_resource(Authorization, "/authorizations/<int:authorization_id>")
api.add_resource(FlowList, "/flows")
api.add_resource(Flow, "/flows/<int:flow_id>")
api.add_resource(LogList, "/logs")
api.add_resource(Log, "/logs/<int:log_id>")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(Logout, "/logout")
api.add_resource(CurrentUser, "/user")
api.add_resource(Resend, "/resend")
api.add_resource(Confirmation, "/confirmation/<string:confirmation_id>")
api.add_resource(Upload, "/upload/<string:flow_name>")
api.add_resource(GoogleLogin, "/google/login")
api.add_resource(GoogleAuthorize, "/google/login/authorized")

if __name__ == "__main__":
    init_db()
    app.run(port=5000)

