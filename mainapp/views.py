from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string

# scrapers
from .scrapers import scrape_amazon

# Create your views here.
def home(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        print(product_name)
        results = scrape_amazon(product_name)[0]
        results_data = [
            {
                'name': results["title"],
                'price': results["rating"],
                'ratings': results["rating"],
                'image_url': results["image_link"]
                # 'image_url': product.image_url
            }
        ]
        print(results_data)

        return JsonResponse({'results': results_data})
    else:
        return render(request, "mainapp/home.html")