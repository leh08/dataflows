from flask import redirect, request
from flask_restful import Resource

from models.source import SourceModel
from models.authorization import AuthorizationModel
from services.oauths import oauth
"""
Use google-api-python-client library for Google is
easiest way. rather than OAuthlib
"""

class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        authorization_url = oauth.get_service('Google').get_authorization_url()
        
        return redirect(
            authorization_url,
            code=302
        )


class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        authorization_response = request.url
        google = oauth.get_service('Google')
        token = google.get_token(authorization_response)
        client = google.create_client(token)
        response = client.get('https://www.googleapis.com/oauth2/v3/userinfo')
        
        data_json = response.json()
        
        source = SourceModel.find_by_name('Google')
        authorization = AuthorizationModel(name=data_json['email'], credential=token, source=source)
        authorization.save_to_db()

        return data_json