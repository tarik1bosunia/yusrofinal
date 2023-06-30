from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from store.models import Product, Variation
from .models import Cart, CartItem
from order.models import City, Area
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from cart.forms import OrderForm

# Create your views here.
from django.http import HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # get the product
    current_user = request.user

    product_variation = []

    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST.get(key)
            try:
                variation = Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except ObjectDoesNotExist:
                pass

    print(product_variation)

    # if the user is authenticated
    if current_user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            if len(product_variation) > 0:
                for item in product_variation:
                    cart_item.variations.add(item)

            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )
            cart_item.variations.clear()
            if len(product_variation) > 0:
                for item in product_variation:
                    cart_item.variations.add(item)
            cart_item.save()
        return redirect('cart')

    # if the user is not authenticated
    else:
        # cart
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        # cart item
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        if cart_items.exists():
            # existing variations => database
            # current variation => product_variation
            # item id => database
            existing_variation_list = []
            cart_item_id_list = []
            for cart_item in cart_items:
                existing_variation = cart_item.variations.all()
                existing_variation_list.append(list(existing_variation))
                cart_item_id_list.append(cart_item.id)

            print("ex variations list: ", existing_variation_list)
            print("pro variations: ", product_variation)

            target = set(product_variation)
            index = -1

            for i, sublist in enumerate(existing_variation_list):
                if set(sublist) == target:
                    index = i
                    break
            if index != -1:
                # increase the cart_item quantity
                print("index:", index)
                cart_item = CartItem.objects.get(product=product, id=cart_item_id_list[index])
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
            else:
                # create a new cart item
                cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

                if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                    cart_item.save()

        else:
            print("cart items:", "empty cart_items")
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )

            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
                cart_item.save()
        return redirect('cart')


# def add_cart(request, product_id):
#     current_user = request.user
#     product = Product.objects.get(id=product_id)  # get the product
#     # If the user is authenticated
#     if current_user.is_authenticated:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
#
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key,
#                                                       variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except:
#                     pass
#
#         is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
#         if is_cart_item_exists:
#             cart_item = CartItem.objects.filter(product=product, user=current_user)
#             ex_var_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)
#
#             if product_variation in ex_var_list:
#                 # increase the cart item quantity
#                 index = ex_var_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, user=current_user)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 user=current_user,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')
#     # If the user is not authenticated
#     else:
#         product_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]
#
#                 try:
#                     variation = Variation.objects.get(product=product, variation_category__iexact=key,
#                                                       variation_value__iexact=value)
#                     product_variation.append(variation)
#                 except:
#                     pass
#
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id=_cart_id(request)
#             )
#         cart.save()
#
#         # is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
#         cart_item = CartItem.objects.filter(product=product, cart=cart)
#         if cart_item.exists():
#             # cart_item = CartItem.objects.filter(product=product, cart=cart)
#             # existing_variations -> database
#             # current variation -> product_variation
#             # item_id -> database
#             ex_var_list = []
#             id = []
#             for item in cart_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)
#
#             print(ex_var_list)
#
#             if product_variation in ex_var_list:
#                 # increase the cart item quantity
#                 index = ex_var_list.index(product_variation)
#                 item_id = id[index]
#                 item = CartItem.objects.get(product=product, id=item_id)
#                 item.quantity += 1
#                 item.save()
#
#             else:
#                 item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#                 if len(product_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*product_variation)
#                 item.save()
#         else:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart,
#             )
#             if len(product_variation) > 0:
#                 cart_item.variations.clear()
#                 cart_item.variations.add(*product_variation)
#             cart_item.save()
#         return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity = cart_item.quantity - 1
            cart_item.save()
        else:
            pass
            # cart_item.delete()
    except ObjectDoesNotExist:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart_view(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total = total + cart_item.product.selling_price * cart_item.quantity
            quantity = quantity + cart_item.quantity

    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items
    }
    return render(request, 'store/cart.html', context)


# def cart(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total) / 100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass  # just ignore
#
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/cart.html', context)


# @login_required(login_url='login')
# def checkout(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         tax = (2 * total) / 100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass  # just ignore
#
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax': tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/checkout.html', context)

# @login_required(login_url='user_login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total = total + cart_item.product.selling_price * cart_item.quantity
            quantity = quantity + cart_item.quantity

    except ObjectDoesNotExist:
        pass  # just ignore
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            # ...
    else:
        form = OrderForm()
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "OrderForm": form,
    }

    return render(request, 'store/checkout.html', context)


def get_cities_by_division(request, division_id):
    if not division_id:
        return JsonResponse({'error': 'Division ID is required.'}, status=400)

    cities = City.objects.filter(division_id=division_id)
    city_list = [{'id': city.id, 'name': city.name} for city in cities]
    return JsonResponse(city_list, safe=False)


def get_areas_by_city(request, city_id):
    if not city_id:
        return JsonResponse({'error': 'City ID is required.'}, status=400)

    areas = Area.objects.filter(city_id=city_id)
    area_list = [{'id': area.id, 'name': area.name} for area in areas]
    return JsonResponse(area_list, safe=False)


@require_POST
def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')

    # Check the coupon code against your backend logic
    if coupon_code == 'SOME_COUPON_CODE':
        # Generate the HTML content based on the coupon code
        additional_html = "<div>Coupon applied successfully!</div>"
    else:
        additional_html = "<div>Invalid coupon code.</div>"

    # Return the additional HTML content as a JSON response
    data = {
        'additional_html': additional_html,
    }

    return JsonResponse(data)
