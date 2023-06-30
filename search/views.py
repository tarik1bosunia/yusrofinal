from django.shortcuts import render
from store.models import Product
from django.db.models import Q
from search.models import Name
# from dal import autocomplete

from django.http import JsonResponse, HttpResponse


def search_product(request):
    products = None
    products_count = 0
    search_query = None

    if 'searchInput' in request.GET:

        search_query = request.GET.get('searchInput')

        if 0 < len(search_query) < 80:
            print(search_query)
            products = Product.objects.filter(
                Q(product_name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__category_name__icontains=search_query) |
                Q(category__slug__contains=search_query) |
                Q(category__description__icontains=search_query) |
                Q(slug__icontains=search_query) |
                Q(slug__icontains=search_query)
            )

    products_count = len(products)
    context = {
        "products": products,
        "products_count": products_count,
        "search_query": search_query
    }

    return render(request, "store/store.html", context)



"""
@ return search keys for autocomplete search feature
"""


# class ProductAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = Product.objects.all()
#
#         if self.q:
#             qs = qs.filter(name__icontains=self.q)
#
#         return qs


def get_search_keys(request):
    current_user = request.user
    search = request.GET.get('search')
    payload = []
    if search:
        if current_user.is_authenticated:
            # search keywords for authenticated user
            pass
        else:
            # search keywords for unauthenticated user
            pass

# def identify_os(request):
#     user_agent = request.META.get('HTTP_USER_AGENT', '')
#     os = 'Unknown'
#
#     if 'Windows' in user_agent:
#         os = 'Windows'
#     elif 'Mac' in user_agent:
#         os = 'Mac OS'
#     elif 'Linux' in user_agent:
#         os = 'Linux'
#     elif 'Android' in user_agent:
#         os = 'Android'
#     elif 'iOS' in user_agent:
#         os = 'iOS'
#
#     return render(request, 'identify_os.html', {'os': os})

# def identify_device(request):
#     user_agent = request.META.get('HTTP_USER_AGENT', '')
#     device = 'Unknown'
#
#     if 'iPhone' in user_agent:
#         device = 'iPhone'
#     elif 'iPad' in user_agent:
#         device = 'iPad'
#     elif 'Android' in user_agent:
#         device = 'Android'
#     elif 'Windows Phone' in user_agent:
#         device = 'Windows Phone'
#     elif 'BlackBerry' in user_agent:
#         device = 'BlackBerry'
#
#     return render(request, 'identify_device.html', {'device': device})
# def search_history(request):
#     session_key = request.session.session_key
#     search_history = SearchHistory.objects.filter(Q(user=request.user) | Q(session_key=session_key)).order_by('-timestamp')
#     return render(request, 'search_history.html', {'search_history': search_history})
# def search(request):
#     if request.method == 'POST':
#         keyword = request.POST.get('keyword', '').strip()
#         if keyword:
#             search_history = SearchHistory(keyword=keyword)
#             if request.user.is_authenticated:
#                 search_history.user = request.user
#             else:
#                 search_history.session_key = request.session.session_key
#             search_history.save()
#
#     return render(request, 'search.html')
# def index(request):
#     return render(request, 'search/search.html')


# def get_names(request):
#     keyword = request.GET.get('keyword')
#     payload = []
#     if keyword:
#         names = Name.objects.filter(name__icontains=keyword)
#
#         for name in names:
#             payload.append({
#                 'name': name.name
#             })
#
#     return JsonResponse({
#         "status": True,
#         "payload": payload
#     })


def autocomplete(request):
    query = request.GET.get('term', '')
    products = Product.objects.filter(name__icontains=query)[:10]
    results = []
    for product in products:
        results.append(product.product_name)
    return JsonResponse(results, safe=False)





# def search_product(request):
#     #     products = None
#     #     products_count = 0
#     if 'keyword' in request.GET:
#         search_query = request.GET.get('keyword')
#         products = Product.objects.filter(Q(product_name__icontains=search_query) | Q(description__icontains=search_query)| Q(category__category_name__icontains=search_query), Q(category__slug__contains=search_query) | Q(category__description__icontains=search_query) | Q(slug__contains=search_query) | Q(slug__contains=search_query))
#         # Convert the search results to a list of dictionaries
#         products_list = []
#         for product in products:
#             products_list.append({
#                 'product_name': product.product_name,
#                 'image_url': product.images.url
#             })
#         # Return the search results as a JSON response
#         return JsonResponse(products_list, safe=False)
#     else:
#         return JsonResponse([], safe=False)


# def search_product(request):
#     products = None
#     products_count = 0
#     if 'keyword' in request.GET:
#         search_query = request.GET.get('keyword')
#         if 0 < len(search_query) < 80:
#             products = Product.objects.filter(Q(product_name__icontains=search_query) | Q(description__icontains=search_query)| Q(category__category_name__icontains=search_query), Q(category__slug__contains=search_query) | Q(category__description__icontains=search_query) | Q(slug__contains=search_query) | Q(slug__contains=search_query))
#             products_count = products.count()
#             # all_products_title = Product.objects.filter(product_name=search_query)
#             # all_products_description = Product.objects.filter(description__icontains=search_query)
#             # all_products_category_title = Product.objects.filter(category__category_name__icontains=search_query)
#             # all_products_category_slug = Product.objects.filter(category__slug__contains=search_query)
#             # all_products_category_description = Product.objects.filter(category__description__icontains=search_query)
#             # all_products_slug = Product.objects.filter(slug__contains=search_query)
#             # products = all_products_title.union(all_products_description, all_products_category_title, all_products_category_slug, all_products_category_description, all_products_slug).order_by('-created_date')
#
#     context = {
#         "products": products,
#         "products_count": products_count,
#     }
#     print("products: ", products)
#     return render(request, "store/store.html", context)
