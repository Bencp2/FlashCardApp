import tkinter as tk
from tkinter import messagebox
from deckMenu import deckMenu as dm
import window as w
import database as db
import TitleLabel as tl

win = w.window()


def callback():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        db.database().commit()
        db.database().close()
        win.destroy()

        

win.protocol("WM_DELETE_WINDOW", callback)

def main():
    tl.TitleBar()
    dm.deckMenuCreate()


main()

win.mainloop()