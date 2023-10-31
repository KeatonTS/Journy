from datetime import date
from connection import Note
from sqlalchemy import delete, insert, select, update

today = date.today()
df = today.strftime("%B %d, %Y")


def createNote(connection, notes, title_answer, today_answer, tom_answer, else_answer):
    connection.execute(insert(notes).
                       values(Title=title_answer,
                              Date=df,
                              Today=today_answer,
                              Tomorrow=tom_answer,
                              General=else_answer))
    connection.commit()


def deleteNote(connection, notes, noteId):
    connection.execute(delete(notes).
                       where(notes.c.note_id == noteId))
    connection.commit()


def updateNote(connection, notes, noteId, title, today, tmrrw, gen):
    connection.execute(update(notes).
                       where(notes.c.note_id == noteId).
                       values(Title=title, Today=today, Tomorrow=tmrrw, General=gen))
    connection.commit()


def readNote(connection, notes, noteId):
    daNote = connection.execute(select(notes.note_id,notes.Date,notes.Today, notes.Tomorrow, notes.General).
                                where(notes.c.note_id == noteId))
    retNote = Note(daNote[0], daNote[1], daNote[2], daNote[3], daNote[4])
    return daNote


def getAllNotes(connection, notes):
    noteList = []
    for row in connection.execute(select(notes)):
        noteList.append(Note(row[0], row[1], row[2], row[3], row[4], row[5]))
    return noteList


def checkExists(connection, notes, noteId):
    daNote = connection.execute(select(notes).
                                where(notes.c.note_id == noteId))
    if (daNote):
        return True
    else:
        return False
