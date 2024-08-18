def mindist(point, R):
    min_dist = 0

    for i in range(len(point)):
        if point[i] < R.dmin[i]:
            min_dist += (point[i] - R.dmin[i]) ** 2
        elif point[i] > R.dmax[i]:
            min_dist += (point[i] - R.dmax[i]) ** 2

    return min_dist