import tkinter as tk
from tkinter import messagebox
from deckMenu import deckMenu as dm
import window as w
import database as db
import TitleLabel as tl

# crsr = db.database().cursor()
# crsr.execute("INSERT INTO deckStudy (deck_id) VALUES (?)", ("29",))

# crsr.execute("DROP TABLE deckStudy")
# crsr.execute("""CREATE TABLE deckStudy (deck_id INTEGER PRIMARY KEY REFERENCES decks(deck_id) ON DELETE CASCADE ON UPDATE CASCADE,
# study_method INTEGER NOT NULL DEFAULT 0,
# study_level INTEGER NOT NULL DEFAULT 0,
# mastery_req INTEGER NOT NULL DEFAULT 3,
# enable_open BOOLEAN NOT NULL DEFAULT false,
# study_starred BOOLEAN NOT NULL DEFAULT false
#  );""")


# db.database().commit()
# db.database().close()



win = w.window()
# def quit_window(icon, item):
#     icon.stop()
#     win.destroy()

# def show_window(icon, item):
#    icon.stop()
#    win.after(0,win.deiconify())   




def callback():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        db.database().commit()
        db.database().close()
        win.destroy()

        

win.protocol("WM_DELETE_WINDOW", callback)

def main():
    tl.TitleBar()
    dm.deckMenuCreate()


main()


win.mainloop()
        





# crsr.execute("DROP TABLE cards")
# crsr.execute("DROP TABLE decks")



# crsr.execute("""CREATE TABLE decks (deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
#  name VARCHAR(255) DEFAULT "unamed",
#  mastered INTEGER NOT NULL DEFAULT 0,
#  size INTEGER NOT NULL DEFAULT 0);""")


# crsr.execute("""CREATE TABLE cards (c_id INTEGER PRIMARY KEY AUTOINCREMENT,
#  deck_id INTEGER NOT NULL REFERENCES decks(deck_id) ON DELETE CASCADE,
#  front VARCHAR(255) DEFAULT "front",
#  back VARCHAR(255) DEFAULT "back",
#  starred BOOLEAN NOT NULL DEFAULT false,
#  correctNum INTEGER NOT NULL DEFAULT 0,
#  mastered BOOLEAN NOT NULL DEFAULT false
#  );""")
#FOREIGN KEY (deck_id) REFERENCES decks(deck_id)
# crsr.execute(sql_command)

# rows = crsr.execute("PRAGMA foreign_keys")
# for r in rows:
#     print(r)

# sql_command = """CREATE TABLE deckToCard (deckID INTEGER NOT NULL,
#  cardID INTEGER NOT NULL,
#  FOREIGN KEY (deckID) REFERENCES decks(deckID),
#  FOREIGN KEY (cardID) REFERENCES cards(cardID));"""
# crsr.execute(sql_command)





# sql_command = """INSERT INTO decks VALUES (1, "deck1", 0, 0);"""

# crsr.execute(sql_command)

# sql_command = """INSERT INTO cards VALUES (1, 1, "card1", "back1", false, 0, false);"""

# crsr.execute(sql_command)

# sql_command = """INSERT INTO decks VALUES (2, "deck2", 0, 0);"""

# crsr.execute(sql_command)



# sql_command = """INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)"""

# crsr.execute("INSERT INTO decks (name) VALUES (?)", ("deck1",))


# crsr.execute("INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)", (4, "front1", "back1"))

# crsr.execute("INSERT INTO decks (name) VALUES (?)", ("deck2",))

# crsr.execute("INSERT INTO decks (name) VALUES (?)", ("deck3",))

# crsr.execute("INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)", (4, "front1", "back1"))

# crsr.execute("DELETE FROM decks where deck_id = 1")


# connection.commit()

# connection.close()

