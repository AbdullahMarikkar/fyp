# src/train.py

import os
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from preprocess import load_labels, preprocess_image, enhance_image
from model import create_model

class ImageDataset(Dataset):
    def __init__(self, image_list, labels, label_map, augment=False):
        self.image_list = image_list
        self.labels = labels
        self.label_map = label_map
        self.augment = augment

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        img_name = self.image_list[idx]
        img_path = os.path.join('data/images', img_name)
        img = preprocess_image(img_path)
        if self.augment:
            img = enhance_image(img)
        
        thermal_label = self.label_map['thermal'][self.labels[img_name][0]]
        natural_label = self.label_map['natural'][self.labels[img_name][1]]
        
        return img, thermal_label, natural_label

# Load labels and split dataset
labels = load_labels('data/labels.csv')
images = list(labels.keys())
train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)

# Define label mappings
label_map = {'thermal': {'heated': 0, 'unheated': 1}, 'natural': {'natural': 0, 'synthetic': 1}}

# Create datasets and dataloaders
train_dataset = ImageDataset(train_images, labels, label_map, augment=True)
val_dataset = ImageDataset(val_images, labels, label_map)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Initialize model, criterion, and optimizer
model = create_model()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for imgs, y_thermal, y_natural in train_loader:
        optimizer.zero_grad()
        thermal_pred, natural_pred = model(imgs)

        loss_thermal = criterion(thermal_pred, y_thermal)
        loss_natural = criterion(natural_pred, y_natural)
        loss = loss_thermal + loss_natural

        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

# Save model
torch.save(model.state_dict(), 'model.pth')
