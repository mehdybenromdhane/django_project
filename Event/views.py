from django.shortcuts import render

from .models import Event
from django.views.generic import ListView

from django.http import HttpResponse
# Create your views here.


def hello(req):

    return HttpResponse("Hello 5twin 2")


def listEvent(request):
    
    events= Event.objects.filter(state=True).order_by('category')
    
    
    return render(request,"event/list.html",{ "data":events })



def detailsEvent(request, ide):
    
    event = Event.objects.get(id=ide)
    
    return render(request,"event/details.html",{"event":event})


class List(ListView):
    model=Event
    context_object_name="data"
    
    template_name="event/list.html"
    
    