from storages import User, Session
import errors
import consts
from uuid import uuid4
import config
import datetime


class UserUtils:
    @classmethod
    def is_block(cls, username):
        user = User.get_by_username(username=username)

        if not user:
            raise errors.UserNotExistError(errors.USER_NOT_EXIST_ERROR)

        return True if user.is_block == consts.USER_BLOCK else False

    @classmethod
    def get_key(cls, username):
        user = User.get_by_username(username)

        if not user:
            raise errors.UserNotExistError(errors.USER_NOT_EXIST_ERROR)

        return user.key


class SessionUtils:
    @classmethod
    def set_token(cls, username):
        token = str(uuid4())
        current_ts = datetime.datetime.now().timestamp()
        ttl = current_ts + config.SESSION_TTL_DEFAULT

        sess = Session.add(
            username=username,
            token=token,
            ttl=ttl
        )

        if not sess:
            raise errors.TokenNotCreatedError(errors.TOKEN_NOT_CREATED_ERROR)

        return token

    @classmethod
    def update_token(cls, token=''):
        sess = Session.get(token=token)

        if not sess:
            raise errors.TokenNotExistError(errors.TOKEN_NOT_EXIST_ERROR)

        token = str(uuid4())
        current_ts = datetime.datetime.now().timestamp()
        ttl = current_ts + config.SESSION_TTL_DEFAULT

        if current_ts >= sess.ttl:
            raise errors.TokenExpireError(errors.TOKEN_EXPIRE_ERROR)

        Session.update(
            username=sess.username,
            token=token,
            ttl=ttl
        )

        if not sess:
            raise errors.TokenNotCreatedError(errors.TOKEN_NOT_CREATED_ERROR)

        return token

    @classmethod
    def delete_token(cls, token=''):
        sess = Session.get(token=token)

        if not sess:
            raise errors.TokenNotExistError(errors.TOKEN_NOT_EXIST_ERROR)

        if not Session.delete(token=token):
            raise errors.TokenNotDeleteError(errors.TOKEN_NOT_DELETE_ERROR)

    @classmethod
    def get_username(cls, token=''):
        sess = Session.get(token=token)

        if not sess:
            raise errors.TokenNotExistError(errors.TOKEN_NOT_EXIST_ERROR)

        return sess.username
