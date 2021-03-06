# Generated by Django 3.1.3 on 2021-02-25 11:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import home.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0005_auto_20210225_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextended',
            name='display_picture',
        ),
        migrations.AlterField(
            model_name='userextended',
            name='gender',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userextended',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProfilePictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_on', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('display_picture', models.ImageField(blank=True, null=True, upload_to=home.models.dpPath)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
