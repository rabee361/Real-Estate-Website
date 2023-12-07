from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.user.username}-{self.price}'


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
    description = models.TextField
    space = models.IntegerField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    coordinates = models.PointField()
    offers = models.ManyToManyField(Offer)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    deadline = models.DateField()
    created = models.DateField(auto_now_add=True)
    property_type = models.CharField(choices=TYPES,max_length=15)
    active = models.BooleanField()
    price = models.IntegerField()


    def __str__(self):
        return f'{self.owner.username}-{self.property_type}'



    


