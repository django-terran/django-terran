from ._format import create_dict_formatted
from ._format import create_list_formatted
from ._format import create_name_formatted
from ..models import Country
from ..models import CountryCurrency
from ..models import Level1Area
from django.contrib import admin


class Level1AreaInline(admin.TabularInline):
    model = Level1Area
    fields = ("id", "iso_3166_a2", "name")
    ordering = ("iso_3166_a2",)
    readonly_fields = ("id", "iso_3166_a2", "name")
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CountryCurrencyInline(admin.TabularInline):
    model = CountryCurrency
    fields = ("id", "currency", "since", "until")
    ordering = ("-since",)
    readonly_fields = ("id", "currency", "since", "until")
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    (
                        "iso_3166_n3",
                        "iso_3166_a2",
                        "iso_3166_a3",
                    ),
                    ("is_enabled",),
                    ("name",),
                    ("currency",),
                    ("languages_formatted",),
                ),
            },
        ),
        (
            "Localization",
            {
                "classes": ("collapse",),
                "fields": (
                    ("names_formatted",),
                    ("address_level1area_names_formatted",),
                    ("address_level2area_names_formatted",),
                    ("address_settlement_names_formatted",),
                    ("address_postcode_names_formatted",),
                    ("address_street_names_formatted",),
                    ("organization_id_names_formatted",),
                    ("organization_id_abbreviations_formatted",),
                    ("person_id_names_formatted",),
                    ("person_id_abbreviations_formatted",),
                    ("iban_names_formatted",),
                ),
            },
        ),
        (
            "Address",
            {
                "fields": (
                    ("address_input_layout_formatted",),
                    ("address_output_format",),
                    ("address_postcode_input_pattern",),
                    ("address_postcode_input_example",),
                ),
            },
        ),
        (
            "Phone",
            {
                "fields": (
                    ("phone_prefixes_formatted",),
                    ("phone_input_pattern",),
                    ("phone_input_example",),
                    ("phone_output_format_formatted",),
                ),
            },
        ),
        (
            "Organization ID",
            {
                "fields": (
                    ("organization_id_input_pattern",),
                    ("organization_id_input_example",),
                    ("organization_id_output_format_formatted",),
                ),
            },
        ),
        (
            "Person ID",
            {
                "fields": (
                    ("person_id_input_pattern",),
                    ("person_id_input_example",),
                    ("person_id_output_format_formatted",),
                ),
            },
        ),
        (
            "IBAN",
            {
                "fields": (
                    ("iban_input_pattern",),
                    ("iban_input_example",),
                    ("iban_output_format_formatted",),
                ),
            },
        ),
    )
    inlines = (
        Level1AreaInline,
        CountryCurrencyInline,
    )
    list_display = (
        "iso_3166_n3",
        "iso_3166_a2",
        "iso_3166_a3",
        "name",
    )
    list_display_links = (
        "iso_3166_n3",
        "iso_3166_a2",
        "iso_3166_a3",
        "name",
    )
    ordering = ("iso_3166_a3",)
    readonly_fields = (
        "address_input_layout_formatted",
        "address_level1area_names_formatted",
        "address_level2area_names_formatted",
        "address_output_format",
        "address_postcode_input_example",
        "address_postcode_input_pattern",
        "address_postcode_names_formatted",
        "address_settlement_names_formatted",
        "address_street_names_formatted",
        "currency",
        "iban_input_example",
        "iban_input_pattern",
        "iban_names_formatted",
        "iban_output_format_formatted",
        "iso_3166_a2",
        "iso_3166_a3",
        "iso_3166_n3",
        "languages_formatted",
        "name",
        "names_formatted",
        "organization_id_abbreviations_formatted",
        "organization_id_input_example",
        "organization_id_input_pattern",
        "organization_id_names_formatted",
        "organization_id_output_format_formatted",
        "person_id_abbreviations_formatted",
        "person_id_input_example",
        "person_id_input_pattern",
        "person_id_names_formatted",
        "person_id_output_format_formatted",
        "phone_input_example",
        "phone_input_pattern",
        "phone_output_format_formatted",
        "phone_prefixes_formatted",
    )
    search_fields = (
        "iso_3166_a2",
        "iso_3166_a3",
        "iso_3166_n3",
        "names__de",
        "names__en",
        "names__es",
        "names__fr",
        "names__ka",
        "names__ru",
        "languages",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    address_input_layout_formatted = create_list_formatted(
        "address_input_layout", description="Address input layout"
    )
    address_level1area_names_formatted = create_name_formatted(
        "address_level1area_names", description="Address level 1 area"
    )
    address_level2area_names_formatted = create_name_formatted(
        "address_level2area_names", description="Address level 2 area"
    )
    address_postcode_names_formatted = create_name_formatted(
        "address_postcode_names", description="Address post code names"
    )
    address_settlement_names_formatted = create_name_formatted(
        "address_settlement_names", description="Address settlement names"
    )
    address_street_names_formatted = create_name_formatted(
        "address_street_names", description="Address street names"
    )
    iban_names_formatted = create_name_formatted("iban_names", description="IBAN names")
    iban_output_format_formatted = create_dict_formatted(
        "iban_output_format", description="IBAN output format"
    )
    languages_formatted = create_list_formatted("languages", description="Languages")
    names_formatted = create_name_formatted("names", description="Names")
    organization_id_abbreviations_formatted = create_name_formatted(
        "organization_id_abbreviations", description="Organization ID abbreviations"
    )
    organization_id_names_formatted = create_name_formatted(
        "organization_id_names", description="Organization ID names"
    )
    organization_id_output_format_formatted = create_dict_formatted(
        "organization_id_output_format", description="Organization ID output format"
    )
    person_id_abbreviations_formatted = create_name_formatted(
        "person_id_abbreviations", description="Person ID abbreviations"
    )
    person_id_names_formatted = create_name_formatted(
        "person_id_names", description="Person ID names"
    )
    person_id_output_format_formatted = create_dict_formatted(
        "person_id_output_format", description="Person ID output format"
    )
    phone_output_format_formatted = create_dict_formatted(
        "phone_output_format", description="Phone output format"
    )
    phone_prefixes_formatted = create_list_formatted(
        "phone_prefixes", description="Phone prefixes"
    )
