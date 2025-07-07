from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from typing import Union

from ._helpers import translate_errors
from .translator import Translator
from .compat import get_all_validation_error_classes


async def i18n_exception_handler(
        r: Request, e: Union[RequestValidationError, Exception]) -> JSONResponse:
    if r.state.fvi_translators and r.state.fvi_translators[r.state.locale]:
        t = r.state.fvi_translators[r.state.locale]
    else:
        t = Translator(r.state.locale, locale_path=r.state.locale_path)
    errors = list(translate_errors(t, e.errors()))
    return JSONResponse(
        {'errors': errors},
        status_code=422,
    )


__all__ = ['i18n_exception_handler']
