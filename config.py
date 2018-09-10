import os
import constants

DEBUG = True
ADMINS = frozenset([
    "yourname@yourdomain.com"
])
SECRET_KEY = os.urandom(24).hex()
UPLOAD_FOLDER = constants.UPLOAD_FOLDER
