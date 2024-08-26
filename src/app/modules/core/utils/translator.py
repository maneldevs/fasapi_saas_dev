class Translator:
    def __init__(self, source: dict[str, dict[str, str]], default_locale: str = "en_US") -> None:
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

    def t(self, key: str, locale: str, **kwargs: dict[str, any]):
        translation = self.get_translation(key, locale)
        return translation.format(**kwargs)

    def t_errors(self, errors: list[dict], locale: str):
        result = []
        for error in errors:
            print(type(error))
            message = error["msg"]
            context = error.get("ctx", {})
            message = self.__get_original_error_message(message, context)
            translated_message = self.t(message, locale, **context)
            error["msg"] = translated_message
            result.append(error)
        return result

    def __get_original_error_message(self, message: str, context: dict[str, any]):
        for k in context.keys():
            placeholder = "{" + k + "}"
            message = message.replace(str(context[k]), placeholder)
        return message
