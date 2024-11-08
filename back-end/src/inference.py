# src/inference.py

import torch
from preprocess import preprocess_image, enhance_image
from model import create_model

# Load model
model = create_model()
model.load_state_dict(torch.load('model.pth'))
model.eval()

def classify_image(image_path):
    img = preprocess_image(image_path)
    img = enhance_image(img)
    img = img.unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        thermal_pred, natural_pred = model(img)
        thermal_state = torch.argmax(thermal_pred, dim=1).item()
        natural_state = torch.argmax(natural_pred, dim=1).item()

    thermal_label = 'heated' if thermal_state == 0 else 'unheated'
    natural_label = 'natural' if natural_state == 0 else 'synthetic'

    print(f"Thermal State: {thermal_label}")
    print(f"Natural State: {natural_label}")

# Example usage
classify_image('data/test/test1.jpg')
