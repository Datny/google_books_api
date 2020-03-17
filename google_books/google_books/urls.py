"""google_books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_all_books, name="show_all"),
    path('book/add', views.add_book, name="add"),
    path('book/<int:pk>/update', views.BookUpdate.as_view(), name='edit'),
    path('book/<int:pk>/delete', views.BookDelete.as_view(), name='delete'),
    path('book/add_from_api', views.find_books_using_google_api, name="add_api")

]
