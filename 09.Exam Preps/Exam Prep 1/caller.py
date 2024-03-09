import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie
from django.db.models import Q, Count, Avg,F

# Create and run your queries within functions

# def create_data():
#     d1 = Director.objects.create(full_name='Akira Kurosawa')
#     d2 = Director.objects.create(full_name='Francis Ford Coppola', years_of_experience=50)
#     d3 = Director.objects.create(full_name='Martin Scorsese', years_of_experience=60,
#                                  nationality= 'American and Italian')
#
#     a1 = Actor.objects.create(full_name='Al Pacino')
#     a2 = Actor.objects.create(full_name='Robert Duvall')
#     a3 = Actor.objects.create(full_name='Joaquin Phoenix')
#
#     m1 = Movie.objects.create(title='The Godfather', rating=9.9, starring_actor=a1, director=d3,
#                               release_date='1972-01-01')
#     m1.actors.add(a1)
#     m1.actors.add(a2)
#
#     m2 = Movie.objects.create(title='Apocalypse Now', rating=9.5, starring_actor=a1, director=d2,
#                               release_date='1972-01-01')
#     m2.actors.add(a1)
#
# create_data()


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = query_name & query_nationality

    elif search_name is not None:
        query = query_name

    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []

    for director in directors:
        result.append(
            f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")

    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."


def get_top_actor():
    actor = Actor.objects.annotate(movies_count=Count('movies'), avg_rating=Avg('movies__rating')).order_by(
        '-movies_count', 'full_name').first()

    if not actor or not actor.movies_count:
        return ""

    actors_movies = [movie.title for movie in actor.movies.all() if movie]

    return f"Top Actor: {actor.full_name}, starring in movies: {', '.join(actors_movies)}, movies average rating: {actor.avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('movie')).order_by('-num_movies', 'full_name')[:3]

    if not actors or actors[0].num_movies== 0:
        return ""

    result = []

    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    # check if it works if not movies
    if movie is None:
        return ""

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    cast = ', '.join([actor.full_name for actor in movie.actors.order_by('full_name')])

    return f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    new_rating = F('rating') + 0.1
    movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not movies:
        return "No ratings increased."

    num_of_movies_updated = movies.update(rating=new_rating)
    return f"Rating increased for {num_of_movies_updated} movies."

get_actors_by_movies_count()
get_top_rated_awarded_movie()
increase_rating()