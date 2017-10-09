###### TALK TO BRANDON ######
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image


import sys

def load_annotation(filename):
    annotations = mpimg.imread(filename)
    slice_info = get_slice_info(filename)
    return annotations, slice_info

def get_slice_info(filename):
    z_slice = int(filename[0:1])
    cube_id = filename[2:10] #string, TODO: make class
    return [z_slice, cube_id]

def get_slice(slice_info):
    f = open(slice_info[1] + ".pickle", "rb")
    metacube = pickle.load(f)
    return metacube["data"][slice_info[0]]

def get_annotation(annotation_image, slice_info):
    cube_slice = get_slice(slice_info)
    annotations = annotation_image - cube_slice
    return annotations

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        annotation = get_annotation(*load_annotation(filename))
        im = Image.fromarray(annotation)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im.save("proof_annotation.png", "PNG")

    except:
        raise
