from glob import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input

def create_model(input_shape=(224, 224, 3)):
    inputs = tf.keras.layers.Input(input_shape)
    base_model = MobileNetV2(include_top=False, weights='imagenet', input_shape=input_shape)
    x = base_model(inputs)
    outputs = tf.keras.layers.GlobalAveragePooling2D()(x)
    
    print("Creating model complete")
    return tf.keras.Model(inputs, outputs)

def load_image(path):
    img = tf.keras.preprocessing.image.load_img(path, target_size=(224, 224))
    img = preprocess_input(np.array(img))
    return img

class Dataloader(tf.keras.utils.Sequence):
    def __init__(self, image_dir, batch_size):
        self.images = np.array(glob(image_dir + '/*.[jpg][png]*'))
        self.batch_size = batch_size
        print("Creating dataloader complete")
    
    def __len__(self):
        return np.ceil(len(self.images) / self.batch_size).astype(np.int32)
    
    def on_epoch_end(self):
        return np.arange(len(self.images))
    
    def __getitem__(self, idx):
        path = self.images[self.batch_size*idx : self.batch_size*(idx+1)]
        image = [load_image(i) for i in path]
        image = np.stack(image)
        return path, image