import database as db
import window as w
import sqlite3
from tkinter import *
from tkinter import messagebox
import cardMenu
import MainFrame as mf
import TitleLabel as tl
from FrameApp import FrameApp
import DeckCreator as dc
from CurrentDeck import CDeck

class deckMenu:

    crsr = db.database().cursor()

    optionsFrame = None 
    selectionFrame = None

    scrollWindow = None

    def deckMenuCreate():

        w.window().title('Deck Menu')
        deckMenu.scrollWindow = mf.MainFrame(property(lambda: w.window()))
        deckMenu.scrollWindow.pack(fill = BOTH, expand = TRUE)

        deckMenu.createOptionsFrame()

        deckMenu.selectionFrame = FrameApp(property(lambda: deckMenu.scrollWindow.getAddFrame()))
        deckMenu.selectionFrame.config(bg = '#4A7A8C')
        deckMenu.selectionFrame.pack(pady = 10)

        tl.TitleBar.changeTitle("Deck Menu")

        deckMenu.createDeckSelection()



    def createOptionsFrame():
        deckMenu.optionsFrame = FrameApp(property(lambda: w.window()))
        deckMenu.optionsFrame.config(bg= '#6CB2CC', relief = RIDGE, borderwidth= 3)
        deckMenu.optionsFrame.place(x= 20, y = 120)
        
        deckMenu.optionsFrame.createOptionsLabel()
        
        newDeckButton = Button(deckMenu.optionsFrame ,text= "Create New Deck", width= 15, height=2, font = "Arial 12", command = lambda: deckMenu.changeToDeckCreator())
        newDeckButton.grid(row=1, column = 0, padx = 10, pady= 10)

    def createDeckSelection():

        decks = deckMenu.crsr.execute("SELECT * FROM decks").fetchall()

        if len(decks) == 0:
            existLabel = Label(deckMenu.selectionFrame,  text ="No Decks Exist", height = 10, width = 70, relief= GROOVE, borderwidth= 5)
            existLabel.pack(pady= 10)

        else:
            for deck in decks:
                dFrame = FrameApp(property(lambda: deckMenu.selectionFrame))
                dFrame.config(relief = GROOVE, borderwidth = 5)
                dFrame.pack(fill = BOTH, pady = 15)

                dName = Label(dFrame,  text ="Name: " + deck[1], width = 40, font = "Arial 12 bold", wraplength= 350)
                dName.pack(pady = 10)
                dInfo = Label(dFrame,  text ="Size: " + str(deck[3]) + "\nMastered: " + str(deck[2]), width = 40, anchor= E, justify= LEFT, font = "Arial 12")
                dInfo.pack(padx = 15)

                dUse =  Button(dFrame ,text= "Use", width=20,height=2, bg = '#C3C7C7', command = lambda curDeck = deck: deckMenu.changeToCardMenu(curDeck))
                dUse.pack(side = RIGHT, padx = 10, pady = 10)
                dDel = Button(master= dFrame ,text= "Delete", width=20, height=2, bg = '#C3C7C7', command = lambda curDeck = deck, curFrame = dFrame: deckMenu.deleteDeck(curDeck, curFrame))
                dDel.pack(side = LEFT, padx = 10, pady = 10)

    @staticmethod
    def deleteDeck(deck, dFrame):
        if messagebox.askokcancel("Delete " + deck[1], "Are you sure you do not want to delete " + deck[1] + "?"):
            deckMenu.crsr.execute("DELETE FROM decks WHERE deck_id=" + str(deck[0]))
            db.database().commit()
            dFrame.destroy()
            if len(deckMenu.crsr.execute("SELECT * FROM decks").fetchall()) == 0:
                existLabel = Label(deckMenu.selectionFrame,  text ="No Decks Exist", height = 10, width = 70, relief= GROOVE, borderwidth= 5)
                existLabel.pack(pady= 10)


    @staticmethod
    def backToMenu():
        deckMenu.deckMenuDestroy()
        deckMenu.deckMenuCreate()

    @staticmethod
    def deckMenuDestroy():
        deckMenu.scrollWindow.destroy()

        deckMenu.optionsFrame.destroy()
        # deckMenu.selectionFrame.destroy()

    def changeToDeckCreator():
        deckMenu.deckMenuDestroy()
        dc.DeckCreator.createDeckCreator(True)

    @staticmethod
    def changeToCardMenu(curDeck):
        deckMenu.deckMenuDestroy()
        CDeck.changeDeck(curDeck)
        cardMenu.cardMenu.cardMenuCreate()

        
