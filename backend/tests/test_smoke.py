"""Smoke tests: verify the API boots and the core auth/question/viva wiring works.

Runs against a throwaway SQLite DB and no Gemini key, so it needs no external
services. Run from the backend/ folder:

    pip install pytest
    pytest
"""
import os

# Configure BEFORE importing the app so settings pick these up.
os.environ["DATABASE_URL"] = "sqlite:///./_test_smoke.db"
os.environ["GEMINI_API_KEY"] = ""  # force the "AI not configured" path
os.environ["JWT_SECRET"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True, scope="module")
def _fresh_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("_test_smoke.db"):
        os.remove("_test_smoke.db")


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_full_flow():
    # register faculty
    r = client.post("/api/auth/register", json={
        "name": "Prof Test", "email": "prof@test.com",
        "password": "secret1", "role": "faculty",
    })
    assert r.status_code == 201, r.text
    faculty_token = r.json()["access_token"]
    fac_headers = {"Authorization": f"Bearer {faculty_token}"}

    # faculty creates a question
    r = client.post("/api/questions", headers=fac_headers, json={
        "subject": "Testing", "text": "What is a unit test?",
        "difficulty": "easy", "expected_answer": "A test of a single unit of code.",
        "keywords": "unit, test, isolation",
    })
    assert r.status_code == 201, r.text
    question_id = r.json()["id"]

    # register + login student
    r = client.post("/api/auth/register", json={
        "name": "Stu Test", "email": "stu@test.com",
        "password": "secret1", "role": "student",
    })
    assert r.status_code == 201, r.text
    student_token = r.json()["access_token"]
    stu_headers = {"Authorization": f"Bearer {student_token}"}

    # /me works
    r = client.get("/api/auth/me", headers=stu_headers)
    assert r.status_code == 200
    assert r.json()["role"] == "student"

    # student starts a viva and gets the question back
    r = client.post("/api/viva/start", headers=stu_headers, json={"num_questions": 5})
    assert r.status_code == 200, r.text
    assert len(r.json()["questions"]) >= 1

    # submitting a text answer should return 503 because no Gemini key is set
    r = client.post("/api/viva/answer-text", headers=stu_headers, json={
        "question_id": question_id, "answer_text": "It tests one unit of code.",
    })
    assert r.status_code == 503, r.text

    # role guard: student cannot create questions
    r = client.post("/api/questions", headers=stu_headers, json={
        "subject": "X", "text": "y",
    })
    assert r.status_code == 403
