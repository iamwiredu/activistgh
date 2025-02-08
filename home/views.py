import ast, json, requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Product, Outing, Payment, MediumLargeStock,Size39to46,Cart, Category,CartObject, Newsletter, UserLogin, Contact, Category
from .deliveryRatesGen import generate_shipping_cost
from .password import generate_password
from django.contrib import messages
from userAdmin.models import Revenue, Notification, DeliveryPriceByRegion, DeliveryPriceByAccra

# Create your views here.
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse



def home(request):
    categories = Category.objects.all()
    context = {
     'categories':categories,
    }
    return render(request, 'home.html', context)


def productDetailPage(request,unique_id):
    product = Product.objects.get(unique_id=unique_id)
    categories = Category.objects.all()
    product_sizeset = product.size_set
    if product.size_set:
        if product_sizeset.name == 'Medium Large Xl 2xl 3xl':
            sizeset_stock,created = MediumLargeStock.objects.get_or_create(product=product)  
        elif product_sizeset.name == '39 - 46':
            sizeset_stock,created = Size39to46.objects.get_or_create(product=product)
    else:
        sizeset_stock = product.stock

    print(product_sizeset)
    if request.method == 'POST':
        if 'subscribe' in request.POST:
            try:
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                subscription = Newsletter(first_name=first_name,last_name=last_name,email=email,phone=phone)
                subscription.save()

                messages.success(request,'Subscribed.')

                # add notification
                new_Notification = Notification(title='New Subscriber',message=f'{email} has subscribed to the newsletter',notification_type='NewsLetter Addition')

                new_Notification.save()
                
                return redirect(f'/product/{unique_id}/')
            except Exception as e:
                print(e)
                messages.error(request,'Error. Try again later.')
                return redirect(f'/product/{unique_id}/')

    context ={
        'product': product,
        'sizeset_stock':sizeset_stock,
        'categories':categories,
    }
    return render(request,'productDetails.html',context)


