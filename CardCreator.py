import database as db
import window as w
from tkinter import *
import cardMenu as cm
import TitleLabel as tl
from FrameApp import FrameApp
import cardMenu as cm
from CurrentDeck import CDeck
from idlelib.redirector import WidgetRedirector


class CardCreator:

    
    crsr = db.database().cursor()

    mainFrame = None
    optionsFrame = None 
    selectionFrame = None

    underlined = [False, False]
    bolded = [False, False]
    colored = [False, False]

    isFoward = False
    isDelete = False
    isFrontFocused = False
    frontInputTags = None
    backInputTags = None
    currentCard = None
    createBool = None

    @staticmethod
    def createCardCreator(card, createOrEdit):
        CardCreator.currentCard = card
        CardCreator.createBool = createOrEdit

        CardCreator.mainFrame = FrameApp(property(lambda: w.window()))
        CardCreator.mainFrame.config(bg = '#4A7A8C')
        CardCreator.mainFrame.pack(fill = BOTH, expand = TRUE)


        CardCreator.selectionFrame = FrameApp(property(lambda: CardCreator.mainFrame))
        CardCreator.selectionFrame.config(relief = GROOVE, borderwidth = 5)
        CardCreator.selectionFrame.pack(pady = 30)
        CardCreator.createOptionsFrame()

        if CardCreator.createBool:
            clabel = Label(CardCreator.selectionFrame,  text = "Enter Front and Back for card", font= "Arial 25 bold underline")
        else:
            clabel = Label(CardCreator.selectionFrame,  text = "Edit Front or/and Back for card", font= "Arial 25 bold underline")
        clabel.pack(pady = 50)

        inputFrameGrid = FrameApp(property(lambda: CardCreator.selectionFrame))
        inputFrameGrid.pack(padx = 10, pady = 20)


        
        frontEditOptionsFrame = FrameApp(property(lambda: inputFrameGrid))

        frontLabel = Label(inputFrameGrid,  text = "Front", font= "Arial 20 bold", width = 20)
        frontLabel.grid(row = 0, column = 1, pady = 10)

        frontBox = FrameApp(property(lambda: inputFrameGrid))
        frontInput = Text(frontBox, height = 10, width =50, wrap= WORD, font = 'Arial')
        CardCreator.createEditingOptions(frontEditOptionsFrame, frontInput)
        frontEditOptionsFrame.grid(row = 0, column = 0)

        if not CardCreator.createBool:
            frontInput.insert(END, CardCreator.currentCard[2])
        frontInput.pack(side = LEFT)
        frontScroll = Scrollbar(frontBox)
        frontInput.config(yscrollcommand= frontScroll.set)

        frontScroll.config(command= frontInput.yview, orient= VERTICAL)
        frontScroll.pack(side = RIGHT, fill = Y, expand = FALSE)
        frontBox.grid(row = 1, column = 0, columnspan= 2, padx = 10)
        
        backEditOptionsFrame = FrameApp(property(lambda: inputFrameGrid))

        backLabel = Label(inputFrameGrid,  text = "Back", font= "Arial 20 bold", width = 20)
        backLabel.grid(row = 0, column = 3, pady = 10)
        
        backBox = Frame(master=inputFrameGrid)
        backInput = Text(master= backBox, height =  10, width = 50, wrap= WORD, font = 'Arial')
        CardCreator.createEditingOptions(backEditOptionsFrame, backInput)
        backEditOptionsFrame.grid(row = 0, column = 2)

        if not CardCreator.createBool:
            backInput.insert(END, CardCreator.currentCard[3])

        backInput.pack(side = LEFT)
        backScroll = Scrollbar(backBox )
        backInput.config(yscrollcommand= backScroll.set)
        backScroll.config(command= backInput.yview, orient= VERTICAL)
        backScroll.pack(side = RIGHT, fill = Y, expand = FALSE)
        
        backBox.grid(row = 1, column = 2, columnspan= 2, padx = 10)

        frontInput.bind("<FocusIn>", lambda event: CardCreator.changeFocus(frontEditOptionsFrame, backEditOptionsFrame, True))
        backInput.bind("<FocusIn>", lambda event: CardCreator.changeFocus(backEditOptionsFrame, frontEditOptionsFrame, False))
        
        frontInput.bind("<<Modified>>",  CardCreator.alterText)
        backInput.bind("<<Modified>>", CardCreator.alterText)
        

        if CardCreator.createBool:
            subButton = Button(CardCreator.selectionFrame ,text= "Create", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: CardCreator.inputResponce(frontInput, backInput))
        else:
            subButton = Button(CardCreator.selectionFrame ,text= "Change", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: CardCreator.inputResponce(frontInput, backInput))
        subButton.pack(side = RIGHT, padx = 20, pady = 10)        
        
        # index = frontInput.index("insert-1c")
        # print(index)
        # if "underline_tag" in frontInput.tag_names(index):
            # frontInput.tag_remove("underline_tag", index1 = index, index2 = index)

    def changeFocus(focusedFrame, unfocusedFrame, frontFocus):

        CardCreator.isFrontFocused = frontFocus
        
        for child in focusedFrame.winfo_children():
            child.config(state = NORMAL)
            

        for child in unfocusedFrame.winfo_children():
            child.config(bg = '#f0f0f0', state = DISABLED)


    def createEditingOptions(editingFrame, textBox):
        
        def do_nothing(event):
            return "break"

        buttonList = list()
        textBox.bind("<Control-t>", do_nothing)

        textBox.tag_config("underline_tag", underline = True)
        buttonList.append(Button(editingFrame, relief= FLAT, text = "U", font = "Arial 12 underline", state = DISABLED))
        buttonList[0].config(command = lambda: CardCreator.underlineText(buttonList[0], textBox))        
        buttonList[0].grid(row = 0, column = 0)
        redirector = WidgetRedirector(textBox)
        

        def on_mark(*args):
            hasIndex = True

            if len(args) > 2:
                if "+1" in args[2]:
                    index = textBox.index("insert")
                elif "-1" in args[2]:
                    index = textBox.index("insert-2c")
                elif args[2][0].isdigit():
                    index = textBox.index(args[2] + "-1c")
                else:
                    print(*args, "GREATER THAN 2")
                    hasIndex = False
            else:
                print(*args, "2 OR LESS")
                index = textBox.index("insert-1c")
            if hasIndex:
                CardCreator.evaluateIndex(textBox, buttonList, index)
            return original_mark(*args)
        def on_delete(*args):
            print(args, "DELETE")
            if "-1" in args[0]:
                index = textBox.index("insert-2c")
            else:
                index = textBox.index("insert-1c")
            CardCreator.isDelete = True
            CardCreator.evaluateIndex(textBox, buttonList, index)
            return original_delete(*args)
        
        original_mark = redirector.register("mark", on_mark )
        original_delete = redirector.register("delete", on_delete)
        # original_right = redirector.register("right", on_right)

        # textBox.bind("<Select>", lambda event: CardCreator.evaluateIndex(event, buttonList))

        # textBox.bind("<cursor>",lambda event: CardCreator.evaluateIndex(event, buttonList))

        # textBox.bind("<KeyRelease-Down>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))
        # textBox.bind("<Down>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))

        # textBox.bind("<KeyRelease-Left>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))
        # textBox.bind("<KeyPress-Left>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))

        # textBox.bind("<Left>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))

        # textBox.bind("<KeyRelease-Right>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))
        # textBox.bind("<KeyPress-Right>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))

        # textBox.bind("<Right>", lambda event: CardCreator.evaluateIndex(textBox, buttonList))

        # textBox.bind("<BackSpace>", lambda event: CardCreator.activateBackSpace(textBox, buttonList))


    def evaluateIndex(textBox, buttonList, index):
        # if CardCreator.isDelete:
        #     index = textBox.index("insert-2c")
        # else:
        #     print("INDEED")
        #     index = textBox.index("insert-1c")
            # print(textBox.get(index1 = index), "BEFORE")

        # for tag in textBox.tag_names(index):
        # print(textBox.get(index1 = index))
        if "underline_tag" in textBox.tag_names(index) and buttonList[0].cget("bg") != '#ABBCFF':
            buttonList[0].config(bg = '#ABBCFF')
            CardCreator.underlined[not CardCreator.isFrontFocused] = True
        if not "underline_tag" in textBox.tag_names(index) and buttonList[0].cget("bg") != '#f0f0f0':
            buttonList[0].config(bg =  '#f0f0f0')       
            CardCreator.underlined[not CardCreator.isFrontFocused] = False

    # def activateBackSpace(textBox, buttonList):
    #     CardCreator.isDelete = True
    #     CardCreator.evaluateIndex(textBox, buttonList)   


    def alterText(event):

        event.widget.edit_modified(False)
        if CardCreator.isDelete:
            CardCreator.isDelete = False 
        else:
            if CardCreator.underlined[not CardCreator.isFrontFocused]:
                event.widget.tag_add("underline_tag", index1 = event.widget.index("insert-1c"))
            else:
                event.widget.tag_remove("underline_tag", index1 = event.widget.index("insert-1c"), index2 = event.widget.index("insert"))  

    def underlineText(button, textBox):
        if textBox.focus_get():
            if textBox.tag_ranges("sel"):
                s0, s1 = (textBox.index("sel.first"), textBox.index("sel.last"))
                if "underline_tag" in textBox.tag_names(s0):
                    button.config(bg = '#f0f0f0')
                    CardCreator.underlined[not CardCreator.isFrontFocused] = False
                    textBox.tag_remove("underline_tag", index1 = s0, index2 = s1)
                else:
                    button.config(bg = '#ABBCFF')
                    CardCreator.underlined[not CardCreator.isFrontFocused] = True
                    textBox.tag_add("underline_tag", s0, s1)

            else:
                index = textBox.index("insert-1c")
                if "underline_tag" in textBox.tag_names(index):
                    button.config(bg = '#f0f0f0')
                    # textBox.tag_remove("underline_tag", index1 = index, index2 = index)
                    CardCreator.underlined[not CardCreator.isFrontFocused] = False
                else:
                    button.config(bg = '#ABBCFF')
                    CardCreator.underlined[not CardCreator.isFrontFocused] = True
                    

                    # textBox.tag_add("underline_tag", index1 = index)
                    
                    


    @staticmethod
    def createOptionsFrame():
        CardCreator.optionsFrame = FrameApp(property(lambda: w.window()))
        CardCreator.optionsFrame.config(bg= '#6CB2CC', relief = RIDGE, borderwidth= 3)
        CardCreator.optionsFrame.place(x= 20, y = 120)
        
        CardCreator.optionsFrame.createOptionsLabel()
        
        backButton = Button(CardCreator.optionsFrame, text= "Back to Cards", width=15, height=2, font = "Arial 12", command = lambda: CardCreator.backToMenu())
        backButton.grid(row = 1, column= 0, padx = 10, pady = 10) 

    @staticmethod
    def inputResponce(frontInput, backInput):
        front = frontInput.get(1.0, "end-1c")
        back = backInput.get(1.0, "end-1c")
        if CardCreator.createBool:
            CardCreator.crsr.execute("INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)", (CDeck.deck[0], front, back,))
            CardCreator.crsr.execute("UPDATE decks SET size = " + str(CDeck.deck[3] + 1) + " WHERE deck_id = " + str(CDeck.deck[0]))
            
        else:
            CardCreator.crsr.execute("UPDATE cards SET front = \"" + frontInput.get(1.0, "end-1c") + "\", back = \"" + str(backInput.get(1.0, "end-1c")) + "\" WHERE c_id = " + str(CardCreator.currentCard[0]))
        
        db.database().commit()
        CDeck.updateDeck()

        CardCreator.backToMenu()

    @staticmethod
    def cardCreatorDestroy():
        CardCreator.mainFrame.destroy()
        CardCreator.optionsFrame.destroy()

    def backToMenu():
        CardCreator.cardCreatorDestroy()
        cm.cardMenu.cardMenuCreate()