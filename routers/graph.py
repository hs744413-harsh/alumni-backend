from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Alumni

router = APIRouter(prefix="/graph", tags=["Graph"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/alumni-network")
def alumni_network(db: Session = Depends(get_db)):

    alumni = db.query(Alumni).all()

    nodes = []
    links = []

    for alum in alumni:

        nodes.append({
            "id": alum.name,
            "group": "alumni",
            "company": alum.company
        })

        # connect alumni to company
        links.append({
            "source": alum.name,
            "target": alum.company
        })

    return {
        "nodes": nodes,
        "links": links
    }