import tkinter

class window:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = tkinter.Tk()
            cls.instance.state('zoomed')
            # cls.instance.bind("<Configure>", lambda e: cls.instance.update())
            cls.instance.config(bg = '#4A7A8C')
            cls.instance.resizable(True, True)

        return cls.instance

        