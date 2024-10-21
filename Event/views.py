from django.shortcuts import render,redirect

from .models import Event,Participants
from django.views.generic import *

from django.http import HttpResponse,JsonResponse
# Create your views here.
from .forms import EventForm

from django.urls import reverse_lazy
import google.generativeai as genai
import requests
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from Person.models import Person


from django.core.files import File
import io
from PIL import Image  
def hello(req):

    return HttpResponse("Hello 5twin 2")



GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

IMAGEGEN_KEY = os.getenv('HUGGING_FACE_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1-base"
headers = {"Authorization": f"Bearer {IMAGEGEN_KEY} "}

def imageGen(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content



def generate_image(request):
    if request.method == 'POST':
    # Generate the image
        data = json.loads(request.body)
        title = data.get('title', '')
        image_bytes = imageGen({
        "inputs": f"event for {title}", 
        })
        # Save the image to a temporary in-memory file
        image = Image.open(io.BytesIO(image_bytes))
        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            image_data = output.getvalue()
        # Save the image temporarily to the filesystem (e.g., in the media directory)
        image_name = 'generated_image.jpg'
        image_path = 'media/images/' + image_name
        with open(image_path, 'wb') as f:
                  f.write(image_data)
        return JsonResponse({'image_url': '/' + image_path})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
        
   











def ai_generate_description(title):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Generate a detailed description for an event with the title in 4 lines: {title}"
    
    response = model.generate_content(prompt)
    return response.text




def generate_description(request):
    
    if request.method=="POST":
        
        data= json.loads(request.body)
        
        title=  data.get('title','')
        description = ai_generate_description(title)
        
        return JsonResponse({'description':description})
    
    return JsonResponse({'error':'Invalid request'}, status=400)
        
         
        
        

def listEvent(request):
    
    events= Event.objects.all().order_by('category')
    
    
    return render(request,"event/list.html",{ "data":events })



def detailsEvent(request, ide):
    
    event = Event.objects.get(id=ide)
    
   
    user = request.user
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
    
    
    
    
@login_required
def addEvent(request):
    
    form = EventForm()
    
    if request.method=="POST":
        form = EventForm(request.POST,request.FILES)
        
        if form.is_valid():
            event = form.save(commit=False)

            form.instance.organisateur = request.user
            
            file_name = os.path.basename('generated_image.jpg')
            print(file_name)
            file_path = os.path.join('media/images', file_name)
            with open(file_path, 'rb') as f:
                event.image.save(file_name, File(f), save=True)
            event.save()
            print (event)
        form.save()
            
        return redirect("list")
            
    
    
    return render(request,"event/add.html", {'form':form})



class add(LoginRequiredMixin,CreateView):
    
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
    
    

    p1 = request.user    
    event1 = Event.objects.get(id=eventId)
    
    particpant = Participants.objects.create(person=p1 , event=event1)
    
    particpant.save()
    
    event1.nbr_participants += 1 
    
    event1.save()
    
    return redirect('list')


def cancel (request, eventId):
    p1 = request.user    
    
    event1 = Event.objects.get(id=eventId)
    
    particpant = Participants.objects.get(person=p1 , event=event1)
    
    particpant.delete()
    
    
    event1.nbr_participants -= 1 
    
    event1.save()
    
    return redirect('list')