def get_stock(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            product_id = data.get('product_id')
            size = data.get('size')

            # Fetch the product and calculate stock for the selected size
            product = Product.objects.get(id=product_id)
            stock = product.get_size(size)  # Adjust as needed for your model method

            return JsonResponse({'stock': stock})

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def shop(request,category_name):
    if '%2520' in category_name:
        split = category_name.split('%2520')
        joined = ' '.join(split)
        category_name = joined
    category = Category.objects.get(name=category_name)
    products = Product.objects.all().filter(product_category=category)
    events = Outing.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        if 'subscribe' in request.POST:
            try:
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                subscription = Newsletter(first_name=first_name,last_name=last_name,email=email,phone=phone)
                subscription.save()

                messages.success(request,'Subscribed.')

                # add notification
                new_Notification = Notification(title='New Subscriber',message=f'{email} has subscribed to the newsletter',notification_type='NewsLetter Addition')

                new_Notification.save()
                
                return redirect(f'/shop/{category_name}/')
            except Exception as e:
                print(e)
                messages.error(request,'Error. Try again later.')
                return redirect(shop)


    context ={
        'products':products,
        'events': events,
        'categories':categories,
    }
    return render(request,'shop.html',context)

# page to list events

    
def makePayment(request,ref):
    categories = Category.objects.all()
    if request.method == 'POST':
        if 'subscribe' in request.POST:
            try:
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                subscription = Newsletter(first_name=first_name,last_name=last_name,email=email,phone=phone)
                subscription.save()

                messages.success(request,'Subscribed.')

                # add notification
                new_Notification = Notification(title='New Subscriber',message=f'{email} has subscribed to the newsletter',notification_type='NewsLetter Addition')

                new_Notification.save()
                
                return redirect(f'/makePayment/{ref}/')
            except Exception as e:
                print(e)
                messages.error(request,'Error. Try again later.')
                return redirect(f'/makePayment/{ref}/')

    else:
        payment = Payment.objects.get(ref=ref)
        ship_to = True

        if payment.destination_country != 'Ghana':
            # international delivery calculate for price:
            # need to quantify the item's into right data form

            items = {
               
                'hoodie':0,
               
            }
            for item in payment.cart.cart_objects.all():
                items['hoodie'] += item.quantity
            delivery_cost = generate_shipping_cost(items,payment.destination_country)
            print(delivery_cost)
            if 'N/A' in str(delivery_cost):
                delivery_cost = 0
                ship_to = False #
            else:
                payment.delivery_price = round(delivery_cost,2)
                payment.save()

            print(items,delivery_cost)
        else:
            if payment.pickupdata == True:
                payment.delivery_price =  0
                payment.save()
            else:
                if payment.state != 'greater_accra':
                    delivery_price_object = DeliveryPriceByRegion.objects.all()[0]
                    delivery_cost = getattr(delivery_price_object,payment.state.lower())
                    payment.delivery_price =  delivery_cost/16
                else:
                    delivery_price_object = DeliveryPriceByAccra.objects.all()[0]
                    delivery_cost = getattr(delivery_price_object,payment.accralocation.lower())
                    payment.delivery_price =  delivery_cost/16

            
                payment.save()
            
        
        context ={
            'payment':payment,
            'ship_to':ship_to,
            'categories':categories,
        }
        return render(request,'makePayment.html',context)



def checkout(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        if 'pay' in request.POST:
            cartData = request.POST.get('cartData')
            cartData =ast.literal_eval(cartData)

            

            # delivery info 
            firstName = request.POST.get('fname')
            lastName = request.POST.get('lname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            orderNotes = request.POST.get('orderNotes')
            street_address_1 = request.POST.get('street_address_1')
            street_address_2 = request.POST.get('street_address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip')
            destination_country = request.POST.get('destination_country')
            deliveryInfo = request.POST.get('deliveryInfo')
            cart_total = request.POST.get('cart-total')
            country_code = request.POST.get('country_code')
            pickupdata = request.POST.get('pickupdata')
            accralocation = request.POST.get('location')

            if pickupdata == 'yes':
                pickupdata = True
            else:
                pickupdata = False

            payment = Payment(first_name=firstName,last_name=lastName,email=email,country_code=country_code,phone=phone,order_notes=orderNotes,street_address_1=street_address_1,street_address_2=street_address_2,city=city,state=state,zip_code=zip_code,destination_country=destination_country,additional_info=deliveryInfo,amount=float(cart_total),pickupdata=pickupdata,accralocation=accralocation)
            print(accralocation)
            payment.save()
            
            # on payment save create cart for payment
            cart = Cart.objects.get_or_create(payment=payment) # create cart for payment
            cart[0].save()

            # loop through cart object list to append to cart
            for obj in cartData:
                product = Product.objects.get(unique_id=obj['product_id'])
                cartObj = CartObject(cart=cart[0],product=product,size=obj['selectedSize'],quantity=obj['quantity'],sizeData=obj['selectedSizeData'] )
                cartObj.save()


            return redirect(makePayment,payment.ref)
        if 'subscribe' in request.POST:
            try:
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                subscription = Newsletter(first_name=first_name,last_name=last_name,email=email,phone=phone)
                subscription.save()

                messages.success(request,'Subscribed.')

                # add notification
                new_Notification = Notification(title='New Subscriber',message=f'{email} has subscribed to the newsletter',notification_type='NewsLetter Addition')

                new_Notification.save()
                
                return redirect(checkout)
            except Exception as e:
                print(e)
                messages.error(request,'Error. Try again later.')
                return redirect(checkout)
    context ={
        'categories':categories,
    }
    return render(request,'checkout.html',context)

def orderSuccess(request,ref):
    if request.method == 'POST':
        if 'subscribe' in request.POST:
            try:
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                subscription = Newsletter(first_name=first_name,last_name=last_name,email=email,phone=phone)
                subscription.save()

                messages.success(request,'Subscribed.')

                # add notification
                new_Notification = Notification(title='New Subscriber',message=f'{email} has subscribed to the newsletter',notification_type='NewsLetter Addition')

                new_Notification.save()
                
                return redirect(f'/orderSuccess/{ref}/')
            except Exception as e:
                print(e)
                messages.error(request,'Error. Try again later.')
                return redirect(f'/orderSuccess/{ref}/')


    payment = Payment.objects.get(ref=ref)
    cart = Cart.objects.get(payment=payment)
    print(f'This is the payment verified {payment.verified}')
    if not payment.verified:  # Simplified comparison
       
        for item in payment.cart.cart_objects.all():
            if item.product.size_set:
                print(f'we are here in if product.size_set {payment.verified}')
                if item.product.size_set.name == 'Medium Large Xl 2xl 3xl':  
                
                    mediumLarge,created = MediumLargeStock.objects.get_or_create(product=item.product)
                    stock_field = getattr(mediumLarge, item.sizeData, None)
                    if stock_field is not None:
                    
                        setattr(mediumLarge, item.sizeData, stock_field - item.quantity)
                        mediumLarge.save()
                elif item.product.size_set.name == '39 - 46':
                    print('size here')
                    size39to46,created = Size39to46.objects.get_or_create(product=item.product)
                    stock_field = getattr(size39to46,item.sizeData,None)
                    print(stock_field,item.quantity)
                    if stock_field is not None:
                        setattr(size39to46, item.sizeData, stock_field - item.quantity)
                        size39to46.save()
            else:
                item.product.stock  -= 1
                item.product.save()
                

        payment.verified = True
        payment.save()

                    # Email content
        subject = 'Strangers Email Receipt'
        text_body = f'Your order was successful follow up on your purchases here'
        html_content = render_to_string('receipt.html', {'first_name': payment.first_name, 'subject': subject, 'body':text_body,'unique_id':payment.unique_id,'payment':payment})
        print(html_content)

        try:
            # Create email object with alternatives
            msg = EmailMultiAlternatives(subject, text_body, "Strangersofficial6@gmail.com", [payment.email])
            msg.attach_alternative(html_content, "text/html")  # Attach the HTML version
            msg.send()
            print('sent')
        except Exception as e:
            print('error')
            print(f'Error sending email: {e}')  # Log the error for debugging


    #code for revenue
    

        year = payment.date_created.year
        month = payment.date_created.month
        amount = payment.amount

       
        revenue, created = Revenue.objects.get_or_create(year=year)
        revenue.update_monthly_revenue(month, amount)
        print(f'the month is {month} and the amount is {amount}')
        cart = Cart.objects.get(payment=payment)

        # create notification
        new_Notification = Notification(title='Product Sold',message=f'GHS{payment.total_actual} paid for order #{payment.order_id}.',notification_type='Product Sold')
        new_Notification.save()

    context ={
        'payment':payment,
        'cart':cart,
    }
    print(payment.verified)
    return render(request,'orderSuccess.html',context)

def contactPage(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        if 'contactSend' in request.POST:
            try:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                message = request.POST.get('message')
                print(message)


                
                


                new_Notification = Notification(title='Contact Form',message=f'{email} has sent a message',notification_type='Contact Form')
                new_Notification.save()

                new_contact = Contact(first_name=first_name,last_name=last_name,email=email,message=message,notification=new_Notification)
                
                new_contact.save()
                messages.success(request,'Message Sent.')

                # add notification

                

                
                return redirect(contactPage)
            except Exception as e:
                print(e)
                messages.error(request,'Error. Try again later.')
                return redirect(contactPage)
            
        if 'subscribe' in request.POST:
            try:
                first_name = request.POST.get('fname')
                last_name = request.POST.get('lname')
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                subscription = Newsletter(first_name=first_name,last_name=last_name,email=email,phone=phone)
                subscription.save()

                messages.success(request,'Subscribed.')

                # add notification
                new_Notification = Notification(title='New Subscriber',message=f'{email} has subscribed to the newsletter',notification_type='NewsLetter Addition')

                new_Notification.save()
                
                return redirect(contactPage)
            except Exception as e:
                print(e)
                messages.error(request,'Error. Try again later.')
                return redirect(contactPage)


    context = {
        'categories':categories,

    }
    return render(request,'contact.html',context)

def bulksms(request):
    if request.method == 'POST':
        message = request.POST.get('Message')
        endPoint = 'https://api.mnotify.com/api/sms/group'
        apiKey = '4Vrc1NP8PUeS4nB51QgHvkD4W'
        
        data = {
            'group_id[]': ['54118'],
            'sender': 'Strangers',
            'message': str(message),
            'message_id':10,
            'is_schedule': "false",
            'schedule_date': ''
        }
        url = endPoint + '?key=' + apiKey
        try:
            response = requests.post(url, data)
            response.raise_for_status()  # Raises HTTPError if the HTTP request returned an unsuccessful status code
            response_data = response.json()
            print("Response Data:", response_data)
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
        except ValueError as e:
            print("Error decoding JSON response:", e)

    return render(request,'bulkSms.html')