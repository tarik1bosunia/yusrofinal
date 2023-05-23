from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.contrib import messages


from order.models import City, Area, Order
from order.forms import OrderForm

from cart.models import Cart, CartItem
from cart.views import _cart_id


def generate_order_number(order_id):
    now = datetime.now()
    order_number = now.strftime("%Y%m%d%H%M%S")
    return order_number + str(order_id)


def place_order_view(request, total=0, quantity=0, discount_for_promo=0):
    current_user = request.user

    # if cart count is less than or equal to zero than redirect to shop
    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)
        print("working: authenticated")
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except Exception as e:
            print("in exception")
            return redirect('store')

    cart_count = cart_items.count()
    print("cart count: ", cart_count)
    if cart_count <= 0:
        return redirect('store')

    for cart_item in cart_items:
        total = total + cart_item.product.selling_price * cart_item.quantity
        quantity = quantity + cart_item.quantity
    grand_total = total - discount_for_promo
    print("grant total: ", grand_total)

    if request.method == 'POST':
        print("post working: ")
        form = OrderForm(request.POST)
        if form.is_valid():
            print("form is working and here: ")
            # store all the billing information on the order table
            order = form.save(commit=False)
            order.order_total = grand_total
            order.discount = discount_for_promo
            order.ip = request.META.get('REMOTE_ADDR')

            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            messages.success(request, 'Your oder has been placed successfully')
            context = {
                "order": order,
                "total": total,
                "grand_total": grand_total,
                "quantity": quantity,
                "discount_for_promo": discount_for_promo,
                "cart_items": cart_items,
                "OrderForm": form,
            }
            return render(request, 'order/payments.html', context)
    else:
        form = OrderForm()
    context = {
        "total": total,
        "grand_total": grand_total,
        "quantity": quantity,
        "discount_for_promo": discount_for_promo,
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


def payments_view(request):
    current_user = request.user
    if current_user.is_authenticated:
        order = Order.objects.get(user=current_user, is_ordered=False)
    else:
        # here oder for unauthenticated user
        pass

    return render(request, 'order/payments.html')
