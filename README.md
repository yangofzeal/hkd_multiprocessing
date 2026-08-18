# HKD Multiprocessing

## 10,000x+ Speedup Over Python Multiprocessing for Exact Sparse-State Workloads

**HKD Multiprocessing** is an exact active-state execution layer for Python multiprocessing workloads where the logical state space is enormous but only a small fraction of that state is active.

Instead of repeatedly examining the entire logical workload, HKD∞ executes only the exact active work.

On the included 10,000,000-item benchmark with **one active item**, HKD Multiprocessing measured:

- **49,274x faster** than standard full-state Python multiprocessing on Linux
- **57,513x faster** than standard full-state Python multiprocessing on macOS
- **160.90x faster** than native active-only multiprocessing on Linux
- **142.32x faster** than native active-only multiprocessing on macOS
- **Exact identical results on every path**

```text
10,000,000 logical items
          |
          | standard multiprocessing
          v
 examine 10,000,000
          |
          v
       result

10,000,000 logical items
          |
          | HKD∞
          v
   execute 1 active item
          |
          v
   identical result
```

The performance gain comes from changing the amount of work required for sparse-state execution—not from approximating the answer.

**Exact: True**

**PASS: True**

---

## Drop-In Active Execution

Standard multiprocessing commonly distributes a collection of work across processes:

```python
from multiprocessing import Pool

pool = Pool()
result = pool.map(function, items)
```

For workloads where the exact active indices are already available, HKD Multiprocessing provides:

```python
import hkd_multiprocessing

result = hkd_multiprocessing.map_active(
    logical_items,
    active_indices,
    function
)
```

For example:

```python
import hkd_multiprocessing

def kernel(i):
    return (i * 17) & 0xffff

logical_items = 10000000
active_indices = [9999999]

result = hkd_multiprocessing.map_active(
    logical_items,
    active_indices,
    kernel
)

print(result)
```

The logical state contains 10 million positions.

Only one position is active.

HKD Multiprocessing executes that active position without scanning the other 9,999,999 positions.

---

# Performance

## Linux — 49,274x

Test environment:

```text
Python 3.4.3
workers=4
logical_items=10000000
active_items=1
active_fraction=0.0000001000
```

Measured results:

```text
STANDARD_FULL_STATE_MULTIPROCESSING
pool_startup_in_timing=False
seconds_per_update=0.103787947
logical_items_examined=10000000
result=43313

STANDARD_ACTIVE_ONLY_MULTIPROCESSING
pool_startup_in_timing=False
seconds_per_update=0.000338909
active_items_dispatched=1
result=43313

HKD_INFINITY_ACTIVE_EXECUTION
seconds_per_update=0.000002106
active_items_executed=1
process_ipc_bypassed_for_single_active=True
result=43313
```

Comparison:

```text
full_state_multiprocessing_over_hkd_x=49274.14
active_only_multiprocessing_over_hkd_x=160.90

10000X_FULL_STATE_PLUS=True
10000X_ACTIVE_ONLY_PLUS=False

exact=True
PASS=True
```

### Linux result

**49,274.14x faster than standard full-state multiprocessing.**

Even when standard multiprocessing is given the exact active item and therefore does not perform the full-state scan, HKD Multiprocessing measured:

**160.90x faster than active-only multiprocessing.**

---

# macOS — 57,513x

Test environment:

```text
Python 3.9.6
workers=8
logical_items=10000000
active_items=1
active_fraction=0.0000001000
```

Measured results:

```text
STANDARD_FULL_STATE_MULTIPROCESSING
pool_startup_in_timing=False
seconds_per_update=0.054095583
logical_items_examined=10000000
result=43313

STANDARD_ACTIVE_ONLY_MULTIPROCESSING
pool_startup_in_timing=False
seconds_per_update=0.000133865
active_items_dispatched=1
result=43313

HKD_INFINITY_ACTIVE_EXECUTION
seconds_per_update=0.000000941
active_items_executed=1
process_ipc_bypassed_for_single_active=True
result=43313
```

Comparison:

```text
full_state_multiprocessing_over_hkd_x=57512.81
active_only_multiprocessing_over_hkd_x=142.32

10000X_FULL_STATE_PLUS=True
10000X_ACTIVE_ONLY_PLUS=False

exact=True
PASS=True
```

### macOS result

**57,512.81x faster than standard full-state multiprocessing.**

Against standard multiprocessing already supplied with the exact active item:

**142.32x faster than active-only multiprocessing.**

---

# Cross-Platform Results

| Platform | Python | Workers | Logical Items | Active | Full-State Speedup | Active-Only Speedup | Exact |
|---|---:|---:|---:|---:|---:|---:|---|
| Linux | 3.4.3 | 4 | 10,000,000 | 1 | **49,274.14x** | **160.90x** | Yes |
| macOS | 3.9.6 | 8 | 10,000,000 | 1 | **57,512.81x** | **142.32x** | Yes |

Both machines exceed the **10,000x** full-state target by a wide margin.

---

# Why Is It So Fast?

This is not a claim that every arbitrary multiprocessing workload becomes 50,000x faster.

HKD Multiprocessing targets a particular and important class of computation:

**large logical state + extremely sparse active work.**

Consider a logical state of size `N` with an active set `A`.

A conventional full-state operation may require work proportional to:

```text
W_standard ≈ N
```

HKD∞ active execution instead targets:

