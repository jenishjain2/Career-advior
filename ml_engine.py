from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_data import career_data

def ml_recommend_career(user_skills):

    careers = []

    career_skill_texts = []

    # Prepare career skill data

    for career, details in career_data.items():

        careers.append(career)

        skills_text = " ".join(details["skills"])

        career_skill_texts.append(skills_text)

    # Convert user skills to text

    user_text = " ".join(user_skills)

    # Combine all text

    all_texts = career_skill_texts + [user_text]

    # TF-IDF Vectorization

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Compare user with careers

    similarity_scores = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )

    # Prepare results

    results = []

    for i, score in enumerate(similarity_scores[0]):

        results.append({

            "career": careers[i],

            "score": int(score * 100)
        })

    # Sort by best match

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results