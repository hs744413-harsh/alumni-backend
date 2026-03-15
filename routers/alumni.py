from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Alumni

router = APIRouter(prefix="/alumni", tags=["Alumni"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_alumni(name: str, company: str, skills: str, branch: str, batch: int, db: Session = Depends(get_db)):

    alum = Alumni(
        name=name,
        company=company,
        skills=skills,
        branch=branch,
        batch=batch
    )

    db.add(alum)
    db.commit()

    return {"message": "Alumni added successfully"}


@router.get("/")
def get_alumni(db: Session = Depends(get_db)):

    alumni = db.query(Alumni).all()

    return alumni