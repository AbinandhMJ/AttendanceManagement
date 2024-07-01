from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Define custom permission
content_type = ContentType.objects.get_for_model(Attendance)
permission = Permission.objects.create(
    codename='view_attendance',
    name='Can view attendance',
    content_type=content_type,
)

# Assign permission to roles (e.g., in a management command or admin interface)
manager_group.permissions.add(permission)
