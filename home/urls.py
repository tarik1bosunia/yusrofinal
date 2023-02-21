from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path("store/", include("store.urls")),
    path("cart/", include("cart.urls")),
    path("account/", include("account.urls")),
]
