from functions.quadratic_split import QuadraticSplit
from classes.RTNodeEntry import RTNodeEntry
from classes.RTNode import RTNode
import toml
import os
import math

config_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'config', 'config.toml')
config = toml.load(config_path)
n = config['rtree']['n']
M = eval(config['rtree']['M'])
RTNodeEntryNum = config['rtree']['RTNodeEntryNum']
RTNodeNum = config['rtree']['RTNodeNum']

def AdjustTree(node1, node2, dim: int):
    global RTNodeNum, RTNodeEntryNum
    # [AT2]
    if node1.parent is None:
        return [node1, node2]

    # [AT3]
    P = node1.parent
    PP = None
    for entry in P.entry:
        # If node1->parent->child == node1
        if entry.child.RTNode_num == node1.RTNode_num:
            # For all entries in node1, check the minimum and maximum among each dimension
            dmin_node = [float('inf')] * dim
            dmax_node = [float('-inf')] * dim
            for child_entry in node1.entry:
                for idx in range(dim):
                    dmin_node[idx] = min(dmin_node[idx], child_entry.dmin[idx])
                    dmax_node[idx] = max(dmax_node[idx], child_entry.dmax[idx])
            entry.dmin = dmin_node.copy()
            entry.dmax = dmax_node.copy()
            break

    # [AT4]
    if node2 is not None:
        # For all entries in node2, check the minimum and maximum among each dimension
        dmin_node = [float('inf')] * dim
        dmax_node = [float('-inf')] * dim
        for entry in node2.entry:
            for idx in range(dim):
                dmin_node[idx] = min(dmin_node[idx], entry.dmin[idx])
                dmax_node[idx] = max(dmax_node[idx], entry.dmax[idx])

        # New NodeList to be inserted in parent node of node2
        new_node_entry = RTNodeEntry(dmin_node, dmax_node, RTNodeEntryNum)
        new_node_entry.child = node2
        RTNodeEntryNum += 1

        # If there is space in the parent node, make an entry
        if len(P.entry) < M:
            P.entry.append(new_node_entry)
            print(
                f"{new_node_entry.RTNodeEntry_num} NodeEntry is put in Node {P.RTNode_num} while adjusting")
            PP = None
        else:
            PP = RTNode(RTNodeNum)
            RTNodeNum += 1
            print(
                f"New Node {PP.RTNode_num} is getting created while adjusting")
            PP.parent = P.parent
            QuadraticSplit(P, PP, new_node_entry)

    return AdjustTree(P, PP, dim)