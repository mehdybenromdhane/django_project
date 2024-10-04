from django.urls import path

from .views import *
urlpatterns = [
    path('bonjour/',  hello),
    
    path('list/' , listEvent),
    
    path('details/<int:ide>' , detailsEvent , name="details"),

    path('listEvent/' , List.as_view())

] 
