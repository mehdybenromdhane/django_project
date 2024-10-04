from django.contrib import admin,messages

# Register your models here.

from .models import *




class nbr_participants(admin.SimpleListFilter):
    
    title="Number of participants"
    parameter_name="nbr_participants"
    
    def lookups(self,request,model_admin):
        return(
            ('No',("No participant")),
            ('Yes',("There are participants"))
        )
    def queryset(self,request,queryset):
        if self.value()=="No":
            return queryset.filter(nbr_participants__exact=0)
        
        if self.value() == "Yes":
            return queryset.filter(nbr_participants__gt=0)





    
        
        
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    
    
    def accept_state(ModelAdmin, request,queryset):
        
        row_updated= queryset.update(state=True)
        
        if (row_updated == 1):
            msg = "1 event was"
            
        else:
            
            msg = f"{row_updated} events were" 
            
        messages.success(request, f"{msg} successfully updated"  )
        
        
        
        
    def refuse_state(ModelAdmin, request,queryset):
        
        row_updated= queryset.update(state=False)
        
        if (row_updated == 1):
            msg = "1 event was"
            
        else:
            
            msg = f"{row_updated} events were" 
            
        messages.success(request, f"{msg} successfully updated"  )
    list_display=('title','nbr_participants','state','category','evt_date','description','participant',)

    actions=[accept_state , refuse_state]
    def numberOfParticipant(self,obj):
        
        nb = obj.participant.count()
        return nb
    
    numberOfParticipant.short_description = " Number"
    
    accept_state.short_description =  "State True"
    refuse_state.short_description =  "State False" 

    list_per_page= 5
    
    
    list_filter=('category',nbr_participants)

    
    
admin.site.register(Participants)