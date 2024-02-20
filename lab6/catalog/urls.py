from django.urls import path

from catalog.views import (AuthorView, BookListView, BookView,
                           PublisherView, GenreView, SuppliersView)

urlpatterns = [
    path('author/<int:id>', AuthorView.as_view(), name='author'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:id>', BookView.as_view(), name='book'),
    path('publisher/<int:id>', PublisherView.as_view(), name='publisher'),
    path('suppliers/', SuppliersView.as_view(), name='suppliers'),
    path('genre/<int:id>', GenreView.as_view(), name='genre'),
]
