import argparse
import json
import os.path

import matplotlib.pyplot as plt
import numpy
import sklearn.datasets as skds
from sklearn.decomposition import PCA as sk_pca

#import umap

# This is a simple dummy script which loads the MNIST digits data
# and projects them into 2 or 3 dimensional space using a variety
# of dimensionality reduction techniques.

# It also packages the projected data in a way that is useful to 
# interactive visualization.

def pca():
    pca = sk_pca(n_components = args['dims'], whiten = True)
    X_new = pca.fit_transform(X)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Dummy Data',
    epilog = 'lol d1m r3d', add_help = 'How to use',
    prog = 'python dummy_mnist.py <options>')

    # Optional arguments.
    parser.add_argument("--type", choices = ["pca", "tsne", "umap"], default = "pca",
        help = "Dimensionality reduction strategy. [DEFAULT: pca]")
    parser.add_argument("--dims", choices = [2, 3], default = 2, type = int,
        help = "Number of projected dimensions. [DEFAULT: 2]")
    parser.add_argument("--seed", type = int, default = 42,
        help = "Random seed used for reproducibility. [DEFAULT: 42]")

    parser.add_argument("-o", "--output", default = "output.json",
        help = "Output file containing the embeddings and data. [DEFAULT: output.txt]")

    # Parse out the arguments.
    args = vars(parser.parse_args())
    if not os.path.isdir(args['output']):
        os.mkdir(args['output'])

    # Load the data.
    data_dict = skds.load_digits()

    # Pull out the images and the labels.
    X, y = data_dict['data'], data_dict['target']
    images = data_dict['images']

    if args['type'] == 'pca':
        pass
    elif args['type'] == 'tsne':
        pass
    elif args['type'] == 'umap':
        pass
    else:
        print(f"Undefined dimensionality reduction method '{args['type']}' specified!")
        quit()
