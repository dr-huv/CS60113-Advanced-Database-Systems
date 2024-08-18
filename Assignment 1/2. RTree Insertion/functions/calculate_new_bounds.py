def calculate_new_bounds(cur_entry, new_entry):
    """Calculate the new bounding box when adding a new entry."""
    new_dmin = [min(cur_entry.dmin[i], new_entry.dmin[i])
                for i in range(len(cur_entry.dmin))]
    new_dmax = [max(cur_entry.dmax[i], new_entry.dmax[i])
                for i in range(len(cur_entry.dmax))]
    return new_dmin, new_dmax