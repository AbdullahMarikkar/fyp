# src/evaluate.py

import torch
from sklearn.metrics import classification_report
from torch.utils.data import DataLoader
from model import create_model
from train import ImageDataset, load_labels, label_map

# Load model and data
model = create_model()
model.load_state_dict(torch.load('model.pth'))
model.eval()

labels = load_labels('data/labels.csv')
images = list(labels.keys())
val_dataset = ImageDataset(images, labels, label_map)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Evaluate
all_thermal_labels = []
all_natural_labels = []
all_thermal_preds = []
all_natural_preds = []

with torch.no_grad():
    for imgs, y_thermal, y_natural in val_loader:
        thermal_pred, natural_pred = model(imgs)
        
        all_thermal_labels.extend(y_thermal.numpy())
        all_natural_labels.extend(y_natural.numpy())
        all_thermal_preds.extend(torch.argmax(thermal_pred, dim=1).numpy())
        all_natural_preds.extend(torch.argmax(natural_pred, dim=1).numpy())

# Classification reports
print("Thermal State Classification Report:")
print(classification_report(
    all_thermal_labels, 
    all_thermal_preds, 
    target_names=['heated', 'unheated'], 
    labels=[0, 1]
))

print("\nNatural State Classification Report:")
print(classification_report(
    all_natural_labels, 
    all_natural_preds, 
    target_names=['natural', 'synthetic'], 
    labels=[0, 1]
))
