# src/train.py

import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from preprocess import load_labels, preprocess_image, enhance_image
from model import create_model

# Load labels and split dataset
labels = load_labels('data/labels.csv')
images = list(labels.keys())
train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)

def get_data(images, labels, label_map):
    X, y_thermal, y_natural = [], [], []
    for img_name in images:
        img = preprocess_image(os.path.join('data/images', img_name))
        img = enhance_image(img)
        X.append(img)
        y_thermal.append(label_map['thermal'][labels[img_name][0]])
        y_natural.append(label_map['natural'][labels[img_name][1]])
    return np.array(X), to_categorical(y_thermal), to_categorical(y_natural)

# Define label mappings
label_map = {'thermal': {'heated': 0, 'unheated': 1}, 'natural': {'natural': 0, 'synthetic': 1}}

# Prepare data
X_train, y_train_thermal, y_train_natural = get_data(train_images, labels, label_map)
X_val, y_val_thermal, y_val_natural = get_data(val_images, labels, label_map)

# Create and train the model
model = create_model()
history = model.fit(X_train, {'thermal_output': y_train_thermal, 'natural_output': y_train_natural},
                    validation_data=(X_val, {'thermal_output': y_val_thermal, 'natural_output': y_val_natural}),
                    epochs=10, batch_size=32)
model.save('model.h5')
