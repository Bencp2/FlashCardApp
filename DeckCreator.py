import database as db
import window as w
from tkinter import *
from tkinter import messagebox
import cardMenu as cm
import TitleLabel as tl
from FrameApp import FrameApp
from EntryApp import EntryApp
import deckMenu as dm
from CurrentDeck import CDeck

class DeckCreator:

    crsr = db.database().cursor()
    mainFrame = None
    optionsFrame = None 
    selectionFrame = None
    nameInput = None
    remainLabel = None
    num = None
    createBool = None

    @staticmethod
    def createDeckCreator(createOrEdit):
        DeckCreator.createBool = createOrEdit

        DeckCreator.mainFrame = FrameApp(property(lambda: w.window()))
        DeckCreator.mainFrame.config(bg = '#4A7A8C')
        DeckCreator.mainFrame.pack(fill = BOTH, expand = TRUE)
        DeckCreator.createOptionsFrame()

        DeckCreator.selectionFrame = FrameApp(property(lambda: DeckCreator.mainFrame))
        DeckCreator.selectionFrame.config(relief = GROOVE, borderwidth = 5)
        DeckCreator.selectionFrame.pack(pady = 30)

        if DeckCreator.createBool:
            deckLabel = Label(DeckCreator.selectionFrame,  text = "Enter name for new deck", font= "Arial 25 bold underline")
        else:
            deckLabel = Label(DeckCreator.selectionFrame,  text = "Edit deck name", font= "Arial 25 bold underline")

        deckLabel.grid(row = 0, column = 0, columnspan= 2, pady = 50)

        DeckCreator.nameInput = EntryApp(property(lambda: DeckCreator.selectionFrame), 80)
        DeckCreator.nameInput = DeckCreator.nameInput.createDeckNameEntry()

        DeckCreator.nameInput.grid(row = 1, column = 0, padx = 20, pady = 5, sticky = S)   

        DeckCreator.remainLabel = Label(DeckCreator.selectionFrame, text = "Remaining Characters: 60", font = "Arial 12")
        DeckCreator.remainLabel.grid(row= 2, column = 0, padx = 20, sticky = NW)
        DeckCreator.nameInput.textVar.trace_add('write', DeckCreator.updateRemaining)
        
        if DeckCreator.createBool:
            subButton = Button(DeckCreator.selectionFrame, text= "Create", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: DeckCreator.inputResponce(DeckCreator.nameInput))
        else:
            subButton = Button(DeckCreator.selectionFrame, text= "Change", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: DeckCreator.inputResponce(DeckCreator.nameInput))

        subButton.grid(row = 1, column = 1, rowspan = 2, padx = 20, pady = 20)
        

    def updateRemaining(*args):
        DeckCreator.num =  60 - len(DeckCreator.nameInput.textVar.get())
        DeckCreator.updateLabel()

    def updateLabel():
        DeckCreator.remainLabel.config(text = "Remaining Characters: " + str(DeckCreator.num))


    def createOptionsFrame():
        DeckCreator.optionsFrame = FrameApp(property(lambda: w.window()))
        DeckCreator.optionsFrame.config(bg= '#6CB2CC', relief = RIDGE, borderwidth= 3)
        DeckCreator.optionsFrame.place(x= 20, y = 120)
        
        DeckCreator.optionsFrame.createOptionsLabel()
        
        if DeckCreator.createBool:
            backButton = Button(DeckCreator.optionsFrame, text= "Back to Decks", width=15, height=2, font = "Arial 12", command = lambda: DeckCreator.backToMenu())
        else:
            backButton = Button(DeckCreator.optionsFrame, text= "Back to Cards", width=15, height=2, font = "Arial 12", command = lambda: DeckCreator.backToMenu())

        backButton.grid(row = 1, column= 0, padx = 10, pady = 10) 

    @staticmethod
    def inputResponce(nameInput):
        name = nameInput.get()
        if DeckCreator.createBool:
            if name == "":
                if messagebox.askokcancel("Create Unamed", "Are you sure you do not want a name?\n The deck will be \"unamed\""):
                    DeckCreator.crsr.execute("INSERT INTO decks DEFAULT VALUES")
                    db.database().commit()
                    DeckCreator.backToMenu()

            else:
                DeckCreator.crsr.execute("INSERT INTO decks (name) VALUES (?)", (name,))
                db.database().commit()
                DeckCreator.backToMenu()
        else:
            DeckCreator.crsr.execute("UPDATE decks SET name= \"" + name + "\" WHERE deck_id = " + str(CDeck.deck[0]))
            db.database().commit()
            CDeck.updateDeck()
            DeckCreator.backToMenu()


    @staticmethod
    def backToMenu():
        DeckCreator.deckCreatorDestroy()
        if DeckCreator.createBool:
            dm.deckMenu.deckMenuCreate()
        else:
            cm.cardMenu.cardMenuCreate()
    

    @staticmethod
    def deckCreatorDestroy():
        DeckCreator.optionsFrame.destroy()
        DeckCreator.mainFrame.destroy()
