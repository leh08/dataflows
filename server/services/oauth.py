from functools import partial
from flask import session
from auths.oauth import configs
from requests_oauthlib import OAuth2Session


class OAuth:
    def __init__(
        self, name,
        client_id=None,
        client_secret=None,
        scope=None,
        authorization_base_url=None,
        redirect_uri=None,
        token_url=None,
        base_url=None,
        token_updater=None,
        token_fetcher=None
    ):
        config = configs.get(name)
        self.name = name
        
        self.client_id = client_id or config.get('client_id')
        self.client_secret = client_secret or config.get('client_secret')
        self.scope = scope or config.get('scope')
        self.authorization_base_url = authorization_base_url or config.get('authorization_base_url')
        self.redirect_uri = redirect_uri or config.get('redirect_uri')
        self.token_url = token_url or config.get('token_url')
        self.base_url = base_url or config.get('base_url')
        self.token_updater = token_updater
        self.token_fetcher = token_fetcher
        
    def create_client(self, token=None, account=None):
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        def token_updater(token, name, account=None):
            if account is None:
                session['oauth_token'][name] = token
                
            else:
                session['oauth_token'][name][account] = token
        
        try:
            token_updater = partial(self.token_updater, name=self.name, account=account)
        
        except:  
            token_updater = partial(token_updater, name=self.name, account=account)
            
        if token:
            
            client = OAuth2Session(
                self.client_id,
                token=token,
                auto_refresh_kwargs=extra,
                auto_refresh_url=self.token_url,
                token_updater=token_updater,
            )
        else:
            if self.token_fetcher is None:
                raise TypeError("Token must be provided.")
            
            token = self.token_fetcher(self.name, account=account)
            
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