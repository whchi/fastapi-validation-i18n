from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, List, Literal, Union

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from pydantic.functional_validators import field_validator
from pydantic.networks import AnyHttpUrl
from starlette.requests import Request

from fastapi_validation_i18n import i18n_exception_handler, I18nMiddleware, Translator
from fastapi_validation_i18n.base import setup

# NEW: Auto-detection for Pydantic v2
# The library now automatically detects whether you're using Pydantic v1 or v2
# and adapts its behavior accordingly. You can check the version like this:
from fastapi_validation_i18n import is_pydantic_v2, get_pydantic_version
print(f"Auto-detected Pydantic version: {get_pydantic_version()} (v2: {is_pydantic_v2()})")

# use this separately
app = FastAPI(debug=True)


def setup_separately(app: FastAPI) -> None:
    app.add_middleware(I18nMiddleware, locale_path='example/locale')

    # for request validation error
    app.add_exception_handler(RequestValidationError, i18n_exception_handler)

    # for pydantic validation error
    # NOTE: With auto-detection, the library automatically registers handlers
    # for all appropriate ValidationError classes based on your Pydantic version
    app.add_exception_handler(ValidationError, i18n_exception_handler)


def setup_with_single_function(app: FastAPI) -> None:
    # NEW: The setup function now automatically detects your Pydantic version
    # and registers the appropriate ValidationError handlers for both v1 and v2
    setup(app)


# setup_separately(app)
setup_with_single_function(app)


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
    def validate_url(cls, v: AnyHttpUrl) -> str:
        return v.__str__()

    @field_validator('ipv4')
    @classmethod
    def validate_ipv4(cls, v: IPv4Address) -> str:
        return v.__str__()


class InnerNestedExample(BaseModel):
    inner_body: List[DeepBody] = Field(..., max_length=2)
    cat: Cat
    ipv6: IPv6Address

    @field_validator('ipv6')
    @classmethod
    def validate_ipv6(cls, v: IPv6Address) -> str:
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
async def root(r: Request) -> dict[str, str]:
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
    return Example(**{'message': 'this will not show up'})  # type: ignore
