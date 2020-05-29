from typing import Callable, Optional, Dict
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
        token_updater=None
        token_fetcher=None
    ):
        config = configs.get(name)
        self.name = name
        
        self._client_id = client_id or config.get('client_id')
        self._client_secret = client_secret or config.get('client_secret')
        self._scope = scope or config.get('scope')
        self._authorization_base_url = authorization_base_url or config.get('authorization_base_url')
        self._redirect_uri = redirect_uri or config.get('redirect_uri')
        self._token_url = token_url or config.get('token_url')
        self._base_url = base_url or config.get('base_url')
        self._token_updater = token_updater
        self._token_fetcher = token_fetcher
        
    def create_client(self, name, account=None, token=None):
        extra = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }
        if token:

            def token_updater(token, account):
                session['oauth_token'][account] = token
            
            token_updater = partial(token_updater, account=account)
            
            client = OAuth2Session(
                self._client_id,
                token=token,
                auto_refresh_kwargs=extra,
                auto_refresh_url=self._token_url,
                token_updater=token_updater,
            )
        else:
            if self._token_updater is None:
                raise NotImplementedError("Token must be provided.")
            client = OAuth2Session(
                self._client_id,
                token=token,
                auto_refresh_kwargs=extra,
                auto_refresh_url=self._token_url,
                token_updater=None,
            )

        return client
    
    def get_authorization_url(self):
        client = OAuth2Session(
            self._client_id,
            scope=self._scope,
            redirect_uri=self._redirect_uri
        )
        
        authorization_url, state = client.authorization_url(
            self._authorization_base_url,
            access_type="offline",
            prompt="select_account"
        )
    
        # State is used to prevent CSRF, keep this for later.
        session['oauth_state'] = state
        
        return authorization_url

    def get_token(self, authorization_response):
        client = OAuth2Session(self._client_id, redirect_uri=self._redirect_uri, state=session['oauth_state'])
        token = client.fetch_token(self._token_url, client_secret=self._client_secret,
                                   authorization_response=authorization_response)
        if _
        return token

    
oauth = OAuth('google')

