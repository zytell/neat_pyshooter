from random import randrange
from bisect import insort


class HashList:
    def __init__(self):
        # set for fast and efficient data access
        self.s = set()
        # list for storing items while sorted (with sorted add)
        self.data = list()

    def __contains__(self, item):
        return item in self.s

    def add(self, item):
        if item not in self.s:
            self.s.add(item)
            self.data.append(item)

    def sorted_add(self, item):
        if item not in self.s:
            self.s.add(item)
            insort(self.data, item)

    def __len__(self):
        return len(self.s)

    def select_random(self):
        if len(self) > 0:
            return self.data[randrange(0, len(self))]

    def __getitem__(self, key):
        return self.data[key]

    def __str__(self):
        return str(self.data)

    def remove(self, element):
        self.s.remove(element)
        self.data.remove(element)

    def pop(self, index):
        element = self.data.pop(index)
        self.s.remove(element)
        return element


def main():
    hs = HashList()
    hs.add('1d')
    hs.add('2b')
    hs.add('3a')
    #
    # print(hs)
    # print(hash(hs))
    # # print(hs[2])
    # [print(x, y) for x, y in zip(hs, [1, 2, 3])]  # nice, zip() works!
    #
    print(hs)
    hs.sorted_add('4c')
    print(hs)


if __name__ == '__main__':
    main()
