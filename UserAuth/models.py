from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ValidateUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=255, blank=True, null=True)
