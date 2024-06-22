from django.shortcuts import render, HttpResponse
from .scrapers import scrape_amazon

# Create your views here.
def home(request):
    if request.method == "POST":
        product_name = "I phone 15"
        print(scrape_amazon(product_name))
        return HttpResponse("Hi")
    else:
        return render(request, "mainapp/home.html")