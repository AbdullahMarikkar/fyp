import os
import torch
from model import SingleHeadModel
from preprocess import preprocess_image, enhance_image

def classify_image(image_path):
    img = preprocess_image(image_path)
    img = enhance_image(img)
    img = img.unsqueeze(0)  # Add batch dimension

    model = SingleHeadModel()
    model.load_state_dict(torch.load('model.pth'))
    model.eval()

    with torch.no_grad():
        output = model(img)
        _, pred = torch.max(output, 1)

    label_map = {0: 'heated', 1: 'natural', 2: 'synthetic'}
    state_label = label_map[pred.item()]
    print(f"State: {state_label}")

# Example usage
classify_image('data/test/test1.jpg')
