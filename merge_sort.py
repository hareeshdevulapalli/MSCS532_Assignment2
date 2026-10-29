"""Merge Sort.

This module follows the MERGE-SORT and MERGE procedures from Chapter 2 of
Introduction to Algorithms (Cormen et al., 4th ed.). The list is split in
half, each half is sorted recursively, and the two sorted halves are merged
back together. The work is the same for every input order, so the running
time is Theta(n lg n) in the best, average, and worst cases.
"""


def merge(values, low, mid, high):
    """Merge the sorted runs values[low..mid] and values[mid+1..high].

    Both runs are copied into temporary lists first, which is where Merge
    Sort's Theta(n) extra memory comes from.
    """
    left = values[low:mid + 1]
    right = values[mid + 1:high + 1]
    i = j = 0
    k = low
    # Repeatedly copy the smaller front item back into values. Using <= keeps
    # equal items in their original order, so the sort is stable.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            values[k] = left[i]
            i += 1
        else:
            values[k] = right[j]
            j += 1
        k += 1
    # One run is used up; copy whatever is left of the other one.
    while i < len(left):
        values[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        values[k] = right[j]
        j += 1
        k += 1


def _merge_sort(values, low, high):
    # Divide: a run of 0 or 1 items is already sorted (the base case).
    if low >= high:
        return
    mid = (low + high) // 2
    # Conquer: sort each half recursively.
    _merge_sort(values, low, mid)
    _merge_sort(values, mid + 1, high)
    # Combine: merge the two sorted halves in linear time.
    merge(values, low, mid, high)


def merge_sort(values):
    """Sort ``values`` in place from smallest to largest and return it.

    Recurrence: T(n) = 2T(n/2) + Theta(n), which solves to Theta(n lg n).
    """
    _merge_sort(values, 0, len(values) - 1)
    return values


if __name__ == "__main__":
    numbers = [41, 17, 93, 5, 62, 28, 74, 50]
    print("Before sorting:", numbers)
    merge_sort(numbers)
    print("After sorting:", numbers)
