import random
# from constants.data_config import *
import os
import toml

config_path = os.path.join(os.path.dirname(
    __file__), '..', 'config', 'config.toml')
config = toml.load(config_path)

n = config['rtree']['n']
N = config['rtree']['N']
LOWER = config['rtree']['LOWER']
UPPER = config['rtree']['UPPER']

def gen_data(n, filename):
    with open(filename, "w") as fout:
        for _ in range(N):
            for _ in range(n):
                
                while True: #just to make sure, max_dim si never less than min_dim (else wrong emaning arises)
                    min_num = random.randint(LOWER, UPPER)
                    max_num = random.randint(LOWER, UPPER)

                    if max_num >= min_num: 
                        break

                fout.write(f'{min_num} {max_num} ') #writing maximum and minimum values of a particular dimesnion (not all the dimensions, we are writing dimension by dimension)

            fout.write('\n') # we use this to go to a new line to store all the dimensions of the next sample object

filename = f"../DATA/testdata_dim={n}_N={N}.txt"

gen_data(n, filename)