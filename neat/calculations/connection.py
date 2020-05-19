
class Connection:
    # like connection_gene, but without redundant info for calculation like innov nums
    def __init__(self, prev, next):
        super().__init__()
        self.prev = prev
        self.next = next

        self.weight = 1.0
        self.enabled = True

    def __eq__(self, other):
        if type(other) != Connection:
            return False
        return self.prev == other.prev and self.next == other.next

    def copy(self):
        cg = Connection(self.prev, self.next)
        cg.weight = self.weight
        cg.enabled = cg.enabled
        return cg
