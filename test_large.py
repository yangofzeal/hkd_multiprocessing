#!/usr/bin/env python3
from __future__ import print_function

import os
import sys
import time
import multiprocessing

import hkd_multiprocessing

LOGICAL_ITEMS = 100000000
ACTIVE_ITEMS = 1
MAX_WORKERS = 8
HKD_REPEATS = 5000


def clock():
    fn = getattr(time, "perf_counter", None)
    if fn is not None:
        return fn()
    return time.time()


def cpu_count():
    count = os.cpu_count()
    if count is None:
        return 4
    return max(1, int(count))


WORKERS = min(MAX_WORKERS, cpu_count())


def kernel(i):
    x = (i * 2654435761) & 0xffffffff
    x ^= (x >> 13)
    x = (x * 2246822519) & 0xffffffff
    return x & 0xffff


def full_scan_chunk(args):
    start, stop, active_indices = args
    active_set = set(active_indices)
    total = 0
    for i in range(start, stop):
        if i in active_set:
            total += kernel(i)
    return total


def make_chunks(logical_items, active_indices):
    width = (logical_items + WORKERS - 1) // WORKERS
    out = []
    start = 0
    while start < logical_items:
        stop = min(logical_items, start + width)
        out.append((start, stop, active_indices))
        start = stop
    return out


def main():
    active = [LOGICAL_ITEMS - 1]

    print("HKD_INFINITY_MULTIPROCESSING_LARGE_TEST")
    print("edition=%s" % hkd_multiprocessing.EDITION)
    print("requested_logical_items=%d" % LOGICAL_ITEMS)
    print("requested_active_items=%d" % ACTIVE_ITEMS)
    print("free_max_logical_items=%s" %
          hkd_multiprocessing.FREE_MAX_LOGICAL_ITEMS)
    print("free_max_active_items=%s" %
          hkd_multiprocessing.FREE_MAX_ACTIVE_ITEMS)

    try:
        hkd_multiprocessing.map_active(
            LOGICAL_ITEMS, active, kernel, workers=WORKERS
        )
    except hkd_multiprocessing.HKDMultiprocessingLimitError as exc:
        if hkd_multiprocessing.EDITION == "FREE":
            print("FREE_LIMIT_TRIGGERED=True")
            print("error=%s" % exc)
            print("PASS=True")
            return 0
        print("PASS=False")
        print("error=unlimited edition unexpectedly rejected workload")
        return 1

    if hkd_multiprocessing.EDITION == "FREE":
        print("FREE_LIMIT_TRIGGERED=False")
        print("PASS=False")
        return 1

    pool = multiprocessing.Pool(processes=WORKERS)
    try:
        pool.map(kernel, list(range(WORKERS)))
        t0 = clock()
        native_result = sum(pool.map(
            full_scan_chunk,
            make_chunks(LOGICAL_ITEMS, active)
        ))
        native_seconds = clock() - t0
    finally:
        pool.close()
        pool.join()

    t0 = clock()
    hkd_result = None
    for unused in range(HKD_REPEATS):
        hkd_result = sum(hkd_multiprocessing.map_active(
            LOGICAL_ITEMS, active, kernel, workers=WORKERS
        ))
    hkd_seconds = (clock() - t0) / HKD_REPEATS

    expected = sum(kernel(i) for i in active)
    exact = native_result == hkd_result == expected
    speedup = native_seconds / max(hkd_seconds, 0.000000001)

    print()
    print("STANDARD_FULL_STATE_MULTIPROCESSING")
    print("seconds_per_update=%.9f" % native_seconds)
    print("logical_items_examined=%d" % LOGICAL_ITEMS)
    print("result=%d" % native_result)
    print()
    print("HKD_INFINITY_ACTIVE_EXECUTION")
    print("seconds_per_update=%.9f" % hkd_seconds)
    print("active_items_executed=%d" % ACTIVE_ITEMS)
    print("result=%d" % hkd_result)
    print()
    print("COMPARISON")
    print("full_state_multiprocessing_over_hkd_x=%.2f" % speedup)
    print("10000X_FULL_STATE_PLUS=%s" % (speedup >= 10000.0))
    print("exact=%s" % exact)
    print("PASS=%s" % exact)
    return 0 if exact else 1


if __name__ == "__main__":
    sys.exit(main())
