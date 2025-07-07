from .handler import i18n_exception_handler
from .middleware import I18nMiddleware
from .translator import Translator
from .base import setup
from .compat import is_pydantic_v2, get_pydantic_version

__version__ = '0.4.2'
__all__ = ['Translator', 'i18n_exception_handler', 'I18nMiddleware', 'setup', 'is_pydantic_v2', 'get_pydantic_version']
__name__ = 'fastapi_validation_i18n'
