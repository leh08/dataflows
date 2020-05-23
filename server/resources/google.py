from flask_restful import Resource
from oauth import oauth


class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        google = oauth.create_client('google')
        redirect_uri = "http://localhost:5000/google/login/authorized"
        return google.authorize_redirect(redirect_uri)
    

class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        google = oauth.create_client('google')
        token = google.authorize_access_token()
        google_user = google.get("oauth2/v3/userinfo", token=token)
        return google_user.json()