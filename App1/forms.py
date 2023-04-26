from django import forms

from .models import Upload_Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Upload_Book
        fields= ('title' , 'author','pdfs',"cover")