from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from authentication.models import CustomUser
from author.models import Author
from abc import ABC
from .forms import AuthorForm  # Import the AuthorForm
from django_ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='5/m', block=True)
def author_id(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "get_author_by_id.html", context={"author": Author.get_by_id(id)})


class AbstractAuthorView(ABC):
    model = Author
    template_name = 'author.html'
    context_object_name = 'authors'
    paginate_by = 10


@ratelimit(key='ip', rate='5/m', block=True)
# class AuthorViewAll(AbstractAuthorView, ListView):
def get_all(request):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "author.html", {"author": Author.get_all()})



@ratelimit(key='ip', rate='5/m', block=True)
def create_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Author created successfully")
            return redirect('all_author')
        else:
            messages.error(request, "Something went wrong")
    else:
        form = AuthorForm()

    return render(request, 'author_form.html', {'form': form})


@ratelimit(key='ip', rate='5/m', block=True)
def delete_author(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("login")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    Author.delete_by_id(id)
    return redirect('all_author')

