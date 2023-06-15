from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, AuctionListing

from .models import User


def index(request):
    listings = AuctionListing.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "categories": categories,
        "listings":listings
    })


def login_view(request):
    if request.method == "POST":
        categories = Category.objects.all()
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "categories":categories
            })
    else:
        categories = Category.objects.all()
        return render(request, "auctions/login.html", {
            "categories": categories
        })


def createListing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/createlisting.html", {
            "categories": categories
        })
    else:
        # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        user = request.user

        # Now you need the category object itself from the database
        category_obj = Category.objects.get(name=category)
        # Create new listing
        aListing = AuctionListing(
            header=title,
            description=description,
            image_url=image_url,
            category=category_obj,
            starting_price=float(price),
            seller=user
        )

        # This will save
        aListing.save()
        return HttpResponseRedirect(reverse(index))


def category_finder(request, category):
    categories = Category.objects.all()
    # Get actual object
    category_obj = Category.objects.get(name=category)
    # Filter only the needed ones
    listings = AuctionListing.objects.filter(category=category_obj)
    return render(request, "auctions/category.html", {
        "header_category": category,
        "categories": categories,
        "listings": listings
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    categories = Category.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "categories": categories
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categories": categories
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{
            "categories": categories
        })
