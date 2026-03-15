from fastapi import APIRouter, UploadFile, File
import shutil
import os

from ai.resume_parser import parse_resume
from ai.resume_classifier import classify_resume
from ai.skill_extractor import extract_skills
from ai.resume_matcher import match_resume_to_mentors
from ai.career_advisor import generate_career_advice

router = APIRouter(prefix="/resume", tags=["Resume AI"])


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # extract resume text
    text = parse_resume(file_path)

    # detect skills
    skills = extract_skills(text)

    # classify resume using ML model
    category = classify_resume(text)

    # find mentors
    mentors = match_resume_to_mentors(skills)

    # generate career advice
    advice = generate_career_advice(category, skills, mentors)

    os.remove(file_path)

    return {
        "resume_category": category,
        "skills_detected": skills,
        "recommended_mentors": mentors,
        "career_advice": advice
    }