from django.test import TestCase

from books.models import Book
from django.db.models import URLField


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Book.objects.create(
            title="Pancerne Serce",
            authors="Jo Nesbo",
            publication_date="2002-10-10",
            isbn_number="9788324589951",
            pages=450,
            pub_language="pl",
            front_cover="https://s.lubimyczytac.pl/upload/books/240000/240112/335640-352x500.jpg",
        )

    def test_first_name_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("title").verbose_name
        self.assertEquals(field_label, "title")

    def test_first_name_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("isbn_number").max_length
        self.assertEquals(max_length, 60)

    def test_object_url_field_is_type_of_url(self):
        book = Book.objects.get(id=1)
        field_type = book._meta.get_field("front_cover")
        self.assertTrue(isinstance(field_type, URLField))
