from django.shortcuts import render, HttpResponse
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
    else:        
        form = registrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return HttpResponse("logout")
