def WriteTree(node, fout):
    if node is None:
        print("No RTree formed")
        return

    fout.write(f"{node.RTNode_num} ")

    if node.parent is not None:
        fout.write(f"{node.parent.RTNode_num} ")
    else:
        fout.write("-1 ")

    dim = len(node.entry[0].dmin) if node.entry else 0
    num_entry = len(node.entry)

    fout.write(f"{num_entry} ")

    for cur_entry in node.entry:
        fout.write(f"{cur_entry.RTNodeEntry_num} ")

        for j in range(dim):
            fout.write(f"{cur_entry.dmin[j]} {cur_entry.dmax[j]} ")

        child_node_num = cur_entry.child.RTNode_num if cur_entry.child is not None else -1
        fout.write(f"{child_node_num} ")

    fout.write("\n")

    for cur_entry in node.entry:
        if cur_entry.child is not None:
            WriteTree(cur_entry.child, fout)