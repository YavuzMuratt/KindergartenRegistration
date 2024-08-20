# Generated by Django 5.1 on 2024-08-16 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "kindergarten_registration",
            "0002_remove_student_kindergarten_remove_student_parents_and_more",
        ),
    ]

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
                ("name", models.CharField(max_length=100)),
                ("branches", models.IntegerField(default=5)),
                ("student_limit_per_class", models.IntegerField(default=10)),
                ("total_student_limit", models.IntegerField(default=50)),
            ],
        ),
        migrations.AddField(
            model_name="student",
            name="school_type",
            field=models.CharField(
                blank=True,
                choices=[("Public", "Public"), ("Private", "Private")],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="sibling_count",
            field=models.IntegerField(default=0),
        ),
    ]
