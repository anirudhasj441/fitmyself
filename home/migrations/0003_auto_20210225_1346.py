# Generated by Django 3.1.3 on 2021-02-25 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_userextended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextended',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
