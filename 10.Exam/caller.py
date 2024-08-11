import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut,Spacecraft,Mission
from main_app.custom_manager import AstronautManager
from django.db.models import Q, Count, F


# Create queries within functions


def get_astronauts(search_string=None):
    result = []
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)).order_by('name')
    if not astronauts:
        return ""

    for astronaut in astronauts:
        status = "Active" if astronaut.is_active == True else "Inactive"
        result.append(f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {status}")
    return '\n'.join(result)


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()
    if not astronaut or astronaut.missions_count == 0:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions."


def get_top_commander():
    top_commander = Astronaut.objects.annotate(commander_count=Count('commander_mission')).order_by('-commander_count', 'phone_number').first()

    if not top_commander or top_commander.missions == 0 or top_commander.commander_count == 0:
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.commander_count} commanded missions."


def get_last_completed_mission():
    mission = Mission.objects.select_related('commander', 'spacecraft').prefetch_related('astronauts').filter(status='Completed').order_by('-launch_date').first()

    if not mission:
        return "No data."

    commander_name = mission.commander.name if mission.commander else "TBA"
    all_astronauts = [a.name for a in mission.astronauts.order_by('name')]
    total_spacewalks = sum([a.spacewalks for a in mission.astronauts.all()])
    return f"The last completed mission is: {mission.name}. Commander: {commander_name}. Astronauts: {', '.join(all_astronauts)}. Spacecraft: {mission.spacecraft.name}. Total spacewalks: {total_spacewalks}."

def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(num_missions = Count('missions')).order_by('-num_missions', 'name').first()
    if not spacecraft or spacecraft.num_missions == 0:
        return "No data."

    num_astronauts =Astronaut.objects.filter(missions__spacecraft=spacecraft).distinct().count()
    return f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, used in {spacecraft.num_missions} missions, astronauts on missions: {num_astronauts}."


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects.filter(weight__gte= 200.0, missions__status = "Planned").distinct()
    if not spacecrafts:
        return "No changes in weight."

    num_of_spacecrafts_affected = 0

    for spacecraft in spacecrafts:
        num_of_spacecrafts_affected +=1
        spacecraft.weight -=200.0
        spacecraft.save()

    avg_weight = sum(s.weight for s in spacecrafts)/len(spacecrafts)
    return f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"