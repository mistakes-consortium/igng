from django.db import models

class GalleryManager(models.Manager):
    def default(self, user):
        o = self.get(title="Default", user=user)
        return  o

    def notdefault(self, user):
        qs = self.exclude(title="Default", deletable=False)
        qs = qs.filter(user=user)
        return qs