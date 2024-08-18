import math
import random
import time


class RTNodeEntry:
    def __init__(self):
        self.dmin = []
        self.dmax = []
        self.RTNodeEntry_num = -1
        self.child = None


class RTNode:
    def __init__(self):
        self.entry = []
        self.RTNode_num = -1
        self.parent = None

# Constants
N = 5000  # N = 0.5 million (number of data points)
N_Trials = 5000  # Number of query rectangles searched

# Range of random numbers generated
LOWER = 0
UPPER = 20

# Global Variables for Max and Min number of children
M = -1
m = -1
RTNodeEntryNum = 0
RTNodeNum = 0
n = -1  # dimension of rectangles
nodes_visited = 0

# Read tree from a dictionary of lines (each line corresponds to a node)


def ReadTree(node, lines):
    if node is None:
        return

    # Find the line corresponding to the current node
    line_tmp = lines[node.RTNode_num]
    line = line_tmp.split()

    node_num = int(line[0])
    parent_node_num = int(line[1])
    num_entry = int(line[2])

    for i in range(num_entry):
        cur_entry = RTNodeEntry()
        cur_entry.RTNodeEntry_num = int(line[3 + i * (2 * n + 2)])

        cur_entry.dmin = [int(line[4 + i * (2 * n + 2) + j * 2])
                          for j in range(n)]
        cur_entry.dmax = [int(line[5 + i * (2 * n + 2) + j * 2])
                          for j in range(n)]

        # Add child node to the rectangle
        child_node_num = int(line[3 + i * (2 * n + 2) + 2 * n + 1])

        if child_node_num != -1:
            cur_entry.child = RTNode()
            cur_entry.child.RTNode_num = child_node_num
            cur_entry.child.parent = node
        else:
            cur_entry.child = None

        node.entry.append(cur_entry)

    # Read subtrees
    for i in range(num_entry):
        cur_entry = node.entry[i]
        if cur_entry.child is not None:
            ReadTree(cur_entry.child, lines)


# Read the file and store it in memory


def ReadFile(filename):
    with open(filename, 'r') as fin:
        lines = {}
        root_line = fin.readline().strip()
        parts = root_line.split()

        # Assuming the root node number is the first integer in the first line
        root_node_num = int(parts[0])

        # Store the first line with the node number as the key
        lines[root_node_num] = root_line

        # Process the rest of the file
        for line in fin:
            line = line.strip()
            if line:
                parts = line.split()
                node_num = int(parts[0])
                lines[node_num] = line

    return root_node_num, lines

# Search RTree Algorithm
# Returns all rectangles that overlap with the query rectangle


def Search(node, S, out):
    global nodes_visited
    if node is None:
        return

    nodes_visited += 1
    num_entry = len(node.entry)

    for i in range(num_entry):
        cur_entry = node.entry[i]

        # Check overlap between current entry and query rectangle
        overlap = True
        for j in range(n):
            if cur_entry.dmax[j] < S.dmin[j] or cur_entry.dmin[j] > S.dmax[j]:
                overlap = False
                break

        if overlap:
            # If the current entry has a child node, search recursively
            if cur_entry.child is not None:
                Search(cur_entry.child, S, out)
            else:
                # If it's a leaf node, add to result
                out.append(cur_entry)


def gen_query_rect():
    min_num, max_num = 0, 0

    query_rect = RTNodeEntry()
    query_rect.child = None
    query_rect.RTNodeEntry_num = -1

    query_rect.dmin = []
    query_rect.dmax = []

    for i in range(n):
        while True:
            min_num = random.randint(LOWER, UPPER)
            max_num = random.randint(LOWER, UPPER)
            if max_num >= min_num:
                break
        query_rect.dmin.append(min_num)
        query_rect.dmax.append(max_num)

    return query_rect
# Print Entry


def printEntry(R):
    for i in range(n):
        print(R.dmin[i], R.dmax[i], end=' ')
    print()


# Main function
if __name__ == "__main__":
    import sys

    # Sanity Check for CLI
    n = 4

    # Create filename
    filename = f"../DATA/RTree_dim={n}_N={N}.txt"

    # Initialize M and m (Max and Min number of children for a node)
    M = math.floor(4096 / (4 * n + 1))
    m = math.floor(M / 2)

    print("Loading File...")
    root_node_num, lines = ReadFile(filename)
    print("Done Loading")

    root = RTNode()
    root.parent = None
    root.RTNode_num = root_node_num

    print("Reading Tree...")
    ReadTree(root, lines)
    print("Reading Complete\n")
    lines.clear()

    random.seed(time.time())
    total_time = 0
    total_nodes_visited = 0

    for i in range(N_Trials):
        query_rect = gen_query_rect()
        print(f"Query Rectangle {i}")

        nodes_visited = 0

        start = time.time()
        out = []
        Search(root, query_rect, out)
        end = time.time()

        time_taken = end - start
        total_time += time_taken
        print(f"Time taken : {time_taken}")

        total_nodes_visited += nodes_visited
        print(f"Number of Nodes visited : {nodes_visited}")

        print(f"Overlapping Rectangles : {len(out)}\n")

    print(f"Average Time Taken : {total_time / N_Trials}")
    print(
        f"Average Number of Nodes visited : {total_nodes_visited / N_Trials}")
