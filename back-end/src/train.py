import os
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from preprocess import preprocess_image, load_labels, enhance_image
from model import SingleHeadModel

class ImageDataset(Dataset):
    def __init__(self, image_dir, labels, label_map, augment=False):
        self.image_dir = image_dir
        self.labels = labels  # Dictionary with filenames as keys
        self.label_map = label_map
        self.augment = augment
        self.image_list = list(self.labels.keys())  # List of filenames

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        filename = self.image_list[idx]
        label = self.labels[filename]
        image_path = os.path.join(self.image_dir, filename)
        img = preprocess_image(image_path)
        if self.augment:
            img = enhance_image(img,'data/enhanced',filename)
        return img, self.label_map[label]

# Define label mapping and load labels
label_map = {'heated': 0, 'natural': 1, 'synthetic': 2}
labels = load_labels('data/labels.csv')
image_dir = 'data/images/'

# Load dataset and initialize DataLoader
dataset = ImageDataset(image_dir, labels, label_map, augment=False)
train_loader = DataLoader(dataset, batch_size=39, shuffle=True)

# Initialize model, loss function, and optimizer
model = SingleHeadModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    for imgs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

# Save model
torch.save(model.state_dict(), 'model.pth')
