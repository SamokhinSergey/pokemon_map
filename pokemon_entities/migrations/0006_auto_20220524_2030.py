# Generated by Django 3.1.14 on 2022-05-24 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_auto_20220524_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemonentity',
            old_name='pokemon',
            new_name='Pokemon',
        ),
    ]
