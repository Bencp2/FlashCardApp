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
    
    backButton = None
    fowardButton = None

    masteryRemainLabel = None
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
        if len(CS.cards) > 0:
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

        if len(CS.cards) == 0:
            noCardLabel = Label(CS.selectionFrame, text = "No cards exist in deck to study!", width = 53, height = 6, font = "Arial 15", relief= GROOVE, borderwidth= 5)
            noCardLabel.pack(pady = 30)


        match CS.deckStudyInfo[2]:
            case 0:
                for card in CS.cards.copy():
                    if card[6]:
                        CS.cards.remove(card)
                        if len(CS.cards) == 0:
                            noCardLabel = Label(CS.selectionFrame, text = "All cards in this deck are mastered!\n\nTip: Increasing amount of correctness for mastery or reseting cards can make them unmastered", width = 53, height = 6, font = "Arial 15", wraplength = 570, relief= GROOVE, borderwidth= 5)
                            noCardLabel.pack(pady = 30)
            case 1:
                for card in CS.cards.copy():

                    if not card[6]:
                        CS.cards.remove(card)
                        if len(CS.cards) == 0:
                            noCardLabel = Label(CS.selectionFrame, text = "No cards in this deck are mastered!", width = 53, height = 6, font = "Arial 15", relief= GROOVE, borderwidth= 5)
                            noCardLabel.pack(pady = 30)
        

        if CS.deckStudyInfo[5]:
            for card in CS.cards.copy():
                if not card[4]:
                    CS.cards.remove(card)
                    if len(CS.cards) == 0:
                        noCardLabel = Label(CS.selectionFrame, text = "No cards in this deck are starred!", width = 53, height = 6, font = "Arial 15", relief= GROOVE, borderwidth= 5)
                        noCardLabel.pack(pady = 30)

        if CS.deckStudyInfo[4]:
            for card in CS.cards:
                if card[5] >= math.ceil((CS.deckStudyInfo[3] * (CS.deckStudyInfo[3] / 2)) / CS.deckStudyInfo[3]):
                    CS.cardDisplays.append(1)
                else:
                    CS.cardDisplays.append(0)
        else:
            CS.cardDisplays = [0] * len(CS.cards)
                
        
    def createStudyDisplay():

        
        CS.cardNumLabel = Label(CS.selectionFrame, text = "1 out of " + str(len(CS.cards)), font = "Arial 20 bold", bg = '#54a6c4')
        CS.cardNumLabel.grid(row = 0, column = 0, pady = 10)

        CS.cardFrame = FrameApp(property(lambda: CS.selectionFrame))
        CS.cardFrame.config(bg = '#54a6c4')
        CS.cardFrame.grid(row = 1, column = 0, pady = 30)

        CS.cardOptionsFrame = FrameApp(property(lambda: CS.selectionFrame))
        CS.cardOptionsFrame.config(relief = RIDGE, borderwidth= 5, width = 1000, height = 250)
        CS.cardOptionsFrame.grid(row = 2, column = 0)
        CS.cardOptionsFrame.grid_propagate(False)
        
        # CS.flipOrRevealButton = Button(CS.cardOptionsFrame, width = 15, height = 2, font = "Arial 12", background = '#C3C7C7')
        # CS.flipOrRevealButton.grid(row = 0, column = 0, padx = 10, pady = 10)

        CS.backButton = Button(CS.cardOptionsFrame, width = 15, height = 2, text = "Back", font = "Arial 12", background = '#C3C7C7', state = DISABLED, command = lambda: CS.viewPreviousCard())
        CS.backButton.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = SW)


        CS.fowardButton = Button(CS.cardOptionsFrame, width = 15, height = 2, text = "Foward", font = "Arial 12", background = '#C3C7C7', command = lambda: CS.viewNextCard())
        CS.fowardButton.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = SE)

        if len(CS.cards) <= 1:
            CS.fowardButton.config(state = DISABLED)


        CS.flipOrRevealQuestionFrame = FrameApp(property(lambda: CS.cardOptionsFrame))
        questionLabel = Label(CS.flipOrRevealQuestionFrame, text = "How did you do?", font = "Arial 12")
        questionLabel.pack(pady = 10)
        correctButton = Button(CS.flipOrRevealQuestionFrame, text = "Correct", background = '#C3C7C7', width = 15, height = 2)
        wrongButton = Button(CS.flipOrRevealQuestionFrame, text = "Incorrect", background = '#C3C7C7', width = 15, height = 2)

        correctButton.config(command = lambda: CS.updateCardScore(True, correctButton, wrongButton))
        wrongButton.config(command = lambda: CS.updateCardScore(False, correctButton, wrongButton))

        correctButton.pack(side = LEFT, padx = 10)
        wrongButton.pack(side = RIGHT, padx = 10)
        
        for n in range(2):
            if n == 1:
                CS.cardOptionsFrame.grid_columnconfigure(n, weight = 1)
                CS.cardOptionsFrame.grid_rowconfigure(n, weight = 1)
            else:   
                CS.cardOptionsFrame.grid_columnconfigure(n, weight = 0)
                CS.cardOptionsFrame.grid_rowconfigure(n, weight = 0)
        
        CS.masteryRemainLabel = Label(CS.cardOptionsFrame, font = "Arial 12")
        CS.masteryRemainLabel.grid(row = 2, column = 1, pady = 10, padx = 10)
        CS.createCardDisplay()


    def createCardDisplay():            
            if CS.cardDisplays[CS.cardNum]:
                
                CS.selectionFrame.pack_configure(padx = 45, side = RIGHT)
                frontLabel = Label(CS.cardFrame, text = "Front", font = "Arial 20 bold underline", bg = '#54a6c4')
                frontLabel.grid(row = 0, column = 0)
                frontBox = FrameApp(property(lambda: CS.cardFrame))
                frontBox.config(relief= RIDGE, borderwidth= 5)
                frontText = Text(frontBox, font = "Arial 15", width = 52, height = 10, wrap = WORD)
                frontText.insert(END,  CS.cards[CS.cardNum][2])
                frontText.config(state = DISABLED)

                frontScroll = Scrollbar(frontBox)
                frontText.config(yscrollcommand= frontScroll.set)

                frontScroll.config(command= frontText.yview, orient= VERTICAL)
                frontText.pack(side = LEFT)
                frontScroll.pack(side = RIGHT, fill = Y, expand = FALSE)
                frontBox.grid(row = 1, column = 0, padx = 10, pady = 10)


                backResponceLabel = Label(CS.cardFrame, text = "Your Answer", font = "Arial 20 bold underline", bg = '#54a6c4')
                backResponceLabel.grid(row = 0, column = 1)

                backResponceBox = FrameApp(property(lambda: CS.cardFrame))
                backResponceBox.config(relief= RIDGE, borderwidth= 5)

                backResponce = Text(backResponceBox, font = "Arial 15", width = 52, height = 10, wrap = WORD)
                
                backResponceScroll = Scrollbar(backResponceBox)
                backResponce.config(yscrollcommand= backResponceScroll.set)
                backResponceScroll.config(command = backResponce.yview, orient= VERTICAL)
                backResponce.pack(side = LEFT)
                backResponceScroll.pack(side = RIGHT, fill = Y, expand = FALSE)
                backResponceBox.grid(row = 1, column = 1, padx = 10, pady = 10)

                CS.flipOrRevealButton = Button(CS.cardOptionsFrame, width = 15, height = 2, font = "Arial 12", background = '#C3C7C7', text = "Reveal Back", command = lambda: CS.revealBack(backResponce), state = NORMAL)
                CS.flipOrRevealButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = NW)
            else:
                CS.selectionFrame.pack_configure(padx = 0, side = TOP)

                cardLabel = Label(CS.cardFrame, text = "Front", font = "Arial 20 bold underline", bg = '#54a6c4')
                cardLabel.grid(row = 0, column = 0)

                cardVisual = Label(CS.cardFrame, text = CS.cards[CS.cardNum][2], width = 52, font = "Arial 15", anchor = NW, wraplength= 570, relief= GROOVE, borderwidth= 5, justify= LEFT)
                cardVisual.grid(row = 1, column = 0, pady = 10)
                CS.adjustCardVisualHeight(cardVisual)

                CS.flipOrRevealButton = Button(CS.cardOptionsFrame, width = 15, height = 2, font = "Arial 12", background = '#C3C7C7', text = "Flip", command = lambda: CS.flipCard(cardVisual, cardLabel), state = NORMAL)
                CS.flipOrRevealButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = NW)                

    @staticmethod
    def adjustCardVisualHeight(cardVisual):
        visualHeight = int(((cardVisual.winfo_reqheight() - 30)/18) + 1)
        if visualHeight < 10:
            cardVisual.config(height = 10)

    def revealBack(responceText):
        CS.flipOrRevealButton.config(state = DISABLED)
        responceText.config(state = DISABLED)

        backLabel = Label(CS.cardFrame, text = "Back", font = "Arial 20 bold underline", bg = '#54a6c4')
        backLabel.grid(row = 2, column = 0, columnspan = 2)

        backBox = FrameApp(property(lambda: CS.cardFrame))
        backBox.config(relief= RIDGE, borderwidth= 5)

        backText = Text(backBox, font = "Arial 15", width = 52, height = 10, wrap = WORD)
        backText.insert(END,  CS.cards[CS.cardNum][3])
        backText.config(state = DISABLED)

        backScroll = Scrollbar(backBox)
        backText.config(yscrollcommand= backScroll.set)
        backScroll.config(command = backText.yview, orient= VERTICAL)
        backText.pack(side = LEFT)
        backScroll.pack(side = RIGHT, fill = Y, expand = FALSE)
        backBox.grid(row = 3, column = 0, columnspan = 2, pady = 10)
        if not CS.cards[CS.cardNum][6]:
            CS.flipOrRevealQuestionFrame.grid(row = 0, column = 1, rowspan = 2, pady = 20)
        else:
            CS.masteryRemainLabel.config(text = "You already have card mastery!")


    def flipCard(cardVisual, cardLabel):
        if cardLabel.cget("text") == "Front":
            cardLabel.config(text = "Back")
            cardVisual.config(text = CS.cards[CS.cardNum][3])
            CS.adjustCardVisualHeight(cardVisual)

            if not CS.flipped:
                CS.flipped = True
                if not CS.cards[CS.cardNum][6]:
                    CS.flipOrRevealQuestionFrame.grid(row = 0, column = 1, rowspan = 2, pady = 20)
                else:
                    CS.masteryRemainLabel.config(text = "You already have card mastery!")
        else:
            cardLabel.config(text = "Front")
            cardVisual.config(text = CS.cards[CS.cardNum][2])
        
    def updateCardScore(user_responce, cButton, wButton):
        cButton.config(state = DISABLED)
        wButton.config(state = DISABLED)

        if user_responce:
            CS.crsr.execute("UPDATE cards SET correctNum = " + str(CS.cards[CS.cardNum][5] + 1) + " WHERE c_id = " + str(CS.cards[CS.cardNum][0]))
            if (CS.cards[CS.cardNum][5] + 1) >= CS.deckStudyInfo[3]:
                if not CS.cards[CS.cardNum][6]:
                    CS.crsr.execute("UPDATE cards SET mastered = TRUE WHERE c_id = " + str(CS.cards[CS.cardNum][0]))
                    CS.crsr.execute("UPDATE decks SET mastered = " + str(CDeck.deck[2] + 1) + " WHERE deck_id = " + str(CDeck.deck[0]))
                    CDeck.updateDeck()
                CS.masteryRemainLabel.config(text = "You have card mastery!")
            else:
                CS.masteryRemainLabel.config(text = "Amount of correct answers until mastery: " + str(CS.deckStudyInfo[3] - (CS.cards[CS.cardNum][5] + 1)))
        else:
            if (CS.cards[CS.cardNum][5] - 1) < 0:
                CS.masteryRemainLabel.config(text = "Amount of correct answers until mastery: " + str(CS.deckStudyInfo[3] - CS.cards[CS.cardNum][5]))
            elif (CS.cards[CS.cardNum][5]) < CS.deckStudyInfo[3]:
                CS.masteryRemainLabel.config(text = "Amuont of correct answers until mastery: " + str(CS.deckStudyInfo[3] - (CS.cards[CS.cardNum][5] - 1)))
                CS.crsr.execute("UPDATE cards SET correctNum = " + str(CS.cards[CS.cardNum][5] - 1) + " WHERE c_id = " + str(CS.cards[CS.cardNum][0]))
                

        CS.cards[CS.cardNum] = CS.crsr.execute("SELECT * FROM cards WHERE c_id = " + str(CS.cards[CS.cardNum][0])).fetchone()

    def viewPreviousCard():

        for child in CS.cardFrame.winfo_children():
            child.destroy()
        CS.flipped = False
        CS.flipOrRevealQuestionFrame.grid_forget()
        for child in CS.flipOrRevealQuestionFrame.winfo_children():
            if child.cget("text") != "How did you do?":
                child.configure(state = NORMAL)

        CS.masteryRemainLabel.config(text = "")
        CS.cardNum -= 1
        CS.cardNumLabel.config(text = str(CS.cardNum + 1) + " out of " + str(len(CS.cards)))

        CS.fowardButton.config(state = NORMAL)
        if CS.cardNum == 0:
            CS.backButton.config(state = DISABLED)
        CS.flipOrRevealButton.destroy()
        CS.createCardDisplay()

    
    def viewNextCard():

        for child in CS.cardFrame.winfo_children():
            child.destroy()
        CS.flipped = False
        CS.flipOrRevealQuestionFrame.grid_forget()
        for child in CS.flipOrRevealQuestionFrame.winfo_children():
            if child.cget("text") != "How did you do?":
                child.configure(state = NORMAL)

        CS.masteryRemainLabel.config(text = "")
        CS.cardNum += 1
        CS.cardNumLabel.config(text = str(CS.cardNum + 1) + " out of " + str(len(CS.cards)))

        CS.backButton.config(state = NORMAL)
        if CS.cardNum == len(CS.cards) - 1:
            CS.fowardButton.config(state = DISABLED)
        CS.flipOrRevealButton.destroy()

        CS.createCardDisplay()
    


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
        CS.flipped = False
        CS.cardNum = 0
        CS.cardDisplays = list()
        CS.cards = list()
        CS.optionsFrame.destroy()
        # CS.selectionFrame.destroy()
        CS.scrollWindow.destroy()


    def backToCardMenu():
        CS.studyPageDestroy()
        cm.cardMenu.cardMenuCreate()



