from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import ai_query, create_student, delete_student, get_students, update_student


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Student API", version="1.0.0", lifespan=lifespan)

app.include_router(create_student.router)
app.include_router(get_students.router)
app.include_router(update_student.router)
app.include_router(delete_student.router)
app.include_router(ai_query.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "docs": "/docs"}