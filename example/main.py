from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, List, Literal, Union

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, ValidationError
from pydantic.networks import AnyHttpUrl
from starlette.requests import Request

from fastapi_validation_i18n import i18n_exception_handler, I18nMiddleware, Translator

app = FastAPI(debug=True)

app.add_middleware(I18nMiddleware, locale_path='example/locale')

# for request validation error
app.add_exception_handler(RequestValidationError, i18n_exception_handler)

# for pydantic validation error
app.add_exception_handler(ValidationError, i18n_exception_handler)


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
    ipv4: IPv4Address

    @field_validator('url')
    @classmethod
    def validate_url(cls, v: AnyHttpUrl):
        return v.__str__()

    @field_validator('ipv4')
    @classmethod
    def validate_ipv4(cls, v: IPv4Address):
        return v.__str__()


class InnerNestedExample(BaseModel):
    inner_body: List[DeepBody] = Field(..., max_length=2)
    cat: Cat
    ipv6: IPv6Address

    @field_validator('ipv6')
    @classmethod
    def validate_ipv6(cls, v: IPv6Address):
        return v.__str__()


CustomType = Annotated[str | int, Field(..., min_length=2, max_length=5)]


class NestedExample(BaseModel):
    body: str = Field(..., max_length=2)
    inner: InnerNestedExample
    custom_input: CustomType


class MyEnum(str, Enum):
    option = 'option'
    choice = 'choice'


class Example(BaseModel):
    string: str = Field(max_length=10)
    integer: int = Field(default=1)
    nested: NestedExample
    ipt_enum: MyEnum


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
    return JSONResponse(content=payload.model_dump())


@app.get('/examples')
async def get_examples() -> Example:
    return Example(**{'message': 'this will not show up'})
