import logging
from functools import wraps
from flask_smorest import abort
from flask_api.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError

from globals import HTTP_422_UNPROCESSABLE_ENTITY


def thread_handle_error(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        try:
            resp = f(*args, **kws)
            return resp
        except Exception as ex:
            logging.error(str(ex))

    return decorated_function


def service_handle_error(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        try:
            resp = f(*args, **kws)
            return resp
        except IntegrityError as ie:
            logging.error(str(ie))
            abort(HTTP_422_UNPROCESSABLE_ENTITY, message=[str(ie)])
        except OperationalError as oe:
            logging.error(str(oe))
            abort(HTTP_500_INTERNAL_SERVER_ERROR, message=[str(oe)])
        except DatabaseError as ie:
            logging.error(str(ie))
            abort(HTTP_422_UNPROCESSABLE_ENTITY, message=[str(ie)])
        except Exception as ex:
            logging.error(str(ex))
            abort(HTTP_500_INTERNAL_SERVER_ERROR, message=[str(ex)])

    return decorated_function
