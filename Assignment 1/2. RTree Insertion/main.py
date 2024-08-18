from functions.RTree_insert import Insert
from functions.write_tree import WriteTree
import os
import toml

config_path = os.path.join(os.path.dirname(
    __file__), '..', 'config', 'config.toml')
config = toml.load(config_path)

n = config['rtree']['n']
N = config['rtree']['N']

in_filename = f"../DATA/testdata_dim={n}_N={N}.txt"
out_filename = f"../DATA/RTree_dim={n}_N={N}.txt"

root_node = Insert(in_filename, n)

with open(out_filename, "w") as fout:
    WriteTree(root_node, fout)