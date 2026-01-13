from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='images/users',default='images/account.jpg')
    location = gis_models.PointField(null=True,blank=True)

    def __str__(self):
        return self.username