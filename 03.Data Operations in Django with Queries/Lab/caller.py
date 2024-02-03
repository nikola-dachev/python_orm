import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Student


def add_students():
    new_student1 = Student(student_id="FC5204", first_name="John", last_name="Doe", birth_date="1995-05-15",
                           email="john.doe@university.com")
    new_student1.save()
    new_student2 = Student(student_id="FE0054", first_name="Jane", last_name="Smith", email="jane.smith@university.com")
    new_student2.save()
    new_student3 = Student(student_id="FH2014", first_name="Alice", last_name="Johnson", birth_date="1998-02-10",
                           email="alice.johnson@university.com")
    new_student3.save()

    Student.objects.create(student_id="FH2015", first_name="Bob", last_name="Wilson", birth_date="1996-11-25",
                           email="bob.wilson@university.com")


def get_students_info():
    all_students = Student.objects.all()
    result = []

    for student in all_students:
        result.append(
            f"Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}")

    return '\n'.join(result)


def update_students_emails():
    all_students = Student.objects.all()
    for student in all_students:
        new_email = student.email.replace("university.com", "uni-students.com")
        student.email = new_email
        student.save()


def truncate_students():
    all_students = Student.objects.all()
    all_students.delete()




# Create and check models
# Run and print your queries