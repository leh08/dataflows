from flask import redirect, request
from flask_restful import Resource

from services.oauth import OAuth
"""
Use google-api-python-client library for Google is
easiest way. rather than OAuthlib
"""

class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        authorization_url = OAuth('google').get_authorization_url()
        
        return redirect(
            authorization_url,
            code=302
        )


class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        authorization_response = request.url
        token = OAuth('google').get_token(authorization_response)
        client = OAuth('google').create_client(token)
        response = client.get('https://www.googleapis.com/oauth2/v1/userinfo')

        return response.json()