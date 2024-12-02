from django.shortcuts import render
from .models import Product
# Create your views here.


def home(request):
    products = Product.objects.all()
    context ={
        'products':products,
    }
    return render(request,'home.html',context)

def productDetailPage(request,unique_id):
    product = Product.objects.get(unique_id=unique_id)
    context ={
        'product': product,
    }
    return render(request,'productDetails.html',context)

def shop(request):
    products = Product.objects.all()
    context ={
        'products':products,
    }
    return render(request,'shop.html',context)