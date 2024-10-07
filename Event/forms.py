
from django.forms import ModelForm,TextInput


from .models import Event
from django import forms


class DateInput(forms.DateInput):
    
    input_type='date'


class EventForm(ModelForm):
    
    class Meta:
        model=Event
        
        fields="__all__"
        
        exclude=('state',"nbr_participants" , "participant")
        
        
        widgets={ 'evt_date':DateInput()    , 'description':TextInput(attrs={'class':'form-control'}) , 'title':TextInput(attrs={'class':'form-control'})}