from django.http import JsonResponse
from django.shortcuts import render
from django.template import Context
from django.template import Template
from django.views import View
from math import cos

from terran.models import Country
from terran.models import Level1Area
from terran.models import Level2Area
from terran.models import Settlement


def get_context_from_request(form_data: dict):
    entity = form_data.get("entity")
    address_country_iso3166_a2 = form_data.get("address_country", "")
    address_level1area_iso3166_a2 = form_data.get("address_level1area", "")
    address_level2area_iso3166_a2 = form_data.get("address_level2area", "")
    address_postcode = form_data.get("address_postcode", "")
    address_settlement = form_data.get("address_settlement", "")
    address_street = form_data.get("address_street", "")
    address_street_line0 = form_data.get("address_street_line0", "")
    address_street_line1 = form_data.get("address_street_line1", "")
    address_street_line2 = form_data.get("address_street_line2", "")
    address_street_line3 = form_data.get("address_street_line3", "")
    person_id = form_data.get("person_id", "")
    person_name = form_data.get("person_name", "")
    organization_id = form_data.get("organization_id", "")
    organization_name = form_data.get("organization_name", "")

    context = {
        "entity": entity,
        "address_country_choices": sorted(list(Country.objects.filter(is_enabled=True)), key=lambda c: c.name),
        "address_level1area_choices": [],
        "address_level2area_choices": [],
        "address_settlement_choices": [],
        "address_country": {
            "order": 0,
            "visible": True,
            "enabled": True,
            "value": None,
            "label": "Country",
        },
        "address_level1area": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
        },
        "address_level2area": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
        },
        "address_postcode": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
            "pattern": None,
            "example": None,
        },
        "address_settlement": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": address_settlement,
            "label": None,
        },
        "address_street": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": address_street,
            "label": None,
        },
        "address_street_line0": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": address_street_line0,
            "label": None,
        },
        "address_street_line1": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": address_street_line1,
            "label": None,
        },
        "address_street_line2": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": address_street_line2,
            "label": None,
        },
        "address_street_line3": {
            "order": 19,
            "visible": False,
            "enabled": False,
            "value": address_street_line3,
            "label": None,
        },
        "address_order_range": range(20),
        "organization": {"visible": False},
        "organization_id": {
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
            "pattern": None,
            "example": None,
        },
        "organization_phone": {
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
            "pattern": None,
            "example": None,
        },
        "person": {"visible": False},
        "person_id": {
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
            "pattern": None,
            "example": None,
        },
        "person_phone": {
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
            "pattern": None,
            "example": None,
        },
        "bank_iban": {
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
            "pattern": None,
            "example": None,
        },
        "bank_account": {
            "visible": False,
            "enabled": False,
            "value": None,
            "label": None,
        },
        "preview": "",
    }

    address_country = None
    address_level1area = None
    address_level2area = None
    address_level1area_choices = []
    address_level2area_choices = []
    address_settlement_choices = []

    if address_country_iso3166_a2:
        address_country = Country.objects.get(iso_3166_a2=address_country_iso3166_a2)
        context["address_country"]["value"] = address_country.iso_3166_a2

    if address_country:
        address_level1area_choices = sorted(
            list(address_country.level1areas.all()),
            key=lambda level1area: level1area.name,
        )
        context["address_level1area_choices"] = address_level1area_choices

        if address_level1area_choices:
            context["address_level1area"]["visible"] = True

    if address_country and address_level1area_iso3166_a2:
        try:
            address_level1area = address_country.level1areas.get(iso_3166_a2=address_level1area_iso3166_a2)
            context["address_level1area"]["value"] = address_level1area.iso_3166_a2
        except Level1Area.DoesNotExist:
            pass

    if address_level1area:
        address_level2area_choices = sorted(
            list(address_level1area.level2areas.all()),
            key=lambda level2area: level2area.name,
        )
        context["address_level2area_choices"] = address_level2area_choices

        if address_level2area_choices:
            context["address_level2area"]["visible"] = True

    if address_level1area and address_level2area_iso3166_a2:
        try:
            address_level2area = address_level1area.level2areas.get(iso_3166_a2=address_level2area_iso3166_a2)
            context["address_level2area"]["value"] = address_level2area.iso_3166_a2
        except Level2Area.DoesNotExist:
            pass

    is_hierarchy_complete = (address_country is not None) and (
        (len(address_level1area_choices) == 0)
        or (
            (len(address_level1area_choices) > 0)
            and (address_level1area is not None)
            and ((len(address_level2area_choices) == 0) or (address_level2area is not None))
        )
    )

    if is_hierarchy_complete:
        address_settlement_choices = []

        if address_level2area:
            address_settlement_choices += list(address_level2area.settlements.all())
        elif address_level1area:
            address_settlement_choices += list(address_level1area.settlements.filter(level2area__isnull=True))
        else:
            address_settlement_choices += list(address_country.settlements.filter(level1area__isnull=True, level2area__isnull=True))

        address_settlement_choices = sorted(address_settlement_choices, key=lambda settlement: -settlement.population)
        address_settlement_choices = address_settlement_choices[:5] + sorted(address_settlement_choices[5:], key=lambda settlement: settlement.name)
        context["address_settlement_choices"] = address_settlement_choices

        # Many capitals are settlements AND administrative divisions.
        if (
            (address_level1area is not None)
            and (not address_settlement)
            and (len(address_settlement_choices) == 1)
            and (address_settlement_choices[0].name == address_level1area.name)
        ):
            context["address_settlement"]["value"] = address_level1area.name

    if address_country:
        layout_part_order = 0
        has_level1area = False

        for field_name in address_country.address_input_layout:
            layout_part_order += 1

            match field_name:
                case "level1area":
                    if address_level1area_choices:
                        context["address_level1area"]["label"] = address_country.address_level1area_name
                        context["address_level1area"]["enabled"] = True
                        context["address_level1area"]["order"] = layout_part_order
                        has_level1area = True
                case "level2area":
                    if address_level2area_choices:
                        context["address_level2area"]["label"] = address_country.address_level2area_name
                        context["address_level2area"]["enabled"] = True
                        context["address_level2area"]["order"] = layout_part_order
                case "postcode":
                    context["address_postcode"]["label"] = address_country.address_postcode_name
                    context["address_postcode"]["enabled"] = is_hierarchy_complete or (not has_level1area)
                    context["address_postcode"]["visible"] = True
                    context["address_postcode"]["order"] = layout_part_order
                    context["address_postcode"]["pattern"] = address_country.address_postcode_input_pattern
                    context["address_postcode"]["example"] = address_country.address_postcode_input_example
                case "settlement":
                    context["address_settlement"]["label"] = address_country.address_settlement_name
                    context["address_settlement"]["enabled"] = is_hierarchy_complete
                    context["address_settlement"]["visible"] = True
                    context["address_settlement"]["order"] = layout_part_order
                case "street":
                    name = address_country.address_street_name

                    if isinstance(name, str):
                        context["address_street"]["label"] = name
                        context["address_street"]["enabled"] = is_hierarchy_complete
                        context["address_street"]["visible"] = True
                        context["address_street"]["order"] = layout_part_order
                    elif isinstance(name, list):
                        for line_index, line_name in enumerate(name):
                            context[f"address_street_line{line_index}"]["label"] = line_name
                            context[f"address_street_line{line_index}"]["enabled"] = is_hierarchy_complete
                            context[f"address_street_line{line_index}"]["visible"] = True
                            context[f"address_street_line{line_index}"]["order"] = layout_part_order
                            layout_part_order += 1

    if address_country:
        if entity == "person":
            context["person"]["visible"] = True

            if address_country.person_id_names:
                context["person_id"]["enabled"] = True
                context["person_id"]["visible"] = True
                context["person_id"]["label"] = address_country.person_id_name
                context["person_id"]["pattern"] = address_country.person_id_input_pattern
                context["person_id"]["example"] = address_country.person_id_input_example

            context["person_phone"]["enabled"] = True
            context["person_phone"]["visible"] = True
            context["person_phone"]["label"] = address_country.phone_name
            context["person_phone"]["pattern"] = address_country.phone_input_pattern
            context["person_phone"]["example"] = address_country.phone_input_example
        elif entity == "organization":
            context["organization"]["visible"] = True

            if address_country.organization_id_names:
                context["organization_id"]["enabled"] = True
                context["organization_id"]["visible"] = True
                context["organization_id"]["label"] = address_country.organization_id_name
                context["organization_id"]["pattern"] = address_country.organization_id_input_pattern
                context["organization_id"]["example"] = address_country.organization_id_input_example

            context["organization_phone"]["enabled"] = True
            context["organization_phone"]["visible"] = True
            context["organization_phone"]["label"] = address_country.phone_name
            context["organization_phone"]["pattern"] = address_country.phone_input_pattern
            context["organization_phone"]["example"] = address_country.phone_input_example

        if address_country.iban_names:
            context["bank_iban"]["enabled"] = True
            context["bank_iban"]["visible"] = True
            context["bank_iban"]["label"] = address_country.iban_name
            context["bank_iban"]["pattern"] = address_country.iban_input_pattern
            context["bank_iban"]["example"] = address_country.iban_input_example
        else:
            context["bank_account"]["enabled"] = True
            context["bank_account"]["visible"] = True

    if entity == "person":
        recipient_text = person_name
    elif entity == "organization":
        recipient_text = organization_name
    else:
        recipient_text = ""

    if address_country:
        street_text = (
            address_street
            if address_street
            else (
                "\n".join(
                    [
                        address_street_line0,
                        address_street_line1,
                        address_street_line2,
                        address_street_line3,
                    ]
                ).strip()
            )
        )

        template = Template(address_country.address_output_format)
        context["preview"] = template.render(
            Context(
                {
                    "has_country": address_country is not None,
                    "has_level1area": (address_country is not None) and (address_level1area is not None),
                    "has_level2area": (address_country is not None) and (address_level2area is not None),
                    "has_postcode": len(address_postcode) > 0,
                    "has_recipient": len(recipient_text) > 0,
                    "has_settlement": len(address_settlement) > 0,
                    "has_street": len(street_text) > 0,
                    "country_name": address_country.name if address_country else None,
                    "level1area_code": (address_level1area.iso_3166_a2[2:].upper() if (address_country and address_level1area) else None),
                    "level1area_name": (address_level1area.name if (address_country and address_level1area) else None),
                    "level2area_code": (address_level2area.iso_3166_a2[2:].upper() if (address_country and address_level2area) else None),
                    "level2area_name": (address_level2area.name if (address_country and address_level2area) else None),
                    "postcode_text": address_postcode,
                    "recipient_text": recipient_text,
                    "settlement_text": address_settlement,
                    "street_text": street_text,
                }
            )
        )

    return context


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        context = get_context_from_request(request.GET)

        return render(request, "signup/signup.html", context)

    def post(self, request, *args, **kwargs):
        context = get_context_from_request(request.POST)

        return render(request, "signup/signup.html", context)


