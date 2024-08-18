from classes.RTNodeEntry import RTNodeEntry
from classes.RTNode import RTNode
from functions.quadratic_split import QuadraticSplit
from functions.adjust_tree import AdjustTree
from functions.choose_leaf import ChooseLeaf
import toml
import os
import math

config_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'config', 'config.toml')
config = toml.load(config_path)

n = config['rtree']['n']
M = config['rtree']['M']
RTNodeEntryNum = config['rtree']['RTNodeEntryNum']
RTNodeNum = config['rtree']['RTNodeNum']

def Insert(filename, dim):
    global RTNodeNum, RTNodeEntryNum
    try:
        with open(filename, "r") as fin:
            root = None
            while line := fin.readline().strip():
                print()

                entry = RTNodeEntry([], [], RTNodeEntryNum)
                entry.RTNodeEntry_num = RTNodeEntryNum
                RTNodeEntryNum += 1
                print(f"NodeEntry {entry.RTNodeEntry_num} for new data")
                entry.child = None

                dmin, dmax = [], []
                flag = 0
                for token in line.split():
                    if token != "0" or token == "0":
                        if not flag:
                            dmin.append(int(token))
                            flag = 1
                        else:
                            dmax.append(int(token))
                            flag = 0
                entry.dmin = dmin.copy()
                entry.dmax = dmax.copy()

                entry_node = ChooseLeaf(root, entry)

                if entry_node is None:
                    entry_node = RTNode(RTNodeNum)
                    RTNodeNum += 1
                    print(f"Node num {entry_node.RTNode_num} is current root")
                    entry_node.parent = None
                    root = entry_node

                print(f"Node {entry_node.RTNode_num} is chosen as leaf")

                new_node = None
                if len(entry_node.entry) < M:
                    print(
                        f"{entry.RTNodeEntry_num} NodeEntry in Node {entry_node.RTNode_num} originally")
                    entry_node.entry.append(entry)
                    split_nodes = AdjustTree(entry_node, None, dim)
                else:
                    new_node = RTNode(RTNodeNum)
                    RTNodeNum += 1
                    print(
                        f"New Node {new_node.RTNode_num} is getting created during Insertion")
                    new_node.parent = entry_node.parent

                    QuadraticSplit(entry_node, new_node, entry)

                    split_nodes = AdjustTree(entry_node, new_node, dim)

                    if split_nodes[1] is not None and split_nodes[0].parent is None and split_nodes[1].parent is None:
                        new_root = RTNode(RTNodeNum)
                        RTNodeNum += 1
                        new_root.parent = None
                        print("New Root creation necessary")

                        entry1 = RTNodeEntry([], [], RTNodeEntryNum)
                        RTNodeEntryNum += 1
                        entry1.child = split_nodes[0]

                        dmin_node = [float('inf')] * dim
                        dmax_node = [float('-inf')] * dim
                        for entry in split_nodes[0].entry:
                            for idx in range(dim):
                                dmin_node[idx] = min(
                                    dmin_node[idx], entry.dmin[idx])
                                dmax_node[idx] = max(
                                    dmax_node[idx], entry.dmax[idx])
                        entry1.dmin = dmin_node.copy()
                        entry1.dmax = dmax_node.copy()

                        entry2 = RTNodeEntry([], [], RTNodeEntryNum)
                        RTNodeEntryNum += 1
                        entry2.child = split_nodes[1]

                        dmin_node = [float('inf')] * dim
                        dmax_node = [float('-inf')] * dim
                        for entry in split_nodes[1].entry:
                            for idx in range(dim):
                                dmin_node[idx] = min(
                                    dmin_node[idx], entry.dmin[idx])
                                dmax_node[idx] = max(
                                    dmax_node[idx], entry.dmax[idx])
                        entry2.dmin = dmin_node.copy()
                        entry2.dmax = dmax_node.copy()

                        new_root.entry.append(entry1)
                        new_root.entry.append(entry2)

                        print(
                            f"NodeEntry {entry1.RTNodeEntry_num} and {entry2.RTNodeEntry_num} pointing Node {entry1.child.RTNode_num} and {entry2.child.RTNode_num} in New Root Node {new_root.RTNode_num}")

                        split_nodes[0].parent = new_root
                        split_nodes[1].parent = new_root

                        root = new_root
                        print(f"Node {root.RTNode_num} is new root")

            return root
    except FileNotFoundError:
        print("[ERROR] Cannot Open File")
        return None