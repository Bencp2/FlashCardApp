import tkinter as tk

class MyText(tk.Text):

    def __init__(self, master=None, **kw):
        tk.Text.__init__(self, master, undo=False, **kw)
        self._undo_stack = []
        self._redo_stack = []
        # create proxy
        self._orig = self._w + "_orig"
        self.tk.createcommand(self._w, self._proxy)


    def _proxy(self, *args):
        if args[0] in ["insert", "delete"]:
            if args[1] == "end":
                index = self.index("end-1c")
            else:
                index = self.index(args[1])
            if args[0] == "insert":
                undo_args = ("delete", index, "{}+{}c".format(index, len(args[2])))
            else:  # args[0] == "delete":
                undo_args = ("insert", index, self.get(*args[:1]))
            self._redo_stack.clear()
            self._undo_stack.append((undo_args, args))
        elif args[0] == "tag":
            if args[1] in ["add", "remove"] and args[2] != "sel":
                indexes = tuple(self.index(ind) for ind in args[3:])
                undo_args = ("tag", "remove" if args[1] == "add" else "add", args[2]) + indexes
                self._redo_stack.clear()
                self._undo_stack.append((undo_args, args))
        result = self.tk.call((self._orig,) + args)
        return result

    def undo(self):
        if not self._undo_stack:
            return
        undo_args, redo_args = self._undo_stack.pop()
        self._redo_stack.append((undo_args, redo_args))
        self.tk.call((self._orig,) + undo_args)

    def redo(self):
        if not self._redo_stack:
            return
        undo_args, redo_args = self._redo_stack.pop()
        self._undo_stack.append((undo_args, redo_args))
        self.tk.call((self._orig,) + redo_args)