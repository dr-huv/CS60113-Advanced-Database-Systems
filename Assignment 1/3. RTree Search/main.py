import math
import random
from queue import PriorityQueue
import time
from classes.RTNode import RTNode
from classes.NearestN import NearestN
from classes.ABLEntry import ABLEntry
from functions.read_tree import read_tree
from functions.read_file import read_file
from functions.gen_query_point import gen_query_point
from functions.mindist import mindist
from functions.minmaxdist import minmaxdist
from functions.objdist import objdist

import os
import toml

config_path = os.path.join(os.path.dirname(
    __file__), '..', 'config', 'config.toml')
config = toml.load(config_path)

# Constants
# Number of query rectangles searched
N_TRIALS = config['rtree']['N_TRIALS']

n = config['rtree']['n']
N = config['rtree']['N']

LOWER = config['rtree']['LOWER']
UPPER = config['rtree']['UPPER']

# Global Variables
M = config['rtree']['M']
m = config['rtree']['m']

RTNodeEntryNum = config['rtree']['RTNodeEntryNum']
RTNodeNum = config['rtree']['RTNodeNum']

nodes_visited = 0

k = 1  # Number of nearest neighbors

def knn_search(node, point, nearest):
    global nodes_visited

    if node is None:
        return

    nodes_visited += 1
    num_entry = len(node.entry)

    # Leaf Node
    if node.entry[0].child is None:
        for i in range(num_entry):
            cur_entry = node.entry[i]
            dist = objdist(point, cur_entry.dmin)

            cur_neighbor = NearestN(cur_entry, dist)

            if nearest.qsize() < k:
                nearest.put((-dist, cur_neighbor))
            elif dist < -nearest.queue[0][0]:
                nearest.get()
                nearest.put((-dist, cur_neighbor))
        return

    # Non-leaf Node
    abl = []
    for i in range(num_entry):
        cur_entry = node.entry[i]
        cur_ablentry = ABLEntry(cur_entry, mindist(
            point, cur_entry), minmaxdist(point, cur_entry))
        abl.append(cur_ablentry)

    abl.sort(key=lambda x: (x.minmaxdist, x.mindist))

    for i in range(num_entry):
        if i >= k and abl[i].mindist > abl[0].minmaxdist:
            continue
        if nearest.qsize() >= k and abl[i].mindist > -nearest.queue[0][0]:
            continue
        knn_search(abl[i].entry.child, point, nearest)


def main():
    global n, k, M, m, nodes_visited
    k = 1

    filename = f"../DATA/RTree_dim={n}_N={N}.txt"

    print("Loading File...")
    root_node_num, lines = read_file(filename)
    print("Done Loading")

    root = RTNode()
    root.RTNode_num = root_node_num

    print("Reading Tree...")
    read_tree(root, lines)
    print("Reading Complete\n")
    lines.clear()

    random.seed(time.time())
    query_point = []

    total_time = 0
    total_nodes_visited = 0

    for i in range(N_TRIALS):
        query_point = gen_query_point()
        print(f"Query Point {i}")

        nodes_visited = 0

        nearest = PriorityQueue()

        start = time.time()
        knn_search(root, query_point, nearest)
        end = time.time()

        time_taken = end - start
        total_time += time_taken
        print(f"Time taken: {time_taken}")

        total_nodes_visited += nodes_visited
        print(f"Number of Nodes visited: {nodes_visited}\n")

    print(f"Average Time Taken: {total_time / N_TRIALS}")
    print(f"Average Number of Nodes visited: {total_nodes_visited / N_TRIALS}")


if __name__ == "__main__":
    main()
