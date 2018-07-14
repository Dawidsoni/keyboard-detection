from Tkinter import *
from tkFileDialog import askopenfilename
from components import LayoutPopup, ImageCanvas, LoadedImageCanvas, NullImageCanvas

def open_image(window):
    filename = askopenfilename()
    if len(filename) == 0:
        return
    window['canvas'].pack_forget()
    window['canvas'] = ImageCanvas(filename, window['root'])
    window['canvas'].mainloop()

def open_layout(window):
    filename = askopenfilename()
    if len(filename) == 0:
        return
    window['canvas'].pack_forget()
    window['canvas'] = LoadedImageCanvas(filename, window['root'])
    window['canvas'].mainloop()

def save_layout(window):
    layout_popup = LayoutPopup(window['root'])
    window['root'].withdraw()
    window['root'].wait_window(layout_popup.top)
    window['root'].deiconify()
    filename, layout_type = layout_popup.input_value, layout_popup.select_value
    if filename is None or len(filename) == 0:
        return 
    window['canvas'].save_to_file(filename, layout_type)

def undo_rectangle(window):
    window['canvas'].undo_rectangle()

def add_menu(window):
    menu_bar = Menu(window['root'])
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open image", command=lambda: open_image(window))
    file_menu.add_command(label="Open layout", command=lambda: open_layout(window))
    file_menu.add_command(label="Save layout", command=lambda: save_layout(window))
    menu_bar.add_cascade(label="File", menu=file_menu)
    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Undo", command=lambda: undo_rectangle(window))
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    window['root'].config(menu=menu_bar)

def main(): 
    window = {'root': Tk(), 'canvas': NullImageCanvas()}
    add_menu(window)
    window['root'].mainloop()

main()
