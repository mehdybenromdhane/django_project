from django.shortcuts import render,redirect

from .models import Event,Participants
from django.views.generic import *

from django.http import HttpResponse
# Create your views here.
from .forms import EventForm

from django.urls import reverse_lazy


from Person.models import Person
def hello(req):

    return HttpResponse("Hello 5twin 2")


def listEvent(request):
    
    events= Event.objects.all().order_by('category')
    
    
    return render(request,"event/list.html",{ "data":events })



def detailsEvent(request, ide):
    
    event = Event.objects.get(id=ide)
    
    user = Person.objects.get(cin=7884)
    
    if user:
        participant= Participants.objects.filter(person=user,event=event)
        
        if participant:
            button_disabled= True
            
        else:
            button_disabled=False
    
    return render(request,"event/details.html",{"event":event , "button":button_disabled})





class List(ListView):
    model=Event
    context_object_name="data"
    
    template_name="event/list.html"
    
    def get_queryset(self):
        
        events = Event.objects.all().order_by('category')
        
        return events
    
    
    
    
def addEvent(request):
    
    form = EventForm()
    
    if request.method=="POST":
        form = EventForm(request.POST,request.FILES)
        
        if form.is_valid():
            
            form.save()
            
            return redirect("list")
            
    
    
    return render(request,"event/add.html", {'form':form})



class add(CreateView):
    
    model=Event
    template_name="event/add.html"
    
    form_class= EventForm
    
    success_url=reverse_lazy("list")
    


class UpdateEvent(UpdateView):
    
    model=Event
    template_name="event/update.html"
    
    form_class=EventForm
    
    success_url=reverse_lazy("list")
    
    

class DeleteEvent(DeleteView):
    model=Event
    template_name="event/delete.html"
    
    success_url=reverse_lazy("list")
    
    

def participer(request, eventId):
    
    
    p1 = Person.objects.get(cin=7884)
    
    event1 = Event.objects.get(id=eventId)
    
    particpant = Participants.objects.create(person=p1 , event=event1)
    
    particpant.save()
    
    event1.nbr_participants += 1 
    
    event1.save()
    
    return redirect('list')


def cancel (request, eventId):
    p1 = Person.objects.get(cin=7884)
    
    event1 = Event.objects.get(id=eventId)
    
    particpant = Participants.objects.get(person=p1 , event=event1)
    
    particpant.delete()
    
    
    event1.nbr_participants -= 1 
    
    event1.save()
    
    return redirect('list')