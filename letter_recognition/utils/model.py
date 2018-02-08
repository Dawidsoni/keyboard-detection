from models import BaseDenseNet
from models import ConvDenseNet
import torch
from torch.autograd import Variable
import string
import numpy as np

def load_state(filename, model_obj):
    model_obj.load_state_dict(torch.load(filename))

def load_base_dense_net(filename, layer_count):
    model = BaseDenseNet(12, layer_count, 0.5, 37, True).cuda()
    load_state(filename, model)
    return model

def load_conv_dense_net(filename, layer_count):
    model = ConvDenseNet(12, layer_count, 0.5, 37, True).cuda()
    load_state(filename, model)
    return model

def encode_class(class_num):
    char_list = [' '] + list(string.ascii_uppercase + string.digits)
    return char_list[class_num]

def get_output_data(model, image_data):
    var_data = Variable(torch.FloatTensor(image_data).cuda())
    output_data = model(var_data)
    return output_data.cpu().data.numpy()

def get_paded_image(image):
    pad_func = (lambda x: x if x % 32 == 0 else x - (x % 32) + 32)
    paded_image = np.zeros((pad_func(image.shape[0]), pad_func(image.shape[1])))
    paded_image[:image.shape[0], :image.shape[1]] = image
    return paded_image

def create_chunked_data(image, dim_chunk_count):
    dim_size = dim_chunk_count * 32
    if image.size[0] > image.size[1]:
        image = image.resize((dim_size, int(image.size[1] * float(dim_size) / image.size[0])))
    else:
        image = image.resize((int(image.size[0] * float(dim_size) / image.size[1]), dim_size))
    chunked_data = get_paded_image(np.array(image, dtype=np.float64))
    data_shape = chunked_data.shape
    chunked_data = np.split(chunked_data, data_shape[0] / 32)
    chunked_data = map(lambda x: np.split(x, data_shape[1] / 32, axis=1), chunked_data)
    return np.array(chunked_data)
