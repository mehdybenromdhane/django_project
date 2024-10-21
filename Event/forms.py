
from django.forms import ModelForm,TextInput,Textarea

from .models import Event
from django import forms


class DateInput(forms.DateInput):
    
    input_type='date'


class EventForm(ModelForm):
    
    class Meta:
        model=Event
        
        fields="__all__"
        
        exclude=('state',"nbr_participants" , "participant",'organisateur')
        
        
    
        widgets={ 'evt_date':DateInput()    , 'description':Textarea(attrs={'class':'form-control' ,'cols':10,'rows':10 , 'required':False}) , 'title':TextInput(attrs={'class':'form-control'})}
        
    image = forms.ImageField(required=False)