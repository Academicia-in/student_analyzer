from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, Base
from app.models import StudentMarks
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Student Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

# Include upload/review/export routes
app.include_router(router)

# Create uploads folder if not exists
os.makedirs("uploads", exist_ok=True)

@app.get("/")
def home():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "message": "Student Analyzer - Database + Upload API working successfully"
        }
    except Exception as e:
        return {
            "error": str(e)
        }
