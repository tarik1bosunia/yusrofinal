from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template.loader import get_template


from store.models import Product, ProductGallery, ReviewRating
from store.forms import ReviewForm
from category.models import Category
from cart.models import Cart, CartItem
from cart.views import _cart_id
from order.models import OrderProduct


def store(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    paginate_by = 2

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True).order_by('-id')
        products_count = products.count()

        # pagination
        paginator = Paginator(products, paginate_by)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        products_count = products.count()

        # pagination
        paginator = Paginator(products, paginate_by)
        page_number = request.GET.get('page')
        paged_products = paginator.get_page(page_number)
        # page = paginator.get_page(page_number)
        # products_template = get_template('includes/product/product_list_store.html')
        # html = products_template.render({'page': page})
        # response_data = {
        #     'products_html': html,
        #     'has_next_page': page.has_next()
        # }
        # return JsonResponse(response_data)

    context = {
        'categories': categories,
        'category': category,
        "products": paged_products,
        "products_count": products_count,
    }
    # # Check if request is AJAX and return JSON response for infinite scroll
    # if request.is_ajax():
    #     next_page_number = paged_products.next_page_number() if paged_products.has_next() else None
    #     has_next_page = paged_products.has_next()
    #     data = {
    #         'next_page_number': next_page_number,
    #         'has_next_page': has_next_page,
    #         'products_html': render(request, 'store/products.html', context).content.decode('utf-8'),
    #     }
    #     return JsonResponse(data)
    return render(request, "store/store.html", context)


def product_details(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        isProductInCart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        product_gallery = ProductGallery.objects.filter(product_id=product.id)

    except Exception as e:
        raise e

    is_already_ordered_product = None
    if request.user.is_authenticated:
        order_product = OrderProduct.objects.filter(user=request.user, product=product, is_ordered=True).first()
        if order_product:
            is_already_ordered_product = True
    #  Get the reviews
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        "product": product,
        "isProductInCart": isProductInCart,
        "product_gallery": product_gallery,
        "is_already_ordered_product": is_already_ordered_product,
        "reviews": reviews,
    }
    return render(request, "store/product_details.html", context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    print("url = ", url)
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            review_form = ReviewForm(request.POST, instance=review)
            review_form.save()
            messages.success(request, "Thank you! Your review has been updated.")

        except ReviewRating.DoesNotExist:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review_rating = ReviewRating()
                review_rating.subject = review_form.cleaned_data['subject']
                review_rating.rating = review_form.cleaned_data['rating']
                review_rating.review = review_form.cleaned_data['review']
                review_rating.ip = request.META.get('REMOTE_ADDR')
                review_rating.product_id = product_id
                review_rating.user_id = request.user.id
                review_rating.save()
                messages.success(request, "Thank you! Your review has been submitted successfully.")

    return redirect(url)
