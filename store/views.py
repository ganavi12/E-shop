from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Category

# Create your views here.
def index(request):
    products = Product.objects.all()
    category_list = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products =  Product.objects.filter(category=category_id)
    return render(request, 'store/index.html', {"products": products, "category_list": category_list})