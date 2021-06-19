import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
try:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print('initialized')
except:
    print("Pass")
    # Invalid device or cannot modify virtual devices once initialized.
    pass
from tensorflow import keras
import numpy as np 
import cv2
import os 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import model_from_json
from tensorflow.keras.applications.vgg16 import VGG16



IMG_SAVE_PATH = 'image_data'
train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

CLASS_MAP = {
    "rock": 0,
    "paper": 1,
    "scissors": 2,
    "none": 3
}
NUM_CLASSES = len(CLASS_MAP)


train_generator = train_datagen.flow_from_directory(
        "./dataset/train",
        target_size=(227,227),
        batch_size=20,
        class_mode="categorical")

validation_generator = validation_datagen.flow_from_directory(
        "./dataset/test",  
        target_size=(227,227),  
        batch_size=10,
        class_mode='categorical')

model = keras.models.Sequential()
model.add(VGG16(include_top=False,input_shape=(227,227,3)))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Convolution2D(NUM_CLASSES, (1, 1), padding='valid'))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.GlobalAveragePooling2D())
model.add(keras.layers.Activation('softmax'))

from tensorflow.keras.optimizers import Adam
model.compile(
    optimizer=Adam(lr==0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)              

history = model.fit(
      train_generator,
      steps_per_epoch=8,  
      epochs=40,
      verbose=2,
      validation_data = validation_generator,
      validation_steps=8)


import matplotlib.pyplot as plt

#-----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
#-----------------------------------------------------------
acc      = history.history[     'accuracy' ]
val_acc  = history.history[ 'val_accuracy' ]
loss     = history.history[    'loss' ]
val_loss = history.history['val_loss' ]

epochs   = range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
plt.plot  ( epochs,     acc )
plt.plot  ( epochs, val_acc )
plt.title ('Training and validation accuracy')
plt.figure()

#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
plt.plot  ( epochs,     loss )
plt.plot  ( epochs, val_loss )
plt.title ('Training and validation loss'   )

model.save("rock-paper-scissors-model.h5")

from numba import cuda 
device = cuda.get_current_device()
device.reset()