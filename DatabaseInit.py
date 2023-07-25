import database as db


def InitiallizeDatabase():
   crsr = db.database().cursor()

   crsr.execute("""CREATE TABLE decks (deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
   name VARCHAR(255) DEFAULT "unamed",
   mastered INTEGER NOT NULL DEFAULT 0,
   size INTEGER NOT NULL DEFAULT 0);""")
    
   crsr.execute("""CREATE TABLE cards (c_id INTEGER PRIMARY KEY AUTOINCREMENT,
   deck_id INTEGER NOT NULL REFERENCES decks(deck_id) ON DELETE CASCADE,
   front VARCHAR(255) DEFAULT "front",
   back VARCHAR(255) DEFAULT "back",
   starred BOOLEAN NOT NULL DEFAULT false,
   correctNum INTEGER NOT NULL DEFAULT 0,
   mastered BOOLEAN NOT NULL DEFAULT false
   );""")

   crsr.execute("""CREATE TABLE cardFont 
   (c_id INTEGER PRIMARY KEY REFERENCES cards(c_id) ON DELETE CASCADE, 
   underline_list VARCHAR(255),
   bold_list VARCHAR(255),
   color_list VARCHAR(255)
   );""")


   # underline_list
   #  How it works: 
   #  object type in program: lists with length of 2 (first for start of underline and second for end of underline) inside another list
   #  Structure Example: [ ["1.0", "2.1"] , ["3.4", "5.2"], ... ] 
   #  CASE 1 (When the underline button is pressed and the index at the cursor is not underlined):
   

   crsr.execute("""CREATE TABLE deckStudy (deck_id INTEGER PRIMARY KEY REFERENCES decks(deck_id) ON DELETE CASCADE ON UPDATE CASCADE,
   study_method INTEGER NOT NULL DEFAULT 0,
   study_level INTEGER NOT NULL DEFAULT 0,
   mastery_req INTEGER NOT NULL DEFAULT 3,
   enable_open BOOLEAN NOT NULL DEFAULT True,
   study_starred BOOLEAN NOT NULL DEFAULT false
   );""")

   db.database().commit()