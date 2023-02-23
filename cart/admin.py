from django.contrib import admin
from .models import Cart, CartItem, Division, City, Area, Order


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Order)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
