# Generated by Django 3.1.3 on 2021-04-10 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_auto_20210407_2021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationforpost',
            name='notification',
        ),
        migrations.RemoveField(
            model_name='notificationforpost',
            name='post',
        ),
        migrations.RemoveField(
            model_name='notificationsforfriendrequest',
            name='friend_request',
        ),
        migrations.RemoveField(
            model_name='notificationsforfriendrequest',
            name='notification',
        ),
        migrations.DeleteModel(
            name='NotificationForBirthday',
        ),
        migrations.DeleteModel(
            name='NotificationForPost',
        ),
        migrations.DeleteModel(
            name='NotificationsForFriendRequest',
        ),
    ]