
class Node:
    def __init__(self, loc, h=None, g=None, father=None):
        self.loc = loc
        self.h = h
        self.g = g
        self.father = father

    def __eq__(self, other):
        return self.loc == other.loc

    def __repr__(self):
        return str(self.loc)

    def get_father(self):
        return self.father

    def get_loc(self):
        return self.loc

    def get_path(self, lst=None):
        if lst is None:
            lst = list()
        lst.append(self.loc)
        if self.father:
            Node.get_path(self.get_father(), lst)
        return lst

    def copy(self):
        return Node(self.loc, self.h, self.g, self.father)

    def get_f(self, w):
        return w*self.h + (1-w)*self.g

    def get_heurisitic(self, target, D=1, D2=1):
        dx = abs(self.loc[0] - target[0])
        dy = abs(self.loc[1] - target[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