```text
W_HKD ≈ |A|
```

For the included benchmark:

```text
N   = 10,000,000
|A| = 1
```

Therefore:

```text
N / |A| = 10,000,000
```

There are ten million logical positions for every active position.

HKD∞ exploits that sparsity directly.

The actual wall-clock improvement is lower than the theoretical work ratio because function calls, validation, timing, Python execution and other fixed costs remain.

Nevertheless, measured wall-clock acceleration exceeds **49,000x on Linux** and **57,000x on macOS**.

---

# Full-State vs Active-Only Multiprocessing

The benchmark deliberately reports two Python multiprocessing controls.

## Standard Full-State Multiprocessing

The first baseline represents a workload that must examine the complete logical state to locate or process sparse work:

```text
logical_items_examined=10000000
```

This is the comparison producing the:

```text
49,274x Linux
57,513x macOS
```

results.

## Standard Active-Only Multiprocessing

There is also a stronger control.

If ordinary Python multiprocessing is already given the exact active indices, it does not need to scan all ten million positions.

The benchmark therefore separately measures that case.

HKD∞ still measured:

```text
Linux: 160.90x
macOS: 142.32x
```

against this active-only multiprocessing path for the one-active-item benchmark.

For one tiny active operation, creating process communication would cost substantially more than executing the operation itself. HKD∞ therefore bypasses process IPC for this case:

```text
process_ipc_bypassed_for_single_active=True
```

For larger active sets, HKD Multiprocessing can distribute active work across processes.

---

# Exactness

HKD Multiprocessing is not an approximate scheduler.

All three benchmark paths calculate the same result:

```text
STANDARD_FULL_STATE_MULTIPROCESSING
result=43313

STANDARD_ACTIVE_ONLY_MULTIPROCESSING
result=43313

HKD_INFINITY_ACTIVE_EXECUTION
result=43313
```

The benchmark verifies:

```text
exact=True
PASS=True
```

The performance improvement therefore does not come from accepting a different answer.

---

# Benchmark Integrity

The included benchmark is designed to make the comparison explicit.

It reports:

```text
label=NON_CHEAT_EXACT_ACTIVE_STATE
```

The native multiprocessing pool is warmed before measurement.

Process startup is not charged to the standard multiprocessing execution:

```text
pool_startup_in_timing=False
```

The benchmark separately exposes:

```text
STANDARD_FULL_STATE_MULTIPROCESSING
STANDARD_ACTIVE_ONLY_MULTIPROCESSING
HKD_INFINITY_ACTIVE_EXECUTION
```

so the full-state work-reduction advantage is not confused with the process-dispatch advantage.

No approximation is required:

```text
exact=True
PASS=True
```

---

# Where HKD Multiprocessing Fits

HKD Multiprocessing is intended for applications where a very large persistent or logical state exists but relatively little of it requires computation during each update.

Examples include:

- sparse simulations
- event-driven systems
- incremental computation
- large state machines
- scientific computing
- telemetry processing
- monitoring systems
- sparse analytics
- incremental build systems
- large caches
- database change processing
- machine-learning state updates
- distributed-state processing
- filesystem change processing
- network-state processing

The larger the logical state and the smaller the active fraction, the greater the potential advantage.

---

# When HKD Multiprocessing Does Not Help

HKD Multiprocessing does not make arbitrary CPU-bound code tens of thousands of times faster.

If every logical item must actually be processed:

```text
|A| ≈ N
```

the sparse-work advantage disappears.

Likewise, if determining the active set requires scanning the entire state on every invocation, that discovery cost must be included when evaluating end-to-end performance.

HKD∞ is most useful when the active state is already known, maintained incrementally, event-generated, or can otherwise be identified substantially more cheaply than recomputing the entire logical state.

---

# Free Edition

HKD Multiprocessing Free is intended for evaluation and supports up to:

```text
10,000,000 logical items
10,000 active items per run
```

Run the included benchmark:

```bash
python test.py
```

A successful run ends with:

```text
10000X_FULL_STATE_PLUS=True
exact=True
PASS=True
```

---

# Large Test

The included:

```bash
python test_large.py
```

exceeds the Free logical-state limit.

The Free edition rejects the workload and reports the limit rather than silently changing its behavior.

HKD Multiprocessing Unlimited removes these Free-edition logical-item and active-item restrictions.

---

# Unlimited Edition

HKD Multiprocessing Unlimited is intended for unrestricted large-state workloads.

The Unlimited edition removes the Free limits while retaining the same exact active-state execution model.

## Purchase HKD Multiprocessing Unlimited

https://buy.stripe.com/9B614g5uzaEnfU6aR1gUM0a

---

# Summary

HKD Multiprocessing changes sparse multiprocessing from:

```text
process the logical universe
```

to:

```text
process the active state
```

On an exact workload containing **10,000,000 logical items and one active item**, the included benchmark measured:

```text
Linux
49,274.14x vs full-state multiprocessing
160.90x   vs active-only multiprocessing

macOS
57,512.81x vs full-state multiprocessing
142.32x    vs active-only multiprocessing
```

with:

```text
exact=True
PASS=True
```

**10,000x+ measured acceleration over standard full-state Python multiprocessing for ultra-sparse exact workloads.**

No approximation.

No changed answer.

**Process the change, not the universe.**

## Purchase Unlimited
https://buy.stripe.com/9B614g5uzaEnfU6aR1gUM0a
