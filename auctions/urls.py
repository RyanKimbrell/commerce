from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categoriesindex", views.categoriesindex, name="categoriesindex"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("createnewlisting", views.create_new_listing, name="createnewlisting"),
    path("newbid/<int:listing_id>", views.new_bid, name="newbid"),
    path("category/<int:category_id>", views.categorylist, name="categorylist"),
    path("newcomment/<int:listing_id>", views.new_comment, name="newcomment"),
    path("addtowatchlist/<int:listing_id>", views.addtowatchlist, name="addtowatchlist"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("removefromwatchlist/<int:listing_id>", views.removefromwatchlist, name="removefromwatchlist")
]
