# Generated by Django 4.1.2 on 2022-10-09 22:58

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                help_text="",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="store.category",
            ),
        ),
    ]
