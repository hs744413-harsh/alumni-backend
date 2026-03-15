from database import SessionLocal
from models import Alumni
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_mentors(query: str):

    db = SessionLocal()

    alumni = db.query(Alumni).all()

    if not alumni:
        return []

    alumni_skills = []
    alumni_data = []

    for alum in alumni:
        if alum.skills:
            alumni_skills.append(alum.skills)
            alumni_data.append(alum)

    # vectorize skills
    vectorizer = CountVectorizer()

    skill_matrix = vectorizer.fit_transform(alumni_skills)

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, skill_matrix)[0]

    results = []

    for idx, score in enumerate(similarities):

        if score > 0.05:
            alum = alumni_data[idx]

            results.append({
                "name": alum.name,
                "company": alum.company,
                "skills": alum.skills,
                "score": float(score)
            })

    db.close()

    # sort by similarity
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:5]