from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    phone = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    invite_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals'
    )

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone
