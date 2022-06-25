import consts
import errors
from storages import User

import os
from Crypto.PublicKey import RSA


class Auth:
    def sign_up(self, username, password):
        if User.get_by_username(username):
            raise errors.UserExistError

        key = RSA.generate(1024, os.urandom).export_key().decode('utf8')

        if not User.add(username, password, key):
            raise errors.UserNotCreatedError(errors.USER_NOT_CRETAED_ERROR)

    def sign_in(self, username, password):
        user = User.get_by_username_and_password(username, password)

        if not user:
            raise errors.UserNotExistError(errors.USER_NOT_EXIST_ERROR)

        return consts.ROLE_USER_TEXT if user.role == 0 else consts.ROLE_ADMIN_TEXT
