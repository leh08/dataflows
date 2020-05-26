import os

DEBUG = True
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"] # For encrypting JWT token
SECRET_KEY = os.environ["SECRET_KEY"] # For encrypting cookie
UPLOADED_FILES_DEST = os.path.join("stores", "files")
JWT_ACCESS_TOKEN_EXPIRES = False
JWT_BLACKLIST_ENABLED = True  # enable blacklist feature
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"] # allow blacklisting for access and refresh tokens