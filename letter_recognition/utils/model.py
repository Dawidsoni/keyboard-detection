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

