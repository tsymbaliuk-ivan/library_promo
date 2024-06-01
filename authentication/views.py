from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from .models import CustomUser
from .forms import RegistrationForm, LoginForm
from django.contrib import messages, auth

def register(request):


    if request.method == 'POST':
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

    form = [{'id_name': 'name', 'name': 'First Name'},
            {'id_name': 'middle_name', 'name': 'Middle name'},
            {'id_name': 'last_name', 'name': 'Last name'},
            {'id_name': 'email', 'name': 'Email'},
            {'id_name': 'password', 'name': 'Password'},
            {'id_name': 'role', 'name': 'Role'}
            ]
    context = {
        'form': form
    }
    return render(request, 'register.html', context=context)

def login_view(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    user = CustomUser.get_by_email(
        email=request.POST['emailAddress']
    )

    if user:
        if not user.check_password(request.POST['password']):
            messages.error(request, 'ERROR! Incorrect password!')
            return redirect("login")
    else:
        messages.error(request, 'ERROR! The user does not exist, please sign up!')
        return redirect("login")

    auth.login(request=request, user=user)
    user.is_active = True
    user.save()
    messages.success(request, 'Success! You are logged in!')

    return redirect("home")

def log_out(request):
    logout(request)
    messages.info(request, "Logged out!")
    return redirect("home")


def get_all(request):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "get_users.html", {"users": CustomUser.get_all()})


def user_info(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "get_user_by_id.html", context={"user": CustomUser.get_by_id(id)})


def delete_user(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    CustomUser.delete_by_id(id)
    return redirect("get_users")

def home(request):
    return render(request, "home.html")