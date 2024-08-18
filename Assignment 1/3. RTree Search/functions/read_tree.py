from classes.RTNodeEntry import RTNodeEntry
from classes.RTNode import RTNode
import toml,os

config_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'config', 'config.toml')
config = toml.load(config_path)

# Constants
# Number of query rectangles searched
N_TRIALS = config['rtree']['N_TRIALS']

n = config['rtree']['n']

def read_tree(node, lines):
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
            read_tree(cur_entry.child, lines)
