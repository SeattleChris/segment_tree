#!/bin/python3
import os
from math import ceil, log2


class SegmentTree:
    def __init__(self, data, func=max, initial=float("-inf")):
        self._func = func
        # if not isinstance(initial, (list, tuple)):
        #     initial = [initial]
        self.initial = initial
        self.n = len(data)
        self.size = 2 * (2 ** ceil(log2(self.n))) - 1
        self.tree = [initial] * self.size
        self.idxmap = [initial] * self.size
        self.datamap = {}
        self.build(data, 0, self.n - 1, 0)

    def build(self, data, start, end, index):
        if start == end:
            print(f"  SE {start} {index=}")
            self.tree[index] = data[start]
            self.idxmap[index] = (start, end)
            self.datamap[index] = start
            return data[start]
        mid = (start + end) // 2
        a = self.build(data, start, mid, index * 2 + 1)
        b = self.build(data, mid + 1, end, index * 2 + 2)
        self.tree[index] = self._op(a, b)
        self.idxmap[index] = (start, end)
        return self.tree[index]

    def _op(self, *args):
        if not args:
            return 0
        result = self.initial
        for arg in args:
            result = self._func(result, arg)
        return result

    def query(self, left, right):
        """Returns the _op result between given indicies of original data."""
        if left < 0 or right > self.n - 1 or left > right:
            raise ValueError("Invalid Input")
        return self._query_util(0, self.n - 1, left, right, 0)

    def _query_util(self, start, end, left, right, index):
        if left <= start and right >= end:  # left == start and right == end
            return self.tree[index]
        if end < left or start > right:
            return 0
        mid = (start + end) // 2
        a = self._query_util(start, mid, left, right, 2 * index + 1)
        b = self._query_util(mid + 1, end, left, right, 2 * index + 2)
        return self._op(a, b)

    def update(self, idx, value):
        if idx < 0 or idx > self.n - 1:
            raise ValueError("Invalid Input")
        diff = value - self.get_value(idx)
        self._update_util(0, self.n - 1, idx, diff, 0)

    def _update_util(self, start, end, idx, diff, index):
        if idx < start or idx > end:
            return
        self.tree[index] += diff
        if start != end:
            mid = (start + end) // 2
            self._update_util(start, mid, idx, diff, 2 * index + 1)
            self._update_util(mid + 1, end, idx, diff, 2 * index + 2)

    def get_value(self, idx):
        return self._get_value_util(0, self.n - 1, idx, 0)

    def _get_value_util(self, start, end, idx, index):
        if start == end:
            return self.tree[index]
        mid = (start + end) // 2
        if idx <= mid:
            return self._get_value_util(start, mid, idx, 2 * index + 1)
        else:
            return self._get_value_util(mid + 1, end, idx, 2 * index + 2)

    def node_range(self, index):
        # left = 2*i +1
        # right = 2*i +2
        # parent = (i - 1) // 2
        result = self.idxmap[index]
        if not isinstance(result, tuple):
            return None
        return result

    def match_value(self, target):
        lo = min(ea for ea in self.tree if ea != self.initial)
        hi = max(ea for ea in self.tree if ea != self.initial)
        lows = [self.node_range(i) for i, val in enumerate(self.tree) if val == lo]
        high = [self.node_range(i) for i, val in enumerate(self.tree) if val == hi]
        return {
            'limits': (lo, hi),
            'lo': lows,
            'hi': high,
            'datamap': self.datamap.items()
        }

def find_close(st):
    deduct = [i for i in range(st.n)]
    target = sum(deduct)
    return st.match_value(target)


def solve(t):
    hi = SegmentTree(t)
    lo = SegmentTree(t, min, float("inf"))
    result = 0
    # for index, res in enumerate(hi.tree):
    #     rng = hi.node_range(index)
    #     print(f"{index}: {res=} {rng}")
    tmp = hi.match_value(0)
    print("** ST max **")
    for key in tmp:
        print(f"{key}: {' '.join(str(v) for v in tmp[key])} ")
    tmp = lo.match_value(0)
    print("** ST min **")
    for key in tmp:
        print(f"{key}: {' '.join(str(v) for v in tmp[key])} ")

    # near = find_close(st)
    # for key in near:
    #     print(f"{key}: {' '.join(str(v) for v in near[key])} ")
    # best = max(key for key in near)
    # group = near[best]
    # result = min(group)
    # print(f"{result=} {group}")
    return result
    #
    # Return the ID
    #

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    t_count = int(input())
    t = list(map(int, input().rstrip().split()))
    id = solve(t)
    fptr.write(str(id) + '\n')
    fptr.close()
