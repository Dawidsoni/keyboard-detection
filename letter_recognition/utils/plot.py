from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import string
from .model import encode_class

def save_generator_sample(image_generator, output_file, row_size=5):
    image_data = []
    for i in range(row_size ** 2):
        _, image = image_generator.generate_image()
        image_data.append(image)
    combined_data = []
    for i in range(row_size):
        sliced_data = image_data[(row_size * i):(row_size * (i + 1))]
        combined_data.append(np.concatenate(sliced_data, axis=1))
    sample_data = np.concatenate(combined_data, axis=0)
    Image.fromarray(sample_data).save(output_file)

def plot_image(image, plot_size=None):
    if plot_size is not None:
        plt.figure(figsize=(16, 12))
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)               
    plt.show()

def plot_images_with_output(image_data, output_data):    
    output_ind = np.argsort(output_data)
    for i in range(image_data.shape[0]):
        ind1, ind2, ind3 = output_ind[i, -1], output_ind[i, -2], output_ind[i, -3]
        print(encode_class(ind1), encode_class(ind2), encode_class(ind3))
        prob_func = (lambda x: np.exp(output_data[i, x]))
        print(prob_func(ind1), prob_func(ind2), prob_func(ind3))
        plot_image(image_data[i, :, :, :].reshape(32, 32))
