import json
import os
from typing import Any, Dict

from ._helpers import get_package_root


class Translator:
    _instances: Dict[str, 'Translator'] = {}

    def __new__(cls, locale: str, **args: Any) -> 'Translator':
        if locale not in cls._instances:
            cls._instances[locale] = super().__new__(cls)
        return cls._instances[locale]

    def __init__(self, locale: str, locale_path: str):
        self.locale = locale
        self.locale_path = locale_path.rstrip('/')
        self.translations: Dict[str, Any] = {}

    def load_translation(self, file_key: str) -> Any | Dict[str, Any] | None:
        if file_key in self.translations:
            return self.translations[file_key]
        file_path = f'{self.locale_path}/{self.locale}/{file_key}.json'
        if not os.path.isfile(file_path):
            file_path = str(
                get_package_root().joinpath(f'locales/{self.locale}/{file_key}.json'))
        try:
            with open(file_path, encoding='utf-8') as file:
                translation = json.load(file)
            self.translations[file_key] = translation
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
            translation = str(translation).format(**kwargs)

        return str(translation)


__all__ = ['Translator']
