import os
import cv2
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


def visualize_feature_maps(model, image_path, true_label):
    """
    Generates and displays a heatmap of the model's feature activation
    using a forward hook, without modifying the model's code.
    """
    # Ensure the model is in evaluation mode
    model.eval()

    # 1. Load and preprocess the image
    original_img = cv2.imread(image_path)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    processed_img = preprocess_image(image_path)
    processed_img = processed_img.unsqueeze(0)  # Add batch dimension

    # --- New Hook-Based Logic ---

    # A. Create a placeholder to store the feature maps
    feature_maps = []

    # B. Define the hook function that will capture the output of the target layer
    def hook_function(module, input, output):
        feature_maps.append(output)

    # C. Register the hook on the desired layer
    # For ShuffleNetV2, 'conv5' is the last convolutional block before the final classifier.
    # This gives us the richest feature representation.
    target_layer = model.base_model.conv5
    hook = target_layer.register_forward_hook(hook_function)

    # 2. Get the model's final output (the hook will automatically capture the features)
    with torch.no_grad():
        output = model(processed_img)

    # D. Remove the hook immediately after use to keep the model clean
    hook.remove()

    # 3. Get the prediction
    _, pred_idx = torch.max(output, 1)
    label_map = {0: "heated", 1: "natural", 2: "synthetic"}
    predicted_label = label_map[pred_idx.item()]

    # 4. Process the captured feature maps to create a heatmap
    # We take the first item since we only processed one image
    captured_features = feature_maps[0]
    heatmap = torch.mean(captured_features[0], dim=0).cpu().numpy()

    # Normalize the heatmap
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)

    # Resize the heatmap and apply a colormap
    heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # 5. Overlay the heatmap on the original image
    superimposed_img = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)

    # 6. Plot the results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle(f"True: {true_label} | Predicted: {predicted_label}", fontsize=16)

    ax1.imshow(original_img)
    ax1.set_title("Original Image")
    ax1.axis("off")

    ax2.imshow(superimposed_img)
    ax2.set_title("Feature Map Heatmap")
    ax2.axis("off")

    plt.show()


# --- HOW TO USE THE FUNCTION (This part remains the same) ---

if __name__ == "__main__":
    # Load your trained model
    model = SingleHeadModel()
    model.load_state_dict(torch.load("model.pth"))  # Make sure the path is correct

    # Create visualizations for a few sample images
    # Replace these with actual paths to your test images
    sample_images = {
        "data/images/img1.jpg": "natural",
        "data/images/img5.jpg": "heated",
        "data/images/img7.jpg": "natural",
        "data/images/img8.jpg": "natural",
        "data/images/S(H)115.jpg": "heated",
        "data/images/S(N)144.jpg": "natural",
        "data/images/S(N)146.jpg": "natural",
        "data/images/S(S)29.jpg": "synthetic",
        "data/images/S(S)31.jpg": "synthetic",
    }

    for img_path, true_label in sample_images.items():
        visualize_feature_maps(model, img_path, true_label)
