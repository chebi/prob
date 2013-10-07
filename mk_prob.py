# produces the probability distribution as a sum of three independent
# pdfs

from shapely.geometry import MultiLineString
from shapely.geometry import Point
from shapely.geometry import LineString
import scipy.special as sp
import scipy.stats as st
import numpy as np
from math import *

import sphere as sph


def rd(x):
    return pi * x / 180


def gr(x):
    return x * 180 / pi

# file with coordinates of the river Spree
s = 'spree.txt'
a = rd(np.genfromtxt(s, delimiter=","))

# coordinates of the Brandenburger Gate
loc_bt = [rd(52.516288), rd(13.377689)]

# Earth radius
r = 6371

# producing set of points for the Spree
prev = a[0]
spree = []
for j in range(1, len(a)):
    loc1 = [prev[0], prev[1]]
    loc2 = [a[j][0], a[j][1]]
    dist = sph.dist_between(loc1, loc2)
    prev = a[j]
    i = 1
    while 0.1 / r * i < dist:
        f, l, a0, a1 = sph.loc_at_dist(loc1, loc2, 0.1 / r * i)
        spree.append([f, l])
        i = i + 1

# producing set of points for the sattelite
satt = []
loc1 = [rd(52.590117), rd(13.39915)]
loc2 = [rd(52.437385), rd(13.553989)]
dist = sph.dist_between(loc1, loc2)
i = 1
while 0.1 / r * i < dist:
    f, l, a0, a1 = sph.loc_at_dist(loc1, loc2, 0.1 / r * i)
    satt.append([f, l])
    i = i + 1


# determining the bounding box
x1 = max(max(a[:, 0]), loc1[0], loc2[0])
y1 = max(max(a[:, 1]), loc1[1], loc2[1])
x0 = min(min(a[:, 0]), loc1[0], loc2[0])
y0 = min(min(a[:, 1]), loc1[1], loc2[1])

# resolution of the grid for calculation of the probability
x_step = (x1 - x0) / 100.0
y_step = (y1 - y0) / 100.0

# grid points
zz = np.zeros((100, 100), float)
f1 = open('4gnuplot.txt', 'w')

# variance of the Gaussian around Spree
sigma = 2.730 / sqrt(2) / sp.erfinv(0.9)

# variance of the Gaussian around the sattelite path
sigma1 = 2.400 / sqrt(2) / sp.erfinv(0.9)

sigma2 = sqrt(4.7 - log(3.877))
mu = 4.7  # mean of the log-normal distribution around Brandenburger Gate

NOP = 100 # number pf points

for i in range(NOP):
    for j in range(NOP):

        loc = [x0 + x_step * i, y0 + y_step * j]

        # calculate distances
        ds = []
        for el in spree:
            ds.append(sph.dist_between(loc, el))
        # find minimum
        d = min(ds) * r

        ds = []
        for el in satt:
            ds.append(sph.dist_between(loc, el))
        # find minimum
        d1 = min(ds) * r

        d2 = sph.dist_between(loc, loc_bt) * r

        # normal distribution near Spree
        p = st.norm.pdf(d, loc=0, scale=sigma)
        #or
        # p = 1.0 / (sqrt(2.0 * pi) * sigma) * \
        #    exp(-d * d / (2.0 * sigma * sigma))

        # normal distribution near sattelite
        p1 = st.norm.pdf(d1, loc=0, scale=sigma1)
        # or
        # p1 = 1.0 / (sqrt(2.0 * pi) * sigma1) * \
        #   exp(-d1 * d1 / (2.0 * sigma1 * sigma1))

        # log-normal distribution around Brandenburger Gate
        p2 = 1.0 / (d2 * sqrt(2.0 * pi) * sigma2) * exp(
            -(log(d2) - mu) * (log(d2) - mu) / (2.0 * sigma2 * sigma2))

        zz[i, j] = p1 + p + p2
        s = str(p1 + p + p2) + " "
        f1.write(s)
    f1.write("\n")
f1.close()

i, j = np.where(zz[:, :] == np.amax(zz))
print x0 + x_step * i, y0 + y_step * j
