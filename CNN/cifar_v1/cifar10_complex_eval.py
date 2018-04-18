# Evaluation program for CIFAR-10
#
# NN-Team-2

import numpy as np

from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

from matplotlib import pyplot
from scipy.misc import toimage

import os.path as path

K.set_image_dim_ordering('th')

# fix random seed for reproducibility
seed = 52
np.random.seed(seed)

# load data
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# normalize inputs from 0-255 to 0.0-1.0
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

# Create the model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(3, 32, 32), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))
# Compile model
epochs = 25
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())

if path.exists('out/cifar10_complex_cnn.h5'):
    model.load_weights('out/cifar10_complex_cnn.h5')

    scores = model.evaluate(X_train, y_train, verbose=0)
    print("Accuracy train: %.2f%%" % (scores[1] * 100))

    scores = model.evaluate(X_test, y_test, verbose=0)
    print("Accuracy test: %.2f%%" % (scores[1] * 100))

    # declare categories:
    categories = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    # pull first 9 images out:
    images = X_train[:9]

    # make prediction
    prediction = model.predict(images)

    # create a grid of 3x3 images
    fig = pyplot.figure()
    for i in range(0, 9):
        ax = pyplot.subplot(330 + 1 + i)
        ax.title.set_text(categories[np.argmax(prediction[i])])
        pyplot.imshow(toimage(images[i]))

    # show the plot
    pyplot.show()
else:
    print('no weights found...')