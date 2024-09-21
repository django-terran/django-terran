from django.conf.global_settings import LANGUAGES
from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe
from json import dumps

LANGUAGE_MAP = dict(LANGUAGES)


def create_dict_formatted(attribute_name, /, **kwargs):
    @admin.display(**kwargs)
    def func(self, obj):
        value = getattr(obj, attribute_name)

        if not value:
            return ""

        result = f'<pre class="literal-block">{dumps(value, ensure_ascii=False, sort_keys=False, indent=4)}</pre>'

        return mark_safe(result)

    return func


def create_list_formatted(attribute_name, /, convert=None, **kwargs):
    @admin.display(**kwargs)
    def func(self, obj):
        value = getattr(obj, attribute_name)

        if not value:
            return ""

        result = '<ol type="i">'

        for item in value:
            if callable(convert):
                item = convert(item)

            result += f"<li>{escape(item)}</li>"

        result += "</ol>"

        return mark_safe(result)

    return func


def create_name_formatted(attribute_name, /, **kwargs):
    @admin.display(**kwargs)
    def func(self, obj):
        value = getattr(obj, attribute_name)

        if not value:
            return ""

        value = sorted(
            [
                (LANGUAGE_MAP.get(language, language), name)
                for language, name in value.items()
            ]
        )

        column_number = min(5, max(1, (len(value) + 9) // 10))
        row_number = (len(value) + column_number - 1) // column_number
        result = "<table>"
        result += "<thead><tr>"

        for _ in range(column_number):
            result += "<th>Locale</th><th>Text</th>"

        result += "</tr></thead>"
        result += "<tbody><tr>"

        for row_index in range(row_number):
            for column_index in range(column_number):
                cell_index = column_index * row_number + row_index

                if cell_index < len(value):
                    locale, name = value[cell_index]
                    result += f"<th>{escape(locale)}</th><td>{escape(name)}</td>"
                else:
                    result += f"<th></th><td></td>"

            result += "</tr><tr>"

        result += "</tr></tbody></table>"

        return mark_safe(result)

    return func
