# Generated by Django 2.2.1 on 2019-10-07 17:08

from django.db import migrations, models
import django.db.models.deletion
import kilometers.models
import uren.models


class Migration(migrations.Migration):

    dependencies = [
        ('kilometers', '0004_location_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='activity',
            field=models.ForeignKey(blank=True, default=uren.models.get_default_km_activity, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trips', to='uren.Activity'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='origin',
            field=models.ForeignKey(default=kilometers.models.get_default_location, on_delete=django.db.models.deletion.PROTECT, related_name='trip_from', to='kilometers.Location'),
        ),
    ]