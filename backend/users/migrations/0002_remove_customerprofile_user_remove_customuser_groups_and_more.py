# Generated by Django 5.2.3 on 2025-07-05 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0004_remove_servicesgiven_salonappointmentid_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='serviceOffered',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='adminProfile',
        ),
        migrations.DeleteModel(
            name='customerProfile',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='employeeProfile',
        ),
    ]
