from django import forms


class BookForm(forms.Form):
    title = forms.CharField(max_length=500)
    authors = forms.CharField(max_length=500)
    publication_date = forms.DateField()
    ISBN_number = forms.CharField(max_length=40)
    pages = forms.IntegerField()
    pub_language = forms.CharField(max_length=40)
    front_cover = forms.URLField()
