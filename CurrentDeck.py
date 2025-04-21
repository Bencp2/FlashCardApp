import CreateDatabase as cd

class CDeck:

    deck = None
    crsr = cd.Database().cursor()


    def changeDeck(newDeck):
        CDeck.deck = newDeck

    def updateDeck():
        CDeck.deck = CDeck.crsr.execute("SELECT * FROM decks WHERE deck_id = " + str(CDeck.deck[0])).fetchone()