# Generated by Django 3.1.14 on 2022-05-24 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20220524_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokemon_entities.pokemon'),
        ),
    ]
