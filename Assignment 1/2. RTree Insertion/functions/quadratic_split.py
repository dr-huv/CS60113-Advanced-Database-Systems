from functions.pick_seeds import PickSeeds
from functions.pick_next import PickNext
import toml,os
import math

config_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'config', 'config.toml')
config = toml.load(config_path)

n = config['rtree']['n']
M = eval(config['rtree']['M'])
m = eval(config['rtree']['m'])

def QuadraticSplit(node1, node2, node_entry_ptr):
    assert len(node1.entry) == M
    num_entries_assigned = 0

    # Copy all the entries into a single list
    all_node_entries = node1.entry.copy()
    all_node_entries.append(node_entry_ptr)

    node1.entry.clear()  # Clear the entries in node1

    init_entries_idx = PickSeeds(all_node_entries)

    if init_entries_idx[0] == -1 or init_entries_idx[1] == -1:
        print("[ERROR] Cannot find Pick Seeds index!!")
        return False

    # Creating initial two groups
    node1.entry.append(all_node_entries[init_entries_idx[0]])
    node2.entry.append(all_node_entries[init_entries_idx[1]])

    if node1.entry[-1].child is not None:
        node1.entry[-1].child.parent = node1
    if node2.entry[-1].child is not None:
        node2.entry[-1].child.parent = node2

    print(
        f"{all_node_entries[init_entries_idx[0]].RTNodeEntry_num} NodeEntry is put in Node {node1.RTNode_num} after split")
    print(
        f"{all_node_entries[init_entries_idx[1]].RTNodeEntry_num} NodeEntry is put in Node {node2.RTNode_num} after split")

    # Delete corresponding elements from all_node_entries
    # Remove the larger index first
    all_node_entries.pop(max(init_entries_idx[0], init_entries_idx[1]))
    # Then remove the smaller index
    all_node_entries.pop(min(init_entries_idx[0], init_entries_idx[1]))
    num_entries_assigned += 2

    # [QS2]
    while num_entries_assigned < M + 1:
        # If one group has so few entries that all the rest must
        # be assigned to it in order for it to have the minimum number m
        if len(node1.entry) + (M + 1 - num_entries_assigned) == m:
            for entry in all_node_entries:
                node1.entry.append(entry)
                if node1.entry[-1].child is not None:
                    node1.entry[-1].child.parent = node1
                print(
                    f"{entry.RTNodeEntry_num} NodeEntry is put in Node {node1.RTNode_num} after split")
                num_entries_assigned += 1
            all_node_entries.clear()
            return True

        if len(node2.entry) + (M + 1 - num_entries_assigned) == m:
            for entry in all_node_entries:
                node2.entry.append(entry)
                if node2.entry[-1].child is not None:
                    node2.entry[-1].child.parent = node2
                print(
                    f"{entry.RTNodeEntry_num} NodeEntry is put in Node {node2.RTNode_num} after split")
                num_entries_assigned += 1
            all_node_entries.clear()
            return True

        # [QS3]
        next_entry = PickNext(node1, node2, all_node_entries)
        if next_entry[0] == -1 or next_entry[1] == -1:
            print("[ERROR] Cannot find Pick Next index!!")
            return False

        # Enter the entry to the corresponding group according to 'identify_group' field of the array
        if next_entry[1] == 0:
            node1.entry.append(all_node_entries[next_entry[0]])
            if node1.entry[-1].child is not None:
                node1.entry[-1].child.parent = node1
            print(
                f"{all_node_entries[next_entry[0]].RTNodeEntry_num} NodeEntry is put in Node {node1.RTNode_num} after split")
        else:
            node2.entry.append(all_node_entries[next_entry[0]])
            if node2.entry[-1].child is not None:
                node2.entry[-1].child.parent = node2
            print(
                f"{all_node_entries[next_entry[0]].RTNodeEntry_num} NodeEntry is put in Node {node2.RTNode_num} after split")

        # Delete corresponding element from all_node_entries
        all_node_entries.pop(next_entry[0])
        num_entries_assigned += 1

    return True