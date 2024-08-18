import math

def calculate_area(dmin, dmax):
    """Calculate the area of a bounding box defined by dmin and dmax."""
    area = 0.0
    for i in range(len(dmin)):
        if dmax[i] != dmin[i]:
            area += math.log(dmax[i] - dmin[i])
    return area