from typing import Any, Dict, Generator, List, Sequence

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from starlette.requests import Request

from .translator import Translator


async def i18n_exception_handler(
        r: Request, e: RequestValidationError | ValidationError) -> JSONResponse:
    errors = Helper.make_errors(e, r.state.locale, r.state.locale_path)
    return JSONResponse(
        {'errors': errors},
        status_code=422,
    )


class Helper:

    @staticmethod
    def make_errors(e: RequestValidationError | ValidationError, locale: str,
                    locale_path: str) -> List[Dict[str, Any]]:
        t = Translator(locale, locale_path=locale_path)
        res = []
        msg_keys = list(Helper.flatten_errors(e.raw_errors))
        for e_idx, error in enumerate(e.errors()):
            ctx = error.get('ctx')
            try:
                if ctx:
                    msg = t.t(f'message.{msg_keys[e_idx]}', **ctx)
                else:
                    msg = t.t(f'message.{msg_keys[e_idx]}')
            except:  # noqa
                msg = error['msg']
            res.append({**error, 'msg': msg})
        return res

    @staticmethod
    def flatten_errors(errors: Sequence[Any]) -> Generator[str, None, None]:
        for error in errors:
            if isinstance(error, ErrorWrapper):
                if isinstance(error.exc, ValidationError):
                    yield from Helper.flatten_errors(error.exc.raw_errors)
                else:
                    yield getattr(error.exc, 'msg_template', error.exc.__str__())
            elif isinstance(error, list):
                yield from Helper.flatten_errors(error)
            else:
                raise RuntimeError(f'Unknown error object: {error}')
