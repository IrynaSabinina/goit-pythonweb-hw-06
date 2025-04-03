from sqlalchemy.orm import Session
from sqlalchemy import func
from entity.models import Student, Grade, Subject, Group
from conf.students_db import SessionLocal  # Centralized DB connection

# Open session
session = SessionLocal()

# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    return (
        session.query(Student.name, func.round(func.avg(Grade.grade), 2))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )

# 2. Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_id):
    return (
        session.query(Student.name, func.round(func.avg(Grade.grade), 2))
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )

# 3. Знайти середній бал у групах з певного предмета
def select_3(subject_id):
    return (
        session.query(Group.name, func.round(func.avg(Grade.grade), 2))
        .select_from(Group)
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.name)
        .all()
    )

# 4. Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    return session.query(func.round(func.avg(Grade.grade), 2)).scalar()

# 5. Знайти які курси читає певний викладач
def select_5(teacher_id):
    return (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )

# 6. Знайти список студентів у певній групі
def select_6(group_id):
    return (
        session.query(Student.name).filter(Student.group_id == group_id).all()
    )

# 7. Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_id, subject_id):
    return (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )

# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_id):
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )

# 9. Знайти список курсів, які відвідує певний студент
def select_9(student_id):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )

# 10. Список курсів, які певному студенту читає певний викладач
def select_10(student_id, teacher_id):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(
            Grade.student_id == student_id, Subject.teacher_id == teacher_id
        )
        .distinct()
        .all()
    )

# 11. Середній бал, який певний викладач ставить певному студентові.
def select_11(teacher_id, student_id):
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(
            Subject.teacher_id == teacher_id, Grade.student_id == student_id
        )
        .scalar()
    )

# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті
def select_12(group_id, subject_id):
    latest_date = (
        session.query(func.max(Grade.date_received))
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar()
    )

    return (
        session.query(Student.name, Grade.grade, Grade.date_received)
        .join(Grade, Student.id == Grade.student_id)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == latest_date,
        )
        .all()
    )

# Виконання запитів (тільки якщо запускається напряму)
if __name__ == "__main__":
    print("📌1📌 Топ 5 студентів із найбільшим середнім балом:", select_1())
    print("📌2📌 Студент із найвищим середнім балом з предмета 2:", select_2(2))
    print("📌3📌 Середній бал у групах з предмета 3:", select_3(3))
    print("📌4📌 Середній бал на потоці:", select_4())
    print("📌5📌 Курси викладача 1:", select_5(1))
    print("📌6📌 Студенти у групі 2:", select_6(2))
    print("📌7📌 Оцінки студентів у групі 1 з предмета 3:", select_7(1, 3))
    print("📌8📌 Середній бал викладача 2:", select_8(2))
    print("📌9📌 Курси студента 5:", select_9(5))
    print("📌10📌 Курси студента 4 у викладача 3:", select_10(4, 3))
    print("📌11📌 Середній бал викладача 2 для студента 5:", select_11(2, 5))
    print("📌12📌 Оцінки студентів у групі 1 з предмета 3 на останньому занятті:", select_12(1, 3))

# Закриваємо сесію після завершення виконання
session.close()
