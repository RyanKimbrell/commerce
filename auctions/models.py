from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    ART = 'ART'
    ANTIQUES = 'ANT'
    COLLECTIBELS = 'COL'
    FASHION = 'FAS'
    GAMES = 'GAM'
    MISCELANEOUS = 'MIS'
    MOVIES = 'MOV'
    MUSIC_EQUIPMENT = 'MUS'
    SPORTING_GOODS = 'SPO'
    TOYS = 'TOY'

    CATEGORIES_CHOICES = [
        (ART, "Art"),
        (ANTIQUES, "Antiques"),
        (COLLECTIBELS, "Collectibles"),
        (FASHION, "Fashion"),
        (GAMES, "Games"),
        (MISCELANEOUS, "Miscelaneous"),
        (MOVIES, "Movies"),
        (MUSIC_EQUIPMENT, "Music Gear & Equipment"),
        (SPORTING_GOODS, "Sporting Goods"),
        (TOYS, "Toys")
    ]

    category = models.CharField(
        max_length=3,
        choices=CATEGORIES_CHOICES,
        default=MISCELANEOUS
        )


    def __str__(self):
        return f"Category: {self.category}"

class Listing(models.Model):
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="listings_in_category")
    title = models.CharField(max_length=64, null=True)
    description = models.TextField(null=True)
    current_bid = models.IntegerField(default=0)
    image_url = models.CharField(max_length=256, null=True)
    related_watchlists = models.ManyToManyField('Watchlist', blank=True, related_name="listings")
    auction_open = models.BooleanField(default=True)


    def __str__(self):
        return f"Listing #{self.id}: {self.title}, Category: {self.category}, Description: {self.description}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=1, related_name="bid_listing")
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    bid = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.bid_user}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="comments_in_listing")
    comment_text = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="user_comments")

    def __str__(self):
        return f"{self.user}: {self.comment_text}"


class Watchlist(models.Model):
    related_listings = models.ManyToManyField(Listing, blank=True, related_name="watchlists")
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1, related_name="user_watchlist")
    def __str__(self):
        return f"{self.related_listings}"
