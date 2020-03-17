from . import models
from datetime import datetime
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'



def change_api_response_to_list_of_book_objects(json_response):
    books = []
    for el in json_response['items']:
        if not el:
           continue
        book = models.Book()
        book.title = el.get('volumeInfo').get('title')
        if el.get('volumeInfo').get('authors'):
            book.authors = ', '.join(map(str, (el.get('volumeInfo').get('authors'))))
        book.pages = el.get('volumeInfo').get('pageCount', 0)
        book.isbn_number = el.get('volumeInfo').get('industryIdentifiers')
        str_isbn = ""
        for isdn in book.isbn_number:
            str_isbn += isdn['type'] + " : " + isdn['identifier'] + " "
        book.isbn_number = str_isbn
        book.pub_language = el['volumeInfo']['language']
        book.front_cover = el.get('volumeInfo', {}).get('imageLinks',{}).get('smallThumbnail', "")
        pub_date = el.get('volumeInfo').get('publishedDate')
        book.publication_date = try_parsing_date(pub_date)
        books.append(book)
    return books


def try_parsing_date(text):
    if not text:
        return "unknown"
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y'):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found')


