from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, AuctionListing, Bid, Comment

from .models import User


def index(request):
    listings = AuctionListing.objects.all()
    # for the navbar
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "categories": categories,
        "listings": listings
    })


def watchlist(request):
    listings = request.user.userswatchlist.all()
    # for the navbar
    categories = Category.objects.all()
    return render(request, "auctions/watchlist.html", {
        "categories": categories,
        "listings": listings
    })


def individual_listing(request, id):
    listing = AuctionListing.objects.get(id=id)
    # get the comments
    comments = Comment.objects.filter(item= listing)
    if request.method == "POST":
        action = request.POST['action']
        if action == "add":
            listing.watchlist.add(request.user)
        elif action == "remove":
            listing.watchlist.remove(request.user)

    # To check if user who pressed this is in Auctionlisting watchlist
    inwatchlist = request.user in listing.watchlist.all()
    # for the navbar
    categories = Category.objects.all()
    return render(request, "auctions/listing.html", {
        "categories": categories,
        "listing": listing,
        "inwatchlist": inwatchlist,
        "comments": comments
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
        # Make a bid object
        bid_obj = Bid(value=float(price), bidder=user)
        bid_obj.save()

        # Now you need the category object itself from the database
        category_obj = Category.objects.get(name=category)
        # Create new listing
        aListing = AuctionListing(
            header=title,
            description=description,
            image_url=image_url,
            # saving category object since it is a foreign key
            category=category_obj,
            # saving bid object since it is a foreign key
            starting_price=bid_obj,
            seller=user
        )

        # This will save
        aListing.save()
        return HttpResponseRedirect(reverse(index))


def category_finder(request, category):
    # Capitalize the first letter since all categories are capitalized and it would be stupid to
    # distinguish between "action" and "Action"
    category = category.capitalize()
    # This is needed for the categories dropdown in the navbar
    categories = Category.objects.all()
    # Get actual object
    try:
        category_obj = Category.objects.get(name=category)
    except:
        category_obj = Category.objects.get(name="Other")
        category = "Other"
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


def add_comment(request, id):
    item = AuctionListing.objects.get(id=id)
    statement = request.POST["comment"]
    comment_obj = Comment(item=item, statement=statement, author=request.user)
    comment_obj.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))




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
