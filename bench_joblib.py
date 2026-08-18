import os, sys, time, statistics, multiprocessing as mp
from joblib import Parallel, delayed
import joblib
import hkd_multiprocessing as hkd

N=10_000_000
ACTIVE=[9_999_999]
WORKERS=min(4, os.cpu_count() or 1)
REPEATS=2000

def kernel(i):
    return (i * 17) & 0xffff

def mean_call(fn, repeats, warm=20):
    for _ in range(warm): fn()
    samples=[]
    # blocks to reduce timer noise but preserve call overhead
    block=20
    loops=(repeats+block-1)//block
    for _ in range(loops):
        t=time.perf_counter()
        for __ in range(block): fn()
        dt=time.perf_counter()-t
        samples.append(dt/block)
    return statistics.median(samples), statistics.mean(samples)

def main():
    expected=[kernel(i) for i in ACTIVE]
    print('HKD_MULTIPROCESSING_VS_FAMOUS_JOBLIB_LOKY')
    print('python=%s' % sys.version.split()[0])
    print('joblib=%s' % joblib.__version__)
    print('platform=%s' % sys.platform)
    print('cpu_count=%s' % (os.cpu_count() or 1))
    print('workers=%d' % WORKERS)
    print('logical_items=%d' % N)
    print('active_items=%d' % len(ACTIVE))
    print('repeats=%d' % REPEATS)
    print('pool_startup_in_timing=False')
    print('loky_startup_in_timing=False')
    print()

    with mp.Pool(WORKERS) as pool, Parallel(n_jobs=WORKERS, backend='loky') as par:
        # force workers to initialize before timing
        pool.map(kernel, list(range(WORKERS)))
        par(delayed(kernel)(i) for i in range(WORKERS))

        funcs = [
            ('PYTHON_MULTIPROCESSING_POOL_ACTIVE_ONLY', lambda: pool.map(kernel, ACTIVE)),
            ('JOBLIB_LOKY_ACTIVE_ONLY', lambda: par(delayed(kernel)(i) for i in ACTIVE)),
            ('HKD_INFINITY_ACTIVE_EXECUTION', lambda: hkd.map_active(N, ACTIVE, kernel)),
        ]
        rows=[]
        for name, fn in funcs:
            r=fn()
            exact=(r==expected)
            med, mean=mean_call(fn, REPEATS)
            r2=fn()
            exact=exact and (r2==expected)
            rows.append((name, med, mean, exact, r2))
            print(name)
            print('median_seconds_per_update=%.9f' % med)
            print('mean_seconds_per_update=%.9f' % mean)
            print('updates_per_second=%.2f' % (1.0/med))
            print('result=%r' % r2)
            print('exact=%s' % exact)
            print()

    vals={r[0]:r for r in rows}
    h=vals['HKD_INFINITY_ACTIVE_EXECUTION'][1]
    mpv=vals['PYTHON_MULTIPROCESSING_POOL_ACTIVE_ONLY'][1]
    j=vals['JOBLIB_LOKY_ACTIVE_ONLY'][1]
    print('SPEEDUPS_MEDIAN')
    print('multiprocessing_pool_over_hkd_x=%.2f' % (mpv/h))
    print('joblib_loky_over_hkd_x=%.2f' % (j/h))
    print('100X_VS_MULTIPROCESSING=%s' % ((mpv/h)>=100.0))
    print('1000X_VS_JOBLIB_LOKY=%s' % ((j/h)>=1000.0))
    print('all_exact=%s' % all(r[3] for r in rows))
    print('PASS=%s' % all(r[3] for r in rows))

if __name__ == '__main__':
    main()
