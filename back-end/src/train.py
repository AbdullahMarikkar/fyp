import os
import numpy as np
import pandas as pd
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from src.preprocess import (
    preprocess_image,
    load_labels,
    gaussian_blur,
    histogram_equalization,
)
from src.model import SingleHeadModel


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
            img = histogram_equalization(img, "data/enhanced", filename)
            img = gaussian_blur(img, save_dir="data/gaussian", filename=filename)
        return img, self.label_map[label]


# Define label mapping and load labels
label_map = {"heated": 0, "natural": 1, "synthetic": 2}
labels = load_labels("data/labels.csv")
image_dir = "data/images/"

# Load dataset and initialize DataLoader
dataset = ImageDataset(image_dir, labels, label_map, augment=False)

# Shuffle dataset before splitting
indices = np.random.permutation(len(dataset))  # Generate shuffled indices

# Compute train-test split sizes
train_size = int(0.70 * len(dataset))
test_size = len(dataset) - train_size

# Split dataset using shuffled indices
train_indices, test_indices = indices[:train_size], indices[train_size:]

# Create train and test datasets using the shuffled indices
train_dataset = torch.utils.data.Subset(dataset, train_indices)
test_dataset = torch.utils.data.Subset(dataset, test_indices)

# Save test dataset filenames to a CSV file
test_filenames = [dataset.image_list[i] for i in test_indices]
test_df = pd.DataFrame({"filename": test_filenames})
test_df.to_csv("data/test_split.csv", index=False)

train_loader = DataLoader(train_dataset, batch_size=330, shuffle=True)

# Initialize model, loss function, and optimizer
model = SingleHeadModel()
# criterion = nn.CrossEntropyLoss() # TODO
criterion = nn.CrossEntropyLoss(weight=torch.tensor([1.2, 1.0, 1.4]))
optimizer = optim.Adam(model.parameters(), lr=0.00150)

# Training loop
num_epochs = 100
best_loss = float("inf")
for epoch in range(num_epochs):
    model.train()
    epoch_loss = 0.0
    for imgs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

    avg_epoch_loss = epoch_loss / len(train_loader)
    print(
        f"Epoch [{epoch + 1}/{num_epochs}] | Avg Loss: {avg_epoch_loss:.4f} | LR: {optimizer.param_groups[0]['lr']:.2e}"
    )

    # Save best model
    if avg_epoch_loss < best_loss:
        best_loss = avg_epoch_loss
        torch.save(model.state_dict(), "best_model.pth")
        print(f"New best model saved with loss: {best_loss:.4f}")

# Save model
torch.save(model.state_dict(), "model.pth")
