from django.urls import path

from .views import *
urlpatterns = [
    path('bonjour/',  hello),
    
    path('list/' , listEvent , name="list"),
    path('add/' , addEvent , name="addEvent"),

    path('details/<int:ide>' , detailsEvent , name="details"),

    path('listEvent/' , List.as_view()),
    path('addEvent/' , add.as_view()),
    path('update/<int:pk>' , UpdateEvent.as_view() , name="update"),
    path('delete/<int:pk>' , DeleteEvent.as_view() , name="delete"),
    path('participer/<int:eventId>' , participer , name="participer"),
    path('cancel/<int:eventId>' , cancel , name="cancel")

] 
