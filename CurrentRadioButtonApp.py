import database as db
import window as w
import sqlite3
import tkinter as tk
import tkinter.font as tkf
import MainFrame as sb
import TitleLabel as tl
from tkinter import *
from tkinter import messagebox

class CurrentRadioButton:

    def __init__(self):
        self.current = None

    def changeSelected(self, currSelected):
        currSelectedNode = currSelected.fget()
        self.current.config(background = w.window().cget('bg'), activebackground = '#c1bec1')
        currSelectedNode.config(background = '#27d8b2', activebackground = '#27d8b2')
        self.current = currSelectedNode
        return self
    
    def selectBegin(self, curRButton):
        curRButtonNode = curRButton.fget()
        self.current = curRButtonNode
        self.current.configure(background = '#27d8b2', activebackground = '#27d8b2')
        return self