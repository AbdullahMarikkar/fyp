import cv2
import os
import pandas as pd
import torch
from torchvision import transforms

def load_labels(csv_path):
    """Load labels from CSV with only the filename as the key."""
    df = pd.read_csv(csv_path)
    return {row['image']: row['state'] for _, row in df.iterrows()}

def preprocess_image(image_path):
    """Load and preprocess the image."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Apply transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = transform(img)
    return img

def enhance_image(img):
    """Enhance image using histogram equalization."""
    img_np = img.permute(1, 2, 0).numpy() * 255.0
    img_np = img_np.astype('uint8')

    img_yuv = cv2.cvtColor(img_np, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)

    transform = transforms.ToTensor()
    return transform(img)
