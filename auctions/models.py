from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name="userbid")

    def __str__(self):
        return f"{self.bid}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=2000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank = True, null=True, related_name="bidprice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null = True,related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null = True, related_name="UserWatchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name="usercomment")
    listing =  models.ForeignKey(Listing, on_delete=models.CASCADE, blank = True, null=True, related_name="listingcomment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"
