
# File store.py 
# Created at 11/05/2023
# Author Khanh

"""
    - Exception of store
"""


from src.constants import Constants
from vibe_library.exceptions import RequestException
from vibe_library.handlerespon import make_response

class ExceptionStoreExists(RequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='E_STORE_ALREADY_EXISTS',
            status=Constants.STATUS_NOT_OK,
            msg='store.error.store_already_exists'
        )

    pass
