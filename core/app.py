import traceback

import config
import handlers
from storages import StorageORM, User, Session

import uvicorn
from fastapi import FastAPI, Request, Cookie, UploadFile, Form, File
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import UserAuth, SignFile, SignFileCheck


app = FastAPI()

storage_orm = StorageORM()
User.set_session(storage_orm.session)
Session.set_session(storage_orm.session)


@app.post('/signin')
async def sign_in(user_auth: UserAuth):
    json_compatible_data = jsonable_encoder(user_auth)
    response = handlers.sign_in_handler(json_compatible_data)
    return response


@app.post('/signup')
async def sign_up(user_auth: UserAuth):
    json_compatible_data = jsonable_encoder(user_auth)
    response = handlers.sign_up_handler(json_compatible_data)
    return response


@app.post('/signout')
async def sign_out(token=Cookie(None)):
    response = handlers.sign_out_handler(token)
    return response


@app.post('/sign/file')
async def sign_file(file: UploadFile, token=Cookie(None)):
    response = await handlers.sign_file_handler(file, token)
    return response


@app.post('/check/sign/file')
async def check_sign_file(
        public_key: str = Form(...),
        signature: str = Form(...),
        file: UploadFile = File(...),
        token=Cookie(None)
    ):
    data = {
        'public_key': public_key,
        'signature': signature
    }

    response = await handlers.check_sign_file_handler(data, file, token)
    return response

# @app.post('/test')
# async def test():
#     import storages
#
#     contract = storages.deploy_contract()
#     print(contract)
#     return JSONResponse({'data': storages.get_transactions_list()})


@app.post('/manage/user/list')
async def manage_user_list(request: Request):
    data = await request.json()
    content = handlers.manage_user_list_handler()
    response = JSONResponse(content=content)
    return response


@app.post('/manage/user/block')
async def manage_user_block(request: Request):
    data = await request.json()
    content = handlers.manage_user_block_handler()
    response = JSONResponse(content=content)
    return response


@app.post('/manage/user/nonblock')
async def manage_user_non_block(request: Request):
    data = await request.json()
    content = handlers.manage_user_non_block_handler()
    response = JSONResponse(content=content)
    return response


@app.get('/doc/scan/list')
async def doc_scan_list():
    content = handlers.doc_scan_list_handler()
    response = JSONResponse(content=content)
    return response


@app.post('/doc/scan/search')
async def doc_scan_search(request: Request):
    data = await request.json()
    content = handlers.doc_scan_search_handler()
    response = JSONResponse(content=content)
    return response


def main():
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
