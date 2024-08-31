# Generated by Django 5.1 on 2024-08-30 10:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Kindergarten",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("student_limit", models.PositiveIntegerField()),
                ("num_classes", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("limit", models.PositiveIntegerField()),
                (
                    "kindergarten",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="classes",
                        to="registration.kindergarten",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("tc_number", models.CharField(max_length=11, unique=True)),
                ("birth_date", models.DateField()),
                ("address", models.CharField(max_length=500)),
                ("toilet_trained", models.BooleanField(default=False)),
                ("school_experience", models.BooleanField(default=False)),
                (
                    "school_type",
                    models.CharField(
                        blank=True,
                        choices=[("Devlet", "Devlet"), ("Özel", "Özel")],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("sibling_count", models.PositiveIntegerField(default=0)),
                ("mother_alive", models.BooleanField(default=True)),
                (
                    "mother_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "mother_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "mother_education",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("mother_job", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "mother_employer",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "mother_salary",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                ("father_alive", models.BooleanField(default=True)),
                (
                    "father_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "father_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "father_education",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("father_job", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "father_employer",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "father_salary",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                ("owns_house", models.BooleanField(default=True)),
                (
                    "marital_status",
                    models.CharField(
                        choices=[("Birlikte", "Birlikte"), ("Ayrı", "Ayrı")],
                        max_length=10,
                    ),
                ),
                (
                    "registration_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("points", models.IntegerField(default=0)),
                ("disqualified", models.BooleanField(default=False)),
                (
                    "assigned_class",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="registration.class",
                    ),
                ),
                (
                    "preferred_kindergarten_1",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="preferred_1",
                        to="registration.kindergarten",
                    ),
                ),
                (
                    "preferred_kindergarten_2",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="preferred_2",
                        to="registration.kindergarten",
                    ),
                ),
                (
                    "preferred_kindergarten_3",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="preferred_3",
                        to="registration.kindergarten",
                    ),
                ),
            ],
        ),
    ]
