def read_file(filename):
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
