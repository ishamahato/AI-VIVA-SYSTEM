# AI Viva

An AI-powered **viva voce (oral examination)** platform. Students answer spoken viva
questions, and the system **transcribes their voice and grades it with AI**, returning a
score out of 10 plus structured feedback. Faculty maintain a question bank and track
student performance through an analytics dashboard.

> This README was reconstructed from two demo screen-recordings of the running app.
> Everything under **Features** is what the app visibly does. The **Tech Stack** section
> mixes confirmed facts with reasonable inferences — items marked *(confirm)* are not
> visible in the recordings and should be verified against the actual code.

---

## Overview

The app has two roles, selected at registration/login:

| Role        | Can do                                                                 |
|-------------|------------------------------------------------------------------------|
| **Student** | Take AI-graded viva sessions, view their score history and feedback    |
| **Faculty** | Manage the question bank, view class-wide analytics                     |

---

## Features

### Authentication
- Register with a role toggle (**Student / Faculty**), full name, email, and password (min 6 characters).
- Login with the same role toggle, email, and password.
- Success toasts: *"Account created. Welcome, &lt;name&gt;!"* / *"Welcome back"*.
- Logout from the top navigation.
- Light/dark theme toggle in the navbar (app shown in dark mode).

### Faculty
- **Faculty Dashboard** with summary stat cards:
  - Total Questions, Total Students, Total Attempts, Average Score (e.g. `3.83/10`).
  - **By Subject** breakdown table: *Subject · Attempts · Avg Score*
    (e.g. Data Structures, Database, Networking, Operating Systems, Programming).
- **Question Bank** (`Manage Questions`) — add a question with:
  - **Subject**
  - **Difficulty** (Easy / Medium / Hard)
  - **Question text**
  - **Model answer / key points** — *"the AI uses this to grade"*
  - **Keywords** (comma separated)
- Existing questions are listed with their *Subject · Difficulty* tag and **Edit / Delete** actions.

### Student
- **Student Dashboard** (`Hi, <name>`) with stat cards:
  - Total Vivas, Average Score (e.g. `4.31/10`), Best Score (e.g. `8/10`).
  - **Recent Attempts** list — each question with its score out of 10.
- **Start New Viva** — a session of **5 questions**.
  - Each question shows its *Subject · Difficulty* and the question text (`Question 1 of 5`).
  - Answers are given **by voice** via a **Start Recording** button (browser asks for microphone permission).
  - After recording: *"Transcribing &amp; grading with AI…"*.
  - **Result screen** per question:
    - Circular **score gauge** out of 10.
    - **Feedback**, **Strengths**, and **To Improve** sections.
    - **Your Answer (transcript)** — the speech-to-text of what was said.
    - **Next Question** to continue.
- **History** page (linked in the navbar) for past attempts.

---

## How grading works (observed behaviour)

1. Student records a spoken answer to a question.
2. The audio is transcribed to text.
3. An AI model grades the transcript against the question's **model answer / keywords**, producing:
   - a numeric score (0–10), and
   - written feedback split into *Feedback / Strengths / To Improve*.

> Example from the demo: a one-word answer ("coding") to a TCP-vs-UDP question
> scored `0.0/10` with feedback explaining it did not address the prompt.

---

## Tech Stack

**Confirmed from the recordings**
- **Frontend dev server:** Vite — the app runs at `http://localhost:5173`.
  (This strongly implies a **React + Vite** single-page app.)
- **Voice capture:** the browser microphone (Web Audio / `getUserMedia` + `MediaRecorder`).
- **AI grading + speech-to-text:** an LLM/transcription pipeline behind the scenes.

**To confirm against the actual code** *(not visible in the demo)*
- Backend framework and language *(confirm)* — an API is required to store users,
  questions, and attempts, and to call the AI/transcription services.
- Database *(confirm)* — e.g. MongoDB / PostgreSQL / SQLite.
- AI provider & model for grading and transcription *(confirm)*.
- Auth mechanism *(confirm)* — e.g. JWT / sessions.

*(Update this section once you confirm the backend, database, and AI provider.)*

---

## Getting Started

> Adjust commands to match the real project layout once confirmed.

### Prerequisites
- Node.js (LTS) and npm / pnpm / yarn
- API keys for the AI / speech-to-text provider *(confirm which)*
- A running backend + database *(confirm)*

### Frontend

```bash
# from the frontend directory
npm install
npm run dev
# opens http://localhost:5173
```

### Backend *(confirm exact commands)*

```bash
# from the backend directory
npm install
npm run dev
```

### Environment variables *(example — replace with the real keys)*

```env
# Frontend
VITE_API_URL=http://localhost:<backend-port>

# Backend
PORT=<backend-port>
DATABASE_URL=<your-database-connection-string>
AI_API_KEY=<your-ai-provider-key>
```

---

## Usage

1. Start the backend and the frontend.
2. Open `http://localhost:5173`.
3. **Register** as Faculty → add questions in the **Question Bank** (set subject,
   difficulty, model answer, and keywords).
4. **Register / log in** as a Student → **Start New Viva** → allow microphone access →
   record each answer → review the AI score and feedback.
5. Track progress on the **Dashboard** (student) and class analytics on the
   **Faculty Dashboard**.

---

## Notes

- The app is microphone-dependent; it must run over `localhost` or HTTPS for the browser
  to grant microphone access.
- Grading quality depends on the **model answer** and **keywords** supplied by faculty for
  each question.

---

*README generated from demo recordings. Please correct any *(confirm)* items so it matches
your actual stack and setup.*
