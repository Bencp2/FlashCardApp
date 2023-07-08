import sqlite3

class database:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = sqlite3.connect("CardBase.db")
            cls.instance.execute("PRAGMA foreign_keys = ON")
        return cls.instance
