import math

def PickSeeds(all_node_entries):
    init_entries_idx = [-1, -1]
    max_dist = float('-inf')

    # [PS1]
    for i in range(len(all_node_entries)):
        for j in range(i+1, len(all_node_entries)):
            entry1 = all_node_entries[i]
            entry2 = all_node_entries[j]

            assert len(entry1.dmax) == len(entry2.dmax)
            dim = len(entry1.dmax)

            # Get the Combined Node
            dmin_combine = [min(entry1.dmin[idx], entry2.dmin[idx])
                            for idx in range(dim)]
            dmax_combine = [max(entry1.dmax[idx], entry2.dmax[idx])
                            for idx in range(dim)]

            # Calculating d = Area(Entry1+Entry2) - Area(Entry1) - Area(Entry2)
            # NOTE: log is taken for numerical stability and avoid overflow
            area1 = sum(math.log(entry1.dmax[idx] - entry1.dmin[idx])
                        for idx in range(dim) if entry1.dmax[idx] != entry1.dmin[idx])
            area2 = sum(math.log(entry2.dmax[idx] - entry2.dmin[idx])
                        for idx in range(dim) if entry2.dmax[idx] != entry2.dmin[idx])
            area_combine = sum(math.log(dmax_combine[idx] - dmin_combine[idx])
                               for idx in range(dim) if dmax_combine[idx] != dmin_combine[idx])
            d = area_combine - area1 - area2

            # [PS2]
            if d > max_dist:
                max_dist = d
                init_entries_idx[0] = i
                init_entries_idx[1] = j

    return init_entries_idx