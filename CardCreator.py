import database as db
import window as w
from tkinter import *
import cardMenu as cm
import TitleLabel as tl
from FrameApp import FrameApp
import cardMenu as cm
from CurrentDeck import CDeck
from idlelib.redirector import WidgetRedirector
from TextApp import MyText

class CardCreator:

    
    crsr = db.database().cursor()

    mainFrame = None
    optionsFrame = None 
    selectionFrame = None

    underlined = [False, False]
    bolded = [False, False]
    colored = [False, False]

    total_frontTag_ids = 0
    frontTag_undo_stack = []
    frontTag_redo_stack = []

    isModified = False
    num_appended = 0


    total_backTag_ids = 0

    backTag_undo_stack = []
    backTag_redo_stack = []

    isInsert = False
    current_insert = []
    isFoward = False
    isDelete = False
    isNotUndoRedoDelete = False
    isUndo = False
    isPaste = False
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
        frontInput = Text(frontBox, height = 10, width =50, wrap= WORD, font = 'Arial', undo = True)
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
        backInput = Text(master= backBox, height =  10, width = 50, wrap= WORD, font = 'Arial', undo = True)
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
        
        frontInput.bind("<<Modified>>", lambda event: CardCreator.updateDeleteAndAlterText(frontInput))
        backInput.bind("<<Modified>>", lambda event: CardCreator.updateDeleteAndAlterText(backInput))

        if CardCreator.createBool:
            subButton = Button(CardCreator.selectionFrame ,text= "Create", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: CardCreator.inputResponce(frontInput, backInput))
        else:
            subButton = Button(CardCreator.selectionFrame ,text= "Change", width=10, height=2, font= "Arial 15", bg = '#C3C7C7', command = lambda: CardCreator.inputResponce(frontInput, backInput))
        subButton.pack(side = RIGHT, padx = 20, pady = 10)        

        # index = frontInput.index("insert-1c")
        # print(index)
        # if "underline_tag" in frontInput.tag_names(index):
            # frontInput.tag_remove("underline_tag", index1 = index, index2 = index)
    def updateDeleteAndAlterText(textBox):
        if CardCreator.isDelete and CardCreator.isInsert:
            CardCreator.isDelete = False
            CardCreator.isInsert = False
        # print("DELETE:", CardCreator.isDelete, "INSERT:", CardCreator.isInsert)
        CardCreator.alterText(textBox)

    def changeFocus(focusedFrame, unfocusedFrame, frontFocus):

        CardCreator.isFrontFocused = frontFocus
        
        for child in focusedFrame.winfo_children():
            child.config(state = NORMAL)
            

        for child in unfocusedFrame.winfo_children():
            child.config(bg = '#f0f0f0', state = DISABLED)


    def createEditingOptions(editingFrame, textBox):
        
        def do_nothing(event):
            return "break"

        def activate_undo(event):
            CardCreator.isUndo = True

            print("UNDO TRUE")
        def activate_redo(event):
            CardCreator.isUndo = False
            print("REDO TRUE")

        def activate_paste(event):
            CardCreator.isPaste = True
        
        buttonList = list()
        textBox.bind("<Control-t>", do_nothing)
        textBox.bind("<Control-z>", lambda event: activate_undo(event))
        textBox.bind("<Control-v>", lambda event: activate_paste(event))

        textBox.bind("<Control-Shift-Z>", lambda event: activate_undo(event))
        textBox.bind("<Control-y>", lambda event: activate_redo(event) )

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
            print(*args, "DELETE")
            if CardCreator.isUndo and args[0][0].isdigit():
                index = textBox.index("insert-1c")
                arg_index = args[0]

                if textBox.index(arg_index + "+1c") == args[1]:
                    if CardCreator.isFrontFocused:
                        popped_action = CardCreator.frontTag_undo_stack.pop()
                        CardCreator.frontTag_redo_stack.append(popped_action)
                        
                    else:
                        popped_action = CardCreator.frontTag_undo_stack.pop()
                        CardCreator.backTag_redo_stack.append(popped_action)

                    CardCreator.num_appended += 1

                else:
                    
                    while textBox.index(arg_index) != args[1]:
                        print(arg_index, args[1])
                        if CardCreator.isFrontFocused:
                            CardCreator.frontTag_redo_stack.append(CardCreator.frontTag_undo_stack.pop())
                        else:
                            CardCreator.backTag_redo_stack.append(CardCreator.backTag_undo_stack.pop())
                        arg_index = textBox.index(arg_index + "+1c")
                        CardCreator.num_appended += 1

            elif not CardCreator.isUndo and args[0][0].isdigit():
                index = textBox.index("insert-1c")
                arg_index = args[0]

                if textBox.index(arg_index + "+1c") == args[1]:
                    if CardCreator.isFrontFocused:
                        CardCreator.frontTag_undo_stack.append(CardCreator.frontTag_redo_stack.pop())
                    else:
                        CardCreator.backTag_undo_stack.append(CardCreator.backTag_redo_stack.pop())
                    CardCreator.num_appended += 1
                else:
                    while textBox.index(arg_index) != args[1]:
                        if CardCreator.isFrontFocused:
                            CardCreator.frontTag_undo_stack.append(CardCreator.frontTag_redo_stack.pop())
                        else:
                            CardCreator.backTag_undo_stack.append(CardCreator.backTag_redo_stack.pop())
                        arg_index = textBox.index(arg_index + "+1c")
                        CardCreator.num_appended += 1
            else:
                CardCreator.isNotUndoRedoDelete = True
                if CardCreator.isFrontFocused:
                    CardCreator.frontTag_redo_stack = []
                else:
                    CardCreator.backTag_redo_stack = []
                
                # index = args[0]
                # if textBox.index(index + "+1c") == args[1]:
                #     if CardCreator.isFrontFocused:
                #         CardCreator.frontTag_undo_stack.append([index, textBox.tag_names(index)])
                #     else:
                #         CardCreator.backTag_undo_stack.append([index, textBox.tag_names(index)])
                #     CardCreator.num_undo += 1
                # else:
                #     while textBox.index(index + "+1c") != args[1]:
                #         if CardCreator.isFrontFocused:
                #             CardCreator.frontTag_undo_stack.append([index, textBox.tag_names(index)])
                #         else:
                #             CardCreator.backTag_undo_stack.append([index, textBox.tag_names(index)])
                #         CardCreator.num_undo += 1
                #         index = textBox.index(index + "+1c")
           

                if "-1" in args[0]:
                    index = textBox.index("insert-2c")              
                    if CardCreator.isFrontFocused:
                        CardCreator.frontTag_undo_stack.append([textBox.index(args[0]), textBox.tag_names(args[0]), textBox.index(args[0]), None])
                    else:
                        CardCreator.backTag_undo_stack.append([textBox.index(args[0]), textBox.tag_names(args[0]), textBox.index(args[0]), None])
                    CardCreator.num_appended = 1
                else:
                    isSelect = False
                    index = textBox.index("insert-1c")
                    if ("insert" == args[0] or args[0] == "sel.first") and len(args) == 2: 
                        if args[0] == "sel.first":
                            isSelect = True
                        s0 = textBox.index(args[len(args) - 2])

                        while textBox.index(s0) != textBox.index(args[len(args) - 1]):
                            if isSelect and textBox.index(s0 + " +1c") == textBox.index(args[len(args) - 1]) and textBox.get(index1 = textBox.index(s0), index2 = textBox.index(args[len(args) - 1])) == '\n':
                                if textBox.index(s0 + " +1c") == textBox.index(END):
                                    break
                            else:
                                if CardCreator.isFrontFocused:
                                    CardCreator.frontTag_undo_stack.append([s0, textBox.tag_names(s0), s0, None])
                                else:
                                    CardCreator.backTag_undo_stack.append([s0, textBox.tag_names(s0), s0, None])
                            s0 = textBox.index(s0 + " +1c")
                            CardCreator.num_appended += 1

                    else:
                        if CardCreator.isFrontFocused:
                            CardCreator.frontTag_undo_stack.append([textBox.index(args[0]), textBox.tag_names(args[0]), textBox.index(args[0]), None])
                        else:
                            CardCreator.backTag_undo_stack.append([textBox.index(args[0]), textBox.tag_names(args[0]), textBox.index(args[0]), None])
                        CardCreator.num_appended = 1


            CardCreator.evaluateIndex(textBox, buttonList, index)
            CardCreator.isDelete = True
            original_delete(*args)
            # CardCreator.updateStacks(textBox)
        
        def on_insert(*args):
            print(args, "INSERT")
            if CardCreator.isDelete and CardCreator.num_appended > 0:
                CardCreator.updateStacks(textBox)
            CardCreator.isInsert = True
            if CardCreator.isUndo and args[0][0].isdigit():
                    s0 = args[0]
                    for arg_index in range(0, len(args[1])):
                        if CardCreator.isFrontFocused:
                            popped_action = CardCreator.frontTag_undo_stack.pop()
                            popped_action[2] = popped_action[0]
                            CardCreator.frontTag_redo_stack.append(popped_action)
                            
                        else:
                            popped_action = CardCreator.backTag_undo_stack.pop()
                            popped_action[2] = popped_action[0]
                            CardCreator.backTag_redo_stack.append(popped_action)
                        CardCreator.num_appended += 1

                        s0 = textBox.index(s0 + "+1c")                        
            elif not CardCreator.isUndo and args[0][0].isdigit():                
                    s0 = args[0]
                    for arg_index in range(0, len(args[1])):
                        if CardCreator.isFrontFocused:
                            popped_action = CardCreator.frontTag_redo_stack.pop()
                            popped_action[2] = popped_action[0]
                            CardCreator.frontTag_undo_stack.append(popped_action)
                        else:
                            popped_action = CardCreator.backTag_redo_stack.pop()
                            popped_action[2] = popped_action[0]
                            CardCreator.backTag_undo_stack.append(CardCreator.backTag_redo_stack.pop())
                        CardCreator.num_appended += 1
                        s0 = textBox.index(s0 + "+1c")
                          
            else:
                if CardCreator.isFrontFocused:
                    CardCreator.frontTag_redo_stack.clear()
                else:
                    CardCreator.backTag_redo_stack.clear()
                CardCreator.current_insert = [args[0], len(args[1])]
                
                # s0 = args[0]
                # for arg_index in range(0, len(args[1])):
                #     if CardCreator.isFrontFocused:
                #         CardCreator.frontTag_undo_stack.append([textBox.index(s0), textBox.tag_names(s0)])
                #     else:
                #         CardCreator.backTag_undo_stack.append([textBox.index(s0), textBox.tag_names(s0)])
                #     s0 = textBox.index(s0 + "+1c")


                    # for c in range(0, CardCreator.num_undo):
                    #     if CardCreator.isFrontFocused:
                    #         CardCreator.frontTag_redo_stack.append(CardCreator.frontTag_undo_stack.pop()) 
                    #     else:
                    #         CardCreator.backTag_redo_stack.append(CardCreator.backTag_undo_stack.pop()) 
                    #     CardCreator.num_redo += 1
                

            original_insert(*args)
            if CardCreator.isPaste:
                CardCreator.isPaste = False
                CardCreator.alterText(textBox)

                
        original_mark = redirector.register("mark", on_mark )
        original_delete = redirector.register("delete", on_delete)
        original_insert = redirector.register("insert", on_insert)
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
    
    # Insert
    # Text: 123456789
    # undoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.8", tags] ]
    # redoList = []
    
    # Undo (Delete)
    # Text: 
    # undoList = []
    # perform undos when appending to redoList
    # redoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.8", tags]]

    # Insert
    # Text: abcdefg
    # undoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.6", tags] ]
    # redoList = []
    # empty redoList when new a character is entered

    # Delete
    # Text: abcd
    # undoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.6", tags], ["1.4", tags], ... , ["1.6", tags] ]
    # redoList = [ ]
    
    # Undo (Insert)
    # Text: abcdefg
    # undoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.6", tags] ]
    # count number of undos (count each append to redoList)
    # redoList = [ ["1.4", tags], ... , ["1.6", tags] ]
    # for number of counted undos, update the tag of the specific location.

    # Undo (Delete)
    # Text: 
    # undoList = [ ]
    # redoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.6", tags], ["1.4", tags], ... , ["1.6", tags] ]

    # Redo (Insert)
    # Text: abcdefg
    # undoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.6", tags] ]
    # redoList = [ ["1.4", tags], ... , ["1.6", tags] ]
    # count number of redos (count each append to undoList)
    # for number of counted redos, update the tag of the specific location.

    # Redo (Delete)
    # Text: abcd
    # undoList = [ ["1.0", tags], ["1.1", tags], ... , ["1.6", tags], ["1.4", tags], ... , ["1.6", tags] ]
    # redoList = [ ]
    # append pops from redoList to redoList  


    # On undo (DELETE):
    # 1. pop a character from undoList
    # 2. append character to redoList
    # 3. count each character popped in num_undo
    # 4. 

    # On any kind of delete (EXCPET undo and redo): 
    # 1. empty redoList
    # 2. append all characters deleted to undoList

    # On any kind of insert (EXCPET undo and redo):
    # 1. empty redoList
    # 2. append all characters inserted to undoList

    def alterText(textBox):

        textBox.edit_modified(False)
        if CardCreator.isModified:
            print("UNDO STACK" ,CardCreator.frontTag_undo_stack)
            print("REDO STACK", CardCreator.frontTag_redo_stack)
        # if CardCreator.num_redo > 0:
        #     for c in range(0, CardCreator.num_redo):
        #         if CardCreator.isFrontFocused:
        #             char_info = CardCreator.frontTag_redo_stack.pop()
        #         else:
        #             char_info = CardCreator.backTag_redo_stack.pop()
        #         for tag in char_info[1]:
        #             event.widget.tag_add(tag, char_info[0])
        #     CardCreator.num_redo = 0
            print(CardCreator.current_insert)
            print(CardCreator.isDelete)

            print("CURRENT", CardCreator.current_insert)
            if CardCreator.isUndo and len(CardCreator.current_insert) == 0 and not CardCreator.isDelete:
                for char_num in reversed(range(0, CardCreator.num_appended)):
                    if CardCreator.isFrontFocused:
                        for tag in CardCreator.frontTag_redo_stack[len(CardCreator.frontTag_redo_stack) - char_num - 1][1]:
                                textBox.tag_add(tag, index1 = textBox.index("insert -" + str(char_num + 1) + "c"))
                    else:
                        for tag in CardCreator.backTag_redo_stack[len(CardCreator.backTag_redo_stack) - char_num - 1][1]:
                            textBox.tag_add(tag, index1 = textBox.index("insert -" + str(char_num + 1) + "c"))     
            elif len(CardCreator.current_insert) == 0 and not CardCreator.isDelete:
                
                for char_num in reversed(range(0, CardCreator.num_appended)):
                    if CardCreator.isFrontFocused:
                        for tag in CardCreator.frontTag_undo_stack[len(CardCreator.frontTag_undo_stack) - char_num - 1][1]:
                            textBox.tag_add(tag, index1 = textBox.index("insert -" + str(char_num + 1) + "c"))
                    else:
                        for tag in CardCreator.backTag_undo_stack[len(CardCreator.backTag_undo_stack) - char_num - 1][1]:
                            textBox.tag_add(tag, index1 = textBox.index("insert -" + str(char_num + 1) + "c"))
            else:
                if len(CardCreator.current_insert) == 2:
                    if CardCreator.underlined[not CardCreator.isFrontFocused]:
                        textBox.tag_add("underline_tag", textBox.index("insert -" + str(CardCreator.current_insert[1] + 1) + "c"), textBox.index("insert"))
                    else:
                        textBox.tag_remove("underline_tag", textBox.index("insert -" + str(CardCreator.current_insert[1] + 1) + "c"),  textBox.index("insert"))   
                    #  event.widget.tag_add(tag, index1 = event.widget.index("insert -" + str(char_num) + "c"))
                    
                    for char_num in reversed(range(0, CardCreator.current_insert[1])):
                        if CardCreator.isFrontFocused:
                            CardCreator.frontTag_undo_stack.append([textBox.index("insert -" + str(char_num + 1) + "c"), textBox.tag_names("insert -" + str(char_num + 1) + "c"), textBox.index("insert -" + str(char_num + 1) + "c"), CardCreator.total_frontTag_ids])
                            CardCreator.total_frontTag_ids += 1
                        else:
                            CardCreator.backTag_undo_stack.append([textBox.index("insert -" + str(char_num + 1) + "c"), textBox.tag_names("insert -" + str(char_num+ 1) + "c"), textBox.index("insert -" + str(char_num + 1) + "c"), CardCreator.total_backTag_ids])
                            CardCreator.total_backTag_ids += 1

                        CardCreator.num_appended += 1
                print("UNDO STACK AFTER" ,CardCreator.frontTag_undo_stack)
                print("REDO STACK AFTER", CardCreator.frontTag_redo_stack)
            CardCreator.updateStacks(textBox) 
 
 
            # CardCreator.current_insert.clear()
            # CardCreator.num_appended = 0
            
            CardCreator.isModified = False
        else:
            CardCreator.isModified = True
        
            # if CardCreator.underlined[not CardCreator.isFrontFocused]:
            #     event.widget.tag_add("underline_tag", index1 = event.widget.index("insert-1c"))
            # else:
            #     event.widget.tag_remove("underline_tag", index1 = event.widget.index("insert-1c"), index2 = event.widget.index("insert"))  
    def updateStacks(textBox):


        def plusOrMinus():
            if CardCreator.isDelete:
                return "-"
            else:
                return "+"


        appendedCounter = CardCreator.num_appended
        index_list = []
        if len(CardCreator.current_insert) == 0 and not CardCreator.isNotUndoRedoDelete:
            
            if CardCreator.isFrontFocused:
                iteration1 = CardCreator.frontTag_redo_stack
                iteration2 = CardCreator.frontTag_undo_stack
                if CardCreator.isUndo:
                    id_stack1 = [el[3] for el in CardCreator.frontTag_undo_stack]
                    id_stack2 = [el[3] for el in CardCreator.frontTag_redo_stack[0: len(iteration1) - CardCreator.num_appended]]
                else:
                    id_stack1 = [el[3] for el in CardCreator.frontTag_redo_stack]
                    id_stack2 = [el[3] for el in CardCreator.frontTag_undo_stack[0: len(iteration2) - CardCreator.num_appended]]

            else:
                iteration1 = CardCreator.backTag_redo_stack
                iteration2 = CardCreator.backTag_undo_stack
                if CardCreator.isUndo:
                    id_stack1 = [el[3] for el in CardCreator.backTag_undo_stack]
                    id_stack2 = [el[3] for el in CardCreator.backTag_redo_stack[0: len(iteration1) - CardCreator.num_appended]]
                    
                else:
                    id_stack1 = [el[3] for el in CardCreator.backTag_redo_stack]
                    id_stack2 = [el[3] for el in CardCreator.backTag_undo_stack[0: len(iteration2) - CardCreator.num_appended]]

                
            action_count = CardCreator.num_appended

            if CardCreator.isUndo:
                # action_count = 0
                print("NUM APPENDED" ,CardCreator.num_appended)

                action_origin = iteration1[len(iteration1) -  CardCreator.num_appended][0]
                print(len(iteration1) -  CardCreator.num_appended)

                index_list = iteration1[len(iteration1) -  CardCreator.num_appended: len(iteration1)]
                # print(len(iteration2) -  CardCreator.num_appended - 1, len(iteration2))
            else:
                print("NUM APPENDED" ,CardCreator.num_appended)
                print("ITERATION2", iteration2)
                action_origin = iteration2[len(iteration2) -  CardCreator.num_appended][0]
                index_list = iteration2[len(iteration2) -  CardCreator.num_appended: len(iteration2)]
            current_index_list = [el[2] for el in index_list]
            print(action_origin)
            print(index_list)
            for action in index_list:
                if CardCreator.isDelete:
                    print("YES")
                    if CardCreator.isUndo and CardCreator.isFrontFocused:
                        print("STACKS 1 and 2" ,id_stack1, id_stack2)
                        if action[3] in id_stack1:
                            CardCreator.frontTag_undo_stack[id_stack1.index(action[3])][2], CardCreator.frontTag_redo_stack[len(iteration1) - action_count][2] = None, None
                        elif action[3] in id_stack2:
                            print("COUNT",action_count)
                            CardCreator.frontTag_redo_stack[id_stack2.index(action[3])][2], CardCreator.frontTag_redo_stack[len(iteration1) - action_count][2] = None, None
                        else:
                            #  print( "HERE",len(iteration2) - action_count)
                            #  print(len(iteration2), action_count)
                             CardCreator.frontTag_redo_stack[len(iteration1) - action_count][2] = None
                    elif CardCreator.isUndo and not CardCreator.isFrontFocused:
                        if action[3] in id_stack1:
                            CardCreator.backTag_undo_stack[id_stack1.index(action[3])][2], CardCreator.backTag_redo_stack[len(iteration1) - action_count][2] = None, None
                        elif action[3] in id_stack2:
                            CardCreator.backTag_redo_stack[id_stack2.index(action[3])][2], CardCreator.backTag_redo_stack[len(iteration1) - action_count][2] = None, None 
                        else:
                            CardCreator.backTag_redo_stack[len(iteration1) - action_count][2] = None
                        # CardCreator.backTag_undo_stack[id_stack1.index(action[3])][2], CardCreator.backTag_redo_stack[current_index_list.index(action[2])] = None, None
                    elif not CardCreator.isUndo and CardCreator.isFrontFocused:
                        if action[3] in id_stack1:
                            CardCreator.frontTag_redo_stack[id_stack1.index(action[3])][2], CardCreator.frontTag_undo_stack[len(iteration2) - action_count][2] = None, None
                        elif action[3] in id_stack2:
                            CardCreator.frontTag_undo_stack[id_stack2.index(action[3])][2], CardCreator.frontTag_undo_stack[len(iteration2) - action_count][2] = None, None
                        else:
                            CardCreator.frontTag_undo_stack[len(iteration2) - action_count][2] = None
                    else:
                        if action[3] in id_stack1:
                            CardCreator.backTag_redo_stack[id_stack1.index(action[3])][2], CardCreator.backTag_undo_stack[len(iteration2) - action_count][2] = None, None
                        elif action[3] in id_stack2:
                            CardCreator.backTag_undo_stack[id_stack2.index(action[3])][2], CardCreator.backTag_undo_stack[len(iteration2) - action_count][2] = None, None
                        else:
                            CardCreator.backTag_undo_stack[len(iteration2) - action_count][2] = None
                        # CardCreator.backTag_redo_stack[id_stack1.index(action[3])][2] = None
                # elif  CardCreator.isDelete:
                #     if CardCreator.isUndo and CardCreator.isFrontFocused:
                #         CardCreator.frontTag_undo_stack[id_stack1.index(action[3])][2] = None
                #     elif CardCreator.isUndo and not CardCreator.isFrontFocused:
                #         CardCreator.backTag_undo_stack[id_stack1.index(action[3])][2] = None
                #     elif not CardCreator.isUndo and CardCreator.isFrontFocused:
                #         CardCreator.frontTag_redo_stack[id_stack1.index(action[3])][2] = None
                #     else:
                #         CardCreator.backTag_redo_stack[id_stack1.index(action[3])][2] = None

                else:
                    if CardCreator.isUndo and CardCreator.isFrontFocused:
                        if action[3] in id_stack1:
                            print(CardCreator.frontTag_redo_stack)
                            CardCreator.frontTag_undo_stack[id_stack1.index(action[3])][2], CardCreator.frontTag_redo_stack[len(iteration1)- action_count][2] = action[0], action[0]
                        elif action[3] in id_stack2:
                            CardCreator.frontTag_redo_stack[id_stack2.index(action[3])][2], CardCreator.frontTag_redo_stack[len(iteration1)- action_count][2] = action[0], action[0]
                        else:
                            CardCreator.frontTag_redo_stack[len(iteration1) - action_count][2] = action[0]
                        # CardCreator.frontTag_undo_stack[id_stack.index(action[3])][2] = CardCreator.frontTag_redo_stack[action_count][2]
                    elif CardCreator.isUndo and not CardCreator.isFrontFocused:
                        if action[3] in id_stack1:
                            CardCreator.backTag_undo_stack[id_stack1.index(action[3])][2], CardCreator.backTag_redo_stack[len(iteration1)- action_count][2] = action[0], action[0]
                        elif action[3] in id_stack2:
                            CardCreator.backTag_redo_stack[id_stack2.index(action[3])][2], CardCreator.backTag_redo_stack[len(iteration1)- action_count][2] = action[0], action[0]
                        else:
                            CardCreator.backTag_redo_stack[len(iteration1) - action_count][2] = action[0]
                        # CardCreator.backTag_undo_stack[id_stack.index(action[3])][2] = CardCreator.backTag_redo_stack[action_count][2]
                    elif not CardCreator.isUndo and CardCreator.isFrontFocused:
                        if action[3] in id_stack1:
                            CardCreator.frontTag_redo_stack[id_stack1.index(action[3])][2], CardCreator.frontTag_undo_stack[len(iteration2) - action_count][2] = action[0], action[0]
                        elif action[3] in id_stack2:
                            CardCreator.frontTag_undo_stack[id_stack2.index(action[3])][2], CardCreator.frontTag_undo_stack[len(iteration2) - action_count][2] = action[0], action[0]
                        else:
                            CardCreator.frontTag_undo_stack[len(iteration2) - action_count][2] = action[0]
                        # CardCreator.frontTag_redo_stack[id_stack.index(action[3])][2] = CardCreator.frontTag_undo_stack[len(iteration2) -  action_count - 1][2]
                    else:
                        if action[3] in id_stack1:
                            CardCreator.backTag_redo_stack[id_stack1.index(action[3])][2], CardCreator.backTag_undo_stack[len(iteration2) - action_count][2] = action[0], action[0]
                        elif action[3] in id_stack2:
                            CardCreator.backTag_undo_stack[id_stack2.index(action[3])][2], CardCreator.backTag_undo_stack[len(iteration2) - action_count][2] = action[0], action[0]
                        else:
                            CardCreator.backTag_undo_stack[len(iteration2) - action_count][2] = action[0]
                        # CardCreator.backTag_redo_stack[id_stack.index(action[3])][2] = CardCreator.backTag_undo_stack[len(iteration2) -  action_count - 1][2]
                action_count -= 1

            current_id_stack = [el[3] for el in index_list]
            action_count = 0
            for action in iteration1:
                if not action[3] in current_id_stack and action[2] != None and float(action[2]) >= float(action_origin):
                    if CardCreator.isFrontFocused:
                        CardCreator.frontTag_redo_stack[action_count][2] = textBox.index(CardCreator.frontTag_redo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")
                    else:
                        CardCreator.backTag_redo_stack[action_count][2] = textBox.index(CardCreator.backTag_redo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")

                action_count += 1

            action_count = 0
            print(iteration2)

            for action in iteration2:
                if not action[3] in current_id_stack and action[2] != None and float(action[2]) >= float(action_origin):
                    if CardCreator.isFrontFocused:
                        CardCreator.frontTag_undo_stack[action_count][2] = textBox.index(CardCreator.frontTag_undo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")
                    else:
                        CardCreator.backTag_undo_stack[action_count][2] = textBox.index(CardCreator.backTag_undo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")
                action_count += 1            



        # elif len(CardCreator.current_insert) == 0 and not CardCreator.isNotUndoRedoDelete: 
        #     action_count = 0
        #     if CardCreator.isFrontFocused:
        #         iteration = CardCreator.frontTag_redo_stack
        #     else:
        #         iteration = CardCreator.backTag_redo_stack
        #     for action in iteration:
        #         if action_count < CardCreator.num_appended:
        #             if appendedCounter >= 1:
        #                 if appendedCounter == 1:
        #                     if CardCreator.isFrontFocused:
        #                         action_origin = CardCreator.frontTag_redo_stack[action_count][0]
        #                     else:
        #                         action_origin = CardCreator.backTag_redo_stack[action_count][0]

        #                 if CardCreator.isDelete:
        #                     if CardCreator.isFrontFocused:
        #                         CardCreator.frontTag_redo_stack[action_count][2] = None
                                
        #                     else:
        #                         CardCreator.backTag_redo_stack[action_count][2] = None
        #                 else:
        #                     if CardCreator.isFrontFocused:
        #                         CardCreator.frontTag_redo_stack[action_count][2] = CardCreator.frontTag_redo_stack[action_count][0]
        #                     else:
        #                         CardCreator.backTag_redo_stack[action_count][2] = CardCreator.backTag_redo_stack[action_count][0]

        #                 appendedCounter -= 1
        #             else:
        #                 if CardCreator.isFrontFocused:
        #                     if CardCreator.frontTag_redo_stack[action_count][2] != None and float(CardCreator.frontTag_redo_stack[action_count][2]) > float(action_origin):
        #                         CardCreator.frontTag_redo_stack[action_count][2] = textBox.index(CardCreator.frontTag_redo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")
        #                 else:
        #                     if CardCreator.backTag_redo_stack[action_count][2] != None and float(CardCreator.backTag_redo_stack[action_count][2]) > float(action_origin):
        #                         CardCreator.backTag_redo_stack[action_count][2] = textBox.index(CardCreator.backTag_redo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")
        #         action_count += 1
        else:
            if CardCreator.isFrontFocused:
                iteration = CardCreator.frontTag_undo_stack
            else:
                iteration = CardCreator.backTag_undo_stack
            action_count = 0 
            index_list = iteration[len(iteration) - CardCreator.num_appended: len(iteration)]
            current_index_list = [el[2] for el in index_list]
            current_id_stack = [el[3] for el in index_list]

            action_origin = iteration[len(iteration) - CardCreator.num_appended][0]
            print("CURRENT DELETE INDEX LIST", current_index_list)
            print("ORIGIN", action_origin)
            for action in iteration:
                
                print("OH BOY", action)
                if CardCreator.isDelete and action[3] in current_id_stack:
                    print(action)
                    print(current_index_list)
                    if CardCreator.isFrontFocused:
                        CardCreator.frontTag_undo_stack[current_id_stack.index(action[3] )][3] = action[3]
                        CardCreator.frontTag_undo_stack[len(iteration) -  current_id_stack.index(action[3]) - 1][2], CardCreator.frontTag_undo_stack[action_count][2] = None, None
                    else:
                        CardCreator.backTag_undo_stack[len(iteration) -  current_id_stack.index(action[3]) - 1][3] = action[3]
                        CardCreator.backTag_undo_stack[len(iteration) -  current_id_stack.index(action[3]) - 1][2], CardCreator.backTag_undo_stack[action_count][2] = None, None
                else:
                    if CardCreator.isFrontFocused:
                        if not action[3] in current_id_stack and CardCreator.frontTag_undo_stack[action_count][2] != None and float(CardCreator.frontTag_undo_stack[action_count][2]) >= float(action_origin):
                            CardCreator.frontTag_undo_stack[action_count][2] = textBox.index(CardCreator.frontTag_undo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")
                    else:
                        if not action[3] in current_id_stack and CardCreator.backTag_undo_stack[action_count][2] != None and float(CardCreator.backTag_undo_stack[action_count][2]) >= float(action_origin):
                            CardCreator.backTag_undo_stack[action_count][2] = textBox.index(CardCreator.backTag_undo_stack[action_count][2] + plusOrMinus() + str(CardCreator.num_appended) + "c")
                action_count += 1
        CardCreator.isNotUndoRedoDelete = False
        CardCreator.isDelete = False
        CardCreator.isInsert = False
        CardCreator.current_insert.clear()
        CardCreator.num_appended = 0
        print("FINISHED UNDO STACK", CardCreator.frontTag_undo_stack)
        print("FINISHED REDO STACK", CardCreator.frontTag_redo_stack)

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
        CardCreator.frontTag_undo_stack.clear()
        CardCreator.frontTag_redo_stack.clear()
        
        CardCreator.backTag_undo_stack.clear()
        CardCreator.backTag_redo_stack.clear()
        CardCreator.total_backTag_ids = 0


        CardCreator.mainFrame.destroy()
        CardCreator.optionsFrame.destroy()

    def backToMenu():
        CardCreator.cardCreatorDestroy()
        cm.cardMenu.cardMenuCreate()