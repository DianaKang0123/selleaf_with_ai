# Generated by Django 5.0.2 on 2024-05-22 15:55

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("lecture", "0001_initial"),
        ("member", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Apply",
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
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "updated_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "apply_status",
                    models.IntegerField(
                        choices=[
                            (-2, "바로 구매"),
                            (-3, "장바구니"),
                            (0, "신청 완료"),
                            (-1, "신청 취소"),
                            (1, "수업 완료"),
                            (2, "신청중"),
                        ],
                        default=2,
                    ),
                ),
                ("date", models.CharField(max_length=100)),
                ("time", models.CharField(max_length=100)),
                ("kit", models.CharField(default="offline", max_length=100)),
                ("quantity", models.IntegerField(default=1)),
                (
                    "lecture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="lecture.lecture",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_apply",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Trainee",
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
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "updated_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("trainee_name", models.CharField(max_length=100)),
                (
                    "apply",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="apply.apply"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_trainees",
                "ordering": ["-id"],
            },
        ),
    ]
