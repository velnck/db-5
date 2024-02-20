from django.db import models

from users.models import Users


class Books(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    isbn = models.CharField(unique=True, max_length=14)
    title = models.CharField()
    publisher = models.ForeignKey('Publishers', null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    supplier = models.ForeignKey('Suppliers', null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class Authors(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'authors'


class AuthorsBooks(models.Model):
    author = models.OneToOneField('Authors', models.CASCADE, primary_key=True)
    book = models.ForeignKey('Books', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'authors_books'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'book'], name='author_book_unique'
            )
        ]


class Suppliers(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    address = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'suppliers'


class Publishers(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    name = models.CharField(unique=True, max_length=256)
    address = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publishers'


class Genres(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    name = models.CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'genres'


class Reviews(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    review_author = models.ForeignKey(Users, models.CASCADE)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    review_text = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'
