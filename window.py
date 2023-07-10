import tkinter

class window:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = tkinter.Tk()
            cls.instance.config(bg = '#4A7A8C')
            cls.instance.geometry('1500x800')
            cls.instance.resizable(False, False)

        return cls.instance

        