from django.contrib import admin
from .models import User, Category, Listing, Comment, Bid

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listed_by", "category", "title", "description", "current_bid")


class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_user", "bid")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "comment_text")


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)