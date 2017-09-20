from taggit.models import TagBase
from django.db import models

class UserTag(TagBase):
    def request_filter(self, request):
        return models.Q(user=request.user)