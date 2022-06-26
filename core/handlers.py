import config
import errors
import consts
import storages
import services
from utils import SessionUtils, UserUtils, IPFSUtils, SearchUtils

import os
from fastapi.responses import JSONResponse


def sign_in_handler(data):
    try:
        username = data['username']
        password = data['password']

        auth = services.Auth()
        role = auth.sign_in(username, password)

        token = SessionUtils.set_token(username)

        content = {'info': consts.RESPONSE_SUCCESS, 'role': role}
        response = JSONResponse(content=content)
        response.set_cookie(key='token', value=token)

    except errors.TokenNotExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenNotCreatedError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.UserNotExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)

    return response


def sign_up_handler(data):
    try:
        username = data['username']
        password = data['password']

        auth = services.Auth()
        auth.sign_up(username, password)

        token = SessionUtils.set_token(username=username)

        content = {'info': consts.RESPONSE_SUCCESS, 'role': consts.ROLE_USER}
        response = JSONResponse(content=content)
        response.set_cookie(key='token', value=token)

    except errors.TokenNotExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenNotCreatedError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.UserNotCreatedError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.UserExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)

    return response


def sign_out_handler(token):
    try:
        SessionUtils.delete_token(token=token)

        content = {'info': consts.RESPONSE_SUCCESS}
        response = JSONResponse(content=content)
        response.set_cookie(key='token', value='')
    except errors.TokenNotExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenNotDeleteError as e:
        content = {'error': e}
        response = JSONResponse(content=content)

    return response


async def sign_file_handler(file, token):
    try:
        username = SessionUtils.get_username(token=token)
        private_key = UserUtils.get_key(username=username)

        if UserUtils.is_block(username=username):
            content = {'error': consts.USER_BLOCK_RESPONSE}
            response = JSONResponse(content=content)
            return response

        file_contents = await file.read()

        with open(f'{config.TMP_PATH_DEFAULT}/{file.filename}', 'wb') as f:
            f.write(file_contents)

        file.close()

        sign_file_inst = services.SignFile()
        public_key, signature = sign_file_inst.sign_file(
            private_key=private_key,
            filename=f'{config.TMP_PATH_DEFAULT}/{file.filename}'
        )

        json_data = {
            'username': username,
            'filename': file.filename,
            'public_key': public_key,
            'signature': signature
        }

        hash = storages.IPFS.add(json_data)

        blockchain = storages.Blockchain()
        blockchain.add(hash)

        os.remove(f'{config.TMP_PATH_DEFAULT}/{file.filename}')

        token = SessionUtils.update_token(token=token)

        content = {'info': consts.RESPONSE_SUCCESS, 'public_key': public_key, 'signature': signature}
        response = JSONResponse(content=content)
        response.set_cookie(key='token', value=token)
    except errors.TokenNotExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenNotCreatedError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenExpireError as e:
        content = {'error': e}
        response = JSONResponse(content=content)

    return response


async def check_sign_file_handler(data, file, token):
    try:
        public_key = data['public_key']
        signature = data['signature']

        print(public_key)
        print(signature)

        username = SessionUtils.get_username(token=token)

        if UserUtils.is_block(username=username):
            content = {'error': consts.USER_BLOCK_RESPONSE}
            response = JSONResponse(content=content)
            return response

        file_contents = await file.read()

        with open(f'{config.TMP_PATH_DEFAULT}/{file.filename}', 'wb') as f:
            f.write(file_contents)

        file.close()

        sign_file_check_inst = services.SignFileCheck()
        result = sign_file_check_inst.verify(
            filename=f'{config.TMP_PATH_DEFAULT}/{file.filename}',
            public_key=public_key,
            signature=signature
        )

        os.remove(f'{config.TMP_PATH_DEFAULT}/{file.filename}')

        token = SessionUtils.update_token(token=token)

        content = {'info': consts.RESPONSE_SUCCESS, 'result': result}
        response = JSONResponse(content=content)
        response.set_cookie(key='token', value=token)
    except errors.TokenNotExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenNotCreatedError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenExpireError as e:
        content = {'error': e}
        response = JSONResponse(content=content)

    return response


def manage_user_list_handler():
    pass


def manage_user_block_handler():
    pass


def manage_user_non_block_handler():
    pass


def doc_scan_list_handler(token):
    try:
        username = SessionUtils.get_username(token=token)

        if UserUtils.is_block(username=username):
            content = {'error': consts.USER_BLOCK_RESPONSE}
            response = JSONResponse(content=content)
            return response

        blockchain = storages.Blockchain()
        txs_uri = blockchain.match_txs_uri()
        extended_info_list = IPFSUtils.extend_info_by_uri(txs_uri)

        extended_info_list = SearchUtils.filter_by_user(
            extended_info_list=extended_info_list,
            username=username
        )

        token = SessionUtils.update_token(token=token)

        content = {'info': consts.RESPONSE_SUCCESS, 'list': extended_info_list}
        response = JSONResponse(content=content)
        response.set_cookie(key='token', value=token)
    except errors.TokenNotExistError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenNotCreatedError as e:
        content = {'error': e}
        response = JSONResponse(content=content)
    except errors.TokenExpireError as e:
        content = {'error': e}
        response = JSONResponse(content=content)

    return response



def doc_scan_search_handler():
    pass
