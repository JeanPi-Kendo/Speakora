from flask import (Blueprint, render_template, request, redirect, url_for)
from app import db
from app.models.user import User
from app.services.audio_service import generate_audio
from app.services.audio_converter import (webm_to_wav)
from app.services.pronunciation_services import (analyze_pronunciation)
from app.models.progress import Progress
import json
import os
import random


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.password == password:

            return redirect(
                url_for("auth.dashboard")
            )

        return "Correo o contraseña incorrectos"

    return render_template(
        "auth/login.html"
    )


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = (
            User.query
            .filter_by(email=email)
            .first()
        )

        if existing_user:

            return (
                "Este correo ya está registrado"
            )

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(
            new_user
        )

        db.session.commit()

        return (
            "Usuario registrado correctamente"
        )

    return render_template(
        "auth/register.html"
    )


@auth.route(
    "/dashboard"
)
def dashboard():

    progress = (
        Progress.query.all()
    )

    completed = len(
        progress
    )

    average_score = 0

    average_attempts = 0

    if completed > 0:
        average_score = (

            sum(

                p.score

                for p in progress

            )

            /

            completed

        )

        average_attempts = (

            sum(

                p.attempts

                for p in progress

            )

            /

            completed

        )

    total_words = 20

    percent = int(

        completed

        /

        total_words

        *

        100

    )

    return render_template(

        "dashboard.html",

        completed=completed,

        average_score=round(
            average_score
        ),

        average_attempts=round(
            average_attempts
        ),

        percent=percent

    )


@auth.route("/profile")
def profile():

    languages = [

        "english",

        "french",

        "german",

        "italian",

        "portuguese"

    ]

    stats = []

    for language in languages:

        progress = (

            Progress.query
            .filter_by(
                language=language
            )
            .all()

        )

        completed = len(
            progress
        )

        avg_score = 0

        avg_attempts = 0

        if completed:

            avg_score = (

                sum(
                    p.score
                    for p in progress
                )

                /

                completed

            )

            avg_attempts = (

                sum(
                    p.attempts
                    for p in progress
                )

                /

                completed

            )

        stats.append({

            "language":
            language,

            "completed":
            completed,

            "score":
            round(
                avg_score
            ),

            "attempts":
            round(
                avg_attempts
            ),

            "percent":
            min(
                completed
                *
                5,

                100

            )

        })

    return render_template(

        "profile.html",

        stats=stats

    )


@auth.route("/practice")
def practice():

    language = request.args.get(
        "language"
    )

    return render_template(
        "practice/select_level.html",
        language=language
    )


@auth.route("/vocabulary")
def vocabulary():
    language = request.args.get("language")
    level = request.args.get("level")
    index = int(request.args.get("index", 0))

    path = f"data/{language}/{level}.json"

    with open(path, "r", encoding="utf-8") as file:
        words = json.load(file)

    # Selecciona 15 palabras aleatorias de las 30
    selected_words = random.sample(words, 15)

    if index >= len(selected_words):
        return render_template("practice/completed.html")

    audio = generate_audio(selected_words[index]["word"])

    return render_template(
        "practice/vocabulary.html",
        word=selected_words[index],
        language=language,
        level=level,
        index=index,
        audio=audio
    )


@auth.route("/pronounce")
def pronounce():

    return render_template(
        "practice/pronounce.html"
    )


@auth.route(
    "/upload-audio",
    methods=["POST"]
)
def upload_audio():

    audio = request.files["audio"]

    word = request.form.get(
        "word",
        "practice"
    )

    folder = (
        "app/uploads/recordings"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    from datetime import datetime

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    filename = (
        f"{word}_{timestamp}.webm"
    )

    path = os.path.join(
        folder,
        filename
    )

    audio.save(
        path
    )

    wav_path = (
        path.replace(
            ".webm",
            ".wav"
        )
    )

    webm_to_wav(
        path,
        wav_path
    )

    result = (
        analyze_pronunciation(
            wav_path,
            word
        )
    )

    score = (
        result["score"]
    )

    attempts = int(

        request.form.get(

            "attempts",

            1

        )

    )

    existing = (

        Progress.query
        .filter_by(

            user_email="demo",

            word=word

        )
        .first()

    )

    if existing:

        if (
            score >
            existing.score
        ):

            existing.score = (
                score
            )

        existing.attempts = (
            attempts
        )

    else:

        new_progress = (

            Progress(

                user_email="demo",

                language="english",

                level="beginner",

                word=word,

                score=score,

                attempts=attempts

            )

        )

        db.session.add(

            new_progress

        )

    db.session.commit()

    return f"""
    Word:
    {word}

    <br><br>

    Spoken:
    {result["spoken"]}

    <br><br>

    Score:
    {score}%
    """


@auth.route("/progress")
def progress():

    data = Progress.query.all()

    result = ""

    for row in data:

        result += (
            f"""
            User: {row.user_email}<br>
            Word: {row.word}<br>
            Score: {row.score}%<br>
            Attempts: {row.attempts}<br>
            <hr>
            """
        )

    return result
