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


def partition(values, low, high):
    """Partition values[low..high] around the pivot values[high].

    Returns the pivot's final index q. Afterwards every item in
    values[low..q-1] is <= the pivot and every item in values[q+1..high] is
    greater than it.
    """
    pivot = values[high]
    # Invariant: values[low..boundary] holds the items found so far that are
    # <= pivot; values[boundary+1..scan-1] holds the items that are > pivot.
    boundary = low - 1
    for scan in range(low, high):
        if values[scan] <= pivot:
            boundary += 1
            values[boundary], values[scan] = values[scan], values[boundary]
    # Drop the pivot between the two groups.
    values[boundary + 1], values[high] = values[high], values[boundary + 1]
    return boundary + 1


def _quick_sort(values, low, high, randomized):
    # Recurse into the smaller side and loop on the larger one. The book's
    # version recurses into both sides; this keeps the call stack at
    # O(lg n) depth so that the Theta(n^2) worst case on sorted input can be
    # measured without hitting Python's recursion limit. The number of
    # comparisons, and so the running time, is unchanged.
    while low < high:
        if randomized:
            pick = random.randint(low, high)
            values[pick], values[high] = values[high], values[pick]
        # Divide: split around the pivot. Combine is free: once both sides
        # are sorted the whole range is sorted.
        q = partition(values, low, high)
        if q - low < high - q:
            _quick_sort(values, low, q - 1, randomized)
            low = q + 1
        else:
            _quick_sort(values, q + 1, high, randomized)
            high = q - 1


def quick_sort(values):
    """Sort ``values`` in place with last-item pivots and return it.

    Recurrences: worst case T(n) = T(n-1) + Theta(n) = Theta(n^2);
    best case T(n) = 2T(n/2) + Theta(n) = Theta(n lg n).
    """
    _quick_sort(values, 0, len(values) - 1, randomized=False)
    return values


def randomized_quick_sort(values):
    """Sort ``values`` in place with random pivots and return it."""
    _quick_sort(values, 0, len(values) - 1, randomized=True)
    return values


if __name__ == "__main__":
    numbers = [19, 64, 7, 88, 33, 51, 12, 45]
    print("Before sorting:", numbers)
    quick_sort(numbers)
    print("After sorting:", numbers)
