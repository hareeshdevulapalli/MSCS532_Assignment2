"""Unit tests for merge_sort, quick_sort, and randomized_quick_sort."""

import random
import unittest

from merge_sort import merge_sort
from quick_sort import quick_sort, randomized_quick_sort

SORTS = [merge_sort, quick_sort, randomized_quick_sort]


class SortTests(unittest.TestCase):
    def check(self, data):
        for sort in SORTS:
            with self.subTest(sort=sort.__name__, data=data[:10]):
                copy = list(data)
                result = sort(copy)
                self.assertIs(result, copy)  # sorted in place
                self.assertEqual(copy, sorted(data))

    def test_empty_and_single(self):
        self.check([])
        self.check([42])

    def test_small_examples(self):
        self.check([19, 64, 7, 88, 33, 51, 12, 45])
        self.check([41, 17, 93, 5, 62, 28, 74, 50])

    def test_sorted_and_reverse(self):
        self.check(list(range(500)))
        self.check(list(range(500, 0, -1)))

    def test_duplicates_and_negatives(self):
        self.check([3, -1, 3, 0, -1, 3, 2, 2, -5])
        self.check([7] * 50)

    def test_random(self):
        rng = random.Random(532)
        for size in (2, 3, 10, 101, 1000):
            self.check([rng.randint(-1000, 1000) for _ in range(size)])

    def test_merge_sort_is_stable(self):
        pairs = [(1, "a"), (0, "b"), (1, "c"), (0, "d")]

        class Key:
            def __init__(self, pair):
                self.pair = pair

            def __le__(self, other):
                return self.pair[0] <= other.pair[0]

        items = [Key(p) for p in pairs]
        merge_sort(items)
        self.assertEqual([k.pair for k in items],
                         [(0, "b"), (0, "d"), (1, "a"), (1, "c")])


if __name__ == "__main__":
    unittest.main()
