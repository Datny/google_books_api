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
from .serializers import change_api_response_to_list_of_book_objects, BookSerializer

from rest_framework import generics
from rest_framework import filters


class BooksApiView(generics.ListAPIView):
    serializer_class = BookSerializer

    # http://127.0.0.1:8000/rest/?data=en&start=2007-02-02&end=2010-01-01
    def get_queryset(self):
        queryset = Book.objects.all()
        data = self.request.query_params.get("data", None)
        start_date = self.request.query_params.get("start", "1000-01-01")
        end_date = self.request.query_params.get("end", "2099-12-12")
        if data is not None:
            queryset = (
                queryset.filter(
                    Q(title__icontains=data)
                    | Q(authors__icontains=data)
                    | Q(pub_language__icontains=data)
                )
                .filter(publication_date__lte=end_date)
                .filter(publication_date__gte=start_date)
            )
        return queryset


def find_books_using_google_api(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        data = search_form.cleaned_data["data"]
        from_date = search_form.cleaned_data["from_date"]
        to_date = search_form.cleaned_data["to_date"]
        if data:
            encoded_search_term = parse.quote(data)
            response = pyt_requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q={encoded_search_term}&maxResults=1&orderBy=relevance&key={google_api_key}"
            )
            json_response = response.json()
            books = change_api_response_to_list_of_book_objects(json_response)
            for book in books:
                if book.publication_date != "unknown":
                    if (
                        book.publication_date > to_date
                        or book.publication_date < from_date
                    ):
                        books.remove(book)
                    book.save()
            return render(
                request,
                "books/book_add_from_gapi.html",
                {"form": search_form, "books": books},
            )

    return render(request, "books/book_add_from_gapi.html", {"form": search_form})


def show_all_books(request):
    books = Book.objects.all()
    form = SearchForm
    add_book_form = BookForm()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["data"].strip()
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
            books = Book.objects.filter(
                Q(title__icontains=query)
                | Q(authors__icontains=query)
                | Q(pub_language__icontains=query)
            )
            books = books.filter(publication_date__lte=to_date).filter(
                publication_date__gte=from_date
            )
            return render(
                request,
                "books/book_show_all.html",
                {
                    "books": books,
                    "search_form": form,
                    "add_book_form": add_book_form,
                    "form_text": query,
                },
            )

    return render(
        request, "books/book_show_all.html", {"books": books, "search_form": form}
    )


def add_book(request):

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add")
        return render(request, "books/book_add.html", {"form": form})

    form = BookForm()
    return render(request, "books/book_add.html", {"form": form})


class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_edit.html"
    success_url = reverse_lazy("show_all")


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("show_all")
