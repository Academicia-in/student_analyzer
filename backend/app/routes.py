from fastapi import APIRouter, UploadFile, File, Body
from fastapi.responses import FileResponse
import pandas as pd
import shutil
import os
from app.extractor import extract_structured_data
from app.database import SessionLocal
from app.models import StudentMarks
router = APIRouter()

UPLOAD_FOLDER = "uploads"

from app.validator import validate_data

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = extract_structured_data(file_path)

    errors = validate_data(data)

    db = SessionLocal()

    new_record = StudentMarks(
        enrollment_no=data.get("enrollment_no"),
        subject_code="IT0007T",
        co1=data.get("co1"),
        co2=data.get("co2"),
        co3=data.get("co3"),
        co4=data.get("co4"),
        co5=data.get("co5"),
        total=data.get("total"),
        status="REVIEW" if errors else "AUTO",
        errors=",".join(errors) if errors else None
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()

    return {
        "data": data,
        "status": "REVIEW_REQUIRED" if errors else "AUTO_SAVED",
        "errors": errors,
        "record_id": new_record.id
    }

@router.get("/review")
def get_review_data():
    db = SessionLocal()

    records = db.query(StudentMarks).filter(StudentMarks.status=="REVIEW").all()

    db.close()

    return records


@router.put("/review/{record_id}")
def update_record(record_id: int, updated_data: dict = Body(...)):
    db = SessionLocal()

    record = db.query(StudentMarks).filter(StudentMarks.id == record_id).first()

    # 🔥 FIX: access nested data properly
    actual_data = updated_data.get("data", {})

    for key, value in actual_data.items():
        if hasattr(record, key):
            setattr(record, key, value)

    record.status = "AUTO"
    record.errors = None

    db.commit()
    db.refresh(record)   # 🔥 important
    db.close()

    return {"message": "Updated successfully"}


@router.get("/export")
def export_excel():
    db = SessionLocal()

    records = db.query(StudentMarks).filter(StudentMarks.status=="AUTO").all()
    db.close()

    # Convert to list
    data = []
    for r in records:
        data.append({
            "Enrollment No": r.enrollment_no,
            "Subject Code": r.subject_code,
            "CO1": r.co1,
            "CO2": r.co2,
            "CO3": r.co3,
            "CO4": r.co4,
            "CO5": r.co5,
            "Total": r.total,
            "Status": r.status
        })

    df = pd.DataFrame(data)

    file_path = "output.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="result.xlsx")