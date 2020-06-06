from app.db import db


class Reviewer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    repository_url = db.Column(db.String(500), nullable=False)
    technologies = db.relationship(
        'Technology',
        secondary='reviewer_technology',
        lazy=False,
        backref=db.backref('reviewers', lazy=True)
    )


reviewer_technology = db.Table(
    'reviewer_technology',
    db.Column(
        'reviewer_id',
        db.Integer,
        db.ForeignKey('reviewer.id'),
        primary_key=True
    ),
    db.Column(
        'technology_id',
        db.Integer,
        db.ForeignKey('technology.id'),
        primary_key=True
    )
)
