from flask import redirect, request
from flask_restful import Resource

"""
Use google-api-python-client library for Google is
easiest way. rather than OAuthlib
"""

class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        authorization_url = ""
        return redirect(
            authorization_url,
            code=302,
            Response={"message": gettext("confirmation_confirmed")}
        )

class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        authorization_response = request.url
        