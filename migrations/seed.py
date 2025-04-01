import sys
import os
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entity.models import Group, Student, Teacher, Subject, Grade  # noqa: E402

fake = Faker()
engine = create_engine(
    "postgresql://postgres:secret@localhost:5432/students_db"
)
Session = sessionmaker(bind=engine)
session = Session()

# Додаємо групи
groups = [Group(name=f"Group {i}") for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Додаємо викладачів
teachers = [Teacher(name=fake.name()) for _ in range(4)]
session.add_all(teachers)
session.commit()

# Додаємо предмети
subjects = [
    Subject(name=fake.word(), teacher_id=fake.random_int(min=1, max=4))
    for _ in range(7)
]
session.add_all(subjects)
session.commit()

# Додаємо студентів
students = [
    Student(name=fake.name(), group_id=fake.random_int(min=1, max=3))
    for _ in range(30)
]
session.add_all(students)
session.commit()

# Додаємо оцінки
grades = [
    Grade(
        student_id=fake.random_int(min=1, max=30),
        subject_id=fake.random_int(min=1, max=7),
        grade=fake.random_int(min=1, max=10),
    )
    for _ in range(200)
]
session.add_all(grades)
session.commit()

session.close()
