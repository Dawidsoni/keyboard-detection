from Tkinter import *

class LayoutPopup(object):
    SELECT_OPTIONS = ["stable", "rotated"]

    def __init__(self, root):
        self.top = Toplevel(root)
        self.input_value = None
        self.select_value = None
        self.input_label = Label(self.top, text="Please enter layout name")
        self.input_label.pack()
        self.input_entry = Entry(self.top)
        self.input_entry.pack()
        self.input_entry.focus()
        self.select_label = Label(self.top, text="Please select layout type")
        self.select_label.pack()
        self.select_var = StringVar(self.top)
        self.select_var.set(LayoutPopup.SELECT_OPTIONS[0])
        self.select_input = OptionMenu(self.top, self.select_var, *LayoutPopup.SELECT_OPTIONS)
        self.select_input.pack()
        self.input_button = Button(self.top, text='OK', command=self.cleanup)
        self.input_button.pack()
        self.top.bind("<Return>", lambda _: self.cleanup())

    def cleanup(self):
        self.input_value = self.input_entry.get()
        self.select_value = self.select_var.get()
        self.top.destroy()


