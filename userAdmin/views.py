import ast
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, RelatedImagesForm
from .models import Revenue, Notification 
from home.models import Product, Newsletter, Payment, NewsletterBatch
from datetime import datetime

#import for emails

from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives, send_mass_mail
from django.template.loader import render_to_string

# import view

from django.views import View



# @login_required(login_url='/login')
def userAdmin(request):
    return render(request,'userAdmin.html')


# Management Db
def managementDb(request):
    sales = len(Payment.objects.all().filter(verified=True))
    payments = Payment.objects.all().filter(verified=True)
    notifications = Notification.objects.all().filter(viewed=False)
    # get current revenue
    currentYear = datetime.now().year
    revenue = Revenue.objects.get_or_create(year=currentYear)

    revenue_amount = 0 

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
    }
    return render(request,'managementDb.html',context)


def distribuition(request):
    subscribers = Newsletter.objects.all()

    context ={
        'subscribers': subscribers,
        'start_value': 1,
    }
    return render(request,'distribuition.html',context)

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

    try:
        relatedImage = product.relatedImages.all()[0]
    except:
        relatedImage = None
    

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
    payments = Payment.objects.all().filter(verified=True)
    orders = len(payments)
    delivered = len(payments.filter(delivered=True))
    not_delivered = len(payments.filter(delivered=False))

    context ={
        'payments':payments,
        'orders':orders,
        'delivered':delivered,
        'not_delivered':not_delivered,
        
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


# CBV

class Notifications_view(View):

    def get(self, request):
        notifications = Notification.objects.all()
        context = {
            'notifications':notifications,
        }
        return render(request,'notifications.html',context)