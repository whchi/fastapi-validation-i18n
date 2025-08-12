from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from .handler import i18n_exception_handler
from .middleware import I18nMiddleware


def setup(app: FastAPI,
          locale_list: tuple[str, ...] = (
              'zh-TW',
              'en-US',
              'ja-JP',
          ),
          locale_path: str = 'locales',
          bind_to_lifespan: bool = False) -> None:
    app.add_middleware(
        I18nMiddleware,
        locale_list=locale_list,
        locale_path=locale_path,
        bind_to_lifespan=bind_to_lifespan,
    )
    app.add_exception_handler(
        RequestValidationError,
        i18n_exception_handler,  # type: ignore[arg-type]
    )
    app.add_exception_handler(ValidationError, i18n_exception_handler)  # type: ignore[arg-type]
