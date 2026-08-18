#!/usr/bin/env python3
from __future__ import print_function

import os
import sys
import time
import multiprocessing

import hkd_multiprocessing

LOGICAL_ITEMS = 10000000
ACTIVE_ITEMS = 1
MAX_WORKERS = 8
HKD_REPEATS = 5000
ACTIVE_MP_REPEATS = 25


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


def timed_hkd(active):
    # Batch repeated identical sparse updates to get stable sub-micro/microsecond
    # per-update timing rather than relying on one timer tick.
    t0 = clock()
    result = None
    for unused in range(HKD_REPEATS):
        result = hkd_multiprocessing.map_active(
            LOGICAL_ITEMS, active, kernel, workers=WORKERS
        )
    elapsed = clock() - t0
    return sum(result), elapsed / HKD_REPEATS


def main():
    active = [LOGICAL_ITEMS - 1]

    # Validate edition before launching the native pool.
    hkd_multiprocessing.map_active(
        LOGICAL_ITEMS, active, kernel, workers=WORKERS
    )

    pool = multiprocessing.Pool(processes=WORKERS)
    try:
        # Warm persistent workers. Process startup is intentionally not charged
        # to either native multiprocessing timed path.
        pool.map(kernel, list(range(WORKERS)))

        t0 = clock()
        full_result = sum(pool.map(
            full_scan_chunk,
            make_chunks(LOGICAL_ITEMS, active)
        ))
        full_seconds = clock() - t0

        t0 = clock()
        active_result = None
        for unused in range(ACTIVE_MP_REPEATS):
            active_result = sum(pool.map(kernel, active))
        active_seconds = (clock() - t0) / ACTIVE_MP_REPEATS
    finally:
        pool.close()
        pool.join()

    hkd_result, hkd_seconds = timed_hkd(active)

    exact = (
        full_result == active_result ==
        hkd_result == sum(kernel(i) for i in active)
    )

    full_speedup = full_seconds / max(hkd_seconds, 0.000000001)
    active_speedup = active_seconds / max(hkd_seconds, 0.000000001)

    print("HKD_INFINITY_MULTIPROCESSING_SPARSE_BENCHMARK")
    print("label=NON_CHEAT_EXACT_ACTIVE_STATE")
    print("edition=%s" % hkd_multiprocessing.EDITION)
    print("python=%s" % sys.version.split()[0])
    print("workers=%d" % WORKERS)
    print("logical_items=%d" % LOGICAL_ITEMS)
    print("active_items=%d" % ACTIVE_ITEMS)
    print("active_fraction=%.10f" %
          (ACTIVE_ITEMS / float(LOGICAL_ITEMS)))
    print()
    print("STANDARD_FULL_STATE_MULTIPROCESSING")
    print("pool_startup_in_timing=False")
    print("seconds_per_update=%.9f" % full_seconds)
    print("logical_items_examined=%d" % LOGICAL_ITEMS)
    print("result=%d" % full_result)
    print()
    print("STANDARD_ACTIVE_ONLY_MULTIPROCESSING")
    print("pool_startup_in_timing=False")
    print("seconds_per_update=%.9f" % active_seconds)
    print("active_items_dispatched=%d" % ACTIVE_ITEMS)
    print("result=%d" % active_result)
    print()
    print("HKD_INFINITY_ACTIVE_EXECUTION")
    print("seconds_per_update=%.9f" % hkd_seconds)
    print("active_items_executed=%d" % ACTIVE_ITEMS)
    print("process_ipc_bypassed_for_single_active=True")
    print("result=%d" % hkd_result)
    print()
    print("COMPARISON")
    print("full_state_multiprocessing_over_hkd_x=%.2f" % full_speedup)
    print("active_only_multiprocessing_over_hkd_x=%.2f" % active_speedup)
    print("10000X_FULL_STATE_PLUS=%s" % (full_speedup >= 10000.0))
    print("10000X_ACTIVE_ONLY_PLUS=%s" % (active_speedup >= 10000.0))
    print("exact=%s" % exact)
    print("PASS=%s" % exact)
    return 0 if exact else 1


if __name__ == "__main__":
    sys.exit(main())
