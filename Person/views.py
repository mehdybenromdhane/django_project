from django.shortcuts import render,redirect


from django.contrib.auth import login,authenticate
# Create your views here.

from .forms import UserRegisterForm

from django.contrib import messages

def register(request):
    
    if request.user.is_authenticated:
        
        return redirect("list")
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            
            user = form.save()
            login(request,user)
            
            return redirect("list")
        else:
            for error in list(form.errors.values()):
                print(request,error)
                
    else:
        form = UserRegisterForm()
        
    return render(request, "auth/register.html", {"form":form})



def login_user(request):
    
    if request.method=="POST":
        
        username = request.POST['username']
        pwd= request.POST['password']
        
        user = authenticate(request,username=username , password=pwd)
        
        if user is not None:
            login(request,user)
            return redirect("list")
        
        else:
            messages.info(request,"Username or password incorrect")
            return redirect("login")
        
    else: 
        
        return render(request,'auth/login.html')