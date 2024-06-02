# Library
(web application for saving information about authors, readers, and books)

With all information about books, authors and orders stored in one place, you no longer have to sift through hoards of spreadsheets to manually search and enter data. Just enter data once, and use it across all web platform.

#### Librarian can :

- Create,update,delete book and its author. 
- See all users.
- See all orders.

#### Registered users can:

- See all available books and authors.
- Search book.
- Order books.
- See their orders. 

# Setup

#### Create local env file

Just run `make test_env`

## install requirement project's packages

```commandline
pip install -r requirements.txt
```

## Run project

Go to the folder with manage.py file, run library
```commandline
python manage.py migrate 
```

```commandline
python manage.py runserver
```


# library Django web app description

appropriate views and templates for:

auth
* Provide the ability to register the user as a librarian or as an ordinary user (guest)
* Provide the ability to log in (guest)
* Provide the ability to Log out (authorized user)


books  (admin/user)

* show information about all books (admin/user)
* provide an opportunity to view a specific book (admin/user);
* provide the ability to filter books by various criteria (author, title, etc.) (admin/user);
* show all books provided to a specific user (by id) (admin);

users  (admin)

* show information about all users (admin/user)
* provide an opportunity to view a specific user (admin/user)

orders  (admin)

* show information about all orders (admin)
* show information about all my orders (user)
* provide an opportunity to create an order (user)
* provide an opportunity to close the order  (admin)

authors  (admin)

* show information about all authors (admin)
* provide an opportunity to create a new author  (admin)
* provide the ability to remove the author if he is not attached to any book (admin)


# Simple DDoS protection

### To avoid exceeding the limit of requests per page, used the ``ratelimit'' library

The restriction blocks access to the page after a certain number of requests from the same IP address within a short period of time
(in my case rate='5/m' - 5 requests per minute)
the decoration looks like this:
@ratelimit(key='ip', rate='5/m', block=True)

* after exceeding the limit, the user receives a 403 error

more details about it on the official resource:
```commandline
https://pypi.org/project/ratelimit/
```

## User identification verification mechanism - reCAPTCHA

![image](https://github.com/tsymbaliuk-ivan/library_promo/assets/99876130/57b245bd-74a3-4732-9480-f56fd458bc5b)


reCAPTCHA - simple and reliable way. 
All you need is to integrate it into your project :

* Install the django-recaptcha package:
* Add reCAPTCHA keys to your Django settings:
* Modify your register view to validate reCAPTCHA:
* Update your template to include reCAPTCHA:

```commandline
https://pypi.org/project/django-recaptcha/
```
This type of protection is applied during login and creation of a new user
When the form is submitted, the server-side view validates the reCAPTCHA response.
If the reCAPTCHA validation passes, the user is created.

