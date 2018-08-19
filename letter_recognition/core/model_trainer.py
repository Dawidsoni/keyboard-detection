import string
import torch
import torch.cuda
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
from sklearn.preprocessing import StandardScaler
import numpy as np

class ModelTrainer:
    def __init__(self, exp_name, model, image_generator, batch_size):
        self.exp_name = exp_name
        self.model = model
        self.image_generator = image_generator
        self.batch_size = batch_size
        self.char_list = list(string.ascii_uppercase + string.digits)

    def map_image_type_to_target(self, image_type):
        (letter, angle_bucket) = image_type
        if letter not in self.char_list:
            return 0
        return 1 + self.char_list.index(letter) + len(self.char_list) * angle_bucket   

    def generate_images(self, image_count):
        data_list = []
        target_list = []
        for i in range(image_count):
            image_type, data = self.image_generator.generate_image()
            target_list.append(self.map_image_type_to_target(image_type))        
            data_list.append(data.flatten())
        data_arr = np.array(data_list, dtype=np.float64)
        target_arr = np.array(target_list, dtype=np.int64)
        return data_arr, target_arr

    def generate_data(self):
        while True:
            data_arr, target_arr = self.generate_images(self.batch_size)
            data_arr = data_arr.reshape(-1, 1, 32, 32)
            data_var = Variable(torch.FloatTensor(data_arr).cuda())
            target_var = Variable(torch.LongTensor(target_arr).cuda())
            yield (data_var, target_var)
    
    def print_accuracy(self, data_name, pred_data, target_data):
        accuracy = pred_data.eq(target_data).sum().float() / float(len(pred_data)) * 100
        print("Accuracy (%s): %.3f" % (data_name, accuracy))    
    
    def train(self, optimizer, iter_count):
        self.model.train()
        for i in range(iter_count):
            train_data, train_target = self.generate_data().next()
            optimizer.zero_grad()
            train_pred = self.model(train_data)
            loss = F.nll_loss(train_pred, train_target)
            loss.backward()    
            optimizer.step()   
            if i % 10 == 0:
                self.print_accuracy("Train set", train_pred.data.max(1)[1], train_target.data)
                print("Loss: %.4f" % (loss.data))
                torch.save(self.model.state_dict(), "{0}.pt".format(self.exp_name))
                print("\n")

    def eval_model(self, iter_count):
        self.model.eval()
        for i in range(iter_count):
            test_data, test_target = self.generate_data().next()
            test_pred = self.model(test_data)
            self.print_accuracy("Test set", test_pred.data.max(1)[1], test_target.data)
