from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )

        return redirect('cart')
    # if the user is not authenticated
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )

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

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity = cart_item.quantity -1
        cart_item.save()
    else:
        pass
        # cart_item.delete()

    return redirect('cart')

    # try:
    #     if request.user.is_authenticated:
    #         cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    #     else:
    #         cart = Cart.objects.get(cart_id=_cart_id(request))
    #         cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    #     if cart_item.quantity > 1:
    #         cart_item.quantity -= 1
    #         cart_item.save()
    #     else:
    #         cart_item.delete()
    # except:
    #     pass
    # return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

    # if request.user.is_authenticated:
    #     cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    # else:
    #     cart = Cart.objects.get(cart_id=_cart_id(request))
    #     cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    # cart_item.delete()
    # return redirect('cart')


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



