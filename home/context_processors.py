from home.models import HomeSlider, HomeSliderImage


def homeSlider(request):
    home_slider = HomeSlider.objects.filter(isActive=True).first()
    home_slider_images = HomeSliderImage.objects.filter(slider_id=home_slider.id)
    # print("home_slider_images: ", home_slider_images)
    return dict(home_slider_images=home_slider_images)
