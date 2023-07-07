import window as w
from tkinter import *
from FrameApp import FrameApp
# import TitleLabel as tl

class MainFrame(Frame):


    # win = w.window()
    # canvas = tk.Canvas(win, highlightthickness= 0, bg = '#4A7A8C')
    # mainFrame = tk.Frame(canvas, bg = '#4A7A8C')
    # scroll = tk.Scrollbar(master = win)

    def __init__(self, parent):
        Frame.__init__(self, parent.fget(), bg =  '#4A7A8C')
        self.canvas = Canvas(self, highlightthickness= 0, bg = '#4A7A8C')
        self.addFrame = FrameApp(property(lambda: self.canvas))
        self.addFrame.config( bg = '#4A7A8C')
        self.scroll = Scrollbar(self)
        self.scroll.config(command= self.canvas.yview, orient= VERTICAL)
        # scrollBar.scroll.pack(side = tk.RIGHT, fill = tk.Y, expand = tk.FALSE)
        # scrollBar.canvas.pack( expand = tk.TRUE, anchor= tk.N, fill = tk.BOTH) 
        
        self.addFrame.bind("<Configure>", lambda e: self.canvas.config(scrollregion= self.canvas.bbox("all")))
        
        self.canvas.create_window((0,0), anchor = NW, window= self.addFrame, width = 1500) 
        # self.addFrame.grid_columnconfigure(0, weight = 1)
        self.canvas.config(yscrollcommand = self.scroll.set, yscrollincrement= 10)
        self.canvas.pack(side = LEFT, expand = TRUE, anchor= N, fill = BOTH) 
        self.scroll.pack(side = RIGHT, fill = Y, expand = FALSE)
        # self.createWin()

    def createWin(self):
        pass
        # win = w.window()
        # scrollBar.canvas = tk.Canvas(win, highlightthickness= 0, bg = '#4A7A8C')
        # scrollBar.mainFrame = tk.Frame(scrollBar.canvas, bg = '#4A7A8C')
        # scrollBar.frame = tk.Frame(scrollBar.mainFrame, bg = '#4A7A8C')
        # scrollBar.frame.pack(expand = )
        # scrollBar.scroll = tk.Scrollbar(master = win)

        # scrollBar.canvas.config( yscrollincrement= 10)

       




        # print((scrollBar.mainFrame.winfo_reqheight()/2))

        # scrollBar.canvas.create_window((scrollBar.canvas.winfo_screenwidth()/2) - , 0, anchor = 'nw', window= scrollBar.mainFrame)
    #    (scrollBar.canvas.winfo_screenwidth()/2), (scrollBar.canvas.winfo_screenheight()/2)
        # scrollBar.frame = tk.Frame(win)
        # scrollBar.frame.pack(expand= tk.TRUE, fill= tk.BOTH)
        # scrollBar.canvas = tk.Canvas(scrollBar.frame, bg = '#4A7A8C')
        
        # scrollBar.scroll = tk.Scrollbar(master = scrollBar.frame, orient= tk.VERTICAL)
        # scrollBar.scroll.pack(side = tk.RIGHT, fill = tk.Y)
        # scrollBar.scroll.config(command = scrollBar.canvas.yview)

        # scrollBar.canvas.config(yscrollcommand= scrollBar.scroll.set)
        # scrollBar.canvas.pack(fill = tk.BOTH, expand = tk.TRUE)



    def getAddFrame(self):
        return self.addFrame
    
    # @staticmethod        
    # def createWindow():
        # scrollBar.canvas.create_window(742,(scrollBar.mainFrame.winfo_reqheight()/2), window= scrollBar.mainFrame, width = 1500)
        # scrollBar.canvas.bind("<Configure>", scrollBar.update())   

    # @staticmethod        
    # def updateMainFrame(wid, hei):
    #     print(wid, "WIDTH")
    #     print(hei, "HEIGHT")
    #     scrollBar.mainFrame.configure(width = wid, height = hei)


    @staticmethod        
    def update():
        pass
        # scrollBar.canvas.update_idletasks()
        # scrollBar.canvas.config(scrollregion=scrollBar.canvas.bbox("all"))
