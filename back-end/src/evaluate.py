import os
import pandas as pd
import torch
import numpy as np
import matplotlib.pyplot as plt
from model import SingleHeadModel
from preprocess import preprocess_image, load_labels
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import classification_report, roc_curve, roc_auc_score
from sklearn.metrics import confusion_matrix
import seaborn as sns


class TestDataset(Dataset):
    def __init__(self, image_dir, test_filenames, labels, label_map):
        self.image_dir = image_dir
        self.test_filenames = test_filenames  # List of test image filenames
        self.labels = labels
        self.label_map = label_map

    def __len__(self):
        return len(self.test_filenames)

    def __getitem__(self, idx):
        filename = self.test_filenames[idx]
        label = self.labels[filename]
        image_path = os.path.join(self.image_dir, filename)
        img = preprocess_image(image_path)
        return img, self.label_map[label]


# Load test filenames
test_df = pd.read_csv("data/test_split.csv")  # TODO : Change to test_split
test_filenames = test_df["filename"].tolist()  # TODO : Change to filename

# test_df = pd.read_csv("data/train_split.csv")
# test_filenames = test_df["filename"].tolist()

# Define label mapping and load labels
label_map = {"heated": 0, "natural": 1, "synthetic": 2}
labels = load_labels("data/labels_augmented.csv")
image_dir = "data/images/"

# Load test dataset
test_dataset = TestDataset(image_dir, test_filenames, labels, label_map)
test_loader = DataLoader(test_dataset, batch_size=141, shuffle=False)

# Load the trained model and evaluate
model = SingleHeadModel()
model.load_state_dict(torch.load("best_model.pth"))
model.eval()

all_labels = []
all_preds = []
all_probs = []

with torch.no_grad():
    for imgs, labels in test_loader:
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

# ==============================================================================
print("\n--- Generating Confusion Matrix ---")
# Compute confusion matrix
cm = confusion_matrix(all_labels, all_preds)

# Create a new figure for the confusion matrix plot
plt.figure(figsize=(8, 6))

# Use seaborn to create a visually appealing heatmap
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["heated", "natural", "synthetic"],
    yticklabels=["heated", "natural", "synthetic"],
)

# Add labels and a title
plt.title("Confusion Matrix")
plt.ylabel("True Label")
plt.xlabel("Predicted Label")

# Display the plot
plt.show()
# ==============================================================================

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
