import os

configs = {
    "google": {
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "scope": ["email", "profile"],
        "authorization_base_url": "https://accounts.google.com/o/oauth2/auth",
        "redirect_uri": 'http://localhost:5000/google/login/authorized',
        "token_url": "https://oauth2.googleapis.com/token",
        "base_url": 'https://www.googleapis.com/'
    }
}