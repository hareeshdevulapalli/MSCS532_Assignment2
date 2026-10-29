"""Merge Sort.

This module follows the MERGE-SORT and MERGE procedures from Chapter 2 of
Introduction to Algorithms (Cormen et al., 4th ed.). The list is split in
half, each half is sorted recursively, and the two sorted halves are merged
back together. The work is the same for every input order, so the running
time is Theta(n lg n) in the best, average, and worst cases.
"""


def merge(arr, first, middle, last):
    """Merge the sorted runs arr[first..middle] and arr[middle+1..last].

    Both runs are copied into temporary lists first, which is where Merge
    Sort's Theta(n) extra memory comes from.
    """
    left_run = arr[first:middle + 1]
    right_run = arr[middle + 1:last + 1]
    li = ri = 0
    out = first
    # Repeatedly copy the smaller front item back into arr. Using <= keeps
    # equal items in their original order, so the sort is stable.
    while li < len(left_run) and ri < len(right_run):
        if left_run[li] <= right_run[ri]:
            arr[out] = left_run[li]
            li += 1
        else:
            arr[out] = right_run[ri]
            ri += 1
        out += 1
    # One run is used up; copy whatever is left of the other one.
    while li < len(left_run):
        arr[out] = left_run[li]
        li += 1
        out += 1
    while ri < len(right_run):
        arr[out] = right_run[ri]
        ri += 1
        out += 1


def _merge_sort(arr, first, last):
    # Divide: a run of 0 or 1 items is already sorted (the base case).
    if first >= last:
        return
    middle = (first + last) // 2
    # Conquer: sort each half recursively.
    _merge_sort(arr, first, middle)
    _merge_sort(arr, middle + 1, last)
    # Combine: merge the two sorted halves in linear time.
    merge(arr, first, middle, last)


def merge_sort(arr):
    """Sort ``arr`` in place from smallest to largest and return it.

    Recurrence: T(n) = 2T(n/2) + Theta(n), which solves to Theta(n lg n).
    """
    _merge_sort(arr, 0, len(arr) - 1)
    return arr


if __name__ == "__main__":
    sample = [41, 17, 93, 5, 62, 28, 74, 50]
    print("Before sorting:", sample)
    merge_sort(sample)
    print("After sorting:", sample)
