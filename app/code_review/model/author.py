from app.db import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    technologies = db.relationship(
        'Technology',
        secondary='author_technology',
        lazy=False,
        backref=db.backref('authors', lazy=True)
    )
    projects = db.relationship('Project', backref='author', lazy=True)

    def is_valid(self):
        for technology in self.technologies:
            if technology is None:
                return False
        return self.name != '' and self.surname != '' and self.email != ''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'''
    <Author
        id: {self.id},
        name: {self.name},
        surname: {self.surname},
        email: {self.email},
        description: {self.description},
        technologies: {self.technologies}
        projects: {self.projects}
    >'''


author_technology = db.Table(
    'author_technology',
    db.Column(
        'author_id',
        db.Integer,
        db.ForeignKey('author.id'),
        primary_key=True
    ),
    db.Column(
        'technology_id',
        db.Integer,
        db.ForeignKey('technology.id'),
        primary_key=True
    )
)
