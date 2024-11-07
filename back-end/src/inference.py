# src/inference.py

import numpy as np
from tensorflow.keras.models import load_model
from preprocess import preprocess_image, enhance_image

model = load_model('model.h5')

def classify_image(image_path):
    img = preprocess_image(image_path)
    img = enhance_image(img)
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    thermal_state = np.argmax(prediction[0], axis=1)[0]
    natural_state = np.argmax(prediction[1], axis=1)[0]

    thermal_label = 'heated' if thermal_state == 0 else 'unheated'
    natural_label = 'natural' if natural_state == 0 else 'synthetic'

    print(f"Thermal State: {thermal_label}")
    print(f"Natural State: {natural_label}")

# Example usage
classify_image('path/to/new/image.jpg')
