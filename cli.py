import argparse
import sys
import os
from conf.students_db import SessionLocal  # Importing centralized DB connection
from entity.models import Group, Student, Teacher, Subject, Grade  # noqa: E402

# Open session
session = SessionLocal()

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
parser.add_argument("--id", type=int, help="ID запису для оновлення або видалення")
parser.add_argument("-n", "--name", type=str, help="Ім'я для створення або оновлення")
parser.add_argument("--group_id", type=int, help="ID групи для студента")
parser.add_argument("--teacher_id", type=int, help="ID викладача для предмета")
parser.add_argument("--subject_id", type=int, help="ID предмета")
parser.add_argument("--student_id", type=int, help="ID студента")
parser.add_argument("--grade", type=int, help="Оцінка")

args = parser.parse_args()

def create_entry():
    """Створює новий запис у відповідній моделі"""
    model_mapping = {
        "Group": Group,
        "Student": Student,
        "Teacher": Teacher,
        "Subject": Subject,
        "Grade": Grade,
    }
    model = model_mapping.get(args.model)
    if not model:
        print("❌ Невідома модель")
        return

    entry_data = {k: v for k, v in vars(args).items() if k in model.__table__.columns and v is not None}
    
    new_entry = model(**entry_data)
    session.add(new_entry)
    session.commit()
    print(f"✅ Запис створено: {new_entry}")

def list_entries():
    """Переглядає всі записи моделі у читабельному форматі"""
    model = {
        "Group": Group,
        "Student": Student,
        "Teacher": Teacher,
        "Subject": Subject,
        "Grade": Grade,
    }.get(args.model)

    if model:
        records = session.query(model).all()
        if records:
            for record in records:
                print({k: v for k, v in record.__dict__.items() if k != "_sa_instance_state"})
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
            for attr, value in vars(args).items():
                if value is not None and attr in model.__table__.columns:
                    setattr(entry, attr, value)
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

# Закриваємо сесію після завершення виконання
session.close()
