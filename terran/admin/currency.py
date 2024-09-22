from ._format import create_name_formatted
from ..models import Country
from ..models import Currency
from django.contrib import admin


class CountryInline(admin.TabularInline):
    model = Country
    fields = ("iso_3166_n3", "iso_3166_a2", "iso_3166_a3", "is_enabled", "name")
    ordering = ("iso_3166_a3",)
    readonly_fields = (
        "iso_3166_n3",
        "iso_3166_a2",
        "iso_3166_a3",
        "is_enabled",
        "name",
    )
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    ("iso_4217_n3",),
                    ("iso_4217_a3",),
                    ("is_enabled",),
                    ("name",),
                    ("decimal_digits",),
                ),
            },
        ),
        (
            "Localization",
            {
                "classes": ("collapse",),
                "fields": (("names_formatted",),),
            },
        ),
    )
    inlines = (CountryInline,)
    list_display = (
        "iso_4217_n3",
        "iso_4217_a3",
        "is_enabled",
        "decimal_digits",
    )
    list_display_links = (
        "iso_4217_n3",
        "iso_4217_a3",
    )
    ordering = ("iso_4217_a3",)
    readonly_fields = (
        "iso_4217_n3",
        "iso_4217_a3",
        "decimal_digits",
        "name",
        "names_formatted",
    )
    search_fields = (
        "iso_4217_n3",
        "iso_4217_a3",
        "names__de",
        "names__en",
        "names__es",
        "names__fr",
        "names__ka",
        "names__ru",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    names_formatted = create_name_formatted("names", description="Names")
