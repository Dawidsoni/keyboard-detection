from core import ImageGenerator
from core import ModelTrainer
from models import BaseDenseNet
from models import ConvDenseNet
import torch.optim as optim
from utils.plot import *
from utils.model import *

def get_image_generators():
    rotate_generator = ImageGenerator(120, True, True)
    in_place_generator = ImageGenerator(120, False, True)
    save_generator_sample(rotate_generator, 'generators/rotate_generator.jpg')
    save_generator_sample(in_place_generator, 'generators/in_place_generator.jpg')
    return rotate_generator, in_place_generator

def train():
    rotate_generator, in_place_generator = get_image_generators()
    model = load_conv_dense_net('state_dicts/eval/in_place_m20_conv_dense.pt', 20)#ConvDenseNet(12, 20, 0.5, 37, True).cuda()
    optimizer = optim.Adam(model.parameters(), lr=0.0003)
    model_trainer = ModelTrainer('state_dicts/train/in_place1', model, in_place_generator, 1500)
    model_trainer.train(optimizer, 1000)

train()
