from tkinter import *
import window as w

class CurrentRadioButton:

    def __init__(self):
        self.current = None

    def changeSelected(self, currSelected):
        currSelectedNode = currSelected.fget()
        self.current.config(background = '#f0f0f0', activebackground = '#c1bec1')
        currSelectedNode.config(background = '#27d8b2', activebackground = '#27d8b2')
        self.current = currSelectedNode
        return self
    
    def selectBegin(self, curRButton):
        curRButtonNode = curRButton.fget()
        self.current = curRButtonNode
        self.current.configure(background = '#27d8b2', activebackground = '#27d8b2')
        return self