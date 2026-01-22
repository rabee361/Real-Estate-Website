from django.contrib.gis.db import models
from users.models import CustomUser


class Address(models.Model):
    country = models.CharField(max_length=30)
    governate = models.CharField(max_length=20)
    area = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=40)
    building_no = models.CharField()

    def __str__(self):
        return f'{self.country}/{self.governate}/{self.area}/{self.neighborhood}/{self.building_no}'

class Estate(models.Model):
    TYPES = (
        ('Shop','Shop'),
        ('House','House'),
        ('Land','Land')
    )
    description = models.TextField()
    space = models.IntegerField()
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    coordinates = models.PointField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    deadline = models.DateField()
    created = models.DateField(auto_now_add=True)
    property_type = models.CharField(choices=TYPES,max_length=15)
    active = models.BooleanField()
    price = models.IntegerField()

    def __str__(self):
        return f'{self.owner.username}-{self.property_type}'

class Covers(models.Model):
    image = models.ImageField(upload_to='covers', default='covers/default.jpg')
    created = models.DateTimeField(auto_now_add=True,null=True)

class ContactMedia(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='contact_media', default='contact_media/default.jpg')
    created = models.DateTimeField(auto_now_add=True,null=True)

class ContactInfo(models.Model):
    value = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True,null=True)

class Offer(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True,null=True)
    estate = models.ForeignKey(Estate, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.username}-{self.price}'

class Section(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True,null=True)

class EstateSection(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,null=True)



    


