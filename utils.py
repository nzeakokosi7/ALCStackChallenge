from passlib.hash import pbkdf2_sha512
import constants


class Utils(object):

    @staticmethod
    def encrypt_password(password):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_encrypted_password(password, hashed_password):

        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in constants.ALLOWED_EXTENSIONS
