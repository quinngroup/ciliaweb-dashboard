import argparse
import json
import os.path

import matplotlib.pyplot as plt
import numpy
import sklearn.datasets as skds
from sklearn.decomposition import PCA as sk_pca

from sklearn.manifold import TSNE as sk_tsne

from umap import UMAP as sk_umap

import json

#
# This is a simple dummy script which loads the MNIST digits data
# and projects them into 2 or 3 dimensional space using a variety
# of dimensionality reduction techniques.

# It also packages the projected data in a way that is useful to
# interactive visualization.
#

#
# Only dump the projection
#
def dumpProjectedJSON(X_proj, outfile, y = None, idx = False):
        out = []
        for index, x_proj in enumerate(X_proj):
                d = {"x": x_proj, "y": None}
                if y is not None:
                        d["y"] = y[index]
                if idx:
                        d["idx"] = index
                out.append(d)

        json.dump(out, open(outfile, "w"))

#
# Dump projection and original data that led to projection
#
def dumpJFullSON(X_proj, X_orig, outfile, y = None):
        out = []
        for index, (x_proj, x_orig) in enumerate(zip(X_proj.tolist(), X_orig)):
                d = {"x": x_proj, "y": None, "data": x_orig}
                if y is not None:
                        d["y"] = y[index]
                out.append(d)

        json.dump(out, open(outfile, "w"))

#
# Calculate PCA projection
#
def pca(X, dims):
        pca = sk_pca(n_components = dims, whiten = True)
        X_new = pca.fit_transform(X)
        return X_new

#
# Calculate TNSE projection
#
def tsne(X, dims):
        tsne = sk_tsne(n_components = dims)
        X_new = tsne.fit_transform(X)
        return X_new

#
# Calculate UMAP projection
#
def umap(X, dims):
        umap = sk_umap(n_components = dims)
        X_new = umap.fit_transform(X)
        return X_new

#
# MAIN Function
#
def main(args):

        # Load the data.
        data_dict = skds.load_digits()

        # Pull out the images and the labels.
        X, y = data_dict['data'], data_dict['target']
        dims = args['dims']
        outfile = args['output']
        images = data_dict['images']
        X_new = []

        if args['type'] == 'pca':
                X_new = pca(X, dims)
        elif args['type'] == 'tsne':
                X_new = tsne(X, dims)
        elif args['type'] == 'umap':
                X_new = umap(X, dims)

        if X_new.any():
                dumpProjectedJSON(X_new.tolist(), outfile, y.tolist())

if __name__ == "__main__":
        #
        # This section is responsible for reading and evaluating
        # all parameters passed using parser
        #

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

        main(args)

        
