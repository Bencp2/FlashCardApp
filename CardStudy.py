import database as db
import window as w
import cardMenu as cm
import MainFrame as mf
import TitleLabel as tl
from CardStudySettings import CSS
from FrameApp import FrameApp
from tkinter import *
from CurrentDeck import CDeck
import random
import math

class CS:


    optionsFrame = None
    selectionFrame = None
    cardFrame = None
    cardOptionsFrame = None
    cardNumLabel = None
    flipOrRevealButton = None
    cardNum = 0
    
    flipOrRevealQuestionFrame = None
    flipped = False

    deckStudyInfo = None
    scrollWindow = None
    

    cardDisplays = list()
    cards = list()
    

    crsr = db.database().cursor()


    def createStudyPage():
        CS.scrollWindow = mf.MainFrame(property(lambda: w.window()))
        CS.scrollWindow.pack(fill = BOTH, expand = TRUE)

        CS.selectionFrame = FrameApp(property(lambda: CS.scrollWindow.getAddFrame()))
        CS.selectionFrame.config(bg = '#54a6c4')
        CS.selectionFrame.pack(pady = 30)

        CS.createDefaultData()
        
        CS.createCardList()
        CS.createStudyDisplay()

        CS.createOptionsFrame()




    def createDefaultData():
        CS.deckStudyInfo = CS.crsr.execute("SELECT * FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()

        if CS.deckStudyInfo == None:
            CS.crsr.execute("INSERT INTO deckStudy (deck_id) VALUES (?)", (CDeck.deck[0],))
            db.database().commit()
            CS.deckStudyInfo = CS.crsr.execute("SELECT * FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()


    def createCardList():
        
        match CS.deckStudyInfo[1]:                
            case 0:
                CS.cards = CS.crsr.execute("SELECT * FROM cards WHERE deck_id = " + str(CDeck.deck[0])).fetchall()
            case 1:
                CS.cards = CS.crsr.execute("SELECT * FROM cards WHERE deck_id = " + str(CDeck.deck[0])).fetchall().reverse()
            case 2:
                curList = CS.crsr.execute("SELECT * FROM cards WHERE deck_id = " + str(CDeck.deck[0])).fetchall()
                length = len(curList)
                for n in range(length):
                    card = random.choice(curList)
                    curList.remove(card)
                    CS.cards.append(card)
            case 3:
                CS.cards = CS.crsr.execute("SELECT * FROM cards WHERE deck_id = " + str(CDeck.deck[0]) + " ORDER BY correctNum ASC").fetchall()
            case 4:
                CS.cards = CS.crsr.execute("SELECT * FROM cards WHERE deck_id = " + str(CDeck.deck[0]) + " ORDER BY correctNum DESC").fetchall()


        match CS.deckStudyInfo[2]:
            case 0:
                for card in CS.cards:
                    if card[6]:
                        CS.cards.remove(card)
            case 1:
                for card in CS.cards:
                    if not card[6]:
                        CS.cards.remove(card)
        
        if CS.deckStudyInfo[5]:
            for card in CS.cards:
                if not card[4]:
                    CS.cards.remove(card)

        
        if CS.deckStudyInfo[4]:
            for card in CS.cards:
                if card[5] >= math.ceil((CS.deckStudyInfo[3] * (CS.deckStudyInfo[3] / 2)) / CS.deckStudyInfo[3]):
                    CS.cardDisplays.append(1)
                else:
                    CS.cardDisplays.append(0)
            

    def createStudyDisplay():

        
        CS.cardNumLabel = Label(CS.selectionFrame, text = "1 out of " + str(len(CS.cards)), font = "Arial 20 bold", bg = '#54a6c4')
        CS.cardNumLabel.grid(row = 0, column = 0, pady = 10)

        CS.cardFrame = FrameApp(property(lambda: CS.selectionFrame))
        CS.cardFrame.config(bg = '#54a6c4')
        CS.cardFrame.grid(row = 1, column = 0, pady = 30)
        
        CS.cardOptionsFrame = FrameApp(property(lambda: CS.selectionFrame))
        CS.cardOptionsFrame.config(relief = RIDGE, borderwidth= 5, width = 1000, height = 250)
        CS.cardOptionsFrame.grid(row = 2, column = 0)
        CS.cardOptionsFrame.pack_propagate(False)
        
        CS.flipOrRevealButton = Button(CS.cardOptionsFrame, width = 15, height = 2, font = "Arial 12")
        # CS.flipOrRevealButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = NW)
        CS.flipOrRevealButton.pack(padx = 10, pady = 10, anchor = NW)

        backButton = Button(CS.cardOptionsFrame, width = 15, height = 2, text = "Back", font = "Arial 12", state = DISABLED, command = lambda: CS.viewPreviousCard())
        backButton.pack(padx = 10, pady = 10, side = LEFT, anchor = S)

        fowardButton = Button(CS.cardOptionsFrame, width = 15, height = 2, text = "Foward", font = "Arial 12", command = lambda: CS.viewNextCard())
        # fowardButton.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = SE)
        fowardButton.pack(padx = 10, pady = 10, side = RIGHT, anchor = S)

        if len(CS.cards) <= 1:
            fowardButton.config(state = DISABLED)
        backButton.bind("<Button-1>", lambda event: CS.updateButtons(backButton, fowardButton))
        fowardButton.bind("<Button-1>", lambda event: CS.updateButtons(fowardButton, backButton))

        CS.flipOrRevealQuestionFrame = FrameApp(property(lambda: CS.cardOptionsFrame))
        # CS.flipOrRevealQuestionFrame.grid(row = 1, column = 1, pady = 20)
        CS.flipOrRevealQuestionFrame.pack(anchor = N)

        CS.createCardDisplay()


    def createCardDisplay():

        

        if CS.cardDisplays[CS.cardNum]:
            
            
            CS.flipOrRevealButton.config(text = "Reveal Back", command = lambda: CS.revealBack(), state = ACTIVE)
        else:
            
            cardLabel = Label(CS.cardFrame, text = "Front", font = "Arial 20 bold underline", bg = '#54a6c4')
            cardLabel.grid(row = 0, column = 0)

            cardVisual = Label(CS.cardFrame, text = CS.cards[0][2], width = 52, height = 5, font = "Arial 15", anchor = NW, wraplength= 570, relief= GROOVE, borderwidth= 5, justify= LEFT)
            cardVisual.grid(row = 1, column = 0, pady = 10)

            CS.flipOrRevealButton.config(text = "Flip", command = lambda: CS.flipCard(cardVisual, cardLabel), state = ACTIVE)
            
    def revealBack():
        CS.flipOrRevealButton.config(state = DISABLED)


    def flipCard(cardVisual, cardLabel):
        if cardLabel.cget("text") == "Front":
            cardLabel.config(text = "Back")
            cardVisual.config(text = CS.cards[CS.cardNum][3])
            if not CS.flipped:
                CS.flipped = True
                questionLabel = Label(CS.flipOrRevealQuestionFrame, text = "How did you do?", font = "Arial 12")
                questionLabel.pack(pady = 10)
                correctButton = Button(CS.flipOrRevealQuestionFrame, text = "Correct", width = 15, height = 2, command = lambda: CS.updateCardScore(True))
                correctButton.pack(side = LEFT, padx = 10)
                wrongButton = Button(CS.flipOrRevealQuestionFrame, text = "Incorrect", width = 15, height = 2, command = lambda: CS.updateCardScore(False))
                wrongButton.pack(side = RIGHT, padx = 10)
                

        else:
            cardLabel.config(text = "Front")
            cardVisual.config(text = CS.cards[CS.cardNum][2])
        
    def updateCardScore(user_responce):
        pass

    def viewPreviousCard():
        pass
    
    def viewNextCard():
        pass
    
    def updateButtons(pressedButton, idleButton):
        pass

    def createOptionsFrame():

        CS.optionsFrame = FrameApp(property(lambda: w.window()))
        CS.optionsFrame.config(bg= '#6CB2CC', relief = RIDGE, borderwidth= 3)
        CS.optionsFrame.place(x= 20, y = 120)

        CS.optionsFrame.createOptionsLabel()

        backButton = Button(CS.optionsFrame ,text= "Back to Cards", width=15, height=2, font = "Arial 12", command = lambda: CS.backToCardMenu())
        backButton.grid(row = 1, column= 0, padx = 10, pady = 10)

        settingsButton = Button(CS.optionsFrame ,text= "Settings", width=15, height=2, font = "Arial 12", command = lambda: CS.changeToSettings())
        settingsButton.grid(row = 2, column= 0, padx = 10, pady = 10)
     

    def refreshStudyPage():
        CS.studyPageDestroy()
        CS.createStudyPage()

    def changeToSettings():
        CS.studyPageDestroy()
        CSS.createSettingsPage()

    def studyPageDestroy():
        CS.optionsFrame.destroy()
        # CS.selectionFrame.destroy()
        CS.scrollWindow.destroy()


    def backToCardMenu():
        CS.studyPageDestroy()
        cm.cardMenu.cardMenuCreate()



