from Tkinter import *

class LetterInputPopup(object):
    def __init__(self, root):
        self.top = Toplevel(root)
        self.input_value = None
        self.input_label = Label(self.top, text="Please enter letter")
        self.input_label.pack()
        self.input_entry = Entry(self.top)
        self.input_entry.pack()
        self.input_entry.focus()
        self.input_button = Button(self.top, text='OK', command=self.cleanup)
        self.input_button.pack()
        self.top.bind("<Return>", lambda _: self.cleanup())

    def cleanup(self):
        self.input_value = self.input_entry.get()
        self.top.destroy()
