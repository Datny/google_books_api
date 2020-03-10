from django.shortcuts import render
from .models import Book
from .forms import BookForm

def show_all(request):
    books = Book.objects.all()
    return render(request, 'show_all.html', {'books': books})


def add_edit(request):
    form = BookForm()
    return render(request, 'add_edit.html', {'form': form})


def add_api(request):
    return render(request, 'add_api.html')

