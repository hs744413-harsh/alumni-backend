from pdfminer.high_level import extract_text
import re


def parse_resume(file_path: str):

    text = extract_text(file_path)

    # clean text
    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text