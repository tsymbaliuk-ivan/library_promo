import datetime
from itertools import count

from django.core.checks import messages
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from authentication.models import CustomUser
from author.models import Author
from book.models import Book
from order.models import Order


from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm  # Import the BookForm

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            book = form.save()  # Save the Book instance

            # Redirect to a book list page after creation
            return redirect('books')

    else:
        form = BookForm()

    # Retrieve the list of authors to populate the dropdown
    authors = Author.objects.all()

    context = {'form': form, 'authors': authors}
    return render(request, 'book_create.html', context)



def all_books(request):
    if request.user.is_authenticated:
        raw_books = Book.objects.all()
        data = []
        for book in raw_books:
            print(book.authors.all())
            authors = ', '.join([f'{author.name} {author.surname}' for author in book.authors.all()])
            print(authors)
            data.append({'id': book.id,
                         'name': book.name,
                         'description': book.description,
                         'authors': authors,
                         'count': book.count})
        context = {
            'data': data
        }
        return render(request, 'books.html', context=context)
    return redirect("login")


def book_info(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        authors = ', '.join([f'{author.name} {author.surname}' for author in book.authors.all()])
        available = book.count - Order.objects.filter(book=book, end_at=None).count()
        context = {'id': book.id,
                   'name': book.name,
                   'description': book.description,
                   'authors': authors,
                   'count': book.count,
                   'available': available}
        return render(request, 'book_info.html', context=context)
    return redirect("login")


def books_ordered_by_user_id(request, id):
    if request.user.is_authenticated and request.user.role == 1:
        if user := CustomUser.get_by_id(id):
            orders = Order.objects.filter(user=user, end_at=None)
            print(orders)
            return render(request, 'books_ordered.html', {'data': orders})
        else:
            messages.error(request, 'ERROR! No user found')
    return redirect("books")

def book_delete(request, book_id):
    # Get the book object to delete
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST['action']
        if action == 'delete':
            book.delete()

            return redirect('books')

    context = {
        'book': book,
    }
    return render(request, 'book_delete.html', context)

def filter_books():
    return None