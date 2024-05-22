# Generated by Django 5.0.2 on 2024-05-22 15:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("member", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Knowhow",
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
                ("knowhow_title", models.CharField(max_length=80)),
                ("knowhow_content", models.CharField(max_length=8000)),
                ("knowhow_count", models.IntegerField(default=0)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_knowhow",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="KnowhowCategory",
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
                ("category_name", models.CharField(max_length=50)),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
                    ),
                ),
            ],
            options={
                "db_table": "tbl_knowhow_category",
            },
        ),
        migrations.CreateModel(
            name="KnowhowFile",
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
                ("file_url", models.ImageField(upload_to="file/%Y/%m/%d")),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
                    ),
                ),
            ],
            options={
                "db_table": "tbl_knowhow_file",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="KnowhowLike",
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
                ("status", models.BooleanField(default=False)),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
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
                "db_table": "tbl_knowhow_like",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="KnowhowPlant",
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
                ("plant_name", models.CharField(max_length=50)),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
                    ),
                ),
            ],
            options={
                "db_table": "tbl_knowhow_plant",
            },
        ),
        migrations.CreateModel(
            name="KnowhowRecommend",
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
                ("recommend_url", models.CharField(max_length=255)),
                ("recommend_content", models.CharField(max_length=30)),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
                    ),
                ),
            ],
            options={
                "db_table": "tbl_knowhow_recommend",
            },
        ),
        migrations.CreateModel(
            name="KnowhowReply",
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
                ("knowhow_reply_content", models.CharField(max_length=50)),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
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
                "db_table": "tbl_knowhow_reply",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="KnowhowReplyLike",
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
                ("status", models.BooleanField(default=False)),
                (
                    "knowhow_reply",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhowreply",
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
                "db_table": "tbl_knowhow_reply_like",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="KnowhowScrap",
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
                ("status", models.BooleanField(default=True)),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
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
                "db_table": "tbl_knowhow_scrap",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="KnowhowTag",
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
                ("tag_name", models.CharField(max_length=50)),
                (
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
                    ),
                ),
            ],
            options={
                "db_table": "tbl_knowhow_tag",
            },
        ),
        migrations.CreateModel(
            name="KnowhowView",
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
                    "knowhow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="knowhow.knowhow",
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
                "db_table": "tbl_knowhow_view",
            },
        ),
    ]