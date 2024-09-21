from ._format import _get_localized_name
from .country import Country
from .level1area import Level1Area
from django.db.models import AutoField
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import Index
from django.db.models import JSONField
from django.db.models import Manager
from django.db.models import Model
from django.db.models import UniqueConstraint


class Level2AreaManager(Manager):
    def get_by_natural_key(self, code):
        if not isinstance(code, str):
            raise Level2Area.DoesNotExist()

        code = code.lower()

        return self.get(iso_3166_a2=code)


class Level2Area(Model):
    objects = Level2AreaManager()

    id = AutoField(primary_key=True, editable=False)
    country = ForeignKey(Country, CASCADE, related_name="+", editable=False)
    level1area = ForeignKey(
        Level1Area, CASCADE, related_name="level2areas", editable=False
    )
    iso_3166_a2 = CharField(max_length=32, editable=False, verbose_name="ISO 3166 A2")
    names = JSONField(editable=False)
    expando = JSONField(default=dict)

    class Meta:
        verbose_name = "Level 2 Area"
        verbose_name_plural = "Level 2 Areas"
        constraints = (
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U1",
                fields=("iso_3166_a2",),
            ),
        )
        indexes = [
            Index(
                name="%(app_label)s_%(class)s_I1",
                fields=(
                    "country",
                    "level1area",
                    "iso_3166_a2",
                ),
            ),
        ]

    def __str__(self):
        return self.name or self.iso_3166_a2

    def natural_key(self):
        return (self.iso_3166_a2,)

    @property
    def name(self):
        return _get_localized_name(self.names)
