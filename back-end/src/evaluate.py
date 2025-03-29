import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from src.model import SingleHeadModel
from src.preprocess import preprocess_image, load_labels
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import classification_report, roc_curve, roc_auc_score


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
label_map = {"heated": 0, "natural": 1, "synthetic": 2}
labels = load_labels("data/labels.csv")
image_dir = "data/images/"

# Initialize dataset and DataLoader
dataset = ImageDataset(image_dir, labels, label_map)
data_loader = DataLoader(dataset, batch_size=39, shuffle=True)

# Load the trained model and evaluate
model = SingleHeadModel()
model.load_state_dict(torch.load("model.pth"))
model.eval()

all_labels = []
all_preds = []
all_probs = []

with torch.no_grad():
    for imgs, labels in data_loader:
        outputs = model(imgs)
        probs = torch.softmax(outputs, dim=1)
        _, preds = torch.max(outputs, 1)
        all_labels.extend(labels.numpy())
        all_preds.extend(preds.numpy())
        all_probs.extend(probs.numpy())

print(
    classification_report(
        all_labels, all_preds, target_names=["heated", "natural", "synthetic"]
    )
)

# Convert lists to NumPy arrays for AUC-ROC calculation
all_labels = np.array(all_labels)
all_probs = np.array(all_probs)  # Ensure all_probs is a NumPy array

# Compute AUC-ROC for each class (One-vs-Rest approach)
for i, class_name in enumerate(["heated", "natural", "synthetic"]):
    binary_labels = np.where(all_labels == i, 1, 0)  # Convert to binary labels
    fpr, tpr, _ = roc_curve(binary_labels, all_probs[:, i])  # type: ignore
    auc_score = roc_auc_score(binary_labels, all_probs[:, i])  # type: ignore

    # Plot ROC curve
    plt.plot(fpr, tpr, label=f"{class_name} (AUC = {auc_score:.2f})")

# Plot formatting
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")  # Diagonal line for reference
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("AUC-ROC Curve")
plt.legend()
plt.grid()
plt.show()
