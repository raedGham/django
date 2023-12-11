from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import registrationForm
from .models import Account
from carts.models import Cart,CartItem
from carts.views import _cart_id
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
                                               email=email, password=password)
            user.phone_number = phone_number

            user.save()

            # user activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html', {
                'request':request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # end activation

            messages.success(request, "Registered sucessfully")
            return redirect('register')
    else:
        form = registrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
              cart = Cart.objects.get(cart_id= _cart_id(request)) 
              is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
              if is_cart_item_exists:
                  cart_item = CartItem.objects.filter(cart=cart)
                  for item in cart_item:
                      item.user = user
                      item.save()

            except:
              pass    
            auth.login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


def activate(request):
    return

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgetPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact = email)

            # user send email to user
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password_email.html', {
                'request':request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Password rest email has been sent to your email address")
            return redirect("login")
            # end send email
        else:     
             messages.error(request, "Account does not exists")
             return redirect("forgetPassword")     
        
    return render(request, 'accounts/forgetPassword.html')


def reset_password_validate(request):
    return