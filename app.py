from flask import *

from flask_sqlalchemy import SQLAlchemy

import os

from recommendation import recommend_career

from resume_parser import extract_skills_from_resume

# =========================================
# FLASK CONFIG
# =========================================

app = Flask(__name__)

app.secret_key = "career_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# =========================================
# USER MODEL
# =========================================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(100)
    )

# =========================================
# USER SKILL TRACKER MODEL
# =========================================

class UserSkill(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100)
    )

    skill = db.Column(
        db.String(100)
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

# =========================================
# CREATE DATABASE
# =========================================

with app.app_context():

    db.create_all()

# =========================================
# HOME PAGE
# =========================================

@app.route("/")

def home():

    return redirect("/login")

# =========================================
# REGISTER
# =========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)

def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return "Username already exists"

        new_user = User(

            username=username,

            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# =========================================
# LOGIN
# =========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            session["user"] = username

            return redirect("/dashboard")

        else:

            return "Invalid username or password"

    return render_template("login.html")

# =========================================
# LOGOUT
# =========================================

@app.route("/logout")

def logout():

    session.pop("user", None)

    return redirect("/login")

# =========================================
# DASHBOARD
# =========================================

@app.route(
    "/dashboard",
    methods=["GET", "POST"]
)

def dashboard():

    if "user" not in session:

        return redirect("/login")

    if request.method == "POST":

        skills_input = request.form["skills"]

        domain = request.form["domain"]

        user_skills = [

            skill.strip().lower()

            for skill in skills_input.split(",")
        ]

        results = recommend_career(

            user_skills,

            domain
        )

        return render_template(

            "result.html",

            results=results
        )

    return render_template("dashboard.html")

# =========================================
# RESUME UPLOAD
# =========================================

@app.route(
    "/upload_resume",
    methods=["POST"]
)

def upload_resume():

    if "user" not in session:

        return redirect("/login")

    file = request.files["resume"]

    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        file.filename
    )

    file.save(filepath)

    extracted_skills = extract_skills_from_resume(
        filepath
    )

    results = recommend_career(

        extracted_skills,

        "All"
    )

    return render_template(

        "result.html",

        results=results
    )

# =========================================
# SAVE USER SKILLS
# =========================================

@app.route(
    "/save_skills",
    methods=["POST"]
)

def save_skills():

    username = session["user"]

    completed_skills = request.form.getlist(
        "completed_skills"
    )

    missing_skills = request.form.getlist(
        "missing_skills"
    )

    # DELETE OLD DATA

    UserSkill.query.filter_by(
        username=username
    ).delete()

    # SAVE COMPLETED SKILLS

    for skill in completed_skills:

        new_skill = UserSkill(

            username=username,

            skill=skill,

            completed=True
        )

        db.session.add(new_skill)

    # SAVE MISSING SKILLS

    for skill in missing_skills:

        new_skill = UserSkill(

            username=username,

            skill=skill,

            completed=False
        )

        db.session.add(new_skill)

    db.session.commit()

    return redirect("/tracker")

# =========================================
# SKILL TRACKER
# =========================================

@app.route("/tracker")

def tracker():

    if "user" not in session:

        return redirect("/login")

    username = session["user"]

    skills = UserSkill.query.filter_by(
        username=username
    ).all()

    total = len(skills)

    completed = len(

        [s for s in skills if s.completed]
    )

    progress = 0

    if total > 0:

        progress = int(

            (completed / total) * 100
        )

    return render_template(

        "tracker.html",

        skills=skills,

        progress=progress
    )

# =========================================
# TOGGLE SKILL STATUS
# =========================================

@app.route(
    "/toggle_skill/<int:skill_id>",
    methods=["POST"]
)

def toggle_skill(skill_id):

    skill = UserSkill.query.get(skill_id)

    if skill:

        skill.completed = not skill.completed

        db.session.commit()

    return redirect("/tracker")

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    app.run(debug=True)

