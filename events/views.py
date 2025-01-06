from django.shortcuts import render
from home.models import Outing
from django.views import View

# Create your views here.

class Events(View):

    def get(self,request):
        events = Outing.objects.all()
        context = {
            'events':events
        }
        return render(request,'events.html',context)


class EventDetailView(View):

    def get(self,request,unique_id):
        return render(request,'eventDetail.html')