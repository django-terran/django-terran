from django.utils.translation import get_language
from django.conf import settings


def _get_localized_name(names: dict[str, str]):
    if not names:
        return ""

    language_code = get_language()

    if language_code:
        return (
            names.get(language_code)
            or names.get(settings.LANGUAGE_CODE)
            or names.get("en")
            or list(names.values())[0]
        )

    return (
        names.get(settings.LANGUAGE_CODE) or names.get("en") or list(names.values())[0]
    )
