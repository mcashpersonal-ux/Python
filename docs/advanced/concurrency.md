# 20 — Concurrency

> Threads and processes run code in parallel. Threads share
> memory(handy,race-risky); processes have separate memory(
> safer, heavier). Pick the tool that matches the workload.

---

## threads- basics

```python
import threading
import time

def work(name):
    time.sleep(1)
    print(name, "done")

t1 = threading.Thread(target=work, args=("a",))
t2 = threading.Thread(target=work, args=("b",))
t1.start()
t2.start()
t1.join()
t2.join()
print("all done")
```

Thread runs target in a new thread. start() launches; join()
waits for it. Without join, main exits early, hatten possibly
mid-print. Two sleeps overlap- total ~1s.

---

## thread pool- ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor
import time

def work(n):
    time.sleep(1)
    return n * n

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(work, range(4)))
print(results) # [0,1,4,9]
```

Pool reuses threads- cheap for many small tasks. .map()
collects results in order; .submit()/future.result() for
fire-and-collect-later. Context manager joins on exit.

---

## processes- ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor

def square(n):
    return n * n

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(square, range(4)))
    print(results)
```

Processes dodge the GIL- real parallelism for CPU-bound
work. Pickling limits args-and results to serializable values,
and the worker must be importable- hence __main__ guard.

---

## process- multiprocessing basics

```python
import multiprocessing

def worker(q):
    q.put("hello")

if __name__ == "__main__":
    ctx = multiprocessing.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=worker, args=(q,))
    p.start()
    p.join()
    print(q.get())
```

multiprocessing spawns fresh interpreters- safe on all OS.
The Queue passes values across processes. Always guard with
if __name__ == "__main__" or Windows will re-importthe module.

---

## locks- protect shared state

```python
import threading

count = 0
lock = threading.Lock()

def bump():
    global count
    for _ in range(1_000_000):
        with lock:
            count += 1

t1 = threading.Thread(target=bump)
t2 = threading.Thread(target=bump)
t1.start()
t2.start()
t1.join()
t2.join()
print(count) # 2000000
```

Without a lock, the += races- you can lose updates. with
lock: guarantees atomic read-modify-write. Rule: keep critical
sections tiny.

---

## queues- thread-safe communication

```python
import threading
import queue
import time

q = queue.Queue()

def producer(q):
    for i in range(5):
        q.put(i)
    q.put(None)

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(item, end=" ")

t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))
t1.start()
t2.start()
t1.join()
t2.join()
print()
```

queue.Queue is thread-safe - no locking is needed to enqueue/
dequeue. None sentinel ends the consumer. Two threads,one
serialized handoff channel.

---

## Next steps

go to Performance & Profiling at advanced/performance.md
