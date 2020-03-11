from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm, SearchForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date

def show_all_books(request):
    books = Book.objects.all()
    form = SearchForm
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
           query = form.cleaned_data['data'].strip()
           from_date = form.cleaned_data['from_date']
           to_date = form.cleaned_data['to_date']
           books = Book.objects.filter(Q(title__icontains=query) | Q(authors__icontains=query) | Q(
               pub_language__icontains=query))
           books = books.filter(publication_date__lte=to_date).filter(publication_date__gte=from_date)

           return render(request, 'books/book_show_all.html', {'books': books,
                                                               'search_form': form,
                                                               'form_text': query})


    return render(request, 'books/book_show_all.html', {'books': books, 'search_form': form})


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('add')
        return render(request, 'books/book_add.html', {'form': form})


    form = BookForm()
    return render(request, 'books/book_add.html', {'form': form})

def add_book_from_google_api(request):
    return render(request, 'books/book_add_from_gapi.html')

class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_edit.html"
    success_url = reverse_lazy("show_all")

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("show_all")

