import cv2
import os
import numpy as np
import pandas as pd

def load_labels(csv_path):
    """Load labels from CSV."""
    df = pd.read_csv(csv_path)
    return {row['image']: (row['thermal_state'], row['natural_state']) for _, row in df.iterrows()}

def preprocess_image(image_path):
    """Load, resize, and normalize the image."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))        # Resize to 224x224
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to RGB
    img = img / 255.0                         # Normalize to [0,1]
    return img

def enhance_image(img):
    """Apply histogram equalization to enhance the image."""
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return img