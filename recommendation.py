
from skills_data import career_data

# =========================================
# RECOMMEND CAREER
# =========================================

def recommend_career(user_skills, selected_domain):

    recommendations = []

    # LOWERCASE SKILLS

    user_skills = [

        skill.lower()

        for skill in user_skills
    ]

    # LOOP THROUGH CAREERS

    for career, details in career_data.items():

        domain = details["domain"]

        career_skills = details["skills"]

        # DOMAIN FILTER

        if (

            selected_domain != "All"

            and

            domain.lower() != selected_domain.lower()

        ):

            continue

        # MATCHING

        matched_skills = []

        missing_skills = []
        priority_skills = []

        score = 0

        total_score = sum(
            career_skills.values()
        )

        for skill, weight in career_skills.items():

            if skill.lower() in user_skills:

                matched_skills.append(skill)

                score += weight

            else:

                missing_skills.append(skill)

                # HIGH PRIORITY SKILLS

                if weight >= 15:

                    priority_skills.append(skill)


        # MATCH %

        match_percentage = int(

            (score / total_score) * 100

        )

        # =========================================
        # CAREER ROADMAP
        # =========================================

        roadmap = []

        month = 1

        for skill in missing_skills:

            roadmap.append(

                f"Month {month}: Learn {skill}"
            )

            month += 1

        # FINAL STEP

        roadmap.append(

            f"Month {month}: Build real-world projects"
        )

        roadmap.append(

            f"Month {month+1}: Apply for internships/jobs"
        )

        # LEARNING TIME

        estimated_months = len(missing_skills) * 2

        learning_time = f"{estimated_months} Months"

        # FINAL DATA

        recommendations.append({

            "career": career,

            "domain": domain,

            "match": match_percentage,

            "matched": matched_skills,

            "missing": missing_skills,

            "roadmap": roadmap,

            "learning_time": learning_time
        })

    # SORTING

    recommendations.sort(

        key=lambda x: x["match"],

        reverse=True
    )

    return recommendations
