# routines for spherical geometry

from numpy import *


# returns distance in radians
def dist_between(loc1,loc2):

    # everything is radians
    f1 = loc1[0]
    f2 = loc2[0]
    l12 = loc2[1] - loc1[1]
    
    return arccos(sin(f1) * sin(f2) + cos(f1) * cos(f2) * cos(l12))

def loc_at_dist(loc1,loc2,ds):

    # ds is great-circle distance in radians
    l12 = loc2[1] - loc1[1]
    l1 = loc1[1]
    f1 = loc1[0]
    f2 = loc2[0]

    a1 = arctan2(sin(l12), (cos(f1) * tan(f2) - sin(f1) * cos(l12)))

    a0 = arcsin(sin(a1) * cos(f1))
    
    # calculationg l0
    s1 = arctan2(tan(f1), cos(a1))
    l01 = arctan2(sin(a0) * sin(s1), cos(s1))
    l0 = l1 - l01


    # coordinates of a point on the line segment at a distance s from P0
    f = arcsin(cos(a0) * sin(s1 + ds))
    l = l0 + arctan2(sin(a0) * sin(s1 + ds) , cos(s1 + ds))
    
    return f,l,a0,a1
