# Student API

A FastAPI student-records API backed by SQLite, with an optional natural-language query endpoint powered by a local Ollama model.

## Run

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API. The SQLite database (`students.db`) and its `students` table are created automatically on startup.

## Endpoints

- `POST /students` creates a student (`name`, `age`, `course`).
- `GET /students` lists all students; `GET /students/{student_id}` gets one.
- `PUT /students/{student_id}` updates a student; `DELETE /students/{student_id}` removes one.
- `POST /ai/query-students` answers a question using the current student records.

The AI endpoint expects Ollama to be running locally with `llama3.2:1b` available. Install it with `ollama pull llama3.2:1b`. Set `OLLAMA_MODEL` to use a different model.