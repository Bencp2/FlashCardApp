import tkinter
import random
import math
import CreateDatabase as cd
import window as w
import CardMenu as cm
import MainFrame as mf
from CardStudySettings import CSS
from FrameApp import FrameApp
from CurrentDeck import CDeck


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

    cardBackHeight = None
    cardFrontHeight = None
    
    statisticsFrame = None
    masteryRemainLabel = None
    flipOrRevealQuestionFrame = None
    flipped = False
    isFlip = False


    deckStudyInfo = None
    scrollWindow = None
    
    masteredStats = 0
    correctStats = None
    incorrectStats = None

    statsLabels = list()
    cardDisplays = list()
    cards = list()
    

    crsr = cd.Database().cursor()


    def createStudyPage():
        CS.scrollWindow = mf.MainFrame(property(lambda: w.window()))
        CS.scrollWindow.pack(fill = tkinter.BOTH, expand = tkinter.TRUE)

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
            cd.Database().commit()
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
            noCardLabel = tkinter.Label(CS.selectionFrame, text = "No cards exist in deck to study!", width = 53, height = 6, font = "Arial 15", relief= tkinter.GROOVE, borderwidth= 5)
            noCardLabel.grid(row = 0, column = 0, pady = 30)


        match CS.deckStudyInfo[2]:
            case 0:
                for card in CS.cards.copy():
                    if card[6]:
                        CS.cards.remove(card)
                        if len(CS.cards) == 0:
                            noCardLabel = tkinter.Label(CS.selectionFrame, text = "All cards in this deck are mastered!\n\nTip: Increasing amount of correctness for mastery or reseting cards can make them unmastered", width = 53, height = 6, font = "Arial 15", wraplength = 570, relief= tkinter.GROOVE, borderwidth= 5)
                            noCardLabel.grid(row = 0, column = 0, pady = 30)
            case 1:
                for card in CS.cards.copy():

                    if not card[6]:
                        CS.cards.remove(card)
                        if len(CS.cards) == 0:
                            noCardLabel = tkinter.Label(CS.selectionFrame, text = "No cards in this deck are mastered!", width = 53, height = 6, font = "Arial 15", relief= tkinter.GROOVE, borderwidth= 5)
                            noCardLabel.grid(row = 0, column = 0, pady = 30)
        

        if CS.deckStudyInfo[5]:
            for card in CS.cards.copy():
                if not card[4]:
                    CS.cards.remove(card)
                    if len(CS.cards) == 0:
                        noCardLabel = tkinter.Label(CS.selectionFrame, text = "No cards in this deck are starred!", width = 53, height = 6, font = "Arial 15", relief= tkinter.GROOVE, borderwidth= 5)
                        noCardLabel.grid(row = 0, column = 0, pady = 30)

        if CS.deckStudyInfo[4]:
            for card in CS.cards:
                if card[5] >= math.ceil((CS.deckStudyInfo[3] * (CS.deckStudyInfo[3] / 2)) / CS.deckStudyInfo[3]):
                    CS.cardDisplays.append(1)
                else:
                    CS.cardDisplays.append(0)
        else:
            CS.cardDisplays = [0] * len(CS.cards)
                
        
    def createStudyDisplay():

        
        CS.cardNumLabel = tkinter.Label(CS.selectionFrame, text = "1 out of " + str(len(CS.cards)), font = "Arial 20 bold", bg = '#54a6c4')
        CS.cardNumLabel.grid(row = 0, column = 0, pady = 10)

        CS.cardFrame = FrameApp(property(lambda: CS.selectionFrame))
        CS.cardFrame.config(bg = '#54a6c4')
        CS.cardFrame.grid(row = 1, column = 0, pady = 30)

        CS.cardOptionsFrame = FrameApp(property(lambda: CS.selectionFrame))
        CS.cardOptionsFrame.config(relief = tkinter.RIDGE, borderwidth= 5, width = 1000, height = 300)
        CS.cardOptionsFrame.grid(row = 2, column = 0)
        CS.cardOptionsFrame.grid_propagate(False)
        
        # CS.flipOrRevealButton = tkinter.Button(CS.cardOptionsFrame, width = 15, height = 2, font = "Arial 12", background = '#C3C7C7')
        # CS.flipOrRevealButton.grid(row = 0, column = 0, padx = 10, pady = 10)

        CS.backButton = tkinter.Button(CS.cardOptionsFrame, width = 15, height = 2, text = "Back", font = "Arial 12", background = '#C3C7C7', state = tkinter.DISABLED, command = lambda: CS.viewPreviousCard())
        CS.backButton.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = tkinter.SW)


        CS.fowardButton = tkinter.Button(CS.cardOptionsFrame, width = 15, height = 2, text = "Foward", font = "Arial 12", background = '#C3C7C7', command = lambda: CS.viewNextCard())
        CS.fowardButton.grid(row = 2, column = 3, padx = 10, pady = 10, sticky = tkinter.SE)

        if len(CS.cards) <= 1:
            CS.fowardButton.config(state = tkinter.DISABLED)


        CS.flipOrRevealQuestionFrame = FrameApp(property(lambda: CS.cardOptionsFrame))
        questionLabel = tkinter.Label(CS.flipOrRevealQuestionFrame, text = "How did you do?", font = "Arial 12")
        questionLabel.pack(pady = 10)
        correctButton = tkinter.Button(CS.flipOrRevealQuestionFrame, text = "Correct", background = '#C3C7C7', width = 15, height = 2)
        wrongButton = tkinter.Button(CS.flipOrRevealQuestionFrame, text = "Incorrect", background = '#C3C7C7', width = 15, height = 2)

        correctButton.config(command = lambda: CS.updateCardScore(True, correctButton, wrongButton))
        wrongButton.config(command = lambda: CS.updateCardScore(False, correctButton, wrongButton))

        correctButton.pack(side = tkinter.LEFT, padx = 10)
        wrongButton.pack(side = tkinter.RIGHT, padx = 10)
        
        rowAndColumnConfiguration = [[0, 0], [1, 0], [0, 1], [0, 0]]
        count = 0
        for row_column in rowAndColumnConfiguration:
            CS.cardOptionsFrame.grid_rowconfigure(count, weight = row_column[0])
            CS.cardOptionsFrame.grid_columnconfigure(count, weight = row_column[1])
            count += 1

        reshuffleButton = tkinter.Button(CS.cardOptionsFrame, text= "Reshuffle", font = "Arial 12", background = '#C3C7C7', width = 15, height = 2, command = lambda: CS.refreshStudyPage())
        reshuffleButton.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = tkinter.NW)

        CS.masteryRemainLabel = tkinter.Label(CS.cardOptionsFrame, font = "Arial 12")
        CS.masteryRemainLabel.grid(row = 2, column = 2, pady = 10, padx = 10)


        CS.createCardDisplay()
        if CS.deckStudyInfo[2] != 1:
            CS.createStatsDisplay()

    # def reshuffleCards():
        
    #     CS.isFlip = False
    #     CS.cardNum = 0
    #     CS.cards = list()
    #     for label in CS.statsLabels:
    #         label.destroy()
    #     CS.statsLabels = list()
    #     CS.cardDisplays = list()
    #     for child in CS.cardFrame.winfo_children():
    #         child.destroy()
    #     CS.flipped = False
    #     CS.flipOrRevealQuestionFrame.grid_forget()
    #     for child in CS.flipOrRevealQuestionFrame.winfo_children():
    #         if child.cget("text") != "How did you do?":
    #             child.configure(state = tkinter.NORMAL)
    #     CS.masteryRemainLabel.config(text = "")
       

    #     CS.backButton.config(state = tkinter.DISABLED)
    #     CS.flipOrRevealButton.destroy()
    #     CS.createCardList()
    #     CS.cardNumLabel.config(text = "1 out of " + str(len(CS.cards)))
    #     if len(CS.cards) > 1:
    #         CS.fowardButton.config(state = tkinter.NORMAL)
    #     else:
    #         CS.fowardButton.config(state = tkinter.DISABLED)
    #     CS.createStatsDisplay()
    #     if len(CS.cards) > 0:
    #         CS.createCardDisplay()
    #     else:
    #         CS.cardNumLabel.destroy()
    #         CS.cardOptionsFrame.destroy()
    #         CS.cardFrame.destroy()

    def createStatsDisplay():
        CS.statisticsFrame = FrameApp(property(lambda: CS.cardOptionsFrame))
        CS.statisticsFrame.config(relief= tkinter.SOLID, borderwidth= 2)
        CS.statisticsFrame.grid(row = 0, column = 3)
        CS.masteredStats = 0

        CS.statsLabels = list()
        if CS.deckStudyInfo[4] and any(CS.cardDisplays) and not all(CS.cardDisplays):
            CS.correctStats = [0] * 3
            CS.incorrectStats = [0] * 3
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Cards mastered: 0", font = "Arial 12 bold", justify= tkinter.LEFT, foreground= '#bf7c14'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "\nTotal correct answers: 0", font = "Arial 12 bold", justify= tkinter.LEFT, foreground= '#37a749'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Correct answers with Flips: 0", font = "Arial 12", justify= tkinter.LEFT, foreground= '#37a749'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Correct answers with Reveals: 0", font = "Arial 12", justify= tkinter.LEFT, foreground= '#37a749'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "\nTotal incorrect answers: 0", font = "Arial 12 bold", justify= tkinter.LEFT, foreground= '#ea1517'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Incorrect answers with Flips: 0", font = "Arial 12", justify= tkinter.LEFT, foreground= '#ea1517'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Incorrect answers with Reveals: 0", font = "Arial 12", justify= tkinter.LEFT, foreground= '#ea1517'))

        else:
            CS.correctStats, CS.incorrectStats = ([0], [0])
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Cards mastered: 0", font = "Arial 12 bold", justify= tkinter.LEFT, foreground= '#bf7c14'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Total correct answers: 0", font = "Arial 12 bold", justify= tkinter.LEFT, foreground= '#37a749'))
            CS.statsLabels.append(tkinter.Label(CS.statisticsFrame, text = "Total incorrect answers: 0", font = "Arial 12 bold", justify= tkinter.LEFT, foreground= '#ea1517'))
        
        labelNum = 0
        for label in CS.statsLabels:
            label.grid(row = labelNum, column = 0, sticky = tkinter.W)
            labelNum += 1
        

    def createCardDisplay():            
            if CS.cardDisplays[CS.cardNum]:
                frontLabel = tkinter.Label(CS.cardFrame, text = "Front", font = "Arial 20 bold underline", bg = '#54a6c4')
                frontLabel.grid(row = 0, column = 0)
                frontBox = FrameApp(property(lambda: CS.cardFrame))
                frontBox.config(relief= tkinter.RIDGE, borderwidth= 5)
                frontText = tkinter.Text(frontBox, font = "Arial 15", width = 52, height = 10, wrap = tkinter.WORD)
                frontText.insert(tkinter.END,  CS.cards[CS.cardNum][2])
                frontText.config(state = tkinter.DISABLED)

                frontScroll = tkinter.Scrollbar(frontBox)
                frontText.config(yscrollcommand= frontScroll.set)

                frontScroll.config(command= frontText.yview, orient= tkinter.VERTICAL)
                frontText.pack(side = tkinter.LEFT)
                frontScroll.pack(side = tkinter.RIGHT, fill = tkinter.Y, expand = tkinter.FALSE)
                frontBox.grid(row = 1, column = 0, padx = 10, pady = 10)


                backResponceLabel = tkinter.Label(CS.cardFrame, text = "Your Answer", font = "Arial 20 bold underline", bg = '#54a6c4')
                backResponceLabel.grid(row = 0, column = 1)

                backResponceBox = FrameApp(property(lambda: CS.cardFrame))
                backResponceBox.config(relief= tkinter.RIDGE, borderwidth= 5)

                backResponce = tkinter.Text(backResponceBox, font = "Arial 15", width = 52, height = 10, wrap = tkinter.WORD)
                
                backResponceScroll = tkinter.Scrollbar(backResponceBox)
                backResponce.config(yscrollcommand= backResponceScroll.set)
                backResponceScroll.config(command = backResponce.yview, orient= tkinter.VERTICAL)
                backResponce.pack(side = tkinter.LEFT)
                backResponceScroll.pack(side = tkinter.RIGHT, fill = tkinter.Y, expand = tkinter.FALSE)
                backResponceBox.grid(row = 1, column = 1, padx = 10, pady = 10)

                CS.flipOrRevealButton = tkinter.Button(CS.cardOptionsFrame, width = 15, height = 2, font = "Arial 12", background = '#C3C7C7', text = "Reveal Back", command = lambda: CS.revealBack(backResponce), state = tkinter.NORMAL)
                CS.flipOrRevealButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tkinter.NW)
            else:
                CS.isFlip = True


                cardLabel = tkinter.Label(CS.cardFrame, text = "Front", font = "Arial 20 bold underline", bg = '#54a6c4')
                cardLabel.grid(row = 0, column = 0)
                cardVisualFrame = FrameApp(property(lambda: CS.cardFrame))
                cardVisualFrame.grid(row = 1, column = 0, pady = 10)

                cardVisual = tkinter.Label(cardVisualFrame, text = CS.cards[CS.cardNum][2], width = 52, font = "Arial 15", anchor = tkinter.NW, wraplength= 570, relief= tkinter.GROOVE, borderwidth= 5, justify= tkinter.LEFT)
                cardVisual.pack(expand = True)
                CS.cardFrontHeight = CS.adjustCardVisualHeight(cardVisual)

                CS.flipOrRevealButton = tkinter.Button(CS.cardOptionsFrame, width = 15, height = 2, font = "Arial 12", background = '#C3C7C7', text = "Flip", command = lambda: CS.flipCard(cardVisual, cardLabel), state = tkinter.NORMAL)
                CS.flipOrRevealButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tkinter.NW)                

    @staticmethod
    def adjustCardVisualHeight(cardVisual):
        visualHeight = int(((cardVisual.winfo_reqheight() - 35)/23) + 1)
        if visualHeight < 10:
            cardVisual.config(height = 10)
            visualHeight = 10
        return visualHeight


    def revealBack(responceText):
        CS.flipOrRevealButton.config(state = tkinter.DISABLED)
        responceText.config(state = tkinter.DISABLED)

        backLabel = tkinter.Label(CS.cardFrame, text = "Back", font = "Arial 20 bold underline", bg = '#54a6c4')
        backLabel.grid(row = 2, column = 0, columnspan = 2)

        backBox = FrameApp(property(lambda: CS.cardFrame))
        backBox.config(relief= tkinter.RIDGE, borderwidth= 5)

        backText = tkinter.Text(backBox, font = "Arial 15", width = 52, height = 10, wrap = tkinter.WORD)
        backText.insert(tkinter.END,  CS.cards[CS.cardNum][3])
        backText.config(state = tkinter.DISABLED)

        backScroll = tkinter.Scrollbar(backBox)
        backText.config(yscrollcommand= backScroll.set)
        backScroll.config(command = backText.yview, orient= tkinter.VERTICAL)
        backText.pack(side = tkinter.LEFT)
        backScroll.pack(side = tkinter.RIGHT, fill = tkinter.Y, expand = tkinter.FALSE)
        backBox.grid(row = 3, column = 0, columnspan = 2, pady = 10)
        if not CS.cards[CS.cardNum][6]:
            CS.flipOrRevealQuestionFrame.grid(row = 0, column = 2, rowspan = 2, pady = 20)
        else:
            CS.masteryRemainLabel.config(text = "You already have card mastery!")


    def flipCard(cardVisual, cardLabel):
        cardVisual.config(height = 0)
        if cardLabel.cget("text") == "Front":
            cardLabel.config(text = "Back")
            cardVisual.config(text = CS.cards[CS.cardNum][3])

            if not CS.flipped:
                CS.flipped = True
                CS.cardBackHeight = CS.adjustCardVisualHeight(cardVisual)

                if not CS.cards[CS.cardNum][6]:
                    CS.flipOrRevealQuestionFrame.grid(row = 0, column = 2, rowspan = 2, pady = 20)
                else:
                    CS.masteryRemainLabel.config(text = "You already have card mastery!")
            else:
                cardVisual.config(height = CS.cardBackHeight)
        else:
            cardLabel.config(text = "Front")
            cardVisual.config(text = CS.cards[CS.cardNum][2])
            cardVisual.config(height = CS.cardFrontHeight)


    def updateCardScore(user_responce, cButton, wButton):
        cButton.config(state = tkinter.DISABLED)
        wButton.config(state = tkinter.DISABLED)
        
        if user_responce:
            CS.crsr.execute("UPDATE cards SET correctNum = " + str(CS.cards[CS.cardNum][5] + 1) + " WHERE c_id = " + str(CS.cards[CS.cardNum][0]))
            if (CS.cards[CS.cardNum][5] + 1) >= CS.deckStudyInfo[3]:
                if not CS.cards[CS.cardNum][6]:
                    CS.crsr.execute("UPDATE cards SET mastered = TRUE WHERE c_id = " + str(CS.cards[CS.cardNum][0]))
                    numMastered = len(CS.crsr.execute("SELECT * FROM cards WHERE deck_id = " + str(CDeck.deck[0]) + " AND mastered = True").fetchall())
                    CS.crsr.execute("UPDATE decks SET mastered = " + str(numMastered) + " WHERE deck_id = " + str(CDeck.deck[0]))
                    CDeck.updateDeck()
                CS.masteryRemainLabel.config(text = "You have card mastery!")
                CS.updateStats(user_responce, True)

            else:
                CS.masteryRemainLabel.config(text = "Amount of correct answers until mastery: " + str(CS.deckStudyInfo[3] - (CS.cards[CS.cardNum][5] + 1)))
                CS.updateStats(user_responce, False)

        else:
            CS.updateStats(user_responce, False)
            if (CS.cards[CS.cardNum][5] - 1) < 0:
                CS.masteryRemainLabel.config(text = "Amount of correct answers until mastery: " + str(CS.deckStudyInfo[3] - CS.cards[CS.cardNum][5]))
            elif (CS.cards[CS.cardNum][5]) < CS.deckStudyInfo[3]:
                CS.masteryRemainLabel.config(text = "Amuont of correct answers until mastery: " + str(CS.deckStudyInfo[3] - (CS.cards[CS.cardNum][5] - 1)))
                CS.crsr.execute("UPDATE cards SET correctNum = " + str(CS.cards[CS.cardNum][5] - 1) + " WHERE c_id = " + str(CS.cards[CS.cardNum][0]))


        CS.cards[CS.cardNum] = CS.crsr.execute("SELECT * FROM cards WHERE c_id = " + str(CS.cards[CS.cardNum][0])).fetchone()

    def updateStats(isCorrect, isMastered):
        if isMastered:
            CS.masteredStats += 1
            CS.statsLabels[0].config(text = "Cards mastered: " + str(CS.masteredStats))
            
        if isCorrect:
            CS.correctStats[0] += 1
            if CS.deckStudyInfo[4] and any(CS.cardDisplays) and not all(CS.cardDisplays):
                CS.statsLabels[1].config(text= "\nTotal correct answers: " + str(CS.correctStats[0]))
            else:
                CS.statsLabels[1].config(text= "Total correct answers: " + str(CS.correctStats[0]))

            if CS.deckStudyInfo[4] and CS.isFlip and any(CS.cardDisplays) and not all(CS.cardDisplays):
                
                CS.correctStats[1] += 1
                CS.statsLabels[2].config(text = "Correct answers with Flips: " + str(CS.correctStats[1]))

            elif CS.deckStudyInfo[4] and not CS.isFlip and any(CS.cardDisplays) and not all(CS.cardDisplays):
                
                CS.correctStats[2] += 1
                CS.statsLabels[3].config(text = "Correct answers with Reveals: " + str(CS.correctStats[2]))

        else:
            CS.incorrectStats[0] += 1
            if CS.deckStudyInfo[4] and any(CS.cardDisplays) and not all(CS.cardDisplays):
                CS.statsLabels[4].config(text = "\nTotal incorrect answers: " + str(CS.incorrectStats[0]))
                if CS.isFlip:
                
                    CS.incorrectStats[1] += 1
                    CS.statsLabels[5].config(text = "Correct answers with Flips: " + str(CS.incorrectStats[1]))

                else:                
                    CS.incorrectStats[2] += 1
                    CS.statsLabels[6].config(text = "Correct answers with Reveals: " + str(CS.incorrectStats[2]))

            else:
                CS.statsLabels[2].config(text = "Total incorrect answers: " + str(CS.incorrectStats[0]))
                
               


    def viewPreviousCard():
        CS.isFlip = False
        for child in CS.cardFrame.winfo_children():
            child.destroy()
        CS.flipped = False
        CS.flipOrRevealQuestionFrame.grid_forget()
        for child in CS.flipOrRevealQuestionFrame.winfo_children():
            if child.cget("text") != "How did you do?":
                child.configure(state = tkinter.NORMAL)
        CS.masteryRemainLabel.config(text = "")
        CS.cardNum -= 1
        CS.cardNumLabel.config(text = str(CS.cardNum + 1) + " out of " + str(len(CS.cards)))

        CS.fowardButton.config(state = tkinter.NORMAL)
        if CS.cardNum == 0:
            CS.backButton.config(state = tkinter.DISABLED)
        CS.flipOrRevealButton.destroy()
        CS.createCardDisplay()

    
    def viewNextCard():
        CS.isFlip = False
        for child in CS.cardFrame.winfo_children():
            child.destroy()
        CS.flipped = False
        CS.flipOrRevealQuestionFrame.grid_forget()
        for child in CS.flipOrRevealQuestionFrame.winfo_children():
            if child.cget("text") != "How did you do?":
                child.configure(state = tkinter.NORMAL)

        CS.masteryRemainLabel.config(text = "")
        CS.cardNum += 1
        CS.cardNumLabel.config(text = str(CS.cardNum + 1) + " out of " + str(len(CS.cards)))

        CS.backButton.config(state = tkinter.NORMAL)
        if CS.cardNum == len(CS.cards) - 1:
            CS.fowardButton.config(state = tkinter.DISABLED)
        CS.flipOrRevealButton.destroy()

        CS.createCardDisplay()
    


    def createOptionsFrame():

        CS.optionsFrame = FrameApp(property(lambda: w.window()))
        CS.optionsFrame.config(bg= '#6CB2CC', relief = tkinter.RIDGE, borderwidth= 3)
        CS.optionsFrame.place(x= 20, y = 120)

        CS.optionsFrame.createOptionsLabel()

        backButton = tkinter.Button(CS.optionsFrame ,text= "Back to Cards", width=15, height=2, font = "Arial 12", command = lambda: CS.backToCardMenu())
        backButton.grid(row = 1, column= 0, padx = 10, pady = 10)

        settingsButton = tkinter.Button(CS.optionsFrame ,text= "Settings", width=15, height=2, font = "Arial 12", command = lambda: CS.changeToSettings())
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



