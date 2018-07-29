import numpy as np 
from math import ceil
import cv2
from . import FragmentShaper

class ChunkExtractor:
    def __init__(self, chunk_count=20):
        self.chunk_count = chunk_count

    def get_chunk_size(self, image):
        return int(ceil(max(image.shape[0], image.shape[1]) / float(self.chunk_count)))

    def get_paded_image(self, image, pad_size):
        pad_func = (lambda x: x if x % pad_size == 0 else x - (x % pad_size) + pad_size)
        paded_image = np.zeros((pad_func(image.shape[0]), pad_func(image.shape[1]), image.shape[2]), dtype=np.uint8)
        paded_image[:image.shape[0], :image.shape[1], :] = image
        return paded_image

    def create_chunked_data(self, image):
        chunk_size = self.get_chunk_size(image)
        image = self.get_paded_image(image, chunk_size)
        chunked_data = np.split(image, image.shape[0] / chunk_size)
        chunked_data = map(lambda x: np.split(x, x.shape[1] / chunk_size, axis=1), chunked_data)
        for row_ind, row_data in enumerate(chunked_data):
            for col_ind, col_data in enumerate(row_data):
                start_x, start_y = row_ind * chunk_size, col_ind * chunk_size
                end_x, end_y = start_x + chunk_size, start_y + chunk_size
                pos_data = {'start_pos': (start_x, start_y), 'end_pos': (end_x, end_y)}
                chunked_data[row_ind][col_ind] = (pos_data, chunked_data[row_ind][col_ind])
        return [item for row in chunked_data for item in row]

    def get_fragment_list(self, image):
        fragment_shaper = FragmentShaper()
        fragment_list = self.create_chunked_data(image)
        fragment_list = map(fragment_shaper.shape_fragment, fragment_list)
        return fragment_list
