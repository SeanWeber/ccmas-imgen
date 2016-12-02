import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def create_model(file_name):
    '''
    :param str file_name: Name of the image file
    :returns:
     Dictionary, where keys are RGB-values and items their probabilities
    '''

    img = mpimg.imread(file_name)

    # Normalization of data to decimal (0.0 - 1.0) representation
    img=img.astype('float16')
    print(img)
    if img.max() > 1.0:
        img /= 255.0

    rgbs = {}
    for i in img:
        for j in i:
            rgb = tuple(j)
            if rgb not in rgbs:
                rgbs[rgb] = 1.0
            else:
                rgbs[rgb] += 1.0
    total = np.sum(list(rgbs.values()))
    distribution = {}
    for rgb, freq in rgbs.items():
        distribution[rgb] = freq / total
    return distribution

if __name__ == "__main__":
    distribution = create_model("../media/starring-night.jpg")
    print(distribution)