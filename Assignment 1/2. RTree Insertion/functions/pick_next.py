import math

def PickNext(node1, node2, all_node_entries):
    next_entry_idx = -1
    identify_group = -1
    dim = len(all_node_entries[0].dmax)

    area_inc1, area_inc2 = [], []

    # [PN1]

    # Calculate Current Area for bounding box of Group 1 and Group 2
    curr_area1 = curr_area2 = 0.0
    dmin_node_curr1 = [float('inf')] * dim
    dmax_node_curr1 = [float('-inf')] * dim
    dmin_node_curr2 = [float('inf')] * dim
    dmax_node_curr2 = [float('-inf')] * dim

    # Group 1
    for entry in node1.entry:
        for idx in range(dim):
            dmin_node_curr1[idx] = min(dmin_node_curr1[idx], entry.dmin[idx])
            dmax_node_curr1[idx] = max(dmax_node_curr1[idx], entry.dmax[idx])

    for idx in range(dim):
        if dmax_node_curr1[idx] > dmin_node_curr1[idx]:
            curr_area1 += math.log(dmax_node_curr1[idx] - dmin_node_curr1[idx])

    # Group 2
    for entry in node2.entry:
        for idx in range(dim):
            dmin_node_curr2[idx] = min(dmin_node_curr2[idx], entry.dmin[idx])
            dmax_node_curr2[idx] = max(dmax_node_curr2[idx], entry.dmax[idx])

    for idx in range(dim):
        if dmax_node_curr2[idx] > dmin_node_curr2[idx]:
            curr_area2 += math.log(dmax_node_curr2[idx] - dmin_node_curr2[idx])

    # Calculate increase in Area
    for entry in all_node_entries:
        new_area1 = new_area2 = 0.0

        for idx in range(dim):
            # Group 1
            dmin_node = min(dmin_node_curr1[idx], entry.dmin[idx])
            dmax_node = max(dmax_node_curr1[idx], entry.dmax[idx])
            if dmax_node != dmin_node:
                new_area1 += math.log(dmax_node - dmin_node)

            # Group 2
            dmin_node = min(dmin_node_curr2[idx], entry.dmin[idx])
            dmax_node = max(dmin_node_curr2[idx], entry.dmax[idx])
            if dmax_node != dmin_node:
                new_area2 += math.log(dmax_node - dmin_node)

        area_inc1.append(new_area1 - curr_area1)
        area_inc2.append(new_area2 - curr_area2)

    # [PN2]
    max_dist = float('-inf')
    for i in range(len(all_node_entries)):
        if abs(area_inc2[i] - area_inc1[i]) > max_dist:
            max_dist = abs(area_inc2[i] - area_inc1[i])
            next_entry_idx = i

            if area_inc1[i] < area_inc2[i]:
                identify_group = 0
            else:
                identify_group = 1

    return next_entry_idx, identify_group