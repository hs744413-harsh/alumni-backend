from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_job(title: str, company: str, description: str, db: Session = Depends(get_db)):

    job = Job(
        title=title,
        company=company,
        description=description
    )

    db.add(job)
    db.commit()

    return {"message": "Job posted successfully"}


@router.get("/")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(Job).all()

    return jobs