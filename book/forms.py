from django import forms
from .models import Book
from author.models import Author
class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Book
        fields = ['name', 'description', 'count']