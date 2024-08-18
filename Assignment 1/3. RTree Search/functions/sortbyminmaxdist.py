def sortbyminmaxdist(able1, able2):
    if able1.minmaxdist != able2.minmaxdist:
        return able1.minmaxdist - able2.minmaxdist
    return able1.mindist - able2.mindist