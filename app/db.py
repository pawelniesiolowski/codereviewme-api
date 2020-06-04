from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import reflection
from sqlalchemy.schema import ForeignKeyConstraint, DropConstraint, DropTable


db = SQLAlchemy()


def init_db(app, db):
    db.app = app
    db.init_app(app)


def drop_everything(db):
    # From: http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything
    conn = db.engine.connect()
    trans = conn.begin()
    inspector = reflection.Inspector.from_engine(db.engine)

    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((), (), name=fk['name'])
            )
        t = db.Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()
