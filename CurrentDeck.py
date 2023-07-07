import database as db

class CDeck:

    deck = None
    crsr = db.database().cursor()


    def changeDeck(newDeck):
        CDeck.deck = newDeck

    def updateDeck():
        CDeck.deck = CDeck.crsr.execute("SELECT * FROM decks WHERE deck_id = " + str(CDeck.deck[0])).fetchone()