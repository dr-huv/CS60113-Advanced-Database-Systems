class RTNode:
    def __init__(self, RTNode_num=0, parent=None):
        self.entry = []  # This will hold a list of RTNodeEntry objects
        self.RTNode_num = RTNode_num
        self.parent = parent  # This will hold a reference to the parent RTNode