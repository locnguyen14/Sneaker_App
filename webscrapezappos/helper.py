import numpy as np
import os
import cv2
import matplotlib.pyplot as plt


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_image_data():
    '''
    A function to load the image from the folder
    Input: none
    Output: 2 numpy array, one for images and one for label of images
    '''

    labels = os.listdir('images/')

    # Empty numpy array with no_column = (width * height) of image
    dataset_features = np.empty((0, 510*250))
    dataset_labels = np.empty((0,1))

    # Read in the image, resize, and finally flatten it
    for label in labels:
        files = os.listdir(f'images/{label}/')
        img_list = []
        for file in files:
            img = cv2.imread(f'images/{label}/{file}', 0) # Read image
            img_list.append(img)
        dim = [(510,250)]*len(img_list)
        interpolation = [cv2.INTER_AREA]*len(img_list)
        img_list_resize = list(map(cv2.resize, img_list, dim, interpolation)) # Resize
        img_list_resize_flatten = list(map(lambda x: x.flatten(), img_list_resize)) # Flatten

        # Some preprocess steps before returning the numpy array
        dataset_features = np.vstack((dataset_features, tuple(img_list_resize_flatten)))
        label_arr = np.array([label]*len(img_list), dtype=object).reshape((len(img_list),1))
        dataset_labels = np.vstack((dataset_labels, tuple(label_arr)))
        
    return dataset_features, dataset_labels



def scree_plot_pca(pca):
    '''
    A function to plot the explain variance ratio of all principals components
    Input: a PCA object 
    Output: None
    '''

    num_components = len(pca.explained_variance_ratio_)
    indx = np.arange(num_components) + 1 # start with 1
    variance_ratio = pca.explained_variance_ratio_

    plt.figure(figsize=(16, 8))

    cumulative_variance_ratio = np.cumsum(variance_ratio)

    plt.bar(indx, variance_ratio)
    plt.ylabel("Variance Explained (%)")
    plt.xlabel("Principal Component")
    plt.grid(False)
    plt.twinx()

    plt.plot(indx, cumulative_variance_ratio)
    plt.ylabel("Cumulative Variance Explained (%)")
    plt.title('Explained Variance Per Principal Component')
    plt.grid(False)

    plt.show()


def image_augment(image): 
        '''
        Create the new image with imge augmentation
        :param path: the path to store the new image
        ''' 
        img = image.copy()
        # Flip Image
        img_flip = cv2.flip(img, flipCode=0)
        
        # Rotate image
        w = img.shape[1]
        h = img.shape[0]
        M = cv2.getRotationMatrix2D((w/2,h/2), angle=90, scale=1.0)
        img_rotate = cv2.warpAffine(img,M,(w,h))
        
        return img_flip, img_rotate