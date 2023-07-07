import database as db
import window as w
import sqlite3
import tkinter as tk
import tkinter.font as tkf
import cardMenu as cm
import CardStudy
import deckMenu as dm
import MainFrame as mf
import TitleLabel as tl
from EntryApp import EntryApp
from FrameApp import FrameApp
from CurrentDeck import CDeck
from tkinter import *
from tkinter import messagebox


class CSS:
    crsr = db.database().cursor()

    optionsFrame = None
    selectionFrame = None
    methodQuestFrame = None
    levelQuestFrame = None
    enableQuestFrame = None
    starredQuestFrame = None
    masteryQuestFrame = None
    masteryEntry = None
    saveAndRestoreButtonFrame = None

    

    mainFrame = None

    def createSettingsPage():

        CSS.mainFrame = FrameApp(property(lambda: w.window()))
        CSS.mainFrame.config(bg = '#4A7A8C')
        CSS.mainFrame.pack(fill = BOTH, expand = TRUE)


        CSS.selectionFrame = FrameApp(property(lambda: CSS.mainFrame))
        CSS.selectionFrame.config(background =  '#54a6c4')
        CSS.selectionFrame.pack(padx = 50, pady = 50, anchor = E)

        CSS.createOptionsFrame()

        CSS.createMethodQuestion()
        CSS.createLevelQuestion()
        CSS.createEnableQuestion()
        CSS.createStarredQuestion()
        CSS.createMasteryQuestion()
        CSS.createSettingButtons()


    def createOptionsFrame():
       
        CSS.optionsFrame = FrameApp(property(lambda: w.window()))
        CSS.optionsFrame.config(bg= '#6CB2CC', relief = RIDGE, borderwidth= 3)
        CSS.optionsFrame.place(x= 20, y = 120)

        CSS.optionsFrame = CSS.optionsFrame.createOptionsLabel()

        backButton = Button(CSS.optionsFrame ,text= "Back to Study", width=15, height=2, font = "Arial 12", command = lambda: CSS.returnToStudyPage())
        backButton.grid(row = 1, column= 0, padx = 10, pady = 10)
   
    def restoreDefaultSettings():
        if messagebox.askokcancel("Restore Default", "Are you sure that you want to restore the default settings?"):
            deckStudyInfo = CSS.crsr.execute("SELECT * FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()
            if deckStudyInfo[1] != 0:
                CSS.crsr.execute("UPDATE deckstudy SET study_method = 0 WHERE deck_id = " + str(CDeck.deck[0]))
                CSS.methodQuestFrame.changeSelectedButton(CSS.methodQuestFrame.radioButtonList[0])
            if deckStudyInfo[2] != 2:
                CSS.crsr.execute("UPDATE deckstudy SET study_level = 2 WHERE deck_id = " + str(CDeck.deck[0]))
                CSS.levelQuestFrame.changeSelectedButton(CSS.levelQuestFrame.radioButtonList[2])
            if not deckStudyInfo[4]:
                CSS.crsr.execute("UPDATE deckstudy SET enable_open = true WHERE deck_id = " + str(CDeck.deck[0]))
                CSS.enableQuestFrame.changeSelectedButton(CSS.enableQuestFrame.radioButtonList[0])
            if deckStudyInfo[5]:
                CSS.crsr.execute("UPDATE deckstudy SET study_starred = false WHERE deck_id = " + str(CDeck.deck[0]))
                CSS.starredQuestFrame.changeSelectedButton(CSS.starredQuestFrame.radioButtonList[1])
            if deckStudyInfo[3] != 3:
                CSS.crsr.execute("UPDATE deckstudy SET mastery_req = 3 WHERE deck_id = " + str(CDeck.deck[0]))
                CSS.crsr.execute("UPDATE cards SET mastered = TRUE WHERE deck_id = " + str(CDeck.deck[0]) + " AND correctNum >= 3")
                CSS.crsr.execute("UPDATE cards SET mastered = FALSE WHERE deck_id = " + str(CDeck.deck[0]) + " AND correctNum < 3")

                CSS.masteryEntry.setStartResponce("3")    


    def updateSettings():
        deckStudyInfo = CSS.crsr.execute("SELECT * FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()
        if deckStudyInfo[1] != CSS.methodQuestFrame.var.get():
            CSS.crsr.execute("UPDATE deckstudy SET study_method = " + str(CSS.methodQuestFrame.var.get()) + " WHERE deck_id = " + str(CDeck.deck[0]))
        if deckStudyInfo[2] != CSS.levelQuestFrame.var.get():
            CSS.crsr.execute("UPDATE deckstudy SET study_level = " + str(CSS.levelQuestFrame.var.get()) + " WHERE deck_id = " + str(CDeck.deck[0]))
        if deckStudyInfo[3] != CSS.masteryEntry.savedResponce:
            CSS.crsr.execute("UPDATE deckstudy SET mastery_req = " + str(CSS.masteryEntry.savedResponce) + " WHERE deck_id = " + str(CDeck.deck[0]))
            CSS.crsr.execute("UPDATE cards SET mastered = TRUE WHERE deck_id = " + str(CDeck.deck[0]) + " AND correctNum >= " + str(CSS.masteryEntry.savedResponce))
            CSS.crsr.execute("UPDATE cards SET mastered = FALSE WHERE deck_id = " + str(CDeck.deck[0]) + " AND correctNum < " + str(CSS.masteryEntry.savedResponce))
            w.window().focus()
            
        if deckStudyInfo[4] != CSS.enableQuestFrame.var.get():
            CSS.crsr.execute("UPDATE deckstudy SET enable_open = " + str(CSS.enableQuestFrame.var.get()) + " WHERE deck_id = " + str(CDeck.deck[0]))
        if deckStudyInfo[5] != CSS.starredQuestFrame.var.get():
            CSS.crsr.execute("UPDATE deckstudy SET study_starred = " + str(CSS.starredQuestFrame.var.get()) + " WHERE deck_id = " + str(CDeck.deck[0]))
        CSS.masteryEntry = CSS.masteryEntry.keepOrCorrectResponce()


        db.database().commit()

    def createMethodQuestion():
        CSS.methodQuestFrame = FrameApp(property(lambda: CSS.selectionFrame))
        CSS.methodQuestFrame.config(relief = RIDGE, borderwidth = 5)
        CSS.methodQuestFrame.grid(row = 0, column = 0, rowspan = 2, padx = 25, pady = 20, sticky = NSEW)

        CSS.methodQuestFrame = CSS.methodQuestFrame.createQuestLabel("Select one of the following study methods you would like you use:", 40, 500)

        optionValue = CSS.crsr.execute("SELECT study_method FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()[0]
        CSS.methodQuestFrame.var = IntVar(value = optionValue)

        textList = ["Same order as cards in Card Menu (Default)", "Opposite order as cards in Card Menu", "Random Order", "Least understood to most understood", "Most understood to least understood"]
    
        
        for count in range(len(textList)):
            CSS.methodQuestFrame = CSS.methodQuestFrame.createRadioButton(textList[count], count)
        CSS.methodQuestFrame = CSS.methodQuestFrame.setVerticalGrid()

        CSS.methodQuestFrame = CSS.methodQuestFrame.setBeginningCurrentRadioButton(optionValue)


    def createLevelQuestion():
        CSS.levelQuestFrame = FrameApp(property(lambda: CSS.selectionFrame))
        CSS.levelQuestFrame.config(relief = RIDGE, borderwidth = 5)
        CSS.levelQuestFrame.grid(row = 0, column = 1, padx = 25, pady = 20, sticky = NSEW)
        CSS.levelQuestFrame = CSS.levelQuestFrame.createQuestLabel("Select one of the following levels of understanding to study:", 45, 500)


        optionValue =  CSS.crsr.execute("SELECT study_level FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()[0]
        CSS.levelQuestFrame.var = IntVar(value = optionValue)

        textList = ["Only non-mastered cards", "Only mastered cards ", "Both non-mastered and mastered cards (Default)"]

        for count in range(0,3):
            CSS.levelQuestFrame = CSS.levelQuestFrame.createRadioButton(textList[count], count)
        CSS.levelQuestFrame = CSS.levelQuestFrame.setVerticalGrid()


        CSS.levelQuestFrame = CSS.levelQuestFrame.setBeginningCurrentRadioButton(optionValue)


    def createEnableQuestion():
        CSS.enableQuestFrame = FrameApp(property(lambda: CSS.selectionFrame))
        CSS.enableQuestFrame.config(relief = RIDGE, borderwidth = 5)
        CSS.enableQuestFrame.grid(row = 1, column = 1, padx = 25, pady = 20, sticky = NSEW)
        CSS.enableQuestFrame = CSS.enableQuestFrame.createQuestLabel("Open Responce:", 15, 500)


        optionValue = CSS.crsr.execute("SELECT enable_open FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()[0]
        CSS.enableQuestFrame.var = BooleanVar(value = optionValue)

        textList = ["Enabled (Default)", "Disabled"]
        boolList = [True, False]

        for count in range(0,2):
            CSS.enableQuestFrame = CSS.enableQuestFrame.createRadioButton(textList[count], boolList[count])
        CSS.enableQuestFrame = CSS.enableQuestFrame.setHorizontalGrid()

        if optionValue:
            CSS.enableQuestFrame = CSS.enableQuestFrame.setBeginningCurrentRadioButton(0)
        else:
            CSS.enableQuestFrame = CSS.enableQuestFrame.setBeginningCurrentRadioButton(1)

    def createStarredQuestion():
        CSS.starredQuestFrame = FrameApp(property(lambda: CSS.selectionFrame))
        CSS.starredQuestFrame.config(relief = RIDGE, borderwidth = 5)
        CSS.starredQuestFrame.grid(row = 2, column = 1, padx = 25, pady = 20, sticky = EW)
        CSS.starredQuestFrame = CSS.starredQuestFrame.createQuestLabel("Starred Only:", 15, 500)

        optionValue = CSS.crsr.execute("SELECT study_starred FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()[0]
        CSS.starredQuestFrame.var = BooleanVar(value = optionValue)

        textList = ["Enabled", "Disabled (Default)"]
        boolList = [True, False]


        for count in range(0,2):
            CSS.starredQuestFrame = CSS.starredQuestFrame.createRadioButton(textList[count], boolList[count])
        CSS.starredQuestFrame = CSS.starredQuestFrame.setHorizontalGrid()

        if optionValue:
            CSS.starredQuestFrame = CSS.starredQuestFrame.setBeginningCurrentRadioButton(0)
        else:
            CSS.starredQuestFrame = CSS.starredQuestFrame.setBeginningCurrentRadioButton(1)

        

    def createMasteryQuestion():
        
        CSS.masteryQuestFrame = FrameApp(property(lambda: CSS.selectionFrame))
        CSS.masteryQuestFrame.config(relief = RIDGE, borderwidth = 5)
        CSS.masteryQuestFrame.grid(row = 2, column = 0, padx = 25, pady = 20, sticky= NSEW)

        CSS.masteryEntry = EntryApp(property(lambda: CSS.masteryQuestFrame), 2)
        CSS.masteryEntry.config(font = "Arial 25")
        CSS.masteryEntry.createMasteryEntry()

        CSS.masteryQuestFrame = CSS.masteryQuestFrame.createQuestLabel("Amount of correct answers (in a row) for a card until that cards mastery:", 35, 400)

        amountValue = CSS.crsr.execute("SELECT mastery_req FROM deckStudy WHERE deck_id = " + str(CDeck.deck[0])).fetchone()[0]

        CSS.masteryEntry = CSS.masteryEntry.setStartResponce(amountValue)

        CSS.masteryEntry.grid(row = 0, column = 1, padx = 10)


    def createSettingButtons():
        CSS.saveAndRestoreButtonFrame = FrameApp(property (lambda: CSS.selectionFrame))
        CSS.saveAndRestoreButtonFrame.config(relief = RIDGE, borderwidth = 5)
        CSS.saveAndRestoreButtonFrame.grid(row = 3, column = 0, padx = 25, pady = 20, sticky = NSEW)

        saveButton = Button(CSS.saveAndRestoreButtonFrame, text = "Save Changes", command= lambda: CSS.updateSettings(), background = '#C3C7C7', font = "Arial 15")
        saveButton.grid(row = 0, column = 0, padx = 20, pady = 10)

        restoreDefaultButton = Button(CSS.saveAndRestoreButtonFrame, text = "Restore Default", command = lambda: CSS.restoreDefaultSettings(), background = '#C3C7C7', font = "Arial 15")
        restoreDefaultButton.grid(row = 0, column = 1, padx = 20, pady = 10)


    


    def studyOptionsPageDestroy():
        CSS.optionsFrame.destroy()
        CSS.mainFrame.destroy()


    def returnToStudyPage():
        CSS.studyOptionsPageDestroy()
        CardStudy.CS.createStudyPage() 


    