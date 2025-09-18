from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payment.models import Payment

# Create your views here.


def home(request):
    return render(request,'html/home.html')

def gallery(request):
    return render(request,'html/gallery.html')



def adminLogin(request): #pass the login form in the admin login page
    if request.method == 'POST':
        username =  request.POST.get('username')
        password  = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/orders/list')
        else:
            messages.error(request,'Error Login in')
            return redirect(adminLogin)

        
            
    return render(request,'html/adminLogin.html')

@login_required(login_url='/')
def orderList(request):
    payments = Payment.objects.all().filter(verified=True)
    context = {
        'payments':payments,
    
    }
    print(payments)
    return render(request,'html/list.html',context)
