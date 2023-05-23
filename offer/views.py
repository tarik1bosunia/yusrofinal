from django.shortcuts import render


def offers_view(request):
    return render(request, 'offer/offers.html')
