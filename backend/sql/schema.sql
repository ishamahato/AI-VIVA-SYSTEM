-- AI Viva System -- PostgreSQL schema
-- The app also auto-creates these via SQLAlchemy on startup,
-- but this file is the canonical reference / for manual DB init.

CREATE TABLE IF NOT EXISTS students (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(120)  NOT NULL,
    email         VARCHAR(255)  NOT NULL UNIQUE,
    password_hash VARCHAR(255)  NOT NULL,
    created_at    TIMESTAMPTZ   DEFAULT now()
);

CREATE TABLE IF NOT EXISTS faculty (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(120)  NOT NULL,
    email         VARCHAR(255)  NOT NULL UNIQUE,
    password_hash VARCHAR(255)  NOT NULL,
    created_at    TIMESTAMPTZ   DEFAULT now()
);

CREATE TABLE IF NOT EXISTS questions (
    id              SERIAL PRIMARY KEY,
    subject         VARCHAR(120) NOT NULL,
    text            TEXT         NOT NULL,
    difficulty      VARCHAR(20)  DEFAULT 'medium',
    expected_answer TEXT,
    keywords        TEXT,
    created_by      INTEGER      REFERENCES faculty(id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ  DEFAULT now()
);

CREATE TABLE IF NOT EXISTS results (
    id           SERIAL PRIMARY KEY,
    student_id   INTEGER     NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    question_id  INTEGER     REFERENCES questions(id) ON DELETE SET NULL,
    transcript   TEXT,
    score        REAL,
    feedback     TEXT,
    strengths    TEXT,
    improvements TEXT,
    created_at   TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject);
CREATE INDEX IF NOT EXISTS idx_results_student   ON results(student_id);
