from itertools import product

import numpy as np
from scipy import stats
from scipy import integrate

def compute_mutual_information(data1, data2, grid1=None, grid2=None, step=100):
    kde = stats.gaussian_kde(np.asarray([data1, data2], dtype=np.float))
    kde1 = stats.gaussian_kde(np.asarray(data1, dtype=np.float))
    kde2 = stats.gaussian_kde(np.asarray(data2, dtype=np.float))
    if grid1 is None:
        grid1 = np.linspace(np.min(data1), np.max(data1), step)
    if grid2 is None:
        grid2 = np.linspace(np.min(data2), np.max(data2), step)
    def integrand(d1, d2):
        p12 = kde([d1, d2])
        p1 = kde1(d1)
        p2 = kde2(d2)
        return p12 * (np.log2(p12) - np.log2(p1) - np.log2(p2)) if p12 * p1 * p2 > 0 else 0.0
    quad1 = lambda d2: integrate.quad(lambda d1: integrand(d1, d2), np.min(grid1), np.max(grid1))[0]
    return integrate.quad(quad1, np.min(grid2), np.max(grid2))[0]

