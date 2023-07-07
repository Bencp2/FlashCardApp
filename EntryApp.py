import database as db
import window as w
import sqlite3
import tkinter as tk
import tkinter.font as tkf
from tkinter import *
from tkinter import messagebox


class EntryApp(Entry):
    def __init__(self, parent, w):
        Entry.__init__(self, parent.fget(), width = w, font = "12")
        self.savedResponce = None
        self.textVar = None

    def createDeckNameEntry(self):
        self.textVar = StringVar()
        self.config(textvariable= self.textVar)
        self.bind("<Return>", lambda event: w.window().focus())
        self.createDeckNameValidation()
        return self

    def createMasteryEntry(self):
        self.bind('<Return>', lambda event: self.saveIntValueLocally())
        self.bind('<Button-1>', lambda event: self.changeToEditMode())
        self.createMasteryValidation()


    def createMasteryValidation(self):
        vcmd = (self.register(self.validateMasteryAmount), "%P")
        self.config(validate= "all", validatecommand= vcmd)

    def createDeckNameValidation(self):
        vcmd = (self.register(self.validateDeckNameSize), "%P")
        self.config(validate= "all", validatecommand= vcmd)


    def validateMasteryAmount(self, value):
        if (str.isdigit(value) and int(value) <= 99 and int(value) >= 1 and len(value) <= 2) or value == "":
            return True
        else:
            return False        

    def validateDeckNameSize(self, name):
        if len(name) > 60:
            return False
        else:
            return True

    def saveIntValueLocally(self):
        w.window().focus()
        if self.get() != "":
            self.savedResponce = int(self.get())
        else:
            self.insert(END , self.savedResponce)



    def changeToEditMode(self):
        self.config(takefocus=1)
        return self

    def setStartResponce(self, responce):
        self.savedResponce = responce
        self.delete(0, END)
        self.insert(END, self.savedResponce)
        return self
        
    def keepOrCorrectResponce(self):
        if self.savedResponce != self.get():
            self.delete(0, END)
            self.insert(END, str(self.savedResponce))
        w.window().focus()

        return self