import random
import toml
import os

config_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'config', 'config.toml')
config = toml.load(config_path)

# Constants
# Number of query rectangles searched
LOWER = config['rtree']['LOWER']
UPPER = config['rtree']['UPPER']
n = config['rtree']['n']

def gen_query_point():
    return [random.randint(LOWER, UPPER) for _ in range(n)]
