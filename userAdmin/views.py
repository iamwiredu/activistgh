from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, RelatedImagesForm
from home.models import Product, Newsletter

#import for emails

from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives, send_mass_mail
from django.template.loader import render_to_string




# @login_required(login_url='/login')
def userAdmin(request):
    return render(request,'userAdmin.html')


# Management Db
def managementDb(request):
    return render(request,'managementDb.html')


def distribuition(request):
    subscribers = Newsletter.objects.all()
    context ={
        'subscibers': subscribers,
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

BATCH_SIZE = 1  # Adjust batch size based on your SMTP provider limits

def send_newsletter_batch(request, batch_index):
    # Fetch email addresses
    subscribers = list(Newsletter.objects.values_list('email', flat=True))
    start = batch_index * BATCH_SIZE
    end = start + BATCH_SIZE
    batch = subscribers[start:end]

    if not batch:
        return JsonResponse({'status': 'completed', 'batch': batch_index})

    # Prepare emails
    messages = []
    for email in batch:
        subject = "Our Latest Newsletter"
        text_body = "Hello! Check out our latest updates."
        html_content = render_to_string('newsletter_email.html', {'subject': subject, 'body': text_body})
        
        # Use EmailMultiAlternatives for HTML emails
        msg = EmailMultiAlternatives(subject, text_body, None, [email])
        msg.attach_alternative(html_content, "text/html")
        messages.append(msg)
    print(subscribers)

    # Send emails in bulk
    try:
        EmailMultiAlternatives.send_messages(messages)# Send all messages in the batch
        print(messages)
    except Exception as e:
        return JsonResponse({'status': 'error', 'batch': batch_index, 'error': str(e)})
        print(messages)
    return JsonResponse({'status': 'success', 'batch': batch_index, 'emails_sent': len(batch)})


def send_emails(request):
    return render(request,'send_email.html')