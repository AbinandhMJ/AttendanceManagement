# Generated by Django 5.0.4 on 2024-06-29 09:34

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=20, unique=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('employee', 'Employee')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in_time', models.DateTimeField(blank=True, null=True)),
                ('clock_out_time', models.DateTimeField(blank=True, null=True)),
                ('break_in_time', models.DateTimeField(blank=True, null=True)),
                ('break_out_time', models.DateTimeField(blank=True, null=True)),
                ('work_duration', models.DurationField(default=datetime.timedelta)),
                ('break_duration', models.DurationField(default=datetime.timedelta)),
                ('overtime_duration', models.DurationField(default=datetime.timedelta)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.userprofile')),
            ],
        ),
    ]
