from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.requests import Request

from ._helpers import translate_errors
from .translator import Translator


async def i18n_exception_handler(
        r: Request, e: RequestValidationError | ValidationError) -> JSONResponse:
    t = Translator(r.state.locale, locale_path=r.state.locale_path)
    errors = translate_errors(t, e.errors())
    return JSONResponse(
        {'errors': errors},
        status_code=422,
    )
