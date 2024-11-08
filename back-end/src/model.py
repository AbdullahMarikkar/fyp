# src/model.py

import torch
import torch.nn as nn
import torchvision.models as models

class DualHeadModel(nn.Module):
    def __init__(self):
        super(DualHeadModel, self).__init__()
        # Load a pretrained model and freeze it
        self.base_model = models.mobilenet_v2(pretrained=True)
        for param in self.base_model.parameters():
            param.requires_grad = False

        # Replace the classifier with global average pooling
        self.base_model = nn.Sequential(*list(self.base_model.children())[:-1], nn.AdaptiveAvgPool2d((1, 1)))

        # Thermal classification head
        self.thermal_head = nn.Linear(1280, 2)
        
        # Natural classification head
        self.natural_head = nn.Linear(1280, 2)

    def forward(self, x):
        x = self.base_model(x)
        x = x.view(x.size(0), -1)  # Flatten
        thermal_output = self.thermal_head(x)
        natural_output = self.natural_head(x)
        return thermal_output, natural_output

def create_model():
    model = DualHeadModel()
    return model
