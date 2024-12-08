from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

# adminDb

# @login_required(login_url='/login')
def userAdmin(request):
    return render(request,'userAdmin.html')