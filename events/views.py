from django.shortcuts import render

# Create your views here.

def events(request,unique_id):
    return render(request,'events.html')