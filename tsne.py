## importing the required packages
import numpy as np
import pandas as pd
from time import time
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
             discriminant_analysis, random_projection)
## Loading and curating the data
def read1file(classes):
    df = pd.read_csv('data/ITP-NRL.csv', index_col='name').fillna(0)
    cols = df.columns.to_list()
    col_list = []
    for i in range(len(classes)):
        col_list.extend([i for _ in range(classes[i])])
    df.columns = col_list
    return df, cols

def readMultiFiles():
    data_path = 'data/tsne/'
    files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    dfs = []
    cols = []
    for f in files:
        df = pd.read_csv(data_path+f, index_col='AccID').fillna(0)
        cols.extend(df.columns.to_list())
        df.columns = [files.index(f) for _ in range(len(df.columns))]
        dfs.append(df)
    df = pd.concat(dfs, axis=1)
    return df, cols

## Function to Scale and visualize the embedding vectors
def plot_embedding(X, cols, y):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)
    plt.figure()
    ax = plt.subplot(111)
    dots = [0 for _ in range(X.shape[0])]
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(cols[i]), color=plt.cm.Set1(y[i]), fontdict={'size': 10})
        #dots[i], = plt.plot(X[i, 0], X[i, 1], '.', color=plt.cm.Set1(y[i]))
    #plt.legend([dots[0], dots[-1]], ['ITP', 'healthy'])
    plt.xticks([]), plt.yticks([])

def plot_3d(X, classes):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    sp, ep = 0, 0#18 + 75, 18 + 75
    colors = ['r', 'b', 'r', 'b']
    markers = ['^', '.', '^', '.']
    for i in range(0, len(classes)):
        ep += classes[i]
        ax.scatter(X[:, 0][sp:ep], X[:, 1][sp:ep], X[:, 2][sp:ep], c=colors[i], marker=markers[i])
        sp = ep

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title('t-SNE')
    plt.axis('tight')

def plot_3d_text(X, cols, classes):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    xs = X[:, 0]
    ys = X[:, 1]
    zs = X[:, 2]

    sp, ep = 0, -1
    colors = ['r', 'b', 'r', 'b']

    i, ii = 1, 0
    sum = classes[ii]
    for col, x, y, z in zip(cols, xs, ys, zs):
        if i > sum:
            ii += 1
            sum += classes[ii]
        #if 18 + 75 < i < 18 + 75 + 64 + 63:
        label = str(col)
        ax.text(x, y, z, label, fontsize=6, color=colors[ii])
        i += 1

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title('t-SNE')
    plt.axis('tight')

def main():
    healthy, JZX = 106, 111
    NCZ, th, ITP, hea = 18, 75, 64, 63
    classes = [ITP, hea]

    df, cols = read1file(classes)

    X = df.iloc[:, :].to_numpy().T
    y = df.columns[:].to_numpy().T

    n_samples, n_features = X.shape

    #----------------------------------------------------------------------
    ## Computing PCA
    '''print("Computing PCA projection")
    t0 = time()
    #X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X)
    X_pca = decomposition.PCA().fit_transform(X)
    plot_embedding(X_pca,
                "Principal Components projection of the digits (time %.2fs)" %
                (time() - t0))'''
    ## Computing t-SNE
    print("Computing t-SNE embedding")
    #tsne = manifold.TSNE(n_components=2)
    tsne = manifold.TSNE(n_components=2, init='pca', perplexity=30, n_iter=1500)
    X_tsne = tsne.fit_transform(X)
    plot_embedding(X_tsne, cols, y)
    #tsne = manifold.TSNE(n_components=3, init='pca', perplexity=30, n_iter=1500)
    #X_tsne = tsne.fit_transform(X)
    #plot_3d(X_tsne, classes)
    #plot_3d_text(X_tsne, cols, classes)
    plt.show()

if __name__ == "__main__":
    main()
