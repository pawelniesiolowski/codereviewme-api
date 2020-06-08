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

    def is_valid(self):
        if len(self.technologies) == 0:
            return False

        for technology in self.technologies:
            if technology is None:
                return False

        return (
            self.name != ''
            and self.description != ''
            and self.repository_url != ''
            and self.author_id is not None
        )

    def format(self):
        technologies = [tech.format() for tech in self.technologies]
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'repository_url': self.repository_url,
            'author_id': self.author_id,
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
    <Project
        id: {self.id},
        name: {self.name},
        description: {self.description},
        repository_url: {self.repository_url},
        author_id: {self.author_id},
        technologies: {self.technologies}
    >'''


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
