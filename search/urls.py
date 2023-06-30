from django.urls import path
from search import views

urlpatterns = [
    path('', views.search_product, name="search_product"),

    path('autocomplete/', views.autocomplete, name='autocomplete'),
    # path('product-autocomplete/', views.ProductAutocomplete.as_view(), name='product-autocomplete'),
    # path('get-names/', views.get_names, name="get_names"),
    # path('search/', views.index, name="search"),

]
