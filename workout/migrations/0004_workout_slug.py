# Generated by Django 3.1.3 on 2021-03-07 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0003_auto_20210304_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='slug',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
