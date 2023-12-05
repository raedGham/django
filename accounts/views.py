from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .forms import registrationForm
from .models import Account
# Create your views here.


def register(request):
    
    if request.method == "POST":
        form = registrationForm(request.POST)
     
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, 
                                               email = email , password = password)
            user.phone_number = phone_number
          
            user.save()
            messages.success(request,"Registered sucessfully")
            return redirect('register')
    else:        
        form = registrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method =="POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
