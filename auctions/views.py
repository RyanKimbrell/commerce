from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

@login_required
def new_listing(request):
    return render(request, "auctions/newlisting.html",{
        "categories": Category.objects.all()
    })


@login_required
def create_new_listing(request):
    if request.method == "POST":
        listing_title = request.POST.get('listingtitle')
        listing_description = request.POST.get('listingdescription')
        starting_bid = request.POST.get('starting_bid')
        listing_image_url = request.POST.get('image_url')
        category_string = request.POST.get('listingcategories')
        listing_category = Category.objects.get(category=category_string[10:])
        listing_current_bid = Bid(bid_user=request.user, bid=starting_bid)
        listing_current_bid.save()
        listing = Listing(listed_by=request.user, title=listing_title, category=listing_category, description=listing_description, current_bid=starting_bid, image_url=listing_image_url)
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))


@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.auction_open = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))



@login_required
def new_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid_user = request.user
    new_bid = request.POST.get('new_bid')
    listing.current_bid = new_bid
    bid_object = Bid(listing=listing, bid_user=bid_user, bid=new_bid)
    listing.save()
    bid_object.save()

    return HttpResponseRedirect(reverse("listing", args=[listing.id]))


@login_required
def watchlist(request):
    user = request.user
    try:
        watchlist = user.user_watchlist
        related_listings = watchlist.related_listings.all()
    except:
        Watchlist.objects.create(user=user)
        watchlist = user.user_watchlist
        related_listings = watchlist.related_listings.all()
    return render(request, "auctions/watchlist.html",{
        "listings": related_listings
    })
    

@login_required
def addtowatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    try:
        user_watchlist = user.user_watchlist
        user_watchlist.related_listings.add(listing)
        user_watchlist.save()
    except:
        Watchlist.objects.create(user=user)
        user_watchlist = user.user_watchlist
        user_watchlist.related_listings.add(listing)
        user_watchlist.save()
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))


@login_required
def removefromwatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    user_watchlist = user.user_watchlist
    user_watchlist.related_listings.remove(listing)
    user_watchlist.save()
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))


def categoriesindex(request):
    return render(request, "auctions/categoriesindex.html",{
        "categories": Category.objects.all()
    })

def categorylist(request, category_id):
    selected_category = Category.objects.get(pk=category_id)
    listings = selected_category.listings_in_category.all()
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": selected_category
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments_in_listing.all()
    highest_bid_object = str(listing.bid_listing.filter(bid=listing.current_bid))
    winner_unformatted = highest_bid_object[17:]
    winner_close = winner_unformatted.replace(">", "")
    winner = winner_close.replace("]", "")
    user = request.user
    if user is not None:
        try:
            watchlist = user.user_watchlist
            related_listings = watchlist.related_listings.all()
        except:
            Watchlist.objects.create(user=user)
            watchlist = user.user_watchlist
            related_listings = watchlist.related_listings.all()
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "comments": comments,
        "winner": winner,
        "watchlist": related_listings
    })

@login_required
def new_comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comment_text = request.POST.get("new_comment")
    user = request.user
    comment = Comment(listing=listing, comment_text=comment_text, user=user)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))


def login_view(request):
    if request.method == "POST":

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
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
