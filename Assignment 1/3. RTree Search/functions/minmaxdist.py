def minmaxdist(point, R):
    minmax_dist = float('inf')

    S = 0
    for i in range(len(point)):
        if point[i] >= (R.dmin[i] + R.dmax[i]) / 2:
            S += (point[i] - R.dmin[i]) ** 2
        else:
            S += (point[i] - R.dmax[i]) ** 2

    for i in range(len(point)):
        if point[i] >= (R.dmin[i] + R.dmax[i]) / 2:
            rM = R.dmin[i]
        else:
            rM = R.dmax[i]

        if point[i] <= (R.dmin[i] + R.dmax[i]) / 2:
            rm = R.dmin[i]
        else:
            rm = R.dmax[i]

        dist = S - (point[i] - rM) ** 2 + (point[i] - rm) ** 2
        if dist < minmax_dist:
            minmax_dist = dist

    return minmax_dist