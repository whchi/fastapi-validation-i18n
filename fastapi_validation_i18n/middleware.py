from typing import Sequence

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp


class I18nMiddleware(BaseHTTPMiddleware):

    def __init__(self,
                 app: ASGIApp,
                 locale_path: str = 'locale',
                 locale_list: Sequence[str] = ('zh-TW'),
                 fallback_locale: str = 'zh-TW'):
        super().__init__(app)
        self.locale_path = locale_path
        self.locale_list = locale_list
        self.fallback_locale = fallback_locale

    async def dispatch(  # type: ignore
            self, request: Request, call_next: RequestResponseEndpoint):
        locale = request.headers.get('accept-language', None) or \
                 request.path_params.get('locale', None) or \
                 request.query_params.get('locale', None) or \
                 self.fallback_locale
        if locale not in self.locale_list:
            locale = self.fallback_locale

        request.state.locale = locale
        request.state.locale_path = self.locale_path

        return await call_next(request)
