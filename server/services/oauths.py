from functools import partial
from flask import session
from auths.oauth import configs
from requests_oauthlib import OAuth2Session


class OAuth:
    def __init__(
        self,
        token_fetcher=None,
        token_updater=None,
    ):
        self.platforms = {}
        self.token_fetcher = token_fetcher
        self.token_updater = token_updater
        
    def register_service(
        self, name,
        client_id=None,
        client_secret=None,
        scope=None,
        authorization_base_url=None,
        redirect_uri=None,
        token_url=None,
        base_url=None,
    ):  
        config = configs.get(name)

        service = OAuthService(
            name,
            token_fetcher = self.token_fetcher,
            token_updater = self.token_updater,
            **config
        )
        
        self.platforms[name] = service
    
    def get_service(self, name):
        return self.platforms[name]
    
    
class OAuthService:
    def __init__(
        self, name,
        client_id=None,
        client_secret=None,
        scope=None,
        authorization_base_url=None,
        redirect_uri=None,
        token_url=None,
        base_url=None,
        token_fetcher=None,
        token_updater=None
        ):
        self.name = name
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.authorization_base_url = authorization_base_url
        self.redirect_uri = redirect_uri
        self.token_url = token_url
        self.base_url = base_url
        
        self.token_fetcher = token_fetcher
        self.token_updater = token_updater
    
    def create_client(self, token=None, account=None):
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        
        if token:
            
            client = OAuth2Session(
                self.client_id,
                token=token,
                auto_refresh_kwargs=extra,
                auto_refresh_url=self.token_url,
                token_updater=self.token_updater,
            )
        else:
            if self.token_fetcher is None:
                raise TypeError("Token must be provided.")
            
            token = self.token_fetcher(self.name, account=account)
                    
            try:
                token_updater = partial(self.token_updater, name=self.name, account=account)
            
            except:
                def default_token_updater(token, name, account=None):
                    if account is None:
                        session['oauth_token'][name] = token
                        
                    else:
                        session['oauth_token'][name][account] = token
                        
                token_updater = partial(default_token_updater, name=self.name, account=account)

            client = OAuth2Session(
                self.client_id,
                token=token,
                auto_refresh_kwargs=extra,
                auto_refresh_url=self.token_url,
                token_updater=token_updater,
            )

        return client
            
    def get_authorization_url(self):
        client = OAuth2Session(
            self.client_id,
            scope=self.scope,
            redirect_uri=self.redirect_uri
        )
        
        authorization_url, state = client.authorization_url(
            self.authorization_base_url,
            access_type="offline",
            prompt="select_account"
        )
    
        # State is used to prevent CSRF, keep this for later.
        session['oauth_state'] = state
        
        return authorization_url

    def get_token(self, authorization_response):
        client = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, state=session['oauth_state'])
        token = client.fetch_token(self.token_url, client_secret=self.client_secret,
                                   authorization_response=authorization_response)

        return token
    
oauth = OAuth()
oauth.register_service('google')