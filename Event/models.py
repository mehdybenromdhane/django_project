from django.db import models

# Create your models here.

from Person.models import Person

from datetime import datetime 
class Event(models.Model):


    category_list =(
        ("Musique","Musique"),
        ("Cinema","Cinema"),
        ("Sport","Sport"),

    )
    title = models.CharField(max_length=40)
    description= models.TextField()
    image= models.ImageField(null=True, upload_to="images/")
    category=models.CharField(max_length=20, choices=category_list)

    state = models.BooleanField(default=False) 

    nbr_participants = models.IntegerField(default=0)
    evt_date = models.DateTimeField(null=True)

    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    organisateur = models.ForeignKey(Person, on_delete=models.SET_NULL , null=True)
    participant = models.ManyToManyField(Person, through="Participants" , related_name="particpant")



    class Meta:
        constraints =[
            models.CheckConstraint(check=models.Q(
              evt_date__gt = datetime.now()

            ) , name = "Please check your event date")
        ]
    def __str__(self):

        return self.title
    

class Participants(models.Model):
    person = models.ForeignKey(Person , on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    participation_date = models.DateTimeField(datetime.now() , null=True, auto_now_add=True) 


    def __str__(self):
        return  f"{self.person} {self.event} "
    
    class Meta: 
        unique_together= ['person','event']

