from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from .forms import NewReviewForm
from .models import Books, Reviews, Authors, Publishers, Genres, Suppliers


class BookListView(ListView):
    template_name = 'main-page.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        books = Books.objects.raw('SELECT books.*, ARRAY_TO_JSON(ARRAY_AGG(authors.*)) AS authors FROM books '
                                  'JOIN authors_books ON books.id = authors_books.book_id '
                                  'JOIN authors ON authors_books.author_id = authors.id '
                                  'GROUP BY books.id ORDER BY title;')
        return books


class AuthorView(ListView):
    template_name = 'catalog/author.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        context['author'] = Authors.objects.raw('SELECT * FROM authors '
                                                'WHERE id = %s',
                                                [self.kwargs['id']])
        context['author'] = context['author'][0]
        return context

    def get_queryset(self):
        books = Books.objects.raw('SELECT books.*, ARRAY_TO_JSON(ARRAY_AGG(authors.*)) '
                                  'AS authors FROM books JOIN authors_books '
                                  'ON books.id = authors_books.book_id '
                                  'JOIN authors ON authors_books.author_id = authors.id '
                                  'WHERE EXISTS (SELECT * FROM authors_books '
                                  'WHERE (author_id, book_id) = (%s, books.id)) '
                                  'GROUP BY books.id ORDER BY title;',
                                  [self.kwargs['id']])
        return books


class PublisherView(ListView):
    template_name = 'catalog/publisher.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(PublisherView, self).get_context_data(**kwargs)
        context['publisher'] = Publishers.objects.raw('SELECT * FROM publishers '
                                                      'WHERE id = %s',
                                                      [self.kwargs['id']])
        context['publisher'] = context['publisher'][0]
        return context

    def get_queryset(self):
        books = Books.objects.raw('SELECT books.*, ARRAY_TO_JSON(ARRAY_AGG(authors.*)) '
                                  'AS authors FROM books JOIN authors_books '
                                  'ON books.id = authors_books.book_id '
                                  'JOIN authors ON authors_books.author_id = authors.id '
                                  'WHERE publisher_id = %s '
                                  'GROUP BY books.id ORDER BY title;',
                                  [self.kwargs['id']])
        return books
    

class GenreView(ListView):
    template_name = 'catalog/genre.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(GenreView, self).get_context_data(**kwargs)
        context['genre'] = Genres.objects.raw('SELECT * FROM genres '
                                              'WHERE id = %s',
                                                  [self.kwargs['id']])
        context['genre'] = context['genre'][0]
        return context

    def get_queryset(self):
        books = Books.objects.raw('SELECT books.*, ARRAY_TO_JSON(ARRAY_AGG(authors.*)) '
                                  'AS authors FROM books JOIN authors_books '
                                  'ON books.id = authors_books.book_id '
                                  'JOIN authors ON authors_books.author_id = authors.id '
                                  'WHERE EXISTS (SELECT * FROM genres_books '
                                  'WHERE (genre_id, book_id) = (%s, books.id)) '
                                  'GROUP BY books.id ORDER BY title;',
                                  [self.kwargs['id']])
        return books


@method_decorator(login_required, name='post')
class CreateReviewView(View):
    form_class = NewReviewForm

    def post(self, request, book_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            connection.cursor().execute('CALL add_review(review_author_id_p => %s, '
                                        'book_id_p => %s, '
                                        'review_text_p => %s)',
                                        [request.user.id, book_id,
                                         form.cleaned_data['review_text']])

        return redirect('book', id=book_id)


class BookView(View):
    template_name = 'catalog/book-full.html'
    review_form_class = CreateReviewView.form_class
    create_review_view_class = CreateReviewView

    def get(self, request, id):
        book = Books.objects.raw('SELECT books.*, publishers.name AS publisher_name,'
                                 'ARRAY_TO_JSON(ARRAY_AGG(genres.*)) AS genres_list FROM books '
                                 'JOIN publishers ON books.publisher_id = publishers.id '
                                 'JOIN genres_books ON books.id = genres_books.book_id '
                                 'JOIN genres ON genres_books.genre_id = genres.id '
                                 'WHERE books.id = %s GROUP BY (books.id, publishers.name);', [id])
        if len(book) == 0:
            return HttpResponseNotFound()
        reviews = Reviews.objects.raw('SELECT reviews.id, reviews.review_text, users.username, '
                                      'reviews.review_author_id '
                                      'FROM reviews JOIN users '
                                      'ON reviews.review_author_id = users.id '
                                      'WHERE book_id = %s;', [id])
        authors = Authors.objects.raw('SELECT * FROM authors '
                                      'JOIN authors_books ON authors.id = authors_books.author_id '
                                      'WHERE book_id = %s;', [id])
        return render(request, self.template_name, {
            'book': book[0],
            'authors': authors,
            'reviews': reviews,
            'review_form': self.review_form_class()
        })

    def post(self, request, id):
        return self.create_review_view_class().post(request, id)


class SuppliersView(View):
    template_name = 'catalog/suppliers-list.html'

    def get(self, request):
        if request.user.is_staff:
            suppliers = Suppliers.objects.raw("SELECT * FROM suppliers")
            return render(request, self.template_name,
                          context={
                              'suppliers': list(suppliers),
                          })
        else:
            return HttpResponse('Unauthorized', status=401)
