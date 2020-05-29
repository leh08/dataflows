from flask import redirect, request, session
from flask_restful import Resource

from services.oauth import oauth
"""
Use google-api-python-client library for Google is
easiest way. rather than OAuthlib
"""

class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        authorization_url = oauth.get_authorization_url()
        
        return redirect(
            authorization_url,
            code=302
        )


class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        authorization_response = request.url
        token = oauth.get_token(authorization_response)
        client = oauth.create_client(token)
        response = client.get('https://www.googleapis.com/oauth2/v1/userinfo')
        email = response.json()['email']
        session['oauth_token'][email] = token

        return response.json()