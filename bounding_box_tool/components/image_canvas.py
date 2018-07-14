from Tkinter import *
from PIL import Image, ImageTk
import pickle
import os
from . import LetterInputPopup


class ImageCanvas(Frame):
    TEXT_OFFSET = 10

    def __init__(self, filepath=None, root=None):
        Frame.__init__(self, root)
        self.filepath = filepath
        self.root = root
        self.pack(expand=YES, fill=BOTH)
        self.cur_rect_x, self.cur_rect_y = (0, 0)
        self.rect_images = []
        self.letter_images = []
        self.canv = Canvas(self, relief=SUNKEN)
        self.canv.config(width=1024, height=768)
        self.image = None
        if filepath is not None:
            self._load_image(filepath)

    def _load_image(self, filename):
        self.image = Image.open(filename)
        self._add_vertical_scrollbar(self.canv)
        self._add_horizontal_scrollbar(self.canv)
        self.canv.pack(side=LEFT, expand=YES, fill=BOTH)
        self.canv.config(scrollregion=(0, 0, self.image.size[0], self.image.size[1]))
        self.canv_image = ImageTk.PhotoImage(self.image)
        self.canv.create_image(0, 0, anchor="nw", image=self.canv_image)
        self.canv.bind("<ButtonPress-1>", self._on_button_press)
        self.canv.bind("<B1-Motion>", self._on_move_press)
        self.canv.bind("<ButtonRelease-1>", self._on_button_release)

    def _add_vertical_scrollbar(self, canv):
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.config(command=canv.yview)
        canv.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _add_horizontal_scrollbar(self, canv):
        scrollbar = Scrollbar(self, orient=HORIZONTAL)
        scrollbar.config(command=canv.xview)
        canv.config(xscrollcommand=scrollbar.set)
        scrollbar.pack(side=BOTTOM, fill=X)

    def _on_button_press(self, event):
        pos_x, pos_y = self.canv.canvasx(event.x), self.canv.canvasy(event.y)
        self.cur_rect_x, self.cur_rect_y = pos_x, pos_y
        self.add_rectangle(pos_x, pos_y, pos_x, pos_y)

    def _on_move_press(self, event):
        pos_x, pos_y = self.canv.canvasx(event.x), self.canv.canvasy(event.y)
        self.canv.coords(self.rect_images[-1], self.cur_rect_x, self.cur_rect_y, pos_x, pos_y)

    def _on_button_release(self, event):
        input_popup = LetterInputPopup(self)
        self.root.withdraw()
        self.wait_window(input_popup.top)
        self.root.deiconify()
        letter = input_popup.input_value
        if letter is None or len(letter) != 1:
            self.letter_images.append(None)
            self.undo_rectangle()
        else:
            letter = letter.upper()
            self.add_letter(letter)

    def add_rectangle(self, start_x, start_y, end_x, end_y):
        self.rect_images.append(self.canv.create_rectangle(start_x, start_y, end_x, end_y, outline="red", width=3))

    def add_letter(self, letter):
            px1, py1, px2, py2 = self.canv.coords(self.rect_images[-1])
            px, py = min(px1, px2) + ImageCanvas.TEXT_OFFSET, min(py1, py2) + ImageCanvas.TEXT_OFFSET
            self.letter_images.append(self.canv.create_text(px, py, fill="orange", text=letter, font="Times 20"))

    def undo_rectangle(self):
        if len(self.rect_images) == 0:
            return
        self.canv.delete(self.rect_images[-1])
        self.canv.delete(self.letter_images[-1])
        self.rect_images.pop()
        self.letter_images.pop()

    def create_letter_layout(self, rect_image, letter_image):
        px1, py1, px2, py2 = self.canv.coords(rect_image)
        return {
            'letter': self.canv.itemcget(letter_image, 'text'),
            'start_pos': (min(px1, px2), min(py1, py2)),
            'end_pos': (max(px1, px2), max(py1, py2))
        }

    def create_layout(self):
        return map(lambda x: self.create_letter_layout(*x), zip(self.rect_images, self.letter_images))

    def save_to_file(self, layout_name, layout_type):
        layout = {
            'layout_name': layout_name,
            'layout_type': layout_type,
            'letters': self.create_layout(),
            'filepath': self.filepath
        }
        filedir = os.path.dirname(self.filepath)
        pickle.dump(layout, open("{0}/{1}.layout".format(filedir, layout_name), 'w'))


class NullImageCanvas(ImageCanvas):
    def __init__(self):
        ImageCanvas.__init__(self)


class LoadedImageCanvas(ImageCanvas):
    def __init__(self, filename, root=None):
        layout = pickle.load(open(filename, 'r'))
        ImageCanvas.__init__(self, layout['filepath'], root)
        for layout_letter in layout['letters']:
            self._add_layout_letter(layout_letter)

    def _add_layout_letter(self, layout_letter):
        start_pos, end_pos = layout_letter['start_pos'], layout_letter['end_pos']
        letter = layout_letter['letter']
        self.add_rectangle(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
        self.add_letter(letter)

