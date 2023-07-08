import CurrentRadioButtonApp as crb
from tkinter import *
from RadioApp import RadiobuttonApp 

class FrameApp(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.fget())
        self.var = None
        self.selected = None
        self.radioButtonList = list()
        self.selected = crb.CurrentRadioButton()
        self.labelList = list()

    # def provideIntVar(self):
    #     return self.var
    
    # def provideBoolVar(self):
    #     return self.boolvar
    
    # def getVar(self):
    #     return self.var.get()

    # def provideSelected(self):
    #     return self.selected

    # def changeSelected(self, button):
    #     self.selected.changeSelected(button)

    # def createIntVar(self):
    #     self.var = IntVar()
    
    # def createBoolVar(self):
    #     self.var = BooleanVar()

    def createRadioButton(self, text, value):
        self.radioButtonList.append(RadiobuttonApp(property(lambda: self), text, value))
        self.radioButtonList[len(self.radioButtonList) - 1].bind('<Button-1>', lambda event, rButton = self.radioButtonList[len(self.radioButtonList) - 1]: self.changeSelectedButton(rButton))
        return self


    def setBeginningCurrentRadioButton(self, optionVal):
        self.selected = self.selected.selectBegin(property(lambda: self.radioButtonList[optionVal]))
        # self.var.set(optionVal)
        return self

    def changeSelectedButton(self, rButton):
        self.var.set(rButton.value)
        self.selected.changeSelected(property(lambda: rButton))

    def setVerticalGrid(self):
        for elm in range(0, len(self.radioButtonList)):
            self.radioButtonList[elm].grid(row = elm + 1, column = 0, padx = 20, pady = 10, sticky = EW)
        return self

    def setHorizontalGrid(self):
        for elm in range(0, len(self.radioButtonList)):
            self.radioButtonList[elm].grid(row = 0, column = elm + 1, padx = 30, pady = 10)
        return self

    def createQuestLabel(self, txt, wid, wrapLen):
        self.labelList.append(Label(self, text = txt, font = "Arial 15 bold", wraplength= wrapLen, relief= GROOVE, borderwidth= 3, width = wid, justify= LEFT))
        self.labelList[len(self.labelList) - 1].grid(row = 0, column = 0, padx = 10, pady = 10)
        return self

    def createOptionsLabel(self):
        self.labelList.append(Label(self,  text ="Options", font= "Arial 15", bg= '#6CB2CC'))
        self.labelList[len(self.labelList) - 1].grid(row = 0, column = 0 ,pady= 20, padx = 10)
        return self

