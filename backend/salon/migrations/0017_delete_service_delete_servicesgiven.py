# Generated by Django 5.2.3 on 2025-07-18 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0016_remove_servicesgiven_salonappointmentid_and_more'),
        ('users', '0011_remove_customerprofile_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='service',
        ),
        migrations.DeleteModel(
            name='servicesGiven',
        ),
    ]
