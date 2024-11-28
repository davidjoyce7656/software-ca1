# Generated by Django 4.2.16 on 2024-11-28 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whiskeycellar', '0003_remove_whiskeybrand_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='whiskey',
            name='abv',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='whiskey',
            name='amount',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='whiskey',
            name='distillery',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='whiskey',
            name='finish',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='whiskey',
            name='nose',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='whiskey',
            name='taste',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
