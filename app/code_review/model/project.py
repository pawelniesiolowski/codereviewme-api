from app.db import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    repository_url = db.Column(db.String(500), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    technologies = db.relationship(
        'Technology',
        secondary='project_technology',
        lazy=False,
        backref=db.backref('projects', lazy=True)
    )


project_technology = db.Table(
    'project_technology',
    db.Column(
        'project_id',
        db.Integer,
        db.ForeignKey('project.id'),
        primary_key=True
    ),
    db.Column(
        'technology_id',
        db.Integer,
        db.ForeignKey('technology.id'),
        primary_key=True
    )
)
