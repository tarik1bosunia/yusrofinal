from django.contrib import admin
from .models import Division, City, Area, Order, OrderProduct


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Division, DivisionAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
