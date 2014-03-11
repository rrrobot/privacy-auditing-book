import numpy as np
import pylab as pl
import matplotlib.font_manager
from scipy import stats

from sklearn import svm
from sklearn.covariance import EllipticEnvelope

import sys,os
sys.path.append("mpldatacursor")
sys.path.append("mpldatacursor/mpldatacursor")
from mpldatacursor import datacursor

# Example settings
n_samples = 200
outliers_fraction = 0.25

if __name__=="__main__":

    # Compare given classifiers under given settings
    xx, yy = np.meshgrid(np.linspace(-7, 7, 500), np.linspace(-7, 7, 500))
    n_inliers = int((1. - outliers_fraction) * n_samples)
    n_outliers = int(outliers_fraction * n_samples)
    ground_truth = np.ones(n_samples, dtype=int)
    ground_truth[-n_outliers:] = 0

    # Fit the problem with varying cluster separation
    np.random.seed(42)

    # Data generation
    X1 = 0.3 * np.random.randn(0.5 * n_inliers, 2) 
    X2 = 0.3 * np.random.randn(0.5 * n_inliers, 2) 
    X = np.r_[X1, X2]
    # Add outliers
    X = np.r_[X, np.random.uniform(low=-6, high=6, size=(n_outliers, 2))]

    # Fit the model with the One-Class SVM
    pl.figure(figsize=(10, 5))
    clf = svm.OneClassSVM(nu=0.95 * outliers_fraction + 0.05, kernel="rbf", gamma=0.1)

    # fit the data and tag outliers
    clf.fit(X)
    y_pred = clf.decision_function(X).ravel()
    threshold = stats.scoreatpercentile(y_pred, 100 * outliers_fraction)
    y_pred = y_pred > threshold
    n_errors = (y_pred != ground_truth).sum()

    # plot the levels lines and the points
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    pl.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7), cmap=pl.cm.Blues_r)
    a = pl.contour(xx, yy, Z, levels=[threshold], linewidths=2, colors='red')
    pl.contourf(xx, yy, Z, levels=[threshold, Z.max()], colors='orange')
    b = pl.scatter(X[:-n_outliers, 0], X[:-n_outliers, 1], c='white')
    c = pl.scatter(X[-n_outliers:, 0], X[-n_outliers:, 1], c='black')
    pl.legend(
        [a.collections[0], b, c],
        ['learned decision function', 'true inliers', 'true outliers'],
        prop=matplotlib.font_manager.FontProperties(size=11))
    datacursor()
    pl.show()
