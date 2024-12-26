import ast
from django.shortcuts import render, redirect
from .models import Product, Outing, Payment, Cart, CartObject, Newsletter
from .deliveryRatesGen import generate_shipping_cost
from django.contrib import messages
from userAdmin.models import Revenue

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

    if request.method == 'POST':
        if 'subscribe' in request.POST:
            try:
                email = request.POST.get('email')
                phone = request.POST.get('phone')

                subscription = Newsletter(email=email,phone=phone)
                subscription.save()

                messages.success(request,'Subscribed.')
                return redirect(shop)
            except:
                messages.error(request,'Error. Try again later.')


    context ={
        'products':products,
        'events': events,
        
    }
    return render(request,'shop.html',context)

def makePayment(request,ref):
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
    return render(request,'checkout.html')

def orderSuccess(request,ref):
    payment = Payment.objects.get(ref=ref)
    payment.verified = True
    payment.save()

    #code for revenue
    
    # Extract year and month from `date_created`
    year = payment.date_created.year
    month = payment.date_created.month
    amount = payment.amount

    # Get or create the Revenue object for the year
    revenue, created = Revenue.objects.get_or_create(year=year)
    # cart 
    cart = Cart.objects.get(payment=payment)

    context ={
        'payment':payment,
        'cart':cart,
    }
    return render(request,'orderSuccess.html',context)

def contactPage(request):
    return render(request,'contact.html')

