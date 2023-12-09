import json
from typing import Any, Dict


class Translator:
    _instances: Dict[str, 'Translator'] = {}

    def __new__(cls, locale: str, **args: Any) -> 'Translator':
        if locale not in cls._instances:
            cls._instances[locale] = super().__new__(cls)
        return cls._instances[locale]

    def __init__(self, locale: str, locale_path: str = 'locale'):
        self.locale = locale
        self.locale_path = locale_path.rstrip('/')

    def load_translation(self, file_key: str) -> Any | Dict[str, Any] | None:
        file_path = f'{self.locale_path}/{self.locale}/{file_key}.json'
        try:
            with open(file_path, encoding='utf-8') as file:
                translation = json.load(file)
            return translation
        except FileNotFoundError:
            return None

    def t(self, key: str, **kwargs: Any) -> str:
        file_key, *translation_keys = key.split('.')
        translation = self.load_translation(file_key)
        if translation is None:
            return f'Key {key} not found in {self.locale} locale'

        for translation_key in translation_keys:
            translation = translation.get(translation_key, None)
            if translation is None:
                return f'Key {key} not found in {self.locale} locale'

        if kwargs:
            translation = translation.format(**kwargs)  # type: ignore

        return translation
