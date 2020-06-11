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

    def is_valid(self):
        if len(self.technologies) == 0:
            return False

        for technology in self.technologies:
            if technology is None:
                return False

        return self.name != '' and self.surname != '' and self.email != ''

    def format(self):
        technologies = [tech.format() for tech in self.technologies]
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'description': self.description,
            'repository_url': self.repository_url,
            'technologies': technologies,
        }

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
    <Reviewer
        id: {self.id},
        name: {self.name},
        surname: {self.surname},
        email: {self.email},
        description: {self.description},
        repository_url = {self.repository_url},
        technologies: {self.technologies}
    >'''


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
