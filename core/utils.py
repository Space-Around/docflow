from storages import User, Session, IPFS
import errors
import consts
from uuid import uuid4
import config
import json
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


class IPFSUtils:
    @classmethod
    def extend_info_by_uri(cls, txs_uri_list):
        for tx_uri in txs_uri_list:
            data = IPFS.cat(tx_uri['uri']).decode("utf-8")
            data_dict = json.loads(json.loads(data))
            tx_uri['info'] = data_dict

        return txs_uri_list

class SearchUtils:
    @classmethod
    def filter_by_user(cls, extended_info_list, username=''):
        extended_info_new_list = []

        for extened_info in extended_info_list:
            if extened_info['info']['username'] == username:
                extended_info_new_list.append(extened_info)

        return extended_info_new_list

    @classmethod
    def search(cls, extened_info_list, keyword=''):
        extened_info_new_list = []

        for extened_info in extened_info_list:
            if keyword in extened_info['tx'] or \
               keyword in extened_info['uri'] or \
               keyword in extened_info['info']['username'] or \
               keyword in extened_info['info']['filename'] or \
               keyword in extened_info['info']['public_key'] or \
               keyword in extened_info['info']['signature']:
                extened_info_new_list.append(extened_info)
        return extened_info_new_list