from django.urls import path
from . import mac_address


urlpatterns = [
    # path('', views.cart_view, name='cart'),
    # path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    # path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    # path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('mac_address/', mac_address.get_mac_address, name='get_mac_address'),

]
