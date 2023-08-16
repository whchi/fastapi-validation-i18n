import json
from typing import Dict


class Translator:
    _instances: Dict[str, 'Translator'] = {}

    def __init__(self, locale: str, locale_path: str = 'locale'):
        self.locale = locale
        self.locale_path = locale_path.rstrip('/')

    def load_translation(self, file_key: str):
        file_path = f'{self.locale_path}/{self.locale}/{file_key}.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                translation = json.load(file)
            return translation
        except FileNotFoundError:
            return None

    def t(self, key: str, **kwargs) -> str:
        file_key, *translation_keys = key.split('.')
        translation = self.load_translation(file_key)
        if translation is None:
            return f'Key {key} not found in {self.locale} locale'

        for translation_key in translation_keys:
            translation = translation.get(translation_key, None)
            if translation is None:
                return f'Key {key} not found in {self.locale} locale'

        if kwargs:
            translation = translation.format(**kwargs)

        return translation  # type: ignore
