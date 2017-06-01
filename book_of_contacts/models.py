from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    session_key = models.CharField(max_length=128, default=None, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    country = models.CharField(max_length=24, default=None, null=True)
    town = models.CharField(max_length=24, default=None, null=True)
    phone_nmb = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    email = models.EmailField(default=None)
    birthday = models.DateField(default=None, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    # def __str__(self):
    #     return "User: %s %s" % (self.first_name, self.last_name)


class Userdata(models.Model):
    api_key = models.CharField(max_length=128, default=None, null=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)

