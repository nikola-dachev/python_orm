import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament,Match
from django.db.models import Count, Q
from main_app.managers import TennisPlayerManager


# Create queries within functions

def get_tennis_players(search_name=None, search_country=None):
    result = []

    if search_name is None and search_country is None:
        return ""

    elif search_name is not None :
        players = TennisPlayer.objects.filter(full_name__icontains=search_name)

    elif search_country is not None:
        players = TennisPlayer.objects.filter(country__icontains=search_country)

    else:
        players = TennisPlayer.objects.filter(Q(full_name__icontains=search_name) & Q(country__icontains=search_country))

    if players:
        players = players.all().order_by('ranking')
        for player in players:
            result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")

        return '\n'.join(result)
    return ''


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()
    if not player:
        return ""

    return f"Top Tennis Player: {player.full_name} with {player.number_of_wins} wins."


def get_tennis_player_by_matches_count():
    top_player = TennisPlayer.objects.annotate(most_matches=Count('matches')).order_by('-most_matches', 'ranking').first()
    if top_player and top_player.most_matches:
        return f"Tennis Player: {top_player.full_name} with {top_player.most_matches} matches played."

    return ''


def get_tournaments_by_surface_type(surface=None):
    result = []
    if surface is None:
        return ""
    tournaments = Tournament.objects.annotate(num_matches=Count('matches')).filter(
        surface_type__icontains=surface).order_by('-start_date')
    if tournaments:
        for tournament in tournaments:
            result.append(
                f"Tournament: {tournament.name}, start date: {tournament.start_date}, matches: {tournament.num_matches}")

        return '\n'.join(result)

    return ""


def get_latest_match_info():
    latest_match = Match.objects.prefetch_related('players').order_by('-date_played', '-id').first()
    if latest_match is None:
        return ""

    players = latest_match.players.order_by('full_name')
    player_one_full_name = players.first().full_name
    player_two_full_name = players.last().full_name
    winner_full_name = latest_match.winner.full_name if latest_match.winner else 'TBA'
    return f"Latest match played on: {latest_match.date_played}, tournament: {latest_match.tournament.name}, score: {latest_match.score}, players: {player_one_full_name} vs {player_two_full_name}, winner: {winner_full_name}, summary: {latest_match.summary}"


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.filter(tournament__name__exact=tournament_name).order_by('-date_played')
    if not matches:
        return "No matches found."

    result = []
    for match in matches:
        winner_full_name = match.winner.full_name if match.winner else 'TBA'
        result.append(f"Match played on: {match.date_played}, score: {match.score}, winner: {winner_full_name}")
    return '\n'.join(result)