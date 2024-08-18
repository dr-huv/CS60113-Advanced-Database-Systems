from functions.calculate_area import calculate_area
from functions.calculate_new_bounds import calculate_new_bounds

def ChooseLeaf(node, E):
    # [CL2]
    if node is None or node.entry[0].child is None:
        return node

    # [CL3]
    min_inc = float('inf')
    min_area = float('inf')
    F = None  # Current best entry

    for cur_entry in node.entry:
        cur_area = calculate_area(cur_entry.dmin, cur_entry.dmax)
        new_dmin, new_dmax = calculate_new_bounds(cur_entry, E)
        new_area = calculate_area(new_dmin, new_dmax)

        area_inc = abs(new_area - cur_area)

        # Update the best entry if this one has the smallest area increase
        if area_inc < min_inc or (area_inc == min_inc and cur_area < min_area):
            min_inc = area_inc
            min_area = cur_area
            F = cur_entry

    print(
        f"Minimum area increase for Choose Leaf is for NodeEntry {F.RTNodeEntry_num}")

    # [CL4]
    return ChooseLeaf(F.child, E) if F else None