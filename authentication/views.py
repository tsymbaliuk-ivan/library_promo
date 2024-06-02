from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from .models import CustomUser
from .forms import RegistrationForm, LoginForm
from django.contrib import messages, auth
from django_ratelimit.decorators import ratelimit
from django.conf import settings
import requests




@ratelimit(key='ip', rate='5/m', block=True)
def register(request):
    form = [{'id_name': 'name', 'name': 'First Name'},
            {'id_name': 'middle_name', 'name': 'Middle name'},
            {'id_name': 'last_name', 'name': 'Last name'},
            {'id_name': 'email', 'name': 'Email'},
            {'id_name': 'password', 'name': 'Password'},
            {'id_name': 'role', 'name': 'Role'}
            ]

    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            data = request.POST
            user = CustomUser.objects.create_user(email=data['email'],
                                                  password=data['password'],
                                                  first_name=data['name'],
                                                  middle_name=data['middle_name'],
                                                  last_name=data['last_name'],
                                                  role=data['role'],
                                                  )
            user.save()
            if user:
                return redirect('home')
        else:
            # Handle reCAPTCHA validation failure
            context = {
                'form': form,
                'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY,
                'error': 'Invalid reCAPTCHA. Please try again.'
            }
            return render(request, 'register.html', context=context)

    context = {
        'form': form,
        'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY
    }
    return render(request, 'register.html', context=context)



@ratelimit(key='ip', rate='5/m', block=True)  # Limit to 5 requests per minute per IP
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.get_by_email(email=email)

            if user:
                if not user.check_password(password):
                    messages.error(request, 'ERROR! Incorrect password!')
                    return redirect("login")
            else:
                messages.error(request, 'ERROR! The user does not exist, please sign up!')
                return redirect("login")

            auth.login(request, user)
            user.is_active = True
            user.save()
            messages.success(request, 'Success! You are logged in!')
            return redirect("home")
        else:
            messages.error(request, 'ERROR! Invalid reCAPTCHA. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



@ratelimit(key='ip', rate='5/m', block=True)
def log_out(request):
    logout(request)
    messages.info(request, "Logged out!")
    return redirect("home")

@ratelimit(key='ip', rate='5/m', block=True)
def get_all(request):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "get_users.html", {"users": CustomUser.get_all()})


@ratelimit(key='ip', rate='5/m', block=True)
def user_info(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "get_user_by_id.html", context={"user": CustomUser.get_by_id(id)})

@ratelimit(key='ip', rate='5/m', block=True)
def delete_user(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    CustomUser.delete_by_id(id)
    return redirect("get_users")
@ratelimit(key='ip', rate='5/m', block=True)
def home(request):
    return render(request, "home.html")