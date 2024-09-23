from ._format import _get_localized_name
from .country import Country
from .level1area import Level1Area
from .level2area import Level2Area
from django.db.models import CASCADE
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import Index
from django.db.models import IntegerField
from django.db.models import JSONField
from django.db.models import Model
from django.db.models import Manager
from django.db.models import UniqueConstraint
from math import cos
from math import radians


SETTLEMENT_PLACE_TYPE_CHOICES = [
    (0, "Other"),
    (ord("C"), "City"),
    (ord("H"), "Hamlet"),
    (ord("T"), "Town"),
    (ord("V"), "Village"),
]


# Latitude ranges from -90 to 90 degrees, while longitude ranges from -180 to 180 degrees.
# All meridians, which are lines of constant longitude and imaginary circles on the Earth’s surface passing through both the North and South geographic poles, are approximately the same length. In contrast, all parallels, which are lines of constant latitude and imaginary circles extending around the Earth parallel to the equator, vary in length.
# The Earth’s circumference is 40,075 km when measured around the equator and 40,007 km when measured through the poles. The length of one degree at the equator is approximately 111.32 km (40,075 km / 360 degrees), which is the greatest length one degree can have. At any other parallel or meridian, one degree will be shorter.
# OpenStreetMap stores coordinates with 7 decimal digits, effectively storing them as integers multiplied by (10^7). This translates to a precision of about 1.1 cm (approximately 0.45 inches) in the worst-case scenario, which is more than sufficient for all practical purposes.
# A double-precision floating-point number can store 14-16 decimal digits. Assuming up to three digits for the whole part (with 180 being the maximum absolute value) and seven digits for the fractional part, this adds up to 10 decimal digits. Therefore, double-precision floating-point numbers are more than adequate for storing longitude and latitude.


class SettlementManager(Manager):
    def filter_neighbors(self, latitude: float, longitude: float):
        lat_index = int(10 * (latitude + 90))
        lat_lower = lat_index - 1
        lat_upper = lat_index + 2
        lon_width = min(9, int(3.3 / (0.1 + cos(radians(latitude)))))
        lon_index = int(10 * (longitude + 180))
        lon_lower = lon_index - lon_width
        lon_upper = lon_index + lon_width + 1
        geocells = []

        for lat in range(lat_lower, lat_upper):
            for lon in range(lon_lower, lon_upper):
                geocells.append(3600 * ((lat + 1800) % 1800) + (lon + 3600) % 3600)

        geocells = sorted(geocells)

        return self.filter(geocell__in=geocells)

    def get_closest(self, latitude: float, longitude: float):
        settlements = self.filter_neighbors(latitude, longitude)
        closest_settlement = None
        closest_distance = 100000

        for settlement in settlements:
            distance = (settlement.latitude - latitude) ** 2
            +(((settlement.longitude - longitude) * cos(radians(latitude))) ** 2)

            if distance < closest_distance:
                closest_distance = distance
                closest_settlement = settlement

        return closest_settlement


class Settlement(Model):
    objects = SettlementManager()

    id = IntegerField(primary_key=True, editable=False)
    country = ForeignKey(Country, CASCADE, related_name="settlements", editable=False)
    level1area = ForeignKey(
        Level1Area, CASCADE, related_name="settlements", null=True, editable=False
    )
    level2area = ForeignKey(
        Level2Area, CASCADE, related_name="settlements", null=True, editable=False
    )
    names = JSONField(editable=False)
    place_type = IntegerField(choices=SETTLEMENT_PLACE_TYPE_CHOICES)
    population = IntegerField()
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    # A value between 0 and 6483600, geographic cell index
    # A geographic cell is a rectange approximately 11x11 km at most.
    # A geographic cell is an effective way to find settlement from latitude and longitude without invoving a GIS engine.
    geocell = IntegerField()
    expando = JSONField()

    class Meta:
        verbose_name = "Settlement"
        verbose_name_plural = "Settlements"
        constraints = (
            UniqueConstraint(
                name="%(app_label)s_%(class)s_U1",
                fields=("id",),
            ),
        )
        indexes = [
            Index(
                name="%(app_label)s_%(class)s_I1",
                fields=(
                    "country",
                    "level1area",
                    "level2area",
                    "place_type",
                ),
            ),
            Index(
                name="%(app_label)s_%(class)s_I2",
                fields=(
                    "country",
                    "level1area",
                    "level2area",
                    "population",
                ),
            ),
            Index(
                name="%(app_label)s_%(class)s_I3",
                fields=(
                    "latitude",
                    "longitude",
                ),
            ),
            Index(
                name="%(app_label)s_%(class)s_I4",
                fields=("geocell",),
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def name(self):
        return _get_localized_name(self.names)

    # Ensure "." as decimal separator and 7 fractional part digits for any locale.
    @property
    def lat(self):
        value = str(int(self.latitude * 10000000))

        return value[:-7] + "." + value[-7:]

    # Ensure "." as decimal separator and 7 fractional part digits for any locale.
    @property
    def lon(self):
        value = str(int(self.longitude * 10000000))

        return value[:-7] + "." + value[-7:]
