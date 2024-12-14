from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, RelatedImagesForm
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

def productEdit(request,unique_id):
    product = Product.objects.get(unique_id=unique_id)
    productFormCreator = ProductForm(instance=product)
    relatedImage = product.relatedImages.all()[0]
    

    if request.method == 'POST':
        if 'editProduct' in request.POST:
            productFormCreator = ProductForm(request.POST, request.FILES,instance=product)    
            if productFormCreator.is_valid(): 
                productFormCreator.save() 
                return redirect(productEdit,unique_id)  # Redirect to the same page or a success page
            else:
                print('error')
        if 'updateBackImage' in request.POST:
            backImage = request.FILES.get('backImage')
            try:
                if backImage:
                    relatedImage.image = backImage
                    relatedImage.save()
            except:
                print('error')



    context ={
        'product':product,
        'productFormCreator':productFormCreator,
    }
    return render(request,'productEdit.html',context)

def ordersList(request):
    return render(request,'ordersList.html')