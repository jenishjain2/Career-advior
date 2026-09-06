
import pdfplumber

# =========================================
# SKILL LIST
# =========================================

skills_list = [

    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "java",
    "kotlin",
    "flutter",
    "aws",
    "docker",
    "linux",
    "git",
    "statistics",
    "pandas",
    "numpy"
]

# =========================================
# EXTRACT SKILLS
# =========================================

def extract_skills_from_resume(pdf_path):

    text = ""

    # READ PDF

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted.lower()

    # FIND SKILLS

    found_skills = []

    for skill in skills_list:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills
