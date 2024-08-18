import toml
import math

# Load the TOML configuration file
config = toml.load('./config/config.toml')

# Retrieve values
n = config['rtree']['n']
M_expression = config['rtree']['M_expression']
m_expression = config['rtree']['m_expression']

# Evaluate expressions
M = eval(M_expression)
m = eval(m_expression)

print(f"M: {M}, m: {m}")  # Output: M: 1024, m: 512