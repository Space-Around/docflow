USER_EXIST_ERROR = 'User exist'
USER_NOT_EXIST_ERROR = 'User not exist'
USER_NOT_CRETAED_ERROR = 'User not created'
TOKEN_NOT_CREATED_ERROR = 'Token not cretaed'
TOKEN_NOT_EXIST_ERROR = 'Token not exist'
TOKEN_NOT_DELETE_ERROR = 'Token not delete'
TOKEN_EXPIRE_ERROR = 'Token expire'


class UserExistError(Exception):
    pass


class UserNotExistError(Exception):
    pass


class UserNotCreatedError(Exception):
    pass


class TokenNotCreatedError(Exception):
    pass


class TokenNotExistError(Exception):
    pass


class TokenNotDeleteError(Exception):
    pass


class TokenExpireError(Exception):
    pass