from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.get_categories, name="categories"),
    path("watchlist", views.get_watchlist, name="watchlist"),
    path("categories/<int:category_id>", views.get_category, name="category"),
    path("listings/<int:listing_id>", views.get_listing, name="listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
