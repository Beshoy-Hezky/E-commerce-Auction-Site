from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Bid(models.Model):
    value = models.FloatField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="users_bid")


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    header = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller")
    image_url = models.CharField(max_length=5000)
    description = models.CharField(max_length=500)
    starting_price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="user_price")
    is_live = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="userswatchlist")

    def __str__(self):
        return f"{self.header} ({self.category})"
