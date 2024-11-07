# src/model.py

import tensorflow as tf
from tensorflow.keras import layers, models

def create_model():
    """Define a CNN model with two output heads for dual classification."""
    base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3),
                                                   include_top=False,
                                                   weights='imagenet')
    base_model.trainable = False

    inputs = layers.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)

    # Thermal state classification head
    thermal_output = layers.Dense(2, activation='softmax', name='thermal_output')(x)

    # Natural state classification head
    natural_output = layers.Dense(2, activation='softmax', name='natural_output')(x)

    model = models.Model(inputs=inputs, outputs=[thermal_output, natural_output])

    # Compile model with categorical crossentropy for both outputs
    model.compile(optimizer='adam',
                  loss={'thermal_output': 'categorical_crossentropy', 'natural_output': 'categorical_crossentropy'},
                  metrics=['accuracy'])
    return model
