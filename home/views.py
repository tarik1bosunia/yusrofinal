from django.shortcuts import render
from home.models import HomeSlider, HomeSliderImage
from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True, show_in_popular_products=True)

    context = {
        "products": products,
    }
    # print('home_slider_images: ', home_slider_images)
    return render(request, "index.html", context)
