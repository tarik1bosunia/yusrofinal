from django.contrib import admin
from .models import Product, ProductGallery, Variation, ReviewRating
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'regular_price', 'selling_price', 'discount_percentage', 'discount_tc', 'stock', 'product_for', 'category', 'points', 'show_in_popular_products', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    # list_filter = ('sector',)
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)



# class ProductGalleryAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image')
#
#
# admin.site.register(ProductGallery, ProductGalleryAdmin)
