from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
import os
from scipy.misc import imread, imresize
import numpy as np

def get_encoder(input_img, image_data, data_dir):

    x = Convolution2D(32, 5, 5, activation='relu', border_mode='same')(input_img)
    x = MaxPooling2D((2, 2), border_mode='same')(x)
    x = Convolution2D(16, 5, 5, activation='relu', border_mode='same')(x)
    x = MaxPooling2D((2, 2), border_mode='same')(x)
    x = Convolution2D(8, 5, 5, activation='relu', border_mode='same')(x)
    x = MaxPooling2D((2, 2), border_mode='same')(x)
    x = Convolution2D(4, 5, 5, activation='relu', border_mode='same')(x)
    encoded = MaxPooling2D((2, 2), border_mode='same')(x)

    # at this point the representation is (8, 4, 4) i.e. 128-dimensional

    x = Convolution2D(4, 5, 5, activation='relu', border_mode='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Convolution2D(8, 5, 5, activation='relu', border_mode='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Convolution2D(16, 5, 5, activation='relu', border_mode='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Convolution2D(32, 5, 5, activation='relu', border_mode='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Convolution2D(1, 5, 5, activation='sigmoid', border_mode='same')(x)

    autoencoder = Model(input_img, decoded)
    if os.path.exists(os.path.join(data_dir,"ae_weights.h5")):
        autoencoder.load_weights(os.path.join(data_dir,"ae_weights.h5"))
        return Model(input_img, encoded)

    autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

    # image_data = [] 
    # for image_file in os.listdir(os.path.join(data_dir, 'images')):
    #     image_data.append(imresize(imread(os.path.join(data_dir, 'images', image_file)),(img_height,img_width))
    #     .reshape((img_height, img_width,1)).astype(np.float32))
    # image_data = np.array(image_data)
    # image_data = (np.random.random(image_data.shape) < image_data).astype(np.float32)
    autoencoder.fit(image_data, image_data, epochs=500, batch_size=256, shuffle=True, callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])

    autoencoder.save_weights(os.path.join(data_dir,"ae_weights.h5"))

    return Model(input_img, encoded)