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
            name="Post",
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
                ("post_title", models.CharField(max_length=80)),
                ("post_content", models.CharField(max_length=8000)),
                ("post_count", models.IntegerField(default=0)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="PostCategory",
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
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.post"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_category",
            },
        ),
        migrations.CreateModel(
            name="PostFile",
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
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.post"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_file",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="PostLike",
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
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.post"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_like",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="PostPlant",
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
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.post"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_plant",
            },
        ),
        migrations.CreateModel(
            name="PostReply",
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
                ("post_reply_content", models.CharField(max_length=50)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.post"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_reply",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="PostReplyLike",
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
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
                (
                    "post_reply",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.postreply"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_reply_like",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="PostScrap",
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
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="member.member"
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.post"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_scrap",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="PostTag",
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
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="post.post"
                    ),
                ),
            ],
            options={
                "db_table": "tbl_post_tag",
            },
        ),
    ]
