import torch
import torch.nn as nn
import torchvision.models as models

class SingleHeadModel(nn.Module):
    def __init__(self):
        super(SingleHeadModel, self).__init__()
        self.base_model = models.mobilenet_v2(pretrained=True)
        for param in self.base_model.parameters():
            param.requires_grad = False

        self.base_model = nn.Sequential(*list(self.base_model.children())[:-1], nn.AdaptiveAvgPool2d((1, 1)))
        self.classification_head = nn.Linear(1280, 3)  # Output for single classification (3 classes)

    def forward(self, x):
        x = self.base_model(x)
        x = x.view(x.size(0), -1)
        output = self.classification_head(x)
        return output
