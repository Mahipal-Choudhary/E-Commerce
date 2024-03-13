from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createListing,name="createlisting"),
    path("displaycategory", views.displaycategory, name = "displaycategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addtoWatchlist/<int:id>", views.AddtoWatchlist, name="addtoWatchlist"),
    path("removefromWatchlist/<int:id>", views.RemovefromWatchlist, name="removefromWatchlist"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("addcomment/<int:id>", views.addcomment, name = "addcomment"),
    path("addBid/<int:id>", views.addBid, name = "addBid"),
    path("CloseAuction/<int:id>",views.CloseAuction,name="CloseAuction"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
]
