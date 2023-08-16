from typing import Annotated, List, Literal, Union

from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from pydantic.fields import Field
from pydantic.networks import AnyHttpUrl
import pytest

from fastapi_validation_i18n.handler import Helper


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


def test_success():
    data = {
        'string': 'string',
        'integer': 1,
        'nested': {
            'body': 'st',
            'inner': {
                'inner_body': [{
                    'deep_body': 'stringstringstringst',
                    'url': 'https://example.com/'
                }],
                'cat': {
                    'pet_type': 'cat',
                    'color': 'black',
                    'black_name': 'string'
                }
            }
        }
    }
    assert Example(**data).dict() == data


def test_i18n_validation():
    data = {
        "string": "ajsdksaldjlskajdlkasjdljaskldjsakldjjslalksajdsak",
        "integer": 1,
        "nested": {
            "body": "asdklsadasd",
            "inner": {
                "inner_body": [{
                    "deep_body": "t",
                    "url": "https:example.com/"
                }, {
                    "deep_body": "t",
                    "url": "https:example.com/"
                }, {
                    "deep_body": "t",
                    "url": "https:example.com/"
                }],
                "cat": {
                    "pet_type": "cat",
                    "color": "ccc",
                    "black_name": "aaaaaaaaasdasdasdasdasdasda"
                }
            }
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        Example(**data)
        assert Helper.make_errors(exc_info.value, 'zh-TW', 'locale') == [{
            "loc": ["body", "string"],
            "msg": "確保此值最多有 10 個字符",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 10
            }
        }, {
            "loc": ["body", "nested", "body"],
            "msg": "確保此值最多有 2 個字符",
            "type": "value_error.any_str.max_length",
            "ctx": {
                "limit_value": 2
            }
        }, {
            "loc": ["body", "nested", "inner", "inner_body"],
            "msg": "確保此值最多包含 2 個項目",
            "type": "value_error.list.max_items",
            "ctx": {
                "limit_value": 2
            }
        }, {
            "loc": ["body", "nested", "inner", "cat"],
            "msg": "鑑別器 'color' 和值 'ccc' 不匹配（允許的值: 'black', 'white'）",
            "type": "value_error.discriminated_union.invalid_discriminator",
            "ctx": {
                "discriminator_key": "color",
                "discriminator_value": "ccc",
                "allowed_values": "'black', 'white'"
            }
        }]
