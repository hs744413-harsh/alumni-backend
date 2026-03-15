from ai.mentor_recommender import recommend_mentors


def match_resume_to_mentors(skills):

    if not skills:
        return []

    query = " ".join(skills)

    mentors = recommend_mentors(query)

    return mentors