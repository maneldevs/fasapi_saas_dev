class Translator:
    def __init__(self, source: dict[str, dict[str, str]], default_locale: str = "es_ES") -> None:
        self.source = source
        self.default_locale = default_locale

    def get_allowed_locales(self) -> list[str]:
        return self.source.keys()

    def get_dictionary(self, locale: str):
        return self.source[locale]

    def get_translation(self, key: str, locale: str):
        if locale not in self.get_allowed_locales():
            locale = self.default_locale
        dictionary = self.get_dictionary(locale)
        return dictionary.get(key, key)

    def t(self, key: str, locale: str, **kwargs: dict[str, str]):
        translation = self.get_translation(key, locale)
        return translation.format(**kwargs)
