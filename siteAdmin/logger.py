from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Patient, Doctor,Admin
from .models import Log

def create_log(user, action, details):
    if isinstance(user, Admin):
        user_type = "Admin"
    elif isinstance(user, Doctor):
        user_type = "Doctor"
    elif isinstance(user, Patient):
        user_type = "Patient"
    else:
        user_type = "Other"
    Log.objects.create(
        user_type=user_type,
        user_id=user.id,
        action=action,
        details=details,
    )