# attendance/management/commands/create_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from attendance.models import UserProfile

class Command(BaseCommand):
    help = 'Creates manager and employee users'

    def handle(self, *args, **kwargs):
        # Create Admin User
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(username='admin', password='admin_password')
            admin_user.save()
            admin_profile = UserProfile.objects.create(user=admin_user, employee_id='A001', role='admin')
            self.stdout.write(self.style.SUCCESS('Admin user created.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))

        # Create Manager User
        if not User.objects.filter(username='manager').exists():
            manager_user = User.objects.create_user(username='manager', password='manager_password')
            manager_user.save()
            manager_profile = UserProfile.objects.create(user=manager_user, employee_id='M001', role='manager')
            self.stdout.write(self.style.SUCCESS('Manager user created.'))
        else:
            self.stdout.write(self.style.WARNING('Manager user already exists.'))

        # Create Employee User
        if not User.objects.filter(username='employee').exists():
            employee_user = User.objects.create_user(username='employee', password='employee_password')
            employee_user.save()
            employee_profile = UserProfile.objects.create(user=employee_user, employee_id='E001', role='employee')
            self.stdout.write(self.style.SUCCESS('Employee user created.'))
        else:
            self.stdout.write(self.style.WARNING('Employee user already exists.'))
