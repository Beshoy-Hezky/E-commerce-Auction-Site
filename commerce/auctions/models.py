from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    header = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller")
    image_url = models.CharField(max_length=5000)
    description = models.CharField(max_length=500)
    starting_price = models.FloatField(null=True, blank=True, default=0.0)
    is_live = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")

    def __str__(self):
       return f"{self.header} ({self.category})"
