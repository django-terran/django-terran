from ._filter import CountryFilter
from ._filter import Level1AreaFilter
from ._filter import Level2AreaFilter
from ._format import create_dict_formatted
from ._format import create_name_formatted
from ..models import Settlement
from django.contrib import admin
from django.utils.safestring import mark_safe


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    (
                        "country",
                        "level1area",
                        "level2area",
                    ),
                    (
                        "name",
                        "place_type",
                        "population",
                    ),
                    (
                        "latitude",
                        "longitude",
                        "geocell",
                    ),
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
    list_display = (
        "id",
        "name",
        "place_type",
        "population",
        "country",
        "level1area",
        "level2area",
    )
    list_display_links = (
        "id",
        "name",
    )
    list_filter = ("place_type", Level2AreaFilter, Level1AreaFilter, CountryFilter)
    ordering = (
        "country__iso_3166_a2",
        "level1area__iso_3166_a2",
        "level2area__iso_3166_a2",
        "population",
    )
    readonly_fields = (
        "country",
        "expando_formatted",
        "geocell",
        "latitude",
        "level1area",
        "level2area",
        "longitude",
        "online_map_formatted",
        "name",
        "names_formatted",
        "place_type",
        "population",
    )
    search_fields = (
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
        else:
            result += f'<a target="_blank" href="https://www.openstreetmap.org/?mlat={obj.lat}&mlon={obj.lon}">Open Street Maps</a>'

        result += f' | <a target="_blank" href="https://www.google.com/maps/search/?api=1&query={obj.lat},{obj.lon}">Google Maps</a>'
        result += f' | <a target="_blank" href="https://bing.com/maps/default.aspx?cp={obj.lat}~{obj.lon}">Bing Maps</a>'

        return mark_safe(result)
