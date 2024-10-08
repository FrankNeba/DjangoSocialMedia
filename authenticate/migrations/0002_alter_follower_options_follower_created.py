# Generated by Django 5.1.1 on 2024-09-19 05:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follower',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='follower',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
