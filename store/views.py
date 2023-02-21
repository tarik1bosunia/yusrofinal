from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from store.models import Product, ProductGallery
from category.models import Category
from cart.models import Cart, CartItem
from cart.views import _cart_id


def store(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by('-id')
        products_count = products.count()

        # pagination
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        products_count = products.count()

        # pagination
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    context = {
        'categories': categories,
        'category': category,
        "products": paged_products,
        "products_count": products_count,
    }
    return render(request, "store/store.html", context)


def product_details(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        isProductInCart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        product_gallery = ProductGallery.objects.filter(product_id=product.id)
    except Exception as e:
        raise e
    context = {
        "product": product,
        "isProductInCart": isProductInCart,
        "product_gallery": product_gallery,
    }
    return render(request, "store/product_details.html", context)


def search(request):
    products = None
    products_count = 0
    if 'keyword' in request.GET:
        search_query = request.GET.get('keyword')
        if 0 < len(search_query) < 80:
            products = Product.objects.filter(Q(product_name=search_query) | Q(description__icontains=search_query)| Q(category__category_name__icontains=search_query), Q(category__slug__contains=search_query) | Q(category__description__icontains=search_query) | Q(slug__contains=search_query) | Q(slug__contains=search_query))
            products_count = products.count()
            # all_products_title = Product.objects.filter(product_name=search_query)
            # all_products_description = Product.objects.filter(description__icontains=search_query)
            # all_products_category_title = Product.objects.filter(category__category_name__icontains=search_query)
            # all_products_category_slug = Product.objects.filter(category__slug__contains=search_query)
            # all_products_category_description = Product.objects.filter(category__description__icontains=search_query)
            # all_products_slug = Product.objects.filter(slug__contains=search_query)
            # products = all_products_title.union(all_products_description, all_products_category_title, all_products_category_slug, all_products_category_description, all_products_slug).order_by('-created_date')

    context = {
        "products": products,
        "products_count": products_count,
    }
    return render(request, "store/store.html", context)

