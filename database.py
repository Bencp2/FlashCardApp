import sqlite3
import os.path
import DatabaseInit as dbi

class database:
    def __new__(cls):
        if not hasattr(cls, 'instance'): 
            if not os.path.isfile("CardBase.db"):
                cls.instance = sqlite3.connect("CardBase.db")
                dbi.InitiallizeDatabase() 
            else:
                cls.instance = sqlite3.connect("CardBase.db")
                cls.instance.execute("PRAGMA foreign_keys = ON")
        return cls.instance
