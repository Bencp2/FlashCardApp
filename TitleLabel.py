from tkinter import *
import window as w

class TitleBar:

    titleLabel = Label(w.window(),  font= "Arial 30 underline", bg= '#37afc8', height = 2, wraplength = 800)
    titleLabel.pack(fill = BOTH)

    def changeTitle(name):
        TitleBar.titleLabel.config(text = name)