from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    publication_date = models.DateField()
    ISBN_number = models.CharField(max_length=40)
    pages = models.IntegerField()
    pub_language = models.CharField(max_length=40)
    front_cover = models.URLField()

#tytuł, autor, data publikacji, numer ISBN, liczba stron, link do okładki i język publikacji.

