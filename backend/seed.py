"""Seed the database with a sample faculty, student, and questions.

Run from the backend/ folder:
    python seed.py

Safe to run multiple times (skips rows that already exist).
"""
from app.database import Base, engine, SessionLocal
from app import models  # noqa: F401  registers all models
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.question import Question
from app.security import hash_password

SAMPLE_QUESTIONS = [
    {
        "subject": "Database",
        "text": "What is database normalization and why is it important?",
        "difficulty": "medium",
        "expected_answer": "Normalization organizes data to reduce redundancy and improve "
        "integrity by dividing tables and defining relationships (1NF, 2NF, 3NF). "
        "It prevents update/insert/delete anomalies.",
        "keywords": "redundancy, integrity, 1NF, 2NF, 3NF, anomalies",
    },
    {
        "subject": "Database",
        "text": "Explain the difference between a primary key and a foreign key.",
        "difficulty": "easy",
        "expected_answer": "A primary key uniquely identifies each row in a table and cannot "
        "be null. A foreign key references the primary key of another table to enforce "
        "referential integrity between tables.",
        "keywords": "primary key, foreign key, unique, referential integrity",
    },
    {
        "subject": "Operating Systems",
        "text": "What is a deadlock and what are its four necessary conditions?",
        "difficulty": "hard",
        "expected_answer": "A deadlock is when processes wait on each other forever. The four "
        "Coffman conditions are mutual exclusion, hold and wait, no preemption, and circular wait.",
        "keywords": "mutual exclusion, hold and wait, no preemption, circular wait",
    },
    {
        "subject": "Operating Systems",
        "text": "Differentiate between a process and a thread.",
        "difficulty": "medium",
        "expected_answer": "A process is an independent program with its own memory space; a "
        "thread is a lightweight unit of execution within a process that shares the process's memory.",
        "keywords": "process, thread, memory, lightweight, execution",
    },
    {
        "subject": "Networking",
        "text": "Explain the difference between TCP and UDP.",
        "difficulty": "medium",
        "expected_answer": "TCP is connection-oriented and reliable with acknowledgements and "
        "ordering; UDP is connectionless, faster, and has no delivery guarantee. TCP suits files, "
        "UDP suits streaming.",
        "keywords": "TCP, UDP, connection-oriented, reliable, connectionless",
    },
    {
        "subject": "Data Structures",
        "text": "What is the time complexity of searching in a balanced binary search tree, and why?",
        "difficulty": "medium",
        "expected_answer": "O(log n), because the tree height is logarithmic and each comparison "
        "halves the remaining search space.",
        "keywords": "O(log n), height, balanced, binary search tree",
    },
    {
        "subject": "Data Structures",
        "text": "Describe how a hash table handles collisions.",
        "difficulty": "hard",
        "expected_answer": "Collisions occur when two keys hash to the same index. Common handling "
        "is chaining (linked lists per bucket) or open addressing (linear/quadratic probing, double hashing).",
        "keywords": "collision, chaining, open addressing, probing, double hashing",
    },
    {
        "subject": "Programming",
        "text": "What is the difference between compile-time and run-time errors? Give an example of each.",
        "difficulty": "easy",
        "expected_answer": "Compile-time errors are caught before execution (e.g. syntax errors). "
        "Run-time errors occur during execution (e.g. dividing by zero, null reference).",
        "keywords": "compile-time, run-time, syntax, exception, division by zero",
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # --- sample faculty ---
        if not db.query(Faculty).filter(Faculty.email == "faculty@viva.test").first():
            db.add(Faculty(
                name="Dr. Sample Faculty",
                email="faculty@viva.test",
                password_hash=hash_password("faculty123"),
            ))
            print("Created faculty: faculty@viva.test / faculty123")

        # --- sample student ---
        if not db.query(Student).filter(Student.email == "student@viva.test").first():
            db.add(Student(
                name="Sample Student",
                email="student@viva.test",
                password_hash=hash_password("student123"),
            ))
            print("Created student: student@viva.test / student123")

        db.commit()

        faculty = db.query(Faculty).filter(Faculty.email == "faculty@viva.test").first()

        # --- sample questions ---
        added = 0
        for q in SAMPLE_QUESTIONS:
            exists = db.query(Question).filter(Question.text == q["text"]).first()
            if not exists:
                db.add(Question(**q, created_by=faculty.id if faculty else None))
                added += 1
        db.commit()
        print(f"Added {added} new question(s). Total: {db.query(Question).count()}")
        print("Seeding complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
