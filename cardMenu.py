import tkinter
import CreateDatabase as cd
import window as w
import CardStudy
import deckMenu as dm
import MainFrame as mf
import TitleLabel as tl
from CurrentDeck import CDeck
from FrameApp import FrameApp
import DeckCreator as dc
# from CardCreator import CardCreator

class cardMenu:

    crsr = cd.Database().cursor()

    optionsFrame = None 
    selectionFrame = None  
    deckInfoFrame = None  
    deckStatsLabel = None

    scrollWindow = None
    

    @staticmethod
    def cardMenuCreate():
        w.window().title("Card Menu")

        cardMenu.scrollWindow = mf.MainFrame(property(lambda: w.window()))
        cardMenu.scrollWindow.pack(fill = tkinter.BOTH, expand = tkinter.TRUE)

        tl.TitleBar.changeTitle("Card Menu")

        cardMenu.createOptionsFrame()


        cardMenu.selectionFrame = FrameApp(property(lambda: cardMenu.scrollWindow.getAddFrame()))
        cardMenu.selectionFrame.config(bg = '#4A7A8C')
        cardMenu.selectionFrame.pack(pady = 10)

        cardMenu.createDeckInfoLabel()

        cardMenu.createCards()



        

    def createOptionsFrame():

        cardMenu.optionsFrame = FrameApp(property(lambda: w.window()))
        cardMenu.optionsFrame.config(bg = '#6CB2CC', relief = tkinter.RIDGE, borderwidth= 3)
        cardMenu.optionsFrame.place(x= 20, y = 120)

        optionsLabel = tkinter.Label(cardMenu.optionsFrame,  text ="Options", relief= tkinter.FLAT, font= "Arial 15", bg= '#6CB2CC')
        optionsLabel.grid(row = 0, column = 0 ,pady= 20, padx = 10)

        deckMenuButton = tkinter.Button(cardMenu.optionsFrame ,text= "Back to Decks", width= 15, height=2, command = lambda: cardMenu.changeToDeckMenu(), font= "Arial 12")
        deckMenuButton.grid(row=1, column = 0, padx = 10, pady = 10)

        # Change to create new card in current page
        # newCardButton = tkinter.Button(cardMenu.optionsFrame ,text= "Create New Card", width= 15, height=2, font = "Arial 12", command=  lambda: cardMenu.changeToCardCreator(None, True))
        # newCardButton.grid(row=2, column = 0, padx = 10, pady = 10)

        studyPageButton = tkinter.Button(cardMenu.optionsFrame ,text= "Study Cards", width= 15, height=2, font = "Arial 12", command=  lambda: cardMenu.changeToStudyPage())
        studyPageButton.grid(row=3, column = 0, padx = 10, pady = 10)

    def createCards():
        cards = cardMenu.crsr.execute("SELECT * FROM cards WHERE deck_id = " + str(CDeck.deck[0])).fetchall()
        if len(cards) == 0:
            existLabel = tkinter.Label(cardMenu.selectionFrame,  text ="No Cards Exist", height = 10, width = 70, relief= tkinter.GROOVE, borderwidth= 5)
            existLabel.pack(pady= 10)

        else:
            for card in cards:
                cFrame = FrameApp(property(lambda: cardMenu.selectionFrame))
                cFrame.config(relief = tkinter.GROOVE, borderwidth = 5)
                cFrame.pack(fill = tkinter.BOTH, pady = 15)

                buttonFrame = FrameApp(property(lambda: cFrame))
                buttonFrame.pack(fill= tkinter.BOTH)
                cDel = tkinter.Button(buttonFrame, text= "Delete", width=10, height=2, bg = '#C3C7C7', command = lambda card_id = card[0], curFrame = cFrame: cardMenu.deleteCard(card_id, curFrame))
                cDel.pack(side = tkinter.LEFT, padx = 10, pady = 10)

                # Change to edit in current page
                # cEdit = tkinter.Button(buttonFrame, text= "Edit", width=10, height=2, bg = '#C3C7C7', command = lambda curCard = card, type = False: cardMenu.changeToCardCreator(curCard, type))
                # cEdit.pack(side = tkinter.LEFT, padx = 10, pady = 10)


                cStar = tkinter.Button(buttonFrame, text= cardMenu.setStarButton(card[4]), width=10, height=2, bg = '#C3C7C7')
                cStar.configure(command = lambda curCard = card, starButton = cStar: cardMenu.starCard(curCard, starButton))
                cStar.pack(side = tkinter.RIGHT, padx = 10, pady = 10)

                inputFrameGrid = FrameApp(property(lambda: cFrame))
                inputFrameGrid.pack( pady = 20, side = tkinter.BOTTOM)

                frontLabel = tkinter.Label(inputFrameGrid,  text = "Front", font= "Arial 20 bold", width = 20)
                frontLabel.grid(row = 0, column = 0, pady = 10)
                front = tkinter.Label(master= inputFrameGrid, width =50, text= card[2], relief= tkinter.RIDGE, borderwidth=5, anchor= tkinter.NW, justify= tkinter.LEFT, font = "Arial 12", wraplength= 450)

                backLabel = tkinter.Label(inputFrameGrid,  text = "Back", font= "Arial 20 bold", width = 20)
                backLabel.grid(row = 0, column = 1, pady = 10)
                back = tkinter.Label(inputFrameGrid, width = 50, text=  card[3], relief= tkinter.RIDGE, borderwidth=5, anchor= tkinter.NW, justify= tkinter.LEFT, font = "Arial 12", wraplength= 450)

                cardMenu.adjustCardInfoHeight(back, front)
                front.grid(row = 1, column = 0, padx = 5, pady= 10, sticky = tkinter.NSEW)
                back.grid(row = 1, column = 1, padx = 5, pady= 10, sticky = tkinter.NSEW)


    @staticmethod
    def adjustCardInfoHeight(backLabel, frontLabel):
        backHeight = int(((backLabel.winfo_reqheight() - 30)/18) + 1)

        frontHeight = int(((frontLabel.winfo_reqheight() - 30)/18) + 1)
        if (frontHeight <= 10) and (backHeight <= 10):
            backLabel.configure(height = 10)
            frontLabel.configure(height = 10)
        elif (frontHeight > 10) and (frontHeight > backHeight):
            backLabel.configure(height = frontHeight)
        else:
            frontLabel.configure(height = backHeight)



        

    @staticmethod
    def createDeckInfoLabel():
        cardMenu.deckInfoFrame = FrameApp(property(lambda: cardMenu.selectionFrame))
        cardMenu.deckInfoFrame.config(relief= tkinter.RIDGE, borderwidth= 5)
        cardMenu.deckInfoFrame.pack()
        cardMenu.deckInfoFrame.grid_columnconfigure(0, weight = 1)
        cardMenu.deckInfoFrame.grid_columnconfigure(1, weight = 5)

        deckInfoLabel = tkinter.Label(cardMenu.deckInfoFrame, text = "Deck Name:", font= "Arial 20 underline bold", wraplength = 650, pady = 5)
        deckInfoLabel.grid(row = 0, column = 0, columnspan=2)

        deckInfoNameLabel = tkinter.Label(cardMenu.deckInfoFrame, text =  CDeck.deck[1], font= "Arial 15", wraplength = 450, pady = 5, width = 50)
        deckInfoNameLabel.grid(row = 1, column = 0, columnspan=2)

        editNameButton = tkinter.Button(cardMenu.deckInfoFrame, text = "Edit Name", height = 2, width = 15, command = lambda: cardMenu.editDeckName(), bg = '#C3C7C7')
        editNameButton.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = tkinter.W)

        cardMenu.deckStatsLabel = tkinter.Label(cardMenu.deckInfoFrame, text = "Size: " + str(CDeck.deck[3]) + "\nMastered: " + str(CDeck.deck[2]), height = 2, font = "Arial 12", justify= tkinter.LEFT)
        cardMenu.deckStatsLabel.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = tkinter.E)

    @staticmethod
    def setStarButton(card):
        if card:
            return "Unstar"
        else:
            return "Star"

    @staticmethod
    def starCard(curCard, starButton):
        c = cardMenu.crsr.execute("SELECT * FROM cards WHERE c_id = " + str(curCard[0])).fetchone()
        if c[4]:
            starButton.configure(text = "Star")

        else:
            starButton.configure(text = "Unstar")
        cardMenu.crsr.execute("UPDATE cards SET starred = " + str(not c[4]) + " WHERE c_id = " + str(c[0]))
        cd.Database().commit()


    @staticmethod
    def editDeckName():
        cardMenu.cardMenuDestroy()
        dc.DeckCreator.createDeckCreator(False)
        dc.DeckCreator.nameInput.setStartResponce(CDeck.deck[1])



    # def changeToCardCreator(curCard, createBool):
    #     cardMenu.cardMenuDestroy()
    #     CardCreator.createCardCreator(curCard, createBool)
        
    
    @staticmethod
    def deleteCard(card_id, cFrame):
        isMastered = cardMenu.crsr.execute("SELECT mastered from cards WHERE c_id = " + str(card_id)).fetchone()
        cardMenu.crsr.execute("DELETE FROM cards WHERE c_id =" + str(card_id))
        if isMastered:
            cardMenu.crsr.execute("UPDATE decks SET mastered = " + str(CDeck.deck[2] - 1) + " WHERE deck_id = " + str(CDeck.deck[0]))
        cardMenu.crsr.execute("UPDATE decks SET size = " + str(CDeck.deck[3] - 1) + " WHERE deck_id = " + str(CDeck.deck[0]))
        cd.Database().commit()
        cFrame.destroy()
        CDeck.updateDeck()
        cardMenu.deckStatsLabel.config(text = "Size: " + str(CDeck.deck[3]) + "\nMastered: " + str(CDeck.deck[2]))
        if len(cardMenu.crsr.execute("SELECT * FROM cards").fetchall()) == 0:
            existLabel = tkinter.Label(cardMenu.selectionFrame,  text ="No Cards Exist", height = 10, width = 70, relief= tkinter.GROOVE, borderwidth= 5)
            existLabel.pack(pady= 10)            


    @staticmethod
    def refreshMenu():
        cardMenu.cardMenuDestroy()
        cardMenu.cardMenuCreate()

    @staticmethod
    def changeToStudyPage():
        cardMenu.cardMenuDestroy()
        CardStudy.CS.createStudyPage()    

    @staticmethod
    def changeToDeckMenu():
        cardMenu.cardMenuDestroy()
        dm.deckMenu.deckMenuCreate()



    @staticmethod
    def cardMenuDestroy():
        cardMenu.optionsFrame.destroy()
        # cardMenu.selectionFrame.destroy()
        cardMenu.scrollWindow.destroy()
