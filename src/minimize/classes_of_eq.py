class DisjointSet:
    def __init__(self, elements):
        self.disjoint_set = list()
        if elements:
            for el in set(elements):
                self.disjoint_set.append([el])

    def find(self, el):
        for _set in self.disjoint_set:
            if el in _set:
                return _set
        return None

    def union(self, el_1, el_2):
        index_1 = None
        index_2 = None

        for _set in self.disjoint_set:
            for i in _set:
                if i == el_1:
                    index_1 = self.disjoint_set.index(_set)
                if i == el_2:
                    index_2 = self.disjoint_set.index(_set)

        if index_1 != index_2:
            self.disjoint_set[index_1] += self.disjoint_set[index_2]
            del self.disjoint_set[index_2]

    def get(self):
        return self.disjoint_set
