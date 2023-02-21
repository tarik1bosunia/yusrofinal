from django.db import models


class HomeSlider(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=False)


class HomeSliderImage(models.Model):
    slider = models.ForeignKey(HomeSlider, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/home_slider', max_length=255)

    def __str__(self):
        return f'{self.id} ... slider: {self.slider.title}'
