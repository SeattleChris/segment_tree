from numbers import Number

class SegmentTree:
    def __init__(self, array):
        self.size = len(array)
        self.tree = [0] * (4 * self.size)
        self.build_tree(array, 0, 0, self.size - 1)

    def build_tree(self, array, tree_index, left, right):
        if left == right:
            self.tree[tree_index] = array[left]
            return
        mid = (left + right) // 2
        self.build_tree(array, 2 * tree_index + 1, left, mid)
        self.build_tree(array, 2 * tree_index + 2, mid + 1, right)
        self.tree[tree_index] = min(self.tree[2 * tree_index + 1], self.tree[2 * tree_index + 2])

    def _op(self) -> (callable, Number):
        return max, float('-inf')


    def _query(self, tree_index, left, right, query_left, query_right):
        if query_left <= left and right <= query_right:
            return self.tree[tree_index]
        mid = (left + right) // 2
        func, val = self._op()
        if query_left <= mid:
            ltree = self._query(2 * tree_index + 1, left, mid, query_left, query_right)
            val = func(val, ltree)
        if query_right > mid:
            rtree = self._query(2 * tree_index + 2, mid + 1, right, query_left, query_right)
            val = func(val, rtree)
        return val

    def query(self, left, right):
        return self._query(0, 0, self.size - 1, left, right)


class MinSegTree(SegmentTree):
    def __init__(self, array):
        super().__init__(array)

    def _op(self) -> (callable, Number):
        return min, float('inf')


class sumSegTree(SegmentTree):
    def __init__(self, array):
        super().__init__(array)

    def _op(self) -> (callable, Number):
        return sum, 0


if __name__ == '__main__':
    array = [1, 3, 2, 5, 4, 6]
    st = SegmentTree(array)
    print(st.query(1, 5)) # 2