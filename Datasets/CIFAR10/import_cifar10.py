import numpy as np

import matplotlib.pyplot as plt
from scipy.misc import toimage
from scipy.misc import imsave

def import_cifar10(category=0, plot=False, save=False):
    categories = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    filter_train = np.load('dataset/x_train_color_{}.npy'.format(categories[category]))

    images = filter_train[:16]
    print(images[0].shape)
    print(images[0])

    # create a single image
    if(save):
        print('saving {}.png'.format(categories[category]))
        imsave('{}.png'.format(categories[category]), images[0])

    if(plot):
        # create a grid of 3x3 images
        plt.figure(figsize=(10, 10))
        for i in range(images.shape[0]):
            plt.subplot(4, 4, i + 1)
            plt.imshow(toimage(images[i]))
            plt.axis('off')
        plt.tight_layout()
        plt.show()

    return filter_train

for i in range(1):
    import_cifar10(category=i, plot=True, save=False)