# Generated by Django 5.0.6 on 2024-10-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0010_remove_enrollment_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True),
        ),
    ]
