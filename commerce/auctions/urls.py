from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.createListing, name="create"),
    path("category/<str:category>", views.category_finder, name="category"),
    path("listing/<int:id>", views.individual_listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist")
]
