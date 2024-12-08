from django.shortcuts import render, redirect
from .models import Product, Outing
from .forms import ProductForm
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
    events = Outing.objects.all()
    context ={
        'products':products,
        'events': events,
    }
    return render(request,'shop.html',context)


# Management Db
def managementDb(request):
    return render(request,'managementDb.html')


def productManagement(request):
    productFormCreator = ProductForm()

    if request.method == 'POST':
        if 'addProduct' in request.POST:
            productFormCreator = ProductForm(request.POST, request.FILES)    
            if productFormCreator.is_valid(): 
                productFormCreator.save() 
                return redirect(productManagement)  # Redirect to the same page or a success page
            else:
                print('error')

    context = {
        'productFormCreator':productFormCreator,
    }

    return render(request,'productManagement.html',context)