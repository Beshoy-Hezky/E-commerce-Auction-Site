from django.contrib import admin
from .models import User,Category,AuctionListing

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(User)
admin.site.register(Category)
