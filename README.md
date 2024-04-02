error message with i18n support in FastAPI

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
## Attention
- For FastAPI >=0.100.0 and pydantic v2, please use **^0.4.0**
- For FastAPI < 0.100.0 nad pydantic v1, please use **^0.3.0**
- built-in locales are **zh-TW, en-US, ja-JP**, you can change the locales by yourself

## How to run
1. publish locales to your app path
```bash
# default to "locale" in your project path
poetry run publish-locale <your-path> [--locale]
```
### Setup in FastAPI
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

there's 3 way to set locale

1. set `accept-language` header to your request
2. set an API with `locale` in path
3. set `locale` query parameter to your request

you can see the [example](https://github.com/whchi/fastapi-validation-i18n/tree/main/example) for more detail
