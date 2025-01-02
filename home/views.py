import ast
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Product, Outing, Payment, Cart, CartObject, Newsletter, UserLogin, Contact
from .deliveryRatesGen import generate_shipping_cost
from .password import generate_password
from django.contrib import messages
from userAdmin.models import Revenue, Notification

# Create your views here.
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render, redirect

def home(request):
    if  request.session.get("authenticated"):
        return redirect('shop/')
    else:
        if request.method == 'POST':
            if 'giveUserPassword' in request.POST:
                email = request.POST.get('email')
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                
                # Generate password logic (ensure this function is defined)
                password = generate_password() 
                
                # Save user information (ensure you have a model to save to)
                userLogin = UserLogin(email=email, first_name=fname, last_name=lname, password=password)
                userLogin.save()

                # Email content
                subject = 'Strangers Password'
                text_body = f'Your password is {password}.'
                html_content = render_to_string('password.html', {'first_name': fname, 'subject': subject, 'body': f'Your password is {password}.'})
                print(html_content)

                try:
                    # Create email object with alternatives
                    msg = EmailMultiAlternatives(subject, text_body, "kwakuwiredu0@gmail.com", [email])
                    msg.attach_alternative(html_content, "text/html")  # Attach the HTML version
                    msg.send()
                    messages.success(request, 'Password sent to email.')
                except Exception as e:
                    messages.error(request, 'Try again later.')
                    print(f'Error sending email: {e}')  # Log the error for debugging

                return redirect(home)
            
            if 'passwordLoginSubmit' in request.POST:
                password = request.POST.get('passwordLogin')

                try:
                    user = UserLogin.objects.get(password=password)
                    if user:
                        request.session["authenticated"] = True
                        return redirect("shop/")  
                    else:
                        messages.error(request, 'Invalid password.')
                        print('invalid')
                        return redirect('/')
                        
                except:
                    messages.error(request, 'Invalid password.')
                    print('invalid')
                    return redirect('/')

        context = {
            # You can add context data if necessary for rendering home page
        }
        return render(request, 'home.html', context)


def productDetailPage(request,unique_id):
    if not request.session.get("authenticated"):
        return redirect('/')
    else:
        product = Product.objects.get(unique_id=unique_id)

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
        }
        return render(request,'productDetails.html',context)

def shop(request):
    if not request.session.get("authenticated"):
        return redirect('/')
    else:
        products = Product.objects.all()
        events = Outing.objects.all()

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
                    
                    return redirect(shop)
                except Exception as e:
                    print(e)
                    messages.error(request,'Error. Try again later.')
                    return redirect(shop)


        context ={
            'products':products,
            'events': events,
            
        }
        return render(request,'shop.html',context)

def makePayment(request,ref):
    if not request.session.get("authenticated"):
        return redirect('/')
    else:
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
                    'tee':0,
                    'hoodie':0,
                    'shorts':0,
                    'joggers':0,
                }
                for item in payment.cart.cart_objects.all():
                    items[item.product.category.lower()] += item.quantity
                delivery_cost = generate_shipping_cost(items,payment.destination_country)
                print(delivery_cost)
                if 'N/A' in str(delivery_cost):
                    delivery_cost = 0
                    ship_to = False #
                else:
                    payment.delivery_price = round(delivery_cost,2)
                    payment.save()

                print(items,delivery_cost)

            
            context ={
                'payment':payment,
                'ship_to':ship_to,
            }
            return render(request,'makePayment.html',context)



def checkout(request):
    if not request.session.get("authenticated"):
        return redirect('/')
    else:
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

                payment = Payment(first_name=firstName,last_name=lastName,email=email,country_code=country_code,phone=phone,order_notes=orderNotes,street_address_1=street_address_1,street_address_2=street_address_2,city=city,state=state,zip_code=zip_code,destination_country=destination_country,additional_info=deliveryInfo,amount=float(cart_total))
                payment.save()
                
                # on payment save create cart for payment
                cart = Cart.objects.get_or_create(payment=payment) # create cart for payment
                cart[0].save()

                # loop through cart object list to append to cart
                for obj in cartData:
                    product = Product.objects.get(unique_id=obj['product_id'])
                    cartObj = CartObject(cart=cart[0],product=product,size=obj['selectedSize'],quantity=obj['quantity'] )
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

        return render(request,'checkout.html')

def orderSuccess(request,ref):
    if not request.session.get("authenticated"):
        return redirect('/')
    else:
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
        payment.verified = True
        payment.save()

        #code for revenue
        
    
        year = payment.date_created.year
        month = payment.date_created.month
        amount = payment.amount

        # Get or create the Revenue object for the year
        revenue, created = Revenue.objects.get_or_create(year=year)
        revenue.update_monthly_revenue(month, amount)
        print(f'the month is {month} and the amount is {amount}')
        cart = Cart.objects.get(payment=payment)

        # create notification
        new_Notification = Notification(title='Product Sold',message=f'GHS{payment.total_actual} paid for order #{payment.order_id}.',notification_type='Contact Form')
        new_Notification.save()

        context ={
            'payment':payment,
            'cart':cart,
        }
        return render(request,'orderSuccess.html',context)

def contactPage(request):
    if not request.session.get("authenticated"):
        return redirect('/')
    else:
        if request.method == 'POST':
            if 'contactSend' in request.POST:
                try:
                    first_name = request.POST.get('first_name')
                    last_name = request.POST.get('last_name')
                    email = request.POST.get('email')
                    message = request.POST.get('message')

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

        }
        return render(request,'contact.html',context)

