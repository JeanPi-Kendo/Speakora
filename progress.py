from app import db


class Progress(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_email = db.Column(
        db.String(100),
        nullable=False
    )

    language = db.Column(
        db.String(50),
        nullable=False
    )

    level = db.Column(
        db.String(50),
        nullable=False
    )

    word = db.Column(
        db.String(100),
        nullable=False
    )

    score = db.Column(
        db.Integer,
        nullable=False
    )

    attempts = db.Column(
        db.Integer,
        nullable=False
    )
