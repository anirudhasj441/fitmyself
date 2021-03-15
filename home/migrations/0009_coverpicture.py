# Generated by Django 3.1.3 on 2021-03-10 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import home.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0008_userextended_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('cover_photo', models.ImageField(blank=True, null=True, upload_to=home.models.coverPhotoPath)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
