import os
import torch
from model import SingleHeadModel
from preprocess import preprocess_image, load_labels
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import classification_report

class ImageDataset(Dataset):
    def __init__(self, image_dir, labels, label_map):
        self.image_dir = image_dir
        self.labels = labels
        self.label_map = label_map
        self.image_list = list(labels.keys())  # List of filenames

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        filename = self.image_list[idx]
        label = self.labels[filename]
        image_path = os.path.join(self.image_dir, filename)
        img = preprocess_image(image_path)
        return img, self.label_map[label]

# Define label mapping and load labels
label_map = {'heated': 0, 'natural': 1, 'synthetic': 2}
labels = load_labels('data/labels.csv')
image_dir = 'data/images/'

# Initialize dataset and DataLoader
dataset = ImageDataset(image_dir, labels, label_map)
data_loader = DataLoader(dataset, batch_size=39, shuffle=True)

# Load the trained model and evaluate
model = SingleHeadModel()
model.load_state_dict(torch.load('model.pth'))
model.eval()

all_labels = []
all_preds = []

with torch.no_grad():
    for imgs, labels in data_loader:
        outputs = model(imgs)
        _, preds = torch.max(outputs, 1)
        all_labels.extend(labels.numpy())
        all_preds.extend(preds.numpy())

print(classification_report(all_labels, all_preds, target_names=['heated', 'natural', 'synthetic']))
