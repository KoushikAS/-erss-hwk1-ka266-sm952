# Generated by Django 4.1.5 on 2023-01-26 21:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('emailId', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('FOUR_SEATER', '4 Seats'), ('SIX_SEATER', '6 Seats')], default='FOUR_SEATER', max_length=15)),
                ('max_passengers', models.IntegerField()),
                ('license_no', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ridesharingapp.user')),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ridesharingapp.vehicle')),
            ],
            bases=('ridesharingapp.user',),
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passengers', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='party_owner', to='ridesharingapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('rideId', models.AutoField(primary_key=True, serialize=False)),
                ('isSharable', models.BooleanField(default=False)),
                ('source', models.CharField(max_length=500)),
                ('destination', models.CharField(max_length=500)),
                ('destinationArrivalTimeStamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('CONFIRMED', 'Confirmed'), ('COMPLETED', 'Completed')], default='OPEN', max_length=10)),
                ('rideOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ride_owner', to='ridesharingapp.party')),
                ('rideShared', models.ManyToManyField(blank=True, to='ridesharingapp.party')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='ridesharingapp.driver')),
            ],
        ),
    ]
