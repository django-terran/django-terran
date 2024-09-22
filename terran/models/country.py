from ._format import _get_localized_name
from .currency import Currency
from django.db.models import AutoField
from django.db.models import BooleanField
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import JSONField
from django.db.models import Manager
from django.db.models import Model
from django.db.models import UniqueConstraint


class CountryManager(Manager):
    def get_by_natural_key(self, code):
        if isinstance(code, int):
            return self.get(iso_3166_n3=code)

        if not isinstance(code, str):
            raise Country.DoesNotExist()

        code = code.upper()

        if len(code) == 2:
            if (code[0] >= "A") and (code[0] <= "Z"):
                return self.get(iso_3166_a2=code)
        elif len(code) == 3:
            if (code[0] >= "A") and (code[0] <= "Z"):
                return self.get(iso_3166_a3=code)
            elif (code[0] >= "0") and (code[0] <= "9"):
                return self.get(iso_3166_n3=int(code))

        raise Country.DoesNotExist()


class Country(Model):
    objects = CountryManager()

    iso_3166_n3 = IntegerField(
        primary_key=True, editable=False, verbose_name="ISO 3166 N3"
    )
    iso_3166_a2 = CharField(
        max_length=2, null=True, editable=False, verbose_name="ISO 3166 A2"
    )
    iso_3166_a3 = CharField(max_length=3, editable=False, verbose_name="ISO 3166 A3")
    is_enabled = BooleanField(default=True)
    currency = ForeignKey(Currency, CASCADE, related_name="+", editable=False)
    names = JSONField(editable=False)
    languages = JSONField(max_length=256, editable=False)
    address_input_layout = JSONField(editable=False)
    address_output_format = CharField(max_length=256, editable=False)
    address_level1area_names = JSONField(null=True, editable=False)
    address_level2area_names = JSONField(null=True, editable=False)
    address_settlement_names = JSONField(null=True, editable=False)
    address_street_names = JSONField(null=True, editable=False)
    address_postcode_names = JSONField(null=True, editable=False)
    address_postcode_input_pattern = CharField(
        max_length=256, null=True, editable=False
    )
    address_postcode_input_example = CharField(
        max_length=256, null=True, editable=False
    )
    phone_names = JSONField(null=True, editable=False)
    phone_prefixes = JSONField(editable=False)
    phone_input_pattern = CharField(max_length=256, editable=False)
    phone_input_example = CharField(max_length=256, editable=False)
    phone_output_format = JSONField(max_length=256, null=True, editable=False)
    organization_id_names = JSONField(
        null=True, editable=False, verbose_name="Organization ID names"
    )
    organization_id_abbreviations = JSONField(
        null=True, editable=False, verbose_name="Organization ID abbreviations"
    )
    organization_id_input_pattern = CharField(
        max_length=256,
        null=True,
        editable=False,
        verbose_name="Organization ID input pattern",
    )
    organization_id_input_example = CharField(
        max_length=256,
        null=True,
        editable=False,
        verbose_name="Organization ID input example",
    )
    organization_id_output_format = JSONField(
        max_length=256,
        null=True,
        editable=False,
        verbose_name="Organization ID output format",
    )
    person_id_names = JSONField(
        null=True, editable=False, verbose_name="Person ID names"
    )
    person_id_abbreviations = JSONField(
        null=True, editable=False, verbose_name="Person ID abbreviations"
    )
    person_id_input_pattern = CharField(
        max_length=256,
        null=True,
        editable=False,
        verbose_name="Person ID input pattern",
    )
    person_id_input_example = CharField(
        max_length=256,
        null=True,
        editable=False,
        verbose_name="Person ID input example",
    )
    person_id_output_format = JSONField(
        max_length=256,
        null=True,
        editable=False,
        verbose_name="Person ID output format",
    )
    iban_names = JSONField(null=True, editable=False, verbose_name="IBAN Names")
    iban_input_pattern = CharField(
        max_length=256, null=True, editable=False, verbose_name="IBAN input pattern"
    )
    iban_input_example = CharField(
        max_length=256, null=True, editable=False, verbose_name="IBAN input example"
    )
    iban_output_format = JSONField(
        max_length=256, null=True, editable=False, verbose_name="IBAN output format"
    )

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        constraints = (
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U1",
                fields=(
                    "iso_3166_a2",
                    "is_enabled",
                ),
            ),
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U2",
                fields=(
                    "iso_3166_a3",
                    "is_enabled",
                ),
            ),
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U3",
                fields=(
                    "iso_3166_n3",
                    "is_enabled",
                ),
            ),
        )

    def __str__(self):
        return self.name or self.iso_3166_a3

    def natural_key(self):
        return (self.iso_3166_n3,)

    @property
    def name(self):
        return _get_localized_name(self.names)

    @property
    def address_level1area_name(self):
        return _get_localized_name(self.address_level1area_names)

    @property
    def address_level2area_name(self):
        return _get_localized_name(self.address_level2area_names)

    @property
    def address_settlement_name(self):
        return _get_localized_name(self.address_settlement_names)

    @property
    def address_street_name(self):
        return _get_localized_name(self.address_street_names)

    @property
    def address_postcode_name(self):
        return _get_localized_name(self.address_postcode_names)

    @property
    def phone_name(self):
        return _get_localized_name(self.phone_names)

    @property
    def organization_id_name(self):
        return _get_localized_name(self.organization_id_names)

    @property
    def organization_id_abbreviation(self):
        return _get_localized_name(self.organization_id_abbreviations)

    @property
    def person_id_name(self):
        return _get_localized_name(self.person_id_names)

    @property
    def person_id_abbreviation(self):
        return _get_localized_name(self.person_id_abbreviations)

    @property
    def iban_name(self):
        return _get_localized_name(self.iban_names)


class CountryCurrencyManager(Manager):
    def get_by_natural_key(self, country_code, currency_code, since):
        if isinstance(country_code, int):
            return self.get(country__iso_3166_n3=country_code, currency=currency_code)

        if not isinstance(code, str):
            raise Country.DoesNotExist()

        code = code.upper()

        if len(code) == 2:
            if (code[0] >= "A") and (code[0] <= "Z"):
                return self.get(
                    country__iso_3166_a2=country_code, currency=currency_code
                )
        elif len(code) == 3:
            if (code[0] >= "A") and (code[0] <= "Z"):
                return self.get(
                    country__iso_3166_a3=country_code, currency=currency_code
                )
            elif (code[0] >= "0") and (code[0] <= "9"):
                return self.get(
                    country__iso_3166_n3=int(country_code), currency=currency_code
                )

        raise Country.DoesNotExist()


class CountryCurrency(Model):
    objects = CountryCurrencyManager()

    id = AutoField(primary_key=True, editable=False)
    country = ForeignKey(Country, CASCADE, related_name="+", editable=False)
    currency = CharField(max_length=3, editable=False, verbose_name="ISO 4217 A3")
    since = DateField(editable=False)
    until = DateField(editable=False, null=True)

    class Meta:
        verbose_name = "Country Currency"
        verbose_name_plural = "Country Currencies"
        constraints = (
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U1",
                fields=("country", "currency", "since"),
            ),
        )

    def __str__(self):
        return f"{self.country} {self.currency} {self.since.isoformat()}"

    def natural_key(self):
        return (self.country.iso_3166_n3, self.currency, self.since)
