from django.urls import path

from .views import hello
urlpatterns = [
    path('bonjour/',  hello),
]
