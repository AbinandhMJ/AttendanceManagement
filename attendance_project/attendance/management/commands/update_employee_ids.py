from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from attendance.models import UserProfile
import uuid

class Command(BaseCommand):
    help = 'Update existing users with unique employee IDs'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created or not profile.employee_id:
                profile.employee_id = str(uuid.uuid4())
                profile.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated employee_id for user: {user.username}'))
