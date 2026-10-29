"""Quick Sort.

This module follows the QUICKSORT and PARTITION procedures from Chapter 7 of
Introduction to Algorithms (Cormen et al., 4th ed.). PARTITION uses the
Lomuto scheme with the last item as the pivot, exactly as in the book. That
choice is what makes already-sorted and reverse-sorted input the worst case:
every partition is as lopsided as possible, giving Theta(n^2) time.

A randomized variant (RANDOMIZED-QUICKSORT, Section 7.3) is also provided. It
swaps a randomly chosen item into the pivot slot first, so no fixed input
order can trigger the worst case and the expected time is O(n lg n).
"""

import random


def partition(arr, first, last):
    """Partition arr[first..last] around the pivot arr[last].

    Returns the pivot's final index. Afterwards every item to its left is
    <= the pivot and every item to its right is greater than it.
    """
    pivot = arr[last]
    # Invariant: arr[first..small_end] holds the items found so far that are
    # <= pivot; arr[small_end+1..idx-1] holds the items that are > pivot.
    small_end = first - 1
    for idx in range(first, last):
        if arr[idx] <= pivot:
            small_end += 1
            arr[small_end], arr[idx] = arr[idx], arr[small_end]
    # Drop the pivot between the two groups.
    arr[small_end + 1], arr[last] = arr[last], arr[small_end + 1]
    return small_end + 1


def _quick_sort(arr, first, last, randomized):
    # Recurse into the smaller side and loop on the larger one. The book's
    # version recurses into both sides; this keeps the call stack at
    # O(lg n) depth so that the Theta(n^2) worst case on sorted input can be
    # measured without hitting Python's recursion limit. The number of
    # comparisons, and so the running time, is unchanged.
    while first < last:
        if randomized:
            rand_idx = random.randint(first, last)
            arr[rand_idx], arr[last] = arr[last], arr[rand_idx]
        # Divide: split around the pivot. Combine is free: once both sides
        # are sorted the whole range is sorted.
        split = partition(arr, first, last)
        if split - first < last - split:
            _quick_sort(arr, first, split - 1, randomized)
            first = split + 1
        else:
            _quick_sort(arr, split + 1, last, randomized)
            last = split - 1


def quick_sort(arr):
    """Sort ``arr`` in place with last-item pivots and return it.

    Recurrences: worst case T(n) = T(n-1) + Theta(n) = Theta(n^2);
    best case T(n) = 2T(n/2) + Theta(n) = Theta(n lg n).
    """
    _quick_sort(arr, 0, len(arr) - 1, randomized=False)
    return arr


def randomized_quick_sort(arr):
    """Sort ``arr`` in place with random pivots and return it."""
    _quick_sort(arr, 0, len(arr) - 1, randomized=True)
    return arr


if __name__ == "__main__":
    sample = [19, 64, 7, 88, 33, 51, 12, 45]
    print("Before sorting:", sample)
    quick_sort(sample)
    print("After sorting:", sample)
