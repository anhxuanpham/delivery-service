# File auth.py 
# Created at 25/03/2023
# Author Khanh

"""
    - Exception of user
"""


from src.constants import Constants
from vibe_library.exceptions import RequestException
from vibe_library.handlerespon import make_response


class ExceptionUserNotExists(RequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='E_USER_NOT_EXISTS',
            status=Constants.STATUS_NOT_OK,
            msg='auth.error.user_not_exists'
        )

    pass

class ExceptionUserHasBlocked(RequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='E_USER_HAS_BLOCKED',
            status=Constants.STATUS_NOT_OK,
            msg='auth.error.user_has_blocked'
        )

    pass

class ExceptionUserAccountNotExists(RequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='E_USER_ACCOUNT_NOT_EXISTS',
            status=Constants.STATUS_NOT_OK,
            msg='auth.error.user_account_not_exists'
        )

    pass

class TokenNotAccept(RequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='ERROR_REFRESH_TOKEN',
            status=Constants.STATUS_NOT_OK,
            msg='This refresh token don\'t accept'
        )

    pass

class InvalidDateFormat(RequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='Invalid_Date_Format',
            status=Constants.STATUS_NOT_OK,
            msg='This date is not valid'
        )
