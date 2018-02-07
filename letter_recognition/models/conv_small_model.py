import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvSmallNet(nn.Module):
    def __init__(self):
        super(ConvSmallNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 5, padding=2)
        self.conv2 = nn.Conv2d(32, 64, 5, padding=2)
        self.fc1 = nn.Linear(64 * 8 * 8, 1024)
        self.fc2 = nn.Linear(1024, 37)
                                                    
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, 64 * 8 * 8)  
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x)
