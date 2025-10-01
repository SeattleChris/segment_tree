#!/bin/python3

# Python3 program to show segment tree operations like construction, query and update
from math import ceil, log2


class SegmentTree:
    def __init__(self, data, func=sum, initial=0):
        self.n = len(data)
        self.size = 2 * (2 ** ceil(log2(self.n))) - 1
        self.tree = [0] * self.size
        self._func = func
        if not isinstance(initial, (list, tuple)):
            initial = [initial]
        self.initial = initial
        self.build(data, 0, self.n - 1, 0)

    def build(self, data, start, end, index):
        if start == end:
            self.tree[index] = data[start]
            return data[start]
        mid = (start + end) // 2
        a = self.build(data, start, mid, index * 2 + 1)
        b = self.build(data, mid + 1, end, index * 2 + 2)
        self.tree[index] = self._op(a, b)
        return self.tree[index]

    def _op(self, *args):
        if not args:
            return 0
        return self._func(*self.initial, *args)

    def query(self, left, right):
        if left < 0 or right > self.n - 1 or left > right:
            raise ValueError("Invalid Input")
        return self._query_util(0, self.n - 1, left, right, 0)

    def _query_util(self, start, end, left, right, index):
        if left <= start and right >= end:
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


def getMid(s, e) :
    """ A utility function to get the middle index from corner indexes. """
    return s + (e - s) // 2

def getSumUtil(st, ss, se, qs, qe, si) :
    """ A recursive function to get the sum of values in the given range of the array.
        The following are parameters for this function.

        st --> Pointer to segment tree
        si --> Index of current node in the segment tree.
            Initially 0 is passed as root is always at index 0
        ss & se --> Starting and ending indexes of the segment
                    represented by current node, i.e., st[si]
        qs & qe --> Starting and ending indexes of query range """

    # If segment of this node is a part of given range, return the sum of the segment
    if qs <= ss and qe >= se:
        return st[si]
    # If segment of this node is outside the given range
    if se < qs or ss > qe:
        return 0
    # If a part of this segment overlaps with the given range
    mid = getMid(ss, se)
    return (getSumUtil(st, ss, mid, qs, qe, 2 * si + 1) +
           getSumUtil(st, mid + 1, se, qs, qe, 2 * si + 2))

def updateValueUtil(st, ss, se, i, diff, si) :
    """ A recursive function to update the nodes which have the given index in their range.
    The following are parameters st, si, ss and se are same as getSumUtil()
    i --> index of the element to be updated.
        This index is in the input array.
    diff --> Value to be added to all nodes which have i in range """
    if i < ss or i > se:
        return  # Base Case: Input index lies outside the range of this segment
    st[si] = st[si] + diff
    if se != ss:
        mid = getMid(ss, se)
        updateValueUtil(st, ss, mid, i,
                        diff, 2 * si + 1)
        updateValueUtil(st, mid + 1, se, i,
                         diff, 2 * si + 2)

def updateValue(arr, st, n, i, new_val) :
    """ The function to update a value in input array and segment tree.
        It uses updateValueUtil() to update the value in segment tree."""
    if i < 0 or i > n - 1:
        raise ValueError("Invalid Input")
    diff = new_val - arr[i]
    arr[i] = new_val
    updateValueUtil(st, 0, n - 1, i, diff, 0)

def getSum(st, n, qs, qe) :
    """ Return sum of elements in range from index qs (query start)
        to qe (query end). It mainly uses getSumUtil()."""
    if qs < 0 or qe > n - 1 or qs > qe:
        raise ValueError("Invalid Input")
    return getSumUtil(st, 0, n - 1, qs, qe, 0)

def constructSTUtil(arr, ss, se, st, si) :
    """ A recursive function that constructs Segment Tree for array[ss..se].
        The si is index of current node in segment tree st."""

    # If there is one element in array, store it in current node of segment tree and return
    if ss == se:
        st[si] = arr[ss]
        return arr[ss]
    # If there are more than one elements, then recur for left and right subtrees and store the sum of values in this node
    mid = getMid(ss, se)
    st[si] = (constructSTUtil(arr, ss, mid, st, si * 2 + 1) +
             constructSTUtil(arr, mid + 1, se, st, si * 2 + 2))
    return st[si]

def constructST(arr, n) :
    """ Function to construct segment tree from given array. This function allocates
        memory for segment tree and calls constructSTUtil() to fill the allocated memory."""
    x = int(ceil(log2(n)))  # Height of segment tree
    max_size = 2 * 2 ** x - 1  # Maximum size of segment tree
    st = [0] * max_size
    constructSTUtil(arr, 0, n - 1, st, 0)
    return st

# Driver Code
if __name__ == "__main__" :
    arr = [1, 3, 5, 7, 9, 11]
    n = len(arr)
    # Build segment tree from given array
    # st = constructST(arr, n)
    st = SegmentTree(arr)
    # Print sum of values in array from index 1 to 3
    print("Sum of values in given range = ",
    #                   getSum(st, n, 1, 3))
                       st.query(1, 3))
    # Update: set arr[1] = 10 and update
    # corresponding segment tree nodes
    # updateValue(arr, st, n, 1, 10)
    st.update(1, 10)
    # Find sum after the value is updated
    print("Updated sum of values in given range = ",
    #                 getSum(st, n, 1, 3), end = "")
                     st.query(1, 3), end = "")
