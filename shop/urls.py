from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    # path("", views.home, name="Home"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("login/", views.Login, name="Login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="SignIn"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("transactions/", views.transaction_details, name="transaction_details"),
    path("receipt/<int:id>/", views.receipt, name="receipt"),
    #path("handlerequest/", views.handlerequest, name="HandleRequest"),

]
urlpatterns += staticfiles_urlpatterns()
