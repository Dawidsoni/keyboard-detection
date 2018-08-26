from PIL import Image, ImageDraw
import random
import numpy as np
from . import ShapeGenerator

class EdgeGenerator:
    COLOR_OFFSET = 30
    BOX_OFFSET = 6
    SHAPED_IMAGE_POS = (32, 32, 64, 64)

    def __init__(self, image, params):
        self.image = image
        self.params = params
        self.im_draw = ImageDraw.Draw(image)

    def generate_bounding_box(self):
        if self.params.text == ' ':
            return [(0, 0), self.image.size]
        col_arr = np.array(self.image)
        min_col = self.params.color - self.COLOR_OFFSET 
        max_col = self.params.color + self.COLOR_OFFSET
        rows, cols = np.where(np.logical_and(col_arr >= min_col, col_arr <= max_col))
        if len(rows) == 0 or len(cols) == 0:
            return [(0, 0), self.image.size]
        start_pos = (np.min(rows) - self.BOX_OFFSET, np.min(cols) - self.BOX_OFFSET)
        end_pos = (np.max(rows) + self.BOX_OFFSET, np.max(cols) + self.BOX_OFFSET)
        return (start_pos, end_pos)

    def generate_edges(self):
        bounding_box = self.generate_bounding_box()
        bounding_image = self.image.crop(bounding_box[0] + bounding_box[1])
        shaped_image = self.image.crop(self.SHAPED_IMAGE_POS)
        ShapeGenerator(shaped_image, self.params.color).generate_shape()
        self.image.paste(shaped_image, self.SHAPED_IMAGE_POS)
        self.image.paste(bounding_image, bounding_box[0] + bounding_box[1])
