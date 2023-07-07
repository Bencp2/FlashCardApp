import database as db
import window as w
import sqlite3
from tkinter import *
from tkinter import messagebox
import cardMenu as cm
import MainFrame as sb
import TitleLabel as tl
from FrameApp import FrameApp
from EntryApp import EntryApp
import deckMenu as dm
import cardMenu as cm
from CurrentDeck import CDeck


class CardCreator:

    
    crsr = db.database().cursor()

    mainFrame = None
    optionsFrame = None 
    selectionFrame = None

    currentCard = None
    createBool = None

    @staticmethod
    def createCardCreator(card, createOrEdit):
        CardCreator.currentCard = card
        CardCreator.createBool = createOrEdit

        CardCreator.mainFrame = FrameApp(property(lambda: w.window()))
        CardCreator.mainFrame.config(bg = '#4A7A8C')
        CardCreator.mainFrame.pack(fill = BOTH, expand = TRUE)


        CardCreator.selectionFrame = FrameApp(property(lambda: CardCreator.mainFrame))
        CardCreator.selectionFrame.config(relief = GROOVE, borderwidth = 5)
        CardCreator.selectionFrame.pack(pady = 30)
        CardCreator.createOptionsFrame()

        if CardCreator.createBool:
            clabel = Label(CardCreator.selectionFrame,  text = "Enter Front and Back for card", font= "Arial 25 bold underline")
        else:
            clabel = Label(CardCreator.selectionFrame,  text = "Edit Front or/and Back for card", font= "Arial 25 bold underline")
        clabel.pack(pady = 50)

        inputFrameGrid = FrameApp(property(lambda: CardCreator.selectionFrame))
        inputFrameGrid.pack(padx = 10, pady = 20)

        frontLabel = Label(inputFrameGrid,  text = "Front", font= "Arial 20 bold", width = 20)
        frontLabel.grid(row = 0, column = 0, pady = 10)

        frontBox = FrameApp(property(lambda: inputFrameGrid))
        frontInput = Text(frontBox, height = 10, width =50, wrap= WORD, font = 'Arial')
        if not CardCreator.createBool:
            frontInput.insert(END, CardCreator.currentCard[2])
        frontInput.pack(side = LEFT)
        frontScroll = Scrollbar(frontBox)
        frontInput.config(yscrollcommand= frontScroll.set)

        frontScroll.config(command= frontInput.yview, orient= VERTICAL)
        frontScroll.pack(side = RIGHT, fill = Y, expand = FALSE)
        frontBox.grid(row = 1, column = 0, padx = 10)



        backLabel = Label(inputFrameGrid,  text = "Back", font= "Arial 20 bold", width = 20)
        backLabel.grid(row = 0, column = 1, pady = 10)
        
        backBox = Frame(master=inputFrameGrid)
        backInput = Text(master= backBox, height =  10, width = 50, wrap= WORD, font = 'Arial')
        if not CardCreator.createBool:
            backInput.insert(END, CardCreator.currentCard[3])

        backInput.pack(side = LEFT)
        backScroll = Scrollbar(backBox )
        backInput.config(yscrollcommand= backScroll.set)
        backScroll.config(command= backInput.yview, orient= VERTICAL)
        backScroll.pack(side = RIGHT, fill = Y, expand = FALSE)

        backBox.grid(row = 1, column = 1, padx = 10)

        if CardCreator.createBool:
            subButton = Button(CardCreator.selectionFrame ,text= "Create", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: CardCreator.inputResponce(frontInput, backInput))
        else:
            subButton = Button(CardCreator.selectionFrame ,text= "Change", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: CardCreator.inputResponce(frontInput, backInput))
        subButton.pack(side = RIGHT, padx = 20, pady = 10)        

    @staticmethod
    def createOptionsFrame():
        CardCreator.optionsFrame = FrameApp(property(lambda: w.window()))
        CardCreator.optionsFrame.config(bg= '#6CB2CC', relief = RIDGE, borderwidth= 3)
        CardCreator.optionsFrame.place(x= 20, y = 120)
        
        CardCreator.optionsFrame.createOptionsLabel()
        
        backButton = Button(CardCreator.optionsFrame, text= "Back to Cards", width=15, height=2, font = "Arial 12", command = lambda: CardCreator.backToMenu())
        backButton.grid(row = 1, column= 0, padx = 10, pady = 10) 

    @staticmethod
    def inputResponce(frontInput, backInput):
        front = frontInput.get(1.0, "end-1c")
        back = backInput.get(1.0, "end-1c")
        if CardCreator.createBool:
            CardCreator.crsr.execute("INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)", (CDeck.deck[0], front, back,))
            CardCreator.crsr.execute("UPDATE decks SET size = " + str(CDeck.deck[3] + 1) + " WHERE deck_id = " + str(CDeck.deck[0]))
            
        else:
            CardCreator.crsr.execute("UPDATE cards SET front = \"" + frontInput.get(1.0, "end-1c") + "\", back = \"" + str(backInput.get(1.0, "end-1c")) + "\" WHERE c_id = " + str(CardCreator.currentCard[0]))
        
        db.database().commit()
        CDeck.updateDeck()

        CardCreator.backToMenu()

    @staticmethod
    def cardCreatorDestroy():
        CardCreator.mainFrame.destroy()
        CardCreator.optionsFrame.destroy()

    def backToMenu():
        CardCreator.cardCreatorDestroy()
        cm.cardMenu.cardMenuCreate()