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
    save_generator_sample(rotate_generator, 'generators/rotate_generator.jpg', 30)
    save_generator_sample(in_place_generator, 'generators/in_place_generator.jpg', 30)
    return rotate_generator, in_place_generator

def train():
    rotate_generator, in_place_generator = get_image_generators()
    model = ConvDenseNet(12, 40, 0.5, 37, True).cuda()
    model = load_conv_dense_net('state_dicts/train/rotate8.pt', 40)
    model_trainer = ModelTrainer('state_dicts/train/rotate8', model, rotate_generator, 500)
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    model_trainer.train(optimizer, 200)
    optimizer = optim.Adam(model.parameters(), lr=0.003)
    model_trainer.train(optimizer, 100)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    model_trainer.train(optimizer, 100)
    optimizer = optim.Adam(model.parameters(), lr=0.0003)
    model_trainer.train(optimizer, 100)
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    model_trainer.train(optimizer, 100)

train()