#    @staticmethod
#    def http_request(uri, headers=None, data=None, method=None):
#        uri, headers, data, method = prepare_request(
#            uri, headers, data, method
#        )
#
#        log.debug('Request %r with %r method' % (uri, method))
#        req = http.Request(uri, headers=headers, data=data)
#        req.get_method = lambda: method.upper()
#        try:
#            resp = http.urlopen(req)
#            content = resp.read()
#            resp.close()
#            return resp, content
#        except http.HTTPError as resp:
#            content = resp.read()
#            resp.close()
#            return resp, content
#
#    def get(self, *args, **kwargs):
#        """Sends a ``GET`` request. Accepts the same parameters as
#        :meth:`request`.
#        """
#        kwargs['method'] = 'GET'
#        return self.request(*args, **kwargs)
#
#    def post(self, *args, **kwargs):
#        """Sends a ``POST`` request. Accepts the same parameters as
#        :meth:`request`.
#        """
#        kwargs['method'] = 'POST'
#        return self.request(*args, **kwargs)
#
#    def put(self, *args, **kwargs):
#        """Sends a ``PUT`` request. Accepts the same parameters as
#        :meth:`request`.
#        """
#        kwargs['method'] = 'PUT'
#        return self.request(*args, **kwargs)
#
#    def delete(self, *args, **kwargs):
#        """Sends a ``DELETE`` request. Accepts the same parameters as
#        :meth:`request`.
#        """
#        kwargs['method'] = 'DELETE'
#        return self.request(*args, **kwargs)
#
#    def patch(self, *args, **kwargs):
#        """Sends a ``PATCH`` request. Accepts the same parameters as
#        :meth:`post`.
#        """
#        kwargs['method'] = 'PATCH'
#        return self.request(*args, **kwargs)
#
#    def request(self, url, data=None, headers=None, format='urlencoded',
#                method='GET', content_type=None, token=None):
#        """
#        Sends a request to the remote server with OAuth tokens attached.
#        :param data: the data to be sent to the server.
#        :param headers: an optional dictionary of headers.
#        :param format: the format for the `data`. Can be `urlencoded` for
#                       URL encoded data or `json` for JSON.
#        :param method: the HTTP request method to use.
#        :param content_type: an optional content type. If a content type
#                             is provided, the data is passed as it, and
#                             the `format` is ignored.
#        :param token: an optional token to pass, if it is None, token will
#                      be generated by tokengetter.
#        """
#
#        headers = dict(headers or {})
#        if token is None:
#            token = self.get_request_token()
#
#        client = self.make_client(token)
#        url = self.expand_url(url)
#        if method == 'GET':
#            assert format == 'urlencoded'
#            if data:
#                url = add_params_to_uri(url, data)
#                data = None
#        else:
#            if content_type is None:
#                data, content_type = encode_request_data(data, format)
#            if content_type is not None:
#                headers['Content-Type'] = content_type
#
#        if self._token_url:
#            # oauth1
#            uri, headers, body = client.sign(
#                url, http_method=method, body=data, headers=headers
#            )
#        else:
#            # oauth2
#            uri, headers, body = client.add_token(
#                url, http_method=method, body=data, headers=headers
#            )
#
#        if hasattr(self, 'pre_request'):
#            # This is designed for some rubbish services like weibo.
#            # Since they don't follow the standards, we need to
#            # change the uri, headers, or body.
#            uri, headers, body = self.pre_request(uri, headers, body)
#
#        if body:
#            data = to_bytes(body, self.encoding)
#        else:
#            data = None
#        resp, content = self.http_request(
#            uri, headers, data=to_bytes(body, self.encoding), method=method
#        )
#        return OAuthResponse(resp, content, self.content_type)
#
#    def authorize(self, callback=None, state=None, **kwargs):
#        """
#        Returns a redirect response to the remote authorization URL with
#        the signed callback given.
#        :param callback: a redirect url for the callback
#        :param state: an optional value to embed in the OAuth request.
#                      Use this if you want to pass around application
#                      state (e.g. CSRF tokens).
#        :param kwargs: add optional key/value pairs to the query string
#        """
#        params = dict(self.request_token_params) or {}
#        params.update(**kwargs)
#
#        if self._token_url:
#            token = self.generate_request_token(callback)[0]
#            url = '%s?oauth_token=%s' % (
#                self.expand_url(self.authorize_url), url_quote(token)
#            )
#            if params:
#                url += '&' + url_encode(params)
#        else:
#            assert callback is not None, 'Callback is required for OAuth2'
#
#            client = self.make_client()
#
#            if 'scope' in params:
#                scope = params.pop('scope')
#            else:
#                scope = None
#
#            if isinstance(scope, str):
#                # oauthlib need unicode
#                scope = _encode(scope, self.encoding)
#
#            if 'state' in params:
#                if not state:
#                    state = params.pop('state')
#                else:
#                    # remove state in params
#                    params.pop('state')
#
#            if callable(state):
#                # state can be function for generate a random string
#                state = state()
#
#            session['%s_oauthredir' % self.name] = callback
#            url = client.prepare_request_uri(
#                self.expand_url(self.authorize_url),
#                redirect_uri=callback,
#                scope=scope,
#                state=state,
#                **params
#            )
#        return redirect(url)
#
#    def tokengetter(self, f):
#        """
#        Register a function as token getter.
#        """
#        self._tokengetter = f
#        return f
#
#    def expand_url(self, url):
#        return urljoin(self.base_url, url)
#
#    def generate_request_token(self, callback=None):
#        # for oauth1 only
#        if callback is not None:
#            callback = urljoin(request.url, callback)
#
#        client = self.make_client()
#        client.callback_uri = _encode(callback, self.encoding)
#
#        realm = self.request_token_params.get('realm')
#        realms = self.request_token_params.get('realms')
#        if not realm and realms:
#            realm = ' '.join(realms)
#        uri, headers, _ = client.sign(
#            self.expand_url(self._token_url),
#            http_method=self.request_token_method,
#            realm=realm,
#        )
#        log.debug('Generate request token header %r', headers)
#        resp, content = self.http_request(
#            uri, headers, method=self.request_token_method,
#        )
#        data = parse_response(resp, content)
#        if not data:
#            raise OAuthException(
#                'Invalid token response from %s' % self.name,
#                type='token_generation_failed'
#            )
#        if resp.code not in (200, 201):
#            message = 'Failed to generate request token'
#            if 'oauth_problem' in data:
#                message += ' (%s)' % data['oauth_problem']
#            raise OAuthException(
#                message,
#                type='token_generation_failed',
#                data=data,
#            )
#        tup = (data['oauth_token'], data['oauth_token_secret'])
#        session['%s_oauthtok' % self.name] = tup
#        return tup
#
#    def get_request_token(self):
#        assert self._tokengetter is not None, 'missing tokengetter'
#        rv = self._tokengetter()
#        if rv is None:
#            raise OAuthException('No token available', type='token_missing')
#        return rv
#
#    def handle_oauth1_response(self, args):
#        """Handles an oauth1 authorization response."""
#        client = self.make_client()
#        client.verifier = args.get('oauth_verifier')
#        tup = session.get('%s_oauthtok' % self.name)
#        if not tup:
#            raise OAuthException(
#                'Token not found, maybe you disabled cookie',
#                type='token_not_found'
#            )
#        client.resource_owner_key = tup[0]
#        client.resource_owner_secret = tup[1]
#
#        uri, headers, data = client.sign(
#            self.expand_url(self.access_token_url),
#            _encode(self.access_token_method)
#        )
#        headers.update(self._access_token_headers)
#
#        resp, content = self.http_request(
#            uri, headers, to_bytes(data, self.encoding),
#            method=self.access_token_method
#        )
#        data = parse_response(resp, content)
#        if resp.code not in (200, 201):
#            raise OAuthException(
#                'Invalid response from %s' % self.name,
#                type='invalid_response', data=data
#            )
#        return data
#
#    def handle_oauth2_response(self, args):
#        """Handles an oauth2 authorization response."""
#
#        client = self.make_client()
#        remote_args = {
#            'code': args.get('code'),
#            'client_secret': self.consumer_secret,
#            'redirect_uri': session.get('%s_oauthredir' % self.name)
#        }
#        log.debug('Prepare oauth2 remote args %r', remote_args)
#        remote_args.update(self.access_token_params)
#        headers = copy(self._access_token_headers)
#        if self.access_token_method == 'POST':
#            headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
#            body = client.prepare_request_body(**remote_args)
#            resp, content = self.http_request(
#                self.expand_url(self.access_token_url),
#                headers=headers,
#                data=to_bytes(body, self.encoding),
#                method=self.access_token_method,
#            )
#        elif self.access_token_method == 'GET':
#            qs = client.prepare_request_body(**remote_args)
#            url = self.expand_url(self.access_token_url)
#            url += ('?' in url and '&' or '?') + qs
#            resp, content = self.http_request(
#                url,
#                headers=headers,
#                method=self.access_token_method,
#            )
#        else:
#            raise OAuthException(
#                'Unsupported access_token_method: %s' %
#                self.access_token_method
#            )
#
#        data = parse_response(resp, content, content_type=self.content_type)
#        if resp.code not in (200, 201):
#            raise OAuthException(
#                'Invalid response from %s' % self.name,
#                type='invalid_response', data=data
#            )
#        return data
#
#    def handle_unknown_response(self):
#        """Handles a unknown authorization response."""
#        return None
#
#    def authorized_response(self, args=None):
#        """Handles authorization response smartly."""
#        if args is None:
#            args = request.args
#        if 'oauth_verifier' in args:
#            data = self.handle_oauth1_response(args)
#        elif 'code' in args:
#            data = self.handle_oauth2_response(args)
#        else:
#            data = self.handle_unknown_response()
#
#        # free request token
#        session.pop('%s_oauthtok' % self.name, None)
#        session.pop('%s_oauthredir' % self.name, None)
#        return data
#
#    def authorized_handler(self, f):
#        """Handles an OAuth callback.
#        .. versionchanged:: 0.7
#           @authorized_handler is deprecated in favor of authorized_response.
#        """
#        @wraps(f)
#        def decorated(*args, **kwargs):
#            log.warn(
#                '@authorized_handler is deprecated in favor of '
#                'authorized_response'
#            )
#            data = self.authorized_response()
#            return f(*((data,) + args), **kwargs)
#        return decorated
