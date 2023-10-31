import sqlalchemy
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine


engine = create_engine("sqlite+pysqlite:///notes.db", echo=True)
conn = engine.connect()
metadata_obj = sqlalchemy.schema.MetaData()

def create_database():
    notes = Table(
        'notes',
        metadata_obj,
        Column("note_id", Integer, primary_key=True),
        Column("Title", String(25), nullable=False),
        Column("Date", String(250), nullable=False),
        Column("Today", String(250), nullable=False),
        Column("Tomorrow", String(250), nullable=False),
        Column("General", String(1000), nullable=False),
    )

    if not sqlalchemy.inspect(engine).has_table("notes"):
        notes.create(engine)

    return notes

def getConn():
    return conn