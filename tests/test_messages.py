from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Annotated, List, Literal, Union

import pytest
from pydantic import BaseModel, field_validator
from pydantic.fields import Field
from pydantic.networks import AnyHttpUrl
from pydantic_core import ValidationError

from fastapi_validation_i18n._helpers import translate_errors
from fastapi_validation_i18n.translator import Translator

translator = Translator('zh-TW', locale_path=str(Path.cwd()) + '/tests/locale')


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

    @field_validator('ipt_enum')
    @classmethod
    def validate_ipt_enum(cls, v: MyEnum):
        return v.value


def test_success():
    data = {
        "string": "string",
        "integer": 1,
        "nested": {
            "body": "st",
            "inner": {
                "inner_body": [{
                    "deep_body": "stringstringstringst",
                    "url": "https://example.com/",
                    "ipv4": "198.51.100.42"
                }],
                "cat": {
                    "pet_type": "cat",
                    "color": "black",
                    "black_name": "string"
                },
                "ipv6": "2001:db8:5b96::426f:8e17:642a"
            },
            "custom_input": "strin"
        },
        "ipt_enum": "option"
    }
    assert Example(**data).model_dump() == data  # type: ignore


def test_i18n_validation():
    data = {
        "string": "string",
        "integer": 1,
        "nested": {
            "body": "st",
            "inner": {
                "inner_body": [{
                    "deep_body": "stringstringstringst",
                    "url": "https://example.com/",
                    "ipv4": "198.51.100.42"
                }],
                "cat": {
                    "pet_type": "dog",
                    "color": "black",
                    "black_name": "string"
                },
                "ipv6": "2001:0db8:5b96:0000:0000:426f:8e17:642a"
            },
            "custom_input": "dddddddd"
        },
        "ipt_enum": "option"
    }
    with pytest.raises(ValidationError) as exc_info:
        Example(**data)

    assert translate_errors(translator, exc_info.value.errors()) == [
        {  # type: ignore
            "type": "literal_error",
            "loc": ("nested", "inner", "cat", "black", "pet_type"),
            "msg": "輸入應為 'cat'",
            "input": "dog",
            "ctx": {
                "expected": "'cat'"
            },
            "url": "https://errors.pydantic.dev/2.5/v/literal_error"
        },
        {
            "type": "too_long",
            "loc": ("nested", "custom_input"),
            "msg": "Value 在驗證後最多應有 5 個項目,而不是 8",
            "input": "dddddddd",
            "ctx": {
                "field_type": "Value",
                "max_length": 5,
                "actual_length": 8
            },
            "url": "https://errors.pydantic.dev/2.5/v/too_long"
        }
    ]
