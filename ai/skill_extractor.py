COMMON_SKILLS = [
    "python",
    "machine learning",
    "data science",
    "deep learning",
    "sql",
    "react",
    "node",
    "ai",
    "nlp",
    "aws",
    "javascript",
    "tensorflow",
    "pytorch"
]


def extract_skills(text: str):

    text = text.lower()

    found_skills = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills