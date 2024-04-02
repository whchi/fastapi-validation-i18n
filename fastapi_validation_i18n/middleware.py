from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class I18nMiddleware(BaseHTTPMiddleware):

    def __init__(self,
                 app: ASGIApp,
                 locale_path: str = 'locales',
                 locale_list: tuple[str, ...] = (
                     'zh-TW',
                     'en-US',
                     'ja-JP',
                 ),
                 fallback_locale: str = 'zh-TW',
                 bind_to_lifespan: bool = False):
        super().__init__(app)
        self.locale_path = locale_path
        self.locale_list = locale_list
        self.fallback_locale = fallback_locale
        self.bind_to_lifespan = bind_to_lifespan

    async def dispatch(self, request: Request,
                       call_next: RequestResponseEndpoint) -> Response:
        locale = request.headers.get('accept-language', None) or \
                 request.path_params.get('locale', None) or \
                 request.query_params.get('locale', None) or \
                 self.fallback_locale
        if locale not in self.locale_list:
            locale = self.fallback_locale

        request.state.locale = locale
        request.state.locale_path = self.locale_path
        request.state.fvi_translators = None
        if self.bind_to_lifespan:
            from fastapi_validation_i18n import Translator
            request.state.fvi_translators = {
                locale: Translator(locale, locale_path=self.locale_path)
                for locale in self.locale_list
            }
        return await call_next(request)


__all__ = ['I18nMiddleware']
