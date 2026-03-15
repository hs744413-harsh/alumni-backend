from database import SessionLocal
from models import Alumni


def search_alumni(query: str):

    db = SessionLocal()

    query_lower = query.lower()

    alumni_list = db.query(Alumni).all()

    results = []

    for alum in alumni_list:

        text = f"{alum.name} {alum.company} {alum.skills} {alum.branch} {alum.batch}"

        if any(word in text.lower() for word in query_lower.split()):

            results.append({
                "name": alum.name,
                "company": alum.company,
                "skills": alum.skills,
                "branch": alum.branch,
                "batch": alum.batch
            })

    db.close()

    return results[:5]