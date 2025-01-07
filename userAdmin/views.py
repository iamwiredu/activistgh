import ast
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, RelatedImagesForm, ProductStockForm,CategoryForm, Size39to46Form,MediumLargeStockForm,DeliveryPriceByRegionForm
from .models import Revenue, Notification, DeliveryPriceByRegion
from home.models import Product, Contact,Newsletter, Payment, NewsletterBatch, RelatedImages,Category
from datetime import datetime
from home.models import MediumLargeStock, Size39to46

#import for emails

from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives, send_mass_mail
from django.template.loader import render_to_string

# import view
from django.db.models import F
from django.views import View



# @login_required(login_url='/login')
def userAdmin(request):
    return render(request,"userAdmin.html")


# Management Db
def managementDb(request):
    sales = len(Payment.objects.all().filter(verified=True))
    payments = Payment.objects.all().filter(verified=True)
    notifications = Notification.objects.all().filter(viewed=False)
  
    delivery = DeliveryPriceByRegion.objects.get(name='standard')
    DeliveryPriceByRegionFormCreator = DeliveryPriceByRegionForm(instance=delivery)
    # get current revenue
    currentYear = datetime.now().year
    revenue = Revenue.objects.get_or_create(year=currentYear)

    revenue_amount = 0 

    if request.method == 'POST':
        form = DeliveryPriceByRegionForm(request.POST,instance=delivery)
        if form.is_valid():
            form.save()
            return redirect(managementDb)  # Redirect to a success page
        else:
            form = DeliveryPriceByRegionForm()
            return redirect(managementDb)

    for sale in Payment.objects.all():
        revenue_amount += sale.amount
    
    subscribers = len(Newsletter.objects.all())

    context = {
        'sales':sales,
        'revenue':revenue,
        'subscribers':subscribers,
        'revenue_amount':revenue_amount,
        'payments':payments,
        'notifications': notifications,
        'DeliveryPriceByRegionFormCreator':DeliveryPriceByRegionFormCreator,
    }
    return render(request,'managementDb.html',context)


def distribuition(request):
    Notification.objects.filter(viewed=False,notification_type='Newsletter Addition').update(viewed=True)
    subscribers = Newsletter.objects.all()
    notifications = Notification.objects.all().filter(viewed=False)

    context ={
        'subscribers': subscribers,
        'start_value': 1,
        'notifications':notifications,
    }
    return render(request,'distribuition.html',context)

def productManagement(request):
    productFormCreator = ProductForm()
    categoryFormCreator = CategoryForm()
    categories = Category.objects.all()
    notifications = Notification.objects.all().filter(viewed=False)

    products = Product.objects.all()

    if request.method == 'POST':
        if 'addProduct' in request.POST:
            productFormCreator = ProductForm(request.POST, request.FILES)    
            if productFormCreator.is_valid(): 
                productFormCreator.save() 
                return redirect(productManagement)  # Redirect to the same page or a success page
            else:
                print('error')
        if 'createCategory' in request.POST:
            categoryFormCreator = CategoryForm(request.POST)
            if categoryFormCreator.is_valid():
                categoryFormCreator.save()
                return redirect(productManagement)
            else:
                print('error')

    context = {
        'productFormCreator':productFormCreator,
        'products':products,
        'categoryFormCreator':categoryFormCreator,
        'categories':categories,
        'notifications':notifications,
    }

    return render(request,'productsManagement.html',context)

class productEdit(View):
    def get_product(self):
        # Access unique_id from URL kwargs
        unique_id = self.kwargs['unique_id']
        return get_object_or_404(Product, unique_id=unique_id)

    def get(self,request,unique_id):
        product = Product.objects.get(unique_id=unique_id)
        productFormCreator = ProductForm(instance=product)
        notifications = Notification.objects.all().filter(viewed=False)
        relatedImage = product.relatedImages.all()
        if product.size_set:
            if product.size_set.name == 'Medium Large Xl 2xl 3xl':
                stock,created = MediumLargeStock.objects.get_or_create(product=product,size_set=product.size_set)
                stockform = MediumLargeStockForm(instance=stock)

            elif product.size_set.name == '39 - 46':
                stock,created = Size39to46.objects.get_or_create(product=product,size_set=product.size_set)
                stockform = Size39to46Form(instance=stock)
        else:
            stock = None
            stockform = ProductStockForm(instance=product)
        context ={
            'product':product,
            'productFormCreator':productFormCreator,
            'notifications':notifications,
            'stock':stock,
            'stockform':stockform,
        }
        return render(request,'productEdit.html',context)
    
    def post(self,request,unique_id):
        product = self.get_product()
        if product.size_set:
            if product.size_set.name == 'Medium Large Xl 2xl 3xl':
                stock,created = MediumLargeStock.objects.get_or_create(product=product,size_set=product.size_set)
                stockform = MediumLargeStockForm(instance=stock)

            elif product.size_set.name == '39 - 46':
                stock,created = Size39to46.objects.get_or_create(product=product,size_set=product.size_set)
                stockform = Size39to46Form(instance=stock)
        else:
            stock = None
            stockform = ProductStockForm(instance=product)
        
        product = self.get_product()
        if 'editProduct' in request.POST:
            productFormCreator = ProductForm(request.POST, request.FILES,instance=product)    
            if productFormCreator.is_valid(): 
                productFormCreator.save() 
                return redirect(productEdit,unique_id)  # Redirect to the same page or a success page
            else:
                print('error')
        if 'addBackImage' in request.POST:
            new_relatedImage = request.FILES.get('backImage')
            try:
                if new_relatedImage:
                    new_relatedImage = RelatedImages(product=product,image=new_relatedImage)
                    new_relatedImage.save()
                    return redirect(f'/productEdit/{unique_id}')
            except:
                print('error')
        if 'updateStock' in request.POST:
            if  product.size_set == None:
                stockform = ProductStockForm(request.POST,instance=product)
            elif product.size_set.name == 'Medium Large Xl 2xl 3xl':
                stockform = MediumLargeStockForm(request.POST,instance=stock)
            elif product.size_set.name == '39 to 46':
                stockform = Size39to46Form(request.POST,instance=stock)
           
               
        
            if stockform.is_valid():
                stockform.save()
                return redirect(f'/productEdit/{unique_id}')
            else:
                print('error')

