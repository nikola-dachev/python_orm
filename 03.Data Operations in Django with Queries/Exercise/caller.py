import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import fyour models here

from main_app.models import Pet
from main_app.models import Artifact
from main_app.models import Location
from main_app.models import Car
from main_app.models import Task
from main_app.models import HotelRoom
from main_app.models import Character

def create_pet(name, species):
    new_pet = Pet(name = name, species = species)
    new_pet.save()
    return f"{new_pet.name} is a very cute {new_pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    new_artifact = Artifact(name = name, origin = origin, age = age, description = description , is_magical = is_magical)
    new_artifact.save()
    return f"The artifact {new_artifact.name} is {new_artifact.age} years old!"


def delete_all_artifacts():
    all_artifacts = Artifact.objects.all()
    all_artifacts.delete()


def show_all_locations():
    all_locations = Location.objects.all().order_by("-id")
    result = []

    for location in all_locations:
        result.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(result)


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    all_capitals = Location.objects.filter(is_capital=True)
    return all_capitals.values('name')


def delete_first_location():
    first_location = Location.objects.first()
    first_location.delete()


def apply_discount():
    all_cars = Car.objects.all()
    for car in all_cars:
        year_as_string = str(car.year)
        discount = 0

        for char in year_as_string:
            discount += int(char)

        price_after_discount = car.price - (car.price * discount/100)
        car.price_with_discount = price_after_discount
        car.save()


def get_recent_cars():
    searched_cars = Car.objects.filter(year__gte=2020).values("model", "price_with_discount")
    return searched_cars


def delete_last_car():
    last_car = Car.objects.last()
    last_car.delete()


def show_unfinished_tasks():
    incompleted_tasks = Task.objects.filter(is_finished=False)
    result = []

    for task in incompleted_tasks:
        result.append(f"Task - {task.title} needs to be done until {task.due_date}!")

    return '\n'.join(result)


def complete_odd_tasks():
    all_tasks = Task.objects.all()

    for task in all_tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''
    for char in text:
        encoded_text += chr(ord(char) - 3)

    searched_tasks = Task.objects.filter(title=task_title)

    for task in searched_tasks:
        task.description = encoded_text
        task.save()

def get_deluxe_rooms():
    all_rooms = HotelRoom.objects.filter(room_type= "Deluxe")
    result = []

    for room in all_rooms:
        if room.id % 2 == 0:
            result.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")

    return '\n'.join(result)

def increase_room_capacity():
    all_rooms = HotelRoom.objects.all().order_by("id")
    previous_room = None

    for room in all_rooms:
        if room.is_reserved == False:
            continue

        if previous_room:
            room.capacity +=previous_room
        else:
            room.capacity += room.id

        previous_room = room.capacity
        room.save()

def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room():
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved == True:
        last_room.delete()




def update_characters():
    Character.objects.filter(class_name="Mage").update(
        level = F("level") + 3,
        intelligence = F("intelligence") - 7
    )

    Character.objects.fiter(class_name="Warrior").update(
        hit_points = F("hit_points") /2,
        dexterity = F("dexterity") +4
    )

    Character.objects.filter(class_name__in= ["Assassin", "Scout"]).update(
        inventory = "The inventory is empty"
    )


def fuse_characters(first_character, second_character):
    Character.objects.create(
        name=f"{first_character.name} {second_character.name}",
        class_name="Fusion",
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory="Bow of the Elven Lords, Amulet of Eternal Wisdom" if first_character.class_name == "Mage" or first_character.class_name == "Scout" else "Dragon Scale Armor, Excalibur"
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence= 40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    searched_characters = Character.objects.filter(invetory="The inventory is empty")
    searched_characters.delete()


