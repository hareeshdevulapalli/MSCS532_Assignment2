"""Time and memory benchmark for Merge Sort and Quick Sort.

Each algorithm is run on sorted, reverse-sorted, and random lists of several
sizes. Execution time is the median of several runs measured with
time.perf_counter. Peak extra memory is measured in a separate run with
tracemalloc, since tracing slows the code down and would distort the timings.

Results are written to results/results.csv and plotted to results/*.png.

    python3 benchmark.py            # full run (sizes up to 8000)
    python3 benchmark.py --quick    # small sizes, for a fast check
"""

import argparse
import csv
import os
import random
import statistics
import sys
import time
import tracemalloc

from merge_sort import merge_sort
from quick_sort import quick_sort, randomized_quick_sort

ALGORITHMS = {
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Randomized Quick Sort": randomized_quick_sort,
}
DATASETS = ["sorted", "reverse", "random"]
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def make_data(kind, n, rng):
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    return [rng.randint(0, 10 * n) for _ in range(n)]


def time_sort(sort, data, repeats):
    """Return the median wall-clock time in milliseconds over ``repeats`` runs."""
    times = []
    for _ in range(repeats):
        copy = list(data)  # every run gets a fresh, unsorted copy
        start = time.perf_counter()
        sort(copy)
        times.append((time.perf_counter() - start) * 1000)
    assert copy == sorted(data)
    return statistics.median(times)


def peak_memory(sort, data):
    """Return the peak memory in KiB allocated while sorting a copy of data."""
    copy = list(data)
    tracemalloc.start()
    sort(copy)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024


def run(sizes, repeats):
    rng = random.Random(532)  # fixed seed so the random lists are repeatable
    rows = []
    for kind in DATASETS:
        for n in sizes:
            data = make_data(kind, n, rng)
            for name, sort in ALGORITHMS.items():
                ms = time_sort(sort, data, repeats)
                kib = peak_memory(sort, data)
                rows.append({"algorithm": name, "dataset": kind, "n": n,
                             "time_ms": round(ms, 3), "peak_kib": round(kib, 1)})
                print(f"{kind:>8} n={n:>6} {name:<22} "
                      f"{ms:10.2f} ms {kib:9.1f} KiB", flush=True)
    return rows


def save_csv(rows, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    styles = {"Merge Sort": ("#1f77b4", "o"), "Quick Sort": ("#d62728", "s"),
              "Randomized Quick Sort": ("#2ca02c", "^")}

    for metric, label, filename in [
            ("time_ms", "Execution time (ms)", "time.png"),
            ("peak_kib", "Peak extra memory (KiB)", "memory.png")]:
        fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
        for ax, kind in zip(axes, DATASETS):
            for name, (color, marker) in styles.items():
                pts = [(r["n"], r[metric]) for r in rows
                       if r["algorithm"] == name and r["dataset"] == kind]
                ax.plot(*zip(*pts), marker=marker, color=color, label=name)
            ax.set_title(f"{kind.capitalize()} input")
            ax.set_xlabel("n (list size)")
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.grid(True, which="both", alpha=0.3)
        axes[0].set_ylabel(label)
        axes[0].legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(os.path.join(RESULTS_DIR, filename), dpi=200)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--quick", action="store_true",
                        help="use small sizes for a fast check")
    args = parser.parse_args()
    sizes = [100, 200, 400] if args.quick else [500, 1000, 2000, 4000, 8000]
    repeats = 3 if args.quick else 5

    print(f"Python {sys.version.split()[0]}, sizes={sizes}, repeats={repeats}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows = run(sizes, repeats)
    save_csv(rows, os.path.join(RESULTS_DIR, "results.csv"))
    plot(rows)
    print(f"Saved results and graphs to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
