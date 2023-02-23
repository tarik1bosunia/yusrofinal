from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('checkout/', views.checkout, name='checkout'),
    path('get_cities_by_division/<int:division_id>/', views.get_cities_by_division, name='get_cities_by_division'),
    path('get_areas_by_city/<int:city_id>/', views.get_areas_by_city, name='get_areas_by_city'),
]
