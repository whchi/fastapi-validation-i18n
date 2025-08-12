![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-validation-i18n)

error message with i18n support in FastAPI

## response example
```json
{
  "errors": [
    {
      "loc": [
        "body",
        "string"
      ],
      "msg": "確保此值最多有 10 個字符",
      "type": "value_error.any_str.max_length",
      "ctx": {
        "limit_value": 10
      }
    },
    {
      "loc": [
        "body",
        "nested",
        "body"
      ],
      "msg": "確保此值最多有 2 個字符",
      "type": "value_error.any_str.max_length",
      "ctx": {
        "limit_value": 2
      }
    },
    {
      "loc": [
        "body",
        "nested",
        "inner",
        "inner_body"
      ],
      "msg": "確保此值最多包含 2 個項目",
      "type": "value_error.list.max_items",
      "ctx": {
        "limit_value": 2
      }
    },
    {
      "loc": [
        "body",
        "nested",
        "inner",
        "cat"
      ],
      "msg": "鑑別器 'color' 和值 'ccc' 不匹配（允許的值: 'black', 'white'）",
      "type": "value_error.discriminated_union.invalid_discriminator",
      "ctx": {
        "discriminator_key": "color",
        "discriminator_value": "ccc",
        "allowed_values": "'black', 'white'"
      }
    }
  ]
}
```
## parameters
all parameters are optional

| param             | description                                                                      | default                     |
|-------------------|----------------------------------------------------------------------------------|-----------------------------|
| locale_path       | the path of your locale files                                                    | locales                     |
| locale_list       | support locales in your app in tuple                                             | ('zh-TW', 'ja-JP', 'en-US') |
| bind_to_life_span | set to `True` if you want the translator instance be created when on app startup | False                       |

## Attention
- For FastAPI >=0.100.0 and pydantic v2, please use **^0.4.0**
- For FastAPI < 0.100.0 nad pydantic v1, please use **^0.3.0**
- built-in locales are **zh-TW, en-US, ja-JP**, you can change the locales by yourself

## How to run
- use `setup`
```py
from fastapi_validation_i18n import setup
from fastapi import FastAPI
app = FastAPI()
setup(app, locale_path=..., locale_list=...)

```
- use middleware and exception handler
```py
from fastapi import FastAPI
from fastapi_validation_i18n import I18nMiddleware, i18n_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.add_middleware(I18nMiddleware, locale_path='your-publish-path')

app.add_exception_handler(
    RequestValidationError,
    i18n_exception_handler
)
```
## Other
- publish locales to your app path
```bash
# default to "locale" in your project path
uv run publish-locale <your-path> [--locale]
```

- how to set locale

there are 3 ways to set locale
1. set `accept-language` header to your request
2. set an API with `locale` in path
3. set `locale` query parameter to your request

you can see the [example](https://github.com/whchi/fastapi-validation-i18n/tree/main/example) for more detail
