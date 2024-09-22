from ._format import _get_localized_name
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import JSONField
from django.db.models import Manager
from django.db.models import Model
from django.db.models import UniqueConstraint


class CurrencyManager(Manager):
    def get_by_natural_key(self, code):
        if isinstance(code, int):
            return self.get(iso_4217_n3=code)

        if not isinstance(code, str):
            raise Currency.DoesNotExist()

        code = code.upper()

        return self.get(iso_4217_a3=code)


class Currency(Model):
    objects = CurrencyManager()

    iso_4217_n3 = IntegerField(
        primary_key=True, editable=False, verbose_name="ISO 4217 N3"
    )
    iso_4217_a3 = CharField(max_length=3, editable=False, verbose_name="ISO 4217 A3")
    is_enabled = BooleanField(default=True)
    names = JSONField(editable=False)
    decimal_digits = IntegerField(editable=False)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        constraints = (
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U1",
                fields=(
                    "iso_4217_n3",
                    "is_enabled",
                ),
            ),
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U2",
                fields=(
                    "iso_4217_a3",
                    "is_enabled",
                ),
            ),
        )

    def __str__(self):
        return self.name or self.iso_4217_a3

    def natural_key(self):
        return (self.iso_4217_a3,)

    @property
    def name(self):
        return _get_localized_name(self.names)
