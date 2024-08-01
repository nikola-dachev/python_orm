import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Review, Article
from django.db.models import Q, Count,Avg
# Create queries within functions


def get_authors(search_name=None, search_email=None):
    result = []

    if search_email is None and search_name is None:
        return ""

    if search_email is not None and search_name is not None:
        authors = Author.objects.filter(
            Q(full_name__icontains=search_name) & Q(email__icontains=search_email)).order_by('-full_name')
    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name).order_by('-full_name')

    elif search_email is not None:
        authors = Author.objects.filter(email__icontains=search_email).order_by('-full_name')


    for author in authors:
        check_banned = 'Banned' if author.is_banned else 'Not Banned'
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {check_banned}")

    return '\n'.join(result)


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()
    if author is None or author.num_articles == 0:
        return ""
    return f"Top Author: {author.full_name} with {author.num_articles} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(published_reviews=Count('reviews')).order_by('-published_reviews', 'email').first()
    if author is None or author.published_reviews == 0:
        return ""
    return f"Top Reviewer: {author.full_name} with {author.published_reviews} published reviews."


def get_latest_article():
    last_published_article = Article.objects.prefetch_related('authors', 'reviews').annotate(
        num_reviews=Count('reviews')).order_by('-published_on').first()
    if last_published_article is None:
        return ""

    authors = last_published_article.authors.order_by('full_name')
    authors_list = []
    for author in authors:
        authors_list.append(author.full_name)

    num_reviews = last_published_article.num_reviews
    avg_rating = sum([r.rating for r in last_published_article.reviews.all()]) / num_reviews if num_reviews else 0.00

    return f"The latest article is: {last_published_article.title}. Authors: {', '.join(authors_list)}. Reviewed: {num_reviews} times. Average Rating: {avg_rating:.2f}."


def get_top_rated_article():
    top_article = Article.objects.prefetch_related('reviews').annotate(avg_rating=Avg('reviews__rating')).order_by(
        '-avg_rating', 'title').first()

    if top_article is None or top_article.reviews.count() == 0:
        return ""

    num_reviews = top_article.reviews.count()

    return f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, reviewed {num_reviews} times."


def ban_author(email=None):
    current_author = Author.objects.prefetch_related('reviews').filter(email__exact=email).first()

    if current_author is None or email is None:
        return "No authors banned."

    current_author.is_banned = True
    current_author.save()

    num_reviews = current_author.reviews.count()
    current_author.reviews.all().delete()

    return f"Author: {current_author.full_name} is banned! {num_reviews} reviews deleted."