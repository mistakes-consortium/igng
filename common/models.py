from django.db import models
from django.conf import settings
from enumfields import EnumIntegerField, Enum

User = settings.AUTH_USER_MODEL
# Create your models here.

class UISettinsEnum(Enum):
    LIGHT = 0
    DARK = 1

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    ui_darkness = EnumIntegerField(UISettinsEnum, default=UISettinsEnum.LIGHT, blank=False, null=False)
