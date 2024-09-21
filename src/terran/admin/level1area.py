from ._filter import CountryFilter
from ._format import create_dict_formatted
from ._format import create_name_formatted
from ..models import Level1Area
from ..models import Level2Area
from django.contrib import admin
from django.utils.safestring import mark_safe


class Level2AreaInline(admin.TabularInline):
    model = Level2Area
    fields = ("id", "iso_3166_a2", "name")
    ordering = ("iso_3166_a2",)
    readonly_fields = ("id", "iso_3166_a2", "name")
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Level1Area)
class Level1AreaAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    ("country",),
                    ("iso_3166_a2",),
                    ("name",),
                    ("online_map_formatted",),
                    ("expando_formatted",),
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
    inlines = (Level2AreaInline,)
    list_display = (
        "iso_3166_a2",
        "name",
        "country",
    )
    list_display_links = (
        "iso_3166_a2",
        "name",
    )
    list_filter = (CountryFilter,)
    ordering = ("iso_3166_a2",)
    readonly_fields = (
        "country",
        "expando_formatted",
        "iso_3166_a2",
        "name",
        "names_formatted",
        "online_map_formatted",
    )
    search_fields = (
        "iso_3166_a2",
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

    expando_formatted = create_dict_formatted("expando", description="Expando")
    names_formatted = create_name_formatted("names", description="Names")

    @admin.display(description="View Online")
    def online_map_formatted(self, obj):
        if not obj:
            return ""

        result = ""

        expando = obj.expando or {}
        open_street_map_type = expando.get("open_street_map_type")
        open_street_map_id = expando.get("open_street_map_id")

        if open_street_map_type and open_street_map_id:
            result += f'<a target="_blank" href="https://www.openstreetmap.org/{open_street_map_type}/{open_street_map_id}">Open Street Maps</a>'

        return mark_safe(result)
