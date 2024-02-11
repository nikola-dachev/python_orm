import os
from datetime import timedelta, date

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book
from main_app.models import Song, Artist
from main_app.models import Product, Review
from main_app.models import Driver, DrivingLicense
from main_app.models import Registration, Owner, Car


# Create queries within functions
def show_all_authors_with_their_books():
    authors = Author.objects.order_by("id")
    result = []
    for author in authors:

        books = Book.objects.filter(author=author)
        # books = author.book_set.all()

        if not books:
            continue

        titles = ', '.join(book.title for book in books)
        result.append(f"{author.name} has written - {titles}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    all_reviews = product.reviews.all()
    total_rating = sum(r.rating for r in all_reviews)
    average_rating = total_rating/ len(all_reviews)

    return average_rating


def get_reviews_with_high_ratings(threshold: int):
    reviews = Review.objects.filter(rating__gte=threshold)
    return reviews


def get_products_with_no_reviews():
    product = Product.objects.filter(reviews__isnull=True).order_by('-name')
    return product


def delete_products_without_reviews():
    product = Product.objects.filter(reviews__isnull=True)
    product.delete()


def calculate_licenses_expiration_dates():
    driving_licenses = DrivingLicense.objects.order_by('-license_number')
    result = []
    for driving_license in driving_licenses:
        expiration_date = driving_license.issue_date + timedelta(days=365)
        result.append(f"License with id: {driving_license.license_number} expires on {expiration_date}!")
    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date):
    issued_date = due_date - timedelta(days=365)
    drivers = Driver.objects.filter(drivinglicense__issue_date__gt=issued_date)
    return drivers


def register_car_by_owner(owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(owner = owner, registration__isnull=True).first()

    car.owner = owner
    car.registration = registration

    car.save()

    registration.registration_date= date.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."