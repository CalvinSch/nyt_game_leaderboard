# Generated by Django 5.0.2 on 2024-02-24 23:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboards', '0002_remove_connectionsscore_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectionsscore',
            name='raw_score_details',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
