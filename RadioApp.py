import window as w
from tkinter import *

class RadiobuttonApp(Radiobutton):

    def __init__(self, parent, txt, val):
        self.parentNode = parent.fget()
        Radiobutton.__init__(self, self.parentNode, variable = self.parentNode.var, text = txt, value = val, anchor = W, font = "Arial 12", activebackground= '#c1bec1')
        self.variable = self.parentNode.var
        self.selected = self.parentNode.selected
        self.value = val
        self.createBindings()

    def createBindings(self):
        self.bind('<Enter>', lambda event: self.changeToHoverColor())
        self.bind('<Leave>', lambda event: self.removeHoverColor())


        

    def changeToHoverColor(self):
        if self.value != self.variable.get():
            self.config(background = '#e7e6e7')
        return self
    
    def removeHoverColor(self):
        if self.value != self.variable.get():
            self.config(background = w.window().cget('bg'))
        return self



    
    