class RTNodeEntry:
    def __init__(self, dmin=None, dmax=None, RTNodeEntry_num=0, child=None):
        self.dmin = dmin if dmin is not None else []
        self.dmax = dmax if dmax is not None else []
        self.RTNodeEntry_num = RTNodeEntry_num
        self.child = child  # This will hold a reference to a child RTNode