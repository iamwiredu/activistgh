from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from home.models import Product
# Create your views here.

# adminDb

# @login_required(login_url='/login')
def userAdmin(request):
    return render(request,'userAdmin.html')


# Management Db
def managementDb(request):
    return render(request,'managementDb.html')


def distribuition(request):
    return render(request,'distribuition.html')

def productManagement(request):
    productFormCreator = ProductForm()
    products = Product.objects.all()

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
        'products':products,
    }

    return render(request,'productsManagement.html',context)