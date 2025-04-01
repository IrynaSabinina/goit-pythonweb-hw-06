import argparse
import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entity.models import Group, Student, Teacher, Subject, Grade  # noqa: E402


# Підключення до бази даних (використовує .env змінні)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:secret@localhost:5432/students_db"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Створення парсера аргументів
parser = argparse.ArgumentParser(description="CLI для роботи з БД")
parser.add_argument(
    "-a",
    "--action",
    choices=["create", "list", "update", "remove"],
    required=True,
    help="Дія: create, list, update, remove",
)
parser.add_argument(
    "-m",
    "--model",
    choices=["Group", "Student", "Teacher", "Subject", "Grade"],
    required=True,
    help="Модель: Group, Student, Teacher, Subject, Grade",
)
parser.add_argument(
    "--id", type=int, help="ID запису для оновлення або видалення"
)
parser.add_argument(
    "-n", "--name", type=str, help="Ім'я для створення або оновлення"
)
parser.add_argument("--group_id", type=int, help="ID групи для студента")
parser.add_argument("--teacher_id", type=int, help="ID викладача для предмета")
parser.add_argument("--subject_id", type=int, help="ID предмета")
parser.add_argument("--student_id", type=int, help="ID студента")
parser.add_argument("--grade", type=int, help="Оцінка")

args = parser.parse_args()


def create_entry():
    """Створює новий запис у відповідній моделі"""
    if args.model == "Group":
        new_entry = Group(name=args.name)
    elif args.model == "Student":
        new_entry = Student(name=args.name, group_id=args.group_id)
    elif args.model == "Teacher":
        new_entry = Teacher(name=args.name)
    elif args.model == "Subject":
        new_entry = Subject(name=args.name, teacher_id=args.teacher_id)
    elif args.model == "Grade":
        new_entry = Grade(
            student_id=args.student_id,
            subject_id=args.subject_id,
            grade=args.grade,
        )
    else:
        print("❌ Невідома модель")
        return
    session.add(new_entry)
    session.commit()
    print(f"✅ Запис створено: {new_entry}")


def list_entries():
    """Переглядає всі записи моделі у читабельному форматі"""
    model_mapping = {
        "Group": Group,
        "Student": Student,
        "Teacher": Teacher,
        "Subject": Subject,
        "Grade": Grade,
    }

    model = model_mapping.get(args.model)

    if model:
        records = session.query(model).all()
        if records:
            for record in records:
                record_dict = record.__dict__
                filtered_dict = {
                    k: v
                    for k, v in record_dict.items()
                    if k != "_sa_instance_state"
                }
                print(filtered_dict)
        else:
            print(f"⚠️ У таблиці {args.model} немає записів.")
    else:
        print("❌ Невідома модель")


def update_entry():
    """Оновлює запис за ID"""
    model = {
        "Group": Group,
        "Student": Student,
        "Teacher": Teacher,
        "Subject": Subject,
        "Grade": Grade,
    }.get(args.model)
    if model and args.id:
        entry = session.query(model).filter_by(id=args.id).first()
        if entry:
            if args.name:
                entry.name = args.name
            if args.group_id:
                entry.group_id = args.group_id
            if args.teacher_id:
                entry.teacher_id = args.teacher_id
            if args.subject_id:
                entry.subject_id = args.subject_id
            if args.student_id:
                entry.student_id = args.student_id
            if args.grade is not None:
                entry.grade = args.grade
            session.commit()
            print(f"✅ Запис оновлено: {entry}")
        else:
            print("❌ Запис не знайдено")
    else:
        print("❌ Невірні параметри")


def remove_entry():
    """Видаляє запис за ID"""
    model = {
        "Group": Group,
        "Student": Student,
        "Teacher": Teacher,
        "Subject": Subject,
        "Grade": Grade,
    }.get(args.model)
    if model and args.id:
        entry = session.query(model).filter_by(id=args.id).first()
        if entry:
            session.delete(entry)
            session.commit()
            print(f"✅ Запис видалено: {entry}")
        else:
            print("❌ Запис не знайдено")
    else:
        print("❌ Невірні параметри")


# Виконання відповідної дії
if args.action == "create":
    create_entry()
elif args.action == "list":
    list_entries()
elif args.action == "update":
    update_entry()
elif args.action == "remove":
    remove_entry()

session.close()
