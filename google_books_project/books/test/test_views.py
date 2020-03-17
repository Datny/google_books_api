from django.test import TestCase
from django.urls import reverse

from books.models import Book

class BookUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Book.objects.create(title="Pancerne Serce", authors='Jo Nesbo', publication_date='2002-10-10',
                            isbn_number='9788324589951', pages=450, pub_language='pl',
                            front_cover='https://s.lubimyczytac.pl/upload/books/240000/240112/335640-352x500.jpg')
        Book.objects.create(title="Big Bad Wolf", authors='Jane Doe', publication_date='1999-01-01',
                            isbn_number='1132125162', pages=241, pub_language='en',
                            front_cover='')

    def test_add_book_from_api_url_exists_at_desired_location(self):
        response = self.client.get('/book/add_from_api')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_add.html')

