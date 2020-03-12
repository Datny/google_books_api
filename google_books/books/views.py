from django.shortcuts import render, redirect, HttpResponse
from .models import Book
from .forms import BookForm, SearchForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from urllib import parse
import requests as pyt_requests
from django.http import Http404, JsonResponse
from .local_settings import google_api_key
import json


#response = pyt_request.get(f"https://www.googleapis.com/books/v1/volumes?q={encoded_search_term}&maxResults=4&orderBy=relevance&key={google_api_key}")

def add_book_from_google_api(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        data = search_form.cleaned_data['data']
        from_date = search_form.cleaned_data['from_date']
        to_date = search_form.cleaned_data['to_date']
        if data:
            encoded_search_term = parse.quote(data)
            response = pyt_requests.get(f"https://www.googleapis.com/books/v1/volumes?q={encoded_search_term}&maxResults=4&orderBy=relevance&key={google_api_key}")
            json_response = response.json()
            return HttpResponse("Do your job with jsons 1st")

    return render(request, 'books/book_add_from_gapi.html', {'form': search_form})


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


class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_edit.html"
    success_url = reverse_lazy("show_all")

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("show_all")

