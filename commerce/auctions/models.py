from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    header = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller")
    image_url = models.CharField(max_length=5000)
    description = models.CharField(max_length=500)
    is_live = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")