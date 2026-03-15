from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Event

router = APIRouter(prefix="/events", tags=["Events"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_event(name: str, location: str, date: str, db: Session = Depends(get_db)):

    event = Event(
        name=name,
        location=location,
        date=date
    )

    db.add(event)
    db.commit()

    return {"message": "Event created successfully"}


@router.get("/")
def get_events(db: Session = Depends(get_db)):

    events = db.query(Event).all()

    return events