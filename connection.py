import db


def start():
    ndb = db.create_database()
    conn = db.getConn()
    return ndb, conn

class Note:
    def __init__(self, id, title, date, tod, tom, gen) -> None:
        self.id = id
        self.title = title
        self.today = tod
        self.tomorrow = tom
        self.general = gen
        self.date = date



