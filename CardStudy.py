import database as db
import window as w
import sqlite3
import tkinter as tk
import tkinter.font as tkf
import cardMenu as cm
import deckMenu as dm
import MainFrame as mf
import TitleLabel as tl
from CardStudySettings import CSS
from FrameApp import FrameApp
from tkinter import *
from tkinter import messagebox
from CurrentDeck import CDeck
import random
import math
class CS:


    optionsFrame = None
    selectionFrame = None

    deckStudyInfo = None
    scrollWindow = None

    cardDisplays = list()
    cards = list()

    crsr = db.database().cursor()


    def createStudyPage():
        CS.scrollWindow = mf.MainFrame(property(lambda: w.window()))
        CS.scrollWindow.pack(fill = BOTH, expand = TRUE)

        CS.selectionFrame = FrameApp(property(lambda: CS.scrollWindow.getAddFrame()))
        CS.selectionFrame.pack(pady = 30)


        CS.createDefaultData()
        
        CS.createCardList()
        # CS.createStudyDisplay()

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
            

    # def createStudyDisplay():
        


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



