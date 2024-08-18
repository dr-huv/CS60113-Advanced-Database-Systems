def objdist(point, object_):
    return sum((point[i] - object_[i]) ** 2 for i in range(len(point)))
