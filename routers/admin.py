from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Alumni, Job, Event, User

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db)):

    alumni_count = db.query(Alumni).count()
    jobs_count = db.query(Job).count()
    events_count = db.query(Event).count()
    users_count = db.query(User).count()

    return {
        "alumni": alumni_count,
        "jobs": jobs_count,
        "events": events_count,
        "users": users_count
    }