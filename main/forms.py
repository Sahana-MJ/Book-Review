from dataclasses import fields
from django import forms
from .models import *

#books added form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'author', 'description', 'published_year', 'image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'rating')
