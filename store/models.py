from django.db import models
from category.models import Category
from django.urls import reverse
from account.models import CustomUser
from django.db.models import Avg, Count

# Create your models here.
# sector_choices = (
#     ('men', 'men'),
#     ('ladies', 'ladies'),
#     ('child', 'child'),
#     ('others', 'others')
# )
# sector_choices = (
#     ('color', 'color'),
#     ('size', 'size'),
# )


product_for_choice = (
    ('mens', 'mens'),
    ('ladies', 'ladies'),
    ('child', 'child'),
    ('others', 'others'),
)


class AvailableProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stock__gt=0)


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    regular_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)
    discount_tc = models.BooleanField(default=False)
    images = models.ImageField(upload_to='photos/products', default="")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    product_for = models.CharField(max_length=100, choices=product_for_choice)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    show_in_popular_products = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # The default manager
    available_products = AvailableProductManager()  # The custom manager

    class Meta:
        ordering = ('-created_date',)

    @property
    def discount_percentage(self):
        try:
            return int((self.regular_price - self.selling_price) * 100 / self.regular_price)
        except ZeroDivisionError:
            return 0

    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    variation_category_choice = (
        ('color', 'color'),
        ('size', 'size'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products/gallery', max_length=255)

    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product galleries'

    def __str__(self):
        return f'{self.product.product_name} ... category: {self.product.category.category_name}'