def ordersList(request):
    Notification.objects.filter(viewed=False,notification_type='Product Sold').update(viewed=True)
    payments = Payment.objects.all().filter(verified=True)
    notifications = Notification.objects.all().filter(viewed=False)
    orders = len(payments)
    delivered = len(payments.filter(delivered=True))
    not_delivered = len(payments.filter(delivered=False))

    context ={
        'payments':payments,
        'orders':orders,
        'delivered':delivered,
        'not_delivered':not_delivered,
        'notifications':notifications,
        
        
    }
    return render(request,'ordersList.html',context)

BATCH_SIZE = 1  # Adjust batch size based on your SMTP provider limits

def send_newsletter_batch(request, batch_index):
    newsLetterBatch = NewsletterBatch.objects.all()[0].batch
   
    
   
    batch = ast.literal_eval(newsLetterBatch)
    batch = batch[batch_index]


    if not batch:
        return JsonResponse({'status': 'completed', 'batch': batch_index})

    # Prepare and send emails
    for email in batch:
        subject = "Our Latest Newsletter"
        text_body = "Hello! Check out our latest updates."
        html_content = render_to_string('newsletter_email.html', {'subject': subject, 'body': text_body})

        # Use EmailMultiAlternatives for HTML emails
        try:
            msg = EmailMultiAlternatives(subject, text_body, "kwakuwiredu0@gmail.com", [email])
            msg.attach_alternative(html_content, "text/html")  # Attach the HTML version
            msg.send()  # Send the email
        except Exception as e:
            print(f"Error sending email to {email}: {e}")
            return JsonResponse({'status': 'error', 'batch': batch_index, 'error': str(e)})

    return JsonResponse({'status': 'success', 'batch': batch_index, 'emails_sent': len(batch)})
def send_emails(request):
    batch_size = NewsletterBatch.objects.all()[0].batch_size
    context ={
        'batch_size':batch_size,
    }
    return render(request,'send_email.html')


def product_order_view(request):
    if request.method == "POST":
        # Fetch the updated order from the POST request
        order_data = request.POST.getlist('order')
        try:
            ids_list = order_data[0].split(',')  # Split the string into a list of IDs

            # Prepare a list of Product objects with updated `product_ordering` values
            products_to_update = []
            for index, product_id in enumerate(ids_list):
                products_to_update.append(Product(id=int(product_id), product_ordering=index))

            # Perform a bulk update
            Product.objects.bulk_update(products_to_update, ['product_ordering'])

            return JsonResponse({'status': 'success', 'message': 'Product order updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})       
        

    # Handle the GET request to display the products
    products = Product.objects.all().order_by('product_ordering')
    return render(request, 'updateOrdering.html', {'products': products})

# CBV

class Notifications_view(View):

    def get(self, request):
        Notification.objects.filter(viewed=False).update(viewed=True)
        

        notifications = Notification.objects.all().filter(viewed=False)
        notifications_table = Notification.objects.all()
        context = {
            'notifications':notifications,
            'notifications_table':notifications_table,
        }
        return render(request,'notifications.html',context)
    
class OrderDetailsView(View):

    def get(self,request,unique_id):
        return render(request,'orderDetailsView.html')


class MessagesReceived(View):
    def get(self,request):
        Notification.objects.filter(viewed=False,notification_type='Contact Form').update(viewed=True)
        notifications = Notification.objects.all().filter(viewed=False)
        contacts = Contact.objects.all()
        context ={
            'notifications':notifications,
            'contacts':contacts,
        }
        return render(request,'messagesReceived.html',context)
    
def deleteRelatedImages(request,id,unique_id):
    relatedImage = RelatedImages.objects.get(id=id)
    relatedImage.delete()
    return redirect(f'/productEdit/{unique_id}')