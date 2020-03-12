from django import forms
from .models import Book
from datetime import date


class BookForm(forms.ModelForm):
    title = forms.CharField(error_messages={'required': 'Please let us know the Title'})
    pages = forms.IntegerField(required=False, min_value=1)  # could be done with Blank =  True in model instead of required
    publication_date = forms.DateField(help_text="YYYY-MM-DD")
    class Meta:
        model = Book
        fields = '__all__'

    def clean_publication_date(self):
        pub_date = self.cleaned_data['publication_date']
        if pub_date > date.today():
            raise forms.ValidationError("Publication date can't be in future")
        return pub_date


class SearchForm(forms.Form):
    data = forms.CharField(max_length=100, required=False, label="What book you are looking for?")
    from_date = forms.DateField(required=False, label="start date:")
    to_date = forms.DateField(required=False, label="end date")

    def clean_data(self):
        return self.cleaned_data['data'].strip()


    def clean_to_date(self):
        to_date = self.cleaned_data['to_date']
        if not to_date:
            to_date = date.max
            return to_date
        else:
            return to_date

    def clean_from_date(self):
        from_date = self.cleaned_data['from_date']
        if not from_date:
            from_date = date.min
            return from_date
        else:
            return from_date



