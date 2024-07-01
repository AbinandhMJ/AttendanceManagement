from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, datetime
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('manager', 'Manager'), ('employee', 'Employee')])

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    clock_in_time = models.TimeField(null=True, blank=True)
    clock_out_time = models.TimeField(null=True, blank=True)
    break_in_time = models.DateTimeField(null=True, blank=True)
    break_out_time = models.DateTimeField(null=True, blank=True)
    work_duration = models.DurationField(default=timedelta)
    break_duration = models.DurationField(default=timedelta)
    overtime_duration = models.DurationField(default=timedelta)
    date = models.DateField()

    def save(self, *args, **kwargs):
        if self.clock_in_time and self.clock_out_time:
            datetime_format = '%H:%M:%S'
            clock_in_datetime = datetime.strptime(self.clock_in_time.strftime(datetime_format), datetime_format)
            clock_out_datetime = datetime.strptime(self.clock_out_time.strftime(datetime_format), datetime_format)
            self.work_duration = clock_out_datetime - clock_in_datetime
            if self.work_duration > timedelta(hours=8, minutes=30):
                self.overtime_duration = self.work_duration - timedelta(hours=8, minutes=30)
            else:
                self.overtime_duration = timedelta(0)
        if self.break_in_time and self.break_out_time:
            self.break_duration = self.break_out_time - self.break_in_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_profile.employee_id} - {self.date}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, employee_id=str(uuid.uuid4()))

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
