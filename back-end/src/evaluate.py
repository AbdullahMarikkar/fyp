# src/evaluate.py

import numpy as np
from sklearn.metrics import classification_report
from tensorflow.keras.models import load_model
from preprocess import load_labels, preprocess_image, enhance_image
from train import label_map

# Load model and labels
model = load_model('model.h5')
labels = load_labels('data/labels.csv')
images = list(labels.keys())

# Prepare data for evaluation
X_test, y_test_thermal, y_test_natural = get_data(images, labels, label_map)

# Predict and evaluate
predictions = model.predict(X_test)
y_pred_thermal = np.argmax(predictions[0], axis=1)
y_pred_natural = np.argmax(predictions[1], axis=1)

print("Thermal State Classification Report:")
print(classification_report(np.argmax(y_test_thermal, axis=1), y_pred_thermal, target_names=['heated', 'unheated']))

print("\nNatural State Classification Report:")
print(classification_report(np.argmax(y_test_natural, axis=1), y_pred_natural, target_names=['natural', 'synthetic']))
