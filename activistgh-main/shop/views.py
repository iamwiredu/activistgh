from django.shortcuts import render,redirect
from .models import Product, RelatedImages
from .forms import DeliveryStatusUpdateForm
from payment.models import Payment
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings 
from .models import Cart, CartObject
from .deliveryRatesGen import generate_shipping_cost
import ast
import json
# Create your views here.

def shop(request):
    products = Product.objects.all().order_by('order_number')
    context ={
        'products':products,
    }
    return render(request,'html/shop.html',context)

def productDetail(request,unique_id):
    product = Product.objects.get(unique_id=unique_id)
    related = Product.objects.all().exclude(name = product.name).filter(tag=product.tag)[:3]
    relatedImages = RelatedImages.objects.all().filter(product=product)
    context ={
        'product':product,
        'related':related,
        'relatedImages':relatedImages,
    }
    return render(request,'html/productDetail.html',context)


def makePayment(request,ref):
    payment = Payment.objects.get(ref=ref)
    paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
    ship_to = False

    # if payment.destination_country != 'Ghana':
    #     # international delivery calculate for price:
    #     # need to quantify the item's into right data form

    #     items = {
    #         'tee':0,
    #         'hoodie':0,
    #         'shorts':0,
    #         'joggers':0,
    #     }
    #     for item in payment.cart.cart_objects.all():
    #         items[item.product.tag] += item.quantity
    #     delivery_cost = generate_shipping_cost(items,payment.destination_country)
    #     print(delivery_cost)
    #     if 'N/A' in str(delivery_cost):
    #         delivery_cost = 0
    #         ship_to = False #
    #     else:
    #         # payment.delivery_price = round(delivery_cost,2)
    #         payment.delivery_price = 0
    #         payment.save()

    #     print(items,delivery_cost)

    context ={
        'payment':payment,
        'paystack_public_key':paystack_public_key,
        'ship_to':ship_to,
    }
    return render(request,'html/makePaymentNew.html',context)

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

     
    return render(request,'html/checkout.html')


def orderSuccess(request,ref):
    
    payment = Payment.objects.get(ref=ref)
    payment.verified = True
    payment.save()

    # 2. Build the link the customer will click to view their order status
    payment_link = f'http://www.activist.store/orderDetails/{payment.ref}'

    # 3. Prepare email context
    context = {
        'payment': payment,
        'payment_link': payment_link,
    }

    # 4. Render the HTML email template
    subject = f"Thank you for your order {payment.first_name}!"
    from_email = 'Activist <contact@activist.store>'
    to_email = str(payment.email)
    
    # A plain-text fallback
    text_content = (
        f"Hi {payment.first_name},\n\n"
        f"Thank you for your order #{payment.order_id}!\n"
        f"To check the status of your order, visit:\n"
        f"{payment_link}\n\n"
        "Thanks again for shopping with us."
    )

    html_content = render_to_string(
        'html/order_confirmation_email.html',
        context
    )

    # 5. Send the email
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
    except Exception as e:
        # you might log this or show a user-friendly message
        print(f"Order confirmation email failed: {e}")


    # cart 
    cart = Cart.objects.get(payment=payment)

    context ={
        'payment':payment,
        'cart':cart,
    }
    return render(request,'html/orderSuccess.html',context)

def orderDetails(request,ref):
    payment = Payment.objects.get(ref=ref)
    DeliveryStatusUpdateFormCreator = DeliveryStatusUpdateForm(instance=payment)

    if request.method == 'POST':
        if 'updateDeliveryStatus' in request.POST:
            DeliveryStatusUpdateFormCreator = DeliveryStatusUpdateForm(request.POST, instance=payment)
            if DeliveryStatusUpdateFormCreator.is_valid():
                DeliveryStatusUpdateFormCreator.save()
                return redirect(f'/orders/list/')
            else:
                print('Form errors:', DeliveryStatusUpdateFormCreator.errors) 
            

    context = {
        'payment':payment,
        'DeliveryStatusUpdateFormCreator':DeliveryStatusUpdateFormCreator,

    }
    print(payment)
    return render(request,'html/orderDetails.html',context)