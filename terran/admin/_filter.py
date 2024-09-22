from ..models import Country
from ..models import Level1Area
from ..models import Level2Area

from django.contrib import admin


class CountryFilter(admin.SimpleListFilter):
    title = "Country"
    parameter_name = "country"

    def expected_parameters(self):
        return [self.parameter_name, "level1area"]

    def lookups(self, request, model_admin):
        return sorted(
            [(country.iso_3166_a2, country.name) for country in Country.objects.all()],
            key=lambda l: l[1],
        )

    def queryset(self, request, queryset):
        country_iso_3166_a2 = self.used_parameters.get("country")

        if country_iso_3166_a2:
            queryset = queryset.filter(country__iso_3166_a2=country_iso_3166_a2)

        return queryset


class Level1AreaFilter(admin.SimpleListFilter):
    title = "Level 1 Area"
    parameter_name = "level1area"

    def expected_parameters(self):
        return [self.parameter_name, "country"]

    def lookups(self, request, model_admin):
        country_iso_3166_a2 = request.GET.get("country")

        if country_iso_3166_a2:
            return sorted(
                [
                    (level1area.iso_3166_a2, level1area.name)
                    for level1area in Level1Area.objects.filter(
                        country__iso_3166_a2=country_iso_3166_a2
                    )
                ],
                key=lambda l: l[1],
            )

        return []

    def queryset(self, request, queryset):
        country_iso_3166_a2 = request.GET.get("country")
        level1area_iso_3166_a2 = self.used_parameters.get("level1area")

        if level1area_iso_3166_a2 and level1area_iso_3166_a2.lower().startswith(
            country_iso_3166_a2.lower()
        ):
            queryset = queryset.filter(level1area__iso_3166_a2=level1area_iso_3166_a2)

        return queryset


class Level2AreaFilter(admin.SimpleListFilter):
    title = "Level 2 Area"
    parameter_name = "level2area"

    def expected_parameters(self):
        return [self.parameter_name, "level1area", "country"]

    def lookups(self, request, model_admin):
        country_iso_3166_a2 = request.GET.get("country")
        level1area_iso_3166_a2 = request.GET.get("level1area")

        if country_iso_3166_a2 and level1area_iso_3166_a2:
            return sorted(
                [
                    (level1area.iso_3166_a2, level1area.name)
                    for level1area in Level2Area.objects.filter(
                        country__iso_3166_a2=country_iso_3166_a2,
                        level1area__iso_3166_a2=level1area_iso_3166_a2,
                    )
                ],
                key=lambda l: l[1],
            )

        return []

    def queryset(self, request, queryset):
        country_iso_3166_a2 = request.GET.get("country")
        level1area_iso_3166_a2 = self.used_parameters.get("level1area")
        level2area_iso_3166_a2 = self.used_parameters.get("level1area")

        if (
            level1area_iso_3166_a2
            and level1area_iso_3166_a2.lower().startswith(country_iso_3166_a2.lower())
        ) and (
            level2area_iso_3166_a2
            and level2area_iso_3166_a2.lower().startswith(
                level1area_iso_3166_a2.lower()
            )
        ):
            queryset = queryset.filter(level2area__iso_3166_a2=level2area_iso_3166_a2)

        return queryset
