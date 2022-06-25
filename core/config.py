APP_HOST = '0.0.0.0'
APP_PORT = 5100

SQLITE_PATH = 'sqlite:///storages/doc_flow.db?check_same_thread=False'

APP_SECRET_KEY = '74fe8de852b371780a41d805d6a229244c61d604'

# 1 day = 60 sec * 60 min * 24 hours
SESSION_TTL_DEFAULT = 60 * 60 * 24

TMP_PATH_DEFAULT = './tmp'