class SignUpEntityHtmxView(View):
    def post(self, request, *args, **kwargs):
        context = get_context_from_request(request.POST)

        return render(request, "signup/htmx/entity.html", context)


class SignUpCountryHtmxView(View):
    def post(self, request, *args, **kwargs):
        context = get_context_from_request(request.POST)

        return render(request, "signup/htmx/address-country.html", context)


class SignUpLevel1AreaHtmxView(View):
    def post(self, request, *args, **kwargs):
        context = get_context_from_request(request.POST)

        return render(request, "signup/htmx/address-level1area.html", context)


class SignUpLevel2AreaHtmxView(View):
    def post(self, request, *args, **kwargs):
        context = get_context_from_request(request.POST)

        return render(request, "signup/htmx/address-level2area.html", context)


class SignUpPreviewHtmxView(View):
    def post(self, request, *args, **kwargs):
        context = get_context_from_request(request.POST)

        return render(request, "signup/htmx/preview.html", context)


class SignUpFindMeView(View):
    def get(self, request, *args, **kwargs):
        latitude = float(request.GET.get("latitude"))
        longitude = float(request.GET.get("longitude"))
        settlement = Settlement.objects.get_closest(latitude, longitude)

        if not settlement:
            return JsonResponse(data={})

        return JsonResponse(
            data={
                "address_country": settlement.country.iso_3166_a2,
                "address_level1area": (settlement.level1area.iso_3166_a2 if settlement.level1area else None),
                "address_level2area": (settlement.level2area.iso_3166_a2 if settlement.level2area else None),
                "address_settlement": settlement.name,
            }
        )
