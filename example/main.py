from typing import Annotated, List, Literal, Union

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic.networks import AnyHttpUrl
from starlette.requests import Request

from fastapi_validation_i18n import i18n_exception_handler, I18nMiddleware, Translator

app = FastAPI()

app.add_middleware(I18nMiddleware, locale_path='example/locale')
app.add_exception_handler(RequestValidationError, i18n_exception_handler)


class BlackCat(BaseModel):
    pet_type: Literal['cat']
    color: Literal['black']
    black_name: str


class WhiteCat(BaseModel):
    pet_type: Literal['cat']
    color: Literal['white']
    white_name: str


Cat = Annotated[Union[BlackCat, WhiteCat], Field(discriminator='color')]


class DeepBody(BaseModel):
    deep_body: str = Field(..., min_length=20)
    url: AnyHttpUrl


class InnerNestedExample(BaseModel):
    inner_body: List[DeepBody] = Field(..., max_items=2)
    cat: Cat


class NestedExample(BaseModel):
    body: str = Field(..., max_length=2)
    inner: InnerNestedExample


class Example(BaseModel):
    string: str = Field(max_length=10)
    integer: int = Field(default=1, min=10)
    nested: NestedExample


@app.get('/')
async def root(r: Request):
    return {
        'message':
            Translator('ja-JP',
                       locale_path='example/locale').t('message.field required'),
        'request_locale_message':
            Translator(r.state.locale,
                       locale_path='example/locale').t('message.field required'),
    }


@app.post('/')
async def post_root(payload: Example) -> JSONResponse:
    return JSONResponse(content=payload.dict())
