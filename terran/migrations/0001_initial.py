# Generated by Django 5.1.2 on 2024-10-23 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                ("iso_4217_n3", models.IntegerField(editable=False, primary_key=True, serialize=False, verbose_name="ISO 4217 N3")),
                ("iso_4217_a3", models.CharField(editable=False, max_length=3, verbose_name="ISO 4217 A3")),
                ("version", models.IntegerField(editable=False)),
                ("is_enabled", models.BooleanField(default=True)),
                ("names", models.JSONField(editable=False)),
                ("decimal_digits", models.IntegerField(editable=False)),
            ],
            options={
                "verbose_name": "Currency",
                "verbose_name_plural": "Currencies",
                "constraints": [
                    models.UniqueConstraint(fields=("iso_4217_n3", "is_enabled"), name="terran_currency_U1"),
                    models.UniqueConstraint(fields=("iso_4217_a3", "is_enabled"), name="terran_currency_U2"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                ("iso_3166_n3", models.IntegerField(editable=False, primary_key=True, serialize=False, verbose_name="ISO 3166 N3")),
                ("iso_3166_a2", models.CharField(editable=False, max_length=2, null=True, verbose_name="ISO 3166 A2")),
                ("iso_3166_a3", models.CharField(editable=False, max_length=3, verbose_name="ISO 3166 A3")),
                ("version", models.IntegerField(editable=False)),
                ("is_enabled", models.BooleanField(default=True)),
                ("names", models.JSONField(editable=False)),
                ("languages", models.JSONField(editable=False, max_length=256)),
                ("address_input_layout", models.JSONField(editable=False)),
                ("address_output_format", models.CharField(editable=False, max_length=256)),
                ("address_level1area_names", models.JSONField(editable=False, null=True)),
                ("address_level2area_names", models.JSONField(editable=False, null=True)),
                ("address_settlement_names", models.JSONField(editable=False, null=True)),
                ("address_street_names", models.JSONField(editable=False, null=True)),
                ("address_postcode_names", models.JSONField(editable=False, null=True)),
                ("address_postcode_input_pattern", models.CharField(editable=False, max_length=256, null=True)),
                ("address_postcode_input_example", models.CharField(editable=False, max_length=256, null=True)),
                ("phone_names", models.JSONField(editable=False, null=True)),
                ("phone_prefixes", models.JSONField(editable=False)),
                ("phone_input_pattern", models.CharField(editable=False, max_length=256)),
                ("phone_input_example", models.CharField(editable=False, max_length=256)),
                ("phone_output_format", models.JSONField(editable=False, max_length=256, null=True)),
                ("organization_id_names", models.JSONField(editable=False, null=True, verbose_name="Organization ID names")),
                ("organization_id_abbreviations", models.JSONField(editable=False, null=True, verbose_name="Organization ID abbreviations")),
                ("organization_id_input_pattern", models.CharField(editable=False, max_length=256, null=True, verbose_name="Organization ID input pattern")),
                ("organization_id_input_example", models.CharField(editable=False, max_length=256, null=True, verbose_name="Organization ID input example")),
                ("organization_id_output_format", models.JSONField(editable=False, max_length=256, null=True, verbose_name="Organization ID output format")),
                ("person_id_names", models.JSONField(editable=False, null=True, verbose_name="Person ID names")),
                ("person_id_abbreviations", models.JSONField(editable=False, null=True, verbose_name="Person ID abbreviations")),
                ("person_id_input_pattern", models.CharField(editable=False, max_length=256, null=True, verbose_name="Person ID input pattern")),
                ("person_id_input_example", models.CharField(editable=False, max_length=256, null=True, verbose_name="Person ID input example")),
                ("person_id_output_format", models.JSONField(editable=False, max_length=256, null=True, verbose_name="Person ID output format")),
                ("iban_names", models.JSONField(editable=False, null=True, verbose_name="IBAN Names")),
                ("iban_input_pattern", models.CharField(editable=False, max_length=256, null=True, verbose_name="IBAN input pattern")),
                ("iban_input_example", models.CharField(editable=False, max_length=256, null=True, verbose_name="IBAN input example")),
                ("iban_output_format", models.JSONField(editable=False, max_length=256, null=True, verbose_name="IBAN output format")),
                ("currency", models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name="+", to="terran.currency")),
            ],
            options={
                "verbose_name": "Country",
                "verbose_name_plural": "Countries",
            },
        ),
        migrations.CreateModel(
            name="Level1Area",
            fields=[
                ("id", models.AutoField(editable=False, primary_key=True, serialize=False)),
                ("iso_3166_a2", models.CharField(editable=False, max_length=32, verbose_name="ISO 3166 A2")),
                ("version", models.IntegerField(editable=False)),
                ("names", models.JSONField(editable=False)),
                ("expando", models.JSONField(default=dict)),
                ("country", models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name="level1areas", to="terran.country")),
            ],
            options={
                "verbose_name": "Level 1 Area",
                "verbose_name_plural": "Level 1 Areas",
            },
        ),
        migrations.CreateModel(
            name="Level2Area",
            fields=[
                ("id", models.AutoField(editable=False, primary_key=True, serialize=False)),
                ("iso_3166_a2", models.CharField(editable=False, max_length=32, verbose_name="ISO 3166 A2")),
                ("version", models.IntegerField(editable=False)),
                ("names", models.JSONField(editable=False)),
                ("expando", models.JSONField(default=dict)),
                ("country", models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name="+", to="terran.country")),
                (
                    "level1area",
                    models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name="level2areas", to="terran.level1area"),
                ),
            ],
            options={
                "verbose_name": "Level 2 Area",
                "verbose_name_plural": "Level 2 Areas",
            },
        ),
        migrations.CreateModel(
            name="Settlement",
            fields=[
                ("id", models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ("version", models.IntegerField(editable=False)),
                ("names", models.JSONField(editable=False)),
                ("place_type", models.IntegerField(choices=[(0, "Other"), (67, "City"), (72, "Hamlet"), (84, "Town"), (86, "Village")])),
                ("population", models.IntegerField()),
                ("latitude", models.FloatField(null=True)),
                ("longitude", models.FloatField(null=True)),
                ("geocell", models.IntegerField()),
                ("expando", models.JSONField()),
                ("country", models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name="settlements", to="terran.country")),
                (
                    "level1area",
                    models.ForeignKey(
                        editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="settlements", to="terran.level1area"
                    ),
                ),
                (
                    "level2area",
                    models.ForeignKey(
                        editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="settlements", to="terran.level2area"
                    ),
                ),
            ],
            options={
                "verbose_name": "Settlement",
                "verbose_name_plural": "Settlements",
            },
        ),
        migrations.CreateModel(
            name="CountryCurrency",
            fields=[
                ("id", models.AutoField(editable=False, primary_key=True, serialize=False)),
                ("currency", models.CharField(editable=False, max_length=3, verbose_name="ISO 4217 A3")),
                ("version", models.IntegerField(editable=False)),
                ("since", models.DateField(editable=False)),
                ("until", models.DateField(editable=False, null=True)),
                ("country", models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name="+", to="terran.country")),
            ],
            options={
                "verbose_name": "Country Currency",
                "verbose_name_plural": "Country Currencies",
                "constraints": [models.UniqueConstraint(fields=("country", "currency", "since"), name="terran_countrycurrency_U1")],
            },
        ),
        migrations.AddConstraint(
            model_name="country",
            constraint=models.UniqueConstraint(fields=("iso_3166_a2", "is_enabled"), name="terran_country_U1"),
        ),
        migrations.AddConstraint(
            model_name="country",
            constraint=models.UniqueConstraint(fields=("iso_3166_a3", "is_enabled"), name="terran_country_U2"),
        ),
        migrations.AddConstraint(
            model_name="country",
            constraint=models.UniqueConstraint(fields=("iso_3166_n3", "is_enabled"), name="terran_country_U3"),
        ),
        migrations.AddIndex(
            model_name="level1area",
            index=models.Index(fields=["country", "iso_3166_a2"], name="terran_level1area_I1"),
        ),
        migrations.AddConstraint(
            model_name="level1area",
            constraint=models.UniqueConstraint(fields=("iso_3166_a2",), name="terran_level1area_U1"),
        ),
        migrations.AddIndex(
            model_name="level2area",
            index=models.Index(fields=["country", "level1area", "iso_3166_a2"], name="terran_level2area_I1"),
        ),
        migrations.AddConstraint(
            model_name="level2area",
            constraint=models.UniqueConstraint(fields=("iso_3166_a2",), name="terran_level2area_U1"),
        ),
        migrations.AddIndex(
            model_name="settlement",
            index=models.Index(fields=["country", "level1area", "level2area", "place_type"], name="terran_settlement_I1"),
        ),
        migrations.AddIndex(
            model_name="settlement",
            index=models.Index(fields=["country", "level1area", "level2area", "population"], name="terran_settlement_I2"),
        ),
        migrations.AddIndex(
            model_name="settlement",
            index=models.Index(fields=["latitude", "longitude"], name="terran_settlement_I3"),
        ),
        migrations.AddIndex(
            model_name="settlement",
            index=models.Index(fields=["geocell"], name="terran_settlement_I4"),
        ),
        migrations.AddConstraint(
            model_name="settlement",
            constraint=models.UniqueConstraint(fields=("id",), name="terran_settlement_U1"),
        ),
    ]
