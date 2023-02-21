from django.urls import path, include
from store import views

urlpatterns = [
    path('', views.store, name="store"),
    path('category/<slug:category_slug>/', views.store, name="products_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name="product_details"),
    path('search/', views.search, name="search"),
    # path('caheckout/', views.checkout, discount_persentage="checkout"),

]
