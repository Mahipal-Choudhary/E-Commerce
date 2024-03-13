from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

def listing(request,id):
    listingData = Listing.objects.get(pk=id)
    #**IMPORTANT**
    isListinginWatchlist = request.user in listingData.watchlist.all()
    #**LEARNING** how to go into that message in Commentclass
    allcomments = Comment.objects.filter(listing = listingData)
    isOwner = listingData.owner.username == request.user.username
    return render(request, "auctions/listing.html",{
        "listing" : listingData,
        "isListinginWatchlist" : isListinginWatchlist,
        "allcomments" : allcomments,
        "isOwner" : isOwner,
    })

def CloseAuction(request,id):
    listingData = Listing.objects.get(pk = id)
    listingData.isActive = False
    listingData.save()
    return HttpResponseRedirect(reverse("index"))

#initial price will be first bid In Bid table then next highest bid will be added to the Bid table
def addBid(request,id):
    newBid = int(request.POST["newBid"])
    listingData = Listing.objects.get(pk=id)
    isListinginWatchlist = request.user in listingData.watchlist.all()
    allcomments = Comment.objects.filter(listing = listingData)
    isOwner = listingData.owner.username == request.user.username

    if newBid > listingData.price.bid:
        updateBid = Bid(bid = newBid, user = request.user)
        updateBid.save()
        #update the initial bid to highest bid
        #when the listing.html render using this function then comments will not be seen if we dont put all the comment with is function 
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing" : listingData,
            "message" : "Bid was updated successfully",
            "update" : True,
            "isListinginWatchlist" : isListinginWatchlist,
            "allcomments" : allcomments,
            "isOwner" : isOwner,
             })
    else:
        return render(request, "auctions/listing.html",{
            "listing" : listingData,
            "message" : "Bid updated Failed",
            "update" : False,
            "isListinginWatchlist" : isListinginWatchlist,
            "allcomments" : allcomments,
            "isOwner" : isOwner,

             })



def addcomment(request,id):
    listing = Listing.objects.get(pk = id)
    author = request.user
    comment = request.POST["newComment"]
    newcomment= Comment(
        author = author,
        listing = listing,
        message = comment
    )
    newcomment.save()
    #ADD more REDIRECT so that the function which render page will have all the variable to render the page and helps to not add same variable to all functions
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def watchlist(request):
    currentuser = request.user
    watchlist = currentuser.UserWatchlist.all()
    return render(request,"auctions/watchlist.html",{
        "watchlist": watchlist,
    })

def AddtoWatchlist(request,id):
    listingData = Listing.objects.get(pk = id)
    currentuser = request.user
    listingData.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def RemovefromWatchlist(request,id):
    listingData = Listing.objects.get(pk = id)
    currentuser = request.user
    # **MANY TO MANY RELATIONSHIP**
    listingData.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def index(request):
    allcategories = Category.objects.all()
    activelisting = Listing.objects.filter(isActive = True)
    return render(request, "auctions/index.html",{
        "listings" : activelisting,
        "categories" : allcategories,
        "heading": "Active Listing",
    })

def closedlisting(request):
    allcategories = Category.objects.all()
    activelisting = Listing.objects.filter(isActive = False)
    return render(request, "auctions/index.html",{
        "listings" : activelisting,
        "categories" : allcategories,
        "heading": "Closed Listing",
    })

def displaycategory(request):
    if request.method == "POST":
        CategoryfromForm = request.POST["category"]
        category = Category.objects.get(categoryName = CategoryfromForm)
        allcategories = Category.objects.all()
        activelisting = Listing.objects.filter(isActive = True, category = category)
        return render(request, "auctions/index.html",{
            "listings" : activelisting,
            "categories" : allcategories,
        })


def createListing(request):
    categories = Category.objects.all()
    if request.method == "GET":
        return render(request, "auctions/create.html",{
            "categories" : categories,
        })
    else:
        #get the data from form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        #who is the user
        currentuser = request.user
        #create objects of Bid
        bid = Bid(bid = float(price), user = currentuser )
        bid.save()

        #Get all the content about the particular category
        categorydata = Category.objects.get(categoryName = category)
        #Create a new listing object
        newlisting = Listing(
            title = title,
            description = description,
            imageUrl = imageurl,
            price = bid,
            owner = currentuser,
            category = categorydata
        )
        #Insert the object in our database
        newlisting.save()
        #Redirect to index page
        return HttpResponseRedirect(reverse("index"))


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
