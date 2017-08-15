import coremltools
from numpy.random import random, permutation
from scipy import misc, ndimage
from scipy.ndimage.interpolation import zoom

import keras
from keras import backend as K
from keras.utils.data_utils import get_file
from keras.models import Sequential, Model
from keras.layers.core import Flatten, Dense, Dropout, Lambda
from keras.layers import Input
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD, RMSprop
from keras.preprocessing import image

def ConvBlock(layers, model, filters, first_layer=False):
    for i in range(layers):
        if first_layer and i == 0:
            model.add(ZeroPadding2D((1,1),input_shape=(3,224,224)))
            print "adding input shape"
        else:
            model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(filters, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

def FCBlock(model):
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))

def VGG_16():
    model = Sequential()
    #model.add(Lambda(vgg_preprocess, input_shape=(3,224,224)))

    ConvBlock(2, model, 64, True)
    ConvBlock(2, model, 128)
    ConvBlock(3, model, 256)
    ConvBlock(3, model, 512)
    ConvBlock(3, model, 512)

    model.add(Flatten())
    FCBlock(model)
    FCBlock(model)
    model.add(Dense(1000, activation='softmax'))
    return model

model = VGG_16()
fpath = get_file('vgg16.h5', 'http://files.fast.ai/models/vgg16.h5', cache_subdir='models')
model.load_weights(fpath)

coreml_model = coremltools.converters.keras.convert(model, input_names = 'image', class_labels = ['one','ten'], is_bgr=True)
